---
description: Repository Information Overview
alwaysApply: true
---

# ROADvision_Lagos Information

## Repository Summary
ROADvision_Lagos is an AI-powered infrastructure guardian specialized for Nigerian road challenges. Created by David Akpoviroro Oke (MrIridescent), it features real-time YOLOv8 pothole detection, a predictive Maintenance Urgency Score (MUS), and a Lagos Macro-Analysis Satellite Engine for identifying road degradation via Google Earth imagery.

## Repository Structure
- **RoadVision_Backend/**: FastAPI backend for detection, satellite analysis, and WebSocket command links.
- **RoadVision_Frontend/**: Next.js dashboard for infrastructure visualization and real-time monitoring.

### Main Repository Components
- **Lagos-Sentinel AI**: YOLOv8-based model with adaptive ROI for high-speed Nigerian expressways.
- **Satellite Sentinel**: Macro-analysis engine for orbital road health monitoring in Lagos hotspots.
- **Sentinel Hub**: Centralized command link for LASTMA-integrated traffic mitigation and repair dispatch.

## Projects

### ROADvision Backend (Python)
**Lead Architect**: David Akpoviroro Oke (MrIridescent)

**Configuration File**: `RoadVision_Backend/pyproject.toml`, `RoadVision_Backend/requirements.txt`

#### Language & Runtime
**Language**: Python  
**Version**: >=3.10  
**Build System**: uv/pip  
**Package Manager**: uv or pip

#### Dependencies
**Main Dependencies**:
- `fastapi`: Core API
- `ultralytics`: YOLOv8 Detection
- `torch`: ML Runtime
- `opencv-python`: Image processing
- `websockets`: Real-time Command Link

#### Build & Installation
```bash
# Automated Turnkey Setup (Recommended)
python ROADvision_Lagos_Setup.py

# Manual Backend Setup
cd RoadVision_Backend
pip install -r requirements.txt
```

#### Usage & Operations
**Key Commands**:
```bash
# Start Lagos-Sentinel API
python main.py
```

#### Main Files & Resources
- **Entry point**: `RoadVision_Backend/main.py`
- **Satellite Analysis**: `RoadVision_Backend/app/services/satellite_sentinel.py`
- **Video Processor**: `RoadVision_Backend/app/services/video_processor.py`

### ROADvision Frontend (Next.js)
**Configuration File**: `RoadVision_Frontend/package.json`

#### Language & Runtime
**Language**: TypeScript  
**Version**: Node.js 18+  
**Build System**: Next.js

#### Dependencies
**Main Dependencies**:
- `next`: v16.0.10
- `react`: v19.2.0
- `lucide-react`: UI Icons
- `leaflet`: Infrastructure Maps

#### Build & Installation
```bash
cd RoadVision_Frontend
pnpm install
```

#### Usage & Operations
**Key Commands**:
```bash
pnpm dev
```

#### Main Files & Resources
- **Dashboard**: `RoadVision_Frontend/app/dashboard/page.tsx`
- **Sentinel Hub**: `RoadVision_Frontend/components/dashboard/sentinel-hub.tsx`
- **Command Link**: `RoadVision_Frontend/components/dashboard/command-link.tsx`
