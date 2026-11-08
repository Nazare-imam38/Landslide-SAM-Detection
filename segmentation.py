from samgeo import SamGeo
import os
import geopandas as gpd

def run_segmentation(image_path, points, model_type="vit_b", output_geojson="data/results/landslides.geojson"):
    """
    Runs SAM segmentation on the post-event image using point prompts.
    """
    print(f"Initializing SAM ({model_type})...", flush=True)
    
    sam = SamGeo(model_type=model_type)
    
    # Patch for AttributeError: 'SamGeo' object has no attribute 'predictor'
    if not hasattr(sam, 'predictor'):
        print("Patching SamGeo predictor...", flush=True)
        from segment_anything import SamPredictor
        sam.predictor = SamPredictor(sam.sam)

    if not os.path.exists(os.path.dirname(output_geojson)):
        os.makedirs(os.path.dirname(output_geojson))

    # Detect image CRS to ensure points are transformed correctly
    import rioxarray
    ds = rioxarray.open_rasterio(image_path)
    image_crs = ds.rio.crs
    print(f"Detected image CRS: {image_crs}", flush=True)

    print(f"Segmenting {image_path} with {len(points)} prompts...", flush=True)
    
    # Use the predictor directly for more control and to avoid internal SamGeo bugs
    sam.set_image(image_path)
    
    # Run prediction - sam.predict with return_results=True returns the mask array
    # We handle the coordinate transformation manually if needed, 
    # but SamGeo's predict should work if point_crs is right.
    # To be extremely safe, we'll try to catch the results.
    mask_data = sam.predict(
        point_coords=points,
        point_labels=[1] * len(points),
        point_crs=image_crs,
        return_results=True
    )
    
    import numpy as np
    print(f"SAM predict returned type: {type(mask_data)}", flush=True)
    
    # Robust unpacking
    def extract_mask(data):
        if isinstance(data, (tuple, list)):
            print(f" Unpacking nested structure of length {len(data)}...", flush=True)
            return extract_mask(data[0])
        return data

    mask = extract_mask(mask_data)
    print(f"Extracted mask type: {type(mask)}", flush=True)
    if isinstance(mask, np.ndarray):
        print(f"Mask shape: {mask.shape}", flush=True)

    if mask is None or (isinstance(mask, np.ndarray) and mask.size <= 1):
        print("Warning: SAM produced an empty or invalid mask.", flush=True)
        return None

    # mask might be (N, H, W). We want to merge all prompts into one mask or keep them.
    # For landslides, we merge them into a single binary mask for the whole area.
    if isinstance(mask, np.ndarray) and len(mask.shape) == 3:
        mask = np.max(mask, axis=0)

    # Force uint8 to avoid PIL int64 errors
    mask_uint8 = (mask > 0).astype(np.uint8)
    
    # Manually set the prediction and save to a temporary TIFF
    temp_tif = "data/results/landslide_mask.tif"
    sam.prediction = mask_uint8
    
    print(f"Saving temporary mask to {temp_tif}...", flush=True)
    sam.save_prediction(temp_tif, dtype='uint8')
    
    # Final conversion to GeoJSON
    print(f"Converting mask to GeoJSON: {output_geojson}...", flush=True)
    sam.tiff_to_geojson(temp_tif, output_geojson)
    
    print(f"Segmentation complete. Results saved to {output_geojson}", flush=True)
    return output_geojson

if __name__ == "__main__":
    # Example integration with Phase 2
    from change_detection import run_phase_2
    
    pre_event = "data/pre/sentinel_best_2024-09-01_2024-09-30.tif"
    post_event = "data/post/sentinel_best_2024-10-01_2024-10-31.tif"
    
    if os.path.exists(pre_event) and os.path.exists(post_event):
        points = run_phase_2(pre_event, post_event)
        if points:
            run_segmentation(post_event, points)
        else:
            print("No point prompts generated from change detection.")
    else:
        print("Required imagery files not found. Run Phase 1 first.")
