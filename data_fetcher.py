import pystac_client
import planetary_computer
import rioxarray
import xarray as xr
from shapely.geometry import box
import datetime
import os
import requests

def fetch_sentinel_imagery(bbox, date_range, cloud_cover_max=10, output_dir="data"):
    """
    Searches for and downloads Sentinel-2 imagery from Microsoft Planetary Computer.
    Direct approach to avoid PROJ/stackstac issues.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, f"sentinel_best_{date_range.replace('/', '_').replace(':', '-')}.tif")
    if os.path.exists(output_path):
        print(f"Skipping fetch: {output_path} already exists.", flush=True)
        return output_path

    print(f"Searching for Sentinel-2 imagery in {bbox} for period {date_range}...", flush=True)
    
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=date_range,
        query={"eo:cloud_cover": {"lt": cloud_cover_max}},
    )

    items = search.item_collection()
    if not items:
        print(f"No items found for {date_range}", flush=True)
        return None

    # Sort items by cloud cover to get the 'best' one first
    items = sorted(items, key=lambda x: x.properties.get("eo:cloud_cover", 100))
    best_item = items[0]
    print(f"Using best item from {best_item.properties['datetime']} (Cloud Cover: {best_item.properties.get('eo:cloud_cover')}%)", flush=True)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    assets_to_download = ["B02", "B03", "B04", "B08"]
    bands_data = {}

    for asset_key in assets_to_download:
        asset_url = best_item.assets[asset_key].href
        print(f"Opening {asset_key} band...", flush=True)
        
        # Open directly with rioxarray from URL
        # We clip it immediately to save memory and time
        ds = rioxarray.open_rasterio(asset_url)
        ds_clipped = ds.rio.clip_box(*bbox, crs="EPSG:4326")
        bands_data[asset_key] = ds_clipped

    # Combine bands into a single dataset
    combined = xr.concat([bands_data[b] for b in assets_to_download], dim="band")
    combined = combined.assign_coords(band=[1, 2, 3, 4]) # Map to asset keys index
    
    output_path = os.path.join(output_dir, f"sentinel_best_{date_range.replace('/', '_').replace(':', '-')}.tif")
    combined.rio.to_raster(output_path)
    
    print(f"Saved composite to {output_path}", flush=True)
    return output_path

def run_phase_1():
    # Smaller AOI for verification: 0.1 degree box (~11km)
    bbox = [-82.5, 35.5, -82.4, 35.6]
    pre_event_range = "2024-09-01/2024-09-30"
    post_event_range = "2024-10-01/2024-10-31"
    
    print("--- Fetching Pre-Event Imagery ---")
    pre_path = fetch_sentinel_imagery(bbox, pre_event_range, output_dir="data/pre")
    
    print("\n--- Fetching Post-Event Imagery ---")
    post_path = fetch_sentinel_imagery(bbox, post_event_range, output_dir="data/post")
    
    return pre_path, post_path

if __name__ == "__main__":
    run_phase_1()
