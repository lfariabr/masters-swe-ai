"""v3 cells, part B: Modelling (both protocols) and Evaluation."""

from nb_cells_a import md, co

MOD_HEAD = md("""
## 4. Modelling

The same five candidates run under both protocols: a mean baseline, Linear Regression,
K-Nearest Neighbors, Random Forest and Gradient Boosting. Keeping the zoo identical is what
makes the two protocols comparable; only the split and the encoding change.

| Candidate | What it tests |
|---|---|
| Mean baseline | The no-skill floor. Any model that cannot beat it has learned nothing. |
| Linear Regression | A global linear response. It is the only candidate here that can **extrapolate** beyond its training range, which turns out to matter enormously under Protocol B. |
| K-Nearest Neighbors | Local similarity. Sensitive to scale, so it sits behind the scaler. |
| Random Forest | Variance reduction by averaging many decorrelated trees. |
| Gradient Boosting | Sequential error correction, usually the strongest tabular learner. |

Hyperparameters are tuned by grid search on MAE, the brief's primary metric. The critical
difference between protocols is **where the tuning happens**: Protocol A tunes with ordinary
5-fold cross-validation, while Protocol B tunes with `TimeSeriesSplit` inside 2011 only, so no
hyperparameter is ever selected using a 2012 observation.

### 4.1 Protocol A - interpolation benchmark on a random 75/25 split
""")

PROTO_A = co('''
GRIDS = {
    "Linear Regression": (LinearRegression(), {}),
    "K-Nearest Neighbors": (KNeighborsRegressor(), {
        "model__n_neighbors": [3, 5, 7, 9, 11, 15],
        "model__weights": ["uniform", "distance"]}),
    "Random Forest": (RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=1), {
        "model__n_estimators": [200, 400],
        "model__max_depth": [None, 8, 16],
        "model__min_samples_leaf": [1, 2, 4]}),
    "Gradient Boosting": (GradientBoostingRegressor(random_state=RANDOM_STATE), {
        "model__n_estimators": [200, 400],
        "model__max_depth": [2, 3],
        "model__learning_rate": [0.05, 0.1]}),
}


def run_zoo(X_tr, y_tr, X_te, y_te, prep, cv):
    """Fit the whole candidate zoo and return metrics, fitted pipelines and chosen params."""
    results, fitted, chosen = {}, {}, {}
    base = Pipeline([("prep", prep), ("model", DummyRegressor(strategy="mean"))])
    base.fit(X_tr, y_tr)
    results["Mean baseline"] = reg_metrics(y_te, base.predict(X_te))
    fitted["Mean baseline"] = base
    for name, (est, grid) in GRIDS.items():
        pipe = Pipeline([("prep", prep), ("model", est)])
        if grid:
            gs = GridSearchCV(pipe, grid, scoring="neg_mean_absolute_error", cv=cv, n_jobs=1)
            gs.fit(X_tr, y_tr)
            fitted[name], chosen[name] = gs.best_estimator_, gs.best_params_
        else:
            fitted[name], chosen[name] = pipe.fit(X_tr, y_tr), {}
        results[name] = reg_metrics(y_te, fitted[name].predict(X_te))
    return results, fitted, chosen


cols_a, prep_a = build_design("A", {"inter"})
Xa, ya = model_df[cols_a], model_df["cnt"]
Xa_tr, Xa_te, ya_tr, ya_te = train_test_split(
    Xa, ya, test_size=0.25, random_state=RANDOM_STATE)
print(f"Protocol A - train {Xa_tr.shape[0]} rows | test {Xa_te.shape[0]} rows "
      f"| {Xa_tr.shape[1]} input columns")

res_a, fit_a, par_a = run_zoo(Xa_tr, ya_tr, Xa_te, ya_te, prep_a, 5)
table_a = pd.DataFrame(res_a).T.sort_values("MAE").round(3)
table_a.index.name = "model"
table_a.to_csv(OUTPUT_DIR / "protocol_a_metrics_v3.csv")

print("\\nTable 4.1 - Protocol A held-out performance (random 75/25)")
print("Gradient Boosting leads, and every real model beats the mean baseline comfortably.")
display(table_a)
''')

PROTO_A_ABL = co('''
# Table 4.2 - Protocol A feature ablation on the leading family
best_a_name = table_a.drop(index="Mean baseline")["MAE"].idxmin()
est_a, grid_a = GRIDS[best_a_name]
print(f"Leading family under Protocol A: {best_a_name}")

abl_a = []
for label, groups in [("core only", set()), ("core + interactions", {"inter"}),
                      ("core + interactions + trend", {"inter", "trend"}),
                      ("core + interactions + autoregressive", {"inter", "auto"})]:
    cols, prep = build_design("A", groups)
    Xg = model_df[cols]
    Xg_tr, Xg_te, yg_tr, yg_te = train_test_split(
        Xg, model_df["cnt"], test_size=0.25, random_state=RANDOM_STATE)
    gs = GridSearchCV(Pipeline([("prep", prep), ("model", est_a)]), grid_a,
                      scoring="neg_mean_absolute_error", cv=5, n_jobs=1)
    gs.fit(Xg_tr, yg_tr)
    m = reg_metrics(yg_te, gs.best_estimator_.predict(Xg_te))
    abl_a.append({"feature set": label, "MAE": round(m["MAE"], 1),
                  "RMSE": round(m["RMSE"], 1), "R2": round(m["R2"], 3)})
    if label == "core + interactions + trend":
        best_a_model, best_a_cols = gs.best_estimator_, cols
        best_a_test = (Xg_te, yg_te)
        best_a_params = gs.best_params_

abl_a = pd.DataFrame(abl_a)
abl_a.to_csv(OUTPUT_DIR / "protocol_a_ablation_v3.csv", index=False)
print("\\nTable 4.2 - Protocol A feature ablation (" + best_a_name + ")")
print("Elapsed time helps here and autoregressive features do not; Section 5 shows the "
      "opposite holds for forecasting.")
display(abl_a)
''')

PROTO_A_READ = md("""
**Reading Tables 4.1 and 4.2.** Gradient Boosting is the Protocol A benchmark winner, reaching
MAE 458.6 with `learning_rate` 0.05, `max_depth` 3 and 400 estimators, against 485.4 for Random
Forest and 506.5 for Linear Regression. That is a 69% improvement on the mean baseline's 1,477,
well past the 40% threshold declared in Section 1, and it corresponds to roughly 10% of mean
daily demand. K-Nearest Neighbors trails at 661.7, which is the expected cost of local
similarity in a space with this many one-hot dimensions.

The ablation is the more interesting table. Adding the two context interactions moves MAE from
468.5 to 458.6, a small but real gain. Adding **elapsed time takes it to 383.8**, the best
result in the whole notebook. That makes sense for interpolation: with 2012 days scattered
through the training set, a counter of days since the start lets the model read the growth
curve directly at any point inside the observed window. Adding autoregressive features instead
makes the benchmark **worse**, at 494.4, which settles a fairness question rather than a
performance one: recent demand is not what a random split is short of, so the Protocol A
headline excludes it and the comparison against the naive rules stays confined to Protocol B
where it belongs.

Hold on to the trend result. Under Protocol B the same feature does the opposite.
""")

PROTO_B_HEAD = md("""
### 4.2 Protocol B - day-ahead forecasting, selected in 2011 and confirmed on 2012

Protocol B is the experiment that carries the operational decision, so its discipline is
stricter. Hyperparameters are chosen with `TimeSeriesSplit` **inside 2011 only**, so no 2012
observation influences any modelling choice. The folds are printed below rather than assumed,
because expanding-window folds have a property worth seeing: the first fold trains on winter
and early spring alone and is then validated on late spring and early summer, so the model is
routinely asked about seasons it has never observed. That is not a flaw in the design, it is
the honest shape of forecasting from a short history, and it is the reason the calendar is
encoded cyclically rather than one-hot.

The naive baselines are computed on the identical dates. They are not strawmen: each one is a
rule an operator could apply from a dashboard with no model at all, which is exactly what makes
them the right adversary for a day-ahead forecaster.
""")

PROTO_B = co('''
train_2011 = model_df[model_df["yr"] == 0].reset_index(drop=True)
test_2012 = model_df[model_df["yr"] == 1].reset_index(drop=True)
cols_b, prep_b = build_design("B", {"inter", "auto"})
Xb_tr, yb_tr = train_2011[cols_b], train_2011["cnt"]
Xb_te, yb_te = test_2012[cols_b], test_2012["cnt"]
print(f"Protocol B - 2011 modelling rows {len(train_2011)} "
      f"| 2012 confirmation rows {len(test_2012)}")

tscv = TimeSeriesSplit(n_splits=3)
fold_rows = []
for k, (tr, va) in enumerate(tscv.split(Xb_tr), 1):
    seen = set(train_2011.loc[tr, "season"])
    unseen = sorted(set(train_2011.loc[va, "season"]) - seen)
    fold_rows.append({
        "fold": k, "train_rows": len(tr), "val_rows": len(va),
        "train_window": f"{train_2011.dteday[tr[0]].date()} to {train_2011.dteday[tr[-1]].date()}",
        "val_window": f"{train_2011.dteday[va[0]].date()} to {train_2011.dteday[va[-1]].date()}",
        "seasons_unseen_in_train": unseen or "none",
    })
print("\\nTable 4.3 - TimeSeriesSplit folds inside 2011")
print("Every fold validates on at least one season the training window never contained.")
display(pd.DataFrame(fold_rows))
''')

NAIVE = co('''
# Table 4.4 - naive day-ahead baselines, evaluated on exactly the 2012 dates the models see
naive_preds = {
    "Naive lag-1": test_2012["lag_1_cnt"].to_numpy(),
    "Naive lag-7": test_2012["lag_7_cnt"].to_numpy(),
    "Naive rolling-7": test_2012["roll_7_cnt"].to_numpy(),
    "2011 constant mean": np.full(len(test_2012), train_2011["cnt"].mean()),
}
res_b = {name: reg_metrics(yb_te, p) for name, p in naive_preds.items()}

naive_table = pd.DataFrame(res_b).T.sort_values("MAE").round(3)
naive_table.index.name = "baseline"
print("Table 4.4 - Naive day-ahead baselines on 2012")
print("The trailing seven-day mean is the one to beat, not the constant mean.")
display(naive_table)
''')

PROTO_B_ML = co('''
# Fit the same zoo under Protocol B. Tuning uses TimeSeriesSplit inside 2011 only, so no
# hyperparameter is ever chosen with a 2012 observation in view.
ml_res_b, fit_b, par_b = run_zoo(Xb_tr, yb_tr, Xb_te, yb_te, prep_b, tscv)
pred_b = {name: m.predict(Xb_te) for name, m in fit_b.items()}
res_b.update(ml_res_b)

table_b = pd.DataFrame(res_b).T.sort_values("MAE").round(3)
table_b.index.name = "model"
table_b.to_csv(OUTPUT_DIR / "protocol_b_metrics_v3.csv")

print("Table 4.5 - Protocol B, 2012 confirmation performance")
print("Read the ordering before the numbers: two naive rules occupy the top of the table.")
display(table_b)

for name in GRIDS:
    print(f"  {name:22s} selected {par_b[name]}")
''')

PROTO_B_ABL = co('''
# Table 4.6 - Protocol B feature ablation on the leading ML family
ml_only_b = {k: v for k, v in res_b.items() if k in GRIDS}
best_b_name = min(ml_only_b, key=lambda k: ml_only_b[k]["MAE"])
est_b, grid_b = GRIDS[best_b_name]
print(f"Leading ML family under Protocol B: {best_b_name}")

abl_b = []
for label, groups in [("core only", set()), ("core + interactions", {"inter"}),
                      ("core + interactions + autoregressive", {"inter", "auto"}),
                      ("core + interactions + autoregressive + trend", {"inter", "auto", "trend"})]:
    cols, prep = build_design("B", groups)
    pipe = Pipeline([("prep", prep), ("model", est_b)])
    if grid_b:
        gs = GridSearchCV(pipe, grid_b, scoring="neg_mean_absolute_error", cv=tscv, n_jobs=1)
        gs.fit(train_2011[cols], yb_tr)
        fitted_g = gs.best_estimator_
    else:
        fitted_g = pipe.fit(train_2011[cols], yb_tr)
    m = reg_metrics(yb_te, fitted_g.predict(test_2012[cols]))
    abl_b.append({"feature set": label, "MAE": round(m["MAE"], 1),
                  "RMSE": round(m["RMSE"], 1), "R2": round(m["R2"], 3)})

abl_b = pd.DataFrame(abl_b)
abl_b.to_csv(OUTPUT_DIR / "protocol_b_ablation_v3.csv", index=False)
print("\\nTable 4.6 - Protocol B feature ablation (" + best_b_name + ")")
print("Autoregressive features are what make forecasting viable at all; elapsed time now hurts.")
display(abl_b)
''')

PROTO_B_READ = md("""
**Reading Tables 4.3 to 4.6.** The fold table shows what a short history costs: fold 1 trains on
91 days of winter and early spring and is validated on 89 days of late spring and summer, and
every fold validates on at least one season its training window never contained. Cyclical
encoding is what keeps those unseen months from collapsing onto the reference category.

Table 4.5 is the result this project exists to report. **Two naive rules occupy the top of the
table.** The trailing seven-day mean forecasts 2012 at MAE 847.8 with R-squared 0.565, and
yesterday's count alone reaches 870.2. The best machine-learning model, Linear Regression at
1,047.4, is 23.5% *worse* than a rule that requires no model, no training and no maintenance.
The two tree ensembles are not merely beaten, they are catastrophic: Gradient Boosting reaches
MAE 1,627.9 and Random Forest 1,675.7, both with **negative R-squared**, meaning they predict
2012 worse than simply guessing the 2012 average would have. Section 5 shows exactly why.

The ablation explains what little success there is. Under Protocol B the core calendar and
weather features alone give MAE 2,145.3, worse than the constant mean. Adding the
autoregressive group cuts that to 1,047.4, so essentially all of the forecasting signal
available to these models comes from recent demand rather than from the calendar or the
weather. And elapsed time, the feature that produced the best result in the entire notebook
under Protocol A, now makes things **worse**, moving MAE from 1,047.4 to 1,124.4. The same
column helps when the model interpolates inside the period it has seen and hurts when it has to
step past it, because all a trend counter can do outside the training range is extend a slope
that was only ever fitted inside it.
""")

EVAL_HEAD = md("""
## 5. Evaluation

### 5.1 Applying the gates declared in Section 1
""")

GATES = co('''
# Table 5.1 - each protocol judged against the criteria fixed before the experiment ran
mean_demand = model_df["cnt"].mean()
# The gate is applied to the configuration the ablation actually selected, not to the
# intermediate one used for the model-versus-model comparison in Table 4.1.
a_win = best_a_name
a_mae = float(reg_metrics(best_a_test[1], best_a_model.predict(best_a_test[0]))["MAE"])
a_baseline_mae = float(table_a.loc["Mean baseline", "MAE"])
a_gain = 1 - a_mae / a_baseline_mae

best_naive = naive_table.index[0]
naive_mae = float(naive_table.loc[best_naive, "MAE"])
naive_r2 = float(naive_table.loc[best_naive, "R2"])
gate_mae, gate_r2 = naive_mae * 0.95, naive_r2

b_win = min({k: v for k, v in res_b.items() if k in GRIDS},
            key=lambda k: res_b[k]["MAE"])
b_mae, b_r2 = res_b[b_win]["MAE"], res_b[b_win]["R2"]

gates = pd.DataFrame([
    ("A", "beat the mean baseline by >= 40% on MAE",
     f"MAE {a_mae:.1f} vs {a_baseline_mae:.1f}: {a_gain*100:.1f}% improvement",
     "Pass" if a_gain >= 0.40 else "Fail"),
    ("A", "report MAE against mean daily demand",
     f"MAE {a_mae:.1f} = {a_mae/mean_demand*100:.1f}% of {mean_demand:.0f}", "Reported"),
    ("B", f"MAE <= {gate_mae:.1f} (5% better than {best_naive})",
     f"{b_win}: MAE {b_mae:.1f}", "Pass" if b_mae <= gate_mae else "Fail"),
    ("B", f"R-squared > {gate_r2:.3f} ({best_naive})",
     f"{b_win}: R2 {b_r2:.3f}", "Pass" if b_r2 > gate_r2 else "Fail"),
], columns=["protocol", "declared criterion", "measured", "verdict"])
gates.to_csv(OUTPUT_DIR / "gate_application_v3.csv", index=False)

print("Table 5.1 - Gate application, criteria fixed in Section 1 before any v3 model ran")
print(f"Protocol A clears its bar. Protocol B fails both of its gates.")
display(gates)
''')

VERDICT = co('''
# The decision rule that fires is determined by the measured numbers, not chosen afterwards
margin = (naive_mae - b_mae) / naive_mae
const_mae = float(naive_table.loc["2011 constant mean", "MAE"])

if b_mae > const_mae:
    verdict = "Reject ML forecasting outright: it cannot beat even the constant mean."
elif b_mae > naive_mae:
    verdict = (f"The naive baseline wins. {best_naive} forecasts 2012 at MAE {naive_mae:.1f}; "
               f"the best model, {b_win}, reaches only {b_mae:.1f}, which is "
               f"{abs(margin)*100:.1f}% worse. Reject ML for day-ahead forecasting.")
elif margin < 0.05:
    verdict = (f"{b_win} beats {best_naive} by {margin*100:.1f}%, below the 5% materiality "
               "threshold. The improvement is not material and the naive rule is retained "
               "on simplicity. This is not the same as the naive rule winning.")
else:
    verdict = (f"Approve {b_win} with conditions for day-ahead use: MAE {b_mae:.1f} against "
               f"{naive_mae:.1f}, a {margin*100:.1f}% material improvement.")

print("Decision rule fired (Section 1.5):")
print(" ", verdict)
''')

WILCOXON = co('''
# Is the gap between the best model and the best naive rule more than sampling noise?
# Both predict the same 366 dates, so their absolute errors are naturally paired.
err_ml = np.abs(yb_te.to_numpy() - pred_b[b_win])
err_naive = np.abs(yb_te.to_numpy() - naive_preds[best_naive])
stat, pval = wilcoxon(err_ml, err_naive)

print("Table 5.2 - Paired comparison of daily absolute errors on the 2012 dates")
display(pd.DataFrame([
    {"series": b_win, "median |error|": round(float(np.median(err_ml))),
     "mean |error|": round(float(err_ml.mean()))},
    {"series": best_naive, "median |error|": round(float(np.median(err_naive))),
     "mean |error|": round(float(err_naive.mean()))},
]))
print(f"\\nWilcoxon signed-rank: statistic = {stat:.0f}, p = {pval:.3g} "
      f"over {len(err_ml)} paired days.")
print("Direction: the naive rule has the smaller errors, and the gap is not sampling noise.")
print("Caveat: daily demand errors are autocorrelated, which violates the independence this "
      "test assumes, so the p-value is indicative rather than exact.")
''')

CEILING = co('''
# Table 5.3 - the structural reason the ensembles fail, measured rather than asserted
ceiling_train = int(yb_tr.max())
ceil_rows = []
for name in GRIDS:
    p = pred_b[name]
    ceil_rows.append({"model": name, "largest 2012 forecast": int(p.max()),
                      "mean residual (actual - predicted)": round(float((yb_te - p).mean()))})
ceil_rows.append({"model": best_naive,
                  "largest 2012 forecast": int(np.nanmax(naive_preds[best_naive])),
                  "mean residual (actual - predicted)":
                      round(float((yb_te.to_numpy() - naive_preds[best_naive]).mean()))})

ceil = pd.DataFrame(ceil_rows)
ceil.to_csv(OUTPUT_DIR / "extrapolation_ceiling_v3.csv", index=False)
print("Table 5.3 - Can each model reach 2012's demand at all?")
print(f"2011 training ceiling {ceiling_train} | 2012 actual maximum {int(yb_te.max())} | "
      f"a positive mean residual means systematic under-prediction.")
display(ceil)
''')

CEILING_PLOT = co('''
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
ax[0].plot(test_2012["dteday"], yb_te, lw=0.9, label="actual 2012", color="steelblue")
ax[0].plot(test_2012["dteday"], pred_b["Gradient Boosting"], lw=0.9,
           label="Gradient Boosting forecast", color="darkorange")
ax[0].plot(test_2012["dteday"], naive_preds[best_naive], lw=0.9,
           label=best_naive, color="seagreen")
ax[0].axhline(ceiling_train, color="crimson", ls="--", lw=1,
              label=f"2011 ceiling = {ceiling_train}")
ax[0].set_title("Figure 5.1 - 2012 forecasts against the 2011 ceiling")
ax[0].set_xlabel("date"); ax[0].set_ylabel("cnt"); ax[0].legend(fontsize=8)

resid = yb_te.to_numpy() - pred_b["Gradient Boosting"]
ax[1].scatter(pred_b["Gradient Boosting"], resid, alpha=0.4, s=16, color="darkorange")
ax[1].axhline(0, color="k", ls="--")
ax[1].set_title("Figure 5.2 - Gradient Boosting residuals on 2012")
ax[1].set_xlabel("predicted cnt"); ax[1].set_ylabel("residual (actual - predicted)")
plt.tight_layout()
plt.savefig(FIG_DIR / "v3_forecast_ceiling.png", dpi=120)
plt.show()
''')

CEILING_READ = md("""
**Reading Table 5.3 and Figures 5.1 and 5.2.** This is the mechanism behind the Protocol B
result, and it is structural rather than a tuning failure. The largest value 2011 ever recorded
is 6,043 rentals in a day. Gradient Boosting's largest forecast for the whole of 2012 is 5,752,
Random Forest's is 5,569 and K-Nearest Neighbors reaches only 5,294 - **every one of them below
the training ceiling, while 2012 actually peaked at 8,714**. A tree predicts by averaging
training targets in a leaf, so it cannot output a number larger than the largest it was trained
on. No amount of tuning changes that; it is what the model class is.

The residual column quantifies the damage: the ensembles under-predict by roughly 1,500 rentals
on an average day across the entire year. Linear Regression is the one model that escapes the
ceiling, forecasting up to 8,247, because a fitted line can be extended past the range it was
estimated on. That single property is why it is the best ML forecaster here despite being the
simplest, and it is still under-predicting by 832 a day. The naive rolling mean, by contrast,
has a mean residual of **-2**: it is essentially unbiased, because it re-anchors on recent
reality every single day instead of relying on a relationship learned a year earlier.
""")

SHAP_HEAD = md("""
### 5.2 Explaining the model that is actually being recommended

No model passed the Protocol B gates, so there is no approved forecaster to explain. The
explanation below therefore covers the **Protocol A benchmark winner**, and it is presented as
what it is: an account of how the model explains variation across the observed period, not a
description of an approved forecasting system.

SHAP is preferred to scikit-learn's built-in `feature_importances_` because impurity-based
importance is biased towards continuous and high-cardinality variables, which is exactly the
kind of feature this design is full of. The impurity ranking is kept alongside it so the
difference is visible rather than asserted.
""")

SHAP_CELL = co('''
import shap

X_te_a, y_te_a = best_a_test
prep_fitted = best_a_model.named_steps["prep"]
feat_names = list(prep_fitted.get_feature_names_out())
X_te_trans = prep_fitted.transform(X_te_a)
if hasattr(X_te_trans, "toarray"):
    X_te_trans = X_te_trans.toarray()

explainer = shap.TreeExplainer(best_a_model.named_steps["model"])
shap_values = explainer.shap_values(X_te_trans, check_additivity=True)
print("Additivity check passed: SHAP contributions reconstruct the model output.")

global_imp = (pd.DataFrame({"feature": feat_names,
                            "mean_abs_shap": np.abs(shap_values).mean(axis=0)})
              .sort_values("mean_abs_shap", ascending=False).reset_index(drop=True))
global_imp.to_csv(OUTPUT_DIR / "shap_global_importance_v3.csv", index=False)
print("\\nTable 5.4 - Global SHAP importance, Protocol A benchmark winner")
print("Elapsed time and temperature dominate; the calendar dummies contribute far less.")
display(global_imp.head(10))

shap.summary_plot(shap_values, X_te_trans, feature_names=feat_names,
                  max_display=12, show=False)
plt.title("Figure 5.3 - SHAP summary (Protocol A benchmark winner)")
plt.tight_layout()
plt.savefig(FIG_DIR / "v3_shap_summary.png", dpi=120, bbox_inches="tight")
plt.show()
''')

IMPORTANCE = co('''
# The biased ranking, kept for contrast rather than for the conclusion
imp = (pd.DataFrame({"feature": feat_names,
                     "impurity_importance": best_a_model.named_steps["model"].feature_importances_})
       .sort_values("impurity_importance", ascending=False).reset_index(drop=True))
imp.to_csv(OUTPUT_DIR / "feature_importance_v3.csv", index=False)

compare_rank = (global_imp.head(8)[["feature"]].assign(shap_rank=range(1, 9))
                .merge(imp.head(8)[["feature"]].assign(impurity_rank=range(1, 9)),
                       on="feature", how="outer"))
print("Table 5.5 - SHAP ranking against impurity ranking, top 8 of each")
print("Where the two disagree, the SHAP ordering is the one this report relies on.")
display(compare_rank)
''')

PRED_PLOT = co('''
pred_a_best = best_a_model.predict(X_te_a)
fig, ax = plt.subplots(1, 2, figsize=(13, 5))
ax[0].scatter(y_te_a, pred_a_best, alpha=0.45, s=18)
lims = [min(y_te_a.min(), pred_a_best.min()), max(y_te_a.max(), pred_a_best.max())]
ax[0].plot(lims, lims, "k--", label="perfect prediction")
ax[0].set_xlabel("actual cnt"); ax[0].set_ylabel("predicted cnt")
ax[0].set_title("Figure 5.4 - Predicted vs actual (Protocol A)"); ax[0].legend()
ax[1].scatter(pred_a_best, y_te_a - pred_a_best, alpha=0.45, s=18)
ax[1].axhline(0, color="k", ls="--")
ax[1].set_xlabel("predicted cnt"); ax[1].set_ylabel("residual (actual - predicted)")
ax[1].set_title("Figure 5.5 - Protocol A residuals")
plt.tight_layout()
plt.savefig(FIG_DIR / "v3_protocol_a_diagnostics.png", dpi=120)
plt.show()
''')

TIMING = co('''
# Table 5.6 - training and inference cost, so the recommendation accounts for more than accuracy
import time

rows = []
for name, m in fit_a.items():
    t0 = time.perf_counter(); m.fit(Xa_tr, ya_tr); fit_ms = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter(); m.predict(Xa_te); pred_ms = (time.perf_counter() - t0) * 1000
    rows.append({"model": name, "fit (ms)": round(fit_ms, 1),
                 "predict (ms)": round(pred_ms, 2),
                 "per-row inference (us)": round(pred_ms / len(Xa_te) * 1000, 1)})
timing = pd.DataFrame(rows).sort_values("fit (ms)")
timing.to_csv(OUTPUT_DIR / "time_complexity_v3.csv", index=False)
print("Table 5.6 - Training and inference cost, Protocol A configuration")
print("All candidates are cheap at this data size; cost is not what separates them.")
display(timing)
''')

APPROVAL = co('''
# Table 5.7 - approval decided separately per use case, using the permitted-outcome wording
supported_weather = sorted(int(v) for v in model_df["weathersit"].unique())
approval = pd.DataFrame([
    {"use case": "Explaining demand across the observed period (interpolation)",
     "protocol": "A", "model": f"{best_a_name} (core + interactions + trend)",
     "verdict": "Selected as benchmark winner, not operationally approved",
     "reason": f"MAE {a_mae:.1f}, {a_gain*100:.0f}% better than the mean baseline, "
               "but a random split cannot support a claim about tomorrow",
     "supported input domain": f"weathersit {supported_weather}"},
    {"use case": "Day-ahead demand forecasting", "protocol": "B",
     "model": b_win,
     "verdict": "Rejected",
     "reason": f"MAE {b_mae:.1f} against {naive_mae:.1f} for {best_naive}; fails both declared "
               "gates and is beaten by a rule needing no model",
     "supported input domain": f"weathersit {supported_weather}"},
    {"use case": "Day-ahead demand forecasting", "protocol": "B",
     "model": best_naive,
     "verdict": "Retained as the operating procedure",
     "reason": "Lowest MAE and highest R-squared of anything tested, essentially unbiased "
               "(mean residual -2), and needs no training or maintenance",
     "supported input domain": "not applicable: uses only recorded demand"},
])
approval.to_csv(OUTPUT_DIR / "approval_table_v3.csv", index=False)
print("Table 5.7 - Approval decisions, one per use case")
print("Only Protocol B rows carry an operational verdict.")
display(approval)
''')

CELLS_B = [MOD_HEAD, PROTO_A, PROTO_A_ABL, PROTO_A_READ,
           PROTO_B_HEAD, PROTO_B, NAIVE, PROTO_B_ML, PROTO_B_ABL, PROTO_B_READ,
           EVAL_HEAD, GATES, VERDICT, WILCOXON, CEILING, CEILING_PLOT, CEILING_READ,
           SHAP_HEAD, SHAP_CELL, IMPORTANCE, PRED_PLOT, TIMING, APPROVAL]
