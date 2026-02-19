# app/services/video_processor.py
# Optimized for GPU with PyTorch model

import cv2
import json
import asyncio
import logging
import torch
from pathlib import Path
from datetime import datetime
from collections import defaultdict, deque
from fastapi import HTTPException
from ultralytics import YOLO
from concurrent.futures import ThreadPoolExecutor

from app.ws.websocket_manager import manager
from app.core.storage import processing_status, detection_results, RESULTS_DIR, update_global_map
from app.services.satellite_sentinel import satellite_sentinel
from typing import Dict

logger = logging.getLogger(__name__)

class LagosTrafficMitigator:
    """Nuanced Mitigation Engine for Lagos Infrastructure Resilience"""
    
    @staticmethod
    def generate_mitigation_plan(results: Dict):
        """Analyze results and suggest traffic diversions for Lagos State"""
        urgency = results.get("urgency_score", 0)
        severity_counts = results.get("summary", {}).get("severity_breakdown", {})
        
        plan = {
            "status": "DORMANT",
            "suggested_actions": [],
            "lastma_alert": False,
            "dispatch_priority": "LOW"
        }
        
        if urgency > 75 or severity_counts.get("CRITICAL", 0) > 0:
            plan["status"] = "ACTIVE"
            plan["lastma_alert"] = True
            plan["dispatch_priority"] = "HIGH"
            plan["suggested_actions"].append("Emergency asphalt patching required (Night-Shift recommended)")
            plan["suggested_actions"].append("LASTMA: Suggest 1-lane closure at detection zone")
            
        elif urgency > 40:
            plan["status"] = "MONITORING"
            plan["dispatch_priority"] = "MEDIUM"
            plan["suggested_actions"].append("Schedule maintenance within 48 hours")
            
        return plan

# Configuration
TRACKER = "bytetrack.yaml"
MIN_DETECTION_FRAMES = 3
DETECTION_TIME_WINDOW = 1.0
CONFIDENCE_THRESHOLD = 0.80
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

# Thread pool for blocking operations
executor = ThreadPoolExecutor(max_workers=4)


class VideoProcessor:
    def __init__(self):
        """Initialize video processor with YOLO model on GPU"""
        try:
            logger.info(f"Loading model on device: {DEVICE}")
            self.model = YOLO("models/best.pt")
            
            if DEVICE == "cuda:0":
                self.model.to(DEVICE)
                logger.info(f"Model loaded on GPU: {torch.cuda.get_device_name(0)}")
            else:
                logger.info("Model loaded on CPU")
            
            # Warmup
            self._warmup()
            logger.info("Video processor ready")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def _warmup(self):
        """Warmup model for optimal performance"""
        try:
            import numpy as np
            dummy = np.zeros((640, 640, 3), dtype=np.uint8)
            self.model.predict(dummy, verbose=False, device=DEVICE)
        except:
            pass

    @staticmethod
    def get_adaptive_params(speed):
        """Get adaptive parameters based on speed"""
        if speed < 30:
            return {"roi_ratio": 0.50, "conf": 0.70}
        elif speed < 60:
            return {"roi_ratio": 0.65, "conf": 0.70}
        else:
            return {"roi_ratio": 0.75, "conf": 0.22}

    @staticmethod
    def calculate_severity(area, confidence):
        """Disruptive Heuristic: Classify pothole hazard level"""
        if area > 20000 and confidence > 0.85:
            return "CRITICAL"
        elif area > 8000:
            return "MEDIUM"
        else:
            return "LOW"

    @staticmethod
    def calculate_urgency_score(confirmed_count, total_frames, severity_counts):
        """NOVEL: Predictive Maintenance Urgency Score (0-100)"""
        if total_frames == 0: return 0
        density = confirmed_count / (total_frames / 30) # potholes per second
        critical_weight = severity_counts.get("CRITICAL", 0) * 10
        medium_weight = severity_counts.get("MEDIUM", 0) * 5
        score = (density * 50) + critical_weight + medium_weight
        return min(100, round(score, 2))

    def detect_frame(self, frame, frame_id, results_log, tracker, confirmed, current_time, speed):
        """Detect potholes in a single frame with tracking"""
        h, w = frame.shape[:2]
        params = self.get_adaptive_params(speed)
        
        # ROI extraction
        roi_y = int(h * (1 - params["roi_ratio"]))
        roi = frame[roi_y:h, :]
        
        detections = []
        count = 0
        new_count = 0
        
        try:
            results = self.model.track(
                roi,
                conf=params["conf"],
                tracker=TRACKER,
                persist=True,
                verbose=False,
                device=DEVICE,
                imgsz=640
            )
            
            for r in results:
                if r.boxes is None or len(r.boxes) == 0:
                    continue
                    
                boxes = r.boxes.xyxy.cpu().numpy()
                confs = r.boxes.conf.cpu().numpy()
                ids = r.boxes.id.cpu().numpy() if r.boxes.id is not None else None
                
                if ids is None:
                    continue
                
                for box, track_id, conf in zip(boxes, ids, confs):
                    x1, y1, x2, y2 = map(int, box)
                    track_id = int(track_id)
                    
                    # Adjust coordinates
                    y1_full, y2_full = y1 + roi_y, y2 + roi_y
                    
                    # Update tracker
                    tracker[track_id].append(current_time)
                    
                    # Check confirmation
                    recent = [t for t in tracker[track_id] if current_time - t <= DETECTION_TIME_WINDOW]
                    
                    if len(recent) >= MIN_DETECTION_FRAMES and track_id not in confirmed:
                        confirmed[track_id] = {
                            "frame": frame_id,
                            "time": current_time,
                            "conf": conf
                        }
                        new_count = 1
                    
                    if track_id in confirmed:
                        count += 1
                        # Calculate center and area
                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1_full + y2_full) / 2)
                        area = (x2 - x1) * (y2_full - y1_full)
                        severity = self.calculate_severity(area, conf)
                        
                        detections.append({
                            "frame_id": frame_id,
                            "pothole_id": track_id,
                            "type": "pothole",
                            "confidence": round(float(conf), 3),
                            "severity": severity,
                            "bbox": {
                                "x1": x1,
                                "y1": y1_full,
                                "x2": x2,
                                "y2": y2_full
                            },
                            "center": {
                                "x": center_x,
                                "y": center_y
                            },
                            "area": area
                        })
            
            if detections:
                results_log["frames"].append({
                    "frame_id": frame_id,
                    "speed_kmh": speed,
                    "roi_ratio": params["roi_ratio"],
                    "potholes": detections
                })
                
        except Exception as e:
            logger.error(f"Detection error: {e}")
        
        return count, new_count

    def _process_video_blocking(self, video_id: str, video_path: str, speed: int, loop):
        """Process video in blocking thread"""
        try:
            asyncio.run_coroutine_threadsafe(
                manager.send_message(video_id, {"type": "status", "status": "processing", "progress": 0}),
                loop
            )
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise Exception("Could not open video")
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            logger.info(f"Processing {video_id}: {total_frames} frames @ {fps:.1f} FPS")
            
            results_log = {"frames": []}
            tracker = defaultdict(lambda: deque(maxlen=20))
            confirmed = {}
            severity_counts = {"LOW": 0, "MEDIUM": 0, "CRITICAL": 0}
            total_detections = 0
            frame_count = 0
            last_progress = 0
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                current_time = frame_count / fps
                
                n, new_found = self.detect_frame(
                    frame, frame_count, results_log, tracker, confirmed, current_time, speed
                )
                total_detections += n
                
                # Check for newly confirmed pothole and update severity counts
                if new_found:
                    latest_pothole_id = max(confirmed.keys())
                    # We need to know the severity of the newly confirmed pothole
                    # Simplified: find it in results_log
                    for f in reversed(results_log["frames"]):
                        for p in f["potholes"]:
                            if p["pothole_id"] == latest_pothole_id:
                                severity_counts[p["severity"]] += 1
                                break
                        else: continue
                        break
                
                # Progress update every 5%
                progress = int((frame_count / total_frames) * 100)
                if progress - last_progress >= 5:
                    processing_status[video_id]["progress"] = progress
                    asyncio.run_coroutine_threadsafe(
                        manager.send_message(video_id, {
                            "type": "progress",
                            "progress": progress,
                            "unique_potholes": len(confirmed),
                            "total_detections": total_detections
                        }),
                        loop
                    )
                    last_progress = progress
            
            cap.release()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
            # Build results
            pothole_list = sorted([
                {
                    "pothole_id": int(pid),
                    "first_detected_frame": info["frame"],
                    "first_detected_time": round(info["time"], 2),
                    "confidence": round(float(info["conf"]), 3)
                }
                for pid, info in confirmed.items()
            ], key=lambda x: x["first_detected_frame"])
            
            frames_with_detections = len(results_log["frames"])
            detection_rate = round((frames_with_detections / frame_count) * 100, 2) if frame_count > 0 else 0
            urgency_score = self.calculate_urgency_score(len(confirmed), frame_count, severity_counts)
            
            results = {
                "video_id": video_id,
                "video_path": video_path,
                "speed_kmh": speed,
                "processed_at": datetime.now().isoformat(),
                "urgency_score": urgency_score,
                "video_info": {
                    "total_frames": total_frames,
                    "fps": round(fps, 2),
                    "duration": round(total_frames / fps, 2),
                    "width": width,
                    "height": height,
                    "resolution": f"{width}x{height}"
                },
                "summary": {
                    "total_frames": frame_count,
                    "unique_potholes": len(confirmed),
                    "total_detections": total_detections,
                    "frames_with_detections": frames_with_detections,
                    "detection_rate": detection_rate,
                    "severity_breakdown": severity_counts
                },
                "pothole_list": pothole_list,
                "frames": results_log["frames"],
                "mitigation_plan": LagosTrafficMitigator.generate_mitigation_plan(
                    {"urgency_score": urgency_score, "summary": {"severity_breakdown": severity_counts}}
                )
            }
            
            detection_results[video_id] = results
            update_global_map(pothole_list, video_id)
            
            with open(RESULTS_DIR / f"{video_id}.json", 'w') as f:
                json.dump(results, f, indent=2)
            
            processing_status[video_id] = {"status": "completed", "progress": 100}
            
            asyncio.run_coroutine_threadsafe(
                manager.send_message(video_id, {
                    "type": "complete",
                    "status": "completed",
                    "summary": results["summary"]
                }),
                loop
            )
            
            # Detailed logging
            unique_ids = sorted([p["pothole_id"] for p in pothole_list])
            logger.info("=" * 60)
            logger.info(f"VIDEO PROCESSING COMPLETE: {video_id}")
            logger.info(f"Total frames: {frame_count}")
            logger.info(f"Total detections: {total_detections}")
            logger.info(f">>> UNIQUE POTHOLES: {len(confirmed)} <<<")
            logger.info(f"Pothole IDs: {unique_ids}")
            logger.info("=" * 60)
            print(f"\n{'='*60}")
            print(f"VIDEO PROCESSING COMPLETE")
            print(f"{'='*60}")
            print(f"Video ID: {video_id}")
            print(f"Frames: {frame_count} | Device: {DEVICE}")
            print(f"Total detections: {total_detections}")
            print(f">>> UNIQUE POTHOLES: {len(confirmed)} <<<")
            print(f"Pothole IDs: {unique_ids}")
            print(f"{'='*60}\n")
            return results
            
        except Exception as e:
            logger.error(f"Error processing {video_id}: {e}")
            processing_status[video_id] = {"status": "error", "message": str(e)}
            asyncio.run_coroutine_threadsafe(
                manager.send_message(video_id, {"type": "error", "message": str(e)}),
                loop
            )
            raise

    async def process_video(self, video_id: str, video_path: str, speed_kmh: int):
        """Async video processing"""
        processing_status[video_id] = {"status": "processing", "progress": 0}
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            executor, self._process_video_blocking, video_id, video_path, speed_kmh, loop
        )

    async def get_status(self, video_id: str):
        """Get processing status"""
        if video_id not in processing_status:
            raise HTTPException(status_code=404, detail="Video ID not found")
        return processing_status[video_id]

    async def get_results(self, video_id: str):
        """Get detection results"""
        if video_id not in detection_results:
            result_file = RESULTS_DIR / f"{video_id}.json"
            if result_file.exists():
                with open(result_file, 'r') as f:
                    detection_results[video_id] = json.load(f)
            else:
                raise HTTPException(status_code=404, detail="Results not found")
        return detection_results[video_id]