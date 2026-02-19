# app/services/satellite_sentinel.py
"""
ROADvision_Lagos: Satellite Sentinel Service
Created by David Akpoviroro Oke (MrIridescent)
Specialized in Macro-scale Infrastructure Monitoring for Lagos, Nigeria
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Simulated Satellite Data (Google Earth / Sentinel-2 integration logic)
LAGOS_REGIONS = [
    {"name": "Ikeja", "lat": 6.5965, "lon": 3.3421},
    {"name": "Lekki", "lat": 6.4584, "lon": 3.6015},
    {"name": "Ikorodu", "lat": 6.6194, "lon": 3.5105},
    {"name": "Badagry", "lat": 6.4253, "lon": 2.8824},
    {"name": "Oshodi", "lat": 6.5540, "lon": 3.3400},
]

class SatelliteSentinel:
    def __init__(self):
        self.data_dir = Path("data/satellite")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.scan_history_file = self.data_dir / "scan_history.json"

    def scan_region(self, region_name: str) -> Dict:
        """
        Simulate a satellite scan of a specific Lagos region.
        In a production environment, this would call Google Earth Engine or Sentinel-2 APIs.
        """
        region = next((r for r in LAGOS_REGIONS if r["name"] == region_name), LAGOS_REGIONS[0])
        
        # Nuanced Logic: Detect macro-erosion hotspots
        # We simulate finding 1-5 major road failures based on satellite pixel degradation
        num_failures = random.randint(1, 5)
        failures = []
        for i in range(num_failures):
            failures.append({
                "id": f"SAT-{region_name}-{i}",
                "lat": region["lat"] + random.uniform(-0.01, 0.01),
                "lon": region["lon"] + random.uniform(-0.01, 0.01),
                "severity": random.choice(["MEDIUM", "CRITICAL"]),
                "type": "Road Failure / Asphalt Erosion",
                "detected_at": datetime.now().isoformat(),
                "confidence": round(random.uniform(0.75, 0.98), 2)
            })
            
        scan_result = {
            "region": region_name,
            "coordinates": {"lat": region["lat"], "lon": region["lon"]},
            "timestamp": datetime.now().isoformat(),
            "failures_detected": failures,
            "infrastructure_score": round(random.uniform(20, 85), 2),
            "sentinel_version": "2.0-Lagos"
        }
        
        self._save_scan(scan_result)
        return scan_result

    def _save_scan(self, result: Dict):
        history = []
        if self.scan_history_file.exists():
            with open(self.scan_history_file, "r") as f:
                history = json.load(f)
        
        history.append(result)
        # Keep last 50 scans
        history = history[-50:]
        
        with open(self.scan_history_file, "w") as f:
            json.dump(history, f, indent=2)

    def get_city_wide_health(self) -> Dict:
        """Aggregate data from all recent scans to provide a city-wide health report"""
        if not self.scan_history_file.exists():
            # Run initial scans for all regions if history is empty
            for r in LAGOS_REGIONS:
                self.scan_region(r["name"])
        
        with open(self.scan_history_file, "r") as f:
            history = json.load(f)
            
        latest_scans = {r["name"]: None for r in LAGOS_REGIONS}
        for scan in reversed(history):
            if latest_scans[scan["region"]] is None:
                latest_scans[scan["region"]] = scan
        
        all_scans = [s for s in latest_scans.values() if s]
        avg_score = sum(s["infrastructure_score"] for s in all_scans) / len(all_scans) if all_scans else 0
        total_failures = sum(len(s["failures_detected"]) for s in all_scans)
        
        return {
            "city": "Lagos",
            "average_infrastructure_score": round(avg_score, 2),
            "total_macro_failures": total_failures,
            "last_city_scan": datetime.now().isoformat(),
            "regional_breakdown": latest_scans
        }

satellite_sentinel = SatelliteSentinel()
