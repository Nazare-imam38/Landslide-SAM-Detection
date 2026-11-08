# 07 — Questions For Project Owner (Nazar E Imam)
## Must Be Resolved Before Using This Project in PhD/Master's Applications

---

## CRITICAL — Must answer before any application

These questions affect scientific claims, personal contribution statements, and application credibility. Answer them honestly before this project is cited in any SOP, LOM, CV, or faculty email.

---

### Q1. Was this project deliberately designed around Hurricane Helene?

**Why it matters:** If yes, you can state that the September–October 2024 study window was intentionally chosen to capture Hurricane Helene's landslide impact in western North Carolina. This is a scientifically significant context (Helene caused catastrophic landsliding, making it a landmark event for remote sensing research). If no, you should not claim it.

**What to say if yes:** "I designed the study window around Hurricane Helene's impact on western North Carolina in September–October 2024."
**What to say if no:** "The study window was September–October 2024 in western North Carolina; I became aware of the connection to Helene after setting those parameters."
**What to say if uncertain:** Do not make the Helene connection in writing until you are certain.

**Status:** NOT VERIFIED from project files.

---

### Q2. Was this completely self-directed, or was it connected to any course, university assignment, internship, or supervisor?

**Why it matters:** If it was a course project or assigned work, it must be described as such. Presenting assigned work as independent research is a serious credibility risk in graduate applications. If it was self-directed, that is a positive signal of initiative.

**What to say if self-directed:** "I built this as an independent personal project outside of any coursework or supervision."
**What to say if course-related:** Describe it accurately as a course or supervised project. It still has value — just different value.

**Status:** NOT VERIFIED from project files. No institutional markers found.

---

### Q3. Did you personally run the complete pipeline that produced the GeoJSON, mask TIF, and susceptibility TIF output files?

**Why it matters:** If you ran the pipeline, you can state that you executed the full workflow and produced the outputs. If the outputs were created differently (e.g., partial run, copied from somewhere, someone else ran it), that must be reflected accurately.

**Evidence available:** All five output files exist on disk. `__pycache__` `.cpython-313.pyc` files exist for the three main Python modules, confirming they were compiled and likely executed on this machine.

**What to say if yes:** "I ran the complete pipeline from data acquisition through segmentation and produced all output files."
**What to say if partially:** Describe exactly which phases you ran personally.

**Status:** PARTIALLY SUPPORTED (output files exist, no git timestamp or terminal log).

---

### Q4. Did you visually inspect the results against the Sentinel-2 imagery and independently recognize the over-segmentation problem?

**Why it matters:** If you identified the failure mode yourself by comparing the GeoJSON output to the satellite imagery, that demonstrates genuine scientific reasoning — you ran the model, evaluated its output, and formed an independent analytical judgment about its failure. This is a strong research skill signal.

If you only became aware of the over-segmentation observation through the research audit documents (this package), you should not claim to have independently identified it.

**What to say if you recognized it yourself:** "When I overlaid the output polygons on the Sentinel-2 imagery, I noticed the dominant polygon was far too large to represent individual landslide scars, suggesting SAM had merged multiple disturbance types."
**What to say if you did not:** Simply do not make this claim. You can still reference the limitation as a finding of the project analysis.

**Status:** NOT VERIFIED from any project file.

---

### Q5. Did the pipeline produce any error messages, warnings, or partial outputs that you had to work around?

**Why it matters:** The code contains a manual bug patch (`if not hasattr(sam, 'predictor')`), a hardcoded PROJ path, and `find_proj.py` and `verify_env.py` utility scripts — all of which suggest you encountered real technical problems and solved them. Describing this debugging experience specifically is valuable in applications as evidence of independent problem-solving.

**Questions to answer:**
- What error did the missing `predictor` attribute cause, and how did you diagnose it?
- What was the PROJ version conflict error message?
- How long did it take to get the full pipeline running?

**Status:** Bug patch VERIFIED in code. Context of discovery NEEDS CONFIRMATION.

---

### Q6. Was GPU (CUDA) available when you ran SAM?

**Why it matters:** SAM vit_b on CPU is slow (~minutes per image on a modern CPU). On GPU it is seconds. Knowing this affects how you describe the computational workflow and whether GPU availability is a reproducibility constraint.

**Evidence available:** `verify_env.py` calls `torch.cuda.is_available()` but no output log is recorded.

**Status:** NEEDS CONFIRMATION.

---

### Q7. Did you attempt to acquire a reference inventory for validation and fail, or did you simply not try?

**Why it matters:** These are different situations. If you searched for a post-Helene landslide inventory (e.g., from USGS rapid damage assessment, NASA COOLR, or the North Carolina Geological Survey) and could not find one publicly available, that is an honest methodological constraint worth mentioning. If you did not attempt it, that is a design gap.

**Status:** NEEDS CONFIRMATION.

---

### Q8. How long did this project take to build, from first code to final output?

**Why it matters:** Duration indicates depth of engagement. "I built this over one weekend" implies a quick prototype. "I worked on this over several weeks" implies sustained effort and iterative problem-solving. Either is acceptable as long as it is accurate.

**Status:** NEEDS CONFIRMATION.

---

### Q9. Is there any write-up, report, presentation, or other document associated with this project beyond the code?

**Why it matters:** The phd.pdf in the directory is the prior research audit document. If there is an actual project report, poster, or presentation, it should be reviewed and could provide additional verifiable details.

**Status:** Only phd.pdf found (prior audit). NEEDS CONFIRMATION whether any other documentation exists.

---

### Q10. What was your motivation for building this specific project?

**Why it matters:** Graduate applications should explain why you chose this problem. The honest answer — whether it was Hurricane Helene news coverage, personal interest in hazard mapping, exploring SAM's geospatial capabilities, or something else — is more credible than a generic statement about passion for remote sensing.

**Status:** NEEDS CONFIRMATION. Cannot be inferred from code.

---

## LOWER PRIORITY — Helpful to know but not critical

| Question | Why it helps |
|---|---|
| Which specific Python and R packages gave you the most difficulty? | Supports the debugging narrative in applications |
| Did you look at the output polygons in QGIS or another GIS tool? | Confirms visual inspection capability |
| Did you try any other approach before settling on SAM? | Demonstrates iterative thinking |
| Are there any other projects in adjacent topics? | Helps build a broader research narrative |
| What is your current academic institution and year of study? | Required for application factual accuracy |

---

## SUMMARY OF UNRESOLVED ITEMS THAT AFFECT APPLICATION TEXT

| Item | Risk if unresolved | Action needed |
|---|---|---|
| Hurricane Helene connection | Inaccurate framing in SOP/LOM | Confirm yes/no |
| Project context (self-directed vs. course) | Misrepresentation risk | Confirm before writing |
| Personal pipeline execution | Cannot claim outputs as personal work | Confirm yes |
| Visual inspection of over-segmentation | Cannot claim independent scientific judgment | Confirm or remove claim |
| Reference inventory attempt | Affects how limitation is described | Confirm search effort |
| GPU availability | Minor; affects computational methods description | Confirm |
| Project duration | Affects depth characterization | Confirm |
