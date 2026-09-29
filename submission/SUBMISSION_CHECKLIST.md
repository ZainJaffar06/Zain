# Cureus resubmission: what's ready and what only you can do

## Ready to upload (in this folder)

| File | What it is |
|---|---|
| `manuscript.docx` | Full revised manuscript: abstract, body, declarations, 29 references, 8 tables, and 5 figures with legends |
| `figures/Figure_1_pipeline_overview.png` … `Figure_5_leakage_ablation.png` | Figures to upload one at a time in the Cureus figure step (no titles embedded) |
| `supplementary_appendix.docx` (+ `figures/Figure_S1_global_SHAP_importance.png`) | Replaces "Online Resource 1". Upload as a supplementary file |
| `response_to_editors.docx` | Point-by-point reply to all 17 items plus the title-text and reconciliation notes |
| `references.md` | Plain reference list to paste into the Cureus Reference Converter |
| `figure_legends.md`, `tables.md` | Legends and tables on their own, for pasting into the Cureus figure and table fields |

## Already handled

- **Affiliation:** set to "Department of Cell Biology and Neuroscience, Rutgers University, New Brunswick, USA", matching your B.S. major on your CV. Dermatology and Biostatistics are removed everywhere.
- **Figure 1:** redrawn in matplotlib so the legend's "Created in Python using matplotlib" is accurate. It now also shows the ablation step.
- **Code repository:** `revision/revision_analyses.py` is on branch `claude/elegant-cray-3o9jmq` of `radfusion-pe-reproduction`, together with a README section. A draft pull request is open there.
- **Numbering:** tables and supplementary tables are numbered in the order they are first cited.
- **Legends:** every table and figure legend names its statistics and software and defines its abbreviations.

## Still yours to do (about 15 minutes)

1. **Cureus profile.** Make it match the manuscript exactly:
   - Name: Zain A. Jaffar
   - Email: zaj14@scarletmail.rutgers.edu
   - Department: Department of Cell Biology and Neuroscience
   - Institution: Rutgers University, New Brunswick, USA
   - Degree: blank or "Undergraduate student"
   - Delete any Dermatology or Biostatistics entries.
2. **Merge the code pull request** in `radfusion-pe-reproduction` before you resubmit. The paper's Data Availability statement points readers to that repo.
3. **Slice-classifier paragraph** (Methods). It was written from `src/exploratory_yolo.py`: YOLOv8n-cls, 2 epochs, 224 px, slice-level only. Edit it if you trained the model differently, or delete it if you never ran it.
4. **AI-use statement** (Additional Information). Keep or reword it; don't restore the old "no LLM" sentence.
5. **References.** Paste `references.md` into the Cureus Reference Converter and click each DOI once. Double-check two entries:
   - ref 9: Gotway MB replaces the old "Gurudu SR";
   - ref 23: set the "Accessed" date to the day you submit.
6. **Upload.** Upload `manuscript.docx`, the five figure PNGs, `supplementary_appendix.docx` (with the Figure S1 PNG) and `response_to_editors.docx`. Then confirm the supplementary file appears in the submission preview.

## Corrections the re-analysis surfaced (all disclosed in the response letter)

- The old Methods said the EHR model was tuned by grid search. The reported numbers actually came from fixed reference hyperparameters (C=0.1, L1 ratio 0.99). A grid search now appears as a sensitivity analysis, and it picks the same values.
- EHR AUPRC was 0.91 in the old text; the correct value is 0.88.
- The SVC operating point differs by one study: 73 true positives instead of 72.
- Old "Online Resource 1" figure was a coefficient heatmap mislabelled as SHAP; replaced.
