# Conference abstract (NCUR / SIIM / MIDL short paper)

**Title:** Two Diagnosis Codes Drive Most of the Gain From Adding Health-Record Data to CT-Based Pulmonary Embolism Detection: An Independent Reproduction and Label-Leakage Audit

**Author:** Zain A. Jaffar, Department of Cell Biology and Neuroscience, Rutgers University, New Brunswick, NJ

**Background:** Models that combine CT pulmonary angiography (CTPA) with electronic health record (EHR) data report near-perfect pulmonary embolism (PE) detection. However, EHR features may already encode the diagnosis they are meant to predict. We tested whether a public multimodal PE benchmark reproduces, and how much of its performance depends on such features.

**Methods:** We reproduced the RadFusion benchmark (1,837 CTPA studies from 1,794 patients; held-out test set n=190). We used the released imaging-model (PENet) scores, trained an elastic-net logistic regression on 1,505 EHR features, and fused the two by averaging their probabilities. Discrimination was measured by AUROC with bootstrap 95% confidence intervals, and models were compared with paired DeLong tests. We measured each feature's contribution with SHAP, then refit the EHR model without prespecified groups of leakage-candidate features: pulmonary-circulation diagnoses, anticoagulants, and D-dimer testing.

**Results:** Fusion reached an AUROC of 0.94 (0.91–0.97), matching the published 0.947. Imaging alone scored 0.80 (0.73–0.85) and EHR alone 0.91 (0.86–0.96). One pulmonary-circulation diagnosis grouping was present in 93.3% of PE-positive and 16.2% of PE-negative training studies (odds ratio 72.3), and it accounted for 40.8% of all SHAP attribution. Removing these two features lowered EHR AUROC to 0.77 (0.70–0.84) and fusion to 0.84 (0.78–0.89), both p<0.001. After removal, fusion no longer differed significantly from imaging alone (p=0.118). Removing the anticoagulant or D-dimer features changed AUROC by at most 0.002.

**Conclusions:** The benchmark is reproducible, but most of its multimodal gain depends on two diagnosis codes that likely record the outcome itself. Multimodal benchmarks should filter EHR data by timestamp and report feature-exclusion ablations.

*(About 290 words in the body. NCUR's limit is 300 words; check each venue's limit before pasting.)*
