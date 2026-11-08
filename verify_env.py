import sys
import pystac_client
import planetary_computer
import stackstac
import rioxarray
import torch
from samgeo import SamGeo

def verify_system():
    print(f"Python version: {sys.version}")
    print(f"Torch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    try:
        catalog = pystac_client.Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace,
        )
        print("Successfully connected to Microsoft Planetary Computer.")
    except Exception as e:
        print(f"Failed to connect to STAC API: {e}")

    print("Checking samgeo initialization...")
    # This might take a second if it checks for models but doesn't download yet
    try:
        sam = SamGeo(model_type="vit_b") # Using vit_b for faster check
        print("SamGeo successfully initialized.")
    except Exception as e:
        print(f"SamGeo initialization failed: {e}")

if __name__ == "__main__":
    verify_system()
