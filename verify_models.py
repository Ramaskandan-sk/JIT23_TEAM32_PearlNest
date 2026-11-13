"""
Quick script to verify all model paths exist before starting the application.
Run this before launching the backend to catch any path issues early.

Usage:
    python verify_models.py
"""

from pathlib import Path
import sys

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from perlnest_pipeline import MODEL1_PATH, MODEL2_PATH, MODEL3_PATH
    MODEL_PATHS = {
        "Model 1 (Tooth Detection)": MODEL1_PATH,
        "Model 2 (Caries Segmentation)": MODEL2_PATH,
        "Model 3 (Findings Segmentation)": MODEL3_PATH,
    }
except Exception:
    MODEL_PATHS = {
        "Model 1 (Tooth Detection)": str((BASE_DIR / "runs/detect/train-model1-retrained/weights/best.pt").resolve()),
        "Model 2 (Caries Segmentation)": str((BASE_DIR / "runs/segment/train-2/weights/best.pt").resolve()),
        "Model 3 (Findings Segmentation)": str((BASE_DIR / "runs/segment/model3-filling-segmentation/weights/best.pt").resolve()),
    }

def verify_models():
    """Check if all model files exist."""
    print("=" * 70)
    print("PERLNEST MODEL PATH VERIFICATION")
    print("=" * 70)
    
    all_exist = True
    
    for model_name, model_path in MODEL_PATHS.items():
        path = Path(model_path)
        exists = path.exists()
        
        status = "[OK]" if exists else "[X]"
        color = "\033[92m" if exists else "\033[91m"
        reset = "\033[0m"
        
        print(f"\n{color}{status}{reset} {model_name}")
        print(f"   Path: {model_path}")
        
        if exists:
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"   Size: {size_mb:.2f} MB")
        else:
            print(f"   Status: FILE NOT FOUND")
            all_exist = False
    
    print("\n" + "=" * 70)
    
    if all_exist:
        print("[OK] All model files found and ready!")
        print("\nYou can now start the application:")
        print("  1. Backend: python backend/api.py")
        print("  2. Frontend: cd frontend && npm run dev")
        print("=" * 70)
        return 0
    else:
        print("[X] Some model files are missing!")
        print("\nPlease check the paths and ensure models are trained.")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    exit_code = verify_models()
    sys.exit(exit_code)
