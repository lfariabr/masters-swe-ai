# Module 7 - Learning Activities (executed)

The Module 7 activity briefs point at hosted demos that are **dead or Colab-locked**:

| Brief says | Reality | What we did |
|---|---|---|
| Run the What-If Tool Colab notebooks | Colab-only, needs `witwidget` + TensorFlow | rebuilt WIT's 5 probes in plain scikit-learn |
| Explore `aix360.mybluemix.net` | IBM Bluemix retired; HELOC needs registration | rebuilt **CEM** + **Protodash** from scratch on German Credit |
| Interact with `titanicexplainer.herokuapp.com` | Heroku killed free dynos in 2022 | rebuilt the dashboard's 4 panels with SHAP |

So these notebooks reproduce the **substance** of each activity locally. They all execute end-to-end.

## The notebooks

| Notebook | Dataset | The point |
|---|---|---|
| `activity1_what_if_wine.ipynb` | **wine quality** (same as Assessment 2) | probe a model without a UI: model comparison, datapoint editor, **counterfactuals**, PDP, slice performance, threshold sweep |
| `activity2_bank_loan_explainability.ipynb` | German Credit (`credit-g`, 1,000 loans) | **one decision, four audiences, four explanations** - officer (global rules), rejected customer (**CEM**), data scientist (**SHAP**), regulator (**Protodash**) |
| `activity3_shap_titanic.ipynb` | Titanic (OpenML) | SHAP end to end: **global** importance/beeswarm/dependence vs **local** waterfall - plus a leakage trap |
| `activity4_eli5_lime_mlxtend.ipynb` | wine | Eli5 / LIME / Mlxtend - and the experiment the brief implies but never runs: **point four explainers at one prediction and check whether they agree**. They do not. |

## How to run

```bash
pip3 install --break-system-packages shap eli5 lime mlxtend \
    scikit-learn pandas matplotlib scipy nbformat nbconvert
python3 build_activities.py                       # regenerate the .ipynb files
python3 -m nbconvert --execute --inplace --to notebook activity*.ipynb
```

Datasets are fetched from OpenML on first run and cached to `dataset/`. Figures land in `outputs/`.
Seeds are fixed (`SEED = 42`); splits are explicit and stratified.

## How to verify

Every notebook is committed **with its outputs**. Three things are worth checking rather than trusting:

1. **`activity3`, additivity:** `base + sum(shap) == model prediction` is asserted in-cell. That equality is
   the Shapley guarantee - if it fails, the explanation is fiction.
2. **`activity3`, the constant-column guard:** `assert not dead` after encoding. This exists because it
   *actually caught a bug* - `fetch_openml` returns `sex` as **`category`** dtype, which slips past an
   `object`-only `select_dtypes` filter, gets coerced to `NaN`, and becomes a constant column. The model
   silently never saw passenger sex: AUC 0.77 and **SHAP(sex) = 0.0000**. Fixed by testing
   `is_numeric_dtype` instead. Post-fix: AUC **0.892**, `sex` the dominant feature (mean |SHAP| 0.183).
3. **`activity1`, the slice table:** overall accuracy 0.940 hides a recall on "good" wines that runs from
   **0.00** (low-alcohol slice) to **0.82** (high-alcohol slice). One number, four very different models.

## Headline results

- **A1:** RF 0.940 acc / 0.952 AUC vs LogReg 0.892 / 0.872 - the black box wins, and cannot explain itself.
  The two models disagree on **6.8%** of test wines, which no accuracy score would ever tell you.
- **A2:** the rejected applicant's *pertinent negative* - **"had your loan duration been 6 months instead
  of 24, you would have been approved."** That is the only one of the four explanations a human can act on.
- **A3:** `sex` dominates (female **+0.256**, male **-0.140**). But `age` ranks **6th of 7** - the model
  learnt *"women first, money second, children a distant third"*, not the folk story. The leaky `boat`
  column scores **0.995 AUC** and SHAP explains it fluently: a confident, well-rendered, worthless
  explanation. That is Aha's *"a wrong explanation is worse than none"*, demonstrated rather than asserted.
- **A4:** four explainers, one model, one wine - **they contradict each other**, see below.

## A4: the finding worth reading

**Eli5 gives a confident, backwards local explanation, and nothing warns you.**

For a binary classifier, `eli5.explain_prediction` returns the **class-0** decision-path weights and
labels them with whatever class you asked for. `targets=None`, `targets=[0]` and `targets=[1]` all return
**identical weights** - only the printed label changes. Read as *"contribution to P(good)"* (the only way
anyone reads it), **every sign is inverted**:

| | `volatile_acidity` on wine #868 | verdict |
|---|---|---|
| **SHAP** | **-0.074** - pushed away from "good" | ✅ correct |
| **Eli5 (raw)** | **+0.076** - pushed toward "good" | ❌ **backwards** |

Eli5 tells you the wine's **vinegar taint is what made it good**. Verified against the model by
intervention: drop this wine's volatile acidity `0.56 -> 0.20` and P(good) goes **0.040 -> 0.407**. It was
hurting. (Ground truth agrees: 30.5% of wines in the lowest volatile-acidity quartile are good, vs 4.3%
in the highest.)

**The part that should genuinely worry you:** Eli5 (raw) tracks SHAP at **+0.98 Spearman** on ranking - a
number that looks like agreement and would pass any review - while agreeing on **direction for 0% of
features**. Negate it and direction agreement is 100%. *Rank correlation cannot see a sign error.*

LIME fails differently and more quietly: its surrogate predicts **0.335** for a wine the model scores at
**0.040** (~7x off, local R² **0.51**). It never fit the neighbourhood, so its coefficients faithfully
describe **a model that was never deployed** - which is why it ranks `alcohol` 1st where SHAP ranks it
8th of 11. That failure is printed in `.score` and `.local_pred`, and nobody looks.

**The transferable habit:** every wrong claim here was caught the same way - **go back to the model and
intervene**. Change the feature, re-predict, see which way it moves. Three lines, and it is the only
thing in the notebook that cannot lie to you, because it is not an explanation - it is the model.

## Still open

- The discussion-forum posts for each activity.
