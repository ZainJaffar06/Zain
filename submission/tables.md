# Tables

**Table 1: Study cohort by predefined split**

| Split | Studies, n | PE-positive, n (%) | PE-negative, n (%) | Central, n (%) | Segmental, n (%) | Subsegmental, n (%) |
|---|---|---|---|---|---|---|
| Training | 1454 | 508 (34.9) | 946 (65.1) | 202 (13.9) | 281 (19.3) | 25 (1.7) |
| Validation | 193 | 108 (56.0) | 85 (44.0) | 27 (14.0) | 52 (26.9) | 29 (15.0) |
| Test | 190 | 110 (57.9) | 80 (42.1) | 28 (14.7) | 54 (28.4) | 28 (14.7) |
| Total | 1837 | 726 (39.5) | 1111 (60.5) | 257 (14.0) | 387 (21.1) | 82 (4.5) |

*Values are n or n (%), with percentages of all studies in that split. PE subtype is shown for PE-positive studies (central, segmental, subsegmental) as the most proximal clot location recorded in the released dataset. Splits are those distributed with RadFusion and used to develop PENet; no studies were excluded. PE: pulmonary embolism.*

**Table 2: EHR feature counts at each preprocessing step**

| EHR table | Rows in released file | Studies after de-duplication | Features released | Features after zero-variance removal |
|---|---|---|---|---|
| Demographics | 1,837 | 1,837 | 12 | 12 |
| Inpatient medications | 1,892 | 1,837 | 1,282 | 618 |
| Outpatient medications | 1,892 | 1,837 | 1,282 | 566 |
| ICD diagnosis groupings | 1,892 | 1,837 | 282 | 258 |
| Laboratory tests | 1,892 | 1,837 | 44 | 42 |
| Vital signs | 1,892 | 1,837 | 9 | 9 |
| Total |  | 1,837 | 2,911 | 1,505 |

*Features released are those in the public RadFusion tables, which were already aggregated into presence/frequency or presence/latest-value indicators and filtered by the dataset authors to diagnosis groupings present in ≥1% of training studies. Fifty-one studies appeared twice with identical rows in five tables and were de-duplicated. After z-standardization, the 1,505 features entered the elastic-net model, which assigned non-zero coefficients to 199. EHR: electronic health record; ICD: International Classification of Diseases.*

**Table 3: Discrimination by modality on the held-out test set**

| Analysis | Arm | AUROC (95% CI) | AUPRC (95% CI) |
|---|---|---|---|
| Full test cohort, n=190 (110 PE-positive/80 PE-negative) | Imaging (provided PENet score) | 0.80 (0.73–0.85) | 0.85 (0.80–0.90) |
|  | EHR (elastic-net) | 0.91 (0.86–0.96) | 0.88 (0.81–0.96) |
|  | Late fusion (average) | 0.94 (0.91–0.97) | 0.95 (0.92–0.98) |
|  | Late fusion (maximum) | 0.89 (0.84–0.94) | 0.87 (0.80–0.95) |
| Non-subsegmental subset, n=162 (82 PE-positive/80 PE-negative) | Imaging (provided PENet score) | 0.84 (0.78–0.90) | 0.86 (0.81–0.91) |
|  | EHR (elastic-net) | 0.92 (0.86–0.96) | 0.86 (0.78–0.95) |
|  | Late fusion (average) | 0.96 (0.93–0.98) | 0.96 (0.92–0.98) |
|  | Late fusion (maximum) | 0.91 (0.86–0.96) | 0.86 (0.78–0.94) |

*Values are point estimates with 95% CIs from 2,000 stratified bootstrap resamples (percentile method). The imaging arm is the PENet score distributed with the benchmark, not a model trained here. The EHR arm is the elastic-net logistic model. Average fusion is the mean and maximum fusion the elementwise maximum of the imaging and EHR probabilities. Paired between-arm tests are given in Table 4. AUROC: area under the receiver operating characteristic curve; AUPRC: area under the precision-recall curve (average precision); CI: confidence interval; EHR: electronic health record; PE: pulmonary embolism.*

**Table 4: Paired comparisons of AUROC between arms**

| Analysis | Comparison (A vs B) | AUROC A | AUROC B | Difference (95% CI) | z | p-value |
|---|---|---|---|---|---|---|
| Full test cohort | Late fusion (average) vs EHR (elastic-net) | 0.94 | 0.91 | +0.031 (+0.001 to +0.061) | 2.03 | 0.042 |
|  | Late fusion (average) vs Imaging (provided PENet score) | 0.94 | 0.80 | +0.148 (+0.086 to +0.210) | 4.68 | <0.001 |
|  | EHR (elastic-net) vs Imaging (provided PENet score) | 0.91 | 0.80 | +0.117 (+0.035 to +0.199) | 2.81 | 0.005 |
|  | Late fusion (maximum) vs EHR (elastic-net) | 0.89 | 0.91 | −0.021 (−0.052 to +0.009) | −1.36 | 0.175 |
|  | Late fusion (average) vs Late fusion (maximum) | 0.94 | 0.89 | +0.052 (+0.023 to +0.082) | 3.50 | <0.001 |
|  | Late fusion (maximum) vs Imaging (provided PENet score) | 0.89 | 0.80 | +0.096 (+0.027 to +0.165) | 2.72 | 0.006 |
| Non-subsegmental subset | Late fusion (average) vs EHR (elastic-net) | 0.96 | 0.92 | +0.041 (+0.009 to +0.072) | 2.49 | 0.013 |
|  | Late fusion (average) vs Imaging (provided PENet score) | 0.96 | 0.84 | +0.117 (+0.056 to +0.179) | 3.73 | <0.001 |
|  | EHR (elastic-net) vs Imaging (provided PENet score) | 0.92 | 0.84 | +0.077 (−0.005 to +0.158) | 1.85 | 0.065 |
|  | Late fusion (maximum) vs EHR (elastic-net) | 0.91 | 0.92 | −0.007 (−0.036 to +0.023) | −0.45 | 0.654 |
|  | Late fusion (average) vs Late fusion (maximum) | 0.96 | 0.91 | +0.047 (+0.017 to +0.077) | 3.07 | 0.002 |
|  | Late fusion (maximum) vs Imaging (provided PENet score) | 0.91 | 0.84 | +0.070 (−0.001 to +0.141) | 1.94 | 0.052 |

*Differences, their 95% CIs, z statistics and two-sided p-values are from the DeLong test for correlated ROC curves. p-values are unadjusted for multiple comparisons and are exploratory. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record.*

**Table 5: Operating-point metrics at a fixed 0.5 threshold (test set, n=190; 110 PE-positive, 80 PE-negative)**

| Metric | EHR (SVC), specificity-oriented | Late fusion (maximum), sensitivity-oriented |
|---|---|---|
| Sensitivity | 73/110 (66%); 0.66 (0.57–0.75) | 106/110 (96%); 0.96 (0.91–0.99) |
| Specificity | 75/80 (94%); 0.94 (0.86–0.97) | 53/80 (66%); 0.66 (0.55–0.76) |
| PPV | 73/78 (94%); 0.94 (0.86–0.97) | 106/133 (80%); 0.80 (0.72–0.86) |
| NPV | 75/112 (67%); 0.67 (0.58–0.75) | 53/57 (93%); 0.93 (0.83–0.97) |
| Accuracy | 148/190 (78%); 0.78 (0.71–0.83) | 159/190 (84%); 0.84 (0.78–0.88) |
| F1 score | 0.78 | 0.87 |
| LR+ (95% CI) | 10.6 (4.5–25.1) | 2.9 (2.1–3.9) |
| LR− (95% CI) | 0.36 (0.27–0.47) | 0.05 (0.02–0.15) |
| Confusion matrix (TP/FP/FN/TN) | 73/5/37/75 | 106/27/4/53 |

*Proportions are shown as n/N (%) followed by the proportion with its Wilson score 95% CI. Likelihood-ratio 95% CIs use the log method. No hypothesis test was performed. Predictive values depend on the enriched test-set prevalence (57.9%) and are optimistic relative to routine practice; likelihood ratios are prevalence-independent. **The EHR column reflects the support-vector classifier (SVC) variant, not the elastic-net logistic model whose discrimination is reported in Table 3.** PE: pulmonary embolism; EHR: electronic health record; PPV/NPV: positive/negative predictive value; LR+/LR−: positive/negative likelihood ratio; TP/FP/FN/TN: true positives/false positives/false negatives/true negatives; CI: confidence interval; F1: harmonic mean of PPV and sensitivity.*

**Table 6: Ten highest-ranked EHR features by SHAP attribution**

| Rank | Feature (source table) | Mean absolute SHAP (log-odds) | Share of total (%) | Cumulative share (%) | Leakage-candidate group |
|---|---|---|---|---|---|
| 1 | DISEASES OF PULMONARY CIRCULATION:presence | 1.757 | 34.4 | 34.4 | Pulmonary-circulation diagnoses |
| 2 | DISEASES OF PULMONARY CIRCULATION:frequency | 0.323 | 6.3 | 40.8 | Pulmonary-circulation diagnoses |
| 3 | DISEASES OF VEINS AND LYMPHATICS, AND OTHER DISEASES OF CIRCULATORY SYSTEM:presence | 0.301 | 5.9 | 46.7 | Venous-disease diagnoses |
| 4 | OTHER DISEASES OF RESPIRATORY SYSTEM:presence | 0.218 | 4.3 | 51.0 | – |
| 5 | Symptoms involving respiratory system and other chest symptoms:frequency | 0.139 | 2.7 | 53.7 | – |
| 6 | NONSPECIFIC ABNORMAL FINDINGS:presence | 0.137 | 2.7 | 56.4 | – |
| 7 | ptt:Binary | 0.130 | 2.5 | 58.9 | – |
| 8 | DISEASES OF ARTERIES, ARTERIOLES, AND CAPILLARIES:presence | 0.125 | 2.5 | 61.4 | – |
| 9 | Symptoms involving respiratory system and other chest symptoms:presence | 0.125 | 2.4 | 63.8 | – |
| 10 | inr:Binary | 0.122 | 2.4 | 66.2 | – |

*Mean absolute SHAP value over the 190 test studies (exact linear SHAP, training-set background, log-odds units) and its share of the summed attribution across all 1,505 features. Group shares of total attribution: pulmonary-circulation diagnoses 40.8%; venous-disease diagnoses 5.9%; anticoagulant/thrombolytic medications 1.0%; D-dimer testing 0.9%. Feature names are as released ("presence" and "frequency" refer to ICD groupings; "Binary" to test ordered; "ptt" and "inr" to partial thromboplastin time and international normalized ratio). EHR: electronic health record; SHAP: SHapley Additive exPlanations; ICD: International Classification of Diseases.*

**Table 7: Presence of leakage-candidate features by PE status**

| Feature | Split | PE-positive, n/N (%) | PE-negative, n/N (%) | Odds ratio | p-value (Fisher's exact) |
|---|---|---|---|---|---|
| Pulmonary-circulation diagnosis (presence) | Training | 474/508 (93.3) | 153/946 (16.2) | 72.3 | <0.001 |
| Pulmonary-circulation diagnosis (presence) | Test | 97/110 (88.2) | 11/80 (13.8) | 46.8 | <0.001 |
| Any anticoagulant/thrombolytic (inpatient or outpatient) | Training | 130/508 (25.6) | 202/946 (21.4) | 1.3 | 0.077 |
| Any anticoagulant/thrombolytic (inpatient or outpatient) | Test | 40/110 (36.4) | 12/80 (15.0) | 3.2 | 0.002 |
| D-dimer measured | Training | 151/508 (29.7) | 302/946 (31.9) | 0.9 | 0.406 |
| D-dimer measured | Test | 32/110 (29.1) | 28/80 (35.0) | 0.8 | 0.431 |
| Venous-disease diagnosis (presence) | Training | 274/508 (53.9) | 195/946 (20.6) | 4.5 | <0.001 |
| Venous-disease diagnosis (presence) | Test | 54/110 (49.1) | 17/80 (21.2) | 3.6 | <0.001 |

*n/N (%) of PE-positive and PE-negative studies in which the feature was recorded as present (non-zero) in the released tables. Odds ratios and two-sided p-values are from Fisher's exact test. PE: pulmonary embolism.*

**Table 8: Label-leakage ablation: EHR and fusion discrimination after excluding leakage-candidate feature groups**

| Model | Features removed / used | EHR AUROC (95% CI) | EHR Δ vs full (95% CI); p | Average-fusion AUROC (95% CI) | Fusion Δ vs full (95% CI); p | Fusion vs imaging alone: Δ; p | Non-subsegmental EHR / fusion AUROC |
|---|---|---|---|---|---|---|---|
| Full model (reference) | 0 / 1,505 | 0.91 (0.86–0.96) | Reference | 0.94 (0.91–0.97) | Reference | +0.148; <0.001 | 0.92 / 0.96 |
| Without pulmonary-circulation diagnoses | 2 / 1,503 | 0.77 (0.70–0.84) | −0.146 (−0.216 to −0.076); <0.001 | 0.84 (0.78–0.89) | −0.104 (−0.156 to −0.053); <0.001 | +0.044; 0.118 | 0.80 / 0.88 |
| Without anticoagulant/thrombolytic medications | 20 / 1,485 | 0.91 (0.86–0.96) | 0.000 (−0.003 to +0.002); 0.756 | 0.94 (0.91–0.97) | 0.000 (−0.003 to +0.002); 0.729 | +0.148; <0.001 | 0.92 / 0.96 |
| Without D-dimer testing | 2 / 1,503 | 0.91 (0.86–0.96) | +0.001 (−0.002 to +0.004); 0.496 | 0.95 (0.91–0.98) | +0.002 (−0.001 to +0.004); 0.142 | +0.150; <0.001 | 0.92 / 0.96 |
| Without all three prespecified groups | 24 / 1,481 | 0.74 (0.67–0.81) | −0.173 (−0.244 to −0.103); <0.001 | 0.83 (0.77–0.88) | −0.114 (−0.167 to −0.061); <0.001 | +0.034; 0.243 | 0.76 / 0.87 |
| Without all three + venous-disease diagnoses | 26 / 1,479 | 0.71 (0.63–0.78) | −0.204 (−0.278 to −0.131); <0.001 | 0.82 (0.76–0.88) | −0.122 (−0.175 to −0.069); <0.001 | +0.026; 0.340 | 0.72 / 0.86 |

*Each row refits the elastic-net EHR model with the reference configuration after removing the listed feature group(s); average late fusion is recomputed with the fixed imaging score (imaging-alone AUROC 0.80). AUROC 95% CIs are from 2,000 stratified bootstrap resamples; differences (Δ), their 95% CIs and two-sided p-values are from paired DeLong tests against the full model, or against imaging alone in the penultimate column. Groups were prespecified on clinical criteria before the ablation was run (Supplementary Table S2). A fall in AUROC measures reliance on the excluded features and does not by itself establish leakage. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record.*
