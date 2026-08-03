"""v4 cells, part A: title, business/data understanding, EDA and preparation."""

md = lambda s: ("markdown", s.strip("\n"))
co = lambda s: ("code", s.strip("\n"))

TITLE = md(r"""
# Predicting Daily Demand for Capital Bikeshare

## Regression Model Comparison and Temporal Robustness Testing

*MLN601 Assessment 3 - CRISP-DM*

Design and Creative Technologies, Torrens University

- **Student:** Luis Guilherme de Barros Andrade Faria - A00187785
- **Subject:** Machine Learning (MLN601)
- **Lecturer:** Dr. Kamran Shaukat
- **Assessment:** 3
- **Date:** August 2026

| Field | Scope |
|---|---|
| Dataset | UCI Bike Sharing, Capital Bikeshare daily and hourly files, Washington DC, 2011-2012 |
| Target | `cnt`: system-wide daily rentals |
| Primary question | Conditional daily-demand estimation from calendar attributes and expected weather |
| Secondary check | Rolling day-ahead temporal robustness, trained in 2011 and evaluated in 2012 |
| Method | Regression comparison within CRISP-DM (Chapman et al., 2000) |
""")

BUSINESS = md(r"""
## 1. Business Understanding

### 1.1 Business objective

Capital Bikeshare is a docked bicycle-sharing system (Capital Bikeshare, n.d.). This project asks:

> **Given calendar attributes and expected weather conditions, how accurately can regression models estimate Capital Bikeshare's system-wide daily rental demand?**

Daily demand is total network rentals in one day. An accurate estimate could support fleet-capacity, staffing and maintenance planning. Station inventory and rebalancing are outside scope because the CSVs lack station identifiers, locations and capacity; station-level data could extend the work.

Lime in Sydney is a contemporary dockless analogy that motivates my interest and makes the assessment closer to my reality. Although its operations differ, it raises a parallel question: how could calendar and weather patterns inform fleet planning in a local system? It motivates the work but is not model evidence.

### 1.2 Data and prediction scope

Each row represents one system-wide day, with `cnt` as total rentals. Calendar attributes are known in advance. Observed weather proxies expected weather; real use would require forecasts. The hourly file supports exploration without changing the daily target.

The primary random 75/25 experiment estimates demand for days resembling 2011-2012 using calendar and weather without past demand. The secondary experiment tests transfer through time: selection uses 2011, then counts through day D plus next-day conditions predict D+1 in 2012. Forecasting all of 2012 on 1 January is separate because later counts would be unavailable.

This report therefore runs three comparisons. The first two answer the assessment question; the third tests whether that answer transfers forward in time.

**Table 1 - What this report compares**

| # | Comparison | Split | Compared against | Question answered | Where |
|---|---|---|---|---|---|
| 1 | Model selection | Random 75/25, training partition only | The other 11 family and feature-set configurations | Which configuration predicts most accurately? | Table 6 |
| 2 | Value of modelling | Random 75/25, holdout opened once | A constant training-mean prediction | Does the selected model beat not modelling at all? | Tables 7 and 8 |
| 3 | Forward transfer | Time-ordered: trained in 2011, scored on 2012 | Naive lag-1, lag-7 and rolling seven-day rules | Does the approach still work on a period it has not seen? | Table 12 |

Comparisons 1 and 2 address the brief. Comparison 3 is an additional check that limits how the result may be used.

### 1.3 Evaluation criteria

MAE is primary because it reports the average miss in rentals per day. RMSE gives more weight to large errors, while R-squared shows explained variation relative to predicting the sample mean.

The training-mean baseline tests whether predictors add value; the primary model must improve MAE by 40%. Rolling seven-day demand is the temporal reference because it adapts to recent demand; the frozen ML model must beat it by 5% on identical 2012 dates.

Model, feature and hyperparameter choices use training-only cross-validation. Lowest MAE leads; configurations within 5% are separated by RMSE and then simplicity. The holdout is used only after selection.

These study-defined criteria came from earlier exploratory versions and are not stakeholder-validated service levels.

### 1.4 Assumptions and limitations

- Observed weather omits forecast error, making reported day-ahead accuracy optimistic.
- Two years provide one year-on-year transition, weak evidence for persistent growth.
- Weather category 4 is absent; an input guard must restrict use to supported categories 1-3.
- System totals cannot answer station questions. The Institute for Transportation and Development Policy (ITDP) publishes bikeshare planning guidance; the National Association of City Transportation Officials (NACTO) publishes network and station-siting guidance. They explain why future station planning also needs identifiers, capacity, trip flows, transit connections and local demand (ITDP, 2018; NACTO, 2016).
""")

DATA_HEAD = md(r"""
## 2. Data Understanding

### 2.1 Source, loading and granularity

The UCI Bike Sharing dataset supplies `day.csv` and `hour.csv` for Capital Bikeshare in 2011-2012 (Fanaee-T & Gama, 2014; University of California, Irvine, n.d.). The daily file is the modelling source. The hourly file is loaded separately for intraday EDA and cross-file validation.
""")

IMPORT_LOAD = co(r'''
import os
import warnings
from pathlib import Path

os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import (
    train_test_split, GridSearchCV, KFold, TimeSeriesSplit, cross_validate
)
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sns.set_theme(style="whitegrid")
RANDOM_STATE = 42

NB_DIR = Path.cwd()
BASE_DIR = NB_DIR.parent if NB_DIR.name == "notebook" else NB_DIR
DATA_DIR = BASE_DIR / "dataset"
OUTPUT_DIR = BASE_DIR / "outputs"
FIG_DIR = OUTPUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

day_df = pd.read_csv(DATA_DIR / "day.csv", parse_dates=["dteday"]).sort_values("dteday").reset_index(drop=True)
hour_df = pd.read_csv(DATA_DIR / "hour.csv", parse_dates=["dteday"]).sort_values(["dteday", "hr"]).reset_index(drop=True)
print("day.csv :", day_df.shape, day_df.dteday.min().date(), "to", day_df.dteday.max().date())
print("hour.csv:", hour_df.shape, hour_df.dteday.min().date(), "to", hour_df.dteday.max().date())
''')

GRANULARITY = co(r'''
hourly_daily = hour_df.groupby("dteday", as_index=False)["cnt"].sum().rename(columns={"cnt": "hourly_sum"})
cross_file = day_df[["dteday", "cnt"]].merge(hourly_daily, on="dteday", how="outer", validate="one_to_one")
cross_file["difference"] = cross_file["hourly_sum"] - cross_file["cnt"]
assert len(cross_file) == 731
assert cross_file["difference"].eq(0).all(), "Hourly cnt does not sum to daily cnt for every date"
hours_per_date = hour_df.groupby("dteday").size()
incomplete_dates = int(hours_per_date.lt(24).sum())
omitted_hour_rows = int((24 - hours_per_date).sum())
assert incomplete_dates == 76 and omitted_hour_rows == 165

granularity = pd.DataFrame([
    {"file": "day.csv", "rows": len(day_df), "observation": "one daily prediction unit",
     "role": "selected for modelling"},
    {"file": "hour.csv", "rows": len(hour_df), "observation": "correlated hourly observations",
     "role": "intraday understanding and cross-file validation"},
])
print("Table 2 - Granularity and role")
display(granularity)
print(f"Cross-file validation passed: hourly cnt sums exactly to daily cnt on all {len(cross_file)} dates.")
print(f"Hourly panel audit: {incomplete_dates} dates have fewer than 24 rows; "
      f"{omitted_hour_rows} zero-demand hour rows are omitted in total.")
''')

GRANULARITY_READ = md(r"""
`hour.csv` is unbalanced: 76 of 731 dates have fewer than 24 observations, with 165 zero-demand rows omitted. An hourly model would change granularity, weight dates unequally and omit those periods. Selecting `day.csv` gives every target day one complete observation **to avoid hourly bias**. The hourly counts still reconstruct all daily totals and remain useful for intraday interpretation.
""")

HOURLY = co(r'''
hour_profile = (hour_df.groupby(["workingday", "hr"], as_index=False)["cnt"].mean())
peaks = (hour_profile.loc[hour_profile.groupby("workingday")["cnt"].idxmax()]
         .assign(day_type=lambda x: x["workingday"].map({0: "Non-working day", 1: "Working day"}))
         [["day_type", "hr", "cnt"]].rename(columns={"hr": "peak_hour", "cnt": "mean_cnt"}))
peaks["mean_cnt"] = peaks["mean_cnt"].round(1)
print("Table 3 - Peak hourly demand")
display(peaks)
assert int(peaks.loc[peaks.day_type == "Working day", "peak_hour"].iloc[0]) == 17
assert np.isclose(peaks.loc[peaks.day_type == "Working day", "mean_cnt"].iloc[0], 525.3)
assert int(peaks.loc[peaks.day_type == "Non-working day", "peak_hour"].iloc[0]) == 13
assert np.isclose(peaks.loc[peaks.day_type == "Non-working day", "mean_cnt"].iloc[0], 372.7)

fig, ax = plt.subplots(figsize=(10.5, 4.6))
for flag, label, color in [(1, "Working day", "#20639B"), (0, "Non-working day", "#ED553B")]:
    p = hour_profile[hour_profile.workingday == flag]
    ax.plot(p.hr, p.cnt, marker="o", ms=3, lw=2, label=label, color=color)
ax.set(title="Figure 1 - Mean hourly rentals by day type", xlabel="hour of day", ylabel="mean hourly cnt")
ax.set_xticks(range(0, 24, 2)); ax.legend()
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_hourly_demand.png", dpi=160); plt.show()
''')

HOURLY_READ = md(r"""
Working-day demand peaks at 17:00 (525.3 rentals), while non-working-day demand peaks at 13:00 (372.7). The profiles are consistent with commute-oriented and broader daytime use, respectively; aggregate counts do not prove trip purpose.
""")

QUALITY = co(r'''
span_days = (day_df.dteday.max() - day_df.dteday.min()).days + 1
norm_cols = ["temp", "atemp", "hum", "windspeed"]
quality = pd.DataFrame([
    ("Daily rows equal calendar span", len(day_df) == span_days, f"{len(day_df)} rows / {span_days} days"),
    ("No date gaps", day_df.dteday.diff().dropna().dt.days.max() == 1, "daily continuity"),
    ("No exact duplicates", day_df.duplicated().sum() == 0, f"{day_df.duplicated().sum()} duplicates"),
    ("No source missing values", day_df.isna().sum().sum() == 0, f"{day_df.isna().sum().sum()} missing"),
    ("casual + registered = cnt", (day_df.casual + day_df.registered == day_df.cnt).all(), "all rows"),
    ("Normalised weather in [0,1]", all(day_df[c].between(0, 1).all() for c in norm_cols), "all four columns"),
    ("Humidity above zero", (day_df.hum > 0).all(), f"{int((day_df.hum == 0).sum())} zero reading"),
    ("Daily weather categories supported", set(day_df.weathersit.unique()) == {1, 2, 3}, "category 4 absent"),
], columns=["check", "pass", "evidence"])
print("Table 4 - Data quality audit")
display(quality)

zero_hum_date = day_df.loc[day_df.hum.eq(0), "dteday"].iloc[0]
zero_hour_rows = hour_df[hour_df.dteday.eq(zero_hum_date)]
print("Zero-humidity date:", zero_hum_date.date(), "| hourly rows:", len(zero_hour_rows),
      "| hourly humidity values:", sorted(zero_hour_rows.hum.unique()))

# Keep a raw frame for sensitivity analysis, then mark the implausible value missing.
raw_day_df = day_df.copy()
day_df.loc[day_df.hum.eq(0), "hum"] = np.nan
assert day_df.hum.isna().sum() == 1
''')

QUALITY_READ = md(r"""
The daily series is complete and `casual + registered = cnt` holds throughout. One date reports zero humidity across 22 hourly rows. It is treated as a recording fault, changed to missing and median-imputed inside each training fold; a sensitivity check tests the decision. Plausible tail values are retained.

Weather category 4 is absent, so the supported domain is 1-3 and still requires an input guard.
""")

VARIABLES = md(r"""
### 2.2 Variables and exploratory analysis

| Variables | Role |
|---|---|
| `cnt` | Continuous target: system-wide rentals per day |
| `season`, `yr`, `mnth`, `holiday`, `weekday`, `workingday` | Calendar predictors |
| `weathersit`, `temp`, `atemp`, `hum`, `windspeed` | Weather predictors |
| `dteday` | Ordering and elapsed-time construction; not passed directly to a model |
| `casual`, `registered` | Descriptive plots only; excluded because they sum exactly to `cnt` |

`casual` and `registered` describe user groups, not independent predictors. Registered users may include commuters, but membership status does not prove trip purpose.
""")

EDA = co(r'''
season_lbl = {1: "winter", 2: "spring", 3: "summer", 4: "autumn"}
weather_lbl = {1: "clear", 2: "mist", 3: "light rain/snow", 4: "heavy rain/snow"}
day_df["season_name"] = day_df.season.map(season_lbl)
day_df["weather_name"] = day_df.weathersit.map(weather_lbl)
day_df["year_name"] = day_df.yr.map({0: "2011", 1: "2012"})

fig, ax = plt.subplots(2, 2, figsize=(13, 9))
sns.histplot(day_df.cnt, bins=30, kde=True, ax=ax[0, 0], color="#20639B")
ax[0, 0].set(title="Daily-rental distribution", xlabel="daily cnt")
sns.lineplot(data=day_df, x="dteday", y="cnt", hue="year_name", ax=ax[0, 1])
ax[0, 1].set(title="Daily demand over time", xlabel="date", ylabel="cnt")
sns.barplot(data=day_df, x="season_name", y="cnt", order=["winter", "spring", "summer", "autumn"], ax=ax[1, 0])
ax[1, 0].set(title="Mean demand by season", xlabel="")
sns.boxplot(data=day_df, x="weather_name", y="cnt", order=["clear", "mist", "light rain/snow", "heavy rain/snow"], ax=ax[1, 1])
ax[1, 1].set(title="Demand by weather category", xlabel="")
fig.suptitle("Figure 2 - Daily demand, season and weather", y=1.01)
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_daily_eda.png", dpi=150); plt.show()

comp = day_df.groupby("season_name")[["casual", "registered"]].mean().reindex(["winter", "spring", "summer", "autumn"])
fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
comp.plot(kind="bar", stacked=True, ax=ax[0], color=["#ED553B", "#20639B"])
ax[0].set(title="Mean user-group composition by season", xlabel="", ylabel="mean daily rentals")
ax[0].tick_params(axis="x", rotation=0)
for c, color in zip(["temp", "atemp", "hum", "windspeed"], ["#20639B", "#3CAEA3", "#F6D55C", "#ED553B"]):
    ax[1].scatter(day_df[c], day_df.cnt, s=10, alpha=.28, label=c, color=color)
ax[1].set(title="Continuous weather measures and demand", xlabel="normalised weather value", ylabel="cnt")
ax[1].legend()
fig.suptitle("Figure 3 - User composition and continuous weather", y=1.02)
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_composition_weather.png", dpi=150); plt.show()
''')

EDA_READ = md(r"""
Demand rises across the two years, peaks in warmer seasons and falls in adverse weather. Registered users provide most rentals, while the casual share expands in warmer seasons. Both user columns remain descriptive because they sum to the target.

**A documentation correction.** The dataset description states `season (1:springer, 2:summer, 3:fall, 4:winter)`. The dates disagree. Code 1 covers December to March at a mean of 12.2 degrees Celsius and the lowest mean demand of 2,604; code 3 covers June to September at 29.0 degrees and the highest mean demand of 5,644. The codes are therefore offset by one quarter from the published labels, and this notebook labels them `1 = winter, 2 = spring, 3 = summer, 4 = autumn` on the evidence of the calendar and temperature rather than the documentation. Nothing in the modelling changes, because `season` enters every pipeline as a categorical code and never as a name; the correction affects the readability of Figures 2, 3 and 13 and the wording of this section.
""")

CALENDAR_EDA = co(r'''
weekday_lbl = {0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"}
day_df["weekday_name"] = day_df.weekday.map(weekday_lbl)

fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
sns.lineplot(data=day_df, x="mnth", y="cnt", hue="year_name", marker="o", ax=ax[0])
ax[0].set(title="Figure 4 - Mean rentals by month and year", xlabel="month", ylabel="mean cnt")
ax[0].set_xticks(range(1, 13))
sns.barplot(data=day_df, x="weekday_name", y="cnt",
            order=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], ax=ax[1])
ax[1].set(title="Figure 5 - Mean rentals by weekday", xlabel="weekday", ylabel="mean cnt")
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_month_weekday.png", dpi=160); plt.show()
''')

CALENDAR_READ = md(r"""
Monthly demand follows the seasonal wave and every 2012 month exceeds its 2011 counterpart. Weekday means vary much less, showing that aggregation blends working-day and leisure patterns visible in the hourly profiles.
""")

CORRELATION = co(r'''
corr_cols = ["season", "yr", "mnth", "holiday", "weekday", "workingday",
             "weathersit", "temp", "atemp", "hum", "windspeed", "cnt"]
corr_matrix = day_df[corr_cols].corr()
cnt_correlations = corr_matrix["cnt"].drop("cnt").sort_values(ascending=False)
assert cnt_correlations.index[0] == "atemp"
assert cnt_correlations.loc["weathersit"] < 0 and cnt_correlations.loc["windspeed"] < 0

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0,
            square=True, cbar_kws={"shrink": .8}, annot_kws={"size": 7})
plt.title("Figure 6 - Correlation matrix for daily variables")
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_correlation_heatmap.png", dpi=160); plt.show()
print("Table 5 - Correlations with cnt")
display(cnt_correlations.round(3).to_frame("correlation_with_cnt"))
''')

CORRELATION_READ = md(r"""
`atemp` has the highest correlation with `cnt` (+0.631), followed by `temp` (+0.627) and `yr` (+0.567). Adverse weather (`weathersit`, -0.297), windspeed (-0.235) and corrected humidity (-0.115) are negative. The near-collinearity of `temp` and `atemp` cautions against interpreting linear coefficients independently; categorical codes also limit causal interpretation.
""")

PAIRPLOT = co(r'''
# Stage 2.6: use seaborn's pairplot function and include its output.
pairplot_data = day_df[["temp", "atemp", "hum", "windspeed", "cnt"]].dropna()
pair_grid = sns.pairplot(pairplot_data, corner=True, diag_kind="kde",
                         plot_kws={"alpha": .3, "s": 12})
pair_grid.fig.suptitle("Figure 7 - Seaborn pairplot of weather variables and daily demand", y=1.02)
pair_grid.savefig(FIG_DIR / "v4_pairplot.png", dpi=140, bbox_inches="tight")
plt.show()
''')

PAIRPLOT_READ = md(r"""
The pairplot confirms positive, nonlinear relationships between demand and both temperature measures. Humidity and windspeed show weaker negative patterns and broad scatter. `temp` and `atemp` move almost identically, consistent with their high correlation, while no single weather variable fully explains demand.
""")

PREP_HEAD = md(r"""
## 3. Data Preparation

Two frames prevent the temporal question from shrinking the primary sample. `primary_df` contains all 731 days and no past-demand inputs. `temporal_df` starts after a causal seven-day warm-up and contains 724 days.
""")

PREP = co(r'''
# Shared calendar/weather engineering. Interactions use only target-day exogenous inputs.
day_df["atemp_hum"] = day_df["atemp"] * day_df["hum"]
day_df["temp_sq"] = day_df["temp"] ** 2
day_df["days_since_start"] = (day_df.dteday - day_df.dteday.min()).dt.days
day_df["mnth_sin"], day_df["mnth_cos"] = np.sin(2*np.pi*day_df.mnth/12), np.cos(2*np.pi*day_df.mnth/12)
day_df["weekday_sin"], day_df["weekday_cos"] = np.sin(2*np.pi*day_df.weekday/7), np.cos(2*np.pi*day_df.weekday/7)
day_df["season_sin"], day_df["season_cos"] = np.sin(2*np.pi*day_df.season/4), np.cos(2*np.pi*day_df.season/4)

primary_df = day_df.copy().reset_index(drop=True)

# Causal temporal features: every window ends before the target day.
day_df["lag_1_cnt"] = day_df.cnt.shift(1)
day_df["lag_7_cnt"] = day_df.cnt.shift(7)
day_df["roll_7_cnt"] = day_df.cnt.shift(1).rolling(7).mean()
assert day_df.lag_1_cnt.equals(day_df.cnt.shift(1))
assert day_df.lag_7_cnt.equals(day_df.cnt.shift(7))
for i in range(7, len(day_df)):
    assert np.isclose(day_df.loc[i, "roll_7_cnt"], day_df.loc[i-7:i-1, "cnt"].mean())
temporal_df = day_df.dropna(subset=["roll_7_cnt"]).reset_index(drop=True)

assert len(primary_df) == 731
assert len(temporal_df) == 724
print("primary_df rows:", len(primary_df), "| temporal_df rows:", len(temporal_df))
''')

DESIGN = co(r'''
PRIMARY_NOMINAL = ["season", "mnth", "weekday", "weathersit"]
PRIMARY_BINARY = ["yr", "holiday", "workingday"]
WEATHER = ["temp", "atemp", "hum", "windspeed"]
CYCLICAL = ["mnth_sin", "mnth_cos", "weekday_sin", "weekday_cos", "season_sin", "season_cos"]
INTERACTIONS = ["atemp_hum", "temp_sq"]
TREND = ["days_since_start"]
AUTOREGRESSIVE = ["lag_1_cnt", "lag_7_cnt", "roll_7_cnt"]

PRIMARY_FEATURE_SETS = {
    "core": PRIMARY_NOMINAL + PRIMARY_BINARY + WEATHER,
    "core + interactions": PRIMARY_NOMINAL + PRIMARY_BINARY + WEATHER + INTERACTIONS,
    "core + interactions + trend": PRIMARY_NOMINAL + PRIMARY_BINARY + WEATHER + INTERACTIONS + TREND,
}
TEMPORAL_FEATURE_SETS = {
    "core": ["weathersit", "holiday", "workingday"] + WEATHER + CYCLICAL,
    "core + interactions": ["weathersit", "holiday", "workingday"] + WEATHER + CYCLICAL + INTERACTIONS,
    "core + interactions + autoregressive": ["weathersit", "holiday", "workingday"] + WEATHER + CYCLICAL + INTERACTIONS + AUTOREGRESSIVE,
    "core + interactions + autoregressive + trend": ["weathersit", "holiday", "workingday"] + WEATHER + CYCLICAL + INTERACTIONS + AUTOREGRESSIVE + TREND,
}

for feature_list in list(PRIMARY_FEATURE_SETS.values()) + list(TEMPORAL_FEATURE_SETS.values()):
    assert "casual" not in feature_list and "registered" not in feature_list
assert all(c not in cols for cols in PRIMARY_FEATURE_SETS.values() for c in AUTOREGRESSIVE)
assert all("yr" not in cols for cols in TEMPORAL_FEATURE_SETS.values())

def make_preprocessor(columns, temporal=False):
    nominal = ["weathersit"] if temporal else [c for c in PRIMARY_NOMINAL if c in columns]
    binary_pool = ["holiday", "workingday"] + ([] if temporal else ["yr"])
    binary = [c for c in binary_pool if c in columns]
    continuous = [c for c in columns if c not in nominal + binary]
    return ColumnTransformer([
        ("nominal", OneHotEncoder(drop="first", handle_unknown="ignore"), nominal),
        ("continuous", Pipeline([("impute", SimpleImputer(strategy="median")),
                                  ("scale", StandardScaler())]), continuous),
        ("binary", "passthrough", binary),
    ])

def pipeline_for(model, columns, temporal=False):
    return Pipeline([("prep", make_preprocessor(columns, temporal=temporal)), ("model", model)])

def metrics(y_true, predictions):
    mse = mean_squared_error(y_true, predictions)
    return {"MAE": mean_absolute_error(y_true, predictions), "MSE": mse,
            "RMSE": float(np.sqrt(mse)), "R2": r2_score(y_true, predictions)}

GRIDS = {
    "Linear Regression": (LinearRegression(), {}),
    "K-Nearest Neighbors": (KNeighborsRegressor(), {
        "model__n_neighbors": [3, 5, 7, 9, 11, 15], "model__weights": ["uniform", "distance"]}),
    "Random Forest": (RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=1), {
        "model__n_estimators": [200, 400], "model__max_depth": [None, 8, 16],
        "model__min_samples_leaf": [1, 2, 4]}),
    "Gradient Boosting": (GradientBoostingRegressor(random_state=RANDOM_STATE), {
        "model__n_estimators": [200, 400], "model__max_depth": [2, 3],
        "model__learning_rate": [0.05, 0.1]}),
}

MODEL_SIMPLICITY = {"Linear Regression": 1, "K-Nearest Neighbors": 2,
                    "Random Forest": 3, "Gradient Boosting": 4}
FEATURE_SIMPLICITY = {name: i for i, name in enumerate(
    ["core", "core + interactions", "core + interactions + trend",
     "core + interactions + autoregressive", "core + interactions + autoregressive + trend"], 1)}

def compact_params(params):
    if not params:
        return "default"
    labels = {"model__learning_rate": "lr", "model__max_depth": "depth",
              "model__n_estimators": "estimators", "model__min_samples_leaf": "leaf",
              "model__n_neighbors": "neighbors", "model__weights": "weights"}
    return "; ".join(f"{labels.get(key, key)}={value}" for key, value in params.items())

def choose_configuration(rows):
    frame = pd.DataFrame(rows).copy()
    best_mae = frame["cv_mean_MAE"].min()
    shortlist = frame[frame["cv_mean_MAE"] <= 1.05 * best_mae].copy()
    shortlist["simplicity"] = shortlist["model"].map(MODEL_SIMPLICITY) + shortlist["feature_set"].map(FEATURE_SIMPLICITY) / 10
    return shortlist.sort_values(["cv_mean_RMSE", "simplicity", "cv_mean_MAE"]).iloc[0]
''')

CELLS_A = [TITLE, BUSINESS, DATA_HEAD, IMPORT_LOAD, GRANULARITY, GRANULARITY_READ,
           HOURLY, HOURLY_READ, QUALITY, QUALITY_READ, VARIABLES, EDA, EDA_READ,
           CALENDAR_EDA, CALENDAR_READ, CORRELATION, CORRELATION_READ,
           PAIRPLOT, PAIRPLOT_READ, PREP_HEAD, PREP, DESIGN]
