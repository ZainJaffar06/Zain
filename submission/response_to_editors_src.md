**Response to the Cureus Editorial Team**

Manuscript: *Independent Reproduction and Label-Leakage Audit of Multimodal Pulmonary Embolism Detection on the RadFusion Benchmark*

Dear Editors,

Thank you for the careful review. We have addressed every point below.

The largest change answers items 1–3. The label-leakage audit is now quantitative: we refit the EHR model without prespecified groups of suspect features and report bootstrap confidence intervals and paired DeLong tests for every comparison. This added one table and one figure (Table 8, Figure 5) and changed the main conclusion from "may partly reflect leakage" to a measured effect:

- Removing the two pulmonary-circulation diagnosis features lowers the EHR AUROC from {{ehr_full}} to {{ehr_nopc}}.
- It lowers the fusion AUROC from {{avg_full}} to {{avg_nopc}}.
- After removal, fusion no longer differs significantly from imaging alone.

All analyses were re-run from the released data with a single script. The corrections we made along the way are listed at the end of this letter.

**Title text in images (raised twice).** All figures were regenerated without embedded titles; captions now carry that information. Figure 1 never contained a title; it was redrawn to show the new ablation step. Figure 3 no longer shows the "No Subsegmental" title.

**Author/affiliation reconciliation.** The author, affiliation and e-mail are now identical in the manuscript and the submission profile:

- Name: Zain A. Jaffar
- Affiliation: «AFFILIATION», Rutgers University, New Brunswick, USA
- E-mail: zaj14@scarletmail.rutgers.edu

The Dermatology and Biostatistics entries have been removed (see item 4).

**1. Methods detail.** The Materials & Methods section now specifies:

- data source, selection, and the dataset authors' own leakage safeguards;
- each preprocessing step, with feature counts (new Table 2);
- missing-data handling;
- exact model configurations: elastic-net C=0.1 and L1 ratio 0.99 with balanced class weights; SVC with an RBF kernel, C=1 and γ="scale";
- the cross-validated grid search, with its search space and selected values (Supplementary Table S2);
- the fusion rules, which have no learned parameters;
- statistical methods;
- a new "Label-leakage audit" subsection that states the prespecified criteria for leakage-candidate features and the three-step procedure (attribution, descriptive association, feature-exclusion ablation).

The exact column list for each group is given in Supplementary Table S1.

**2. Results: quantitative reporting.** All AUROC and AUPRC values now carry bootstrap 95% CIs (Table 3). Between-arm differences are tested with paired DeLong tests (Table 4). The leakage findings are reported numerically:

- mean absolute SHAP values and shares of attribution (Table 6, Supplementary Figure S1);
- prevalence of each suspect feature by PE status, with Fisher's exact tests (Table 7);
- the feature-exclusion ablation (Table 8, Figure 5).

**3. Discussion.** The Discussion now covers:

- the implications of the measured leakage for deployment and for model evaluation;
- the limitations of the audit, in particular that without timestamps reliance cannot be split into leakage versus legitimate history;
- a new "Recommendations for multimodal benchmarking" subsection with five concrete practices.

**4. Degree and affiliation.** The author is an undergraduate student (B.S. candidate, Cell Biology and Neuroscience) at Rutgers University and holds no degree yet. The Dermatology and Biostatistics entries reflected unrelated activities, not an appointment or a unit that supported this work, so they have been removed. The single affiliation is «AFFILIATION», Rutgers University, New Brunswick, USA.

**5. Citations.** All citable statements are now referenced. The reference list grew from 11 to 29 entries, adding:

- epidemiology and guidelines [1,2];
- workforce [8];
- clinical scores [3-7];
- reproducibility and leakage [18-20];
- statistical methods [24-26];
- software [27];
- EHR process bias [28];
- decision-curve analysis [29].

**6. Figure 3 caption.** The caption now reports the figure's own non-subsegmental values:

- imaging 0.84
- EHR 0.92
- average fusion 0.96
- maximum fusion 0.91, now evaluated on this subset

The orphaned duplicate caption and the duplicate paragraph under Table 1 were removed.

**7. Slice-level classifier.** The Future Work sentence was removed. A short "Exploratory slice-level classifier (not part of any reported result)" subsection in Materials & Methods now describes this work and states that it contributes to no reported result.

**8. Table 2 footnote.** The operating-point table (now Table 5) carries a footnote stating that its EHR column is the SVC variant, not the elastic-net model reported in Table 3.

**9. Online Resource 1.** Renamed "Supplementary Appendix" to follow Cureus conventions and uploaded as a supplementary file. It contains:

- Supplementary Figure S1: the global SHAP importance, replacing an earlier coefficient heatmap;
- Supplementary Table S1: leakage-candidate columns;
- Supplementary Table S2: sensitivity analyses;
- Supplementary Table S3: the updated TRIPOD+AI map.

All in-text references were updated.

**10. Affiliation string.** This is a single affiliation, not two affiliations or a cross-departmental appointment. It is formatted as «AFFILIATION», Rutgers University, New Brunswick, USA.

**11. Image creation.** Each figure legend now names the software used to create it: Python, matplotlib, scikit-learn and SHAP, with versions. Figure 1 was redrawn in matplotlib to include the feature-exclusion ablation step.

**12. Discussion citations.** The Discussion now cites:

- the dataset documentation [15];
- clinical scores [3,4,6];
- EHR process bias [28];
- TRIPOD+AI [21];
- decision-curve analysis [29].

**13. Scores and scales.** The following are now cited: Wells [3], revised Geneva [4], PERC [5], YEARS [6], age-adjusted D-dimer [7], and the ICD-9-CM/ICD-10-CM classification [23].

**14. Software.** A Software subsection lists Python {{v_python}}, scikit-learn {{v_sklearn}}, SHAP {{v_shap}}, NumPy {{v_numpy}}, pandas {{v_pandas}}, SciPy {{v_scipy}} and matplotlib {{v_mpl}}, with the analysis year ({{run_year}}), and cites scikit-learn and SHAP.

**15. Sample size, sampling and selection.** A "Sample size" paragraph explains:

- No a priori calculation was performed, because the complete public benchmark and its predefined splits fix the sample size.
- Sampling was a census of the released dataset.
- Precision is reported as 95% CIs.

Selection and inclusion are inherited from the source dataset [11,15,16], and no further exclusions were applied. The dataset authors' own exclusions, including removing diagnosis codes from the index encounter, are described. A new cohort table (Table 1) reports n (%) PE-positive and PE subtype by split and explains why the test set (57.9%) is more PE-enriched than the full cohort (39.5%).

**16. n (%), test statistics and abbreviations in tables.** Every table now:

- reports n or n/N (%) where applicable;
- names the statistical method in its legend (bootstrap percentile CIs, DeLong test, Wilson score intervals, log-method likelihood-ratio CIs, Fisher's exact test);
- defines all abbreviations.

**17. Reference formatting.** All references follow the Cureus style:

- The MICCAI and NeurIPS papers [9,22] are formatted as conference proceedings.
- The RadFusion preprint [16] is marked as a preprint.
- Article numbers were corrected (e198719, e078378).
- The NeurIPS entry no longer carries a mismatched arXiv DOI.

**Corrections made during re-analysis.** We report these for transparency:

- **Methods versus the actual pipeline.** The original Methods described cross-validated hyperparameter tuning. The published numbers were in fact produced with the fixed hyperparameters of the benchmark's reference implementation. The Methods now state this. A cross-validated grid search, added as a sensitivity analysis, selects the same values.
- **Rare-code filter.** It was applied by the dataset authors before release, not by us.
- **EHR average precision.** Corrected from 0.91 to {{ehr_auprc}}.
- **SVC operating point.** It differs by one test study from the original submission ({{svc_tp}} rather than 72 true positives), a result of re-running the probability calibration step. All other reproduced values are unchanged to two decimals.
- **Supplementary figure.** The previous supplementary figure showed model coefficients, not SHAP values, and has been replaced.

Sincerely,

Zain A. Jaffar
