# ROADvision_Lagos: Sentinel Backend Engine
**Lead Architect**: David Akpoviroro Oke (MrIridescent)

The core engine of ROADvision_Lagos, providing AI-driven infrastructure governance through FastAPI and YOLOv8.

---

## 🛠️ Core Features

- **Lagos-Sentinel AI**: Edge inference optimized for high-speed expressways (YOLOv8 + ByteTrack).
- **Satellite Macro-Analysis**: Integration with orbital data for regional road health monitoring.
- **Predictive Scoring**: Calculation of the **Maintenance Urgency Score (MUS)** based on hazard density and severity.
- **Traffic Mitigation**: Real-time diversion suggestions for municipal authorities.
- **Contractor Accountability**: Blockchain-inspired audit log for repair verification.

---

## 🏗️ Technical Stack

- **Framework**: FastAPI (Async Performance)
- **Deep Learning**: Ultralytics YOLOv8 + PyTorch
- **Computer Vision**: OpenCV
- **Real-time**: WebSockets (Broadcast manager)
- **Database**: Persistent JSON storage for Global Road Map and Audit Logs

---

## 🚀 Manual Setup

While `ROADvision_Lagos_Setup.py` is recommended, manual installation is possible:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup Directories**:
   ```bash
   mkdir -p uploads results models data/reports data/satellite data/audit
   ```
3. **Launch Engine**:
   ```bash
   python main.py
   ```

---

## 🔌 API Specification (Sentinel v2.0)

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/upload` | POST | Upload video and set analysis speed. |
| `/api/status/{id}` | GET | Real-time processing progress. |
| `/api/results/{id}` | GET | Granular detection logs and severity report. |
| `/api/satellite/city-health` | GET | Aggregated city-wide infrastructure index. |
| `/api/city/flood-risk` | GET | Predictive erosion modeling (Lagos specific). |
| `/api/audit/verify-repair` | POST | Contractor repair verification and audit log. |

---

**ROADvision_Lagos** - *Precision Infrastructure Governance for Nigeria.*  
**Created by David Akpoviroro Oke (MrIridescent)**
