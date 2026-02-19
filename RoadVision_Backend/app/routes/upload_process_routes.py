# app/routes/upload_process_routes.py

from fastapi import APIRouter, UploadFile, File, WebSocket, WebSocketDisconnect, HTTPException
import asyncio
from app.services.upload_service import UploadService
from app.services.video_processor import VideoProcessor
from app.ws.websocket_manager import manager
from app.core.storage import (
    processing_status, 
    detection_results, 
    GLOBAL_MAP_FILE, 
    DATA_DIR, 
    add_live_feedback, 
    get_live_feedback
)
import json
from pathlib import Path
from datetime import datetime

from app.services.satellite_sentinel import satellite_sentinel
from app.services.flood_correlation import flood_service
from app.services.contractor_audit import contractor_audit

router = APIRouter()

@router.get("/city/flood-risk")
async def get_flood_risk(region: str = "Lekki", rainfall_mm: float = 50.0):
    """NICHE LEADER: Correlate rainfall and topography with pothole formation"""
    return flood_service.calculate_erosion_risk(region, rainfall_mm)

@router.post("/audit/verify-repair")
async def verify_repair(contractor_id: str, pothole_id: str):
    """NICHE LEADER: AI verification of contractor repairs"""
    return contractor_audit.submit_repair(contractor_id, pothole_id, "before.jpg", "after.jpg")

@router.get("/satellite/city-health")
async def get_lagos_city_health():
    """NOVEL: Get city-wide infrastructure health report from satellite data"""
    return satellite_sentinel.get_city_wide_health()

@router.get("/satellite/scan")
async def scan_lagos_region(region: str = "Ikeja"):
    """Scan specific Lagos region via satellite sentinel"""
    return satellite_sentinel.scan_region(region)

upload_service = UploadService()
video_processor = VideoProcessor()


@router.post("/upload")
async def upload_video(file: UploadFile = File(...), speed_kmh: int = 30):
    """Upload video and start background processing"""
    return await upload_service.upload_video(file, speed_kmh)


@router.get("/status/{video_id}")
async def get_status(video_id: str):
    """Get current processing status"""
    return await video_processor.get_status(video_id)


@router.get("/results/{video_id}")
async def get_results(video_id: str):
    """Get detection results for a processed video"""
    return await video_processor.get_results(video_id)


@router.get("/videos")
async def list_videos():
    """List all processed videos"""
    videos = []
    for video_id, status in processing_status.items():
        video_info = {
            "video_id": video_id,
            "status": status["status"],
            "progress": status["progress"]
        }
        
        if video_id in detection_results:
            video_info["summary"] = detection_results[video_id]["summary"]
        
        videos.append(video_info)
    
    return {"videos": videos}


@router.get("/analytics/global-map")
async def get_global_map():
    """NOVEL: Get aggregated pothole data for global visualization"""
    if GLOBAL_MAP_FILE.exists():
        with open(GLOBAL_MAP_FILE, 'r') as f:
            return json.load(f)
    return {"potholes": [], "stats": {"total_detected": 0}}


@router.get("/city/report/{video_id}")
async def generate_city_report(video_id: str):
    """DISRUPTIVE: Generate a formal JSON report for city authorities"""
    if video_id not in detection_results:
        await video_processor.get_results(video_id)
        
    results = detection_results[video_id]
    report = {
        "report_id": f"REP-{video_id[:8]}",
        "generated_at": datetime.now().isoformat(),
        "location_summary": "Detected Road Hazards",
        "urgency_index": results.get("urgency_score", 0),
        "hazards": results.get("pothole_list", []),
        "recommendation": "IMMEDIATE REPAIR" if results.get("urgency_score", 0) > 70 else "SCHEDULED MAINTENANCE"
    }
    
    report_path = DATA_DIR / "reports" / f"report_{video_id}.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
        
    return report


@router.post("/dispatch/repair")
async def dispatch_repair_bot(pothole_id: int, location: str = "Unknown"):
    """NOVEL: Mock endpoint for autonomous repair drone dispatch"""
    # In a real scenario, this would trigger a robot/drone
    message = f"Autonomous repair unit ROAD-BOT-01 dispatched to {location} for pothole #{pothole_id}"
    
    # Persistent Log
    entry = add_live_feedback("SYSTEM", message)
    
    # Real-time Broadcast
    await manager.broadcast_command_link({
        "type": "feedback",
        **entry
    })
    
    return {
        "status": "dispatched",
        "unit_id": "ROAD-BOT-01",
        "eta": "15 minutes",
        "target_pothole": pothole_id,
        "message": message
    }


@router.websocket("/ws/command-link")
async def command_link_endpoint(websocket: WebSocket):
    """NOVEL: Global Command Link for real-time peer-to-peer communication and system logs"""
    await manager.connect_command_link(websocket)
    
    try:
        # Send history on connect
        history = get_live_feedback()
        await websocket.send_json({
            "type": "history",
            "messages": history
        })
        
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "message":
                user = data.get("user", "Anonymous")
                msg = data.get("message", "")
                
                # Persist
                entry = add_live_feedback(user, msg)
                
                # Broadcast
                await manager.broadcast_command_link({
                    "type": "feedback",
                    **entry
                })
                
    except WebSocketDisconnect:
        manager.disconnect_command_link(websocket)
    except Exception as e:
        print(f"Command Link Error: {e}")
        manager.disconnect_command_link(websocket)


@router.websocket("/ws/{video_id}")
async def websocket_endpoint(websocket: WebSocket, video_id: str):
    """WebSocket for real-time processing updates"""
    
    await manager.connect(video_id, websocket)
    
    try:
        # Send initial status if available
        if video_id in processing_status:
            await websocket.send_json({
                "type": "status",
                **processing_status[video_id]
            })
        
        # Keep connection alive and wait for processing to complete
        while True:
            # Check if processing is done
            if video_id in processing_status:
                status = processing_status[video_id]["status"]
                if status in ["completed", "error"]:
                    # Send final status and close gracefully
                    await websocket.send_json({
                        "type": "status",
                        **processing_status[video_id]
                    })
                    break
            
            # Keep connection alive with a ping/pong mechanism
            try:
                # Wait for any message from client (like ping) with timeout
                await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
            except asyncio.TimeoutError:
                # Send a heartbeat to keep connection alive
                try:
                    await websocket.send_json({"type": "heartbeat"})
                except:
                    break
            except:
                break
            
            # Small delay to prevent busy loop
            await asyncio.sleep(0.1)
    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error for {video_id}: {e}")
    finally:
        manager.disconnect(video_id)