"""Fill the manuscript template with numbers from results/ and append tables, legends and references.
Outputs submission/manuscript.md (then converted to .docx with pandoc)."""
import json, re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
SUB = ROOT / "submission"
R = json.load(open(RES / "results.json"))
t1 = pd.read_csv(RES / "table1_discrimination.csv")
dl = pd.read_csv(RES / "delong_tests.csv")
abl = pd.read_csv(RES / "table4_leakage_ablation.csv")
prev = pd.read_csv(RES / "leakage_feature_prevalence.csv")
shap = pd.read_csv(RES / "shap_ranking.csv")
sens = pd.read_csv(RES / "sensitivity_analyses.csv")
cohort = pd.read_csv(RES / "table_cohort.csv")
fmap = pd.read_csv(RES / "leakage_feature_map.csv")


def f2(x): return f"{x:.2f}"
def ci(a, lo, hi): return f"{a:.2f} (95% CI {lo:.2f}–{hi:.2f})"
def ci_short(a, lo, hi): return f"{a:.2f} ({lo:.2f}–{hi:.2f})"
def pv(p): return "<0.001" if p < 0.001 else f"{p:.3f}"
def sd(x):
    x = 0.0 if abs(x) < 0.0005 else x
    return (f"{x:+.3f}" if x else "0.000").replace("-", "−")


def arm(analysis, name):
    return t1[(t1.Analysis == analysis) & (t1.Arm == name)].iloc[0]


FULL, NS = "Full test cohort", "Non-subsegmental subset"
IMG, EHR, AVG, MAX = "Imaging (provided PENet score)", "EHR (elastic-net)", "Late fusion (average)", "Late fusion (maximum)"


def dlr(analysis, a, b):
    return dl[(dl.Analysis == analysis) & (dl.Comparison == f"{a} vs {b}")].iloc[0]


def dstr(r):
    return f"{sd(r.Difference)} (95% CI {sd(r.Diff_lo)} to {sd(r.Diff_hi)})"


def abr(name):
    return abl[abl.Model == name].iloc[0]


A_FULL, A_PC = abr("Full model (reference)"), abr("Without pulmonary-circulation diagnoses")
A_AC, A_DD = abr("Without anticoagulant/thrombolytic medications"), abr("Without D-dimer testing")
A_3, A_4 = abr("Without all three prespecified groups"), abr("Without all three + venous-disease diagnoses")


def pr(feature, split):
    return prev[(prev.Feature == feature) & (prev.Split == split)].iloc[0]


PC = "Pulmonary-circulation diagnosis (presence)"
AC = "Any anticoagulant/thrombolytic (inpatient or outpatient)"
pc_tr, pc_te = pr(PC, "Training"), pr(PC, "Test")
ac_tr, ac_te = pr(AC, "Training"), pr(AC, "Test")
pct = lambda s: s.split("(")[1].rstrip(")")
V = R["versions"]; ops = R["table2"]; svc, mx = ops["EHR (SVC)"], ops["Late fusion (maximum)"]
gshare = R["shap"]["group_share_pct"]
ranks = shap[shap.leakage_group.notna()].groupby("leakage_group")["rank"].min()
se = R["se_check"]; se_diff = max(abs(v["bootstrap_se"] - v["delong_se"]) for v in se.values())
gs = R["grid_search"]["best_params"]
s_rows = sens.set_index("Analysis")


def srow(prefix):
    return s_rows.loc[[i for i in s_rows.index if i.startswith(prefix)][0]]


def prop(t):  # (k, n, p, lo, hi)
    k, n, p, lo, hi = t
    return f"{k}/{n} ({100*p:.1f}%; 95% CI {100*lo:.1f}–{100*hi:.1f})"


vals = {
    "avg_full": f2(arm(FULL, AVG).AUROC), "ehr_full": f2(arm(FULL, EHR).AUROC), "img_full": f2(arm(FULL, IMG).AUROC),
    "d_avg_ehr": f"{dlr(FULL, AVG, EHR).Difference:.3f}", "p_avg_ehr": pv(dlr(FULL, AVG, EHR).p),
    "shap_pc": f"{gshare['Pulmonary-circulation diagnoses']:.1f}",
    "pc_train_pos": pct(pc_tr["PE-positive, n/N (%)"]) + "%", "pc_train_neg": pct(pc_tr["PE-negative, n/N (%)"]) + "%",
    "pc_train_pos_pct": pct(pc_tr["PE-positive, n/N (%)"]), "pc_train_neg_pct": pct(pc_tr["PE-negative, n/N (%)"]),
    "ehr_nopc": f2(A_PC["EHR AUROC"]), "avg_nopc": f2(A_PC["Average fusion AUROC"]),
    "p_nopc_img": pv(A_PC["Fusion vs imaging p"]),
    "missing_sentence": "The joined matrix contained no missing values, so no imputation was required." if R["preprocessing"]["missing_values_imputed"] == 0 else f"{R['preprocessing']['missing_values_imputed']} missing values were set to 0 (absence).",
    "n_features": f"{R['preprocessing']['total_features']:,}", "n_nonzero": str(R["model"]["elastic_net"]["nonzero_coefficients"]),
    "svc_sentence": "The SVC hyperparameters were library defaults and were not tuned.",
    "se_agree": f"{se_diff:.3f}",
    "run_year": V["run_date"][:4], "v_python": V["Python"], "v_sklearn": V["scikit-learn"], "v_shap": V["SHAP"],
    "v_numpy": V["NumPy"], "v_pandas": V["pandas"], "v_scipy": V["SciPy"], "v_mpl": V["matplotlib"],
    "avg_full_ci": ci(*arm(FULL, AVG)[["AUROC", "AUROC_lo", "AUROC_hi"]]),
    "ehr_full_ci": ci(*arm(FULL, EHR)[["AUROC", "AUROC_lo", "AUROC_hi"]]),
    "max_full_ci": ci(*arm(FULL, MAX)[["AUROC", "AUROC_lo", "AUROC_hi"]]),
    "img_full_ci": ci(*arm(FULL, IMG)[["AUROC", "AUROC_lo", "AUROC_hi"]]),
    "avg_ns_ci": ci_short(*arm(NS, AVG)[["AUROC", "AUROC_lo", "AUROC_hi"]]),
    "ehr_ns_ci": ci_short(*arm(NS, EHR)[["AUROC", "AUROC_lo", "AUROC_hi"]]),
    "max_ns_ci": ci_short(*arm(NS, MAX)[["AUROC", "AUROC_lo", "AUROC_hi"]]),
    "img_ns_ci": ci_short(*arm(NS, IMG)[["AUROC", "AUROC_lo", "AUROC_hi"]]),
    "d_avg_ehr_full": dstr(dlr(FULL, AVG, EHR)), "p_avg_ehr_full": pv(dlr(FULL, AVG, EHR).p),
    "d_avg_img_full": dstr(dlr(FULL, AVG, IMG)), "p_avg_img_full": pv(dlr(FULL, AVG, IMG).p),
    "d_ehr_img_full": dstr(dlr(FULL, EHR, IMG)), "p_ehr_img_full": pv(dlr(FULL, EHR, IMG).p),
    "d_max_ehr_full": dstr(dlr(FULL, MAX, EHR)), "p_max_ehr_full": pv(dlr(FULL, MAX, EHR).p),
    "d_avg_max_full": dstr(dlr(FULL, AVG, MAX)), "p_avg_max_full": pv(dlr(FULL, AVG, MAX).p),
    "d_avg_ehr_ns": dstr(dlr(NS, AVG, EHR)), "p_avg_ehr_ns": pv(dlr(NS, AVG, EHR).p),
    "svc_counts": f"{svc['TP']} true positives, {svc['FP']} false positives, {svc['FN']} false negatives, {svc['TN']} true negatives",
    "svc_sens": prop(svc["Sensitivity"]), "svc_spec": prop(svc["Specificity"]),
    "svc_lrp": ci_short(*svc["LR+"]).replace("(", "(95% CI ") if False else f"{svc['LR+'][0]:.1f} (95% CI {svc['LR+'][1]:.1f}–{svc['LR+'][2]:.1f})",
    "mx_counts": f"{mx['TP']} true positives, {mx['FP']} false positives, {mx['FN']} false negatives, {mx['TN']} true negatives",
    "mx_sens": prop(mx["Sensitivity"]), "mx_npv": prop(mx["NPV"]),
    "mx_lrn": f"{mx['LR-'][0]:.2f} (95% CI {mx['LR-'][1]:.2f}–{mx['LR-'][2]:.2f})",
    "shap1": f"{shap.iloc[0].mean_abs_shap:.2f}", "shap2": f"{shap.iloc[1].mean_abs_shap:.2f}",
    "shap_veins": f"{gshare['Venous-disease diagnoses']:.1f}", "shap_ac": f"{gshare['Anticoagulant/thrombolytic medications']:.1f}",
    "shap_dd": f"{gshare['D-dimer testing']:.1f}",
    "rank_ac": str(ranks["Anticoagulant/thrombolytic medications"]), "rank_dd": str(ranks["D-dimer testing"]),
    "pc_train_pos_full": pc_tr["PE-positive, n/N (%)"].replace(")", "%)"), "pc_train_neg_full": pc_tr["PE-negative, n/N (%)"].replace(")", "%)"),
    "pc_or_train": f"{pc_tr['Odds ratio']:.1f}",
    "pc_test_pos_full": pc_te["PE-positive, n/N (%)"].replace(")", "%)"), "pc_test_neg_full": pc_te["PE-negative, n/N (%)"].replace(")", "%)"),
    "ac_train_pos": ac_tr["PE-positive, n/N (%)"].replace(")", "%)"), "ac_train_neg": ac_tr["PE-negative, n/N (%)"].replace(")", "%)"),
    "ac_train_p": pv(ac_tr["Fisher p"]),
    "ac_test_pos": ac_te["PE-positive, n/N (%)"].replace(")", "%)"), "ac_test_neg": ac_te["PE-negative, n/N (%)"].replace(")", "%)"),
    "ac_test_p": pv(ac_te["Fisher p"]),
    "ehr_nopc_ci": ci(A_PC["EHR AUROC"], A_PC["EHR lo"], A_PC["EHR hi"]),
    "d_ehr_nopc": f"{sd(A_PC['EHR Δ vs full'])}, 95% CI {sd(A_PC['EHR Δ lo'])} to {sd(A_PC['EHR Δ hi'])}",
    "avg_nopc_ci": ci(A_PC["Average fusion AUROC"], A_PC["Average fusion lo"], A_PC["Average fusion hi"]),
    "d_avg_nopc": f"{sd(A_PC['Average fusion Δ vs full'])}, 95% CI {sd(A_PC['Average fusion Δ lo'])} to {sd(A_PC['Average fusion Δ hi'])}",
    "d_nopc_img": f"difference {sd(A_PC['Fusion vs imaging Δ'])}", "d_full_img": sd(A_FULL["Fusion vs imaging Δ"]),
    "min_p_small": pv(min(A_AC["EHR p"], A_AC["Average fusion p"], A_DD["EHR p"], A_DD["Average fusion p"])),
    "ehr_all3_ci": ci(A_3["EHR AUROC"], A_3["EHR lo"], A_3["EHR hi"]),
    "avg_all3_ci": ci(A_3["Average fusion AUROC"], A_3["Average fusion lo"], A_3["Average fusion hi"]),
    "p_all3_img": pv(A_3["Fusion vs imaging p"]),
    "ehr_all4_ci": ci(A_4["EHR AUROC"], A_4["EHR lo"], A_4["EHR hi"]),
    "avg_all4_ci": ci(A_4["Average fusion AUROC"], A_4["Average fusion lo"], A_4["Average fusion hi"]),
    "s_scale_ehr": f2(srow("Standardization")["EHR AUROC"]), "s_scale_avg": f2(srow("Standardization")["Average fusion AUROC"]),
    "gs_params": f"C={gs['C']} and L1 ratio {gs['l1_ratio']}, the same as the reference configuration,",
    "s_gs_ehr": f2(srow("Elastic-net tuned")["EHR AUROC"]), "s_gs_avg": f2(srow("Elastic-net tuned")["Average fusion AUROC"]),
    "s_gs3_ehr": f2(srow("Grid-searched")["EHR AUROC"]), "s_gs3_avg": f2(srow("Grid-searched")["Average fusion AUROC"]),
    "abs_d_ehr_nopc": f"{abs(A_PC['EHR Δ vs full']):.2f}", "abs_d_avg_nopc": f"{abs(A_PC['Average fusion Δ vs full']):.2f}",
    "mx_sens_pt": f"{mx['Sensitivity'][2]:.2f}", "mx_npv_pt": f"{mx['NPV'][2]:.2f}",
    "svc_spec_pt": f"{svc['Specificity'][2]:.2f}", "svc_ppv_pt": f"{svc['PPV'][2]:.2f}",
    "AFFILIATION": "School of Arts and Sciences",
}

src = (SUB / "manuscript_src.md").read_text()
src = src.replace("«AFFILIATION»", vals["AFFILIATION"])
missing = set(re.findall(r"\{\{(\w+)\}\}", src)) - set(vals)
assert not missing, missing
body = re.sub(r"\{\{(\w+)\}\}", lambda m: vals[m.group(1)], src).replace("p=<", "p<")

# ---------------------------------------------------------------- tables
def md_table(df):
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(out)


T = []
T.append(("Table 1: Study cohort by predefined split",
          md_table(cohort.rename(columns={"Split": "Split"})),
          "Values are n or n (%), with percentages of all studies in that split. PE subtype is shown for PE-positive studies (central, segmental, subsegmental) as the most proximal clot location recorded in the released dataset. Splits are those distributed with RadFusion and used to develop PENet; no studies were excluded. PE: pulmonary embolism."))

pp = R["preprocessing"]["per_table"]
names = {"Demographics": "Demographics", "INP_MED": "Inpatient medications", "OUT_MED": "Outpatient medications",
         "ICD": "ICD diagnosis groupings", "LABS": "Laboratory tests", "Vitals": "Vital signs"}
rows = []
for k in ["Demographics", "INP_MED", "OUT_MED", "ICD", "LABS", "Vitals"]:
    d = pp[k]
    rows.append({"EHR table": names[k], "Rows in released file": f"{d['rows_in_file']:,}", "Studies after de-duplication": f"{d['studies']:,}",
                 "Features released": f"{d['features_raw']:,}", "Features after zero-variance removal": f"{d['features_after_zero_variance']:,}"})
rows.append({"EHR table": "Total", "Rows in released file": "", "Studies after de-duplication": "1,837",
             "Features released": f"{sum(pp[k]['features_raw'] for k in pp):,}", "Features after zero-variance removal": f"{R['preprocessing']['total_features']:,}"})
T.append(("Table 2: EHR feature counts at each preprocessing step", md_table(pd.DataFrame(rows)),
          f"Features released are those in the public RadFusion tables, which were already aggregated into presence/frequency or presence/latest-value indicators and filtered by the dataset authors to diagnosis groupings present in ≥1% of training studies. Fifty-one studies appeared twice with identical rows in five tables and were de-duplicated. After z-standardization, the {R['preprocessing']['total_features']:,} features entered the elastic-net model, which assigned non-zero coefficients to {R['model']['elastic_net']['nonzero_coefficients']}. EHR: electronic health record; ICD: International Classification of Diseases."))

rows = []
for a in [FULL, NS]:
    for name in [IMG, EHR, AVG, MAX]:
        r = arm(a, name)
        rows.append({"Analysis": f"{a}, n={r['n (PE+/PE−)'].split(' ')[0]} ({r['n (PE+/PE−)'].split('(')[1].rstrip(')').replace('/', ' PE-positive/')} PE-negative)" if name == IMG else "",
                     "Arm": name, "AUROC (95% CI)": ci_short(r.AUROC, r.AUROC_lo, r.AUROC_hi), "AUPRC (95% CI)": ci_short(r.AUPRC, r.AUPRC_lo, r.AUPRC_hi)})
T.append(("Table 3: Discrimination by modality on the held-out test set", md_table(pd.DataFrame(rows)),
          "Values are point estimates with 95% CIs from 2,000 stratified bootstrap resamples (percentile method). The imaging arm is the PENet score distributed with the benchmark, not a model trained here. The EHR arm is the elastic-net logistic model. Average fusion is the mean and maximum fusion the elementwise maximum of the imaging and EHR probabilities. Paired between-arm tests are given in Table 4. AUROC: area under the receiver operating characteristic curve; AUPRC: area under the precision-recall curve (average precision); CI: confidence interval; EHR: electronic health record; PE: pulmonary embolism."))

rows = []
for a in [FULL, NS]:
    for _, r in dl[dl.Analysis == a].iterrows():
        x, y = r.Comparison.split(" vs ")
        first = not any(q.get("_a") == a for q in rows)
        rows.append({"_a": a, "Analysis": a if first else "",
                     "Comparison (A vs B)": f"{x} vs {y}", "AUROC A": f2(r["AUROC A"]), "AUROC B": f2(r["AUROC B"]),
                     "Difference (95% CI)": f"{sd(r.Difference)} ({sd(r.Diff_lo)} to {sd(r.Diff_hi)})", "z": f"{r.z:.2f}".replace("-", "−"), "p-value": pv(r.p)})
T.append(("Table 4: Paired comparisons of AUROC between arms", md_table(pd.DataFrame(rows).drop(columns="_a")),
          "Differences, their 95% CIs, z statistics and two-sided p-values are from the DeLong test for correlated ROC curves. p-values are unadjusted for multiple comparisons and are exploratory. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record."))


def cell(t):
    k, n, p, lo, hi = t
    return f"{k}/{n} ({100*p:.0f}%); {p:.2f} ({lo:.2f}–{hi:.2f})"


rows = []
for m in ["Sensitivity", "Specificity", "PPV", "NPV", "Accuracy"]:
    rows.append({"Metric": m, "EHR (SVC), specificity-oriented": cell(svc[m]), "Late fusion (maximum), sensitivity-oriented": cell(mx[m])})
rows.append({"Metric": "F1 score", "EHR (SVC), specificity-oriented": f"{svc['F1']:.2f}", "Late fusion (maximum), sensitivity-oriented": f"{mx['F1']:.2f}"})
rows.append({"Metric": "LR+ (95% CI)", "EHR (SVC), specificity-oriented": f"{svc['LR+'][0]:.1f} ({svc['LR+'][1]:.1f}–{svc['LR+'][2]:.1f})", "Late fusion (maximum), sensitivity-oriented": f"{mx['LR+'][0]:.1f} ({mx['LR+'][1]:.1f}–{mx['LR+'][2]:.1f})"})
rows.append({"Metric": "LR− (95% CI)", "EHR (SVC), specificity-oriented": f"{svc['LR-'][0]:.2f} ({svc['LR-'][1]:.2f}–{svc['LR-'][2]:.2f})", "Late fusion (maximum), sensitivity-oriented": f"{mx['LR-'][0]:.2f} ({mx['LR-'][1]:.2f}–{mx['LR-'][2]:.2f})"})
rows.append({"Metric": "Confusion matrix (TP/FP/FN/TN)", "EHR (SVC), specificity-oriented": f"{svc['TP']}/{svc['FP']}/{svc['FN']}/{svc['TN']}", "Late fusion (maximum), sensitivity-oriented": f"{mx['TP']}/{mx['FP']}/{mx['FN']}/{mx['TN']}"})
T.append(("Table 5: Operating-point metrics at a fixed 0.5 threshold (test set, n=190; 110 PE-positive, 80 PE-negative)", md_table(pd.DataFrame(rows)),
          "Proportions are shown as n/N (%) followed by the proportion with its Wilson score 95% CI. Likelihood-ratio 95% CIs use the log method. No hypothesis test was performed. Predictive values depend on the enriched test-set prevalence (57.9%) and are optimistic relative to routine practice; likelihood ratios are prevalence-independent. **The EHR column reflects the support-vector classifier (SVC) variant, not the elastic-net logistic model whose discrimination is reported in Table 3.** PE: pulmonary embolism; EHR: electronic health record; PPV/NPV: positive/negative predictive value; LR+/LR−: positive/negative likelihood ratio; TP/FP/FN/TN: true positives/false positives/false negatives/true negatives; CI: confidence interval; F1: harmonic mean of PPV and sensitivity."))

top = shap.head(10)
rows = [{"Rank": int(r["rank"]), "Feature (source table)": r.feature, "Mean absolute SHAP (log-odds)": f"{r.mean_abs_shap:.3f}",
         "Share of total (%)": f"{r.share_of_total_pct:.1f}", "Cumulative share (%)": f"{r.cumulative_share_pct:.1f}",
         "Leakage-candidate group": r.leakage_group if isinstance(r.leakage_group, str) else "–"} for _, r in top.iterrows()]
T.append(("Table 6: Ten highest-ranked EHR features by SHAP attribution", md_table(pd.DataFrame(rows)),
          f"Mean absolute SHAP value over the 190 test studies (exact linear SHAP, training-set background, log-odds units) and its share of the summed attribution across all {R['preprocessing']['total_features']:,} features. Group shares of total attribution: pulmonary-circulation diagnoses {gshare['Pulmonary-circulation diagnoses']:.1f}%; venous-disease diagnoses {gshare['Venous-disease diagnoses']:.1f}%; anticoagulant/thrombolytic medications {gshare['Anticoagulant/thrombolytic medications']:.1f}%; D-dimer testing {gshare['D-dimer testing']:.1f}%. Feature names are as released (\"presence\" and \"frequency\" refer to ICD groupings; \"Binary\" to test ordered; \"ptt\" and \"inr\" to partial thromboplastin time and international normalized ratio). EHR: electronic health record; SHAP: SHapley Additive exPlanations; ICD: International Classification of Diseases."))

p2 = prev.copy(); p2["Odds ratio"] = p2["Odds ratio"].map(lambda x: f"{x:.1f}"); p2["Fisher p"] = p2["Fisher p"].map(pv)
p2 = p2.rename(columns={"Fisher p": "p-value (Fisher's exact)"})
T.append(("Table 7: Presence of leakage-candidate features by PE status", md_table(p2),
          "n/N (%) of PE-positive and PE-negative studies in which the feature was recorded as present (non-zero) in the released tables. Odds ratios and two-sided p-values are from Fisher's exact test. PE: pulmonary embolism."))

rows = []
for _, r in abl.iterrows():
    ref = r.Model.startswith("Full")
    rows.append({"Model": r.Model, "Features removed / used": f"{int(r['Features removed'])} / {int(r['Features used']):,}",
                 "EHR AUROC (95% CI)": ci_short(r["EHR AUROC"], r["EHR lo"], r["EHR hi"]),
                 "EHR Δ vs full (95% CI); p": "Reference" if ref else f"{sd(r['EHR Δ vs full'])} ({sd(r['EHR Δ lo'])} to {sd(r['EHR Δ hi'])}); {pv(r['EHR p'])}",
                 "Average-fusion AUROC (95% CI)": ci_short(r["Average fusion AUROC"], r["Average fusion lo"], r["Average fusion hi"]),
                 "Fusion Δ vs full (95% CI); p": "Reference" if ref else f"{sd(r['Average fusion Δ vs full'])} ({sd(r['Average fusion Δ lo'])} to {sd(r['Average fusion Δ hi'])}); {pv(r['Average fusion p'])}",
                 "Fusion vs imaging alone: Δ; p": f"{sd(r['Fusion vs imaging Δ'])}; {pv(r['Fusion vs imaging p'])}",
                 "Non-subsegmental EHR / fusion AUROC": f"{r['EHR AUROC nonsub']:.2f} / {r['Fusion AUROC nonsub']:.2f}"})
T.append(("Table 8: Label-leakage ablation: EHR and fusion discrimination after excluding leakage-candidate feature groups", md_table(pd.DataFrame(rows)),
          f"Each row refits the elastic-net EHR model with the reference configuration after removing the listed feature group(s); average late fusion is recomputed with the fixed imaging score (imaging-alone AUROC {f2(arm(FULL, IMG).AUROC)}). AUROC 95% CIs are from 2,000 stratified bootstrap resamples; differences (Δ), their 95% CIs and two-sided p-values are from paired DeLong tests against the full model, or against imaging alone in the penultimate column. Groups were prespecified on clinical criteria before the ablation was run (Supplementary Table S2). A fall in AUROC measures reliance on the excluded features and does not by itself establish leakage. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record."))

tables_md = "\n\n".join(f"**{t}**\n\n{tab}\n\n*{leg}*" for t, tab, leg in T)

# ---------------------------------------------------------------- figure legends
FIGS = [
    ("Figure 1: Overview of the reproduced pipeline and audit",
     "The imaging input is the study-level PENet score distributed with RadFusion (grey: reused, not retrained). The EHR arm is an independently re-implemented elastic-net logistic model (green). The two probabilities are combined by late fusion (average or maximum) to give a study-level PE prediction. SHAP attribution of the EHR arm supports feature interpretation and the label-leakage audit (orange), which is quantified by the feature-exclusion ablation. Created by the author in Python using matplotlib. CTPA: computed tomography pulmonary angiography; EHR: electronic health record; PE: pulmonary embolism; SHAP: SHapley Additive exPlanations."),
    ("Figure 2: ROC curves on the full test cohort (n=190)",
     f"Receiver operating characteristic curves for the provided imaging scores (AUROC {f2(arm(FULL, IMG).AUROC)}), the re-implemented EHR arm ({f2(arm(FULL, EHR).AUROC)}), average late fusion ({f2(arm(FULL, AVG).AUROC)}) and maximum late fusion ({f2(arm(FULL, MAX).AUROC)}); 95% bootstrap CIs are shown in the legend. The dashed line indicates chance. Generated in Python {V['Python']} using matplotlib {V['matplotlib']} and scikit-learn {V['scikit-learn']}. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record; ROC: receiver operating characteristic."),
    ("Figure 3: ROC curves on the non-subsegmental subset (n=162)",
     f"ROC curves on the non-subsegmental subset for the provided imaging scores (AUROC {f2(arm(NS, IMG).AUROC)}), the re-implemented EHR arm ({f2(arm(NS, EHR).AUROC)}), average late fusion ({f2(arm(NS, AVG).AUROC)}) and maximum late fusion ({f2(arm(NS, MAX).AUROC)}); 95% bootstrap CIs are shown in the legend. The subset excludes the 28 test studies whose PE was confined to subsegmental vessels. Generated in Python {V['Python']} using matplotlib {V['matplotlib']} and scikit-learn {V['scikit-learn']}. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record; PE: pulmonary embolism; ROC: receiver operating characteristic."),
    ("Figure 4: SHAP beeswarm summary for the EHR arm",
     "Each point is one test study. Horizontal position is the SHAP value (contribution to the model's log-odds output) and colour encodes the underlying feature value (red, high; blue, low). The 19 highest-ranked features are shown individually and the remainder are summed in the bottom row. The two pulmonary-circulation diagnosis features are the strongest contributors and are the basis of the label-leakage audit described in the Discussion (Temporal label leakage in the EHR arm). Generated in Python using SHAP " + V["SHAP"] + " and matplotlib " + V["matplotlib"] + ". EHR: electronic health record; SHAP: SHapley Additive exPlanations."),
    ("Figure 5: Label-leakage ablation",
     f"AUROC with 95% bootstrap CIs for the EHR arm (red) and average late fusion (blue) after refitting the EHR model without each prespecified leakage-candidate feature group. The shaded band and vertical line show the imaging-alone AUROC ({f2(arm(FULL, IMG).AUROC)}) and its 95% CI. Numerical values and paired DeLong tests are in Table 8. Generated in Python {V['Python']} using matplotlib {V['matplotlib']}. AUROC: area under the receiver operating characteristic curve; CI: confidence interval; EHR: electronic health record."),
]
FIG_FILES = ["Figure_1_pipeline_overview.png", "Figure_2_ROC_full_test_cohort.png", "Figure_3_ROC_nonsubsegmental.png",
             "Figure_4_SHAP_beeswarm.png", "Figure_5_leakage_ablation.png"]
figs_md = "\n\n".join(f"**{t}**\n\n*{l}*" for t, l in FIGS)
figs_with_img = "\n\n".join(f"![](figures/{f}){{width=6in}}\n\n**{t}**\n\n*{l}*" for f, (t, l) in zip(FIG_FILES, FIGS))

refs = (SUB / "references.md").read_text()
decl = (SUB / "declarations.md").read_text()
out = body + "\n\n" + decl + "\n\n# References\n\n" + refs + "\n\n# Tables\n\n" + tables_md + "\n\n# Figures\n\n" + figs_with_img + "\n"
(SUB / "manuscript.md").write_text(out)
(SUB / "figure_legends.md").write_text("# Figure legends\n\n" + figs_md + "\n")
(SUB / "tables.md").write_text("# Tables\n\n" + tables_md + "\n")
json.dump(vals, open(SUB / "filled_values.json", "w"), indent=1)
print("ok", len(body.split()), "words in body")
abstract = body.split("# Abstract")[1].split("**Keywords")[0]
print("abstract words:", len(abstract.split()))

# ---------------------------------------------------------------- response letter
vals["ehr_auprc"] = f2(arm(FULL, EHR).AUPRC)
vals["svc_tp"] = str(svc["TP"])
rl = (SUB / "response_to_editors_src.md").read_text().replace("«AFFILIATION»", vals["AFFILIATION"])
miss = set(re.findall(r"\{\{(\w+)\}\}", rl)) - set(vals)
assert not miss, miss
(SUB / "response_to_editors.md").write_text(re.sub(r"\{\{(\w+)\}\}", lambda m: vals[m.group(1)], rl))
