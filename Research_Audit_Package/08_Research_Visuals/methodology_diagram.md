# Methodology Diagram — Landslide+SAM Detection Pipeline
## Text-based flowchart for use in applications and presentations

```
╔══════════════════════════════════════════════════════════════════════════╗
║          LANDSLIDE+SAM AUTOMATED DETECTION PIPELINE                      ║
║          Study Area: Western North Carolina, USA                         ║
║          Period: September–October 2024 (~100 km²)                       ║
╚══════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────┐
│  DATA SOURCES (Free, Public)                                │
│                                                             │
│  Microsoft Planetary Computer STAC API                     │
│  ├── Sentinel-2 L2A  (10m, B02/B03/B04/B08)               │
│  │   ├── Pre-event: September 2024                         │
│  │   └── Post-event: October 2024                          │
│  └── ALOS World 3D DEM  (~30m elevation)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: DATA ACQUISITION  [data_fetcher.py]               │
│                                                             │
│  • STAC query with cloud_cover < 10%                        │
│  • Select minimum cloud-cover scene per period              │
│  • Extract B02, B03, B04, B08 via rioxarray URL             │
│  • Clip to study bounding box                               │
│  • Stack → 4-band GeoTIFF (pre & post)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2a: TERRAIN ANALYSIS  [change_detection.py]          │
│                                                             │
│  • Fetch ALOS DEM, clip to bbox                             │
│  • numpy.gradient(elevation) → dx, dy                       │
│  • slope = arctan(|∇z|/30) × 180/π                         │
│  • Save: alos_slope.tif                                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2b: CHANGE DETECTION  [change_detection.py]          │
│                                                             │
│  • Reproject pre-event + slope to post-event grid           │
│  • NDVI_pre = (B08-B04)/(B08+B04)                          │
│  • NDVI_post = same for October scene                       │
│  • dNDVI = NDVI_pre - NDVI_post                            │
│                                                             │
│  DUAL THRESHOLD (physics-informed):                         │
│  ┌─────────────────────────────────┐                        │
│  │  dNDVI > 0.4                    │ ← vegetation removal   │
│  │      AND                        │                        │
│  │  slope > 20°                    │ ← geomorphic condition │
│  └─────────────────────────────────┘                        │
│                                                             │
│  • Extract coordinates from masked pixels                   │
│  • Sample up to 100 point prompts                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │  100 geographic point prompts
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: AI SEGMENTATION  [segmentation.py]                │
│                                                             │
│  Foundation Model: SAM vit_b (Meta AI — zero-shot)          │
│                                                             │
│  • sam.set_image(post_event_tif)                            │
│  • sam.predict(point_coords, point_labels=[1...])           │
│  • Merge N masks → np.max(axis=0)                          │
│  • Cast uint8 binary                                        │
│  • Save: landslide_mask.tif                                 │
│  • Vectorize: landslides.geojson  [EPSG:32617]             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 4: SUSCEPTIBILITY MAPPING  [validation.R]            │
│                                                             │
│  Using R: terra + sf                                        │
│  • slope_norm = slope / max(slope)                          │
│  • dist_norm = 1 - (dist_to_detections / max_dist)         │
│  • susceptibility = 0.6×slope_norm + 0.4×dist_norm        │
│  • Save: susceptibility.tif                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
╔══════════════════════════════════════════════════════════════╗
║  OUTPUTS                                                     ║
║  ├── landslides.geojson     (vector polygons, EPSG:32617)   ║
║  ├── landslide_mask.tif     (binary raster)                 ║
║  ├── susceptibility.tif    (0–1 risk surface)               ║
║  └── alos_slope.tif        (slope in degrees)               ║
╚══════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════╗
║  KEY FINDING                                                 ║
║                                                             ║
║  Zero-shot SAM produced over-segmented output:              ║
║  dominant polygon spans ~9km × 11km (full AOI)              ║
║  → model merged all disturbance types into one mask         ║
║  → cannot distinguish landslide from flood/erosion          ║
║  → domain adaptation required for accurate mapping          ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Variable Definitions

| Variable | Physical Meaning | Threshold | Rationale |
|---|---|---|---|
| dNDVI | Vegetation index change (pre − post) | > 0.4 | Captures major vegetation removal events |
| Slope | Terrain gradient in degrees | > 20° | Minimum slope for landslide initiation |
| Combined mask | dNDVI AND slope | Both conditions | Physically: changed vegetation on steep terrain |

---

## Technology Stack

```
Python 3.13
├── rioxarray       — raster I/O, reprojection, bbox clip
├── xarray          — multi-band array operations
├── numpy           — gradient calculation, thresholding
├── pystac-client   — STAC API querying
├── planetary-computer — PC authentication
├── samgeo          — SAM geospatial wrapper
├── segment-anything — SAM model (Meta AI)
├── torch           — SAM backend
└── geopandas       — GeoJSON export

R
├── terra           — raster operations, distance analysis
└── sf              — vector operations, CRS transformation
```

*Source files: main.py, data_fetcher.py, change_detection.py, segmentation.py, validation.R*
