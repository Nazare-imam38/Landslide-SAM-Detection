# 03 — Research Contributions and Findings
## Project: Landslide+SAM Detection Pipeline

---

## WHAT WAS ACTUALLY ACCOMPLISHED

A fully automated, three-phase geospatial pipeline was designed and implemented in Python and R. The pipeline acquires cloud-filtered satellite imagery and terrain data from free public APIs, applies domain-informed spectral and terrain thresholding to identify candidate change locations, uses a pre-trained foundation segmentation model (SAM) to delineate boundaries around those locations, and produces vector polygon outputs and a continuous susceptibility raster. The pipeline runs end-to-end from a single entry point (`main.py`) and includes skip logic, memory-efficient Dask chunking, manual library debugging, and an independent R post-processing stage. All five output files exist on disk.

**This is more than a classroom exercise** in that it: integrates five independent data/computation layers; bridges Python and R; required real debugging of a third-party library bug; adapted a general-purpose AI model to a geospatial physical problem; and produced actual outputs from real satellite data covering a real post-disaster landscape. **It falls short of completed applied research** because no quantitative validation was performed and no reference inventory exists.

---

## VERIFIED FINDINGS

### Finding 1 — Technical
An end-to-end landslide detection pipeline is implementable using only free data (Planetary Computer), no labeled training data (SAM zero-shot), and standard open-source geospatial libraries. The pipeline successfully produces vector polygon outputs.
**Evidence:** All output files present. Source code functional.

### Finding 2 — Methodological
Combining dNDVI > 0.4 with slope > 20° provides a physically principled pre-filter for SAM prompting that reduces false positives from flat-area disturbances (floods, agriculture) and focuses detection on geomorphically plausible locations.
**Evidence:** `change_detection.py` dual-threshold mask logic. Domain knowledge embedded in threshold values.

### Finding 3 — Observational (inferred, not formally measured)
When a post-disaster scene has widespread severe disturbance (as in a major hurricane impact zone), SAM with scattered point prompts produces a single large over-segmented polygon rather than individual landslide scars. The dominant polygon in `landslides.geojson` spans nearly the full ~100 km² study AOI — geometrically inconsistent with individual landslide bodies in the Blue Ridge Mountains.
**Evidence:** GeoJSON geometry analysis. Polygon bounding coordinates span Easting ~363,950–373,170 m (~9 km), Northing ~3,929,390–3,940,620 m (~11 km).

### Finding 4 — Scientific gap (observational)
The pipeline cannot distinguish between landslide scars, river inundation, mass soil erosion, and other forms of disturbance that produce vegetation removal on steep terrain. All produce similar dNDVI signals, and SAM has no capacity to differentiate them.
**Evidence:** Only two variables used (dNDVI, slope). No multi-class output. No disturbance-type labels.

---

## DOCUMENTED PERSONAL CONTRIBUTIONS

| Contribution | Type | Confidence |
|---|---|---|
| Designed 3-phase pipeline architecture | Architectural | Confirmed personal |
| Implemented STAC-based Sentinel-2 acquisition | Technical | Confirmed personal |
| Implemented ALOS DEM fetch and slope derivation | Technical | Confirmed personal |
| Implemented dNDVI + slope change detection | Methodological + Technical | Confirmed personal |
| Implemented SAM segmentation with samgeo | Technical | Confirmed personal |
| Diagnosed and patched samgeo predictor bug | Technical debugging | Confirmed personal |
| Designed physics-guided prompt sampling strategy | Methodological | Confirmed personal |
| Implemented R susceptibility mapping | Technical | Confirmed personal |
| Wrote F1 score validation function | Technical | Confirmed personal |
| Debugged PROJ library conflicts on Windows | Environment | Confirmed personal |
| Ran pipeline to produce all output files | Operational | Likely personal — needs confirmation |

---

## SCIENTIFIC SIGNIFICANCE

**Honest assessment:**

The project demonstrates a valid idea — that foundation models can be directed toward specific physical problems through domain-informed prompting — but it does not prove the idea works well. The absence of validation means no scientific claim about accuracy can be made. The over-segmentation finding is scientifically interesting but was not investigated systematically.

The project's scientific significance lies in what it revealed about the problem:
- Spectral + terrain filtering is necessary but insufficient for disturbance-type attribution
- SAM's zero-shot performance degrades under severe, widespread scene disturbance
- The intersection of change detection and foundation model segmentation is a legitimate and underexplored research problem
- Validation data is the critical missing component, not algorithmic complexity

---

## METHODOLOGICAL ORIGINALITY

The methodology combines existing tools in a new way. It does not develop a new algorithm, a new model, or a new training procedure. The original elements are:

1. The specific integration strategy: using physical thresholds to generate SAM prompts (rather than using SAM on the full image or with arbitrary prompts)
2. The cross-language pipeline (Python for AI/geospatial processing, R for spatial statistics)
3. The susceptibility model that combines terrain and proximity-to-detection signals

None of these are publishable as novel algorithms. They are design decisions in a prototype pipeline.

**Classification:** Integration of existing methods in a new applied workflow.

---

## PRACTICAL IMPORTANCE

The approach is practically relevant for rapid post-disaster mapping in data-scarce environments: it requires no labeled training data, no specialized hardware beyond CPU inference, and only free publicly available data sources. If validated, a pipeline of this type could support disaster response workflows. In its current state, it is a proof of concept, not an operational tool.

---

## WHAT THE PROJECT DOES NOT DEMONSTRATE

- That detected polygons represent actual landslides (unvalidated)
- That SAM performs acceptably on Sentinel-2 imagery in general
- That the dNDVI/slope thresholds are optimal for this region
- That the susceptibility heatmap reflects true risk
- That the approach generalizes beyond western North Carolina in October 2024
- Any new algorithm, model architecture, or training procedure
- Any quantitative performance metric
