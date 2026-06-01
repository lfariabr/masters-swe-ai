# Wine Quality Regression Analysis
*MLN601 Machine Learning - Assessment 1 Notebook/Report Skeleton v1*

## Working Metadata

| Item | Detail |
|---|---|
| Subject | MLN601 - Machine Learning |
| Assessment | Assessment 1 - Regression Analysis |
| Task | Build and document a linear regression model using the CRISP-DM process |
| Recommended case | Predict red wine quality from physicochemical wine attributes |
| Length | 1,000 words (+/-10%) inside the notebook/PDF report |
| Weight | 20% |
| Due | Sunday at end of Module 4; README currently records 28/06/2026 |
| Learning outcomes | SLO b, SLO c, SLO d |
| Required deliverables | `.ipynb`, PDF exported from the notebook, and `.txt` source-code file |
| Current status | v2: notebook built at `notebook/MLN601FariaLuisBrief1.ipynb`, reads the local red wine CSV, executed end to end with embedded outputs and real metrics; report prose and remaining `[bracket]` decisions still to finalise |

---

## Brief Requirements Snapshot

| Required element | How this skeleton handles it | Evidence target |
|---|---|---|
| Use Jupyter Notebook on Azure ML or Google Colab with Python 3.6 | Notebook plan uses Python 3.6-compatible syntax and standard `pandas`, `seaborn`, and `scikit-learn` imports | Notebook runs end to end without local-only paths |
| Follow the six CRISP-DM stages | Report draft is structured as Business Understanding, Data Understanding, Data Preparation, Modelling, Evaluation, and Deployment/reflection | Each heading contains Markdown explanation plus code/output where relevant |
| Use the UCI wine quality dataset | v1 recommends the red wine CSV for a clear, smaller regression scope | Include exact dataset page, direct CSV URL, and acquisition method |
| Use linear regression | Modelling section uses `sklearn.linear_model.LinearRegression` only | Record model parameters and any revised runs |
| Include pairplot output | Data Understanding cell plan includes a seaborn `pairplot` and correlation heatmap | Notebook comments interpret independent/dependent variable relationships |
| Interpret results | Evaluation section defines MAE, RMSE, R2, baseline comparison, residual review, and coefficient interpretation | State whether the model meets the evaluation criteria |
| No real deployment required | Deployment section is framed as lessons learned and future improvements | Reflect on what went right, what went wrong, and what to improve |
| Submit clean artefacts | Recommended submission structure lists final filenames from the brief | `.ipynb`, `.pdf`, and `.txt` code files align with brief naming |

## Rubric Strategy

| Rubric area | Weight | High-distinction move |
|---|---:|---|
| Business Understanding | 10% | Frame the wine-quality prediction as useful but explicitly oversimplified; define business value, target variable, and measurable success criteria |
| Data Understanding | 20% | Specify UCI source, selected red wine dataset, variables, units/levels, structure, missing data, descriptive stats, pairplot, and interpretation |
| Data Preparation | 10% | Explain data selection, target/features, train/test split, cleaning decisions, duplicate/missing-value treatment, and why scaling is or is not needed |
| Modelling and Evaluation | 20% | Use linear regression transparently, record parameters, compare baseline vs revised runs, report MAE/RMSE/R2, interpret coefficients and residuals |
| Deployment | 20% | Provide a thoughtful CRISP-DM reflection: what worked, limitations, future model/data improvements, and why this is decision support rather than production automation |
| Deliverables | 20% | Notebook runs without errors, PDF matches notebook, code is clear, Markdown documents the full end-to-end process |

## Suggested Word Budget

| Section | Target words | Notes |
|---|---:|---|
| Business Understanding | 140-170 | Define problem, scope, stakeholders, and evaluation criteria |
| Data Understanding | 250-300 | Highest factual detail: source, variables, quality, plots, pairplot comments |
| Data Preparation | 120-150 | Keep concise but explicit about selected rows/columns and split |
| Modelling | 150-180 | Linear regression assumptions, parameters, runs, rationale |
| Evaluation | 150-180 | Results table, baseline comparison, coefficient/residual interpretation |
| Deployment / lessons learned | 120-150 | Required reflection instead of actual deployment |
| Total body | ~1,000 | Keep code comments short; move larger tables/plots to appendices if needed |

## Draft Thesis

This notebook uses the CRISP-DM process to build a transparent linear regression model that predicts red wine quality from physicochemical measurements in the UCI wine quality dataset. The model is useful as an interpretable baseline because it links variables such as alcohol, acidity, sulphates, and density to a predicted quality score. However, the report should acknowledge that wine quality is subjective and ordinal, so a linear regression prediction is an oversimplified decision-support tool rather than a production-ready replacement for expert tasting or more advanced modelling.

---

# Recommended Submission Structure

```text
Assessment1/
  MLN601_Assessment1_Report_Skeleton.md
  notebook/
    MLN601FariaLuisBrief1.ipynb
  exports/
    MLN601FariaLuisBrief1.pdf
    MLN601FariaLuisBrief1.txt
  outputs/
    model_metrics.csv
    coefficients.csv
    figures/
      pairplot.png
      correlation_heatmap.png
      residuals.png
```

> The brief asks for `MLN601LastNameFirstNameBrief1.ipynb` and `MLN601LastNameFirstNameBrief1.pdf`. Use the exact LMS-required naming in the final submission if the facilitator gives a different convention.

---

# Notebook / Report Draft

## 0. Title Cell

**Suggested notebook title:**

`MLN601 Assessment 1: Regression Analysis of UCI Red Wine Quality`

**Include:**

| Field | Draft value |
|---|---|
| Student | Luis Faria |
| Subject | MLN601 Machine Learning |
| Assessment | Assessment 1 - Regression Analysis |
| Dataset | UCI Wine Quality - red wine data |
| Algorithm | Linear Regression |
| Methodology | CRISP-DM |

---

## 1. Business Understanding

### 1.1 Project Objective

Wine producers measure chemical properties such as acidity, sulphates, residual sugar, and alcohol concentration during production. This project tests whether those objective measurements can be used to predict wine quality, recorded as a sensory score between 1 and 10. The recommended scope is the UCI red wine dataset only, because it keeps the target population clear and avoids mixing red and white wine distributions in a short assessment.

The machine learning task is supervised regression: the input variables are the 11 physicochemical attributes and the dependent variable is `quality`. A useful model would help a winery or quality-control team screen batches for likely low or high quality before final expert tasting. The prediction should be treated as decision support because the quality label is subjective, ordinal, and likely influenced by non-chemical factors not captured in the dataset.

### 1.2 Evaluation Criteria

| Criterion | Draft decision |
|---|---|
| Prediction metric | Use MAE and RMSE to express average prediction error in quality-score units |
| Model fit | Use R2 to show variance explained by the linear model |
| Baseline comparison | Compare against predicting the training-set mean quality for every test row |
| Practical success | Model should beat the baseline and produce interpretable coefficients, while acknowledging limited precision |
| Communication success | Explain the result in non-specialist terms for a quality-control stakeholder |

> Final writing note: explicitly say that a perfect model is unrealistic because wine quality is judged by humans and the dataset only contains physicochemical variables.

---

## 2. Data Understanding

### 2.1 Data Acquisition

| Item | Detail |
|---|---|
| Source organisation | UCI Machine Learning Repository (dataset id 186) |
| Dataset page | `https://archive.ics.uci.edu/dataset/186/wine+quality` |
| Selected file | `winequality-red.csv`, downloaded into `Assessment1/dataset/` |
| Acquisition method | Read the local CSV with `pandas.read_csv(path, sep=";")`; the notebook resolves `dataset/winequality-red.csv` relative to its own folder and falls back to the legacy UCI URL (`.../ml/machine-learning-databases/wine-quality/winequality-red.csv`) if the file is absent |
| Confirmed shape | 1,599 rows x 12 columns (verified in notebook output) |

### 2.2 Variable Description

| Variable | Role | Type / level | Unit or meaning to verify |
|---|---|---|---|
| `fixed acidity` | Feature | Continuous numeric | Non-volatile acids, commonly reported as g/dm3 |
| `volatile acidity` | Feature | Continuous numeric | Acetic acid measure, commonly reported as g/dm3 |
| `citric acid` | Feature | Continuous numeric | Citric acid concentration, commonly reported as g/dm3 |
| `residual sugar` | Feature | Continuous numeric | Sugar remaining after fermentation, commonly reported as g/dm3 |
| `chlorides` | Feature | Continuous numeric | Salt/chloride concentration, commonly reported as g/dm3 |
| `free sulfur dioxide` | Feature | Continuous numeric | Free SO2, commonly reported as mg/dm3 |
| `total sulfur dioxide` | Feature | Continuous numeric | Total SO2, commonly reported as mg/dm3 |
| `density` | Feature | Continuous numeric | Wine density |
| `pH` | Feature | Continuous numeric | Acidity/basicity scale |
| `sulphates` | Feature | Continuous numeric | Sulphate concentration, commonly reported as g/dm3 |
| `alcohol` | Feature | Continuous numeric | Alcohol percentage by volume |
| `quality` | Target | Ordinal integer | Sensory quality score, 0-10 scale in dataset description |

### 2.3 Data Quality Checks

Run and comment on:

```python
df.shape
df.head()
df.info()
df.describe().T
df.isna().sum()
df.duplicated().sum()
df["quality"].value_counts().sort_index()
```

**Draft interpretation placeholders:**

- The dataset contains only numeric columns, which simplifies regression modelling.
- Missing-value checks return 0 across all columns (consistent with the UCI documentation), so no imputation is required.
- Duplicate rows: 240. They are retained in the base model because the dataset has no unique sample ID and identical physicochemical readings can legitimately recur; a sensitivity note is added in Evaluation.
- The target distribution is concentrated on scores 5 and 6, with very few wines at the extremes (3, 4, 8), which limits the model's ability to learn the tails.

### 2.4 Exploratory Analysis

Required plots:

| Plot | Purpose | Interpretation to write |
|---|---|---|
| Target count plot | Shows distribution of quality scores | Note imbalance and scarcity of extreme quality levels |
| Histograms | Shows skew/outliers in physicochemical variables | Identify skewed variables such as residual sugar or chlorides if present |
| Correlation heatmap | Shows linear relationships across all variables | Highlight strongest positive/negative correlations with `quality` |
| Seaborn pairplot | Required by brief to inspect relationships between variables | Comment on visible linearity, clusters, outliers, and weak relationships |

**Expected interpretation direction to verify after plotting:**

- `alcohol` often has a positive relationship with quality.
- `volatile acidity` often has a negative relationship with quality.
- `sulphates` and `citric acid` may show weaker positive relationships.
- Many relationships are likely weak or noisy, supporting the point that linear regression is an interpretable baseline rather than a perfect predictor.

---

## 3. Data Preparation

### 3.1 Data Selection

The selected dataset is the red wine CSV from UCI. The features are all 11 physicochemical columns, and the target is `quality`. Red wine is selected instead of combining red and white wine because the brief allows a focused target and the smaller scope makes interpretation easier in a 1,000-word report.

```python
target_col = "quality"
feature_cols = [col for col in df.columns if col != target_col]

X = df[feature_cols]
y = df[target_col]
```

### 3.2 Cleaning and Train/Test Split

Cleaning should be minimal and evidence-based. If there are no missing values, state that imputation was not needed. If duplicate rows are removed, report the before/after shape and explain why. Split the data before fitting the model to protect the test set from training influence.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)
```

**Draft decision table:**

| Preparation decision | Rationale | Final value |
|---|---|---|
| Missing values | Check before modelling; impute only if required | None found (0); no imputation |
| Duplicate rows | Report count; remove only if justified | 240 found; retained (no unique ID, readings can recur) |
| Feature scaling | Not required for ordinary least squares predictions, but useful if comparing standardized coefficients | Not used in base model |
| Train/test split | Enables out-of-sample evaluation | 80/20 split, `random_state=42` |
| Target treatment | Treat ordinal score as continuous for linear regression | Required simplification |

---

## 4. Modelling

### 4.1 Model Choice

The assessment requires a linear regression model. Linear regression is appropriate as a first baseline because it is transparent, fast, and produces coefficients that can be interpreted as the estimated change in predicted quality for a one-unit change in each feature, holding other features constant. The limitation is that it assumes approximately linear relationships and treats the sensory quality score as continuous.

### 4.2 Model Assumptions

| Assumption | How to check or discuss |
|---|---|
| Linear relationship | Pairplot, correlation heatmap, predicted vs actual plot |
| Independent errors | Dataset rows represent separate wine observations; note any uncertainty |
| Homoscedasticity | Residual plot should not show strong funnel pattern |
| Residual normality | Histogram or Q-Q plot optional; not required for prediction but useful for interpretation |
| Limited multicollinearity | Correlation heatmap; optionally note strong feature-feature correlations |
| Continuous target | Treat `quality` as continuous despite being an ordinal score |

### 4.3 Base Model Run

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def regression_metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred),
    }

baseline_pred = np.full(shape=y_test.shape, fill_value=y_train.mean())
baseline_metrics = regression_metrics(y_test, baseline_pred)

model_all = LinearRegression(fit_intercept=True)
model_all.fit(X_train, y_train)
pred_all = model_all.predict(X_test)
all_metrics = regression_metrics(y_test, pred_all)

metrics_table = pd.DataFrame([
    {"model": "Mean baseline", **baseline_metrics},
    {"model": "Linear regression - all features", **all_metrics},
])
metrics_table
```

### 4.4 Parameter Settings and Revisions

| Run | Inputs | Parameter settings | Rationale | Result placeholder |
|---|---|---|---|---|
| Baseline | None; predict train mean | Not applicable | Shows whether linear regression adds value | MAE 0.685, RMSE 0.811, R2 -0.01 |
| Run 1 | All 11 features | `fit_intercept=True`, default `LinearRegression` settings | Required simple interpretable model | MAE 0.504, RMSE 0.625, R2 0.403 |
| Run 2 | Features with abs(corr) >= 0.10 vs quality | Same linear regression settings | Tests whether a simpler model performs similarly and is easier to explain | MAE 0.506, RMSE 0.627, R2 0.399 |

Possible feature-selection code:

```python
corr_with_quality = df.corr()["quality"].drop("quality")
corr_abs = corr_with_quality.abs().sort_values(ascending=False)
selected_features = list(corr_abs[corr_abs >= 0.10].index)

X_selected = df[selected_features]
X_train_sel, X_test_sel, y_train_sel, y_test_sel = train_test_split(
    X_selected,
    y,
    test_size=0.20,
    random_state=42
)

model_selected = LinearRegression(fit_intercept=True)
model_selected.fit(X_train_sel, y_train_sel)
pred_selected = model_selected.predict(X_test_sel)
selected_metrics = regression_metrics(y_test_sel, pred_selected)
```

Coefficient table:

```python
coef_table = pd.DataFrame({
    "feature": X_train.columns,
    "coefficient": model_all.coef_
}).sort_values("coefficient", ascending=False)

coef_table
```

---

## 5. Evaluation

### 5.1 Results Summary

| Model | MAE | RMSE | R2 | Interpretation |
|---|---:|---:|---:|---|
| Mean baseline | 0.685 | 0.811 | -0.01 | Predicts average quality for every wine |
| Linear regression - all features | 0.504 | 0.625 | 0.403 | Main required model |
| Linear regression - selected features | 0.506 | 0.627 | 0.399 | Optional revised run; near-identical, simpler to explain |

**Observed coefficients (interpret with caution).** Largest magnitudes from the executed run: `density` -10.35, `chlorides` -1.81, `volatile acidity` -1.00, `sulphates` +0.84, `alcohol` +0.28. The very large `density` coefficient is a multicollinearity artefact (density correlates with alcohol and residual sugar), so coefficients should be read as model weights, not causal effect sizes. The sign pattern is still sensible: more alcohol and sulphates push quality up, while higher volatile acidity and chlorides push it down.

### 5.2 Evaluation Narrative

Write the final narrative after running the notebook:

1. State whether linear regression improves over the mean baseline.
2. Translate RMSE into wine-quality score units, for example: "an RMSE of 0.63 means predictions are typically about 0.6 of a quality-score point away from the true label."
3. Interpret R2 without overstating it: "the model explains about 40% of variance in the test set."
4. Identify strongest positive and negative coefficients, but warn that correlated features make coefficients sensitive.
5. Discuss residuals and whether the model struggles with high or low quality wines.

Suggested residual plots:

```python
import matplotlib.pyplot as plt
import seaborn as sns

residuals = y_test - pred_all

plt.figure(figsize=(7, 5))
sns.scatterplot(x=pred_all, y=residuals)
plt.axhline(0, color="black", linewidth=1)
plt.xlabel("Predicted quality")
plt.ylabel("Residual")
plt.title("Residuals vs predicted quality")
plt.show()

plt.figure(figsize=(7, 5))
sns.scatterplot(x=y_test, y=pred_all)
plt.xlabel("Actual quality")
plt.ylabel("Predicted quality")
plt.title("Actual vs predicted wine quality")
plt.show()
```

### 5.3 Evaluation Decision

Draft decision sentence:

> The model **does** meet the evaluation criteria because it **beats** the mean baseline on MAE (0.504 vs 0.685) and RMSE (0.625 vs 0.811), produces an R2 of **0.40**, and offers interpretable relationships between wine chemistry and quality. However, it should be used only as a baseline because the target variable is subjective and the pairplot/residuals indicate that the relationships are not fully linear.

---

## 6. Deployment / Lessons Learned

The brief does not require model deployment. Use this section as a CRISP-DM reflection.

### 6.1 Lessons Learned

Draft points to convert into prose:

- CRISP-DM forced the project to define the prediction goal before writing code.
- Reading the data source directly from UCI improved reproducibility.
- Data quality checks showed that "clean" numeric data still needs analysis of target imbalance, duplicate rows, and outliers.
- Pairplot and correlation analysis were useful for seeing why linear regression may perform only moderately.
- Linear regression is easy to explain to stakeholders, but it may underfit wine quality because relationships may be non-linear and the target is ordinal.

### 6.2 Future Improvements

| Improvement | Why it matters |
|---|---|
| Cross-validation | More stable estimate than one train/test split |
| Regularised regression | Ridge/Lasso can reduce coefficient instability from correlated variables |
| Feature engineering | Ratios or transformations may capture chemistry effects more effectively |
| Compare red vs white wine | Tests whether separate wine types behave differently |
| Non-linear models | Decision trees or random forests may capture relationships missed by linear regression |
| Deployment controls | Any production use would require data validation, model monitoring, and human review |

Draft closing:

> Overall, the exercise shows that a simple linear regression model can provide a reproducible and interpretable baseline for wine-quality prediction, but model performance and business value depend on careful problem framing, transparent evaluation, and honest communication of limitations.

---

# Notebook Cell Plan

## Cell 1 - Imports

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
```

## Cell 2 - Load Data

```python
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"

df = pd.read_csv(DATA_URL, sep=";")
df.head()
```

## Cell 3 - Inspect Structure and Quality

```python
print(df.shape)
print(df.info())
display(df.describe().T)
display(df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())
display(df["quality"].value_counts().sort_index())
```

## Cell 4 - Visual Exploration

```python
plt.figure(figsize=(7, 4))
sns.countplot(x="quality", data=df)
plt.title("Distribution of wine quality scores")
plt.show()

plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation heatmap")
plt.show()

sns.pairplot(
    df,
    corner=True,
    diag_kind="hist",
    plot_kws={"alpha": 0.25, "s": 12}
)
plt.show()
```

> If the full pairplot is too dense for the final PDF, keep it in the notebook and also include a smaller pairplot of `quality`, `alcohol`, `volatile acidity`, `sulphates`, `citric acid`, and `density` for readable interpretation.

## Cell 5 - Prepare Features and Split

```python
target_col = "quality"
feature_cols = [col for col in df.columns if col != target_col]

X = df[feature_cols]
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)
```

## Cell 6 - Train and Evaluate Model

```python
def regression_metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred),
    }

baseline_pred = np.full(shape=y_test.shape, fill_value=y_train.mean())
model = LinearRegression(fit_intercept=True)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

results = pd.DataFrame([
    {"model": "Mean baseline", **regression_metrics(y_test, baseline_pred)},
    {"model": "Linear regression", **regression_metrics(y_test, predictions)},
])
results
```

## Cell 7 - Interpret Coefficients and Residuals

```python
coefficients = pd.DataFrame({
    "feature": feature_cols,
    "coefficient": model.coef_,
}).sort_values("coefficient", ascending=False)

display(coefficients)

residuals = y_test - predictions

plt.figure(figsize=(7, 5))
sns.scatterplot(x=predictions, y=residuals)
plt.axhline(0, color="black", linewidth=1)
plt.xlabel("Predicted quality")
plt.ylabel("Residual")
plt.title("Residuals vs predicted quality")
plt.show()
```

## Cell 8 - Save Submission Support Files

```python
results.to_csv("model_metrics.csv", index=False)
coefficients.to_csv("coefficients.csv", index=False)
```

For the required `.txt` source-code deliverable, export or copy the final notebook code cells into:

```text
MLN601FariaLuisBrief1.txt
```

---

# Appendix A - Rubric Checklist

| Checklist item | Status |
|---|---|
| Brief read and summarised | Done in v1 scaffold |
| CRISP-DM six stages present | Drafted |
| Business objective and evaluation criteria defined | Drafted |
| UCI source and direct dataset link included | Drafted |
| Dataset acquisition method stated | Drafted |
| Variables, units, and target described | Drafted; verify unit wording before final |
| Missing data and duplicate checks included | Done (0 missing, 240 duplicates) |
| Pairplot included with interpretation prompt | Done (focused pairplot + optional full pairplot) |
| Data selection and cleaning decisions documented | Drafted |
| Linear regression imported and used | Drafted |
| Parameter settings recorded | Drafted |
| Revised run documented if used | Drafted |
| MAE, RMSE, R2, and baseline comparison included | Done (metrics computed and saved) |
| Evaluation criteria conclusion included | Done (model beats baseline, R2 0.40) |
| Deployment reflection included | Drafted |
| Notebook runs without errors | Done; executed end to end locally with embedded outputs |
| PDF exported from notebook | To do (export from Colab/Azure or local `nbconvert --to pdf`) |
| `.txt` source-code file prepared | To do |
| APA references checked | To do |

## Appendix B - Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Pairplot is too large for the PDF | Report becomes unreadable | Keep full pairplot in notebook and add a smaller selected-variable pairplot for explanation |
| Linear regression performs modestly | Evaluation may look weak | Compare against mean baseline and explain that a transparent baseline is the task goal |
| Target variable is ordinal | Regression assumptions are imperfect | Acknowledge the simplification in Business Understanding and Evaluation |
| Feature coefficients are misleading due to multicollinearity | Interpretation may overclaim causality | Use cautious wording and support with correlation/residual plots |
| Notebook export via LaTeX fails | Submission delay | Test PDF export early; fallback to browser print only if facilitator accepts it |
| Dataset URL fails during final run | Notebook may not reproduce | Cache a local copy only after documenting the original UCI URL and acquisition method |

## Appendix C - Final Draft Tasks

1. ✅ Notebook created at `Assessment1/notebook/MLN601FariaLuisBrief1.ipynb`.
2. ✅ Data loaded from the local `dataset/` CSV (URL fallback retained); also runnable on Colab/Azure.
3. ✅ Actual shape (1,599 x 12), missing values (0), duplicates (240), and target distribution recorded.
4. ✅ Target plot, correlation heatmap, pairplot, residual plot, and actual-vs-predicted plot generated and saved to `outputs/figures/`.
5. ✅ Baseline and linear regression metrics computed.
6. ✅ Optional selected-feature revised run included.
7. 🔥 Replace remaining `[bracket]` decisions in the report prose with the recorded numbers.
8. 🕐 Cut report prose to 900-1,100 words.
9. 🕐 Export final `.ipynb`, PDF, and `.txt` code deliverables.
10. 🕐 Check APA references and file naming against LMS instructions.

---

# Reference Starter List

Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS Inc. https://www.the-modeling-agency.com/crisp-dm.pdf

Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Modeling wine preferences by data mining from physicochemical properties. *Decision Support Systems, 47*(4), 547-553. https://archive.ics.uci.edu/dataset/186/wine+quality

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825-2830. https://jmlr.org/papers/v12/pedregosa11a.html

Torrens University Australia. (2024). *MLN601 Assessment 1 brief: Regression Analysis*.

University of California, Irvine. (n.d.). *Wine quality data set*. UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/186/wine+quality
