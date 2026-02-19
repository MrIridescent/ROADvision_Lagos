# ROADvision_Lagos: AI Infrastructure Guardian
**Created by David Akpoviroro Oke (MrIridescent)**

ROADvision_Lagos is a high-fidelity, turnkey AI infrastructure governance platform specialized for solving Nigerian road infrastructure challenges. It disrupts the cycle of road decay through a "cocktail" of disruptive features: real-time YOLOv8 hazard detection, predictive maintenance scoring, and satellite macro-analysis.

---

## 🇳🇬 Niche Leader Capabilities

- **Lagos-Sentinel AI**: Real-time YOLOv8 detection of potholes, cracks, and road failures with adaptive ROI for high-speed expressways.
- **Satellite Sentinel**: Macro-scale infrastructure monitoring via satellite imagery (Google Earth/Sentinel-2) to identify road erosion in inaccessible city zones.
- **Traffic Mitigation Engine**: Automated diversion suggestions for **LASTMA** based on critical infrastructure failure hotspots.
- **Flood-Pothole Correlation**: Predictive modeling that uses topography (elevation) and rainfall data to identify "Erosion Incubation Zones."
- **Contractor Audit Portal**: AI-verified accountability log that compares "Before" and "After" repair data to ensure maintenance efficiency.
- **Sentinel Hub & Command Link**: Real-time P2P communication and city-wide alert system for rapid response teams.

---

## 🏗️ Project Structure

```
ROADvision_Lagos/
├── RoadVision_Backend/      # FastAPI Server & AI Logic
│   ├── app/
│   │   ├── services/
│   │   │   ├── satellite_sentinel.py  # Orbital monitoring
│   │   │   ├── flood_correlation.py   # Erosion prediction
│   │   │   └── contractor_audit.py    # Accountability portal
│   │   └── routes/
│   └── models/               # YOLOv8 Weights
├── RoadVision_Frontend/     # Next.js 15 Dashboard
│   ├── app/
│   │   ├── dashboard/        # Central monitoring
│   │   └── satellite-sentinel/ # Orbital visualization
│   └── components/
└── ROADvision_Lagos_Setup.py # Automated Turnkey Installer
```

---

## 🚀 Turnkey Setup (Noob-Friendly)

The system is designed to be **Plug-and-Play**.

1. **Verify Prerequisites**: Ensure you have Python 3.10+, Node.js 18+, and FFmpeg installed.
2. **Run the Setup Wizard**:
   ```bash
   python ROADvision_Lagos_Setup.py
   ```
3. **Start the Sentinel Backend**:
   ```bash
   cd RoadVision_Backend && python main.py
   ```
4. **Start the Visual Dashboard**:
   ```bash
   cd RoadVision_Frontend && npm run dev
   ```

---

## 📡 API & Operational Links

- **Dashboard**: `http://localhost:3000`
- **Satellite Health**: `GET /api/v1/satellite/city-health`
- **Flood Risk Analysis**: `GET /api/v1/city/flood-risk?region=Lekki&rainfall_mm=80`
- **Repair Verification**: `POST /api/v1/audit/verify-repair`
- **Command Link (WS)**: `ws://localhost:8000/api/v1/ws/command-link`

---

## 🔧 Hardware Recommendations (Lagos-Sentinel Grade)

- **GPU**: NVIDIA RTX 3070+ (8GB VRAM) for real-time edge inference.
- **RAM**: 16GB+ DDR4.
- **OS**: Ubuntu 22.04 LTS (Recommended) or Windows 11 (WSL2).

---

**ROADvision_Lagos** - *Securing Nigeria's Roads through AI Precision.*  
**Lead Architect**: David Akpoviroro Oke (MrIridescent)
