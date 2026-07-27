# MLN601 Assessment 3 - plan for v3 (revision 4)

Status: draft for review, nothing implemented yet.
Base: `notebook/MLN601FariaLuisBrief3v2.ipynb` (46 cells, executed).
Target: `notebook/MLN601FariaLuisBrief3v3.ipynb` + `submission/MLN601FariaLuisBrief3.{ipynb,pdf,txt}`.
Due: 19/08/2026. Weight 40%. Issue #189.

> **Revision history.** Draft 1 proposed a forecast gate that a naive rule beats, and bet on a
> trend feature that makes forecasts worse. Both were tested and both were wrong. Revision 2
> fixed those with measured evidence but still described 2012 as an untouched holdout opened
> once, which is false. Revision 3 corrects that framing and separates benchmarking from
> operational approval. Revision 4 adds the hourly-file evidence on the `hum = 0` day, and
> corrects a proposed guardrail that would have broken every temporal fold.

## Framing statement for the report

> The v3 is a retrospective methodological correction of the v2. Protocol A reproduces the
> conventional random-split benchmark the brief asks for. Protocol B evaluates rolling
> day-ahead forecasting with causal autoregressive inputs and temporal model selection.
> Because 2012 informed the redesign, its results are **confirmation evidence rather than a
> pristine blind test**. Operational approval depends only on whether a learned model
> materially outperforms the strongest naive day-ahead baseline.

## Verified facts, measured before planning

All figures below were computed directly from `dataset/day.csv` (731 rows, 2011-01-01 to
2012-12-31), not taken from the v2 narrative.

**Naive temporal baselines, scored on 2012:**

| Baseline | MAE | R2 |
|---|---|---|
| Rolling 7-day mean (shifted) | 847.8 | 0.565 |
| Previous day (lag 1) | 870.2 | 0.513 |
| Same day last week (lag 7) | 1110.4 | 0.235 |
| 2011 mean, constant | 2488.7 | -1.509 |

**Tuned v2 models on the same 2012 target, trained on 2011:**

| Model | MAE | R2 |
|---|---|---|
| Gradient Boosting | 2024.2 | -0.503 |
| Random Forest | 2034.4 | -0.511 |
| Linear Regression | 2121.8 | -0.656 |

Every current model loses to the rolling 7-day mean by a factor of more than two.

**Trend feature smoke test** (`days_since_start` added, same hyperparameters, train 2011,
test 2012):

| Model | MAE without trend | MAE with trend |
|---|---|---|
| Linear Regression | 2121.8 | 3637.8 |
| Random Forest | 2034.4 | 2162.9 |
| Gradient Boosting | 2024.2 | 2377.0 |

The trend feature makes every model worse. Trees do not extrapolate simply because they are
given a clock, and one year of history cannot separate trend from seasonality. It stays as an
ablation hypothesis, not as a fix.

**Data quality facts, measured:**

- `weathersit` counts: 1 clear = 463, 2 mist = 247, 3 light rain/snow = 21, **4 heavy
  rain/snow = zero rows**. Category 4 is absent from the dataset entirely.
- IQR outliers: `cnt` = 0, `temp` = 0, `atemp` = 0, `hum` = 2, `windspeed` = 13. The target has
  no IQR outliers.
- **`hum = 0` occurs on exactly one row: 2011-03-10, which has `weathersit = 3`, light
  rain/snow.** Zero humidity on a rain day is physically impossible, and the next lowest
  humidity in the dataset is 0.188. `windspeed` has no zero rows.
- **Hourly-file corroboration for that day**, checked in `dataset/hour.csv`: 2011-03-10 has
  only **22 hourly rows instead of 24** (hours 3 and 4 are absent from the file entirely),
  **all 22 carry `hum = 0`**, and 20 of them are `weathersit = 3`. It is also the **only date
  in the entire hourly dataset with any `hum = 0` row**. Missing hours plus a physically
  impossible reading, isolated to one date, points to a sensor or logging failure that day
  rather than an aggregation artefact in `day.csv`. Describe it as a *suspected missing or
  faulty measurement*, since the underlying cause is not documented anywhere in the dataset
  README.
- Growth: 2011 mean 3,406 vs 2012 mean 5,600, a 64.4% increase. 2011 maximum 6,043, 2012
  maximum 8,714, and **175 of 366 days in 2012 (48%) sit above the entire 2011 ceiling**.
- **Encoding collision, verified:** with `OneHotEncoder(drop="first", handle_unknown="ignore")`
  fitted on categories [1, 2, 3], `weathersit = 1` (clear) encodes as `[0, 0]` and an unseen
  `weathersit = 4` (heavy rain/snow) also encodes as `[0, 0]`. They are identical. In
  production the model would read a blizzard as perfect weather. This needs a guardrail, not
  just a footnote.
- **The obvious guardrail does not work, verified.** Switching to
  `handle_unknown="error"` breaks the temporal protocol entirely. Under `TimeSeriesSplit` on a
  single year, the validation block always contains calendar categories the training block has
  never seen, because time-ordered slicing is exactly what produces that. Measured on 2011:

  | Split | Fold | Training window | Categories unseen in validation |
  |---|---|---|---|
  | n_splits=5 | 0 | Jan 1 - Mar 6 (65 rows) | `mnth` [4, 5], `season` [2] |
  | n_splits=5 | 1 | Jan 1 - May 5 (125 rows) | `mnth` [6, 7], `season` [3] |
  | n_splits=5 | 4 | Jan 1 - Nov 1 (305 rows) | `mnth` [12] |
  | n_splits=3 | 0 | Jan 1 - Apr 2 (92 rows) | `mnth` [5, 6, 7], `season` [3] |

  Every fold, in both configurations. `handle_unknown="error"` would raise on all of them and
  the grid search would never complete. The correct architecture separates the two concerns:
  keep `handle_unknown="ignore"` inside the pipeline because it is structurally required, and
  put the out-of-domain guard **outside the pipeline** as an explicit input-validation step
  before scoring. The model should not learn to handle category 4; it should refuse to answer.
- **Fold composition is itself a limitation.** With `n_splits=5`, fold 0 trains on 65 days,
  all of them winter. A validation fold whose training window contains one season cannot
  validate seasonal behaviour. This constrains the choice of `n_splits` and must be reported
  rather than hidden.

## Known defect in v2 that must be fixed

The v2 "time-ordered forecasting check" is not honest yet. Cell 27 runs `GridSearchCV` on the
random 75/25 training set, which contains both 2011 and 2012 days. Cell 36 then calls
`clone(model).fit(X_2011, y_2011)`. `clone` preserves the chosen hyperparameters and only
resets the fitted state, so **2012 data influenced the configuration used in the supposedly
unseen temporal test**. The v3 gives the temporal protocol its own selection loop.

## Status of the 2012 data: confirmation, not blind test

This must be stated plainly in the notebook rather than glossed over. 2012 has already been
used during v2 development to:

- score every model in the v2 temporal check,
- discover that the rolling 7-day mean is the strongest naive baseline,
- test and reject `days_since_start`,
- set the 5% margin in the v3 gate,
- shape the expected narrative.

None of that can be undone, and with only two years of data there is no untouched slice left to
hold back. The honest wording for the notebook:

> 2012 is a retrospective temporal benchmark already examined during v2 development, not a
> pristine unseen holdout. Its role in v3 is confirmation of a corrected methodology.

Do not write "opened once", "blind test" or "never seen" anywhere about 2012. The gates in the
next section are therefore **predeclared for the v3 confirmation study following exploratory
analysis in v2**, which is a weaker but truthful claim.

## Success criteria

**Protocol A, interpolation (random 75/25):** an academic benchmark reproducing the
conventional approach the brief asks for.
- Must beat the mean baseline (MAE 1,663) by at least 40%.
- Report MAE normalised against mean daily demand (~4,500) so the error is interpretable
  without inventing a business tolerance.
- **Protocol A names a benchmark winner but grants no operational approval.** The rubric asks
  which model performs best, so a winner is named; a random split cannot support a claim about
  forecasting tomorrow, so it cannot approve anything for deployment.

**Protocol B, day-ahead forecasting (temporal):** the sole basis for operational approval.
- Adversary is the **strongest naive day-ahead baseline**, currently the rolling 7-day mean.
- Explicit thresholds: **MAE <= 847.8 x 0.95 = 805.4** and **R-squared > 0.565**.
- A model that cannot materially beat the strongest naive baseline is not approved as a
  forecaster, regardless of how well it scores on Protocol A.

**What each protocol is permitted to conclude**, so the report never approves a deployment on
the strength of a split it has just called dishonest:

| Protocol | Permitted outcome |
|---|---|
| A, random interpolation | Benchmark winner named. Not operationally approved. |
| B, temporal day-ahead | Operational approval decision: approved, conditionally approved, or rejected. |

**Declared tie-break:** when two models are within 5% on the primary metric, prefer the lower
RMSE (fewer catastrophic days); if still tied, prefer the simpler and more interpretable model.
Random Forest and Gradient Boosting are already effectively tied on Protocol A, so this rule
will be used.

**Metrics reported:** MAE (primary, the brief's metric), plus MSE, RMSE and R-squared, since
the rubric mentions MSE and R-squared.

## Decision rules, written before the experiment

The conclusion is **not** pre-written this time. Protocol B resolves to exactly one of these,
determined by the measured numbers:

| Condition | Verdict |
|---|---|
| ML beats best naive MAE by >= 5% and R2 > 0.565 | Approve with conditions for day-ahead use |
| ML beats naive but by < 5% | No material improvement over naive; naive retained on simplicity |
| ML MAE higher than best naive | Naive baseline wins; reject ML for forecasting |
| ML fails to beat even the constant mean | Reject ML forecasting outright |

Note the distinction between rows 2 and 3. If a model scores MAE 830 against the naive 847.8,
the correct statement is "the improvement is not material", **not** "the naive rule wins".

## Decisions taken (flagged for Luis to overrule)

**Forecast horizon: rolling day-ahead, decided.** The brief asks to predict demand "for a given
day and weather forecast", and the operationally realistic question is what tomorrow looks
like, with yesterday's counts already known. This is what makes autoregressive features and
baselines legitimate. Under an "forecast all of 2012 on 1 January" horizon they would be
invalid. The horizon must be stated explicitly in section 1.

**Use case: system-wide daily rental demand, not station rebalancing.** The dataset is a daily
aggregate for the whole system, with no station, location, inventory or availability columns.
It supports demand planning, staffing, fleet sizing and maintenance scheduling.

**Personal grounding, allowed with limits.** Luis is a daily bike-share user (Lime) for commute
and errands, which legitimately motivates the question of why daily demand varies. Constraints:
declare Lime as a contemporary dockless analogue rather than the same docked system; keep the
perspective rider-side; and do **not** claim `registered` means commuter and `casual` means
leisure, since those are membership categories, not trip purposes. Correct phrasing: *"the
observed patterns are consistent with commuter-oriented registered usage and more
weather-sensitive casual usage."* Personal experience motivates the question, the EDA supports
the conclusion.

## Section-by-section plan

### Section 1 - Business Understanding

- Frame the problem as **next-day, system-wide rental demand**, with the Lime-grounded
  rationale, phrased within the limits above.
- State the forecast horizon explicitly.
- Declare both protocols up front, with what each can and cannot support: A is a benchmark, B
  is the approval basis.
- Declare the success criteria, the decision rules and the tie-break, and label them as
  predeclared for the v3 confirmation study following v2 exploration.
- **Assumptions and limitations**, stated here rather than buried: the dataset contains
  *observed* weather, not weather *forecasts*, so Protocol B assumes a perfect weather forecast
  and is optimistic relative to production. Only two years of history exist. Severe weather
  (category 4) is entirely absent. 2012 is confirmation evidence, not a blind holdout.

### Section 2 - Data Understanding

Keep every existing EDA plot. Add:

- Table 2.1 - **data quality audit**: schema and dtypes, row count 731 against the expected
  daily span, missing values, duplicate rows, the identity `casual + registered == cnt`, date
  continuity with no gaps, normalised columns within [0, 1], and the `weathersit` category
  distribution. Columns: check, result, pass or fail, action taken.
- Table 2.2 - **outlier and plausibility review**, with three distinct verdict types rather
  than one:
  1. *statistical outlier* (e.g. the 13 `windspeed` values beyond 1.5 IQR),
  2. *physically implausible or potentially miscoded* (the `hum = 0` row on a rain day),
  3. *action*: retain with caveat, sensitivity test, or documented correction.
  For `hum = 0` specifically, the audit verdict is **fail, corrected before modelling**, not
  "outlier retained". Treatment:

```python
df.loc[df["hum"] == 0, "hum"] = np.nan          # one row, 2011-03-10
# SimpleImputer(strategy="median") inside the Pipeline, fitted per training fold
```

  Median imputation inside the pipeline, never a global fill, so the imputer is fitted only on
  each training fold. Do **not** interpolate between neighbouring days: on the day-ahead
  contract that would pull the following day's value backwards into the feature row. Report a
  sensitivity check (results with the row imputed versus with the row dropped). One row in 731
  will almost certainly change nothing, and demonstrating that is the point. Cite the hourly
  corroboration from the verified-facts section.
- An explicit note that `weathersit = 4` has zero rows, and that supported input is categories
  1 to 3 only.
- Number every table and figure (`Table 2.1`, `Figure 2.3`) with a printed caption and a
  one-line "so what" underneath, following the Assessment 2 v8 convention.

### Section 3 - Data Preparation

Keep the leakage-safe `ColumnTransformer` inside each pipeline. Organise features into **four**
declared groups, each with its own independent ablation so that an interaction and a trend are
never adopted or rejected as a single bundled decision:

1. **Core**: the existing calendar and weather features.
2. **Context interactions**: `atemp_humidity_interaction` (renamed from the inaccurate
   `heat_index`, since inputs are normalised and `atemp` is already a feels-like measure) and
   `temp_squared`, which captures the "too hot is also bad" curvature the EDA hints at.
3. **Trend**: `days_since_start`. Smoke-tested and expected to fail; reporting a measured
   negative is the point.
4. **Autoregressive, day-ahead only**: the causal formulas, exactly:

```python
df = df.sort_values("dteday").reset_index(drop=True)   # order before any feature work
df["lag_1_cnt"]  = df["cnt"].shift(1)
df["lag_7_cnt"]  = df["cnt"].shift(7)
df["roll_7_cnt"] = df["cnt"].shift(1).rolling(7).mean()   # shift THEN roll
```

The `shift(1)` before `rolling(7)` is what makes the rolling mean causal: Tuesday's feature may
use Monday's actual count only because the operating contract is rolling day-ahead, where
yesterday's totals are known by the time tomorrow is forecast. State this contract explicitly.

**Guardrails to implement and assert, not just describe:**
- dates sorted before any feature construction, never shuffled in Protocol B,
- assertions that no feature row contains same-day or future information,
- the first seven rows (incomplete lag window) dropped identically for **every** temporal
  candidate, including the naive baselines,
- all models and baselines scored on exactly the same set of dates, verified by assertion,
- `TimeSeriesSplit` fold boundaries printed: train start, train end, validation start,
  validation end, and row counts for each fold.

**Severe-weather guardrail, as abstention rather than encoding.** `weathersit = 4` encodes
identically to `weathersit = 1` under the current encoder, so a blizzard reads as clear
weather. Two things are true and both matter: `handle_unknown="error"` cannot be used, because
it breaks every temporal fold (measured, see verified facts), and simply adding an explicit
category-4 column would not help either, since the model has never seen that column active
during training and has no basis for a prediction. The answer is refusal, implemented outside
the pipeline:

```python
SUPPORTED_WEATHERSIT = {1, 2, 3}   # measured support of the training data

def guarded_predict(model, X):
    if not set(X["weathersit"]).issubset(SUPPORTED_WEATHERSIT):
        raise OutOfDomainError("weathersit outside trained support; escalate to human review")
    return model.predict(X)
```

Keep `handle_unknown="ignore"` inside the pipeline where it is structurally required. Document
in the approval table and the deployment sketch that the model is validated for weather
categories 1 to 3 only, and that severe weather must trigger an out-of-distribution warning
with a conservative fallback or human review, never an automatic score.

**Ablation threshold declared before running:** a feature group is adopted only if it improves
that protocol's primary metric by at least 3% relative, measured on that protocol's own
training cross-validation. Run per group and per protocol. Report every result, negatives
included.

### Section 4 - Modelling, two protocols with separate selection

**Protocol A - interpolation benchmark.** Random 75/25 split, with the cross-validator stated
explicitly rather than inherited by accident:

```python
KFold(n_splits=5, shuffle=True, random_state=42)
```

Scored on negative MAE. Baseline: mean.

**Protocol B - day-ahead forecasting.** Selection happens **inside 2011 only**:

```
2011 only -> TimeSeriesSplit -> GridSearchCV -> freeze hyperparameters
2012 only -> confirmation evaluation (retrospective benchmark, not a blind holdout)
```

With roughly 365 training days, the `TimeSeriesSplit` windows need deliberate choice. Measured:
at `n_splits=5` the first fold trains on 65 days, all winter, which cannot validate seasonal
behaviour; at `n_splits=3` the first fold trains on 92 days, still winter and early spring.
There is no configuration that fixes this with one year of data, so pick the setting, print
every fold's date range and row count, and report the limitation rather than hide it. This is
also the reason `handle_unknown="ignore"` must stay in the encoder.

Baselines for Protocol B: lag 1, lag 7 and shifted rolling 7-day mean, all scored on the same
2012 dates as the models.

Also document the tuning history the brief asks for: the grid searched, the values selected,
and one line on why each grid was bounded that way.

Outputs:
- Table 4.1 - full results matrix: models plus baselines, both protocols, MAE / MSE / RMSE /
  R-squared.
- Table 4.2 - **protocol MAE comparison** (not "degradation ratio", which would imply a causal
  comparison between protocols that use different features and different distributions).
- Figure 4.1 - grouped bar chart of MAE by model and protocol, with the naive baselines drawn
  as reference lines.

### Section 5 - Evaluation

- Table 5.1 - **gate application**, each model against each declared criterion, per protocol,
  pass or fail.
- Predicted-versus-actual and residual plots, numbered.
- Keep the 2012 ceiling plot from v2: it concretely shows why trees cannot extrapolate, with
  48% of 2012 days above anything seen in training.
- **Explainability chosen by winner**: `TreeExplainer` if an ensemble is the subject,
  `LinearExplainer` if Linear Regression is. Global beeswarm plus a local waterfall for one
  high-demand day and one badly-missed day. Keep sklearn's `feature_importances_` as a
  secondary chart and state why SHAP is preferred, that impurity importance is biased towards
  continuous and high-cardinality features. If no model passes the Protocol B gate, explain
  only the Protocol A benchmark winner and do not present it as an approved forecaster.
- Table 5.2 - **approval table**, decided **separately per use case**: one verdict for the
  interpolation benchmark (winner named, no operational approval) and one for day-ahead
  forecasting (approval or rejection per the decision rules above). Each row: model, protocol,
  verdict, reason, intended use. Use the permitted-outcome wording: Protocol A rows read
  "selected as benchmark winner, not operationally approved"; only Protocol B rows carry
  approved, conditionally approved or rejected. Every approval row must also record the
  supported input domain (weather categories 1 to 3).

### Section 6 - Deployment and lessons

Write only once the numbers are in, following whichever decision rule fired. Include as
deployment requirements regardless of outcome:

- out-of-domain weather detection with fallback, given the category 4 encoding collision,
- MAE drift monitoring,
- the multi-year history needed before any trend or extrapolation claim is credible,
- the gap between observed weather and forecast weather, which this study cannot measure.

Keep the honest-evaluation lesson and connect it back to Assessment 2: declaring criteria
before looking at results is what makes a negative result publishable rather than embarrassing.

### Appendices and closing

- Appendix A - glossary of metrics and terms.
- Appendix B - proposed operational deployment sketch, in the Assessment 2 style.
- Reproducibility cell printing Python and library versions plus the random seed.
- Update the Statement of Acknowledgement with the tools actually used for v3 and check the
  model names are current.

## Compliance notes

**Word count.** The brief specifies 2,000 words +/- 10%, so 1,800 to 2,200. Dr Kamran's verbal
flexibility on Assessment 2 does not automatically transfer. Also note the brief does **not**
say appendices are excluded from the count, so moving text into an appendix may not remove it
from the total. Recommendation: keep the whole document near the range rather than relying on
an exclusion that is not written down.

**PDF export route: accepted deviation, closed, not a pending item.** The brief says "direct
PDF download via LaTeX from the Notebook", while the pipeline used on Assessments 1 and 2 is
HTML plus headless Chrome. Assessment 1 scored 20/20, High Distinction, on the Deliverables
criterion using that pipeline, with the marker explicitly noting the notebook runs without
errors and matches the PDF. Recorded position: the HTML/Chrome export is an accepted formatting
deviation, and the v3 notebook, PDF and text export will be verified against the same executed
source.

## Deliverables

- `submission/MLN601FariaLuisBrief3.ipynb`
- `submission/MLN601FariaLuisBrief3.pdf`
- `submission/MLN601FariaLuisBrief3.txt` (source code)

Same export pipeline as Assessments 1 and 2. Verify no table is cut across pages.

## Order of work

1. Confirm the decisions above, especially the day-ahead horizon and the word-count position.
2. Copy v2 to v3. Add the quality audit, the numbering convention, the limitations block and
   the 2012-is-confirmation framing.
3. Build the four feature groups and the per-group, per-protocol ablation harness, with the
   causal-lag assertions in place before anything is measured.
4. Implement Protocol B correctly: `TimeSeriesSplit` selection inside 2011 with printed folds,
   confirmation evaluation on 2012, naive baselines on identical dates.
5. Run everything, apply the gates, and let the decision rules pick the verdict.
6. Add SHAP for whichever model the verdict makes relevant, plus the approval table.
7. Write sections 1 and 6 to match what actually happened.
8. Clean run from a fresh kernel, then export the submission package.

## Open questions for Luis

- Day-ahead horizon confirmed? Everything autoregressive depends on it.
- Word count: hold the whole document to roughly 2,000, or take the risk on Kamran's stated
  preference for longer text?
- If the decision rules land on "naive wins" or "no material improvement", are you comfortable
  submitting that as the headline conclusion? It is the strongest and most honest result
  available, but it is a bolder report than "Random Forest achieved R-squared 0.88".
