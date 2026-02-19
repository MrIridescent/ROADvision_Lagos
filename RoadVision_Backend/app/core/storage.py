# app/core/storage.py

from pathlib import Path
from typing import Dict, List
import json
from datetime import datetime

# Directory setup
UPLOAD_DIR = Path("uploads")
RESULTS_DIR = Path("results")
DATA_DIR = Path("data")

UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

GLOBAL_MAP_FILE = DATA_DIR / "global_road_map.json"
FEEDBACK_FILE = DATA_DIR / "live_feedback.json"
REPORTS_DIR = DATA_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# In-memory storage for processing status and results
processing_status: Dict[str, dict] = {}
detection_results: Dict[str, dict] = {}

def update_global_map(new_detections: list, video_id: str):
    """Update the crowdsourced global road health map with persistent storage"""
    try:
        data = {"potholes": [], "stats": {"total_detected": 0, "last_update": ""}}
        if GLOBAL_MAP_FILE.exists():
            with open(GLOBAL_MAP_FILE, 'r') as f:
                data = json.load(f)
        
        for d in new_detections:
            d["video_id"] = video_id
            data["potholes"].append(d)
            
        data["stats"]["total_detected"] = len(data["potholes"])
        data["stats"]["last_update"] = datetime.now().isoformat()
            
        with open(GLOBAL_MAP_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Global map update failed: {e}")

def add_live_feedback(user: str, message: str):
    """Save persistent real-time feedback messages"""
    try:
        data: List[dict] = []
        if FEEDBACK_FILE.exists():
            with open(FEEDBACK_FILE, 'r') as f:
                data = json.load(f)
        
        new_entry = {
            "id": str(datetime.now().timestamp()),
            "user": user,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        data.append(new_entry)
        
        # Keep only last 100 messages
        data = data[-100:]
        
        with open(FEEDBACK_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return new_entry
    except Exception as e:
        print(f"Feedback storage failed: {e}")
        return None

def get_live_feedback():
    """Retrieve feedback history"""
    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return []
