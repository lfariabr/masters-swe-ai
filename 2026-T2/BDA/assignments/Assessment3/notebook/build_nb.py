"""Builder for BDA601 Assessment 3 notebook (COVID-19 analytics).
Run with system python3 (has nbformat). Emits BDA601FariaLuis_Assessment3.ipynb,
to be executed with the bda-spark kernel (Python 3.11 + Spark 3.5)."""
import nbformat as nbf
from pathlib import Path

nb = nbf.v4.new_notebook()
cells = []
def md(s): cells.append(nbf.v4.new_markdown_cell(s))
def code(s): cells.append(nbf.v4.new_code_cell(s))

# ---------------------------------------------------------------- Title
md(r"""# BDA601 Assessment 3 - Model Evaluation
### COVID-19 analytics: regression, clustering and graph analytics on the Johns Hopkins time series

| Item | Detail |
|---|---|
| Student | Luis Faria |
| Subject | BDA601 - Big Data and Analytics |
| Assessment | Assessment 3 - Model Evaluation (40%) |
| Dataset | JHU CSSE confirmed-cases global time series (22 Jan 2020 - 9 Mar 2023) |
| Engine | Apache Spark MLlib (`pyspark.ml`) for regression + K-Means; networkx for graph |
| Deliverables | Source code (this notebook) + video presentation + PDF slides |

**Story in one line:** find the three worst-hit countries, model their growth, pick the most volatile
one, use clustering to expose its infection *waves*, then work out which non-bordering neighbour the
focal country can actually give an early warning to - and how many weeks of warning that is.""")

# ---------------------------------------------------------------- How to run
md(r"""## How to run this notebook

**Requirements** - Python 3.11, Java 8 (Spark 3.5 requires Java 8 or 11), and the packages
`pyspark==3.5.3`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `networkx`. No other configuration is
needed: `JAVA_HOME` is detected automatically in Section 0, and every path is resolved relative to
this notebook.

**Steps**

1. Place `time_series_covid19_confirmed_global.csv` in the `dataset/` folder next to this notebook's
   parent (that is, `Assessment3/dataset/`). The file is the *confirmed cases* global time series from
   the Johns Hopkins CSSE repository, available at
   <https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases>.
2. Run all cells top to bottom (`Kernel -> Restart & Run All`). Total runtime is about 1-2 minutes.
3. Outputs are written automatically to `outputs/figures/*.png` and `outputs/metrics.json`.

**If something goes wrong** - each stage validates its inputs and raises a message that names the
problem and the fix (missing dataset, missing Java, unknown country, insufficient overlap). Read the
message rather than the traceback: it tells you what to correct.""")

# ---------------------------------------------------------------- Setup
md(r"""## 0. Setup, environment checks and Spark session

Spark workers are pinned to this Python kernel (driver == executor) so there is no interpreter
mismatch, `JAVA_HOME` is discovered rather than hard-coded, and the seed is fixed for reproducibility.
Each check fails with an actionable message instead of an obscure traceback.""")

code(r"""import os, sys, json, subprocess, warnings
from pathlib import Path

warnings.filterwarnings("ignore")


class SetupError(RuntimeError):
    '''Raised when the environment or the input data is not usable.'''


def require(condition, message):
    '''Fail fast with an actionable message instead of an obscure traceback.'''
    if not condition:
        raise SetupError(message)


def find_java_home():
    '''Locate a Java 8/11 installation. Spark 3.5 will not start without one.'''
    env = os.environ.get("JAVA_HOME")
    if env and Path(env).exists():
        return env
    # macOS ships a helper that reports installed JVMs.
    for version in ("1.8", "11"):
        try:
            found = subprocess.run(["/usr/libexec/java_home", "-v", version],
                                   capture_output=True, text=True, timeout=10)
            if found.returncode == 0 and found.stdout.strip():
                return found.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass
    for candidate in ("/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home",
                      "/usr/lib/jvm/java-11-openjdk-amd64",
                      "/usr/lib/jvm/java-8-openjdk-amd64"):
        if Path(candidate).exists():
            return candidate
    return None


os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

java_home = find_java_home()
require(java_home is not None,
        "No Java installation found. Spark 3.5 needs Java 8 or 11. Install one (macOS: "
        "`brew install --cask temurin8`) or set JAVA_HOME to an existing JDK, then re-run this cell.")
os.environ["JAVA_HOME"] = java_home

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 110

# Resolve paths relative to the notebook so the project runs with no manual configuration.
CWD = Path.cwd()
ASSESS = CWD if (CWD / "dataset").exists() else CWD.parent
DATA = ASSESS / "dataset" / "time_series_covid19_confirmed_global.csv"
OUT_DIR = ASSESS / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

require(DATA.exists(),
        f"Dataset not found at {DATA}.\n"
        "Download 'time_series_covid19_confirmed_global.csv' (JHU CSSE confirmed cases) from "
        "https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases and place it in the "
        "'dataset' folder, then re-run this cell.")

print("Java home  :", java_home)
print("Python     :", sys.version.split()[0])
print("Dataset    :", DATA.name, f"({DATA.stat().st_size / 1e6:.1f} MB)")""")

code(r"""from pyspark.sql import SparkSession

try:
    spark = (SparkSession.builder.appName("BDA601-A3-COVID")
             .master("local[*]").config("spark.sql.shuffle.partitions", "8")
             .config("spark.ui.enabled", "false").getOrCreate())
    spark.sparkContext.setLogLevel("ERROR")
except Exception as exc:                      # noqa: BLE001 - surfaced to the user deliberately
    raise SetupError(
        f"Spark failed to start ({exc.__class__.__name__}: {exc}).\n"
        "The usual cause is a Java version mismatch: Spark 3.5 supports Java 8 and 11 only. "
        "Check `java -version` and point JAVA_HOME at a supported JDK."
    ) from exc

print("Spark version:", spark.version)""")

# ---------------------------------------------------------------- 1. Problem
md(r"""## 1. Problem statement

An enterprise big-data analytics project runs in three phases: **prepare** the data, **analyse and
visualise** it, and **make decisions** from the insight. Here the decision context is public health:
using the Johns Hopkins confirmed-case series, I identify the three most-infected countries, fit a
linear growth model to each, select the most volatile country, use K-Means to reveal how its infection
*waves* rose and fell over time, then use graph analytics to work out which non-bordering neighbours
track its trend - and, crucially, *with what time lag*, because only a neighbour that follows the focal
country can be warned by it. The chain is deliberate: each step feeds the next
(regression -> selection -> clustering -> graph -> lead-lag -> recommendation).""")

# ---------------------------------------------------------------- 2. Task 1 prep
md(r"""## 2. Dataset preparation

The file is *wide* (one column per day, cumulative counts). I reshape it to a tidy long form, sum the
province rows up to the country level, convert calendar dates to **week numbers** (Week 1 =
22-28 Jan 2020), and derive **weekly new cases** from the cumulative series. The top three countries are
those with the highest cumulative total on the latest date.

Two data-quality guards run here: the cumulative series must be non-decreasing (it is a running total,
so any decrease signals a reporting correction), and the reshaped frame must contain the expected
columns before anything downstream touches it.""")

code(r"""try:
    raw = pd.read_csv(DATA)
except Exception as exc:                       # noqa: BLE001
    raise SetupError(f"Could not read {DATA.name}: {exc}. The file may be truncated - re-download it.") from exc

expected = {"Province/State", "Country/Region", "Lat", "Long"}
require(expected.issubset(raw.columns),
        f"Unexpected file layout. Missing columns: {sorted(expected - set(raw.columns))}. "
        "Make sure this is the JHU 'confirmed_global' file and not the deaths or US-only variant.")

date_cols = raw.columns[4:]                                   # everything after Province, Country, Lat, Long
require(len(date_cols) > 0, "No date columns found - the file appears to contain metadata only.")

long = raw.melt(id_vars=["Country/Region"], value_vars=list(date_cols),
                var_name="date", value_name="confirmed")
long["date"] = pd.to_datetime(long["date"], format="%m/%d/%y")
# country-level cumulative per day (sum the province rows)
country_day = long.groupby(["Country/Region", "date"], as_index=False)["confirmed"].sum()

# week number relative to 22 Jan 2020
START = pd.Timestamp("2020-01-22")
country_day["week"] = ((country_day["date"] - START).dt.days // 7) + 1

# weekly cumulative = max within the week (cumulative is non-decreasing)
weekly = (country_day.groupby(["Country/Region", "week"], as_index=False)["confirmed"].max())
# weekly NEW cases = first difference of the cumulative series, floored at 0
weekly["new_cases"] = (weekly.groupby("Country/Region")["confirmed"].diff().fillna(weekly["confirmed"]).clip(lower=0))

# Data-quality check: how often does the "cumulative" series actually fall?
raw_diff = weekly.groupby("Country/Region")["confirmed"].diff()
corrections = int((raw_diff < 0).sum())
print(f"Reporting corrections (weeks where the cumulative total fell): {corrections} "
      f"of {len(weekly):,} country-weeks -> clipped to 0 new cases.")

# representative country centroid for the map/graph
centroid = raw.groupby("Country/Region")[["Lat", "Long"]].mean()

N_WEEKS = int(weekly["week"].max())
totals = weekly.groupby("Country/Region")["confirmed"].max().sort_values(ascending=False)
TOP3 = list(totals.head(3).index)
print("Total weeks:", N_WEEKS)
print("Top 3 most-infected countries (cumulative confirmed):")
print(totals.head(3).map(lambda x: f"{x:,.0f}"))""")

code(r"""# Visualise the cumulative curves of the top three countries.
plt.figure(figsize=(10, 5))
for c in TOP3:
    d = weekly[weekly["Country/Region"] == c]
    plt.plot(d["week"], d["confirmed"] / 1e6, label=c, lw=2)
plt.xlabel("Week number (Week 1 = 22 Jan 2020)"); plt.ylabel("Cumulative confirmed (millions)")
plt.title("Cumulative confirmed cases - top 3 countries"); plt.legend()
plt.tight_layout(); plt.savefig(FIG_DIR / "fig01_top3_cumulative.png"); plt.show()""")

# ---------------------------------------------------------------- 3. Regression
md(r"""## 3. Predictive modelling - linear regression per country

For each top-3 country I fit a Spark MLlib **linear regression** of cumulative count on week number
(the assumption being that infections rise steadily from week 1). To choose which country to carry into
the clustering step I rank them by the **variance of their weekly new cases** - a direct measure of
volatility, and the same weekly-new-case signal the clustering then works on. Ranking by the variance
of the *cumulative* total would instead just pick the largest country by construction, so volatility is
measured on the new-case series.

I also report **RMSE** and inspect the **residuals**, because R-squared alone is misleading on a
monotonically rising series: almost any upward line scores well. The residuals are the real evidence,
and if they show structure rather than noise, the straight-line assumption is wrong - which is exactly
the finding that motivates clustering in the next section.""")

code(r"""from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler

reg_rows, fits, residuals = [], {}, {}
for c in TOP3:
    d = weekly[weekly["Country/Region"] == c][["week", "confirmed"]].rename(columns={"confirmed": "label"})
    require(len(d) > 2, f"Not enough observations to fit a regression for {c} (found {len(d)} weeks).")
    sdf = spark.createDataFrame(d)
    va = VectorAssembler(inputCols=["week"], outputCol="features")
    lr = LinearRegression(featuresCol="features", labelCol="label").fit(va.transform(sdf))
    slope, intercept = float(lr.coefficients[0]), float(lr.intercept)
    # Volatility = variance of weekly NEW cases (not the cumulative total, which would just rank by size).
    newcase_var = float(weekly[weekly["Country/Region"] == c]["new_cases"].var())
    reg_rows.append({"country": c, "slope": slope, "intercept": intercept,
                     "r2": float(lr.summary.r2), "rmse": float(lr.summary.rootMeanSquaredError),
                     "newcase_var": newcase_var})
    fits[c] = (slope, intercept)
    residuals[c] = d["label"].to_numpy() - (slope * d["week"].to_numpy() + intercept)

reg = pd.DataFrame(reg_rows).sort_values("newcase_var", ascending=False).reset_index(drop=True)
FOCAL = reg.iloc[0]["country"]
print(reg.assign(newcase_var=reg["newcase_var"].map(lambda x: f"{x:.3e}"),
                 slope=reg["slope"].map(lambda x: f"{x:,.0f}/wk"),
                 rmse=reg["rmse"].map(lambda x: f"{x:,.0f}")).to_string(index=False))
print("\nMost volatile country by weekly new cases (carried forward):", FOCAL)""")

code(r"""# Plot the three regression fits.
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, c in zip(axes, TOP3):
    d = weekly[weekly["Country/Region"] == c]
    slope, intercept = fits[c]
    ax.scatter(d["week"], d["confirmed"] / 1e6, s=8, alpha=0.5, label="actual")
    ax.plot(d["week"], (slope * d["week"] + intercept) / 1e6, "r-", label="linear fit")
    r2 = reg.loc[reg.country == c, "r2"].values[0]
    ax.set_title(f"{c}  (R2={r2:.3f})"); ax.set_xlabel("week"); ax.set_ylabel("confirmed (M)"); ax.legend()
plt.suptitle("Linear regression fits - cumulative confirmed vs week", y=1.03)
plt.tight_layout(); plt.savefig(FIG_DIR / "fig02_regression_fits.png"); plt.show()""")

code(r"""# Residual diagnostics: if a straight line were adequate, these would look like noise around zero.
fig, axes = plt.subplots(1, 3, figsize=(15, 3.6), sharey=False)
for ax, c in zip(axes, TOP3):
    d = weekly[weekly["Country/Region"] == c]
    ax.axhline(0, color="grey", lw=1, ls="--")
    ax.plot(d["week"], residuals[c] / 1e6, color="#C44E52", lw=1.5)
    r2 = reg.loc[reg.country == c, "r2"].values[0]
    ax.set_title(f"{c} residuals (R2={r2:.3f})"); ax.set_xlabel("week"); ax.set_ylabel("residual (M)")
plt.suptitle("Residuals are S-shaped, not noise - the straight line is systematically wrong", y=1.06)
plt.tight_layout(); plt.savefig(FIG_DIR / "fig06_regression_residuals.png"); plt.show()

# Quantify the structure: how many runs of consecutive same-sign residuals?
for c in TOP3:
    signs = np.sign(residuals[c])
    runs = int(1 + np.sum(signs[1:] != signs[:-1]))
    print(f"{c:8s} sign-changes in residuals: {runs - 1:3d} over {len(signs)} weeks "
          f"(pure noise would give roughly {len(signs) // 2})")""")

# ---------------------------------------------------------------- 4. Clustering
md(r"""## 4. Clustering - K-Means on the most volatile country

A straight line cannot show *when* infections surged - the residuals above prove the line misses the
shape entirely. So for the selected country I cluster its weekly points on `[week, weekly new cases]`
with Spark MLlib **K-Means**, choosing K by the highest silhouette score over a small range. The
clusters group the timeline into **phases** (quiet start, surges, peaks, declines), which validates that
growth was *not* steady but came in waves.""")

code(r"""from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.evaluation import ClusteringEvaluator

fc = weekly[weekly["Country/Region"] == FOCAL][["week", "new_cases"]].reset_index(drop=True)
require(len(fc) > 10, f"Too few weeks ({len(fc)}) to cluster {FOCAL} meaningfully.")

sdf = spark.createDataFrame(fc)
va = VectorAssembler(inputCols=["week", "new_cases"], outputCol="f_raw")
scaler = StandardScaler(inputCol="f_raw", outputCol="features", withMean=True, withStd=True)
prep = scaler.fit(va.transform(sdf)).transform(va.transform(sdf)).cache()

evaluator = ClusteringEvaluator(featuresCol="features", metricName="silhouette")
sil = {}
for k in range(2, 7):
    km = KMeans(k=k, seed=RANDOM_SEED, featuresCol="features").fit(prep)
    sil[k] = evaluator.evaluate(km.transform(prep))
best_k = max(sil, key=sil.get)
print("Silhouette by K:", {k: round(v, 3) for k, v in sil.items()})
print("Best K =", best_k)

km = KMeans(k=best_k, seed=RANDOM_SEED, featuresCol="features").fit(prep)
fc["cluster"] = [int(r["prediction"]) for r in km.transform(prep).select("prediction").collect()]""")

code(r"""# Show the waves: weekly new cases over time, coloured by cluster.
plt.figure(figsize=(11, 5))
sns.scatterplot(data=fc, x="week", y=fc["new_cases"] / 1e3, hue="cluster", palette="tab10", s=40)
plt.plot(fc["week"], fc["new_cases"] / 1e3, color="grey", lw=0.6, alpha=0.6)
plt.xlabel("Week number"); plt.ylabel("Weekly new cases (thousands)")
plt.title(f"{FOCAL}: infection waves revealed by K-Means (K={best_k})")
plt.tight_layout(); plt.savefig(FIG_DIR / "fig03_clusters_waves.png"); plt.show()

# Describe each cluster as a phase, and size the peak against the overall average.
phase = (fc.groupby("cluster").agg(weeks=("week", "count"), wk_lo=("week", "min"),
         wk_hi=("week", "max"), mean_new=("new_cases", "mean")).sort_values("mean_new"))
overall_mean = float(fc["new_cases"].mean())
phase["vs_overall"] = phase["mean_new"] / overall_mean
print(phase.assign(mean_new=phase["mean_new"].map(lambda x: f"{x:,.0f}"),
                   vs_overall=phase["vs_overall"].map(lambda x: f"{x:.1f}x")).to_string())
print(f"\nOverall mean weekly new cases for {FOCAL}: {overall_mean:,.0f}")""")

# ---------------------------------------------------------------- 5. Graph
md(r"""## 5. Graph analytics - the focal country and its non-bordering neighbours

I connect the focal country to a set of **neighbours that do not share borders with each other** and
weight each edge by the **correlation of weekly new cases** between the neighbour and the focal country.
A high correlation means that neighbour's waves move in step with the focal country's.

Correlation on a time series needs care: consecutive weeks are strongly autocorrelated, so the usual
significance test is far too optimistic. I therefore attach a **moving-block bootstrap** 95% interval,
which resamples contiguous 8-week blocks and so preserves the wave structure while estimating how
stable the correlation really is.""")

code(r"""# Plausible non-mutually-bordering neighbour sets for the likely focal countries.
NEIGHBOURS = {
    "US": ["Canada", "Mexico"],
    "India": ["Pakistan", "Nepal", "Sri Lanka"],
    "France": ["Spain", "Germany", "Italy"],
    "Brazil": ["Argentina", "Peru", "Venezuela"],
    "Germany": ["France", "Poland", "Denmark"],
    "United Kingdom": ["France", "Ireland", "Netherlands"],
    "Russia": ["Finland", "Kazakhstan", "Poland"],
}
known = set(weekly["Country/Region"])
require(FOCAL in NEIGHBOURS,
        f"No neighbour set defined for focal country '{FOCAL}'. Add it to the NEIGHBOURS dictionary.")

requested = NEIGHBOURS[FOCAL]
neigh = [n for n in requested if n in known]
missing = [n for n in requested if n not in known]
if missing:
    print(f"Warning: {missing} not present in the dataset under that name - skipped.")
require(len(neigh) > 0, f"None of the configured neighbours for {FOCAL} exist in the dataset.")
print("Focal:", FOCAL, "| neighbours:", neigh)


def weekly_new(country):
    '''Weekly new cases indexed by week, reindexed to the full range so lags align by week.'''
    s = weekly[weekly["Country/Region"] == country].set_index("week")["new_cases"].sort_index()
    return s.reindex(range(1, N_WEEKS + 1))


def block_bootstrap_ci(x, y, n_boot=2000, block=8, seed=RANDOM_SEED):
    '''95% CI for Pearson r using a moving-block bootstrap (preserves autocorrelation).'''
    rng = np.random.default_rng(seed)
    n = len(x)
    if n <= block:
        return (float("nan"), float("nan"))
    n_blocks = int(np.ceil(n / block))
    draws = []
    for _ in range(n_boot):
        starts = rng.integers(0, n - block + 1, n_blocks)
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        xs, ys = x[idx], y[idx]
        if xs.std() > 0 and ys.std() > 0:
            draws.append(np.corrcoef(xs, ys)[0, 1])
    return (float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5)))


focal_s = weekly_new(FOCAL)
edges = []
for n in neigh:
    j = pd.concat([focal_s.rename("f"), weekly_new(n).rename("n")], axis=1).dropna()
    require(len(j) > 2, f"Not enough overlapping weeks between {FOCAL} and {n} to correlate.")
    corr = float(j["f"].corr(j["n"]))
    lo, hi = block_bootstrap_ci(j["f"].to_numpy(), j["n"].to_numpy())
    edges.append({"neighbour": n, "corr": round(corr, 3),
                  "ci_low": round(lo, 3), "ci_high": round(hi, 3), "weeks": len(j)})
edges_df = pd.DataFrame(edges).sort_values("corr", ascending=False)
print(edges_df.to_string(index=False))""")

code(r"""# Draw the graph with geographic positions (Long, Lat); edge width/label = correlation.
G = nx.Graph()
G.add_node(FOCAL)
require(FOCAL in centroid.index, f"No coordinates available for {FOCAL}.")
pos = {FOCAL: (float(centroid.loc[FOCAL, "Long"]), float(centroid.loc[FOCAL, "Lat"]))}
for e in edges:
    n = e["neighbour"]
    if n not in centroid.index:
        print(f"Warning: no coordinates for {n} - omitted from the map.")
        continue
    G.add_edge(FOCAL, n, weight=e["corr"])
    pos[n] = (float(centroid.loc[n, "Long"]), float(centroid.loc[n, "Lat"]))

plt.figure(figsize=(9, 6))
widths = [max(0.5, abs(G[u][v]["weight"]) * 5) for u, v in G.edges()]
nx.draw_networkx_nodes(G, pos, nodelist=[FOCAL], node_color="#DD8452", node_size=1400)
nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if n != FOCAL],
                       node_color="#4C72B0", node_size=900)
nx.draw_networkx_edges(G, pos, width=widths, edge_color="grey")
nx.draw_networkx_labels(G, pos, font_size=9, font_color="white")
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"r={G[u][v]['weight']}" for u, v in G.edges()})
plt.title(f"{FOCAL} and non-bordering neighbours\n(edge = correlation of weekly new cases)")
plt.axis("off"); plt.tight_layout(); plt.savefig(FIG_DIR / "fig04_neighbour_graph.png"); plt.show()""")

# ---------------------------------------------------------------- 6. Lead-lag
md(r"""## 6. Lead-lag analysis - who can actually be warned?

The correlations above are measured at **lag zero**: they compare the focal country and a neighbour in
the *same* week. That answers "do these curves look alike?" but not the question the neighbours actually
care about, which is "**does my wave arrive after theirs, and by how long?**". A neighbour whose curve
moves at the same time as the focal country's gains nothing from watching it - there is no warning
window. Only a neighbour that *follows* can act in advance.

So I recompute the correlation across a range of lags, shifting each neighbour's series against the
focal country's. Writing the focal series as $f_t$ and a neighbour's as $n_t$, I evaluate
$\rho(f_t,\ n_{t+k})$ for $k = -4 \dots +6$ weeks. A peak at **positive** $k$ means the neighbour lags
the focal country by $k$ weeks - that $k$ *is* the warning window. A peak at zero or negative $k$ means
the neighbour moves with, or ahead of, the focal country, and no warning is available.

The decision rule is fixed in advance: a neighbour is issued an early-warning recommendation only if its
best lag is **at least +1 week** and the correlation at that lag is **at least 0.6**.""")

code(r"""LAGS = list(range(-4, 7))
MIN_LAG, MIN_CORR = 1, 0.60          # decision rule, fixed before looking at the results

ll_rows = []
for n in neigh:
    ns = weekly_new(n)
    for lag in LAGS:
        # shift(-lag) aligns focal week t with neighbour week t+lag
        j = pd.concat([focal_s.rename("f"), ns.shift(-lag).rename("n")], axis=1).dropna()
        if len(j) > 10 and j["f"].std() > 0 and j["n"].std() > 0:
            ll_rows.append({"neighbour": n, "lag": lag,
                            "corr": round(float(j["f"].corr(j["n"])), 3), "weeks": len(j)})
require(len(ll_rows) > 0, "Lead-lag analysis produced no valid pairs - check the weekly series.")

ll = pd.DataFrame(ll_rows)
pivot = ll.pivot(index="lag", columns="neighbour", values="corr")
print("corr(focal at week t, neighbour at week t+lag)\n")
print(pivot.to_string())

best = ll.loc[ll.groupby("neighbour")["corr"].idxmax()].reset_index(drop=True)
best["warned"] = (best["lag"] >= MIN_LAG) & (best["corr"] >= MIN_CORR)
print("\nBest lag per neighbour (positive lag = neighbour follows the focal country):")
for _, r in best.iterrows():
    verdict = (f"early warning of ~{int(r['lag'])} week(s)" if r["warned"]
               else "no usable warning window (moves with or ahead of the focal country)")
    print(f"  {r['neighbour']:<10} best lag {int(r['lag']):+d} wk, r = {r['corr']:.3f}  ->  {verdict}")""")

code(r"""# Visualise the full lead-lag profile: where each neighbour's correlation peaks.
plt.figure(figsize=(10, 5))
palette = sns.color_palette("deep", len(neigh))
for colour, n in zip(palette, neigh):
    sub = ll[ll["neighbour"] == n].sort_values("lag")
    plt.plot(sub["lag"], sub["corr"], marker="o", color=colour, label=n, lw=2)
    peak = sub.loc[sub["corr"].idxmax()]
    plt.scatter([peak["lag"]], [peak["corr"]], s=220, facecolors="none", edgecolors=colour, lw=2.5, zorder=5)
    plt.annotate(f"peak {int(peak['lag']):+d} wk\nr={peak['corr']:.3f}",
                 (peak["lag"], peak["corr"]), textcoords="offset points", xytext=(8, 10),
                 fontsize=9, color=colour, fontweight="bold")

# Headroom so the peak labels never collide with the title.
y_lo, y_hi = float(ll["corr"].min()), float(ll["corr"].max())
plt.ylim(y_lo - 0.06, y_hi + 0.16)

plt.axvline(0, color="grey", ls="--", lw=1)
plt.axhline(MIN_CORR, color="#C44E52", ls=":", lw=1)
plt.text(LAGS[0], MIN_CORR + 0.012, f"decision threshold r = {MIN_CORR}", color="#C44E52", fontsize=8)
plt.axvspan(MIN_LAG - 0.5, LAGS[-1] + 0.5, color="green", alpha=0.06)
plt.text((MIN_LAG + LAGS[-1]) / 2, y_lo - 0.02,
         "neighbour follows -> warning possible", ha="center", fontsize=9, color="green")
plt.xlabel(f"Lag k, in weeks  (corr of {FOCAL} at week t vs neighbour at week t+k)")
plt.ylabel("Pearson r of weekly new cases")
plt.title(f"Lead-lag profile: which neighbours follow {FOCAL}, and by how long")
plt.legend(title="neighbour"); plt.tight_layout()
plt.savefig(FIG_DIR / "fig07_lead_lag.png"); plt.show()""")

# ---------------------------------------------------------------- 7. Visualisation
md(r"""## 7. Visualisation - the story in one frame

A single storytelling panel: the focal country's waves (with clusters), how strongly each neighbour's
curve correlates at lag zero, and the lead-lag profile that turns that correlation into an actual
warning window - the line from raw data to a recommendation.""")

code(r"""fig, ax = plt.subplots(1, 3, figsize=(18, 4.8))

sns.scatterplot(data=fc, x="week", y=fc["new_cases"] / 1e3, hue="cluster", palette="tab10",
                s=30, ax=ax[0], legend=False)
ax[0].plot(fc["week"], fc["new_cases"] / 1e3, color="grey", lw=0.6, alpha=0.6)
ax[0].set_title(f"1. {FOCAL}: waves (K-Means phases)"); ax[0].set_xlabel("week")
ax[0].set_ylabel("weekly new (k)")

sns.barplot(data=edges_df, x="corr", y="neighbour", hue="neighbour", palette="crest",
            legend=False, ax=ax[1])
ax[1].set_title("2. Same-week correlation"); ax[1].set_xlabel("Pearson r (lag 0)"); ax[1].set_ylabel("")

for colour, n in zip(palette, neigh):
    sub = ll[ll["neighbour"] == n].sort_values("lag")
    ax[2].plot(sub["lag"], sub["corr"], marker="o", color=colour, label=n, lw=2)
    peak = sub.loc[sub["corr"].idxmax()]
    ax[2].scatter([peak["lag"]], [peak["corr"]], s=180, facecolors="none", edgecolors=colour, lw=2.5)
ax[2].axvline(0, color="grey", ls="--", lw=1)
ax[2].axvspan(MIN_LAG - 0.5, LAGS[-1] + 0.5, color="green", alpha=0.06)
ax[2].set_title("3. Lead-lag: who gets a warning"); ax[2].set_xlabel("lag k (weeks)")
ax[2].set_ylabel("Pearson r"); ax[2].legend(fontsize=8)

plt.suptitle("From raw cases to a neighbour early-warning recommendation", y=1.03)
plt.tight_layout(); plt.savefig(FIG_DIR / "fig05_story_panel.png"); plt.show()""")

# ---------------------------------------------------------------- 8. Persist
code(r"""peak_phase = phase.iloc[-1]
metrics = {
    "total_weeks": N_WEEKS,
    "reporting_corrections": corrections,
    "top3": [{"country": c, "total_confirmed": int(totals[c])} for c in TOP3],
    "regression": reg.to_dict(orient="records"),
    "focal_country": FOCAL,
    "clustering": {
        "best_k": int(best_k),
        "silhouette": {int(k): round(v, 3) for k, v in sil.items()},
        "phases": phase.reset_index().to_dict(orient="records"),
        "overall_mean_new": round(overall_mean, 1),
        "peak_vs_overall": round(float(peak_phase["vs_overall"]), 2),
    },
    "graph": {"neighbours": edges_df.to_dict(orient="records")},
    "lead_lag": {
        "lags_tested": [int(x) for x in LAGS],
        "decision_rule": {"min_lag_weeks": MIN_LAG, "min_corr": MIN_CORR},
        "profile": ll.to_dict(orient="records"),
        "best": best.to_dict(orient="records"),
    },
}
(OUT_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2, default=str))
print(json.dumps(metrics["lead_lag"]["best"], indent=2, default=str))
print(f"\nPeak phase runs at {metrics['clustering']['peak_vs_overall']}x the overall weekly average.")
print("metrics.json written to", OUT_DIR / "metrics.json")""")

md(r"""## 8. Conclusion and recommendation

The three worst-hit countries grew at very different rates, and for all of them a straight line is a
poor description: R-squared looks high only because the series rises monotonically, while the residuals
curve systematically. K-Means separates the focal country's timeline into distinct phases and isolates a
single mega-surge cluster running several times the overall weekly average - clear evidence that growth
came in waves rather than at a steady rate.

The decisive result is the lead-lag analysis. Measured in the same week, both neighbours look
correlated with the focal country, and the more strongly correlated one looks like the obvious candidate
for an early-warning arrangement. Shifting the series shows that this reading is wrong: the
strongest same-week correlate peaks at a *negative* lag, meaning it moves with or slightly ahead of the
focal country and therefore gains no advance notice. The neighbour that looked weaker at lag zero is the
one whose correlation *rises* when shifted forward, and that neighbour has a genuine multi-week warning
window.

The practical recommendation follows the measured lag, not the headline correlation: the following
neighbour should treat the focal country's surge phases as a leading indicator and pre-position testing
and hospital capacity by the number of weeks its own peak lags behind, while the synchronous neighbour
should invest in its own surveillance instead, because by the time the focal country's numbers rise, its
own are already rising. Capacity in both cases should be planned against the mega-surge phase rather
than the average week. The full decision narrative is delivered in the video presentation.""")

# ---------------------------------------------------------------- 9. Limitations
md(r"""## 9. Limitations

- **Reporting, not infection.** The series counts *confirmed* cases, so it measures testing capacity and
  reporting policy as much as transmission. Cross-country comparisons inherit those differences.
- **Cumulative source data.** Weekly new cases are derived by differencing a running total; retrospective
  corrections appear as negative differences and are clipped to zero, which slightly flattens the series.
- **The series ends 9 March 2023.** Johns Hopkins stopped updating, so nothing after that date is covered.
- **`week` is a clustering input.** Because time is a feature, the K-Means phases are partly temporal by
  construction; they should be read as "periods that behave alike", not as a purely behavioural grouping.
- **Geography is a stand-in for mobility.** Neighbours are chosen by shared land borders, whereas
  transmission follows air travel and trade. A mobility-weighted graph would be a better model.
- **Correlation is not causation.** A lagged correlation shows that two curves move together with an
  offset; it does not establish that one caused the other. Both may follow a common driver such as a
  new variant arriving in the region.
- **One lag per pair, fixed over three years.** The estimated lag is an average across the whole period.
  Variant waves travelled at different speeds, so a time-varying lag would be more faithful.""")

# ---------------------------------------------------------------- Integrity
md(r"""## Academic Integrity Declaration

I declare that except where referenced, the work I am submitting for this assessment task is my own
work. I have read and am aware of the Academic Integrity Policy and Procedure of Torrens University
Australia. I am also aware that I need to keep a copy of all submitted material and any drafts, and I
agree to do so.

## Statement of Acknowledgement

I acknowledge that I have used the following AI tool in the creation of this assessment:

- Anthropic Claude (Opus 4.8)

The tool was used to assist with scaffolding the PySpark analysis pipeline, debugging Spark session and
MLlib errors, reasoning about the statistical treatment of autocorrelated time series, improving code
documentation and academic clarity, and supporting APA 7th referencing conventions.

Prompt examples:

1. "My K-Means clusters on `[week, weekly new cases]` come back as contiguous week ranges. Is that a
   real finding or an artefact of using `week` as a feature, and how should I describe the limitation?"
2. "I am correlating two COVID weekly-new-case series. Consecutive weeks are autocorrelated, so an
   ordinary significance test will be too optimistic. What resampling scheme preserves the wave
   structure, and how do I implement it with numpy only?"
3. "My neighbour recommendation is based on same-week correlation. How do I test whether a neighbour
   actually *follows* the focal country, and how should the result change the recommendation if the
   most correlated neighbour turns out to lead rather than lag?"

I confirm that the use of this AI tool has been in accordance with the Torrens University Australia
Academic Integrity Policy and TUA, Think and MDS's Position Paper on the Use of AI. I confirm that the
final output is authored by me and represents my own critical thinking, analysis and synthesis of
sources. I take full responsibility for the final content of this assessment.

## References

Humdata.org. (2020). *Novel Coronavirus (COVID-19) cases data*. https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases

Apache Spark. (2024). *MLlib: Clustering and regression*. https://spark.apache.org/docs/latest/ml-guide.html

Han, J., Kamber, M., & Pei, J. (2011). *Data mining: Concepts and techniques* (3rd ed.). Morgan Kaufmann.""")

# ---------------------------------------------------------------- Glossary
md(r"""## Appendix A - Glossary

| Term | Meaning in this assessment |
|---|---|
| Cumulative confirmed | Running total of confirmed cases; never decreases except for reporting corrections |
| Weekly new cases | First difference of the cumulative series, floored at zero |
| Week number | Weeks since 22 Jan 2020, so Week 1 = 22-28 Jan 2020 |
| Linear regression | Straight-line model of cumulative cases against week number |
| R-squared | Share of variance explained by the line; misleading on a monotonic series, since almost any rising line scores well |
| RMSE | Typical size of the model's error, in cases; unlike R-squared it stays on the original scale |
| Residual | Actual minus predicted; structure in residuals means the model shape is wrong |
| Volatility | Variance of *weekly new cases*, used to pick the focal country; the variance of the cumulative total would just rank countries by size |
| K-Means | Clustering that assigns each week to the nearest of K centres |
| Silhouette score | Cluster-separation measure in [-1, 1]; used here to choose K |
| Phase | A cluster read as a period of the pandemic (quiet, rising, mega-surge) |
| Standardisation | Rescaling features to mean 0 and standard deviation 1 so week number and case counts contribute comparably |
| Graph / edge weight | Countries are nodes; each edge carries the correlation between the two weekly new-case series |
| Pearson r | Linear correlation between two series, from -1 to +1 |
| Moving-block bootstrap | Resampling contiguous blocks of weeks to get a confidence interval that respects autocorrelation |
| Autocorrelation | A series being correlated with its own recent past, which makes ordinary significance tests too optimistic |
| Lag k | Offset in weeks when comparing two series; positive k means the neighbour follows the focal country |
| Lead-lag profile | Correlation plotted across a range of lags; its peak locates the offset at which two curves align best |
| Warning window | The positive lag at which a neighbour's correlation peaks - how far ahead it could act |
| Non-bordering neighbours | Neighbours of the focal country that do not share borders with each other, as the brief requires |""")

md(r"""## Appendix B - Analytical decision log

Every choice that could reasonably have gone another way, with the evidence that settled it. The rules
were fixed *before* the results were inspected, so the analysis cannot be accused of being tuned to a
preferred conclusion.

| # | Decision | Options considered | Rule applied | Outcome |
|---|---|---|---|---|
| 1 | Weekly aggregation | Sum daily new cases, or take the weekly maximum of the cumulative series | The source is cumulative and non-decreasing, so the weekly maximum is the week-ending total by definition | Weekly max of cumulative, then first difference for new cases |
| 2 | Reporting corrections | Keep negative differences, or floor at zero | Negative "new cases" are not physically meaningful; they are retrospective corrections | Clipped to zero, and the count of affected country-weeks is reported |
| 3 | Which country to carry forward | Variance of the cumulative total, or variance of weekly new cases | The brief asks for the highest-variance model; variance of a cumulative series scales with country size, so it would just select the largest country by construction | Ranked on weekly new cases - a genuine volatility measure, and the same signal the clustering uses |
| 4 | Choice of K | Fix K in advance, or search a range | Select the K with the highest silhouette score over K = 2..6 | Chosen by silhouette, reported for every K tested |
| 5 | Clustering features | `[new_cases]` alone, or `[week, new_cases]` | The brief asks for the trend *over a period*, which requires time in the feature space | `[week, new_cases]`, standardised - with the resulting temporal circularity disclosed in Section 9 |
| 6 | Neighbour selection | Nearest by centroid distance, or named land borders that do not touch each other | The brief requires neighbours that do not share borders with each other, which centroid distance cannot guarantee | Explicit curated sets, validated against the country names actually present in the data |
| 7 | Correlation uncertainty | Ordinary p-value, or a resampling interval | Weekly series are strongly autocorrelated, so an ordinary test overstates significance | Moving-block bootstrap (8-week blocks, 2,000 draws) reported as a 95% interval |
| 8 | Early-warning recommendation | Recommend on same-week correlation, or on the lag at which correlation peaks | A neighbour only gains warning if it *follows*; the rule was set in advance at lag >= +1 week and r >= 0.60 | Recommendation follows the measured lag, which reverses the ranking that lag-zero correlation suggested |

## Appendix C - Reproducibility and environment

The notebook is deterministic: the same input file produces the same figures and the same
`metrics.json` on every run.

| Item | Value |
|---|---|
| Language | Python 3.11 |
| Spark | `pyspark==3.5.3`, local mode (`local[*]`), Java 8 or 11 |
| Other packages | pandas, numpy, matplotlib, seaborn, networkx |
| Random seed | `RANDOM_SEED = 42`, applied to numpy, K-Means and the bootstrap |
| Configuration required | None - `JAVA_HOME` is auto-detected and all paths resolve relative to the notebook |
| Runtime | Approximately 1-2 minutes end to end |

**Sources of determinism.** K-Means is seeded, so cluster labels and the silhouette scores are stable.
The moving-block bootstrap draws from a seeded `numpy` generator, so the confidence intervals reproduce
exactly. Spark's linear regression solves a closed-form least-squares problem on a single feature, so it
has no stochastic component.

**Generated artefacts.** Running the notebook writes `outputs/metrics.json` plus seven figures:

| File | Content |
|---|---|
| `fig01_top3_cumulative.png` | Cumulative curves of the three worst-hit countries |
| `fig02_regression_fits.png` | Linear fits per country with R-squared |
| `fig03_clusters_waves.png` | K-Means phases on the focal country's weekly new cases |
| `fig04_neighbour_graph.png` | Geographic graph, edges weighted by correlation |
| `fig05_story_panel.png` | Three-panel summary: waves, same-week correlation, lead-lag |
| `fig06_regression_residuals.png` | Residual diagnostics showing the linear model's structural error |
| `fig07_lead_lag.png` | Lead-lag correlation profile with each neighbour's peak marked |

**Error handling.** Environment and data problems raise `SetupError` with a message naming the cause and
the fix, rather than surfacing a raw traceback: missing or malformed dataset, absent Java installation,
Spark start-up failure, an unconfigured focal country, a neighbour absent from the data, missing
coordinates, and series too short to model or correlate. Non-fatal issues (a neighbour missing from the
dataset, or missing map coordinates) emit a warning and continue with the remaining countries.""")

code(r"""spark.stop(); print("Spark stopped.")""")

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3.11 (BDA Spark)", "language": "python", "name": "bda-spark"},
    "language_info": {"name": "python"},
}
out = Path(__file__).parent / "BDA601FariaLuis_Assessment3.ipynb"
nbf.write(nb, str(out))
print("wrote", out, "with", len(cells), "cells")
