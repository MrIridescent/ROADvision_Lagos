#!/usr/bin/env python3
"""
ROADvision_Lagos: AI Infrastructure Guardian Setup v2.0
Created by David Akpoviroro Oke (MrIridescent)
Specialized for Nigerian Road Infrastructure Challenges
"""

import os
import sys
import shutil
import subprocess
import platform
import time
from pathlib import Path

# --- Configuration ---
BACKEND_DIR = Path("RoadVision_Backend")
FRONTEND_DIR = Path("RoadVision_Frontend")
REQUIRED_COMMANDS = ["python", "pip", "node", "npm"]
DATA_DIRS = ["uploads", "results", "models", "data", "data/reports", "data/satellite", "data/audit"]

def print_header(text):
    print("\n" + "🇳🇬 " + "=" * 60 + " 🇳🇬")
    print(f" {text.center(58)} ")
    print("🇳🇬 " + "=" * 60 + " 🇳🇬\n")

def check_command(cmd):
    return shutil.which(cmd) is not None

def run_cmd(cmd, cwd=None, shell=False):
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=shell, check=True, 
                               capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def setup_wizard():
    print_header("ROADvision_Lagos: AI Infrastructure Guardian")
    print("Developed by David Akpoviroro Oke (MrIridescent)")
    
    # --- System Verification ---
    print("\n[1/5] Verifying System Requirements...")
    missing = [cmd for cmd in REQUIRED_COMMANDS if not check_command(cmd)]
    if missing:
        print(f"❌ ERROR: Missing system dependencies: {', '.join(missing)}")
        print("Please install Python 3.10+, Node.js 18+, and FFmpeg before continuing.")
        sys.exit(1)
    
    print(f"✅ System: {platform.system()} {platform.release()}")
    time.sleep(1)

    # --- Directory Preparation ---
    print("\n[2/5] Initializing Lagos Infrastructure Directories...")
    for d in DATA_DIRS:
        dir_path = BACKEND_DIR / d
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  - Verified {dir_path}")
    
    # --- Backend Setup ---
    print("\n[3/5] Setting Up Lagos-Sentinel Backend (Python FastAPI)...")
    req_file = BACKEND_DIR / "requirements.txt"
    if req_file.exists():
        print("  Installing core dependencies for Nigerian Road Analysis...")
        success, _ = run_cmd([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
        if not success:
            print("  ⚠️ Pip install issues. Forcing core components...")
            run_cmd([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "ultralytics", "torch", "opencv-python", "websockets"])
    
    # --- Frontend Setup ---
    print("\n[4/5] Setting Up Lagos-Sentinel Dashboard (Next.js)...")
    if FRONTEND_DIR.exists():
        pkg_manager = "pnpm" if check_command("pnpm") else "npm"
        print(f"  Using {pkg_manager} to install frontend packages...")
        success, _ = run_cmd([pkg_manager, "install"], cwd=FRONTEND_DIR)
        if not success:
            print(f"  ⚠️ {pkg_manager} install failed. Check node version (18+ required).")
    
    # --- Finalizing ---
    print("\n[5/5] Finalizing ROADvision_Lagos Initialization...")
    print_header("LAGOS-SENTINEL SETUP COMPLETE")
    print("To start the system, run these commands in TWO separate terminals:")
    print("-" * 60)
    print("🇳🇬 BACKEND:  cd RoadVision_Backend && python main.py")
    print("🇳🇬 FRONTEND: cd RoadVision_Frontend && npm run dev")
    print("-" * 60)
    print("Dashboard: http://localhost:3000")
    print("API Docs:  http://localhost:8000/docs")
    print("\nCreator Branding: David Akpoviroro Oke (MrIridescent)")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    setup_wizard()
