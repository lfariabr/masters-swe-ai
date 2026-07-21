"""Build MLN601 Assessment 2 v8 from the v7 notebook and v8 result files."""

from __future__ import annotations

import re
from copy import deepcopy
from pathlib import Path

import nbformat
import pandas as pd


HERE = Path(__file__).resolve().parent
BASE_DIR = HERE.parent
SOURCE = HERE / "MLN601FariaLuisBrief2v7.ipynb"
TARGET = HERE / "MLN601FariaLuisBrief2v8.ipynb"
OUTPUT_DIR = BASE_DIR / "outputs"


def clean_text(value: str) -> str:
    value = value.replace("_v7", "_v8")
    value = value.replace("—", "-").replace("–", "-")
    value = re.sub(r"\bproxy\b", "representative stand-in", value, flags=re.IGNORECASE)
    return value


def markdown(content: str):
    return nbformat.v4.new_markdown_cell(clean_text(content.strip()))


def code(content: str):
    return nbformat.v4.new_code_cell(clean_text(content.strip()))


def result_narratives() -> dict[str, str]:
    matrix_path = OUTPUT_DIR / "model_matrix_cv_v8.csv"
    selection_path = OUTPUT_DIR / "selection_summary_v8.csv"
    test_path = OUTPUT_DIR / "finalist_test_metrics_v8.csv"
    ablation_path = OUTPUT_DIR / "feature_ablation_v8.csv"
    if not all(path.exists() for path in (matrix_path, selection_path, test_path, ablation_path)):
        return {
            "section4": "Results will be interpreted after the first clean execution.",
            "section5": "Finalist results will be interpreted after the first clean execution.",
            "approval": "The approval table will be populated from the frozen CV decision.",
            "section6": "Final lessons will be updated after the first clean execution.",
            "api": "The serving backlog will be checked after the approved v8 model is known.",
        }

    matrix = pd.read_csv(matrix_path)
    selection = pd.read_csv(selection_path)
    test = pd.read_csv(test_path)
    ablation = pd.read_csv(ablation_path)
    approved = selection.loc[selection["role"] == "approved"].iloc[0]
    approved_cv = matrix[
        (matrix["model"] == approved["model"])
        & (matrix["treatment"] == approved["treatment"])
    ].iloc[0]
    approved_test = test[
        (test["model"] == approved["model"])
        & (test["treatment"] == approved["treatment"])
    ].iloc[0]
    treatment_text = {
        "Original": "original distribution",
        "SMOTE": "SMOTE",
        "Class weight": "class weighting",
    }[approved["treatment"]]

    delta = pd.read_csv(OUTPUT_DIR / "treatment_deltas_v8.csv")
    smote_delta = delta[delta["comparison"] == "SMOTE - Original"]
    mean_sens = smote_delta["delta_sensitivity_low"].mean()
    mean_spec = smote_delta["delta_specificity_high"].mean()
    mean_auc = smote_delta["delta_roc_auc"].mean()
    rf_best = matrix[matrix["model"] == "Random Forest"].sort_values(
        "balanced_accuracy", ascending=False
    ).iloc[0]
    tree_best = matrix[matrix["model"] == "Decision Tree"].sort_values(
        "balanced_accuracy", ascending=False
    ).iloc[0]
    ablation_row = ablation.iloc[-1]

    section4 = f"""
**Interpretation:**

- Across the nine model families, SMOTE changed mean sensitivity by {mean_sens:+.3f},
  mean specificity by {mean_spec:+.3f}, and mean AUC by {mean_auc:+.3f}. This separates
  an operating-point change from a ranking improvement.
- The best Random Forest treatment reached balanced accuracy {rf_best['balanced_accuracy']:.3f},
  compared with {tree_best['balanced_accuracy']:.3f} for the best single Decision Tree.
  The ensemble comparison therefore measures the benefit of averaging many trees against
  the loss of one directly readable rule set.
- Gaussian Naive Bayes keeps continuous measurements, while Bernoulli, Multinomial and
  Complement variants transform them to fit different assumptions. Their result is evidence
  about assumption fit, not a success or failure label.
- The sulfur feature set was {'retained' if bool(ablation_row['retained']) else 'rejected'}.
  Its best material gain was {ablation_row['material_gain']:.4f} against the predeclared
  0.01 rule.
- The frozen recommendation from training CV is **{approved['model']} with
  {treatment_text}**, with AUC {approved_cv['roc_auc']:.3f}, sensitivity
  {approved_cv['sensitivity_low']:.3f}, specificity {approved_cv['specificity_high']:.3f},
  and balanced accuracy {approved_cv['balanced_accuracy']:.3f}.
"""

    section5 = f"""
The frozen **{approved['model']} with {treatment_text}** is the approved model. On the
held-out test it achieved AUC {approved_test['roc_auc']:.3f}, sensitivity
{approved_test['sensitivity_low']:.3f}, specificity {approved_test['specificity_high']:.3f},
balanced accuracy {approved_test['balanced_accuracy']:.3f}, and low-class F1
{approved_test['f1_low']:.3f}.

Operationally, it caught {int(approved_test['tp'])} of
{int(approved_test['tp'] + approved_test['fn'])} genuinely low-quality lots, missed
{int(approved_test['fn'])}, and sent {int(approved_test['fp'])} acceptable lots for
unnecessary review. The test set retained its original class distribution and was never
resampled.
"""

    approval_rows = []
    for _, row in test.iterrows():
        passes = (
            row["roc_auc"] >= 0.75
            and row["sensitivity_low"] >= 0.70
            and row["specificity_high"] >= 0.70
        )
        decision = "Approve for controlled pilot" if (
            row["model"] == approved["model"]
            and row["treatment"] == approved["treatment"]
        ) else "Do not approve"
        if decision != "Approve for controlled pilot" and passes:
            reason = "Passes test gates, but was not the CV-selected recommendation"
        elif not passes:
            failed = []
            if row["roc_auc"] < 0.75:
                failed.append("AUC")
            if row["sensitivity_low"] < 0.70:
                failed.append("sensitivity")
            if row["specificity_high"] < 0.70:
                failed.append("specificity")
            reason = "Misses test " + ", ".join(failed) + " gate"
        else:
            reason = "Selected by CV gates, balanced accuracy and interpretability rule"
        approval_rows.append(
            f"| {row['model']} | {row['treatment']} | **{decision}** | {reason} |"
        )
    approval = "\n".join(
        [
            "| Finalist | Treatment | Decision | Reason |",
            "|---|---|---|---|",
            *approval_rows,
        ]
    )

    section6 = f"""
### What went well
- The expanded matrix turned model selection into a controlled comparison: nine families,
  identical folds, three treatment strategies and one set of business gates.
- Running the original distribution first made the effect of SMOTE and class weighting
  measurable rather than assumed.
- The final {approved['model']} recommendation follows the evidence instead of preserving
  the v7 choice by default.

### Challenges
- Classification requires several metrics at once. Higher sensitivity can create more false
  alarms, while higher AUC does not guarantee a useful default threshold.
- Sampling, class weighting and ensemble learning solve different problems. SMOTE changes
  the training distribution, weighting changes error cost, and Random Forest reduces the
  variance of one tree by averaging many trees.
- Naive Bayes variants required different preprocessing because wine chemistry is continuous,
  while Bernoulli expects binary evidence and Multinomial or Complement models expect
  non-negative magnitude features.

### What can be improved in the future
- Estimate the real cost of a missed weak lot, an unnecessary hold and another tasting, then
  calibrate the decision threshold instead of accepting 0.5 automatically.
- Collect real lot IDs, timestamps, process conditions and release outcomes, then validate on
  a later production period or an independent producer.
- Monitor probability calibration, data drift, hold rate, weak-lot escapes and red versus white
  performance during a human-supervised shadow pilot.
"""

    api = (
        f"The current Sommelier API serves the v7 balanced Decision Tree. The v8 approved "
        f"model is {approved['model']} with {treatment_text}, so aligning "
        "the deployed artifact and its parity contract is a documented engineering backlog "
        "item unless that model remains the balanced Decision Tree."
    )
    return {
        "section4": section4,
        "section5": section5,
        "approval": approval,
        "section6": section6,
        "api": api,
    }


source_nb = nbformat.read(SOURCE, as_version=4)
nb = nbformat.v4.new_notebook(metadata=deepcopy(source_nb.metadata))

# Sections 0-3 are retained from v7. Outputs are cleared and paths become v8.
for source_cell in source_nb.cells[:27]:
    cell = deepcopy(source_cell)
    cell.source = clean_text(cell.source)
    if cell.cell_type == "code":
        cell.outputs = []
        cell.execution_count = None
    nb.cells.append(cell)

nb.cells[1].source = nb.cells[1].source.replace(
    "Decision Tree Classification and CRISP-DM",
    "Comparative Classification and CRISP-DM",
).replace(
    "| Required algorithm | Decision Tree - default, AUC-tuned and balanced variants |",
    "| Required algorithm | Decision Tree, expanded into a nine-family comparison |",
).replace(
    "| Sensitivity studies | Leakage-safe SMOTE and kernel SVM benchmark |",
    "| Experiment | Original, fold-only SMOTE and class-weighted training arms |",
).replace(
    "every model is framed as an interpretable decision-support tool",
    "every model is framed as a decision-support candidate with post-selection explanation",
)
nb.cells[3].source = nb.cells[3].source.replace(
    "Among candidates passing every gate, priority goes to sensitivity, then balanced accuracy, interpretability, and simplicity.",
    "Among candidates passing every gate, balanced accuracy ranks them. A technical tie below 0.01 is resolved by interpretability, followed by simplicity.",
)

narrative = result_narratives()

nb.cells.extend([
    markdown(r"""
## 4. Modelling
"""),
    markdown(r"""
### 4.1 Candidate models and rationale

The Decision Tree remains the required algorithm, but the post-submission discussion with
Dr Kamran identified a stronger experiment: compare several model families first on the
original training distribution, then with SMOTE, and finally with class weighting where the
algorithm supports it. Every comparison uses the same five stratified folds and ROC-AUC tuning.

| Model | What it tests | Required preprocessing |
|---|---|---|
| Logistic Regression | Interpretable linear probability boundary | StandardScaler |
| KNN | Local nonlinear relationships; sensitive to scale and 12 dimensions | StandardScaler |
| Decision Tree | Directly readable rules and feature interactions | None |
| SVM | Maximum-margin linear and nonlinear boundaries | StandardScaler |
| GaussianNB | Continuous measurements represented by class-conditional Gaussian distributions | None |
| BernoulliNB | Information loss when each measurement becomes above or below its training median | Fold-fitted median binarizer |
| MultinomialNB | Non-negative magnitude evidence under a count-like assumption | MinMaxScaler |
| ComplementNB | Naive Bayes variant designed to reduce imbalance effects in count-like data | MinMaxScaler |
| Random Forest | Ensemble averaging of many trees to reduce variance | None |

The majority classifier remains the no-skill baseline. Bernoulli, Multinomial and Complement
Naive Bayes are assumption stress tests: their fit to continuous laboratory measurements must
be judged from evidence, not presumed.
"""),
    code(r"""
# 4.1 - Shared experiment definitions
import json
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.naive_bayes import BernoulliNB, ComplementNB, GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler


class MedianBinarizer(BaseEstimator, TransformerMixin):
    'Learn feature medians from one training fold, then return binary evidence.'

    def fit(self, X_values, y_values=None):
        values = np.asarray(X_values)
        self.medians_ = np.median(values, axis=0)
        self.n_features_in_ = values.shape[1]
        return self

    def transform(self, X_values):
        return (np.asarray(X_values) > self.medians_).astype(float)


CV = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
cv_scoring = {
    "roc_auc": "roc_auc",
    "sensitivity_low": make_scorer(recall_score, pos_label=1),
    "specificity_high": make_scorer(recall_score, pos_label=0),
    "balanced_accuracy": "balanced_accuracy",
    "f1_low": "f1",
}

MODEL_SPECS = {
    "Logistic Regression": {
        "preprocess": StandardScaler(),
        "model": LogisticRegression(max_iter=5000, solver="liblinear", random_state=RANDOM_STATE),
        "grid": {"model__C": [0.01, 0.1, 1, 10]},
    },
    "KNN": {
        "preprocess": StandardScaler(),
        "model": KNeighborsClassifier(),
        "grid": {
            "model__n_neighbors": [5, 11, 21, 31],
            "model__weights": ["uniform", "distance"],
        },
    },
    "Decision Tree": {
        "preprocess": "passthrough",
        "model": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "grid": {
            "model__max_depth": [3, 4, 5, 6, 8, None],
            "model__min_samples_leaf": [1, 5, 10, 20],
            "model__criterion": ["gini", "entropy"],
        },
    },
    "SVM": {
        "preprocess": StandardScaler(),
        "model": SVC(probability=True, random_state=RANDOM_STATE),
        "grid": {
            "model__kernel": ["rbf", "linear"],
            "model__C": [0.1, 1, 10],
        },
    },
    "GaussianNB": {
        "preprocess": "passthrough",
        "model": GaussianNB(),
        "grid": {"model__var_smoothing": [1e-9, 1e-7]},
    },
    "BernoulliNB": {
        "preprocess": MedianBinarizer(),
        "model": BernoulliNB(binarize=0.5),
        "grid": {"model__alpha": [0.1, 1.0]},
    },
    "MultinomialNB": {
        "preprocess": MinMaxScaler(),
        "model": MultinomialNB(),
        "grid": {"model__alpha": [0.1, 1.0]},
    },
    "ComplementNB": {
        "preprocess": MinMaxScaler(),
        "model": ComplementNB(),
        "grid": {"model__alpha": [0.1, 1.0]},
    },
    "Random Forest": {
        "preprocess": "passthrough",
        "model": RandomForestClassifier(
            n_estimators=200, random_state=RANDOM_STATE, n_jobs=1
        ),
        "grid": {
            "model__max_depth": [None, 10, 5],
            "model__min_samples_leaf": [1, 5, 20],
        },
    },
}

WEIGHTED_MODELS = {"Logistic Regression", "Decision Tree", "SVM", "Random Forest"}
matrix_rows = []
searches = {}
fitted_models = {}


def build_candidate(model_name, treatment):
    spec = MODEL_SPECS[model_name]
    estimator = clone(spec["model"])
    if treatment == "Class weight":
        estimator.set_params(class_weight="balanced")
    steps = [("preprocess", clone(spec["preprocess"]) if spec["preprocess"] != "passthrough" else "passthrough")]
    if treatment == "SMOTE":
        steps.append(("smote", SMOTE(random_state=RANDOM_STATE)))
    steps.append(("model", estimator))
    return ImbPipeline(steps)


def run_search(model_name, treatment, X_values=X_train, y_values=y_train):
    candidate = build_candidate(model_name, treatment)
    search = GridSearchCV(
        candidate,
        MODEL_SPECS[model_name]["grid"],
        scoring=cv_scoring,
        refit="roc_auc",
        cv=CV,
        n_jobs=1,
        return_train_score=False,
        error_score="raise",
    )
    search.fit(X_values, y_values)
    index = search.best_index_
    row = {
        "model": model_name,
        "treatment": treatment,
        "roc_auc": search.cv_results_["mean_test_roc_auc"][index],
        "roc_auc_std": search.cv_results_["std_test_roc_auc"][index],
        "sensitivity_low": search.cv_results_["mean_test_sensitivity_low"][index],
        "sensitivity_low_std": search.cv_results_["std_test_sensitivity_low"][index],
        "specificity_high": search.cv_results_["mean_test_specificity_high"][index],
        "specificity_high_std": search.cv_results_["std_test_specificity_high"][index],
        "balanced_accuracy": search.cv_results_["mean_test_balanced_accuracy"][index],
        "balanced_accuracy_std": search.cv_results_["std_test_balanced_accuracy"][index],
        "f1_low": search.cv_results_["mean_test_f1_low"][index],
        "f1_low_std": search.cv_results_["std_test_f1_low"][index],
        "best_params": json.dumps(search.best_params_, sort_keys=True),
    }
    matrix_rows.append(row)
    searches[(model_name, treatment)] = search
    fitted_models[(model_name, treatment)] = search.best_estimator_
    return row


print("Table 4.1 - Candidate families and experimental controls")
print("Nine model families will use the same folds, metrics and held-out boundary.")
display(pd.DataFrame({
    "Model": list(MODEL_SPECS),
    "Original": "Yes",
    "SMOTE": "Yes",
    "Class weight": ["Yes" if name in WEIGHTED_MODELS else "Not supported"
                     for name in MODEL_SPECS],
}).set_index("Model"))
"""),
    markdown(r"""
### 4.2 Experiment A - original distribution

This arm makes no attempt to balance the classes. Scaling, median binarisation and
non-negative scaling are model requirements, not balancing. Hyperparameters are selected by
five-fold ROC-AUC on the training partition only. The SVM search retains RBF and linear kernels;
poly and sigmoid were already weaker in v7 and are not repeated.
"""),
    code(r"""
# 4.2 - Original training distribution
dummy_scores = cross_validate(
    DummyClassifier(strategy="most_frequent"), X_train, y_train,
    cv=CV, scoring=cv_scoring, n_jobs=1,
)
matrix_rows.append({
    "model": "Majority baseline",
    "treatment": "Original",
    **{metric: dummy_scores["test_" + metric].mean() for metric in cv_scoring},
    **{metric + "_std": dummy_scores["test_" + metric].std() for metric in cv_scoring},
    "best_params": "{}",
})

original_rows = [run_search(model_name, "Original") for model_name in MODEL_SPECS]
original_display = pd.DataFrame(original_rows).set_index("model")
print("Table 4.2 - Original-distribution tuning results (training CV)")
print("This is the untreated reference needed to measure every balancing trade-off.")
display(original_display[["roc_auc", "sensitivity_low", "specificity_high",
                          "balanced_accuracy", "f1_low"]].round(3))
"""),
    markdown(r"""
### 4.3 Experiment B - SMOTE

SMOTE is inside the imbalanced-learn pipeline. For every validation rotation, preprocessing
and synthetic observations are learned from that fold's training portion only:

```text
CV training fold -> preprocessing -> SMOTE -> classifier
CV validation fold --------------------------> scoring
Held-out test set ----------------------------> final evaluation only
```

The held-out test set remains outside both GridSearchCV and SMOTE. It keeps the original class
distribution and is never resampled.
"""),
    code(r"""
# 4.3 - SMOTE inside each training fold
smote_rows = [run_search(model_name, "SMOTE") for model_name in MODEL_SPECS]
smote_display = pd.DataFrame(smote_rows).set_index("model")
print("Table 4.3 - SMOTE tuning results (training CV)")
print("Synthetic minority observations exist only inside each training fold.")
display(smote_display[["roc_auc", "sensitivity_low", "specificity_high",
                       "balanced_accuracy", "f1_low"]].round(3))
"""),
    markdown(r"""
### 4.4 Experiment C - class weighting

Logistic Regression, Decision Tree, SVM and Random Forest support
`class_weight="balanced"`. This arm changes the cost of minority-class errors without adding
or deleting observations. KNN and the Naive Bayes estimators do not expose the same parameter,
so manufacturing an equivalent would make the comparison less clear.
"""),
    code(r"""
# 4.4 - Cost-sensitive training without synthetic observations
weighted_rows = [run_search(model_name, "Class weight")
                 for model_name in MODEL_SPECS if model_name in WEIGHTED_MODELS]
weighted_display = pd.DataFrame(weighted_rows).set_index("model")
print("Table 4.4 - Class-weight tuning results (training CV)")
print("Weights alter error cost while preserving every original training observation.")
display(weighted_display[["roc_auc", "sensitivity_low", "specificity_high",
                          "balanced_accuracy", "f1_low"]].round(3))
"""),
    markdown(r"""
### 4.5 Treatment comparison

The master table combines all model-treatment pairs. The delta table then subtracts each
model's untreated result, so a gain in sensitivity can be read beside any loss in specificity
or AUC. The plot draws the same change as an arrow from Original to SMOTE.
"""),
    code(r"""
# 4.5.1 - Master CV matrix and treatment deltas
model_matrix = pd.DataFrame(matrix_rows)
model_matrix["passes_auc"] = model_matrix["roc_auc"] >= 0.75
model_matrix["passes_sensitivity"] = model_matrix["sensitivity_low"] >= 0.70
model_matrix["passes_specificity"] = model_matrix["specificity_high"] >= 0.70
model_matrix["passes_all_gates"] = model_matrix[
    ["passes_auc", "passes_sensitivity", "passes_specificity"]
].all(axis=1)
model_matrix.to_csv(OUTPUT_DIR / "model_matrix_cv_v8.csv", index=False)

delta_rows = []
for model_name in MODEL_SPECS:
    original = model_matrix[
        (model_matrix["model"] == model_name)
        & (model_matrix["treatment"] == "Original")
    ].iloc[0]
    for treatment in ("SMOTE", "Class weight"):
        treated = model_matrix[
            (model_matrix["model"] == model_name)
            & (model_matrix["treatment"] == treatment)
        ]
        if treated.empty:
            continue
        treated = treated.iloc[0]
        delta_rows.append({
            "model": model_name,
            "comparison": treatment + " - Original",
            "delta_sensitivity_low": treated["sensitivity_low"] - original["sensitivity_low"],
            "delta_specificity_high": treated["specificity_high"] - original["specificity_high"],
            "delta_balanced_accuracy": treated["balanced_accuracy"] - original["balanced_accuracy"],
            "delta_f1_low": treated["f1_low"] - original["f1_low"],
            "delta_roc_auc": treated["roc_auc"] - original["roc_auc"],
        })
treatment_deltas = pd.DataFrame(delta_rows)
treatment_deltas.to_csv(OUTPUT_DIR / "treatment_deltas_v8.csv", index=False)

print("Table 4.5 - Master model-treatment matrix (training CV)")
print("The gates are applied before any held-out test result is opened.")
display(model_matrix[["model", "treatment", "roc_auc", "sensitivity_low",
                      "specificity_high", "balanced_accuracy", "f1_low",
                      "passes_all_gates"]].round(3))

print("\nTable 4.6 - Treatment deltas against each untreated model")
print("Positive sensitivity with negative specificity quantifies the review-workload trade-off.")
display(treatment_deltas.round(3))
"""),
    code(r"""
# 4.5.2 - Sensitivity-specificity movement caused by SMOTE
fig, ax = plt.subplots(figsize=(10, 7))
palette = sns.color_palette("tab10", n_colors=len(MODEL_SPECS))
for colour, model_name in zip(palette, MODEL_SPECS):
    original = model_matrix[(model_matrix["model"] == model_name)
                            & (model_matrix["treatment"] == "Original")].iloc[0]
    smote = model_matrix[(model_matrix["model"] == model_name)
                         & (model_matrix["treatment"] == "SMOTE")].iloc[0]
    ax.scatter(original["specificity_high"], original["sensitivity_low"],
               color=colour, marker="o", s=55)
    ax.scatter(smote["specificity_high"], smote["sensitivity_low"],
               color=colour, marker="X", s=75, label=model_name)
    ax.annotate("", xy=(smote["specificity_high"], smote["sensitivity_low"]),
                xytext=(original["specificity_high"], original["sensitivity_low"]),
                arrowprops={"arrowstyle": "->", "color": colour, "lw": 1.3})
ax.axhline(0.70, color="grey", linestyle="--", linewidth=1)
ax.axvline(0.70, color="grey", linestyle="--", linewidth=1)
ax.set_xlabel("Specificity for high-quality lots")
ax.set_ylabel("Sensitivity for low-quality lots")
ax.set_title("Figure 4.1 - Original to SMOTE operating-point movement")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", title="SMOTE endpoint")
plt.tight_layout()
plt.savefig(FIG_DIR / "v8_sampling_tradeoffs.png", dpi=120, bbox_inches="tight")
plt.show()
print("Figure 4.1 - Circles are Original; X markers are SMOTE; arrows show the change.")
"""),
    markdown(r"""
### 4.6 Gates and finalist selection

The original v7 gates remain unchanged: AUC at least 0.75, sensitivity at least 0.70 and
specificity at least 0.70. Among candidates passing all gates, balanced accuracy ranks them.
Scores within 0.01 are treated as a technical tie and resolved by interpretability: one tree's
rules first, then linear coefficients or simple class distributions, then ensemble or local
similarity models.

Four roles are frozen from training CV: best untreated, best SMOTE, best class-weighted and best
ensemble. Duplicate winners appear only once in the held-out evaluation.
"""),
    code(r"""
# 4.6 - Apply gates and freeze finalists without reading X_test
INTERPRETABILITY_RANK = {
    "Decision Tree": 1,
    "Logistic Regression": 2,
    "GaussianNB": 3,
    "BernoulliNB": 4,
    "MultinomialNB": 5,
    "ComplementNB": 6,
    "Random Forest": 7,
    "SVM": 8,
    "KNN": 9,
}


def best_in_pool(pool):
    passing = pool[pool["passes_all_gates"]]
    candidates = passing if not passing.empty else pool
    return candidates.sort_values(
        ["balanced_accuracy", "roc_auc"], ascending=False
    ).iloc[0]


role_pools = {
    "best untreated": model_matrix[
        (model_matrix["treatment"] == "Original")
        & (model_matrix["model"] != "Majority baseline")
    ],
    "best SMOTE": model_matrix[model_matrix["treatment"] == "SMOTE"],
    "best class weighted": model_matrix[model_matrix["treatment"] == "Class weight"],
    "best ensemble": model_matrix[model_matrix["model"] == "Random Forest"],
}
role_winners = []
for role, pool in role_pools.items():
    winner = best_in_pool(pool)
    role_winners.append({"role": role, "model": winner["model"],
                         "treatment": winner["treatment"]})

passing = model_matrix[model_matrix["passes_all_gates"]].copy()
if passing.empty:
    approved = model_matrix.sort_values("balanced_accuracy", ascending=False).iloc[0]
else:
    best_balanced_accuracy = passing["balanced_accuracy"].max()
    tied = passing[
        passing["balanced_accuracy"] >= best_balanced_accuracy - 0.01
    ].copy()
    tied["interpretability_rank"] = tied["model"].map(INTERPRETABILITY_RANK)
    approved = tied.sort_values(
        ["interpretability_rank", "balanced_accuracy"], ascending=[True, False]
    ).iloc[0]

role_winners.append({"role": "approved", "model": approved["model"],
                     "treatment": approved["treatment"]})
selection_summary = pd.DataFrame(role_winners)
selection_summary.to_csv(OUTPUT_DIR / "selection_summary_v8.csv", index=False)

finalist_keys = []
for row in role_winners:
    key = (row["model"], row["treatment"])
    if key not in finalist_keys:
        finalist_keys.append(key)
approved_key = (approved["model"], approved["treatment"])

print("Table 4.7 - Frozen finalist roles from training CV")
print("The held-out test remains unopened while these roles and the recommendation are fixed.")
display(selection_summary)
print("\nApproved from CV:", approved_key)
"""),
    markdown(r"""
### 4.7 Feature ablation

The v7 sulfur experiment remains, now applied to the CV-approved model. Bound SO2 and the free
SO2 ratio are added together, the complete model pipeline is re-tuned, and the pair is retained
only if AUC or balanced accuracy improves by at least 0.01 without reducing sensitivity or
specificity by more than 0.02.
"""),
    code(r"""
# 4.7 - Training-only feature ablation on the CV-approved model
def add_sulfur_features(frame):
    result = frame.copy()
    result["bound_sulfur_dioxide"] = (
        result["total sulfur dioxide"] - result["free sulfur dioxide"]
    )
    result["free_so2_ratio"] = (
        result["free sulfur dioxide"] / result["total sulfur dioxide"]
    )
    return result


X_train_engineered = add_sulfur_features(X_train)
engineered_search = GridSearchCV(
    build_candidate(*approved_key),
    MODEL_SPECS[approved_key[0]]["grid"],
    scoring=cv_scoring,
    refit="roc_auc",
    cv=CV,
    n_jobs=1,
    error_score="raise",
)
engineered_search.fit(X_train_engineered, y_train)
engineered_index = engineered_search.best_index_
engineered_metrics = {
    metric: engineered_search.cv_results_["mean_test_" + metric][engineered_index]
    for metric in cv_scoring
}
base_metrics = model_matrix[
    (model_matrix["model"] == approved_key[0])
    & (model_matrix["treatment"] == approved_key[1])
].iloc[0]
auc_gain = engineered_metrics["roc_auc"] - base_metrics["roc_auc"]
balanced_gain = engineered_metrics["balanced_accuracy"] - base_metrics["balanced_accuracy"]
material_gain = max(auc_gain, balanced_gain)
retained = bool(
    material_gain >= 0.01
    and engineered_metrics["sensitivity_low"] >= base_metrics["sensitivity_low"] - 0.02
    and engineered_metrics["specificity_high"] >= base_metrics["specificity_high"] - 0.02
)

feature_ablation = pd.DataFrame([
    {
        "feature_set": "Base 12 features",
        "roc_auc": base_metrics["roc_auc"],
        "sensitivity_low": base_metrics["sensitivity_low"],
        "specificity_high": base_metrics["specificity_high"],
        "balanced_accuracy": base_metrics["balanced_accuracy"],
        "material_gain": 0.0,
        "retained": not retained,
    },
    {
        "feature_set": "Base + bound SO2 + free SO2 ratio",
        **engineered_metrics,
        "material_gain": material_gain,
        "retained": retained,
    },
])
feature_ablation.to_csv(OUTPUT_DIR / "feature_ablation_v8.csv", index=False)
approved_uses_engineered = retained
if retained:
    fitted_models[approved_key] = engineered_search.best_estimator_

print("Table 4.8 - Feature ablation on the CV-approved pipeline")
print("The 0.01 materiality rule decides whether two extra sulfur features earn their cost.")
display(feature_ablation.round(4))
"""),
    markdown(narrative["section4"]),
    markdown(r"""
## 5. Evaluation
"""),
    markdown(r"""
The test partition is opened only after the model matrix, gates, finalist roles and feature
ablation are frozen. It is used with its original distribution and is never resampled. The
finalist table answers whether each training-CV result generalises to unseen observations.
"""),
    code(r"""
# 5.0 - Evaluate only the frozen unique finalists on the untouched test set
def model_scores(model, X_values):
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X_values)[:, 1]
    return model.decision_function(X_values)


def class_metrics(model, X_values, y_values):
    prediction = model.predict(X_values)
    score = model_scores(model, X_values)
    tn, fp, fn, tp = confusion_matrix(y_values, prediction, labels=[0, 1]).ravel()
    sensitivity = recall_score(y_values, prediction, pos_label=1)
    specificity = recall_score(y_values, prediction, pos_label=0)
    return {
        "accuracy": accuracy_score(y_values, prediction),
        "precision_low": precision_score(y_values, prediction, pos_label=1, zero_division=0),
        "sensitivity_low": sensitivity,
        "specificity_high": specificity,
        "f1_low": f1_score(y_values, prediction, pos_label=1, zero_division=0),
        "balanced_accuracy": balanced_accuracy_score(y_values, prediction),
        "g_mean": np.sqrt(sensitivity * specificity),
        "roc_auc": roc_auc_score(y_values, score),
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
    }


test_rows = []
for model_name, treatment in finalist_keys:
    X_final_test = (
        add_sulfur_features(X_test)
        if (model_name, treatment) == approved_key and approved_uses_engineered
        else X_test
    )
    test_rows.append({
        "model": model_name,
        "treatment": treatment,
        **class_metrics(fitted_models[(model_name, treatment)], X_final_test, y_test),
    })
finalist_test = pd.DataFrame(test_rows)
finalist_test.to_csv(OUTPUT_DIR / "finalist_test_metrics_v8.csv", index=False)

print("Table 5.1 - Frozen finalists on the untouched held-out test")
print("These are the only candidates evaluated after the CV decision was frozen.")
display(finalist_test[["model", "treatment", "accuracy", "precision_low",
                       "sensitivity_low", "specificity_high", "f1_low",
                       "balanced_accuracy", "g_mean", "roc_auc"]].round(3))
"""),
    code(r"""
# 5.0.1 - ROC curves for frozen finalists
plt.figure(figsize=(8, 6))
for model_name, treatment in finalist_keys:
    X_final_test = (
        add_sulfur_features(X_test)
        if (model_name, treatment) == approved_key and approved_uses_engineered
        else X_test
    )
    score = model_scores(fitted_models[(model_name, treatment)], X_final_test)
    fpr, tpr, _ = roc_curve(y_test, score, pos_label=1)
    auc = roc_auc_score(y_test, score)
    plt.plot(fpr, tpr, linewidth=2,
             label=f"{model_name}, {treatment} (AUC = {auc:.3f})")
plt.plot([0, 1], [0, 1], "k--", label="Random (AUC = 0.500)")
plt.xlabel("False-positive rate (1 - specificity)")
plt.ylabel("True-positive rate (sensitivity)")
plt.title("Figure 5.1 - Frozen-finalist ROC curves")
plt.legend(loc="lower right", fontsize=8)
plt.tight_layout()
plt.savefig(FIG_DIR / "v8_finalist_roc.png", dpi=120)
plt.show()
print("Figure 5.1 - ROC compares ranking; the confusion matrices show the operating point.")
"""),
    code(r"""
# 5.0.2 - Confusion matrices for frozen finalists
n_finalists = len(finalist_keys)
fig, axes = plt.subplots(1, n_finalists, figsize=(5 * n_finalists, 4.2))
axes = np.atleast_1d(axes)
for ax, (model_name, treatment) in zip(axes, finalist_keys):
    X_final_test = (
        add_sulfur_features(X_test)
        if (model_name, treatment) == approved_key and approved_uses_engineered
        else X_test
    )
    prediction = fitted_models[(model_name, treatment)].predict(X_final_test)
    cm = confusion_matrix(y_test, prediction, labels=[0, 1])
    ConfusionMatrixDisplay(cm, display_labels=["high", "low"]).plot(
        ax=ax, cmap="Blues", colorbar=False
    )
    ax.set_title(f"{model_name}\n{treatment}")
fig.suptitle("Figure 5.2 - Frozen-finalist confusion matrices", y=1.04)
plt.tight_layout()
plt.savefig(FIG_DIR / "v8_finalist_confusion_matrices.png", dpi=120,
            bbox_inches="tight")
plt.show()
print("Figure 5.2 - FN is a weak lot missed; FP is an acceptable lot sent to review.")
"""),
    code(r"""
# 5.0.3 - Classification report for the approved model
approved_model = fitted_models[approved_key]
X_approved_train = add_sulfur_features(X_train) if approved_uses_engineered else X_train
X_approved_test = add_sulfur_features(X_test) if approved_uses_engineered else X_test
approved_prediction = approved_model.predict(X_approved_test)
approved_report = pd.DataFrame(classification_report(
    y_test,
    approved_prediction,
    target_names=["high (>=6)", "low (<6)"],
    output_dict=True,
    zero_division=0,
)).T.round(3)
approved_report.to_csv(OUTPUT_DIR / "classification_report_v8.csv")
print("Table 5.2 - Classification report for the CV-approved model")
print("The low-class row is the operational screening result; accuracy alone is insufficient.")
display(approved_report)
"""),
    markdown(r"""
### 5.1 Explainable AI

The explanation method follows the approved model instead of forcing every model into a tree
explanation. Tree-based winners use `TreeExplainer`; Logistic Regression uses coefficients and
`LinearExplainer`. A model-agnostic SHAP fallback remains available if another family wins.
Every explanation targets class 1, which is low quality.
"""),
    code(r"""
# 5.1.1 - Prepare class-1 explanations for the approved pipeline
def transform_for_estimator(pipeline, frame):
    transformed = frame
    for _, step in pipeline.steps[:-1]:
        if hasattr(step, "transform"):
            transformed = step.transform(transformed)
    return np.asarray(transformed)


approved_model_name, approved_treatment = approved_key
approved_estimator = approved_model.named_steps["model"]
approved_feature_names = list(X_approved_test.columns)
X_train_model = transform_for_estimator(approved_model, X_approved_train)
X_test_model = transform_for_estimator(approved_model, X_approved_test)

if approved_model_name in {"Decision Tree", "Random Forest"}:
    explanation_kind = "tree probability"
    explanation_limit = min(len(X_test_model), 500 if approved_model_name == "Random Forest" else len(X_test_model))
    explained_positions = np.arange(explanation_limit)
    explainer = shap.TreeExplainer(approved_estimator)
    shap_all = explainer(X_test_model[explained_positions])
    if shap_all.values.ndim == 3:
        low_index = list(approved_estimator.classes_).index(1)
        low_values = shap_all.values[:, :, low_index]
        base_values = np.asarray(shap_all.base_values)
        low_base = base_values[:, low_index] if base_values.ndim == 2 else np.repeat(
            base_values[low_index], explanation_limit
        )
    else:
        low_values = shap_all.values
        low_base = shap_all.base_values
    low_shap = shap.Explanation(
        values=low_values,
        base_values=low_base,
        data=X_test_model[explained_positions],
        feature_names=approved_feature_names,
    )
    target_score = approved_estimator.predict_proba(
        X_test_model[explained_positions]
    )[:, list(approved_estimator.classes_).index(1)]
elif approved_model_name == "Logistic Regression":
    explanation_kind = "linear log-odds"
    explained_positions = np.arange(len(X_test_model))
    background = shap.sample(X_train_model, min(300, len(X_train_model)), random_state=RANDOM_STATE)
    explainer = shap.LinearExplainer(approved_estimator, background)
    low_shap = explainer(X_test_model)
    target_score = approved_estimator.decision_function(X_test_model)
else:
    explanation_kind = "model-agnostic probability"
    explained_positions = np.arange(min(200, len(X_test_model)))
    background = shap.sample(X_train_model, min(100, len(X_train_model)), random_state=RANDOM_STATE)
    explainer = shap.Explainer(
        lambda values: approved_estimator.predict_proba(values)[:, 1],
        background,
        feature_names=approved_feature_names,
    )
    low_shap = explainer(X_test_model[explained_positions])
    target_score = approved_estimator.predict_proba(
        X_test_model[explained_positions]
    )[:, 1]

reconstructed_score = np.asarray(low_shap.base_values) + np.asarray(low_shap.values).sum(axis=1)
max_additivity_error = float(np.max(np.abs(reconstructed_score - target_score)))
print("Explanation method:", explanation_kind)
print("Explained held-out rows:", len(explained_positions))
print("Maximum additivity error: %.2e" % max_additivity_error)
"""),
    markdown(r"""
**Interpretation:**

- The explanation method is selected from the approved model family.
- The additivity check verifies that the feature contributions reconstruct the explained
  class-1 score at machine precision for tree and linear explainers.
- For Random Forest, a fixed held-out sample limits explanation cost without entering training.
"""),
    code(r"""
# 5.1.2 - Global class-1 SHAP importance and direction
shap_global = pd.DataFrame({
    "feature": approved_feature_names,
    "mean_absolute_shap": np.abs(low_shap.values).mean(axis=0),
}).sort_values("mean_absolute_shap", ascending=False).reset_index(drop=True)
shap_global.to_csv(OUTPUT_DIR / "shap_global_importance_v8.csv", index=False)

print("Table 5.3 - Global SHAP importance for the approved model")
print("Mean absolute SHAP ranks which laboratory measurements move low-quality risk most.")
display(shap_global.round(4))

shap.plots.beeswarm(low_shap, max_display=min(14, len(approved_feature_names)), show=False)
plt.title("Figure 5.3 - Global SHAP direction of low-quality risk")
plt.tight_layout()
plt.savefig(FIG_DIR / "v8_shap_global.png", dpi=120, bbox_inches="tight")
plt.show()
"""),
    markdown(r"""
**Interpretation:**

- Mean absolute SHAP ranks overall influence; the beeswarm adds direction and distribution.
- Positive values push the score toward class 1, meaning higher low-quality risk.
- These are model associations, not evidence that changing one chemical measurement will cause
  a sensory-quality change.
"""),
    code(r"""
# 5.1.3 - Local explanation of one correctly flagged low-quality lot
explained_y = y_test.iloc[explained_positions].to_numpy()
explained_prediction = approved_model.predict(X_approved_test.iloc[explained_positions])
true_positive_positions = np.flatnonzero(
    (explained_y == 1) & (explained_prediction == 1)
)
if len(true_positive_positions):
    explained_probabilities = approved_model.predict_proba(
        X_approved_test.iloc[explained_positions]
    )[:, list(approved_model.classes_).index(1)]
    tp_probabilities = explained_probabilities[true_positive_positions]
    local_position = int(true_positive_positions[
        np.argmin(np.abs(tp_probabilities - np.median(tp_probabilities)))
    ])
else:
    local_position = int(np.argmax(target_score))

local_explanation = low_shap[local_position]
local_table = pd.DataFrame({
    "feature": approved_feature_names,
    "value": X_test_model[explained_positions[local_position]],
    "shap_toward_low_quality": local_explanation.values,
}).assign(
    absolute_shap=lambda frame: frame["shap_toward_low_quality"].abs()
).sort_values("absolute_shap", ascending=False).drop(
    columns="absolute_shap"
).reset_index(drop=True)
local_table.to_csv(OUTPUT_DIR / "shap_local_example_v8.csv", index=False)

source_position = explained_positions[local_position]
source_index = X_test.index[source_position]
local_probability = approved_model.predict_proba(
    X_approved_test.iloc[[source_position]]
)[0, list(approved_model.classes_).index(1)]
print("Representative correctly flagged low-quality lot: row", source_index)
print("Predicted low-quality probability: %.3f" % local_probability)
print("Table 5.4 - Local SHAP decomposition")
print("The largest positive and negative contributions explain why this lot was reviewed.")
display(local_table.head(6).round(4))

shap.plots.waterfall(local_explanation, max_display=min(14, len(approved_feature_names)), show=False)
plt.title("Figure 5.4 - Local SHAP explanation of one flagged lot")
plt.tight_layout()
plt.savefig(FIG_DIR / "v8_shap_local.png", dpi=120, bbox_inches="tight")
plt.show()
"""),
    markdown(r"""
**Interpretation:**

- This local explanation answers why one specific lot crossed the review threshold.
- Quality-control staff can verify the dominant measurements against the laboratory record.
- Human review remains necessary because a plausible model explanation is not a causal finding.
"""),
    markdown("### 5.2 Operational result"),
    markdown(narrative["section5"]),
    markdown("### 5.3 Approval decision"),
    markdown(narrative["approval"] + "\n\nApproval means human-supervised triage, not automated release or rejection. Threshold calibration remains deferred until real business costs are available."),
    markdown("## 6. Deployment / Lessons Learned"),
    markdown(narrative["section6"]),
])

# Keep declarations and references, then replace the glossary and API note for v8.
for index in (60, 61, 62):
    cell = deepcopy(source_nb.cells[index])
    cell.source = clean_text(cell.source)
    nb.cells.append(cell)

nb.cells.extend([
    markdown(r"""
## Appendix A - Glossary

| Term | Meaning in this assessment |
|---|---|
| Cross-validation (CV) | Five repeated train-validation rotations inside the training partition |
| Held-out test set | Untouched 20% used only after finalist selection; never resampled |
| ROC-AUC | Ability to rank low-quality samples above high-quality samples across thresholds |
| Sensitivity | Share of genuinely low-quality lots correctly flagged |
| Specificity | Share of genuinely high-quality lots correctly cleared |
| Precision | Share of low-quality flags that are correct |
| Balanced accuracy | Mean of sensitivity and specificity |
| Class imbalance | Unequal frequency: 37.4% low versus 62.6% high after deduplication |
| Original treatment | Training on the observed class distribution without balancing |
| SMOTE | Synthetic minority observations created only inside CV training folds |
| Class weighting | Higher error cost for the minority class without synthetic observations |
| Ensemble learning | Combining multiple learners; Random Forest averages many trees |
| Logistic Regression | Linear classifier producing class probabilities from weighted features |
| KNN | Classifier based on nearby training observations in feature space |
| GaussianNB | Naive Bayes variant for continuous Gaussian feature distributions |
| BernoulliNB | Naive Bayes variant for binary evidence |
| MultinomialNB | Naive Bayes variant designed for non-negative count-like magnitude features |
| ComplementNB | Naive Bayes variant using complement-class statistics to reduce imbalance bias |
| Leakage | Validation or test information entering model training or preprocessing |
| SHAP | Additive contributions explaining how features move a model score |
| Human-supervised pilot | Model routes review while staff retain release authority |
"""),
    markdown(r"""
## Appendix B - Sommelier API proof of concept

The existing portfolio project serves the same UCI workflow through FastAPI and Streamlit. It
demonstrates engineering delivery, not external model validation.

| Layer | Technology | Notes |
|---|---|---|
| ML core | scikit-learn 1.9.0, joblib | Deterministic training from 5,320 deduplicated rows |
| API | FastAPI, Uvicorn, Pydantic | Validated REST scoring and model provenance |
| Interface | Streamlit | Public interface with local inference and API fallback |
| Repository | github.com/lfariabr/sommelier-api | Source, parity tests and release notes |

""" + narrative["api"] + r"""

Per-lot explanations, prediction storage, threshold calibration and drift monitoring remain
future pilot work.
"""),
    markdown("## Appendix C - Wine Lot Review Pipeline"),
])

pipeline_image = deepcopy(source_nb.cells[66])
pipeline_image.source = clean_text(pipeline_image.source)
nb.cells.append(pipeline_image)

for cell in nb.cells:
    cell.source = clean_text(cell.source)
    if cell.cell_type == "code":
        cell.outputs = []
        cell.execution_count = None

nbformat.write(nb, TARGET)
print(f"Wrote {TARGET} with {len(nb.cells)} cells")
