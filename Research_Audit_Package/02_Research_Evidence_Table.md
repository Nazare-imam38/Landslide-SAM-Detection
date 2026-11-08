# 02 — Research Evidence Table
## Project: Landslide+SAM Detection Pipeline

All claims are classified as:
- **VERIFIED** — Directly supported by source code, results, or reliable documentation
- **PARTIALLY SUPPORTED** — Some evidence exists but validation or documentation is incomplete
- **PROPOSED** — Mentioned or planned but not implemented
- **NOT VERIFIED** — No sufficient supporting evidence located

---

| # | Claim | Actual Evidence | File Path | Function / Section | Evidence Status | Limitation |
|---|---|---|---|---|---|---|
| 1 | Sentinel-2 L2A imagery was acquired for September 2024 | Pre-event GeoTIFF exists on disk | `data/pre/sentinel_best_2024-09-01_2024-09-30.tif` | `data_fetcher.py → fetch_sentinel_imagery()` | **VERIFIED** | Single best scene, no pixel-level QA |
| 2 | Sentinel-2 L2A imagery was acquired for October 2024 | Post-event GeoTIFF exists (~8,113 KB) | `data/post/sentinel_best_2024-10-01_2024-10-31.tif` | `data_fetcher.py → fetch_sentinel_imagery()` | **VERIFIED** | Single best scene, no pixel-level QA |
| 3 | Bands B02, B03, B04, B08 were used | Explicit in data_fetcher.py asset list | `data_fetcher.py` line: `assets_to_download = ["B02", "B03", "B04", "B08"]` | `fetch_sentinel_imagery()` | **VERIFIED** | — |
| 4 | Microsoft Planetary Computer STAC API was used | API URL hardcoded in two modules | `data_fetcher.py`, `change_detection.py` | `pystac_client.Client.open(...)` | **VERIFIED** | Requires active API access |
| 5 | Scenes filtered by cloud cover <10% | API query parameter explicit | `data_fetcher.py` | `query={"eo:cloud_cover": {"lt": 10}}` | **VERIFIED** | Scene-level filter only; pixel clouds possible |
| 6 | ALOS World 3D DEM was fetched from Planetary Computer | Slope output file exists; fetch code present | `data/dem/alos_slope.tif`, `change_detection.py` | `get_alos_dem()` | **VERIFIED** | First result used without selection criteria |
| 7 | Slope was calculated using numpy central difference | Code explicit | `change_detection.py` | `get_alos_dem()`: `dx, dy = np.gradient(data_vals)` | **VERIFIED** | Simplified gradient; ~30m resolution assumed |
| 8 | dNDVI threshold of 0.4 applied | Hardcoded in function signature and mask | `change_detection.py` | `generate_prompts(..., dndvi_threshold=0.4, ...)` | **VERIFIED** | Threshold not calibrated to study area |
| 9 | Slope threshold of 20 degrees applied | Hardcoded in function signature and mask | `change_detection.py` | `generate_prompts(..., slope_threshold=20)` | **VERIFIED** | Threshold not calibrated |
| 10 | Up to 100 point prompts sampled from mask | Explicit step calculation | `change_detection.py` | `step = max(1, len(coords) // 100)` | **VERIFIED** | Sampling reduces spatial coverage |
| 11 | SAM vit_b was used for segmentation | Model type hardcoded | `segmentation.py`, `verify_env.py` | `SamGeo(model_type="vit_b")` | **VERIFIED** | Not fine-tuned on remote sensing data |
| 12 | SAM was used as zero-shot (no training) | No training code anywhere in project | All files | — | **VERIFIED** | SA-1B training domain mismatch |
| 13 | samgeo predictor bug was manually patched | Explicit patch code present | `segmentation.py` | Lines: `if not hasattr(sam, 'predictor'):` | **VERIFIED** | Indicates library version issue |
| 14 | Mask was merged across N prompts using np.max | Explicit in code | `segmentation.py` | `mask = np.max(mask, axis=0)` | **VERIFIED** | Merging loses per-prompt attribution |
| 15 | landslide_mask.tif was saved as uint8 | Explicit cast | `segmentation.py` | `mask_uint8 = (mask > 0).astype(np.uint8)` | **VERIFIED** | — |
| 16 | landslides.geojson exists in EPSG:32617 | File present; CRS in header | `data/results/landslides.geojson` | GeoJSON `crs` property | **VERIFIED** | Over-segmentation likely |
| 17 | susceptibility.tif was produced | File exists | `data/results/susceptibility.tif` | `validation.R → generate_susceptibility_heatmap()` | **VERIFIED** | Uncalibrated weights |
| 18 | Susceptibility weights are 0.6 (slope) + 0.4 (proximity) | Hardcoded | `validation.R` | `heatmap <- (0.6 * slope_norm) + (0.4 * dist_norm)` | **VERIFIED** | Arbitrary; no statistical basis |
| 19 | F1 score function was written | Code present | `validation.R` | `calculate_f1_score()` | **VERIFIED** | Never called with real data |
| 20 | F1 score was computed against reference data | **No evidence** | — | — | **NOT VERIFIED** | Reference inventory absent |
| 21 | Reference inventory exists for validation | File missing from directory | `data/inventory/historical_landslides.gpkg` | `validation.R` (commented) | **NOT VERIFIED** | Critical gap |
| 22 | Any quantitative accuracy metric was produced | No metric files found anywhere | — | — | **NOT VERIFIED** | No validation performed |
| 23 | Project was motivated by Hurricane Helene | Not stated in any file | — | — | **NOT VERIFIED** | Strong inference from dates/location |
| 24 | Project is self-directed with no supervisor | No institutional markers in any file | — | — | **PARTIALLY SUPPORTED** | Needs personal confirmation |
| 25 | Pipeline was run to completion by Nazar | Output files exist; no git history | All output files in `data/results/` | — | **PARTIALLY SUPPORTED** | No timestamp/commit evidence |
| 26 | Study area is western North Carolina | Bbox [-82.5,35.5,-82.4,35.6] verified | `data_fetcher.py`, `change_detection.py` | `bbox` variable in both files | **VERIFIED** | — |
| 27 | SAM produces over-segmentation on this scene | Inferred from polygon geometry | `data/results/landslides.geojson` | Main polygon extent | **PARTIALLY SUPPORTED** | Not formally measured |
| 28 | stackstac was deliberately avoided | In requirements but not called | `requirements.txt`, all .py files | — | **PARTIALLY SUPPORTED** | Likely PROJ conflict reason |
| 29 | PROJ path was manually hardcoded | Explicit in main.py | `main.py` lines 4-8 | `os.environ['PROJ_LIB']` | **VERIFIED** | Non-portable configuration |
| 30 | Python 3.13 was used | Inferred from __pycache__ filenames | `__pycache__/*.cpython-313.pyc` | — | **VERIFIED** | — |
| 31 | GPU/CUDA availability | torch.cuda.is_available() called | `verify_env.py` | `verify_system()` | **PARTIALLY SUPPORTED** | Result not recorded in any file |
| 32 | No collaborators contributed | No multi-author markers anywhere | — | — | **PARTIALLY SUPPORTED** | Needs personal confirmation |
| 33 | New algorithm or model was developed | **No evidence** | — | — | **NOT VERIFIED** | Existing tools combined in pipeline |
| 34 | Results are scientifically validated | **No evidence** | — | — | **NOT VERIFIED** | Validation not completed |

---

### Summary Count

| Status | Count |
|---|---|
| VERIFIED | 20 |
| PARTIALLY SUPPORTED | 7 |
| NOT VERIFIED | 7 |
| PROPOSED | 0 |

---

*Note: "NOT VERIFIED" does not mean the claim is false. It means the available project files do not provide sufficient evidence to confirm it.*
