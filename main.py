import os
import sys

# Force the correct PROJ path inside the script logic
# We use the rasterio version because it is Minor Version 5 (required by the libraries)
proj_path = r"C:\Users\user\AppData\Roaming\Python\Python313\site-packages\rasterio\proj_data"
os.environ['PROJ_LIB'] = proj_path
os.environ['PROJ_DATA'] = proj_path

print(f"--- Hardcoded PROJ_LIB to: {proj_path} ---", flush=True)

from data_fetcher import run_phase_1
from change_detection import run_phase_2
from segmentation import run_segmentation

def main():
    print("=== Landslide Detection Pipeline Started ===", flush=True)
    try:
        # Phase 1: Data Fetching
        print("\n--- Phase 1: Fetching Sentinel-2 Imagery ---", flush=True)
        pre_path, post_path = run_phase_1()
        
        if not pre_path or not post_path:
            print("Error: Phase 1 failed to acquire imagery. Exiting.", flush=True)
            return

        # Phase 2: Change Detection
        print("\n--- Phase 2: Change Detection & Prompt Generation ---", flush=True)
        points = run_phase_2(pre_path, post_path)
        
        if not points:
            print("No potential landslide points detected. Exiting.", flush=True)
            return

        # Phase 3: SAM Segmentation
        print("\n--- Phase 3: AI-Based Segmentation ---", flush=True)
        results_path = run_segmentation(post_path, points)
        
        print(f"\n=== Pipeline Completed Successfully ===", flush=True)
        print(f"Final Landslide Polygons: {results_path}", flush=True)
        print("\nTo run scientific validation, use the 'validation.R' script.", flush=True)
    except Exception as e:
        print(f"\n!!! Pipeline failed with error: {e}", flush=True)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
