# 01 — Complete Research Audit
## Project: Landslide+SAM Detection Pipeline
### Researcher: Nazar E Imam
### Audit Date: October 2026

---

## 1. PROJECT IDENTITY AND OBJECTIVES

| Field | Value |
|---|---|
| Project name | Landslide Detection Pipeline (informal: Landslide+SAM) |
| Domain | Geospatial AI, Remote Sensing, Natural Hazard Detection |
| Language(s) | Python 3.13, R |
| Status | Exploratory prototype — pipeline runs, outputs exist, validation incomplete |
| Institutional context | None confirmed. All evidence points to self-directed personal project |
| Year | No earlier than late 2024 (data windows Sep–Oct 2024) |
| Supervision | None identified in any file |
| Collaborators | None identified |
| Publication status | Not submitted |

**Reconstructed objective:**
Develop an automated end-to-end pipeline that detects and delineates landslide-affected areas from freely available satellite and elevation data, combining spectral change detection with AI-based boundary segmentation, without requiring labeled landslide training data.

---

## 2. SCIENTIFIC BACKGROUND

Landslides are destructive hazards in steep mountainous terrain, tightly coupled to extreme precipitation. Rapid post-event mapping is critical for emergency response. Manual mapping is slow; automated remote sensing offers a scalable alternative.

A landslide strips vegetation and exposes bare soil, producing a measurable drop in NDVI. Combined with terrain slope, this spectral change provides a physically grounded detection signal.

SAM (Segment Anything Model, Meta AI, 2023) is a promptable foundation model trained on ~11M natural images. Its zero-shot generalization is attractive for geospatial applications where labeled training data is scarce.

**Core research question:**
> Can spectral change detection (dNDVI) combined with terrain conditioning (slope) and a foundation segmentation model (SAM) produce landslide boundary maps from public satellite and DEM data, without requiring labeled landslide training data?

**Study area:** Western North Carolina, bbox `[-82.5, 35.5, -82.4, 35.6]`, ~100 km², Blue Ridge Mountains. Time window: September–October 2024. Consistent with Hurricane Helene impact zone (late September 2024) — **inferred, not explicitly stated in code**.

---

## 3. DATASETS

### 3.1 Sentinel-2 L2A — Pre-Event

| Field | Detail |
|---|---|
| Source | Microsoft Planetary Computer STAC API |
| Collection | `sentinel-2-l2a` |
| Period | 2024-09-01 / 2024-09-30 |
| Bands | B02, B03, B04, B08 (Blue, Green, Red, NIR) |
| Resolution | 10 m |
| Cloud filter | <10% cloud cover; lowest-cloud scene selected |
| Output | `data/pre/sentinel_best_2024-09-01_2024-09-30.tif` |
| Preprocessing | STAC query → sort by cloud cover → band extraction → bbox clip → concat → GeoTIFF |
| Evidence | `data_fetcher.py` |

### 3.2 Sentinel-2 L2A — Post-Event

| Field | Detail |
|---|---|
| Period | 2024-10-01 / 2024-10-31 |
| Output | `data/post/sentinel_best_2024-10-01_2024-10-31.tif` (~8,113 KB) |
| Role | Reference grid for reprojection; primary SAM input |
| Evidence | `data_fetcher.py` |

### 3.3 ALOS World 3D DEM (AW3D30)

| Field | Detail |
|---|---|
| Source | Microsoft Planetary Computer, `alos-dem` collection |
| Resolution | ~30 m |
| Variables | Elevation (m); slope derived numerically |
| Output | `data/dem/alos_slope.tif` |
| Preprocessing | Fetch → clip → numpy gradient → arctan slope → GeoTIFF |
| Evidence | `change_detection.py` |

### 3.4 Reference Landslide Inventory — NOT PRESENT

| Field | Detail |
|---|---|
| File | `data/inventory/historical_landslides.gpkg` |
| Purpose | Reference polygons for F1/precision/recall |
| Status | **File does not exist in project directory** |
| Evidence | Referenced in commented code in `validation.R` |

### 3.5 Derived Variables

| Variable | Source | Formula | Threshold |
|---|---|---|---|
| NDVI pre | B08, B04 | (NIR-Red)/(NIR+Red) | — |
| NDVI post | B08, B04 | Same | — |
| dNDVI | NDVI_pre − NDVI_post | Pixel subtraction | > 0.4 |
| Slope | ALOS DEM | arctan(|∇z|/30) × 180/π | > 20° |
| Susceptibility | slope_norm + proximity_norm | 0.6×slope + 0.4×proximity | — |

**Data integration:** Spatial reprojection matching via `rioxarray.rio.reproject_match()`. All rasters aligned to post-event Sentinel-2 grid.

---

## 4. COMPLETE RESEARCH METHODOLOGY

### Workflow

```
[Problem: Automated landslide detection without labeled training data]
        |
        v
[PHASE 1: Data Acquisition] ← data_fetcher.py
  1. Connect to Microsoft Planetary Computer STAC API
  2. Query sentinel-2-l2a: bbox + date range + cloud_cover < 10
  3. Sort results by cloud cover, select minimum
  4. Open B02, B03, B04, B08 via rioxarray URL
  5. Clip each band to study bbox
  6. Concatenate bands → 4-band xarray
  7. Export as GeoTIFF (pre-event, post-event)
        |
        v
[PHASE 2a: Slope Derivation] ← change_detection.py → get_alos_dem()
  8. Query alos-dem collection, select first item
  9. Open and clip DEM raster
  10. numpy.gradient(elevation) → dx, dy
  11. slope = arctan(sqrt(dx²+dy²)/30) × 180/π
  12. Save as slope GeoTIFF
        |
        v
[PHASE 2b: Change Detection] ← change_detection.py → generate_prompts()
  13. Load pre/post GeoTIFFs with Dask chunking
  14. Reproject pre and slope to post-event grid
  15. NDVI_pre = (B08-B04)/(B08+B04) [band index 4 and 1]
  16. NDVI_post = same
  17. dNDVI = NDVI_pre - NDVI_post
  18. dNDVI.compute() — Dask → NumPy
  19. mask = (dNDVI > 0.4) AND (slope > 20°)
  20. coords = numpy.argwhere(mask)
  21. Sample every nth point, max 100 prompts
  22. Convert pixel indices to lon/lat coordinates
        |
        v
[PHASE 3: SAM Segmentation] ← segmentation.py → run_segmentation()
  23. Initialize SamGeo(model_type="vit_b")
  24. Patch missing predictor attribute if needed
  25. sam.set_image(post_event_tif)
  26. sam.predict(point_coords, point_labels=[1...], point_crs)
  27. Unpack nested mask structure recursively
  28. If mask.shape = (N,H,W): np.max(mask, axis=0)
  29. Cast to uint8 binary
  30. sam.save_prediction(landslide_mask.tif)
  31. sam.tiff_to_geojson(landslide_mask.tif, landslides.geojson)
        |
        v
[PHASE 4: Susceptibility Mapping] ← validation.R
  32. Load slope.tif and landslides.geojson with terra/sf
  33. slope_norm = slope / max(slope)
  34. dist_raster = terra::distance(slope, detections)
  35. dist_norm = 1 - (dist_raster / max(dist_raster))
  36. susceptibility = 0.6×slope_norm + 0.4×dist_norm
  37. Write susceptibility.tif
        |
        v
[OUTPUTS]
  - landslides.geojson (EPSG:32617, polygon features)
  - landslide_mask.tif (binary raster)
  - susceptibility.tif (0–1 risk surface)
  - alos_slope.tif (slope in degrees)
```

### Key Methodological Decisions

1. **STAC + rioxarray direct URL access** (not stackstac): `stackstac` is in requirements but avoided in implementation — evidence of a deliberate decision to bypass it due to PROJ version conflicts on Windows (documented by `find_proj.py` and hardcoded PROJ_LIB in `main.py`).

2. **Monthly best-scene selection**: Simple cloud-rank selection rather than medoid compositing or pixel-quality masking. Practical choice for a prototype but scientifically coarser.

3. **Dual-threshold change detection**: dNDVI > 0.4 AND slope > 20°. These thresholds are domain-informed (vegetation loss + gravitational susceptibility) but not calibrated to the study area. No sensitivity analysis was performed.

4. **Dask chunking**: `chunks=True` in rioxarray open calls — evidence of deliberate memory management for large GeoTIFFs.

5. **SAM vit_b (not vit_l or vit_h)**: Smaller model chosen, likely for computational reasons on local hardware.

6. **Prompt sampling to 100 points**: Hard cap on SAM inputs — evidence of awareness that too many prompts can degrade performance or be computationally expensive.

7. **Manual samgeo bug patch**: The code explicitly checks for a missing `predictor` attribute and patches it — evidence of independent debugging and library adaptation.

---

## 5. AI / ML COMPONENTS

### SAM (Segment Anything Model, vit_b)

| Property | Detail |
|---|---|
| Model type | Foundation segmentation model — Vision Transformer Base |
| Usage mode | Zero-shot prompted inference — no training, no fine-tuning |
| Input | 4-band Sentinel-2 GeoTIFF + geographic point prompts |
| Output | Binary segmentation mask |
| Pre-training data | Meta SA-1B (natural photos — NOT remote sensing) |
| Adaptation | Physics-guided prompt strategy via upstream change detection filter |
| Evaluation | None |
| Novel contribution | Integration into physically constrained geospatial pipeline; not a new model |

**What SAM could not do:**
SAM is a visual boundary detector. It cannot confirm that a detected region is a landslide, explain why a slope failed, represent hydroclimatic triggering conditions, distinguish landslide from flood or erosion, or learn any physical environmental mechanism. The model responds to visual contrast in image patches; it does not understand the geophysical process. Segmentation accuracy, even if validated, would only measure boundary agreement with a reference map — not process understanding, causal attribution, or transferability.

---

## 6. RESULTS AND FINDINGS

### Produced Outputs

| Output | File | Status |
|---|---|---|
| Pre-event imagery | `data/pre/sentinel_best_2024-09-01_2024-09-30.tif` | Present |
| Post-event imagery | `data/post/sentinel_best_2024-10-01_2024-10-31.tif` | Present (~8 MB) |
| Slope raster | `data/dem/alos_slope.tif` | Present |
| Landslide mask | `data/results/landslide_mask.tif` | Present |
| Landslide polygons | `data/results/landslides.geojson` | Present, EPSG:32617 |
| Susceptibility raster | `data/results/susceptibility.tif` | Present |
| Validation metrics | — | **Not produced** |

### Spatial Findings

The GeoJSON output contains one very large polygon (bounding ~9 km × 11 km in UTM Zone 17N coordinates) with complex interior rings, plus ~60 smaller discrete polygons. The dominant polygon's extent spans nearly the entire study AOI. This is geometrically inconsistent with individual landslide scars, which are typically 0.01–1 km² in the Blue Ridge. This pattern is consistent with SAM over-segmentation: with multiple prompts scattered across a severely disturbed scene, SAM merges adjacent changed areas into a single large mask.

### Quantitative Performance

**No verified quantitative performance evaluation was found.**

The `validation.R` script contains a working F1/precision/recall function based on area overlap. However, the reference inventory file (`historical_landslides.gpkg`) is absent from the project directory. The function was never called with real data. No metrics of any kind were computed.

### What the Project Demonstrated

1. A fully automated pipeline from satellite data download to vector polygon output is technically feasible using only free data and no labeled training data.
2. The dual-threshold change detection approach is physically meaningful but insufficient to discriminate disturbance types.
3. SAM, used with spectral prompts on a severely disturbed post-disaster scene, produces over-segmented output that conflates multiple disturbance types.
4. Without a reference inventory, no scientific claim about detection accuracy is defensible.

---

## 7. CONTRIBUTION AND MATURITY

### Contribution Classification

| Contribution | Classification | Evidence |
|---|---|---|
| End-to-end automated detection pipeline | VERIFIED (Technical) | Source code + outputs |
| Physics-guided SAM prompt strategy | PARTIALLY SUPPORTED (Methodological) | Implemented but not evaluated |
| Susceptibility heatmap from detections | VERIFIED (Technical) | validation.R + susceptibility.tif |
| Quantitative landslide detection accuracy | NOT VERIFIED | No reference data |
| Novel algorithm or model development | NOT VERIFIED | Existing tools combined |
| Scientific finding about landslide distribution | NOT VERIFIED | No validated output |

### Research Maturity: Exploratory Prototype

The pipeline exceeds a classroom exercise (it integrates five separate data/computation layers across two languages and required non-trivial debugging). It falls short of completed applied research because validation is absent. No journal submission is appropriate in current state.

---

## 8. LIMITATIONS

| # | Limitation | Type |
|---|---|---|
| 1 | No validated reference inventory | Observed |
| 2 | Quantitative metrics not computed | Observed |
| 3 | SAM not fine-tuned on remote sensing imagery | Observed |
| 4 | Over-segmentation in dominant output polygon | Observed (inferred) |
| 5 | Cannot distinguish landslide from flood/erosion/clearcut | Observed (structural) |
| 6 | Heuristic susceptibility weights, uncalibrated | Observed |
| 7 | Single best-scene monthly composite, no pixel QA | Observed |
| 8 | 30m DEM vs 10m imagery resolution mismatch | Observed |
| 9 | No hydroclimatic trigger variables | Observed (structural) |
| 10 | No TWI, curvature, aspect, geology, drainage | Observed (structural) |
| 11 | Single study area, single event | Observed |
| 12 | No uncertainty quantification | Observed |
| 13 | Geographic transferability untested | Unknown |
| 14 | Susceptibility model circularly depends on detection errors | Observed (structural) |

---

## 9. PERSONAL CONTRIBUTIONS (Nazar E Imam)

No git history or commit authorship is available in the workspace. Attribution is based on single-developer code structure and absence of any multi-author markers.

| Task | Attribution | Evidence |
|---|---|---|
| Pipeline architecture (main.py) | Confirmed personal | Single-author code style |
| STAC data acquisition module | Confirmed personal | data_fetcher.py |
| Change detection + slope module | Confirmed personal | change_detection.py |
| SAM segmentation module | Confirmed personal | segmentation.py |
| samgeo bug patch | Confirmed personal | Explicit patch code in segmentation.py |
| R validation + susceptibility | Confirmed personal | validation.R |
| PROJ environment debugging | Confirmed personal | find_proj.py, main.py |
| Running pipeline to completion | Likely personal (output files exist) | Needs confirmation |
| Visual inspection of outputs | Unknown | No documentation found |
| Reference inventory acquisition | Not performed | File missing |

---

## 10. REPRODUCIBILITY

**Classification: Medium**

The pipeline is deterministic and fully automated. Re-running `main.py` produces the same outputs given the same API access and environment. Dependency on Planetary Computer API access and a specific Windows PROJ configuration reduces practical reproducibility for others. No Docker, conda environment file, or platform-agnostic setup is provided.

---

*Scientific accuracy audit: All claims grounded in source code, output files, or clearly labelled inference. No information was invented.*
