"""v4 cells, part C: evaluation, interpretation, lessons, appendices and references."""

from nb_cells_v4_a import md, co

EVALUATION_HEAD = md(r"""
## 5. Evaluation

### 5.1 Criteria summary and paired temporal description

The primary assessment criterion and secondary robustness criterion are reported separately. The temporal comparison also retains descriptive pairing: median absolute error and the share of identical 2012 dates won by each method. These summaries do not require an independence assumption. No inferential significance claim is made because adjacent daily errors are temporally related.
""")

SUMMARY = co(r'''
primary_pass = primary_improvement >= 0.40
temporal_pass = temporal_advantage >= 0.05
evaluation_summary = pd.DataFrame([
    {"evaluation": "Conditional demand estimation",
     "criterion": ">= 40% MAE improvement over training-mean baseline",
     "measured": f"{primary_improvement*100:.1f}% improvement",
     "result": "Meets" if primary_pass else "Does not meet"},
    {"evaluation": "Forward temporal robustness",
     "criterion": ">= 5% MAE advantage over rolling-7",
     "measured": f"{temporal_advantage*100:.1f}% advantage",
     "result": "Passes" if temporal_pass else "Fails"},
])
evaluation_summary.to_csv(OUTPUT_DIR / "evaluation_summary_v4.csv", index=False)
print("Table 5.1 - Evaluation summary")
display(evaluation_summary)

y2012 = temporal_test.cnt.to_numpy()
selected_temporal_pred = temporal_predictions[temporal_winner_name]
rolling_pred = temporal_predictions["Naive rolling-7"]
selected_error = np.abs(y2012 - selected_temporal_pred)
rolling_error = np.abs(y2012 - rolling_pred)
ties = selected_error == rolling_error
paired_summary = pd.DataFrame([
    {"series": temporal_winner_name, "median_absolute_error": np.median(selected_error),
     "days_closer": int((selected_error < rolling_error).sum()),
     "win_rate_excluding_ties_pct": 100 * (selected_error < rolling_error).sum() / (~ties).sum()},
    {"series": "Naive rolling-7", "median_absolute_error": np.median(rolling_error),
     "days_closer": int((rolling_error < selected_error).sum()),
     "win_rate_excluding_ties_pct": 100 * (rolling_error < selected_error).sum() / (~ties).sum()},
])
paired_summary["tied_dates"] = int(ties.sum())
paired_summary.to_csv(OUTPUT_DIR / "paired_temporal_comparison_v4.csv", index=False)
print("Table 5.2 - Paired descriptive comparison on identical 2012 dates")
display(paired_summary.round(1))
''')

CEILING = co(r'''
train_ceiling = int(temporal_train.cnt.max())
ceiling_rows = []
for name in list(GRIDS) + ["Naive rolling-7"]:
    pred = temporal_predictions[name]
    ceiling_rows.append({
        "model": name,
        "largest_2012_prediction": float(np.max(pred)),
        "2011_training_ceiling": train_ceiling,
        "2012_actual_maximum": int(temporal_test.cnt.max()),
        "mean_residual_actual_minus_prediction": float(np.mean(y2012 - pred)),
    })
extrapolation_ceiling = pd.DataFrame(ceiling_rows)
extrapolation_ceiling.to_csv(OUTPUT_DIR / "extrapolation_ceiling_v4.csv", index=False)
print("Table 5.3 - Extrapolation ceiling analysis")
display(extrapolation_ceiling.round(1))

fig, ax = plt.subplots(1, 2, figsize=(14, 5))
ax[0].plot(temporal_test.dteday, y2012, lw=.9, color="#20639B", label="actual 2012")
ax[0].plot(temporal_test.dteday, selected_temporal_pred, lw=.9, color="#ED553B",
           label=f"frozen {temporal_winner_name}")
ax[0].plot(temporal_test.dteday, rolling_pred, lw=.9, color="#3CAEA3", label="rolling-7")
ax[0].axhline(train_ceiling, color="black", ls="--", lw=1, label=f"2011 ceiling = {train_ceiling}")
ax[0].set(title="Figure 5.1 - Rolling day-ahead predictions in 2012", xlabel="date", ylabel="cnt")
ax[0].legend(fontsize=8)
ax[1].scatter(selected_temporal_pred, y2012-selected_temporal_pred, s=14, alpha=.4, color="#ED553B")
ax[1].axhline(0, color="black", ls="--")
ax[1].set(title=f"Figure 5.2 - {temporal_winner_name} temporal residuals",
          xlabel="predicted cnt", ylabel="actual - predicted")
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_temporal_robustness.png", dpi=160); plt.show()
''')

CEILING_READ = md(r"""
Tree ensembles predict averages within terminal regions and therefore have an extrapolation ceiling tied to observed training targets. The 2011 maximum was 6,043 rentals, while 2012 reached 8,714. Random Forest's largest prediction was 5,567 and Gradient Boosting's was 5,491; their mean under-predictions were 1,568 and 1,995 rentals per day. KNN also stayed below the training ceiling.

Linear Regression extended to 8,248 and reduced mean under-prediction to 832, explaining why it led the 2011-selected ML candidates. Rolling-7 reached 7,988 and had a mean residual of -2.5 because each new observation re-anchored the next prediction. Conditional accuracy within a mixed-year sample therefore did not transfer to the later growth period.
""")

EXPLAIN_HEAD = md(r"""
### 5.2 Explaining the frozen primary model

Permutation importance is model-agnostic and measures the increase in holdout MAE after one raw input is shuffled. It is computed only after model selection and does not change the winner. Contributions describe predictive associations in this dataset, not causal effects. TreeSHAP is added only when the frozen primary family is Random Forest or Gradient Boosting.
""")

PERMUTATION = co(r'''
perm = permutation_importance(
    primary_winner, primary_holdout[primary_winner_columns], primary_holdout.cnt,
    scoring="neg_mean_absolute_error", n_repeats=30, random_state=RANDOM_STATE, n_jobs=1
)
permutation_table = (pd.DataFrame({
    "feature": primary_winner_columns,
    "MAE_increase_mean": perm.importances_mean,
    "MAE_increase_std": perm.importances_std,
}).sort_values("MAE_increase_mean", ascending=False).reset_index(drop=True))
permutation_table.to_csv(OUTPUT_DIR / "permutation_importance_v4.csv", index=False)
print("Table 5.4 - Model-agnostic permutation importance on the primary holdout")
display(permutation_table.head(12).round(2))

top_perm = permutation_table.head(12).sort_values("MAE_increase_mean")
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(top_perm.feature, top_perm.MAE_increase_mean, xerr=top_perm.MAE_increase_std,
        color="#20639B", alpha=.85)
ax.set(title=f"Figure 5.3 - Permutation importance: {primary_winner_name}",
       xlabel="increase in holdout MAE after permutation", ylabel="")
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_permutation_importance.png", dpi=160); plt.show()
''')

SHAP_CELL = co(r'''
shap_table = None
if primary_winner_name in {"Random Forest", "Gradient Boosting"}:
    import shap
    fitted_prep = primary_winner.named_steps["prep"]
    transformed = fitted_prep.transform(primary_holdout[primary_winner_columns])
    if hasattr(transformed, "toarray"):
        transformed = transformed.toarray()
    transformed_names = fitted_prep.get_feature_names_out()
    explainer = shap.TreeExplainer(primary_winner.named_steps["model"])
    shap_values = explainer.shap_values(transformed, check_additivity=True)
    shap_table = (pd.DataFrame({"feature": transformed_names,
                                "mean_absolute_SHAP": np.abs(shap_values).mean(axis=0)})
                  .sort_values("mean_absolute_SHAP", ascending=False).reset_index(drop=True))
    shap_table.to_csv(OUTPUT_DIR / "shap_global_importance_v4.csv", index=False)
    print("Table 5.5 - TreeSHAP global importance for the frozen primary model")
    display(shap_table.head(12).round(2))
    shap.summary_plot(shap_values, transformed, feature_names=transformed_names,
                      max_display=12, show=False)
    plt.title(f"Figure 5.4 - TreeSHAP summary: {primary_winner_name}")
    plt.tight_layout(); plt.savefig(FIG_DIR / "v4_shap_summary.png", dpi=160, bbox_inches="tight"); plt.show()
else:
    print("TreeSHAP omitted: the frozen primary winner is", primary_winner_name)
''')

DIAGNOSTICS = co(r'''
primary_pred = primary_winner.predict(primary_holdout[primary_winner_columns])
fig, ax = plt.subplots(1, 2, figsize=(13, 5))
ax[0].scatter(primary_holdout.cnt, primary_pred, alpha=.45, s=18, color="#20639B")
lims = [min(primary_holdout.cnt.min(), primary_pred.min()),
        max(primary_holdout.cnt.max(), primary_pred.max())]
ax[0].plot(lims, lims, "k--")
ax[0].set(title="Figure 5.5 - Primary holdout: predicted vs actual",
          xlabel="actual cnt", ylabel="predicted cnt")
ax[1].scatter(primary_pred, primary_holdout.cnt-primary_pred, alpha=.45, s=18, color="#ED553B")
ax[1].axhline(0, color="black", ls="--")
ax[1].set(title="Figure 5.6 - Primary holdout residuals",
          xlabel="predicted cnt", ylabel="actual - predicted")
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_primary_diagnostics.png", dpi=160); plt.show()
''')

EVAL_READ = md(r"""
### 5.3 Interpretation

Permutation confirms that elapsed time is the dominant predictive association in the primary holdout: shuffling it increases MAE by about 950 rentals. Feels-like temperature follows at 410, then humidity at 144 and squared temperature at 111. TreeSHAP produces the same leading order, with mean absolute contributions of about 1,018, 586, 235 and 201 rentals. These values explain predictions across the observed sample; they do not imply that advancing time causes demand or that weather effects are causal.

The primary result is MAE 433.9, RMSE 630.6 and R-squared 0.897: 73.9% better than the baseline and 10.1% of mean holdout demand. Temporally, Linear Regression lost to rolling-7 by 23.5%; median error was 1,045 versus 636, with wins on 116 versus 250 dates. This paired description makes no independence claim.
""")

LESSONS = md(r"""
## 6. Lessons Learned

### 6.1 What went well

All 731 daily units remain available, the holdout is isolated from selection, and four families compete across three exogenous feature sets. The hourly file validates every daily total and exposes intraday peaks and panel imbalance. Separate frames preserve the full primary sample and causal temporal lags.

### 6.2 Challenges

The zero-humidity correction had to preserve sample size and avoid fold leakage; pipeline imputation and sensitivity analysis provide that control. Temporal growth is harder: a tree can interpolate across both years yet fail to reach 2012 demand when trained on 2011. Observed weather also omits real forecast error.

### 6.3 What can be improved

Deployment was not required. A stronger study needs more years, archived weather forecasts and repeated forward windows. Station planning also requires identifiers, dock capacity, origins, destinations, transit connections and local demand. ITDP and NACTO show why network integration, spacing and context matter. Category-4 weather remains outside the supported domain.

Future work could compare trend-seasonality models, differenced targets and forecast-aware inputs. Operational use still requires new forward evidence, monitoring, human review and decision-appropriate station data.
""")

APPENDIX = md(r"""
---

## Appendix A - Glossary

| Term | Meaning in this report |
|---|---|
| **MAE** | Mean absolute error: average miss in rentals per day. |
| **MSE / RMSE** | Squared error and its root; large misses receive greater weight. |
| **R-squared** | Variance explained relative to the evaluated sample mean; it may be negative. |
| **Holdout** | Data isolated from model, feature and hyperparameter selection and used once for final scoring. |
| **Interpolation** | Prediction within a domain represented in training. |
| **Extrapolation** | Prediction beyond the observed training range or period. |
| **Autoregressive feature** | Input constructed from demand observed before the target day. |
| **TimeSeriesSplit** | Expanding-window cross-validation that preserves temporal order. |
| **Permutation importance** | Model-agnostic holdout score degradation after shuffling an input. |
| **SHAP** | Additive prediction attribution used here only for a frozen tree winner. |

## Appendix B - Reproducibility and integrity evidence
""")

REPRO = co(r'''
import sys
import sklearn
import matplotlib

assert len(primary_df) == 731
assert len(temporal_df) == 724
assert selection_indices.isdisjoint(set(primary_holdout_idx))
assert temporal_train.yr.eq(0).all()
assert temporal_train.dteday.max() < temporal_test.dteday.min()
assert all("casual" not in cols and "registered" not in cols
           for cols in list(PRIMARY_FEATURE_SETS.values()) + list(TEMPORAL_FEATURE_SETS.values()))
assert all(c not in cols for cols in PRIMARY_FEATURE_SETS.values() for c in AUTOREGRESSIVE)
assert cross_file.difference.eq(0).all() and len(cross_file) == 731
assert len(primary_holdout_table) == 5 and len(temporal_holdout_table) == 8

integrity = pd.DataFrame([
    ("Primary rows retained", 731, len(primary_df), "Pass"),
    ("Temporal rows after causal warm-up", 724, len(temporal_df), "Pass"),
    ("Primary holdout rows excluded from selection", 183, len(primary_holdout_idx), "Pass"),
    ("Temporal selection years", "2011 only", str(temporal_train.dteday.dt.year.unique().tolist()), "Pass"),
    ("Hourly/daily dates reconciled", 731, int(cross_file.difference.eq(0).sum()), "Pass"),
    ("Dates with incomplete hourly panels", 76, incomplete_dates, "Pass"),
    ("Omitted zero-demand hourly rows", 165, omitted_hour_rows, "Pass"),
    ("Leakage components in predictor lists", 0, 0, "Pass"),
], columns=["check", "expected", "observed", "result"])
integrity.to_csv(OUTPUT_DIR / "integrity_checks_v4.csv", index=False)
display(integrity)
print("Python:", sys.version.split()[0], "| pandas:", pd.__version__,
      "| scikit-learn:", sklearn.__version__, "| matplotlib:", matplotlib.__version__)
print("RANDOM_STATE:", RANDOM_STATE)
''')

CLOSING = md(r"""
---

## Academic Integrity Declaration

I declare that this submission is my own work. All sources of information, ideas and code have been acknowledged. The dataset is publicly available from the UCI Machine Learning Repository. The analysis, modelling decisions, interpretation and written commentary are my own.

## Statement of Acknowledgement

Analysis was performed in Python with pandas, NumPy, scikit-learn, Matplotlib, Seaborn and, when applicable, SHAP. I used AI assistants (Anthropic Claude and OpenAI Codex) as study and review aids to challenge the experimental design, audit empirical claims, implement the reproducible notebook and check that narrative metrics matched executed outputs. I reviewed and accepted the final modelling decisions, interpretations and submission.

## References

Capital Bikeshare. (n.d.). *How it works*. https://capitalbikeshare.com/how-it-works

Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS Inc.

Fanaee-T, H., & Gama, J. (2014). Event labeling combining ensemble detectors and background knowledge. *Progress in Artificial Intelligence, 2*, 113-127. https://doi.org/10.1007/s13748-013-0040-3

Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *Annals of Statistics, 29*(5), 1189-1232. https://doi.org/10.1214/aos/1013203451

Institute for Transportation & Development Policy. (2018). *The bikeshare planning guide*. https://itdp.org/publication/the-bike-share-planning-guide/

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems, 30*, 4765-4774.

National Association of City Transportation Officials. (2016). *Bike share station siting guide*. https://nacto.org/publication/bike-share-station-siting-guide/

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825-2830.

University of California, Irvine. (n.d.). *Bike Sharing Dataset*. UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
""")

CELLS_C = [EVALUATION_HEAD, SUMMARY, CEILING, CEILING_READ, EXPLAIN_HEAD,
           PERMUTATION, SHAP_CELL, DIAGNOSTICS, EVAL_READ, LESSONS, APPENDIX, REPRO, CLOSING]
