# MLN601 Assessment 3 - plan for v3 (revision 2)

Status: draft for review, nothing implemented yet.
Base: `notebook/MLN601FariaLuisBrief3v2.ipynb` (46 cells, executed).
Target: `notebook/MLN601FariaLuisBrief3v3.ipynb` + `submission/MLN601FariaLuisBrief3.{ipynb,pdf,txt}`.
Due: 19/08/2026. Weight 40%. Issue #189.

> Revision 2 replaces the first draft of this plan. The first draft proposed a forecast gate
> that a naive rule beats, and bet on a trend feature that makes the forecast worse. Both were
> tested and both were wrong. The numbers below are measured, not assumed.

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

Every current model loses to "yesterday's demand" by a factor of more than two. This is the
single most important fact in the assessment and the v3 is built around it.

**Trend feature smoke test** (`days_since_start` added, same hyperparameters, train 2011,
test 2012):

| Model | MAE without trend | MAE with trend |
|---|---|---|
| Linear Regression | 2121.8 | 3637.8 |
| Random Forest | 2034.4 | 2162.9 |
| Gradient Boosting | 2024.2 | 2377.0 |

The trend feature makes every model worse. Trees do not extrapolate simply because they are
given a clock, and one year of history cannot separate trend from seasonality. It stays in the
plan as an ablation hypothesis, not as a fix.

**Data quality facts:**

- `weathersit` counts: 1 clear = 463, 2 mist = 247, 3 light rain/snow = 21, **4 heavy
  rain/snow = zero rows**. Category 4 is absent from the dataset, so severe-weather behaviour
  cannot be validated at all.
- IQR outliers: `cnt` = 0, `temp` = 0, `atemp` = 0, `hum` = 2, `windspeed` = 13. The target has
  no IQR outliers. Do not pre-write a narrative about extreme-weather outlier days.
- Growth: 2011 mean 3,406 vs 2012 mean 5,600, a 64.4% increase. 2011 maximum 6,043, 2012
  maximum 8,714, and **175 of 366 days in 2012 (48%) sit above the entire 2011 ceiling**.

## Known defect in v2 that must be fixed

The v2 "time-ordered forecasting check" is not honest yet. Cell 27 runs `GridSearchCV` on the
random 75/25 training set, which contains both 2011 and 2012 days. Cell 36 then calls
`clone(model).fit(X_2011, y_2011)`. `clone` preserves the chosen hyperparameters and only
resets the fitted state, so **2012 data influenced the configuration used in the supposedly
unseen temporal test**. The v3 must give the temporal protocol its own selection loop.

## Decisions taken (flagged for Luis to overrule)

**Forecast horizon: day-ahead, decided.** The brief asks to predict demand "for a given day and
weather forecast", and the operationally realistic question is what tomorrow looks like, with
yesterday's counts already known. This choice is what makes autoregressive features and
baselines legitimate. If the horizon were instead "forecast all of 2012 on 1 January", lag and
rolling features would be unavailable and the whole autoregressive branch would be invalid.
Stating the horizon explicitly in section 1 is mandatory either way.

**Use case: system-wide daily rental demand, not station rebalancing.** The dataset is a daily
aggregate for the whole system, with no station, location, inventory or availability columns.
It supports demand planning, staffing, fleet sizing and maintenance scheduling. It does not
support station-level rebalancing decisions, and the v1 plan overclaimed that.

**Personal grounding, allowed with limits.** Luis is a daily bike-share user (Lime) for commute
and errands, which legitimately grounds why daily demand varies: commuters are steady, leisure
riders are weather-sensitive, and that is exactly the `registered` versus `casual` split the
EDA shows. Two constraints: declare Lime as a contemporary dockless analogue rather than the
same docked system, and keep the perspective to rider-side. Any operator-side claim about cost
or acceptable error must be labelled an assumption with no stakeholder evidence behind it.

## Success criteria, relative rather than invented

The first draft proposed "MAE below 800" and "MAE below 1,200" as if they were business
tolerances. There is no stakeholder, cost model or reference behind those numbers, and the
forecast one is beaten by a lag-1 rule. Replace with criteria that are defensible:

**Protocol A, interpolation (random 75/25):**
- Must beat the mean baseline (MAE 1,663) by at least 40%.
- Report MAE normalised against mean daily demand (~4,500) so the error is interpretable
  without inventing a tolerance.

**Protocol B, day-ahead forecasting (temporal):**
- Must beat the **best naive temporal baseline** by at least 5% on MAE. The bar is the rolling
  7-day mean at MAE 847.8, not the constant mean.
- Must achieve R-squared above 0.565, the rolling baseline's value.
- A model that cannot beat yesterday's demand is not approved as a forecaster, regardless of
  how good it looks on Protocol A.

**Declared tie-break, stated before any results:** when two models are within 5% on the primary
metric, prefer the lower RMSE (fewer catastrophic days); if still tied, prefer the simpler and
more interpretable model. Random Forest and Gradient Boosting are already effectively tied on
Protocol A, so this rule will be used.

**Metrics reported:** MAE (primary, the brief's metric), plus MSE, RMSE and R-squared, since
the rubric mentions MSE and R-squared.

## Section-by-section plan

### Section 1 - Business Understanding

- Frame the problem as **next-day, system-wide rental demand**, with the Lime-grounded
  rationale for why daily demand planning matters.
- State the forecast horizon explicitly.
- Declare both evaluation protocols up front as deliberate experimental design, with the
  question each answers: Protocol A measures interpolation within known conditions, Protocol B
  measures forecasting forward in time.
- Declare the success criteria and the tie-break rule above, before any modelling.
- **Assumptions and limitations**, stated here rather than buried: the dataset contains
  *observed* weather, not weather *forecasts*, so Protocol B implicitly assumes a perfect
  weather forecast and will be optimistic relative to production. Only two years of history are
  available. Severe weather (category 4) is entirely absent.

### Section 2 - Data Understanding

Keep every existing EDA plot, they already cover the brief well. Add:

- Table 2.1 - **data quality audit**: schema and dtypes, row count 731 against the expected
  daily span, missing values, duplicate rows, the identity `casual + registered == cnt`, date
  continuity with no gaps, normalised columns within [0, 1], and the `weathersit` category
  distribution. Columns: check, result, pass or fail, action taken.
- Table 2.2 - **outlier review** by IQR, reporting the measured result (`cnt` 0, `hum` 2,
  `windspeed` 13) and the decision. Run first, interpret second. Do not pre-write conclusions.
- An explicit note that `weathersit = 4` has zero rows, so the model has never seen heavy
  rain or snow and its behaviour on such days is unvalidated. This belongs in limitations too.
- Number every table and figure (`Table 2.1`, `Figure 2.3`) with a printed caption and a
  one-line "so what" underneath, following the Assessment 2 v8 convention.

### Section 3 - Data Preparation

Keep the leakage-safe `ColumnTransformer` inside each pipeline, that part of v2 is correct.
Organise features into three declared groups so the ablation can test them separately:

1. **Core** (used by both protocols): the existing calendar and weather features.
2. **Trend** (`days_since_start`): tested as a hypothesis, with the smoke-test result above
   already suggesting it will fail. Reporting a measured negative is the point.
3. **Autoregressive, day-ahead only** (`lag_1_cnt`, `lag_7_cnt`, `roll_7_cnt`): computed on the
   date-ordered series and shifted so no same-day or future value can enter a row. Legitimate
   only under the day-ahead horizon, which is why the horizon had to be decided first.

Rename the interaction feature from `heat_index` to `atemp_humidity_interaction`. The inputs
are normalised and `atemp` is already a feels-like measure, so calling the product a heat index
is inaccurate.

**Ablation with a threshold declared before running:** a feature group is adopted only if it
improves the protocol's primary metric by at least 3% relative, measured on training
cross-validation for that protocol. Run the ablation **independently per protocol**, since a
feature can help forecasting and hurt interpolation or the reverse. Report every result,
including the negatives.

### Section 4 - Modelling, two protocols with separate selection

**Protocol A - interpolation.** Random 75/25 split, `GridSearchCV` with 5-fold CV scored on
negative MAE, exactly as v2. Baseline: mean.

**Protocol B - day-ahead forecasting.** Selection happens **inside 2011 only**:

```
2011 only -> TimeSeriesSplit -> GridSearchCV -> freeze hyperparameters
2012 only -> single final evaluation, opened once
```

Baselines: lag 1, lag 7 and rolling 7-day mean, all computed on 2012. This closes the v2 defect
and makes the temporal result defensible.

Also document the tuning history the brief asks for ("document all revisions until the best
model is reached"): a short table of the grid searched, the values selected, and one line on
why each grid was bounded that way.

Outputs:
- Table 4.1 - full results matrix: five models plus baselines, both protocols, MAE / MSE /
  RMSE / R-squared.
- Table 4.2 - degradation table, MAE ratio between protocols.
- Figure 4.1 - grouped bar chart of MAE by model and protocol, with the naive baselines drawn
  as reference lines so the collapse is visible in one image.

### Section 5 - Evaluation

- Table 5.1 - **gate application**, each model against each declared criterion, per protocol,
  pass or fail.
- Predicted-versus-actual and residual plots, numbered, for the approved model of each
  protocol.
- The 2012 ceiling plot from v2 is worth keeping: it shows concretely why trees cannot
  extrapolate, with 48% of 2012 days above anything seen in training.
- **Explainability chosen by winner**: `TreeExplainer` if an ensemble is approved,
  `LinearExplainer` if Linear Regression is. Global beeswarm plus a local waterfall for one
  high-demand day and one badly-missed day. Keep sklearn's `feature_importances_` as a
  secondary chart and state why SHAP is preferred, that impurity importance is biased towards
  continuous and high-cardinality features. If no model passes the Protocol B gate, explain
  only the model approved for interpolation and do not present it as an approved forecaster.
- Table 5.2 - **approval table**, with approval decided **separately per use case**: one
  verdict for interpolation planning, one for day-ahead forecasting. Each row: model, protocol,
  approved / rejected / approved with conditions, the reason, and the intended use.

### Section 6 - Deployment and lessons

Write this only once the numbers are in. The expected shape, to be confirmed:

> For interpolation under known conditions an ensemble is approved as a planning aid. For
> day-ahead forecasting, no model trained on a single year beats the rolling 7-day mean, so
> the ML models are rejected for that use and the naive rule is the correct production answer
> today. Reversing that requires multi-year history, autoregressive features validated under
> the day-ahead horizon, and monitoring of MAE drift.

Keep the honest-evaluation lesson, which is the real intellectual content here, and connect it
back to the Assessment 2 experience: declaring criteria before looking at results is what makes
a negative result publishable rather than embarrassing.

### Appendices and closing

- Appendix A - glossary of metrics and terms.
- Appendix B - proposed operational deployment sketch, in the Assessment 2 style.
- Reproducibility cell printing Python and library versions plus the random seed.
- Update the Statement of Acknowledgement with the tools actually used for v3 and check the
  model names are current.

## Word count

The brief specifies 2,000 words +/- 10%, so 1,800 to 2,200. Dr Kamran's verbal flexibility on
Assessment 2 does not automatically transfer to Assessment 3. Recommendation: keep the body
within the stated range and move overflow into appendices, which is what worked on BDA601.
Luis to confirm, since he knows how the marking has actually gone.

## Deliverables

- `submission/MLN601FariaLuisBrief3.ipynb`
- `submission/MLN601FariaLuisBrief3.pdf`
- `submission/MLN601FariaLuisBrief3.txt` (source code)

Same export pipeline as Assessments 1 and 2: HTML export, 12px CSS, headless Chrome to PDF,
`nbconvert --to script` with the base64 line stripped. Verify no table is cut across pages.

## Order of work

1. Confirm the decisions above, especially the day-ahead horizon and the word-count position.
2. Copy v2 to v3. Add the quality audit, the numbering convention and the limitations block.
3. Build the three feature groups and the per-protocol ablation harness.
4. Implement Protocol B correctly: `TimeSeriesSplit` selection inside 2011, single evaluation
   on 2012, naive baselines alongside.
5. Run everything, apply the gates, and let the results decide the approvals.
6. Add SHAP for whichever model is approved, plus the approval table.
7. Rewrite sections 1 and 6 to match what actually happened.
8. Clean run from a fresh kernel, then export the submission package.

## Open questions for Luis

- Day-ahead horizon confirmed? Everything autoregressive depends on it.
- Word count: hold to 1,800-2,200 in the body, or take the risk on Kamran's preference for
  longer text?
- If no model beats the naive forecasting baseline, are you comfortable submitting "the naive
  rule wins" as the headline conclusion? It is the strongest and most honest result available,
  but it is a bolder report than "Random Forest achieved R-squared 0.88".
