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
print("Table 14 - Evaluation summary")
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
print("Table 15 - Paired descriptive comparison on identical 2012 dates")
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
print("Table 16 - Extrapolation ceiling analysis")
display(extrapolation_ceiling.round(1))

fig, ax = plt.subplots(1, 2, figsize=(14, 5))
ax[0].plot(temporal_test.dteday, y2012, lw=.9, color="#20639B", label="actual 2012")
ax[0].plot(temporal_test.dteday, selected_temporal_pred, lw=.9, color="#ED553B",
           label=f"frozen {temporal_winner_name}")
ax[0].plot(temporal_test.dteday, rolling_pred, lw=.9, color="#3CAEA3", label="rolling-7")
ax[0].axhline(train_ceiling, color="black", ls="--", lw=1, label=f"2011 ceiling = {train_ceiling}")
ax[0].set(title="Figure 9 - Rolling day-ahead predictions in 2012", xlabel="date", ylabel="cnt")
ax[0].legend(fontsize=8)
ax[1].scatter(selected_temporal_pred, y2012-selected_temporal_pred, s=14, alpha=.4, color="#ED553B")
ax[1].axhline(0, color="black", ls="--")
ax[1].set(title=f"Figure 10 - {temporal_winner_name} temporal residuals",
          xlabel="predicted cnt", ylabel="actual - predicted")
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_temporal_robustness.png", dpi=160); plt.show()
''')

CEILING_READ = md(r"""
Tree ensembles predict averages within terminal regions and therefore have an extrapolation ceiling tied to observed training targets. The 2011 maximum was 6,043 rentals, while 2012 reached 8,714. Random Forest's largest prediction was 5,567 and Gradient Boosting's was 5,491; their mean under-predictions were 1,568 and 1,995 rentals per day. KNN also stayed below the training ceiling.

Linear Regression extended to 8,248 and reduced mean under-prediction to 832, explaining why it led the 2011-selected ML candidates. Rolling-7 reached 7,988 and had a mean residual of -2.5 because each new observation re-anchored the next prediction. Conditional accuracy within a mixed-year sample therefore did not transfer to the later growth period.
""")

EXPLAIN_HEAD = md(r"""
### 5.2 Explaining the frozen primary model

Permutation importance is model-agnostic and measures the increase in holdout MAE after one raw input is shuffled. It is computed only after model selection and does not change the winner. Contributions describe predictive associations in this dataset, not causal effects. TreeSHAP (Lundberg & Lee, 2017) is added only when the frozen primary family is Random Forest or Gradient Boosting.
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
print("Table 17 - Model-agnostic permutation importance on the primary holdout")
display(permutation_table.head(12).round(2))

top_perm = permutation_table.head(12).sort_values("MAE_increase_mean")
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(top_perm.feature, top_perm.MAE_increase_mean, xerr=top_perm.MAE_increase_std,
        color="#20639B", alpha=.85)
ax.set(title=f"Figure 11 - Permutation importance: {primary_winner_name}",
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
    print("Table 18 - TreeSHAP global importance for the frozen primary model")
    display(shap_table.head(12).round(2))
    shap.summary_plot(shap_values, transformed, feature_names=transformed_names,
                      max_display=12, show=False)
    plt.title(f"Figure 12 - TreeSHAP summary: {primary_winner_name}")
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
ax[0].set(title="Figure 13 - Primary holdout: predicted vs actual",
          xlabel="actual cnt", ylabel="predicted cnt")
ax[1].scatter(primary_pred, primary_holdout.cnt-primary_pred, alpha=.45, s=18, color="#ED553B")
ax[1].axhline(0, color="black", ls="--")
ax[1].set(title="Figure 14 - Primary holdout residuals",
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

The method built during Assessments 1 and 2 carried straight into this project and shortened the setup considerably. Declaring criteria before modelling, keeping a holdout untouched until selection finishes, running an ablation to attribute a metric change to a cause, and operating the notebook as a submission artefact were all decided in earlier assessments, so this one reached a working pipeline much faster. The remaining effort went into the questions specific to this dataset instead of into process.

The design also held up under its own checks. All 731 daily units remain available for the primary question, the holdout is isolated from every selection decision, and four families compete across three exogenous feature sets. The hourly file validates every daily total and exposes both intraday peaks and panel imbalance.

### 6.2 Challenges

Understanding the data took longer than fitting the models. Two files describe the same system at different granularities, `casual` and `registered` sum to the target and cannot be predictors, and one humidity reading is physically impossible. Diagnosing that reading required cross-checking the hourly file, and the correction then had to preserve sample size and stay inside the pipeline folds.

The concept that took longest to internalise is the difference between interpolation and extrapolation. A tree fits both years comfortably when they are shuffled together, and the same tree cannot reach 2012 demand when trained on 2011 alone, because a terminal region can only average values it has already seen. That is a property of the model class rather than a tuning failure, and it explains why the simplest candidate transferred best.

### 6.3 What can be improved

The strongest limitations are evidential. More years, archived weather forecasts and repeated forward windows would test whether the temporal result reflects this transition or a permanent property. Station-level planning would additionally need identifiers, dock capacity, trip origins and destinations, transit connections and local demand, which is why the ITDP and NACTO guidance points beyond this dataset. Category-4 weather remains outside the supported domain.

Methodologically, trend-seasonality decomposition, differenced targets and forecast-aware inputs are the natural next comparisons.

The extension I would most like to build is a small service that turns the frozen primary model into something usable: send it a date, its season and a weather forecast, and receive an estimated daily volume with the supported-domain guard applied. Appendix C sketches that idea, including the parts this study shows it must not claim.
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

APPENDIX_C = md(r"""
## Appendix C - Proposed extension: a demand estimation service

This appendix sketches the engineering extension named in Section 6.3. It is a proposal, not a
deployed system, and the evidence in Section 5 constrains what it may offer.

### C.1 What it would do

A caller sends a date, its season and a weather forecast; the service returns an estimated daily
rental volume from the frozen primary model, together with the supported input domain.

```
POST /estimate
{ "date": "2013-04-18", "season": 2, "weathersit": 1,
  "temp": 0.58, "atemp": 0.55, "hum": 0.61, "windspeed": 0.18 }

-> { "estimated_daily_rentals": 5120,
     "expected_absolute_error": 434,
     "basis": "conditional estimate, observed 2011-2012 distribution",
     "supported_weathersit": [1, 2, 3] }
```

Returning the expected error alongside the point estimate matters more than the estimate itself.
A planner who receives 5,120 without 434 will read a precision the model does not have.

### C.2 Proposed layers

| Layer | Technology | Purpose |
|---|---|---|
| Model artefact | scikit-learn pipeline, joblib | The frozen Gradient Boosting configuration and its preprocessing, serialised together |
| Contract | JSON | Feature order, supported `weathersit` categories, holdout metrics, source notebook hash |
| API | FastAPI, Pydantic | Typed request validation and the domain guard |
| Interface | Streamlit | A form for planners who will not call an API |
| Monitoring | Scheduled job | Daily scoring of yesterday's estimate against realised demand |

The pattern follows my Sommelier API project from Assessments 1 and 2, where the same separation
between a framework-agnostic model core and thin serving surfaces is already implemented.

### C.3 What this study forbids it from claiming

The temporal check is the reason this appendix is short about forecasting.

- The service may answer **conditional** questions: given these conditions, what does the
  2011-2012 relationship imply? That is the question the primary experiment evaluated.
- It may **not** be presented as a next-day forecaster. Section 4.2 measured the frozen model
  at 23.5% worse than a rolling seven-day mean on 2012. A forecasting endpoint would either
  serve the rolling mean or wait for new forward evidence.
- Any request outside `weathersit` 1 to 3 must be rejected for human review rather than scored,
  because category 4 never appears in training.

### C.4 Geolocation and alerts

Two ideas worth recording, with their preconditions.

**Station-level geolocation.** Plotting expected demand onto a map through a mapping API is
straightforward as an interface, and unsupported as an inference. This dataset carries no station
identifier, coordinate, dock capacity or trip origin, so nothing in this notebook can attribute
system demand to a location. Delivering it honestly means acquiring station-level data first;
ITDP and NACTO describe the network, spacing and capacity variables that work would need
(ITDP, 2018; NACTO, 2016).

**Custom alerts.** Two alert types are supported by evidence already collected. A *domain alert*
fires when a request falls outside the supported weather categories. A *drift alert* fires when
the rolling error of the deployed estimate exceeds its holdout MAE over a defined window, which is
the mechanism that would have caught the temporal failure in production rather than in a notebook.
A demand-threshold alert for staffing would be useful but needs a stakeholder-defined threshold
that this project does not have.
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

Analysis was performed in Python with pandas, NumPy, scikit-learn, Matplotlib, Seaborn and SHAP.

I acknowledge that I have used the following AI tool(s) in the creation of this report:
- Anthropic Claude Opus 5
- OpenAI ChatGPT Codex 5.6

Both tools were used to assist with understanding ML concepts, challenging the experimental design, auditing empirical claims against executed outputs, structuring the technical pipeline, improving clarity of academic language, and supporting APA 7th referencing conventions.

Prompt examples:
1. "Explain why a random split over a two-year time series supports a conditional demand estimate but not a next-day forecast, and how to run both experiments so that neither contaminates the other."
2. "Show why a tree ensemble trained on 2011 cannot predict 2012 demand above its training maximum, and propose a way to measure that ceiling instead of asserting it."
3. "Build a causal seven-day rolling baseline for a day-ahead comparison using shift before rolling, and write the assertion that proves the window never includes the target day."

I confirm that the use of these tools has been in accordance with the Torrens University Australia Academic Integrity Policy and TUA, Think and MDS's Position Paper on the Use of AI. I confirm that the final output is authored by me and represents my own critical thinking, analysis, and synthesis of sources. I take full responsibility for the final content of this report.

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
           PERMUTATION, SHAP_CELL, DIAGNOSTICS, EVAL_READ, LESSONS, APPENDIX, REPRO,
           APPENDIX_C, CLOSING]
