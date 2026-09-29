**Independent Reproduction and Label-Leakage Audit of Multimodal Pulmonary Embolism Detection on the RadFusion Benchmark**

Zain A. Jaffar ^1^

^1^ «AFFILIATION», Rutgers University, New Brunswick, USA

Corresponding author: Zain A. Jaffar, zaj14@scarletmail.rutgers.edu

# Abstract

**Introduction:** The RadFusion benchmark showed that combining computed tomography pulmonary angiography (CTPA) with structured electronic health record (EHR) data improves pulmonary embolism (PE) detection, but it has not been independently reproduced or audited. We reproduced its multimodal late-fusion result and quantified how much depends on EHR features that may encode the diagnosis itself.

**Methods:** We used RadFusion (1,837 CTPA studies; held-out test set of 190 studies, 110 [57.9%] PE-positive). The imaging input was held fixed by reusing the study-level PENet score distributed with the benchmark. We re-implemented the EHR arm as an elastic-net logistic model and combined the two arms by average and maximum late fusion. We report the area under the receiver operating characteristic curve (AUROC) with bootstrap 95% confidence intervals and paired DeLong tests. The EHR arm was audited with SHapley Additive exPlanations (SHAP) and a feature-exclusion ablation of prespecified leakage-candidate groups: pulmonary-circulation diagnoses, anticoagulant or thrombolytic medications, and D-dimer testing.

**Results:** Average fusion reached an AUROC of {{avg_full}}, compared with {{ehr_full}} for the EHR arm (difference {{d_avg_ehr}}; p={{p_avg_ehr}}) and {{img_full}} for imaging alone. The pulmonary-circulation diagnosis grouping, which contains PE itself, accounted for {{shap_pc}}% of total SHAP importance. It was present in {{pc_train_pos}} of PE-positive versus {{pc_train_neg}} of PE-negative training studies. Removing its two features lowered the EHR AUROC to {{ehr_nopc}} and the fusion AUROC to {{avg_nopc}} (both p<0.001), after which fusion no longer differed significantly from imaging alone (p={{p_nopc_img}}). Removing anticoagulant or D-dimer features changed the AUROC by at most 0.002.

**Conclusions:** The benchmark result reproduces. However, much of its EHR contribution depends on a single diagnosis grouping that contains the target condition, so reported multimodal gains may overstate pretest predictive value. Releasing index-relative feature timestamps and routinely reporting feature-exclusion sensitivity analyses would strengthen multimodal benchmarks.

**Keywords:** pulmonary embolism, reproducibility, multimodal machine learning, late fusion, label leakage, interpretability, electronic health records, computed tomography pulmonary angiography

# Introduction

Pulmonary embolism (PE) is a common and potentially fatal manifestation of venous thromboembolism, which ranks among the leading causes of cardiovascular death worldwide [1,2]. Diagnosis rests on CT pulmonary angiography (CTPA), interpreted together with clinical context recorded in the electronic health record (EHR) and structured by pretest-probability rules such as the Wells score, the revised Geneva score, the PE rule-out criteria (PERC), and the YEARS algorithm with or without age-adjusted D-dimer thresholds [2-7]. Timely interpretation is limited by radiologist workload and workforce shortfalls [8]. Diagnostic-support tools that are both accurate and interpretable could therefore help extend expert-level reading to more settings.

Deep learning for PE has advanced along two tracks. Imaging models range from vessel-aligned convolutional networks [9] and two-stage detectors [10] to end-to-end volumetric classifiers such as PENet [11], purpose-built detection networks [12], and multitask imaging models [13]. Separately, EHR-only models predict PE from structured clinical data [14]. The RadFusion benchmark combined the two and showed that multimodal fusion of CTPA and EHR outperforms either modality alone [15,16]. Even so, most approaches remain unimodal and opaque. This limits clinical trust, because such models neither reflect the multimodal reasoning of radiologists nor expose the basis of a prediction [17].

Three gaps motivate this work. First, independent reproductions of medical machine-learning results are uncommon, even though reproducibility is a prerequisite for trustworthy translation [18]. Second, interpretability is rarely evaluated alongside performance. Third, and specific to this benchmark: when a model draws on longitudinal EHR features, some of those features may be recorded at the same time as, or after, the diagnosis they are used to predict. This is a form of target (label) leakage, a well-described cause of optimistic performance in machine learning [19,20].

We therefore hold the imaging input fixed by reusing the study-level vision-model scores distributed with the benchmark, re-implement the EHR arm independently, and reproduce the late-fusion step. We then audit the resulting EHR model with feature attribution and quantify the audit with a feature-exclusion ablation. Throughout, "detection" denotes study-level classification (PE present versus absent), not embolus localization. Our contributions are:

- an independent reproduction of RadFusion late fusion with the imaging input held fixed, so that the reproduction isolates the EHR arm and the fusion rule;
- uncertainty-quantified reporting: bootstrap confidence intervals, paired DeLong tests, and operating points with likelihood ratios;
- a label-leakage audit that measures how much of the EHR and fusion discrimination depends on features that may encode the diagnosis.

We make no claim of a novel architecture or of state-of-the-art performance.

# Materials & Methods

**Figure 1** summarizes the analysis pipeline.

## Study design and reporting

This is a retrospective secondary analysis of a public, de-identified benchmark, reported according to the TRIPOD+AI statement [21]. No new data were collected, so institutional review board approval was not required.

## Data source, participants and selection

We used the Stanford AIMI RadFusion dataset [16], which contains 1,837 CTPA studies from 1,794 patients, retrospectively assembled at a single academic medical center. Each study has a study-level PE label (PE present or absent), a PE subtype for positive studies (central, segmental, or subsegmental), a predefined split assignment (training, validation, or test), and paired structured EHR features. Patient selection, the reference-standard labeling procedure, and split construction were performed by the dataset authors and are described in the source publications [11,15,16]. According to that documentation, EHR features summarize the 12 months preceding the CT examination. ICD diagnosis codes recorded under the same encounter number as the CT examination, or within 24 hours before it, were removed by the dataset authors to limit leakage [15]. Diagnosis codes were collapsed into diagnosis groupings, and groupings present in fewer than 1% of training studies were removed before release. The released tables contain aggregated presence and frequency indicators, not timestamps relative to the index examination.

We applied no additional inclusion or exclusion criteria: every one of the 1,837 studies was analyzed. **Table 1** shows the cohort by split. The splits are those used to develop PENet [11]. The training split is 34.9% PE-positive, whereas the validation and test splits are enriched (56.0% and 57.9%), so the test-set prevalence exceeds that of the full cohort (39.5%). The test set comprises 190 studies (110 PE-positive, 80 PE-negative); 28 of its positive studies are subsegmental.

**Sample size.** No a priori sample size calculation was performed. This reproduction used the complete RadFusion benchmark and its predefined splits, which fixes the sample size. Sampling was therefore a census of the released dataset rather than a random or consecutive sample drawn by us. The precision achieved is reported as 95% confidence intervals for every estimate. For a test set of 110 positive and 80 negative studies, the AUROC intervals have half-widths of about 0.03–0.07.

## Imaging arm (provided vision-model scores)

The imaging input was the study-level probability distributed with RadFusion (the `pred` column of the released vision file). It was generated by the benchmark's PENet three-dimensional convolutional network [11]. No imaging model was trained, fine-tuned, or evaluated for any reported result. Reusing the released scores keeps the imaging input identical to the reference benchmark, so any divergence from the published result is attributable to the re-implemented EHR arm and the fusion step. Imaging performance reported here is therefore inherited from the benchmark, not established by this study.

## EHR feature processing

The six released EHR tables were demographics, inpatient medications, outpatient medications, ICD diagnosis groupings, laboratory tests, and vital signs. Medications are represented as presence and frequency across 641 drug classes, laboratory tests as presence and latest value for 22 tests, and 141 diagnosis groupings as presence and frequency. Each table was processed as follows:

1. Fifty-one studies that appeared twice with byte-identical rows in five tables were de-duplicated.
2. Constant (zero-variance) columns were removed.
3. Each remaining feature was standardized to zero mean and unit variance, following the reference implementation [15].

Standardization used the mean and standard deviation across all 1,837 studies. This step does not use labels, and a sensitivity analysis fitted standardization on the training split only. The tables were then joined on the study identifier. {{missing_sentence}} No further frequency filter was applied beyond the <1% filter already applied by the dataset authors. **Table 2** reports the feature counts at each step; the final feature matrix contained {{n_features}} features.

## EHR models

The primary EHR model was an elastic-net-regularized logistic regression (scikit-learn LogisticRegression; saga solver). Its hyperparameters were fixed a priori to those of the reference implementation [15]: inverse regularization strength C=0.1, L1 ratio 0.99, a maximum of 1,000 iterations, and random seed 0. Class imbalance was handled with balanced class weights, which are inversely proportional to class frequency in the training split. The model was fitted on the training split only (1,454 studies). The validation split was not used for fitting or model selection, and the test split was used only for evaluation. Of the {{n_features}} input features, {{n_nonzero}} received a non-zero coefficient.

A sensitivity analysis tuned the same model on the training split by five-fold stratified cross-validated grid search, scored by AUROC, over C ∈ {0.01, 0.1, 1.0} and L1 ratio ∈ {0.5, 0.9, 0.99}. As a secondary EHR estimator, used for the specificity-oriented operating point in Table 5, a support-vector classifier (SVC) was fitted: radial basis function kernel, C=1.0, γ="scale", no class weighting, with probability estimates from scikit-learn's internal Platt scaling. {{svc_sentence}} Multidimensional scaling was used for exploratory visualization only.

## Late fusion

Study-level imaging and EHR probabilities were combined by two late-fusion rules: the arithmetic mean (average fusion) and the elementwise maximum (maximum fusion). This is consistent with prior evidence that late combination performs competitively for multimodal PE detection [15]. Neither rule has learned parameters, so no fusion weights were fitted on any split.

## Interpretability

We computed exact SHapley Additive exPlanations (SHAP) values for the elastic-net model with the linear explainer [22], using the training split as the background distribution. Values are expressed in log-odds units. Each feature's global importance was summarized as its mean absolute SHAP value over the 190 test studies, and as its share of the summed mean absolute SHAP value across all features. Attribution was applied to the EHR arm only; because the imaging scores were not generated here, no saliency maps accompany the imaging arm.

## Label-leakage audit

Before any ablation result was computed, we prespecified three leakage-candidate feature groups using explicit clinical criteria:

- **(a) Diagnosis groupings whose code range contains the target condition.** The "diseases of pulmonary circulation" grouping contains PE (ICD-9-CM 415.1; ICD-10-CM I26) [23]. This group has two features: presence and frequency.
- **(b) Treatments for the target condition.** Inpatient and outpatient heparin and related preparations, coumarin-type anticoagulants, direct factor Xa inhibitors, direct thrombin inhibitors, and thrombolytic enzymes: 20 features.
- **(c) Diagnostic workup for the target condition.** D-dimer presence and latest value: 2 features.

A fourth, secondary group was defined by the same logic: **(d) venous-disease diagnoses** (the grouping containing deep-vein thrombosis; 2 features). It captures a condition that is typically diagnosed during the PE workup. The exact column list is given in Supplementary Table S2 and is released with the code.

The audit had three steps:

1. **Attribution.** Features were ranked by mean absolute SHAP value, and each group's share of total attribution was computed.
2. **Descriptive association.** For each group, the proportion of PE-positive and PE-negative studies with the feature present was compared by Fisher's exact test.
3. **Feature-exclusion ablation.** The elastic-net model was refit with an identical configuration after removing each group in turn, then groups (a)–(c) together, then (a)–(d) together. Fusion was recomputed for each variant. Each ablated model was compared with the full model, and each ablated fusion with imaging alone, by paired DeLong test.

A fall in discrimination after exclusion shows how much the model relies on those features. It does not by itself prove leakage, because a documented history of venous thromboembolism is also a legitimate risk factor [3].

## Statistical analysis

Discrimination was summarized by AUROC and average precision (area under the precision-recall curve, AUPRC). The 95% CIs for both came from 2,000 stratified bootstrap resamples of the test set (percentile method; seed 42). As a check, the bootstrap and DeLong standard errors for AUROC agreed within {{se_agree}}. Paired comparisons of correlated AUROCs used the DeLong test [24], which reports the difference with its 95% CI and a two-sided p-value.

At a fixed, untuned probability threshold of 0.5 we report:

- sensitivity, specificity, positive and negative predictive values (PPV, NPV), and accuracy, each as n/N (%) with Wilson score 95% CIs [25];
- F1 score;
- positive and negative likelihood ratios (LR+, LR−), with 95% CIs by the log method [26].

Associations between binary features and the PE label were tested with Fisher's exact test.

The full test cohort was the primary analysis. The non-subsegmental subset (test studies excluding those whose PE was confined to subsegmental vessels; n=162) was secondary, because subsegmental clots are the smallest and most diagnostically ambiguous and are conventionally analyzed separately in this benchmark [15]. Tests were two-sided with α=0.05. No adjustment for multiple comparisons was made, so p-values are interpreted as exploratory.

## Software

Analyses were run in {{run_year}} with:

- Python {{v_python}}
- scikit-learn {{v_sklearn}} [27]
- SHAP {{v_shap}} [22]
- NumPy {{v_numpy}}
- pandas {{v_pandas}}
- SciPy {{v_scipy}}
- matplotlib {{v_mpl}}

The RadFusion dataset is available through the Stanford AIMI Shared Datasets program under its data-use terms; the author does not redistribute it. All analysis code, the exact leakage-candidate column list, library versions, and random seeds are available at https://github.com/ZainJaffar06/radfusion-pe-reproduction. Every reported number is regenerated by a single script.

## Exploratory slice-level classifier (not part of any reported result)

Separately from this reproduction, we explored a compact candidate imaging backbone: a YOLOv8n-cls image classifier (Ultralytics), fine-tuned for two epochs at 224×224 pixels on individual CTPA slices labeled as PE or no PE, and evaluated at the slice level only. Its outputs were never aggregated to study level, never combined with the EHR arm, and contribute to no result, table, or figure in this article. Slice-level accuracy under strong class imbalance approaches the majority-class base rate and is not a meaningful measure of PE detection, so no slice-level results are reported. The code is included in the repository for transparency.

# Results

## Cohort and features

**Table 1** shows the cohort by split. **Table 2** shows the features retained after each preprocessing step.

## Reproduction of the benchmark result

**Table 3** summarizes discrimination, and **Figures 2 and 3** show the ROC curves.

On the full test cohort, average late fusion achieved an AUROC of {{avg_full_ci}}. This compares with {{ehr_full_ci}} for the EHR arm, {{max_full_ci}} for maximum fusion, and {{img_full_ci}} for the provided imaging scores.

On the non-subsegmental subset, the corresponding values were:

- average fusion: {{avg_ns_ci}}
- EHR arm: {{ehr_ns_ci}}
- maximum fusion: {{max_ns_ci}}
- imaging: {{img_ns_ci}}

The full-cohort fusion AUROC closely matches the 0.947 (95% CI 0.946–0.948) reported for the benchmark's best multimodal model, a late elastic-average fusion over the same PENet scores [15]. Because both analyses use the same released imaging scores, this agreement isolates the re-implemented EHR arm and the fusion step.

## Paired comparisons between arms

**Table 4** gives the paired DeLong comparisons.

On the full cohort:

- **Average fusion vs. EHR arm:** {{d_avg_ehr_full}}; p={{p_avg_ehr_full}}. This is nominally significant but would not survive a multiplicity correction, so it should be read as modest.
- **Average fusion vs. imaging:** {{d_avg_img_full}}; p={{p_avg_img_full}}.
- **EHR arm vs. imaging:** {{d_ehr_img_full}}; p={{p_ehr_img_full}}.
- **Maximum fusion vs. EHR arm:** {{d_max_ehr_full}}; p={{p_max_ehr_full}} (no significant difference).
- **Average vs. maximum fusion:** {{d_avg_max_full}}; p={{p_avg_max_full}} (average fusion higher).

The non-subsegmental subset showed the same pattern: average fusion vs. EHR arm {{d_avg_ehr_ns}}; p={{p_avg_ehr_ns}}.

## Operating points

**Table 5** reports the operating-point metrics at a threshold of 0.5.

**Specificity-oriented EHR (SVC) configuration:** {{svc_counts}}.

- sensitivity {{svc_sens}}
- specificity {{svc_spec}}
- LR+ {{svc_lrp}}

**Sensitivity-oriented maximum-fusion configuration:** {{mx_counts}}.

- sensitivity {{mx_sens}}
- NPV {{mx_npv}}
- LR− {{mx_lrn}}

## Feature attribution

**Figure 4** shows the SHAP summary, and **Supplementary Figure S1** shows the global importance ranking. **Table 6** lists the ten highest-ranked features.

The two pulmonary-circulation diagnosis features ranked first and second, with mean absolute SHAP values of {{shap1}} and {{shap2}} log-odds. Together they accounted for {{shap_pc}}% of total attribution. The venous-disease grouping ranked third ({{shap_veins}}%).

The other prespecified groups contributed little:

- anticoagulant and thrombolytic features: {{shap_ac}}% in total (highest rank {{rank_ac}})
- D-dimer features: {{shap_dd}}% (highest rank {{rank_dd}})

## Label-leakage audit

**Table 7** shows how common each leakage-candidate feature was by PE status.

A pulmonary-circulation diagnosis was recorded in {{pc_train_pos_full}} PE-positive versus {{pc_train_neg_full}} PE-negative training studies (odds ratio {{pc_or_train}}; p<0.001). In the test set the corresponding figures were {{pc_test_pos_full}} versus {{pc_test_neg_full}}.

For the other groups:

- **Anticoagulant or thrombolytic exposure:** similar in the training split ({{ac_train_pos}} vs {{ac_train_neg}}; p={{ac_train_p}}) but more common among PE-positive test studies ({{ac_test_pos}} vs {{ac_test_neg}}; p={{ac_test_p}}).
- **D-dimer testing:** did not differ by PE status in either split.

**Table 8** and **Figure 5** show the feature-exclusion ablation.

Removing only the two pulmonary-circulation features lowered the EHR AUROC from {{ehr_full}} to {{ehr_nopc_ci}}. The difference was {{d_ehr_nopc}} (p<0.001). The average-fusion AUROC fell from {{avg_full}} to {{avg_nopc_ci}}, a difference of {{d_avg_nopc}} (p<0.001). With these features excluded, fusion no longer differed significantly from imaging alone ({{d_nopc_img}}; p={{p_nopc_img}}), whereas the full model's advantage was {{d_full_img}} (p<0.001).

Removing the anticoagulant/thrombolytic group or the D-dimer group alone changed neither the EHR nor the fusion AUROC by more than 0.002 (all p≥{{min_p_small}}).

Removing groups (a)–(c) together gave:

- EHR AUROC {{ehr_all3_ci}}
- fusion AUROC {{avg_all3_ci}}; fusion vs. imaging alone, p={{p_all3_img}}

Additionally removing the venous-disease group gave:

- EHR AUROC {{ehr_all4_ci}}
- fusion AUROC {{avg_all4_ci}}

The non-subsegmental subset showed the same pattern (**Table 8**).

## Sensitivity analyses

**Supplementary Table S1** reports the sensitivity analyses.

- **Standardization fitted on the training split only:** EHR AUROC {{s_scale_ehr}}, fusion AUROC {{s_scale_avg}}.
- **Cross-validated grid search:** selected {{gs_params}} and gave EHR {{s_gs_ehr}} and fusion {{s_gs_avg}}.
- **Grid search after excluding groups (a)–(c):** EHR {{s_gs3_ehr}} and fusion {{s_gs3_avg}}.

The ablation finding therefore does not depend on the fixed reference hyperparameters.

# Discussion

This independent reproduction supports three findings.

First, with the imaging input held fixed, the re-implemented EHR arm and fusion step recover the published benchmark result ({{avg_full}} against 0.947). This is the reproducibility claim of this work.

Second, the ordering of the arms matches the benchmark. Average fusion is highest, and maximum fusion performs no better than the EHR arm, so the choice of fusion rule matters. The advantage of average fusion over the EHR arm is small and only nominally significant.

Third, and most consequential, most of the EHR contribution depends on a single diagnosis grouping that contains the target condition. Without that grouping, the multimodal model is not demonstrably better than the imaging model alone.

## Temporal label leakage in the EHR arm

Multimodal benchmarks that pair imaging with longitudinal EHR features assume the EHR features are available before the index examination. The RadFusion authors took explicit steps toward this: they restricted features to the preceding 12 months and removed diagnosis codes from the index encounter and the preceding 24 hours [15]. Our audit indicates that those steps may not fully remove diagnosis-related signal.

A pulmonary-circulation diagnosis was present in {{pc_train_pos_pct}}% of PE-positive but only {{pc_train_neg_pct}}% of PE-negative training studies. A prior history of venous thromboembolism is a legitimate risk factor, weighted as such in the Wells and revised Geneva scores [3,4]. However, a prior pulmonary-circulation diagnosis in more than nine of ten patients with PE is far higher than a history-only feature would plausibly produce. Several processes could explain it: codes carried from linked encounters that fall outside the encounter-number rule; problem-list or billing entries back-dated to the diagnostic episode; or repeat imaging in patients with known or recently treated PE.

The released tables cannot distinguish these explanations, because they carry no timestamps relative to the index study. The ablation nevertheless bounds the practical consequence. Two of {{n_features}} features account for an EHR AUROC difference of {{abs_d_ehr_nopc}} and a fusion difference of {{abs_d_avg_nopc}}. Once they are removed, the fusion gain over imaging alone becomes small and statistically uncertain.

The anticoagulant and D-dimer concerns raised in our initial attribution analysis were not borne out quantitatively. Removing either group left discrimination unchanged, and D-dimer testing was equally common in PE-positive and PE-negative studies. This is consistent with process-driven EHR signals, such as whether a test was ordered [28], being less informative here than diagnosis coding.

These results do not invalidate the benchmark or imply that its authors erred. They identify a verification step that the released data do not currently support. The EHR AUROC of {{ehr_full}} and the fusion AUROC of {{avg_full}} are best read as upper bounds under the released feature definitions, not as estimates of pretest discrimination. The ablated values ({{ehr_nopc}} and {{avg_nopc}}) are closer to a conservative lower bound. Excluding the pulmonary-circulation grouping also removes any legitimate history-of-PE signal it contains, so the true pretest value lies between these bounds.

## Implications for clinical deployment and model evaluation

In an imaging-informatics workflow, a late-fusion model would sit between study acquisition and the reading worklist, reordering studies for expert review rather than replacing it. A sensitivity-oriented operating point (sensitivity {{mx_sens_pt}}, NPV {{mx_npv_pt}}) suits triage, and a specificity-oriented point (specificity {{svc_spec_pt}}, PPV {{svc_ppv_pt}}) suits confirmatory use. The leakage finding bears directly on both roles.

At the moment a CTPA enters the worklist, the diagnosis code the EHR arm relies on most would usually not yet exist for a first presentation of PE. The deployed model would therefore behave more like the ablated model than like the benchmark model. For evaluation, the lesson is that a reproduced AUROC, however close to the published value, does not validate the features that produce it. Attribution combined with a quantitative exclusion analysis is a cheap and informative complement to headline discrimination.

Predictive values here were measured at a test-set prevalence of 57.9%. This far exceeds that of routine suspected-PE populations; in a large prospective management study, PE was confirmed in about one in seven patients [6]. Only the likelihood ratios transfer across settings.

## Recommendations for multimodal benchmarking

We suggest five practices for multimodal medical-AI benchmarks that pair imaging with EHR data:

1. **Release index-relative timestamps.** Distribute feature timestamps relative to the index examination, or pre-computed variants censored at the index time, so users can verify that features are available at prediction time.
2. **Report exclusion analyses routinely.** Report a feature-exclusion or censored-feature sensitivity analysis whenever features could encode the target (diagnosis codes, treatments, and diagnostic tests for the target condition).
3. **Quantify uncertainty in comparisons.** Report CIs and paired tests (for example, DeLong) for between-arm comparisons, rather than point estimates alone.
4. **Follow reporting guidance.** Use TRIPOD+AI [21] and document how each EHR feature was derived.
5. **Compare against clinical rules.** Benchmark against established pretest-probability rules [3-7] at a realistic prevalence.

## Limitations

**Dataset.** Development and evaluation used a single-center benchmark with no external or prospective validation. The test set is enriched for PE (57.9%), which inflates predictive values. The leakage audit is limited by the released data. Without index-relative timestamps we can measure how much the model relies on the suspect features, but we cannot determine how much of that reliance is true leakage and how much is legitimate history. We also could not verify the preprocessing that generated the released imaging scores.

**Model.** This is a reproduction, not a novel architecture. The imaging AUROC is inherited from the benchmark, so any optimism in those scores propagates into the fusion results. The EHR discrimination (elastic-net) and the specificity-oriented operating point (SVC) come from different estimators, so Tables 3 and 5 do not describe a single model. Feature standardization in the reference implementation used feature distributions from all splits, although a training-only sensitivity analysis gave the same result.

**Statistical.** The advantage of average fusion over the EHR arm was nominally significant without adjustment for multiple comparisons. Operating points use an untuned 0.5 threshold, and neither probability calibration nor decision-curve analysis [29] was performed.

**Clinical.** The pipeline was not benchmarked against clinical pretest-probability rules. Subgroup and fairness performance across RadFusion's protected attributes was not assessed. The system is a research prototype and is not intended for clinical use.

# Conclusions

With the imaging input held fixed, an independently re-implemented EHR arm and late-fusion step recover the published RadFusion multimodal result ({{avg_full}} against 0.947). However, a diagnosis grouping that contains the target condition drives most of the EHR contribution. Removing two such features lowers the fusion AUROC to {{avg_nopc}}, and fusion then no longer differs significantly from imaging alone. Multimodal gains on this benchmark should therefore be read as gains under the released feature definitions, not as prospective pretest performance. Releasing index-relative feature timestamps, and routinely reporting feature-exclusion sensitivity analyses, would allow the temporal audit this question requires.
