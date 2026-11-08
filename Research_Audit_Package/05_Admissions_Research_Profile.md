# 05 — Admissions Research Profile
## Researcher: Nazar E Imam
## Project: Landslide+SAM Detection Pipeline

---

## THREE-SENTENCE PROJECT SUMMARY

I built an automated pipeline that detects post-event landslide-affected areas by combining spectral vegetation change detection (dNDVI) and terrain slope analysis from Sentinel-2 and ALOS DEM data, using Microsoft Planetary Computer's STAC API, to generate geographic point prompts for the Segment Anything Model (SAM), which then delineates change boundaries as vector polygons. The pipeline operates without labeled training data, runs end-to-end from a single Python script, and produces landslide boundary polygons and a susceptibility raster, requiring a manual library patch to adapt SAM for geospatial use. The results demonstrated that while the physical filtering approach was methodologically appropriate, zero-shot SAM produced over-segmented output on a severely disturbed post-hurricane scene, revealing that foundation models require either domain adaptation or significantly constrained prompting strategies to perform accurately in geospatial disturbance detection.

---

## DETAILED RESEARCH SUMMARY (~400 words)

Rapid, accurate mapping of landslide-affected areas following extreme events is critical for disaster response and risk assessment, but traditional approaches relying on manual interpretation or field surveys are too slow to be operationally useful. This project investigated whether a free-data, no-training-label automated detection pipeline could be constructed by combining satellite-derived spectral change analysis with a pre-trained foundation segmentation model.

The pipeline processes Sentinel-2 Level-2A multispectral imagery (10 m, Bands B02/B03/B04/B08) and ALOS World 3D DEM data (30 m), both accessed through Microsoft Planetary Computer's STAC API. A pre-event scene from September 2024 and post-event scene from October 2024 covering a 0.1° × 0.1° bounding box in western North Carolina were acquired and processed. Change detection was performed by computing the difference in NDVI between epochs (dNDVI) and applying a dual threshold (dNDVI > 0.4 AND terrain slope > 20°), based on the physical reasoning that landslides remove vegetation from steep terrain. Pixels satisfying both conditions generated geographic point prompts that were passed to Meta AI's Segment Anything Model (vit_b variant), which delineated object boundaries around those locations without any task-specific training. Outputs were vectorized to GeoJSON and a susceptibility surface was computed in R using a weighted combination of slope and proximity to detections.

The pipeline ran successfully and produced all expected output files. However, the dominant segmentation output was a single polygon spanning nearly the full study area — a geometrically implausible result indicating that SAM merged multiple disturbance types across a severely disturbed post-hurricane scene into a single mask rather than identifying individual landslide bodies. A planned quantitative validation against a historical reference inventory was not completed, as the inventory was not acquired.

The project demonstrated three things clearly. First, an end-to-end detection pipeline using only free public data and zero-shot AI is technically feasible. Second, physical pre-filtering of AI prompts (slope + dNDVI) is a principled design decision but insufficient to prevent over-segmentation under extreme scene conditions. Third, and most importantly, SAM has no understanding of physical processes — it responds to visual contrast, not geomorphic mechanism — meaning that segmentation output cannot be interpreted as evidence of landslide occurrence without independent validation and domain adaptation.

These limitations define the natural next research steps: fine-tuning SAM on labeled landslide remote sensing data, integrating hydroclimatic trigger variables for disturbance-type attribution, and developing physics-informed models that generalize across events and geographies.

---

## THREE CV BULLET POINTS

- **Developed an automated post-event landslide detection pipeline** integrating Sentinel-2 multispectral change detection, ALOS DEM terrain analysis, and Segment Anything Model (SAM vit_b) boundary delineation via Microsoft Planetary Computer STAC API; produced vector polygon outputs and a susceptibility raster for a ~100 km² study area in western North Carolina (Python, R, rioxarray, samgeo, terra/sf)

- **Designed a physics-guided AI prompting strategy** combining NDVI temporal differencing (dNDVI > 0.4) with slope conditioning (>20°) to constrain SAM prompt locations to geomorphically plausible landslide initiation zones, demonstrating methodological integration of domain physical knowledge with zero-shot foundation model inference

- **Identified over-segmentation failure mode** in zero-shot SAM applied to post-disaster remote sensing scenes and implemented library-level debugging (samgeo predictor patch, PROJ version resolution) to enable execution of the complete pipeline; results revealed fundamental limitations of zero-shot foundation models for geophysical disturbance delineation without domain adaptation

---

## MASTER'S LETTER OF MOTIVATION — RESEARCH PARAGRAPH

Working with post-event Sentinel-2 imagery and ALOS terrain data, I built a pipeline that detects candidate landslide areas by combining temporal NDVI change analysis with slope thresholding, then uses those detections as prompts for Meta AI's Segment Anything Model to delineate change boundaries without requiring labeled training data. The pipeline ran successfully and produced vector polygons covering a ~100 km² area in western North Carolina following the September 2024 storm period. The result, however, exposed a problem I had not anticipated: the model produced a single large polygon spanning nearly the entire study area, merging flood-affected terrain, debris flows, and bare-soil exposures into one boundary rather than identifying individual landslide scars. This happened because SAM responds to visual image contrast, not to physical process — it had no way to distinguish between disturbance types that look similar spectrally. That failure made it clear that accurate, scientifically meaningful disturbance mapping requires models that incorporate physical environmental knowledge rather than simply detecting where an image looks different. That is the question I want to pursue at the graduate level.

---

## PHD FACULTY OUTREACH PARAGRAPH

**[Template — to be adapted with specific faculty research details]**

My interest in your work on [remote sensing / GeoAI / Earth observation] stems from a specific problem I encountered building an automated landslide detection pipeline. I combined Sentinel-2 spectral change detection with slope-conditioned SAM prompting to identify post-event disturbance areas, but found that zero-shot SAM produced over-segmented output that could not distinguish landslides from flood inundation or erosion — because the model responds to visual contrast without any representation of physical mechanism. This raised the question of how foundation models for geospatial disturbance mapping can be conditioned on environmental-process information, rather than image appearance alone. I would be interested in exploring this within your laboratory's research on [interpretable AI / Earth observation / physics-informed modeling], where I think the problem of physically grounded, transferable disturbance attribution connects directly to your work on [specific faculty topic].

---

## RESEARCH SKILLS DEMONSTRATED

| Skill | Evidence |
|---|---|
| Satellite remote sensing | Sentinel-2 acquisition, preprocessing, spectral indices |
| Terrain analysis | DEM-based slope derivation, spatial derivatives |
| Geospatial data processing | rioxarray, xarray, geopandas, CRS handling |
| STAC / cloud geospatial APIs | Microsoft Planetary Computer, pystac-client |
| Foundation AI model integration | SAM (samgeo), zero-shot inference, prompt engineering |
| Python pipeline development | Modular 3-phase pipeline, skip logic, Dask chunking |
| R spatial analysis | terra, sf, raster operations, vector-raster interaction |
| Library debugging | samgeo predictor patch, PROJ version resolution |
| Scientific reasoning | Physical threshold selection, limitation analysis |
| Research self-assessment | Honest identification of over-segmentation failure |

---

## POTENTIAL FACULTY RESEARCH DIRECTIONS

| Research Area | Connection Strength | Specific Connection |
|---|---|---|
| GeoAI and Foundation Models | Strong | SAM adaptation, prompt engineering, domain transfer |
| Remote Sensing and EO | Strong | Sentinel-2 processing, change detection, spectral analysis |
| Natural Hazards and Disaster Resilience | Strong | Landslide detection, post-event mapping, susceptibility |
| Interpretable/Explainable AI | Medium | SAM black-box limitation motivates interpretability research |
| Causal Inference in Earth Science | Medium | Attribution of disturbance type to triggering factors |
| Physics-informed AI | Medium | Gap between current prototype and physically grounded model |
| Hydrology / Ecohydrology | Weak-Medium | Soil moisture and precipitation as trigger variables |
| Urban GIS Applications | Weak | Not demonstrated in this project |

---

## MASTER'S RESEARCH QUESTION

**Can parameter-efficient fine-tuning of SAM on labeled Sentinel-2 landslide imagery produce a domain-adapted segmentation model that achieves measurably higher detection accuracy and geographic transferability compared to zero-shot SAM for post-event landslide mapping?**

Scope: 1–2 training events, 2–3 test events in different regions, using Landslide4Sense or equivalent labeled dataset. Evaluation: IoU, F1, cross-event generalization. Feasible within 18–24 months.

---

## PHD RESEARCH QUESTION

**How can physical slope-stability knowledge and hydroclimatic triggering variables be integrated into a foundation model architecture to produce disturbance-type-attributing, geographically transferable predictions that are both accurate and physically interpretable — moving beyond detection of where a surface changed to scientific attribution of why it changed?**

Extension of Master's: adds physics-informed constraints, causal inference analysis, multi-class disturbance attribution, and cross-regional generalization testing.

---

## INTERVIEW PREPARATION QUESTIONS AND ANSWERS

See `07_Questions_For_Project_Owner.md` for unconfirmed personal details that should be resolved before any interview.

**Q1: What scientific problem did your project address?**
A: The project attempted to detect and map landslide-affected areas after an extreme event using freely available satellite data and a pre-trained AI model (SAM), without requiring any labeled landslide training data. The core scientific problem was whether a physics-guided prompting strategy could make a general-purpose foundation model useful for domain-specific geohazard mapping.

**Q2: Why did you choose dNDVI and slope as your two variables?**
A: NDVI captures photosynthetically active vegetation biomass — a landslide removes forest cover and exposes bare soil, causing a sharp drop. Using the pre/post difference (dNDVI) isolates change rather than absolute state. Slope conditioning is physically motivated: landslides almost exclusively initiate on slopes above a minimum angle (~15–20°), so a slope threshold eliminates flat-area disturbances like floods or agricultural changes that would otherwise generate false positives.

**Q3: Why did you use SAM and not a supervised classifier?**
A: The primary reason was data scarcity — no labeled landslide inventory for the study area existed. SAM's zero-shot capability means it can delineate boundaries without task-specific training. The tradeoff is that it knows nothing about landslide morphology; it responds only to visual contrast. I used the change detection output to guide SAM's prompts rather than applying it blindly to the full image.

**Q4: What went wrong with the segmentation output?**
A: The dominant output polygon is far too large — it spans nearly the entire 100 km² study area, which is geometrically inconsistent with individual landslide bodies that are typically 0.01–1 km² in the Blue Ridge. The most likely explanation is that when many point prompts are distributed across a severely and continuously disturbed scene, SAM merges adjacent changed regions into a single large mask. This is a known limitation of SAM on images where disturbance is spatially contiguous rather than isolated.

**Q5: Why was no validation performed?**
A: The validation code was written (F1 precision/recall function in R) and was designed to compare detected polygons against a reference inventory. However, the reference inventory file was never acquired. This is the most significant gap in the project — without reference data, no accuracy claim can be made.

**Q6: What would you do differently?**
A: Before running the pipeline, I would acquire or digitize a reference inventory, even if small, to enable at minimum a qualitative and simple area-overlap validation. I would also investigate fine-tuning SAM on a public landslide dataset before applying it zero-shot, and I would add Sentinel-1 SAR data to provide a cloud-penetrating signal for cloud-affected post-storm scenes.

**Q7: What does the susceptibility map actually represent?**
A: It is a heuristic weighted surface: 60% slope (normalized) plus 40% proximity to detected change (normalized). It is not statistically calibrated and the weights are arbitrary. It provides a qualitative sense of relative spatial risk given the inputs but should not be interpreted as a validated probability of landslide occurrence.

**Q8: Can this pipeline generalize to other regions or events?**
A: It has not been tested anywhere else. The thresholds (dNDVI > 0.4, slope > 20°) are hardcoded and were not calibrated to the study area. SAM's zero-shot behavior might differ in other biomes or under different disturbance severities. Geographic transferability is entirely unknown.

**Q9: What programming and tools did you use?**
A: Python 3.13 with rioxarray, xarray, numpy, pystac-client, planetary-computer, samgeo, segment-anything, geopandas, and torch. R with terra and sf. Development was on a personal Windows machine; a significant portion of setup time involved debugging PROJ library version conflicts.

**Q10: How does this project connect to your PhD research interests?**
A: The project showed me concretely where existing AI tools break down when applied to physical environmental problems: SAM cannot distinguish a landslide from a flood because it has no knowledge of physical mechanisms. That gap — between AI tools that detect patterns and AI systems that understand physical processes — is what I want to investigate at the graduate level. Specifically, I am interested in how physical knowledge and causal structure can be incorporated into foundation models to make their predictions not just accurate but environmentally meaningful and transferable.
