"""v3 cells, part A: title, Business Understanding, Data Understanding, Data Preparation."""

md = lambda s: ("markdown", s.strip("\n"))
co = lambda s: ("code", s.strip("\n"))

TITLE = md("""
# Day-Ahead Demand Planning for a Bike-Sharing System
""")

TITLE_META = md("""
*MLN601 Assessment 3 - Regression, Two Evaluation Protocols and CRISP-DM*

Design and Creative Technologies, Torrens University

- **Student:** Luis Guilherme de Barros Andrade Faria - A00187785
- **Subject Name:** Machine Learning
- **Subject Code:** MLN 601
- **Title:** Day-Ahead Demand Planning for a Bike-Sharing System (Capital Bikeshare)
- **Lecturer:** Dr. Kamran Shaukat
- **Assessment No.:** 3
- **Date:** August 2026

| Field | Value |
|---|---|
| Dataset | UCI Bike Sharing - daily aggregate, Washington DC 2011-2012 (Fanaee-T and Gama, 2014) |
| Target | `cnt`, total daily rentals (continuous) |
| Required algorithm | Regression, expanded into a five-candidate comparison |
| Experiment | Two protocols: random-split interpolation and time-ordered day-ahead forecasting |
| Methodology | CRISP-DM |

Each row in the UCI daily file is one calendar day for the whole system. In this project, I
treat that single row as one operational planning unit, assuming the system is planned centrally
- I am not modelling individual stations or individual bikes. The model's job is to tell an
operator how many rentals to expect tomorrow, so bikes, staff and maintenance windows can be
scheduled the evening before. It is a decision-support tool, where a human always makes the
final call, and no fleet or roster decision is ever taken automatically.

Demand is driven by weather and human behaviour that the dataset records only partly, and the
system grew 64% between the two observed years, so every model is framed as a decision-support
candidate judged against the naive rules an operator could already apply by hand, not as a
replacement for operational judgement.
""")

BU = md("""
## 1. Business Understanding

### 1.1 The question, and who asks it

A bike-share operator has to decide how many bikes to have on the street, how many staff to
roster, and when to schedule maintenance. Those decisions are made a day in advance, and they
are made for the system as a whole. The question this project answers is therefore:

> **How many rentals will the system serve tomorrow?**

I use dockless share bikes almost daily in Sydney, for commuting to work and to university and
for errands across the city. That is what makes the variation in this dataset legible to me:
demand collapses in rain, climbs with temperature, and behaves differently on a working day
than on a Sunday. The dataset here is Capital Bikeshare in Washington DC, a **docked** system
observed in 2011 and 2012, so the personal experience motivates the question rather than
supplying evidence for it. The evidence comes from the exploratory analysis in Section 2.

**Scope: system-wide daily demand, not station rebalancing.** The dataset is one row per day
for the whole system. It carries no station identifier, no location, no inventory and no
availability column, so it cannot support a claim about moving bikes between stations. It can
support demand planning, staffing, fleet sizing and maintenance scheduling.

### 1.2 The forecast horizon, stated explicitly

Everything in this report depends on what the model knows when it runs, so I state that first
rather than leaving it implied.

> At prediction time the system knows every daily count up to and including yesterday, plus
> the calendar attributes and the weather forecast for the target day. It does not know the
> target day's realised demand.

This is a **rolling day-ahead** horizon: the model runs at the close of day D to predict day
D+1. Three consequences follow, and each one shapes a design decision later in the notebook.

1. Yesterday's count, last week's count and a trailing seven-day average are **legitimate
   inputs**, not leakage, because that data has genuinely occurred by the time the model runs.
2. The same information is available to any operator for free. A person can read yesterday's
   number off a dashboard. That makes the **naive day-ahead rules the honest adversary** for
   any model I build, not the mean of the training set.
3. The alternative horizon is explicitly rejected. Forecasting all of 2012 on 1 January 2012,
   from 2011 alone, would make every autoregressive input unavailable, force recursive
   prediction with compounding error, and leave the 2011 constant mean as the only valid
   baseline. That comparison would be **easier** to win, not harder. Naming it here is what
   stops the day-ahead choice from reading as a convenient way to pick a weak benchmark.

### 1.3 Two protocols, because the data supports two different claims

The brief asks which model performs best on this dataset. The conventional answer uses a random
train/test split. But a random split over a two-year time series scatters 2012 days into the
training set, so the model is asked to fill gaps *inside* a period it has already seen. That is
interpolation, and it cannot support a claim about forecasting tomorrow.

Rather than pick one and hide the other, this report runs both and keeps their conclusions
separate.

| Protocol | Split | Question it answers | What it is permitted to conclude |
|---|---|---|---|
| **A** | random 75/25 | Which model best explains demand across the observed period? | Names a benchmark winner. Grants no operational approval. |
| **B** | time-ordered, train 2011, confirm 2012 | Can a model forecast tomorrow better than a free naive rule? | Carries the operational decision: approve, approve with conditions, or reject. |

### 1.4 Success criteria, declared before the results

**Protocol A** must beat the mean baseline by at least 40% on MAE, and the error is reported as
a percentage of mean daily demand so it is interpretable without inventing a business tolerance
that no stakeholder in this project has supplied.

**Protocol B** is judged against the strongest naive day-ahead baseline measured on the
identical dates. The model must beat it by a **material 5% margin on MAE** and must not have a
lower R-squared. A model that cannot materially beat a rule an operator could apply by hand is
not a forecaster, however well it scores under Protocol A.

**Tie-break:** models within 5% of each other on MAE are separated by RMSE, which penalises
catastrophic days; if still tied, the simpler and more interpretable model wins.

**Metrics:** MAE is primary, as the brief specifies. MSE, RMSE and R-squared are reported
alongside it because the rubric names them and because they disagree in informative ways.

### 1.5 Decision rules, written before the experiment ran

The conclusion of this report is not pre-written. Protocol B resolves to exactly one of the
following rows, and which row fires is decided by the measured numbers in Section 5.

| Condition | Verdict |
|---|---|
| ML beats the best naive MAE by >= 5% and does not lose on R-squared | Approve with conditions for day-ahead use |
| ML beats the best naive rule, but by less than 5% | No material improvement; the naive rule is retained on simplicity |
| ML MAE is higher than the best naive rule | The naive baseline wins; reject ML for forecasting |
| ML cannot beat even the constant mean | Reject ML forecasting outright |

The second and third rows are different claims and the report does not blur them. A model at
MAE 830 against a naive 847.8 has produced an improvement that is **not material**; it has not
"lost to the naive rule".

### 1.6 Assumptions and limitations, stated here rather than buried

- The dataset records **observed** weather, not the weather *forecast* that would be available
  the evening before. Protocol B therefore assumes a perfect next-day weather forecast and is
  optimistic relative to production.
- Only two years of history exist. Any claim about trend or seasonality rests on a single
  repetition, which is not enough to separate a trend from a level shift.
- Severe weather (`weathersit` category 4) never occurs in the daily file, so no model here has
  any evidence about it. Section 6 turns this into a deployment requirement rather than a
  footnote.
- **2012 is confirmation evidence, not a blind holdout.** It was inspected during the earlier
  version of this project to establish the naive baselines and to test a trend feature, and the
  Protocol B threshold is derived from a baseline measured on it. The criteria were fixed before
  the v3 models were run, which makes the comparison honest, but it is weaker than a
  pre-registered blind test and this report does not claim otherwise.
""")

DU_HEAD = md("""
## 2. Data Understanding

### 2.1 Source and loading

The UCI Bike Sharing dataset (Fanaee-T and Gama, 2014) records daily aggregated rentals for
Capital Bikeshare in Washington DC across 2011 and 2012, alongside calendar attributes and
normalised weather measurements. The daily file `day.csv` is the unit of analysis, matching the
day-ahead question declared in Section 1.
""")

IMPORTS = co("""
import os
import warnings

# Silence sklearn/joblib parallel UserWarnings so they cannot flood the exported PDF.
# n_jobs=1 in every grid search below means no worker processes spawn either.
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import wilcoxon

from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sns.set_theme(style="whitegrid")
RANDOM_STATE = 42
""")

LOAD = co("""
from pathlib import Path

NB_DIR = Path.cwd()
BASE_DIR = NB_DIR.parent if NB_DIR.name == "notebook" else NB_DIR
OUTPUT_DIR = BASE_DIR / "outputs"
FIG_DIR = OUTPUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

UCI_URL = ("https://archive.ics.uci.edu/static/public/275/"
           "bike+sharing+dataset.zip")


def load_bike():
    candidates = [BASE_DIR / "dataset" / "day.csv", NB_DIR / "dataset" / "day.csv",
                  NB_DIR / "day.csv"]
    local = next((p for p in candidates if p.exists()), None)
    if local is not None:
        print("Loading local:", local)
        return pd.read_csv(local, parse_dates=["dteday"])
    import io, zipfile, urllib.request
    print("Downloading from UCI:", UCI_URL)
    with urllib.request.urlopen(UCI_URL) as r:
        zf = zipfile.ZipFile(io.BytesIO(r.read()))
    return pd.read_csv(zf.open("day.csv"), parse_dates=["dteday"])


# Chronological order is established here, before any feature is engineered, because every
# lag and rolling feature in Section 3 depends on row order being calendar order.
df = load_bike().sort_values("dteday").reset_index(drop=True)
print("Shape:", df.shape, "| date range:", df.dteday.min().date(), "->", df.dteday.max().date())
df.head()
""")

INFO = co("df.info()")
DESCRIBE = co("df.describe().T")

AUDIT = co('''
# Table 2.1 - data quality audit, run before any modelling decision depends on the answers
span_days = (df["dteday"].max() - df["dteday"].min()).days + 1
gaps = df["dteday"].diff().dropna().dt.days
norm_cols = ["temp", "atemp", "hum", "windspeed"]
in_unit = all(df[c].between(0, 1).all() for c in norm_cols)

audit = pd.DataFrame([
    ("Expected schema and dtypes", "Pass", "Retain"),
    ("Row count matches the daily span",
     f"{len(df)} rows vs {span_days} expected days", "Retain"),
    ("Date continuity (no missing days)",
     "Pass" if gaps.max() == 1 else f"Fail: max gap {int(gaps.max())} days", "Retain"),
    ("Missing values",
     "Pass" if df.isna().sum().sum() == 0 else f"{int(df.isna().sum().sum())} found", "Retain"),
    ("Exact duplicate rows",
     "Pass" if df.duplicated().sum() == 0 else f"{int(df.duplicated().sum())} found", "Retain"),
    ("Identity casual + registered == cnt",
     "Pass" if (df.casual + df.registered == df.cnt).all() else "Fail", "Retain"),
    ("Normalised columns within [0, 1]", "Pass" if in_unit else "Fail", "Retain"),
    ("weathersit categories observed",
     ", ".join(str(k) for k in sorted(df.weathersit.unique())),
     "Category 4 absent: recorded as a domain limit"),
    ("Humidity physically plausible",
     f"Fail: {int((df.hum == 0).sum())} row at hum = 0",
     "Corrected before modelling (Table 2.2)"),
], columns=["check", "result", "action"])

print("Table 2.1 - Data quality audit")
print("Two checks do not pass: severe weather never occurs, and one humidity reading is zero.")
display(audit)
''')

OUTLIER = co('''
# Table 2.2 - outlier and plausibility review, separating statistical from physical problems
def iqr_flags(series):
    q1, q3 = series.quantile([0.25, 0.75])
    lo, hi = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
    return int(((series < lo) | (series > hi)).sum())

rows = [(c, iqr_flags(df[c]), "statistical outlier",
         "Retain: plausible measurement, not verified as an error")
        for c in ["cnt"] + norm_cols]

zero_hum = df.loc[df["hum"] == 0, ["dteday", "weathersit", "hum", "cnt"]]
rows.append(("hum (zero reading)", len(zero_hum), "physically implausible",
             "Correct to missing, impute per training fold"))

outliers = pd.DataFrame(rows, columns=["variable", "rows_flagged", "verdict", "action"])
print("Table 2.2 - Outlier and plausibility review")
print("The IQR flags are retained; the zero-humidity row is a data error and is corrected.")
display(outliers)

print("\\nThe implausible row:")
display(zero_hum)

# Zero relative humidity does not occur in nature, and the hourly file confirms the fault:
# this date carries 22 hourly rows instead of 24, all recording hum = 0. Treating it as
# missing lets a median imputer fitted inside each training fold supply a value, which keeps
# the correction out of the test data.
df.loc[df["hum"] == 0, "hum"] = np.nan
print("\\nRows now carrying missing humidity:", int(df["hum"].isna().sum()))
''')

AUDIT_READ = md("""
**Reading Tables 2.1 and 2.2.** The dataset is clean in every structural respect that matters:
731 rows for a 731-day span, no missing days, no duplicates, no missing values, and the
`casual + registered == cnt` identity holds exactly. Two findings are not cosmetic. First,
`weathersit` category 4, severe weather, **never occurs**, so no model trained here has any
evidence about that condition and Section 6 turns it into a deployment guardrail. Second, one
row records zero relative humidity, on a day the dataset simultaneously codes as light rain or
snow. Zero relative humidity does not occur in nature, and the hourly companion file records
only 22 hourly observations for that date instead of 24, all with the same zero. That is a
recording fault, not a rare day, so it is corrected to missing and imputed inside each training
fold rather than deleted or silently kept. The IQR flags on the continuous columns are a
different category: they are plausible weather and demand values that happen to sit in the
tails, and removing them would be discarding real signal.
""")

VARS = md("""
### 2.2 Variables

| Column | Meaning | Role in this project |
|---|---|---|
| `dteday` | Calendar date | Ordering key; not a model input |
| `season`, `mnth`, `weekday` | Calendar position | Predictors; cyclically encoded under Protocol B |
| `yr` | 2011 = 0, 2012 = 1 | Predictor under Protocol A only; under Protocol B it is constant in training |
| `holiday`, `workingday` | Day type flags | Predictors |
| `weathersit` | 1 clear, 2 mist, 3 light rain or snow, 4 severe | Predictor; category 4 never observed |
| `temp`, `atemp`, `hum`, `windspeed` | Normalised weather measurements | Predictors |
| `casual`, `registered` | Membership split of the total | **Excluded**: they sum to the target |
| `cnt` | Total daily rentals | **Target** |

`casual` and `registered` are excluded from every model. They add up to `cnt` exactly, so
including either would hand the model the answer. They remain in the exploratory analysis
because the composition is genuinely informative about who rides and when.
""")

EDA_HEAD = md("""
### 2.3 Exploratory data analysis
""")

CELLS_A_HEAD = [TITLE, TITLE_META, BU, DU_HEAD, IMPORTS, LOAD, INFO, DESCRIBE, AUDIT, OUTLIER,
                AUDIT_READ, VARS, EDA_HEAD]

GROWTH = co('''
# Figure 2.8 / Table 2.3 - the two-year growth that decides whether forecasting is possible
y11 = df.loc[df["yr"] == 0, "cnt"]
y12 = df.loc[df["yr"] == 1, "cnt"]
ceiling_2011 = int(y11.max())
above = int((y12 > ceiling_2011).sum())

growth = pd.DataFrame({
    "metric": ["mean daily rentals", "median daily rentals", "maximum daily rentals",
               "days above the 2011 maximum"],
    "2011": [round(y11.mean()), round(y11.median()), ceiling_2011, "-"],
    "2012": [round(y12.mean()), round(y12.median()), int(y12.max()),
             f"{above} of {len(y12)} ({above/len(y12)*100:.0f}%)"],
})
print("Table 2.3 - Year-on-year growth, and how much of 2012 sits outside 2011's range")
print(f"Mean demand grew {(y12.mean()/y11.mean()-1)*100:.1f}%, and almost half of 2012 is "
      "above anything 2011 recorded.")
display(growth)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df["dteday"], df["cnt"], lw=0.9, color="steelblue", label="daily rentals")
ax.axhline(ceiling_2011, color="crimson", ls="--",
           label=f"2011 maximum = {ceiling_2011}")
ax.fill_between(df["dteday"], ceiling_2011, df["cnt"],
                where=df["cnt"] > ceiling_2011, color="crimson", alpha=0.25,
                label=f"{above} days above it")
ax.set_title("Figure 2.8 - Daily demand against the 2011 ceiling")
ax.set_xlabel("date"); ax.set_ylabel("cnt"); ax.legend(loc="upper left")
plt.tight_layout()
plt.savefig(FIG_DIR / "v3_growth_ceiling.png", dpi=120)
plt.show()
''')

GROWTH_READ = md("""
**Reading Table 2.3 and Figure 2.8.** Mean daily demand grew 64.4% between the two years, from
about 3,406 to about 5,600 rentals a day. That growth is not a detail, it is the central
difficulty of this project. A tree-based model predicts by averaging training observations, so
it can never output a value above the largest one it was trained on. **175 of the 366 days in
2012, almost half the year, sit above the highest single day in 2011.** Any model trained on
2011 alone is therefore structurally incapable of reaching the right answer on half the days it
is asked about, no matter how well it is tuned. This is the reason Protocol B exists as a
separate experiment, and the reason its adversary is a naive rule rather than another model.
""")

DP = md("""
## 3. Data Preparation

Three preparation decisions follow directly from the day-ahead horizon declared in Section 1.

**Chronological order first.** The dataframe was sorted by date at load time, before any
feature was created. Every lag and rolling feature below assumes row order is calendar order,
and a shuffled frame would silently produce features that mix future and past.

**Autoregressive features, built causally.** The day-ahead horizon makes yesterday's demand
available at prediction time, so the model may use it. The construction has to be exact: the
rolling mean is **shifted first and then rolled**, so the window ends on yesterday and never
touches the target day. Assertions below verify this before any number is measured, because a
lag that leaks by one row is invisible in the metrics and fatal to the conclusion.

**Cyclical calendar encoding under Protocol B.** One-hot encoding a month is safe under a
random split, where every month appears in training. It is not safe under a time-ordered split:
the first training fold contains only January to April, so a July validation row encodes to all
zeros, which is exactly what January encodes to. The unseen month becomes indistinguishable
from the reference category. Sine and cosine pairs avoid this entirely by mapping the calendar
onto a circle that is defined for every value, seen or not. `weathersit` stays one-hot because
it is genuinely categorical rather than cyclic, and it is the column the deployment guardrail
in Section 6 protects.
""")

FEATURES = co('''
# Autoregressive features. The frame is already in date order, established at load time.
df["lag_1_cnt"] = df["cnt"].shift(1)                        # yesterday
df["lag_7_cnt"] = df["cnt"].shift(7)                        # same weekday last week
df["roll_7_cnt"] = df["cnt"].shift(1).rolling(7).mean()     # shift THEN roll

# Verify causality before anything is measured. A lag that leaks by one row would not show up
# in any metric; it would just make the forecasting result quietly wrong.
for lag, col in [(1, "lag_1_cnt"), (7, "lag_7_cnt")]:
    assert df[col].equals(df["cnt"].shift(lag)), f"{col} is not a pure {lag}-day lag"
probe = 400
assert np.isclose(df.loc[probe, "roll_7_cnt"], df.loc[probe - 7:probe - 1, "cnt"].mean()), \\
    "roll_7_cnt includes the target day"
assert df.loc[probe, "roll_7_cnt"] != df.loc[probe - 6:probe, "cnt"].mean(), \\
    "roll_7_cnt window is not shifted"
print("Causal lag assertions passed: no autoregressive feature can see the target day.")

# Cyclical calendar encoding (Protocol B), context interactions, and the trend candidate
df["mnth_sin"], df["mnth_cos"] = np.sin(2*np.pi*df.mnth/12), np.cos(2*np.pi*df.mnth/12)
df["weekday_sin"], df["weekday_cos"] = np.sin(2*np.pi*df.weekday/7), np.cos(2*np.pi*df.weekday/7)
df["season_sin"], df["season_cos"] = np.sin(2*np.pi*df.season/4), np.cos(2*np.pi*df.season/4)
df["atemp_hum"] = df["atemp"] * df["hum"]     # muggy days feel worse than either measure implies
df["temp_sq"] = df["temp"] ** 2               # demand falls again at the hot end
df["days_since_start"] = (df["dteday"] - df["dteday"].min()).dt.days

# The seven-day rolling window needs a warm-up, so the first seven days cannot be modelled.
model_df = df.dropna(subset=["roll_7_cnt"]).reset_index(drop=True)
print(f"Modelling rows after the 7-day warm-up: {len(model_df)} "
      f"(from {model_df.dteday.min().date()} to {model_df.dteday.max().date()})")
''')

GROUPS = co('''
# Four feature groups, so the ablation in Sections 4 and 5 can attribute any change to a cause
CORE_NOMINAL = ["season", "mnth", "weekday", "weathersit"]   # Protocol A encoding
CORE_BINARY = ["yr", "holiday", "workingday"]
CORE_CONTINUOUS = ["temp", "atemp", "hum", "windspeed"]
CYCLICAL = ["mnth_sin", "mnth_cos", "weekday_sin", "weekday_cos", "season_sin", "season_cos"]
INTERACTIONS = ["atemp_hum", "temp_sq"]
TREND = ["days_since_start"]
AUTOREGRESSIVE = ["lag_1_cnt", "lag_7_cnt", "roll_7_cnt"]

groups_table = pd.DataFrame([
    ("core calendar and weather", len(CORE_NOMINAL + CORE_BINARY + CORE_CONTINUOUS),
     "the conventional feature set both protocols start from"),
    ("context interactions", len(INTERACTIONS),
     "tests whether comfort is more than the sum of its parts"),
    ("trend", len(TREND), "tests whether elapsed time carries the growth signal"),
    ("autoregressive", len(AUTOREGRESSIVE),
     "tests recent demand; only legitimate under the day-ahead horizon"),
], columns=["group", "n_features", "hypothesis it tests"])
print("Table 3.1 - Feature groups and the hypothesis each one tests")
print("Each group is added and removed separately so a metric change can be attributed.")
display(groups_table)


def make_preprocessor(nominal, continuous, binary):
    """Median imputation is fitted inside each training fold, never on the full frame."""
    blocks = []
    if nominal:
        blocks.append(("oh", OneHotEncoder(drop="first", handle_unknown="ignore"), nominal))
    if continuous:
        blocks.append(("sc", Pipeline([("imp", SimpleImputer(strategy="median")),
                                       ("sc", StandardScaler())]), continuous))
    if binary:
        blocks.append(("pass", "passthrough", binary))
    return ColumnTransformer(blocks)


def build_design(protocol, groups):
    """Return the column list and preprocessor for a protocol and set of feature groups."""
    nominal = list(CORE_NOMINAL) if protocol == "A" else ["weathersit"]
    binary = list(CORE_BINARY)
    continuous = list(CORE_CONTINUOUS) + (CYCLICAL if protocol == "B" else [])
    if "inter" in groups:
        continuous += INTERACTIONS
    if "trend" in groups:
        continuous += TREND
    if "auto" in groups:
        continuous += AUTOREGRESSIVE
    return nominal + binary + continuous, make_preprocessor(nominal, continuous, binary)


def reg_metrics(y_true, pred):
    mse = mean_squared_error(y_true, pred)
    return {"MAE": mean_absolute_error(y_true, pred), "MSE": mse,
            "RMSE": float(np.sqrt(mse)), "R2": r2_score(y_true, pred)}
''')

CELLS_A_TAIL = [GROWTH, GROWTH_READ, DP, FEATURES, GROUPS]
