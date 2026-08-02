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
| Method | Regression comparison within CRISP-DM |
""")

BUSINESS = md(r"""
## 1. Business Understanding

### 1.1 Business objective

Capital Bikeshare is a docked bicycle-sharing system. This project asks:

> **Given calendar attributes and expected weather conditions, how accurately can regression models estimate Capital Bikeshare's system-wide daily rental demand?**

The estimate may inform fleet-capacity, staffing and maintenance planning. It does not estimate station inventory, bike availability or rebalancing needs. I use Lime in Sydney as a contemporary dockless analogy that motivated my interest; its operating model is different and supplies no evidence for this analysis. Capital Bikeshare's own service information establishes the docked operating context, while ITDP describes demand, network integration and performance as linked system-planning concerns (Capital Bikeshare, n.d.; ITDP, 2018).

### 1.2 Data and prediction scope

The modelling unit is one calendar day for the whole system. Predictors are calendar attributes and expected weather conditions. The primary random 75/25 experiment estimates conditional demand across the observed 2011-2012 domain and includes no past-demand features. It answers the assessment question directly.

The secondary experiment tests whether a model selected within 2011 remains useful for rolling one-day-ahead prediction in 2012. At the end of day D, counts through D and the next day's calendar and weather are assumed available. This makes lagged demand causal for this check. Forecasting all of 2012 from 1 January is a different task because later 2012 counts would then be unavailable.

### 1.3 Evaluation criteria

MAE is primary because it reports an average miss in rentals per day. MSE, RMSE and R-squared provide supporting views of large errors and explained variance.

- **Conditional demand estimation:** improve MAE by at least 40% over a training-mean baseline on the fixed 25% holdout.
- **Forward temporal robustness:** improve MAE by at least 5% over the rolling seven-day baseline on the identical 2012 dates.
- **Selection rule:** choose the lowest cross-validated MAE; configurations within 5% of that value are compared by cross-validated RMSE and then simplicity.

These study-defined criteria came from earlier exploratory versions. They support consistent analysis but are not stakeholder-validated service levels.

### 1.4 Assumptions and limitations

- The records contain observed weather. Treating it as expected next-day weather assumes perfect forecasts and makes the temporal check optimistic.
- Two years provide only one year-on-year transition, limiting evidence about persistent trend and seasonality.
- Daily `weathersit` category 4 is absent, so predictions require a supported-domain guard for categories 1-3.
- System-wide totals cannot answer station questions. ITDP and NACTO show that real network planning also needs station IDs, capacity, origin-destination flows, transit connections and local station demand (ITDP, 2018; NACTO, 2016).
""")

DATA_HEAD = md(r"""
## 2. Data Understanding

### 2.1 Source, loading and granularity

The UCI Bike Sharing dataset supplies `day.csv` and `hour.csv` for Capital Bikeshare in 2011-2012 (Fanaee-T & Gama, 2014). The daily file is the modelling source. The hourly file is loaded separately for intraday EDA and cross-file validation.
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
print("Table 2.1 - Granularity and role")
display(granularity)
print(f"Cross-file validation passed: hourly cnt sums exactly to daily cnt on all {len(cross_file)} dates.")
print(f"Hourly panel audit: {incomplete_dates} dates have fewer than 24 rows; "
      f"{omitted_hour_rows} zero-demand hour rows are omitted in total.")
''')

GRANULARITY_READ = md(r"""
`hour.csv` is not a balanced panel: 76 of 731 dates contribute fewer than 24 observations, with 165 hourly rows omitted in total. The hourly counts still reconstruct each daily total exactly, so those omitted rows contribute zero demand to the daily aggregate. An hourly model would change the target granularity, weight dates unequally and fail to observe those zero-demand periods, which could bias hourly estimates upward. `day.csv` already incorporates the complete daily total and gives each target day exactly one observation. The hourly file remains useful for intraday interpretation without altering the modelling unit.
""")

HOURLY = co(r'''
hour_profile = (hour_df.groupby(["workingday", "hr"], as_index=False)["cnt"].mean())
peaks = (hour_profile.loc[hour_profile.groupby("workingday")["cnt"].idxmax()]
         .assign(day_type=lambda x: x["workingday"].map({0: "Non-working day", 1: "Working day"}))
         [["day_type", "hr", "cnt"]].rename(columns={"hr": "peak_hour", "cnt": "mean_cnt"}))
peaks["mean_cnt"] = peaks["mean_cnt"].round(1)
print("Table 2.2 - Peak hourly demand")
display(peaks)
assert int(peaks.loc[peaks.day_type == "Working day", "peak_hour"].iloc[0]) == 17
assert np.isclose(peaks.loc[peaks.day_type == "Working day", "mean_cnt"].iloc[0], 525.3)
assert int(peaks.loc[peaks.day_type == "Non-working day", "peak_hour"].iloc[0]) == 13
assert np.isclose(peaks.loc[peaks.day_type == "Non-working day", "mean_cnt"].iloc[0], 372.7)

fig, ax = plt.subplots(figsize=(10.5, 4.6))
for flag, label, color in [(1, "Working day", "#20639B"), (0, "Non-working day", "#ED553B")]:
    p = hour_profile[hour_profile.workingday == flag]
    ax.plot(p.hr, p.cnt, marker="o", ms=3, lw=2, label=label, color=color)
ax.set(title="Figure 2.1 - Mean hourly rentals by day type", xlabel="hour of day", ylabel="mean hourly cnt")
ax.set_xticks(range(0, 24, 2)); ax.legend()
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_hourly_demand.png", dpi=160); plt.show()
''')

HOURLY_READ = md(r"""
Working-day demand peaks at 17:00 with a mean of 525.3 rentals, while non-working-day demand peaks at 13:00 with 372.7. The concentrated evening working-day peak is consistent with commute-oriented use; the broader midday profile is consistent with daytime leisure and errands. Aggregate counts do not identify trip purpose, so these are pattern interpretations, not proof of why a trip occurred.
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
print("Table 2.3 - Data quality audit")
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
The daily series is structurally complete and the identity `casual + registered = cnt` holds on every row. One date reports zero relative humidity; its companion hourly records contain only 22 rows and all repeat zero. The value is treated as a recording fault, changed to missing, and median-imputed inside each training fold. A later sensitivity check measures whether this correction changes the selected model's conclusion. Statistical tail values are retained because they remain plausible demand or weather observations.

Weather category 4 does not occur. The supported input domain is therefore categories 1-3; an implementation using `handle_unknown="ignore"` still needs an input guard because silent encoding is not evidence of supported prediction.
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
season_lbl = {1: "spring", 2: "summer", 3: "fall", 4: "winter"}
weather_lbl = {1: "clear", 2: "mist", 3: "light rain/snow", 4: "heavy rain/snow"}
day_df["season_name"] = day_df.season.map(season_lbl)
day_df["weather_name"] = day_df.weathersit.map(weather_lbl)
day_df["year_name"] = day_df.yr.map({0: "2011", 1: "2012"})

fig, ax = plt.subplots(2, 2, figsize=(13, 9))
sns.histplot(day_df.cnt, bins=30, kde=True, ax=ax[0, 0], color="#20639B")
ax[0, 0].set(title="Daily-rental distribution", xlabel="daily cnt")
sns.lineplot(data=day_df, x="dteday", y="cnt", hue="year_name", ax=ax[0, 1])
ax[0, 1].set(title="Daily demand over time", xlabel="date", ylabel="cnt")
sns.barplot(data=day_df, x="season_name", y="cnt", order=["spring", "summer", "fall", "winter"], ax=ax[1, 0])
ax[1, 0].set(title="Mean demand by season", xlabel="")
sns.boxplot(data=day_df, x="weather_name", y="cnt", order=["clear", "mist", "light rain/snow", "heavy rain/snow"], ax=ax[1, 1])
ax[1, 1].set(title="Demand by weather category", xlabel="")
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_daily_eda.png", dpi=150); plt.show()

comp = day_df.groupby("season_name")[["casual", "registered"]].mean().reindex(["spring", "summer", "fall", "winter"])
fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
comp.plot(kind="bar", stacked=True, ax=ax[0], color=["#ED553B", "#20639B"])
ax[0].set(title="Mean user-group composition by season", xlabel="", ylabel="mean daily rentals")
ax[0].tick_params(axis="x", rotation=0)
for c, color in zip(["temp", "atemp", "hum", "windspeed"], ["#20639B", "#3CAEA3", "#F6D55C", "#ED553B"]):
    ax[1].scatter(day_df[c], day_df.cnt, s=10, alpha=.28, label=c, color=color)
ax[1].set(title="Continuous weather measures and demand", xlabel="normalised weather value", ylabel="cnt")
ax[1].legend()
plt.tight_layout(); plt.savefig(FIG_DIR / "v4_composition_weather.png", dpi=150); plt.show()
''')

EDA_READ = md(r"""
Demand rises across the two years, follows a strong seasonal pattern and is lower under adverse weather. Temperature and feels-like temperature have the clearest positive associations; humidity and wind are weaker and generally negative. Registered users provide most rentals, while the casual share expands in warmer seasons. The group composition remains descriptive because either component would leak the target into a predictor list.
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
           PREP_HEAD, PREP, DESIGN]
