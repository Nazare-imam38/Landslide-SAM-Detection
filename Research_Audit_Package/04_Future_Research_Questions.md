# 04 — Future Research Questions
## Project: Landslide+SAM Detection Pipeline

---

## INTRODUCTION

The three research questions below emerge directly from limitations and gaps demonstrated by the Landslide+SAM project. Each is motivated by a specific finding or structural gap. None are generic AI-in-GIS questions.

---

## RESEARCH QUESTION 1 (Master's Level)
### Can SAM be fine-tuned on labeled landslide remote sensing data to produce accurate, transferable landslide boundary delineation across geographically diverse events?

**Motivating finding/limitation:**
The Landslide+SAM pipeline demonstrated that zero-shot SAM, prompted with physical-threshold point locations, produces an over-segmented output when the study area has widespread severe disturbance. The model drew boundaries based on visual contrast in the Sentinel-2 image, not landslide morphology. The critical problem is the domain gap: SAM was trained on natural photographs, not multispectral remote sensing imagery. It has never seen a landslide scar.

**Why this problem matters:**
Landslide inventories are essential for risk assessment, but manual digitization is slow. If SAM could be fine-tuned with a modest labeled dataset of landslide polygons from Sentinel-2 or other satellite imagery, it could be deployed for rapid post-event mapping across regions. This directly addresses the current project's core failure mode.

**Proposed approach:**
1. Acquire a multi-event labeled landslide inventory (e.g., Bijukchhen et al. Landslide4Sense dataset; NASA COOLR; USGS post-Helene mapping if available)
2. Fine-tune SAM using parameter-efficient adaptation (e.g., LoRA or adapter layers) on labeled Sentinel-2 landslide patches
3. Evaluate on held-out events in different geographic regions (Nepal, California, Italy)
4. Compare against: (a) zero-shot SAM (current approach), (b) dNDVI thresholding alone, (c) U-Net trained on same data

**Possible datasets:**
- Landslide4Sense (Bijukchhen et al., 2022) — global Sentinel-2 landslide dataset
- NASA COOLR cooperative landslide repository
- BGS National Landslide Database (UK)
- USGS post-Helene rapid damage assessment (if public)

**Testable hypothesis:**
Fine-tuned SAM will achieve significantly higher IoU (>0.5) compared to zero-shot SAM (<0.2 estimated from over-segmentation observation) on an independent held-out landslide event dataset.

**Evaluation strategy:**
Intersection over Union (IoU), Precision, Recall, F1-score against digitized reference polygons. Cross-event and cross-region generalization tests.

**Expected contribution:**
Establishes whether fine-tuning SAM on a relatively small remote sensing dataset (hundreds to low thousands of labeled events) produces a domain-adapted foundation segmentation model useful for rapid landslide mapping. Methodologically, it would determine whether parameter-efficient fine-tuning of SAM is sufficient or whether full re-training is needed.

**Master's feasibility:** High. Fine-tuning SAM on a public labeled dataset is computationally feasible (university GPU cluster), methodologically well-scoped, and produces evaluable outputs within 18–24 months.

**PhD extension:** The fine-tuned model can be analyzed for interpretability — which image features activate the segmentation? Can attention maps reveal whether the model learns morphologically meaningful features (concave scar shape, elongated deposit geometry) or arbitrary texture correlations? This connects to interpretable GeoAI.

---

## RESEARCH QUESTION 2 (Master's Level)
### How can hydroclimatic triggering variables (precipitation intensity, antecedent soil moisture) be integrated with spectral change detection to improve the attribution of satellite-detected surface changes to specific disturbance types (landslide vs. flood inundation vs. erosion)?

**Motivating finding/limitation:**
The current pipeline cannot distinguish a landslide from a flood deposit, an erosion feature, or debris flow jams, because all produce similar dNDVI signals on steep terrain. The two-variable filter (dNDVI, slope) identifies change on slopes but provides no information about the triggering mechanism or disturbance type. This is the most fundamental scientific limitation of the project — it detects change, not landslides.

**Why this problem matters:**
Misclassified detections (flood pixels labeled as landslides, or vice versa) corrupt any inventory, misrepresent hazard distribution, and mislead risk assessment. In the Hurricane Helene context, widespread flooding and landsliding co-occurred; separating them from satellite data is a real scientific and operational problem.

**Proposed approach:**
1. Integrate storm precipitation data (GPM IMERG at 0.1°/30min) and antecedent soil moisture (SMAP L3 at ~36 km/daily or Sentinel-1-derived soil moisture) as auxiliary input variables
2. Build a multi-class classifier (e.g., Random Forest or XGBoost) using spectral change features + terrain features + hydroclimatic features as inputs, with landslide/flood/stable as target classes
3. Use SHAP values to identify which variables contribute most to each class prediction — this provides the interpretability layer
4. Train on a manually labeled subset; validate on held-out locations

**Possible datasets:**
- GPM IMERG (NASA) — precipitation
- SMAP (NASA) — soil moisture
- ALOS DEM derivatives (slope, TWI, curvature, aspect)
- Sentinel-1 SAR — cloud-penetrating, flood inundation mapping
- Hand-digitized labels from current project area

**Testable hypothesis:**
Adding hydroclimatic variables will improve multi-class classification F1-score (landslide vs. flood) by a statistically significant margin over spectral + terrain features alone.

**Evaluation strategy:**
Multi-class F1-score, confusion matrix, SHAP feature importance analysis, comparison with spectral-only baseline.

**Expected contribution:**
Demonstrates that disturbance-type attribution from satellite data requires hydroclimatic context, not just spectral and terrain signals. Provides an interpretable feature importance framework that could generalize to other event types and regions. Moves from "detecting change" toward "understanding what kind of change occurred and why."

**Master's feasibility:** Medium-high. Requires multi-source data integration and a labeled training set, but all data are freely available and the classification framework is well-established.

**PhD extension:** Replace the Random Forest with a physics-constrained neural network in which known physical relationships (e.g., slope stability criteria) constrain the model's decision boundary. Investigate whether physical constraints improve out-of-distribution generalization to events with different triggering conditions.

---

## RESEARCH QUESTION 3 (PhD Level)
### Can a spatiotemporal, process-aware AI model for post-disaster disturbance mapping be designed such that its predictions are physically interpretable, causally attributable to specific triggering conditions, and transferable to geographic regions and event types not represented in its training data?

**Motivating finding/limitation:**
Both limitations above converge on the same deeper problem: the current pipeline, and most existing remote sensing change detection methods, detect where change occurred but cannot explain why, cannot distinguish overlapping process types, and cannot transfer reliably to new events or regions. SAM is a black box with no environmental knowledge. The change detection thresholds are empirically chosen without physical calibration. Transferability is completely untested. This represents the gap between operational geospatial AI tools and scientifically grounded environmental intelligence.

**Why this problem matters:**
For landslide risk assessment to be scientifically credible and operationally useful across diverse regions, detection models must generalize beyond training conditions. This requires either very large training datasets (impractical for low-frequency events) or models that encode physical knowledge about slope stability, rainfall thresholds, and geomorphic processes so that they can reason from first principles about new environments.

**Proposed approach:**
1. Build on Research Questions 1 and 2 to establish validated detection and attribution benchmarks
2. Develop a physics-informed deep learning architecture in which slope stability criteria, rainfall intensity–duration thresholds, and geomorphic constraints are embedded as differentiable physical modules
3. Train on a geographically diverse multi-event dataset and evaluate transferability to held-out geographic regions using domain adaptation metrics
4. Apply causal discovery methods (e.g., PCMCI, Granger causality) to time-series of satellite observations and hydroclimatic variables to investigate whether detected changes are causally linked to specific triggering factors, or merely correlated

**Possible datasets:**
- Global landslide databases (NASA COOLR, GLC, Kirschbaum et al.)
- ERA5 reanalysis (precipitation, soil moisture, temperature)
- SRTM / ALOS / Copernicus DEM global terrain
- Multi-event Sentinel-1/2 time series

**Testable hypothesis:**
Physics-informed models will show significantly better geographic transferability (IoU drop <20% when tested on unseen regions) compared to data-only models (IoU drop >50%), because physical constraints act as a form of domain-invariant inductive bias.

**Evaluation strategy:**
Leave-one-region-out cross-validation. IoU, F1-score, calibration curves. Causal strength metrics from causal discovery analysis. Ablation study isolating contribution of physical constraints.

**Expected contribution:**
Original methodological contribution to the intersection of physics-informed machine learning, causal inference, and geospatial hazard modeling. Addresses a fundamental scientific problem: how to build AI systems for Earth observation that are not only accurate but physically meaningful and transferable.

**Master's feasibility:** The causal inference and physics-informed components make this PhD-level. A Master's could investigate the transferability component alone.

**PhD suitability:** High. Directly addresses open research problems in GeoAI, interpretable AI, and Earth system modeling.

---

## CONNECTING THE THREE QUESTIONS

```
Current project gap:
"SAM detected change but could not confirm process, explain mechanism,
or distinguish disturbance types"
        |
        v
RQ1: Can domain-adapted SAM accurately delineate landslide boundaries?
(Addresses: model domain gap, validation deficit)
        |
        v
RQ2: Can multi-variable classifiers attribute disturbance type using
hydroclimatic context?
(Addresses: process discrimination, interpretability)
        |
        v
RQ3: Can physics-informed, causally grounded AI generalize disturbance
detection across regions and event types?
(Addresses: transferability, physical meaningfulness, causal attribution)
```
