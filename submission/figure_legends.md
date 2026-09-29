# Figure legends

**Figure 1: Overview of the reproduced pipeline and audit**

*The imaging input is the study-level PENet score distributed with RadFusion (grey: reused, not retrained). The EHR arm is an independently re-implemented elastic-net logistic model (green). The two probabilities are combined by late fusion (average or maximum) to give a study-level PE prediction (blue). The label-leakage audit of the EHR arm (orange) comprises SHAP attribution, the prevalence of leakage-candidate features by PE status, and a feature-exclusion ablation. Created in Python 3.11.15 using matplotlib 3.11.2. CTPA: computed tomography pulmonary angiography; EHR: electronic health record; PE: pulmonary embolism; SHAP: SHapley Additive exPlanations.*

**Figure 2: ROC curves on the full test cohort (n=190)**

*Receiver operating characteristic curves for the provided imaging scores (AUROC 0.80), the re-implemented EHR arm (0.91), average late fusion (0.94) and maximum late fusion (0.89); 95% bootstrap CIs are shown in the legend. The dashed line indicates chance. Generated in Python 3.11.15 using matplotlib 3.11.2 and scikit-learn 1.9.1. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record; ROC: receiver operating characteristic.*

**Figure 3: ROC curves on the non-subsegmental subset (n=162)**

*ROC curves on the non-subsegmental subset for the provided imaging scores (AUROC 0.84), the re-implemented EHR arm (0.92), average late fusion (0.96) and maximum late fusion (0.91); 95% bootstrap CIs are shown in the legend. The subset excludes the 28 test studies whose PE was confined to subsegmental vessels. Generated in Python 3.11.15 using matplotlib 3.11.2 and scikit-learn 1.9.1. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record; PE: pulmonary embolism; ROC: receiver operating characteristic.*

**Figure 4: SHAP beeswarm summary for the EHR arm**

*Each point is one test study. Horizontal position is the SHAP value (contribution to the model's log-odds output) and colour encodes the underlying feature value (red, high; blue, low). The 19 highest-ranked features are shown individually and the remainder are summed in the bottom row. The two pulmonary-circulation diagnosis features are the strongest contributors and are the basis of the label-leakage audit described in the Discussion (Temporal label leakage in the EHR arm). Generated in Python using SHAP 0.51.0 and matplotlib 3.11.2. EHR: electronic health record; SHAP: SHapley Additive exPlanations.*

**Figure 5: Label-leakage ablation**

*AUROC with 95% bootstrap CIs for the EHR arm (red) and average late fusion (blue) after refitting the EHR model without each prespecified leakage-candidate feature group. The shaded band and vertical line show the imaging-alone AUROC (0.80) and its 95% CI. Numerical values and paired DeLong tests are in Table 8. Generated in Python 3.11.15 using matplotlib 3.11.2. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record.*
