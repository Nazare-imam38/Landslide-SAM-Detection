import rioxarray
import numpy as np
import os
import pystac_client
import planetary_computer
import stackstac
from shapely.geometry import box

def calculate_ndvi(ds):
    """Calculates NDVI from Sentinel-2 bands (NIR: B08, Red: B04)"""
    # Assuming ds has bands B08 and B04
    nir = ds.sel(band="B08")
    red = ds.sel(band="B04")
    return (nir - red) / (nir + red)

def get_alos_dem(bbox, output_path="data/dem/alos_slope.tif"):
    """Fetches ALOS DEM and calculates slope."""
    if os.path.exists(output_path):
        print(f"Skipping DEM fetch: {output_path} already exists.", flush=True)
        return output_path

    print(f"Fetching ALOS DEM for {bbox}...", flush=True)
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    search = catalog.search(
        collections=["alos-dem"],
        bbox=bbox,
    )

    items = search.item_collection()
    if not items:
        print("No DEM items found.", flush=True)
        return None

    # Use the first item
    item = items[0]
    asset_url = item.assets["data"].href
    print(f"Opening DEM from {asset_url}...", flush=True)
    
    # Direct fetch with rioxarray to avoid PROJ/stackstac issues on this system
    dem = rioxarray.open_rasterio(asset_url)
    # The DEM is already in EPSG:4326, so we clip directly
    dem_clipped = dem.rio.clip_box(*bbox)
    
    # Simple slope calculation (central difference)
    data_vals = dem_clipped.values[0]
    dx, dy = np.gradient(data_vals)
    res = 30 # Approx 30m resolution for ALOS DEM
    slope = np.arctan(np.sqrt(dx**2 + dy**2) / res) * (180 / np.pi)
    
    slope_xr = dem_clipped.copy(data=slope[np.newaxis, ...])
    
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
        
    slope_xr.rio.to_raster(output_path)
    print(f"Saved slope map to {output_path}", flush=True)
    return output_path

def generate_prompts(pre_tif, post_tif, slope_tif, dndvi_threshold=0.4, slope_threshold=20):
    """Identifies potential landslide points based on dNDVI and Slope."""
    print("Performing change detection...", flush=True)
    
    # Use chunks=True to use Dask for memory-efficient loading of large TIFFs
    with rioxarray.open_rasterio(pre_tif, chunks=True) as pre, \
         rioxarray.open_rasterio(post_tif, chunks=True) as post, \
         rioxarray.open_rasterio(slope_tif, chunks=True) as slope:

        # Ensure all rasters are on the same grid (match to post-event resolution/bounds)
        pre = pre.rio.reproject_match(post)
        slope = slope.rio.reproject_match(post)

        # Calculate NDVI
        ndvi_pre = (pre.sel(band=4) - pre.sel(band=1)) / (pre.sel(band=4) + pre.sel(band=1))
        ndvi_post = (post.sel(band=4) - post.sel(band=1)) / (post.sel(band=4) + post.sel(band=1))
        
        dndvi = (ndvi_pre - ndvi_post).compute()
        slope_data = slope.values[0]
    
    # Apply conditions: dNDVI > 0.4 and Slope > 20 degrees
    mask = (dndvi > dndvi_threshold) & (slope.sel(band=1) > slope_threshold)
    
    # Find coordinates of mask
    coords = np.argwhere(mask.values)
    
    # Convert pixel coords to lat/lon (simplified)
    # We take a sample of points to avoid overwhelming SAM if it's a large area
    points = []
    if coords.size > 0:
        # Sample every 10th point or limit to 100 points for first pass
        step = max(1, len(coords) // 100)
        for y, x in coords[::step]:
            lon = mask.x.values[x]
            lat = mask.y.values[y]
            points.append((lon, lat))
            
    print(f"Generated {len(points)} point prompts.")
    return points

def run_phase_2(pre_tif, post_tif):
    bbox = [-82.5, 35.5, -82.4, 35.6]
    slope_path = get_alos_dem(bbox)
    
    if not slope_path:
        return []

    points = generate_prompts(pre_tif, post_tif, slope_path)
    return points

if __name__ == "__main__":
    # Example paths (adjust based on Phase 1 output)
    pre_event = "data/pre/sentinel_best_2024-09-01_2024-09-30.tif"
    post_event = "data/post/sentinel_best_2024-10-01_2024-10-31.tif"
    
    if os.path.exists(pre_event) and os.path.exists(post_event):
        points = run_phase_2(pre_event, post_event)
        print(f"Found {len(points)} potential landslide points.")
    else:
        print("Required imagery files not found. Run Phase 1 first.")
