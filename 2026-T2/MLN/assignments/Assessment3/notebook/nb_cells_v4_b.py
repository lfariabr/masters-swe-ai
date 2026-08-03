"""v4 cells, part B: training-only selection and frozen holdout evaluations."""

from nb_cells_v4_a import md, co

MODELLING_HEAD = md(r"""
## 4. Modelling

Four regression families are compared with lightweight grids in scikit-learn (Pedregosa et al., 2011). Linear Regression tests a global additive relationship; K-Nearest Neighbors tests local similarity; Random Forest averages decorrelated trees; Gradient Boosting sequentially corrects residuals (Friedman, 2001). Scaling and fold-fitted median imputation live inside every pipeline.

### 4.1 Primary model comparison: random 75/25 holdout

The split is created once with `random_state=42`. Only the 75% training partition participates in family, feature-set and hyperparameter selection. Each of the 12 family/feature-set combinations uses shuffled five-fold `KFold` and MAE scoring. The 25% holdout is accessed only after the global configuration and one configuration per family have been frozen.
""")

PRIMARY_SELECT = co(r'''
all_indices = primary_df.index.to_numpy()
primary_train_idx, primary_holdout_idx = train_test_split(
    all_indices, test_size=0.25, random_state=RANDOM_STATE
)
assert set(primary_train_idx).isdisjoint(primary_holdout_idx)
assert len(primary_train_idx) == 548 and len(primary_holdout_idx) == 183

primary_train = primary_df.loc[primary_train_idx].copy()
primary_holdout = primary_df.loc[primary_holdout_idx].copy()
primary_cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
primary_rows, primary_estimators = [], {}

for feature_name, columns in PRIMARY_FEATURE_SETS.items():
    for model_name, (estimator, grid) in GRIDS.items():
        search = GridSearchCV(
            pipeline_for(clone(estimator), columns, temporal=False), grid,
            scoring="neg_mean_absolute_error", cv=primary_cv, n_jobs=1, refit=True
        )
        search.fit(primary_train[columns], primary_train.cnt)
        rmse_cv = cross_validate(
            search.best_estimator_, primary_train[columns], primary_train.cnt,
            cv=primary_cv, scoring="neg_root_mean_squared_error", n_jobs=1
        )["test_score"]
        row = {
            "model": model_name, "feature_set": feature_name,
            "cv_mean_MAE": -search.best_score_,
            "cv_std_MAE": search.cv_results_["std_test_score"][search.best_index_],
            "cv_mean_RMSE": -rmse_cv.mean(), "cv_std_RMSE": rmse_cv.std(),
            "best_params": compact_params(search.best_params_),
        }
        primary_rows.append(row)
        primary_estimators[(model_name, feature_name)] = search.best_estimator_

primary_cv_table = (pd.DataFrame(primary_rows)
                    .sort_values(["cv_mean_MAE", "cv_mean_RMSE"])
                    .reset_index(drop=True))
primary_cv_table.to_csv(OUTPUT_DIR / "primary_cv_selection_v4.csv", index=False)

primary_choice = choose_configuration(primary_rows)
primary_family_choices = {
    family: choose_configuration([r for r in primary_rows if r["model"] == family])
    for family in GRIDS
}
primary_winner_name = primary_choice["model"]
primary_winner_features = primary_choice["feature_set"]
primary_winner_columns = PRIMARY_FEATURE_SETS[primary_winner_features]
primary_winner = primary_estimators[(primary_winner_name, primary_winner_features)]

# Leakage audit: choices contain CV statistics from training indices only; the holdout has not
# been passed to fit, GridSearchCV, cross_validate or choose_configuration.
selection_indices = set(primary_train_idx)
assert selection_indices.isdisjoint(set(primary_holdout_idx))
assert len(primary_df) == 731
print("Table 4.1 - Primary CV selection (training partition only)")
display(primary_cv_table.round({"cv_mean_MAE": 1, "cv_std_MAE": 1,
                                "cv_mean_RMSE": 1, "cv_std_RMSE": 1}))
print("Frozen primary configuration:", primary_winner_name, "|", primary_winner_features,
      "|", primary_choice["best_params"])
''')

PRIMARY_HOLDOUT = co(r'''
# First use of the fixed 25% holdout: score one training-selected configuration per family.
primary_holdout_rows = []
mean_model = DummyRegressor(strategy="mean").fit(
    np.zeros((len(primary_train), 1)), primary_train.cnt
)
baseline_pred = mean_model.predict(np.zeros((len(primary_holdout), 1)))
primary_holdout_rows.append({"model": "Mean baseline", "feature_set": "constant training mean",
                             "best_params": "default", **metrics(primary_holdout.cnt, baseline_pred)})

primary_family_predictions = {}
for family, choice in primary_family_choices.items():
    feature_name = choice["feature_set"]
    columns = PRIMARY_FEATURE_SETS[feature_name]
    fitted = primary_estimators[(family, feature_name)]
    pred = fitted.predict(primary_holdout[columns])
    primary_family_predictions[family] = pred
    primary_holdout_rows.append({"model": family, "feature_set": feature_name,
                                 "best_params": choice["best_params"],
                                 **metrics(primary_holdout.cnt, pred)})

primary_holdout_table = (pd.DataFrame(primary_holdout_rows)
                         .sort_values("MAE").reset_index(drop=True))
primary_holdout_table.to_csv(OUTPUT_DIR / "primary_holdout_metrics_v4.csv", index=False)
primary_metrics = primary_holdout_table.loc[
    primary_holdout_table.model.eq(primary_winner_name)
].iloc[0]
primary_baseline = primary_holdout_table.loc[
    primary_holdout_table.model.eq("Mean baseline")
].iloc[0]
primary_improvement = 1 - primary_metrics.MAE / primary_baseline.MAE
primary_mae_pct = primary_metrics.MAE / primary_holdout.cnt.mean()
primary_summary = pd.DataFrame([{
    "selected_model": primary_winner_name,
    "feature_set": primary_winner_features,
    "best_params": primary_choice["best_params"],
    "holdout_MAE": primary_metrics.MAE,
    "holdout_RMSE": primary_metrics.RMSE,
    "holdout_R2": primary_metrics.R2,
    "mean_baseline_MAE": primary_baseline.MAE,
    "baseline_improvement_pct": 100 * primary_improvement,
    "MAE_pct_of_holdout_mean_demand": 100 * primary_mae_pct,
}])
primary_summary.to_csv(OUTPUT_DIR / "primary_summary_v4.csv", index=False)
print("Table 4.2 - Frozen family configurations on the primary holdout")
display(primary_holdout_table.round({"MAE": 1, "MSE": 1, "RMSE": 1, "R2": 3}))
print("Table 4.3 - Final selected-model summary")
display(primary_summary.round(3))
''')

HUM_SENSITIVITY = co(r'''
# Sensitivity of the frozen primary winner to retaining the raw hum=0 record.
raw_primary = primary_df.copy()
raw_primary.loc[raw_primary.dteday.eq(zero_hum_date), "hum"] = 0.0
raw_primary["atemp_hum"] = raw_primary.atemp * raw_primary.hum
sens_model = clone(primary_winner).fit(
    raw_primary.loc[primary_train_idx, primary_winner_columns],
    raw_primary.loc[primary_train_idx, "cnt"]
)
sens_pred = sens_model.predict(raw_primary.loc[primary_holdout_idx, primary_winner_columns])
corrected_pred = primary_winner.predict(primary_holdout[primary_winner_columns])
humidity_sensitivity = pd.DataFrame([
    {"treatment": "hum=0 marked missing; fold-fitted median imputation",
     **metrics(primary_holdout.cnt, corrected_pred)},
    {"treatment": "raw hum=0 retained", **metrics(primary_holdout.cnt, sens_pred)},
])
humidity_sensitivity.to_csv(OUTPUT_DIR / "humidity_sensitivity_v4.csv", index=False)
print("Table 4.4 - Humidity correction sensitivity on the frozen primary model")
display(humidity_sensitivity.round({"MAE": 2, "MSE": 1, "RMSE": 2, "R2": 4}))
''')

PRIMARY_READ = md(r"""
**Primary result.** Gradient Boosting with interactions and elapsed-time trend was frozen at CV MAE 477.0 (SD 34.1) and RMSE 657.6. Random Forest entered the 5% shortlist at MAE 498.0 but had higher RMSE (723.5). The selected grid point used learning rate 0.1, depth 2 and 400 estimators.

On the untouched 183-day holdout it reached MAE 433.9, RMSE 630.6 and R-squared 0.897. MAE was 73.9% below the baseline's 1,663.0 and equalled **10.1% of mean holdout demand**, meeting the 40% criterion. Random Forest reached 446.6, KNN 501.0 and Linear Regression 529.9; the winner remained frozen.

Marking zero humidity missing produced MAE 433.9 versus 430.9 when retained. The sub-1% difference leaves the conclusion unchanged; fold-fitted imputation preserves the physically plausible treatment.
""")

TEMPORAL_HEAD = md(r"""
### 4.2 Secondary temporal robustness check

Selection now uses `TimeSeriesSplit(n_splits=3)` inside 2011. The temporal design excludes `yr`, which is constant in the training year. It compares core cyclical calendar/weather inputs, interactions, causal recent-demand inputs and an optional elapsed-time trend. One configuration per family and the global temporal configuration are frozen before any 2012 score is produced.
""")

TEMPORAL_SELECT = co(r'''
temporal_train = temporal_df[temporal_df.yr.eq(0)].copy().reset_index(drop=True)
temporal_test = temporal_df[temporal_df.yr.eq(1)].copy().reset_index(drop=True)
assert temporal_train.dteday.max() < pd.Timestamp("2012-01-01")
assert temporal_test.dteday.min() >= pd.Timestamp("2012-01-01")
assert all("yr" not in columns for columns in TEMPORAL_FEATURE_SETS.values())

temporal_cv = TimeSeriesSplit(n_splits=3)
fold_table = []
for fold, (tr, va) in enumerate(temporal_cv.split(temporal_train), 1):
    fold_table.append({
        "fold": fold, "train_rows": len(tr), "validation_rows": len(va),
        "train_window": f"{temporal_train.dteday.iloc[tr[0]].date()} to {temporal_train.dteday.iloc[tr[-1]].date()}",
        "validation_window": f"{temporal_train.dteday.iloc[va[0]].date()} to {temporal_train.dteday.iloc[va[-1]].date()}",
    })
print("Table 4.5 - TimeSeriesSplit folds within 2011")
display(pd.DataFrame(fold_table))

temporal_rows, temporal_estimators = [], {}
for feature_name, columns in TEMPORAL_FEATURE_SETS.items():
    for model_name, (estimator, grid) in GRIDS.items():
        search = GridSearchCV(
            pipeline_for(clone(estimator), columns, temporal=True), grid,
            scoring="neg_mean_absolute_error", cv=temporal_cv, n_jobs=1, refit=True
        )
        search.fit(temporal_train[columns], temporal_train.cnt)
        rmse_cv = cross_validate(
            search.best_estimator_, temporal_train[columns], temporal_train.cnt,
            cv=temporal_cv, scoring="neg_root_mean_squared_error", n_jobs=1
        )["test_score"]
        row = {"model": model_name, "feature_set": feature_name,
               "cv_mean_MAE": -search.best_score_,
               "cv_std_MAE": search.cv_results_["std_test_score"][search.best_index_],
               "cv_mean_RMSE": -rmse_cv.mean(), "cv_std_RMSE": rmse_cv.std(),
               "best_params": compact_params(search.best_params_)}
        temporal_rows.append(row)
        temporal_estimators[(model_name, feature_name)] = search.best_estimator_

temporal_cv_table = (pd.DataFrame(temporal_rows)
                     .sort_values(["cv_mean_MAE", "cv_mean_RMSE"]).reset_index(drop=True))
temporal_cv_table.to_csv(OUTPUT_DIR / "temporal_cv_selection_v4.csv", index=False)
temporal_choice = choose_configuration(temporal_rows)
temporal_family_choices = {
    family: choose_configuration([r for r in temporal_rows if r["model"] == family])
    for family in GRIDS
}
temporal_winner_name = temporal_choice["model"]
temporal_winner_features = temporal_choice["feature_set"]
temporal_winner = temporal_estimators[(temporal_winner_name, temporal_winner_features)]

# Selection records and fitted estimators contain 2011 only. 2012 has not been scored yet.
assert temporal_train.yr.eq(0).all()
assert not temporal_train.dteday.isin(temporal_test.dteday).any()
print("Table 4.6 - Temporal CV selection (2011 only)")
display(temporal_cv_table.round({"cv_mean_MAE": 1, "cv_std_MAE": 1,
                                 "cv_mean_RMSE": 1, "cv_std_RMSE": 1}))
print("Frozen temporal configuration:", temporal_winner_name, "|", temporal_winner_features,
      "|", temporal_choice["best_params"])
''')

TEMPORAL_SCORE = co(r'''
# First 2012 scoring: frozen family candidates and causal baselines use identical dates.
temporal_rows_2012, temporal_predictions = [], {}
for family, choice in temporal_family_choices.items():
    feature_name = choice["feature_set"]
    columns = TEMPORAL_FEATURE_SETS[feature_name]
    fitted = temporal_estimators[(family, feature_name)]
    pred = fitted.predict(temporal_test[columns])
    temporal_predictions[family] = pred
    temporal_rows_2012.append({"model": family, "feature_set": feature_name,
                               "best_params": choice["best_params"],
                               **metrics(temporal_test.cnt, pred)})

temporal_baseline_predictions = {
    "Naive lag-1": temporal_test.lag_1_cnt.to_numpy(),
    "Naive lag-7": temporal_test.lag_7_cnt.to_numpy(),
    "Naive rolling-7": temporal_test.roll_7_cnt.to_numpy(),
    "2011 constant mean": np.full(len(temporal_test), temporal_train.cnt.mean()),
}
for name, pred in temporal_baseline_predictions.items():
    temporal_predictions[name] = pred
    temporal_rows_2012.append({"model": name, "feature_set": "causal baseline",
                               "best_params": "default", **metrics(temporal_test.cnt, pred)})

temporal_holdout_table = (pd.DataFrame(temporal_rows_2012)
                          .sort_values("MAE").reset_index(drop=True))
temporal_holdout_table.to_csv(OUTPUT_DIR / "temporal_holdout_metrics_v4.csv", index=False)
temporal_selected_metrics = temporal_holdout_table.loc[
    temporal_holdout_table.model.eq(temporal_winner_name)
].iloc[0]
rolling_metrics = temporal_holdout_table.loc[
    temporal_holdout_table.model.eq("Naive rolling-7")
].iloc[0]
temporal_advantage = 1 - temporal_selected_metrics.MAE / rolling_metrics.MAE
print("Table 4.7 - Frozen temporal candidates and baselines on 2012")
display(temporal_holdout_table.round({"MAE": 1, "MSE": 1, "RMSE": 1, "R2": 3}))
''')

TEMPORAL_READ = md(r"""
**Temporal result.** Linear Regression with interactions and causal autoregressive inputs was frozen from 2011 at CV MAE 602.5 and CV RMSE 763.2. Adding elapsed-time trend raised CV MAE to 665.8, so the trend was excluded before 2012 evaluation. This contrast with the primary result shows that elapsed time helps interpolate within a mixed-year domain but does not establish a transferable growth law.

In 2012, the frozen Linear Regression reached MAE 1,047.4, RMSE 1,204.0 and R-squared 0.546. Rolling-7 reached MAE 847.8, RMSE 1,178.3 and R-squared 0.565, leaving the selected model 23.5% worse on MAE. Random Forest scored MAE 1,673.3, while the 2011-selected Gradient Boosting and KNN configurations exceeded 2,000. Forward temporal robustness therefore fails.

A rolling one-day-ahead test can update lags after every observed day. A forecast issued for all of 2012 on 1 January could not use those later counts and would be a different experiment with a longer horizon and recursively unavailable inputs.
""")

CELLS_B = [MODELLING_HEAD, PRIMARY_SELECT, PRIMARY_HOLDOUT, HUM_SENSITIVITY, PRIMARY_READ,
           TEMPORAL_HEAD, TEMPORAL_SELECT, TEMPORAL_SCORE, TEMPORAL_READ]
