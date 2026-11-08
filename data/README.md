# Data Directory Structure

This folder contains input remote sensing data, digital elevation models (DEM), and output results for the Landslide SAM Detection pipeline.

## Directory Structure
- `pre/`: Pre-event multispectral imagery (e.g., Sentinel-2 Level-2A GeoTIFFs, September 2024).
- `post/`: Post-event multispectral imagery (e.g., Sentinel-2 Level-2A GeoTIFFs, October 2024).
- `dem/`: Digital Elevation Model rasters & derived products (e.g., ALOS AW3D30 slope raster).
- `results/`: Pipeline outputs including vector polygons (`landslides.geojson`), binary raster masks (`landslide_mask.tif`), and susceptibility maps.

> **Note**: Raw satellite imagery and heavy raster files (`*.tif`, `*.tiff`) are excluded from version control via `.gitignore` to maintain a lightweight repository. To re-fetch imagery, execute `python main.py` or run `data_fetcher.py`.
