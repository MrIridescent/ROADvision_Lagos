# ROADvision_Lagos: Environment Specifications
**Lead Architect**: David Akpoviroro Oke (MrIridescent)

This document outlines the optimal deployment environments for the ROADvision_Lagos AI infrastructure sentinel.

---

## 💻 1. Hardware Requirements (Sentinel Grade)

For real-time edge inference on high-speed Lagos expressways (Ikorodu, Lekki, Third Mainland):

- **GPU**: NVIDIA RTX 3070 / 4070 or higher (8GB+ VRAM).
- **CPU**: Intel Core i7 (12th Gen+) or AMD Ryzen 7 (5000+).
- **RAM**: 16GB DDR4/DDR5 (32GB recommended for large batch processing).
- **Storage**: 500GB NVMe SSD (High speed for video buffering).

---

## 🛠️ 2. Software Prerequisites

- **Python**: 3.10 or 3.11 (optimized for PyTorch 2.6+).
- **Node.js**: 18.x or 20.x (LTS recommended).
- **FFmpeg**: Required for video frame extraction.
- **CUDA Toolkit**: 11.8 or 12.1 (Must match GPU drivers).

---

## 🏗️ 3. Directory Architecture (ROADvision v2.0)

| Path | Purpose |
| :--- | :--- |
| `RoadVision_Backend/` | Core FastAPI server and YOLOv8 logic. |
| `RoadVision_Frontend/` | Next.js 15 interactive dashboard. |
| `RoadVision_Backend/data/` | Persistent Global Road Map and Audit Logs. |
| `RoadVision_Backend/uploads/` | Raw video footage storage. |
| `RoadVision_Backend/results/` | AI detection JSON reports. |

---

## 🚀 4. Rapid Deployment (Turnkey)

The **ROADvision_Lagos_Setup.py** script automates the entire process:

```bash
python ROADvision_Lagos_Setup.py
```

**Post-Setup Launch**:
1. **Backend**: `cd RoadVision_Backend && python main.py`
2. **Frontend**: `cd RoadVision_Frontend && npm run dev`

---

## 🇳🇬 5. Specialized Lagos Calibration

- **Speed-Adaptive ROI**: The system automatically adjusts detection regions based on vehicle speed (30km/h vs 80km/h).
- **Low-Latency WebSockets**: Optimized for 4G/LTE connectivity in metropolitan Lagos areas.
- **Persistent Governance**: Data persists across sessions in `global_road_map.json` for city-wide historical analysis.

---

**ROADvision_Lagos** - *Securing Nigeria's Roads through AI Precision.*  
**Created by David Akpoviroro Oke (MrIridescent)**
