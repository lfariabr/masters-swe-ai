# MLN601 Assessment 3 - plan for v3

Status: draft for review, nothing implemented yet.
Base: `notebook/MLN601FariaLuisBrief3v2.ipynb` (46 cells, executed).
Target: `notebook/MLN601FariaLuisBrief3v3.ipynb` + `submission/MLN601FariaLuisBrief3.{ipynb,pdf,txt}`.
Due: 19/08/2026. Weight 40%. Issue #189.

## Why a v3 at all

The v2 notebook is a solid regression study with one genuinely strong finding: on a
time-ordered split (train 2011, predict 2012) every model collapses, with MAE about 4.3x
worse and negative R-squared. That finding is currently presented as a late reality check
rather than as the reason the report reaches its conclusion.

At the same time, v2 repeats three of the four criticisms Dr Kamran wrote on Assessment 1:

1. "define what success looks like from a technical machine-learning perspective" - v2 has
   no numeric success criterion, only "beat the baseline with a low MAE".
2. "more verification and validation methods on data quality... document any quality issues"
   - v2 has a single cell with `isna().sum()`, duplicates and an identity check.
3. "you could also derive new attributes that will be helpful" - v2 has zero engineered
   features, and its own section 6 lists the obvious ones as future work.
4. "explicitly justify which model(s) should be approved for business use" - cell 34 calls
   Random Forest best, cell 40 shows Gradient Boosting best on the honest split and all
   models failing, and the notebook never states what is approved.

The v3 closes those four gaps and lifts the Assessment 2 v8 conventions that graded well.

## Current v2 numbers, for reference

Random 75/25 split (interpolation):

| Model | MAE | RMSE | R2 |
|---|---|---|---|
| Random Forest | 450.9 | 683.3 | 0.879 |
| Gradient Boosting | 473.3 | 663.2 | 0.886 |
| Linear Regression | 566.1 | 775.0 | 0.844 |
| K-Nearest Neighbors | 721.1 | 926.9 | 0.777 |
| Mean baseline | 1663.0 | 1983.3 | -0.021 |

Time-ordered split, train 2011 predict 2012 (extrapolation):

| Model | MAE | R2 | Times worse |
|---|---|---|---|
| Gradient Boosting | 2024.2 | -0.503 | 4.28x |
| Random Forest | 2034.4 | -0.511 | 4.51x |
| K-Nearest Neighbors | 2065.1 | -0.574 | 2.86x |
| Linear Regression | 2121.8 | -0.656 | 3.75x |
| Mean baseline | 2488.7 | -1.509 | 1.50x |

Structural cause already documented in v2: 2011 training ceiling 6,043; largest Random Forest
2012 forecast 5,275; 2012 actual maximum 8,714; every model under-predicts.

## Section-by-section plan

### Section 1 - Business Understanding (rewrite, still short)

Add a **declared success criteria** block, before any modelling, in the Assessment 2 gate
style. Proposed wording to review:

- Primary gate: test MAE must be **below 800 bikes per day**, roughly 17% of the mean daily
  demand of about 4,500, which is the tolerance a rebalancing crew can absorb.
- Mandatory gate: the model must beat the mean baseline on MAE by at least 40%.
- Forecast gate (new, and the interesting one): on the time-ordered protocol the model must
  keep MAE below 1,200 and R-squared above 0. Anything that cannot beat a constant is not a
  forecaster.
- Declared tie-break, stated before results: when two models are within 5% of each other on
  the primary metric, prefer the one with the lower RMSE (fewer catastrophic days), and if
  still tied, prefer the simpler and more interpretable model. This matters because Random
  Forest and Gradient Boosting are effectively tied in v2 and no rule currently resolves it.

Also state the two evaluation protocols up front as a deliberate experimental design, not as
an afterthought: random 75/25 answers "how well does this interpolate within known
conditions", time-ordered answers "can it forecast forward". Both are reported for every
model.

### Section 2 - Data Understanding (add a formal quality audit)

Keep all existing EDA plots, they are good and cover the brief. Add before them:

- Table 2.1 - **data quality audit**: one row per check (schema/dtypes, row count vs expected
  731, missing values, duplicate rows, identity `casual + registered == cnt`, date continuity
  with no gaps, value ranges of the normalised columns within [0, 1], `weathersit` category 4
  frequency). Each row: check, result, pass/fail, action taken.
- Table 2.2 - **outlier review** on `cnt`, `hum`, `windspeed` using IQR, with a documented
  decision. Expected finding: a small number of extreme-weather and holiday days. Decision to
  keep them, because they are real operational days rather than recording errors, and to note
  that they will drive the largest residuals. This mirrors the Assessment 2 approach that
  scored well.
- One explicit note on `weathersit` category 4 (heavy rain/snow), which has very few days, and
  what that means for the model's reliability on severe weather.

Number every table and figure as `Table 2.1`, `Figure 2.3` and so on, with the printed caption
plus a one-line "so what" underneath, exactly as in the Assessment 2 v8 notebook.

### Section 3 - Data Preparation (add feature engineering plus ablation)

Keep the leakage-safe `ColumnTransformer` inside each pipeline, that part is already correct.
Add an engineered feature set, tested rather than assumed:

- `days_since_start` - a **continuous time trend** replacing the reliance on the binary `yr`
  flag. This is the direct fix for the extrapolation failure, and it is the one most likely to
  produce a positive result.
- `heat_index` - an interaction of `atemp` and `hum`, since comfort is not temperature alone.
- `temp_squared` - captures the "too hot is also bad" curvature the EDA hints at.
- `lag_7_cnt` and `roll_7_cnt` - demand one week earlier and the trailing weekly mean. These
  need care: computed on the ordered series and shifted so no future information enters a row.
  If they cannot be made leakage-safe inside the CV folds cleanly, document that and drop them
  rather than risk leakage. Note that a day-ahead planner realistically does have last week's
  counts, so they are operationally legitimate.

Then run an **ablation with a threshold declared before the run**: the engineered set is
adopted only if it improves the primary metric by at least 3% relative on training
cross-validation. Report the result either way. A negative result is a documented result, as
in Assessment 2.

Expected outcome, to be confirmed by the run: `days_since_start` materially improves the
time-ordered protocol and barely changes the random-split protocol. If so, that becomes the
report's strongest single argument.

### Section 4 - Modelling (restructure into two protocols)

Same five estimators, same grids as v2, plus the tuning history the brief asks for
("document all revisions until the best model is reached"): a short table of the grid
searched, the selected values, and one line on why the grid was set that way.

Run each model under both protocols and produce:

- Table 4.1 - full results matrix, five models by two protocols, with MAE, RMSE and R-squared.
- Table 4.2 - the degradation table (`times_worse`), already in v2 as `split_comparison_v2`.
- Figure 4.1 - grouped bar chart of MAE by model and protocol, so the collapse is visible in
  one image.

### Section 5 - Evaluation (add gates, approval and SHAP)

- Table 5.1 - **gate application**: each model against each declared gate, pass or fail.
  Expected: several models pass the interpolation gates, and possibly none pass the forecast
  gate unless the time-trend feature rescues it.
- Keep the predicted-versus-actual and residual plots, numbered.
- Replace `feature_importances_` as the primary explanation with **SHAP** on the approved
  model: `TreeExplainer`, global beeswarm plus a local waterfall for one high-demand day and
  one badly-missed day. Keep the sklearn importances as a secondary chart and state why SHAP
  is preferred, that impurity importance is biased towards high-cardinality and continuous
  features. This also lines up with Module 7 of the subject, Automated and Explainable
  Machine Learning.
- Table 5.x - **approval table**, one row per model: approved, rejected, or approved with
  conditions, plus the reason and the intended use. This is the direct answer to the
  Assessment 1 feedback, and it must be unambiguous.

### Section 6 - Deployment and lessons

Rewrite around what the evidence actually supports. Draft position, to be adjusted once the
numbers are in: approve one ensemble for **intra-year operational planning** under the stated
MAE tolerance, and explicitly **reject all current models for year-ahead forecasting** unless
the time-trend feature clears the forecast gate. State the required conditions for a
production rollout: multi-year history, continuous trend feature, monitoring of MAE drift,
and a documented fallback when severe weather is forecast.

Keep the honest-evaluation lesson, which is the real intellectual content of this assessment.

### Appendices and closing

- Appendix A - glossary of the metrics and terms used.
- Appendix B - proposed operational deployment sketch, in the style of the Assessment 2
  appendices, showing where the model would sit in a rebalancing workflow.
- Update the Statement of Acknowledgement with the tools actually used for v3, and check the
  model names are current.
- Add a reproducibility cell that prints Python and library versions and the random seed.

## Deliverables and submission

Per the brief:

- `MLN601FariaLuisBrief3.ipynb`
- `MLN601FariaLuisBrief3.pdf`
- a `.txt` with the source code

Create `Assessment3/submission/` and use the same export pipeline that worked for Assessments
1 and 2: HTML export, 12px CSS, headless Chrome to PDF, and `nbconvert --to script` with the
base64 line stripped for the text file. Verify no table is cut across pages in the PDF.

Word count is not a constraint for this subject, so the narrative can stay explanatory.

## Order of work

1. Confirm this plan and the proposed gate numbers, they are guesses and should reflect what
   Luis considers an acceptable planning error.
2. Copy v2 to v3, add the quality audit and the numbering convention.
3. Add engineered features and run the ablation. This is the step that determines the story.
4. Restructure modelling into the two-protocol matrix and apply the gates.
5. Add SHAP and the approval table.
6. Rewrite sections 1 and 6 to match the actual results.
7. Full clean run from a fresh kernel, then export the submission package.

## Open questions for Luis

- Are the proposed gates realistic? Specifically, is an average error of 800 bikes per day on
  about 4,500 acceptable to a rebalancing operation, or should it be tighter?
- Include the lag and rolling features, accepting the extra care needed to keep them
  leakage-free, or keep the feature set purely calendar and weather?
- Keep the Random Forest as the headline model if it stays ahead on MAE, or let the tie-break
  rule move it to Gradient Boosting on RMSE grounds?
