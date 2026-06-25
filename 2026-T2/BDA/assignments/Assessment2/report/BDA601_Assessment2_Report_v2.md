# Predicting Telecommunications Customer Churn

*BDA601 Big Data and Analytics - Assessment 2 - Visualisation and Model Development (v2)*

| Item | Detail |
|---|---|
| Subject | BDA601 - Big Data and Analytics |
| Assessment | Assessment 2 - Visualisation and Model Development |
| Case | Telco customer churn (IBM sample via Kaggle), modified to 16 attributes |
| Length | 1,000 words (±10%): body prose; tables, figures, references, and appendices excluded |
| Weight | 30% |
| Due | 11.55 pm AEST, Sunday end of Module 8 - 26/07/2026 |
| SLOs assessed | c) clean/manipulate/visualise data · d) design analytical models · e) communicate findings |
| Deliverables | Modified dataset CSV · Jupyter notebook (PySpark MLlib) · this report |

**How this report and the notebook map to the rubric** (the spine I write to, not part of the submission):

| Rubric attribute | Weight | Where |
|---|---:|---|
| Exploratory data analysis | 15% | Notebook §3 (stats + 5 visual types) |
| Data pre-processing & feature selection | 15% | Notebook §4 |
| Predictive model building (Spark MLlib) | 20% | Notebook §5 + §5b (recall optimisation) |
| Clarity & presentation of notebook | 10% | Notebook (narrative + labelled charts) |
| Missing-value handling strategy | 10% | Report §3 |
| Interpretation of data analysis | 30% | Report §4 |

---

# Report

## 1. Problem and approach

Retaining a subscriber is far cheaper than acquiring a new one, so a telco that can predict *who*
will churn can target its retention budget effectively (EMC Education Services, 2015). Working from
the IBM/Kaggle Telco sample (7,043 customers), I removed the five attributes specified in the brief
to obtain a 16-attribute dataset with `Churn` as the target, then built and interpreted a decision
tree in Apache Spark's MLlib (Apache Spark, 2024). The decision tree was chosen because it is
interpretable: each split reads as a plain business rule a retention team can act on, while still
capturing non-linear interactions between contract, tenure and service attributes. I then optimised
the model for recall, the metric that matters most for retention (§4.3).

## 2. Data preparation and exploratory analysis

Exploratory analysis (notebook §3) produced both statistical summaries (central tendency and
dispersion) and five visual representations - class-balance bar, histograms, box plots, a correlation
heatmap and a pair plot. Three findings shaped the modelling. First, the target is **imbalanced**:
only 26.5% of customers churn, so a model that blindly predicts "no churn" already scores 73.5%
accuracy. Second, **tenure and contract type** separate churners most clearly - churn is concentrated
in the first months of low-tenure, month-to-month customers. Third, `tenure` and `TotalCharges` are
strongly correlated (r = 0.825), a redundancy noted for feature selection. Cleaning addressed one
anomaly: 11 `TotalCharges` values were blank, all for brand-new customers with `tenure = 0`; these
were imputed with the median. The `customerID` identifier was dropped, leaving 14 predictors that
were string-indexed, marked as categorical, and assembled into a feature vector for the model.

## 3. Handling missing values

The decision tree identified **`Contract`** as the single most important attribute (importance 0.43,
ahead of `tenure` at 0.18 and `TechSupport` at 0.10). Because this one attribute carries most of the
model's signal, simply deleting rows with a missing contract would discard a large, non-random slice
of customers and bias the sample toward complete records. To test a more realistic scenario I
simulated heavy missingness - randomly removing 30% of `Contract` values - and then **imputed the
mode** ("Month-to-month"), since `Contract` is categorical and the mode is the statistically
defensible single-value replacement (the median plays the same role for numeric attributes).
Re-fitting the model on the imputed data left performance essentially intact: test accuracy moved
from 0.766 to 0.783 and F1 from 0.765 to 0.770. The slight *rise* is itself informative - because the
mode "Month-to-month" coincides with the dominant churn signal, imputation pushed the tree harder
onto that split rather than degrading it. This is partly an artefact of injecting the majority,
high-churn category, and it masks genuine information loss; a real deployment should therefore prefer
a model-based imputer (predicting the missing attribute from the others) so the replacement reflects
each customer rather than the global mode.

## 4. Interpretation of the churn analysis

### 4.1 Effectiveness

On the held-out test set the baseline tree classified **76.6%** of customers correctly, with F1 0.765
and AUC 0.732 - but against the 73.5% base rate it beats the naive "predict everyone stays" model by
only three percentage points. More importantly for a retention use case, the **churn-class recall is
just 55.3%** - of 376 actual churners the model caught 208 and missed 168 (the false negatives in the
confusion matrix). Accuracy is therefore a misleading headline: with imbalanced classes, a high
accuracy hides poor performance on the minority class the business cares about. Churn-class precision
is 56.4%, so just over half of the flagged customers would genuinely have left; the 161 false
positives are retention offers wasted on stayers - a cheaper error than letting a real churner walk.
This baseline is **only partially satisfactory** - interpretable and above the base rate, but missing
nearly half of all churners is too leaky for targeting retention spend, so recall (not accuracy) is
the metric I optimise in Section 4.3.

### 4.2 Who is churning

The model paints a consistent picture, corroborated by both the feature importances and the tree's
top splits. The customers most likely to churn are on **month-to-month contracts** (the root split,
and by far the strongest driver), have **low tenure**, lack **technical support**, and tend to pay by
**electronic check** with **paperless billing**. In short, churn concentrates among newer,
low-commitment customers who have not been locked in by a longer contract or value-added services.
Customers on one- or two-year contracts with longer tenure rarely leave. This directly suggests where
retention effort pays off: converting month-to-month customers to longer terms and bundling tech
support early in the lifecycle.

### 4.3 Improving the model - especially recall

Rather than leave these as recommendations, I implemented and measured three standard remedies on the
held-out test set, keeping the interpretable tree as the headline model (Table 1).

| Model | Threshold | Accuracy | Precision (churn) | Recall (churn) | F1 (churn) | AUC |
|---|---:|---:|---:|---:|---:|---:|
| Decision tree (baseline) | 0.50 | 0.766 | 0.564 | 0.553 | 0.558 | 0.732 |
| Decision tree (tuned) | 0.34 | 0.756 | 0.536 | **0.649** | 0.587 | 0.732 |
| Weighted tree | 0.50 | 0.721 | 0.486 | **0.753** | 0.591 | 0.743 |
| Random Forest (CV) | 0.50 | 0.788 | 0.635 | 0.487 | 0.551 | **0.822** |
| Random Forest (tuned) | 0.38 | 0.766 | 0.555 | **0.649** | 0.598 | **0.822** |

*Table 1. Recall-focused model comparison on the test set (notebook §5b, `fig09`-`fig10`).*

First, **tuning the decision threshold** from 0.5 to 0.34 (chosen on validation to maximise churn-class
F1) lifted recall from 0.553 to **0.649** at almost no cost to accuracy (0.766 to 0.756) - the cheapest
win, since it changes only the cut-off, not the model. The AUC is unchanged at 0.732, the key lesson: a
threshold re-balances precision against recall but does not improve how the model *ranks* customers.
Second, **class weighting** (weighting churn rows by inverse frequency) pushed recall highest, to
**0.753**, but at a real precision cost (0.486) - the option to pick only if the retention team would
rather over-contact than miss churners. Third, a **Random Forest selected by 3-fold cross-validation**
lifted AUC sharply from 0.732 to **0.822**, a genuine gain in ranking quality; with its threshold tuned
to 0.38 it reaches recall 0.649 at the best precision-recall balance of all options (F1 0.598). I would
therefore score customers with the Random Forest at that operating point while retaining the single
tree for explanation. Two further levers remain: re-introducing the strong predictors the brief
required me to drop, and the model-based imputation noted in §3. Together these turn a leaky baseline
into a model that catches roughly two-thirds of churners and confirm that accuracy was never the right
target - recall and AUC are.

## 5. Conclusion

The Spark MLlib decision tree predicts churn modestly above the base rate and, more valuably, explains
it: short-tenure, month-to-month customers without tech support are the flight risk. Given the class
imbalance, churn recall and F1 - not raw accuracy - are the right yardsticks. Optimising for recall
delivered measurable gains: threshold tuning alone raises the interpretable tree's recall from 0.553 to
0.649, class weighting reaches 0.753, and a cross-validated Random Forest lifts AUC from 0.732 to 0.822.
The tree remains the explanation a retention team can act on; the Random Forest at a 0.38 threshold is
the model I would deploy for scoring.

---

# References

Apache Spark. (2024). *MLlib: Classification and regression*. https://spark.apache.org/docs/latest/ml-classification-regression.html

EMC Education Services. (2015). *Data science and big data analytics: Discovering, analyzing, visualizing and presenting data*. John Wiley & Sons.

Kaggle. (2020). *Telco customer churn - IBM sample data sets*. https://www.kaggle.com/blastchar/telco-customer-churn

Marr, B. (2021). *Data strategy: How to profit from a world of big data, analytics and artificial intelligence* (2nd ed.). Kogan Page.

---

# Statement of Acknowledgement

I acknowledge that I have used the following AI tool(s) in the creation of this report:
- Anthropic Claude Opus 4.8

This tool was used to assist with structuring the analysis pipeline, debugging the PySpark
configuration, improving the clarity of academic language, and framing the churn interpretation. I
confirm that the use of these tools has been in accordance with the Torrens University Australia
Academic Integrity Policy and the TUA, Think and MDS Position Paper on the Use of AI. I confirm that
the final output is authored by me and represents my own critical thinking, analysis, and synthesis
of sources. I take full responsibility for the final content of this report.

---

# Planning companion (not part of submission)

## Real numbers (from `outputs/metrics.json`, notebook executed end to end)

| Metric | Value |
|---|---|
| Rows / predictors | 7,043 / 14 |
| Base rate (churn / stay) | 26.5% / 73.5% |
| Tuned tree depth | 8 (selected on validation) |
| Baseline test accuracy / F1 / AUC | 0.766 / 0.765 / 0.732 |
| Baseline churn recall / precision | 0.553 / 0.564 |
| Confusion (TN, FP, FN, TP) | 867, 161, 168, 208 |
| Most important attribute | Contract (0.43), tenure (0.18), TechSupport (0.10) |
| Missing-value test (Contract, 30% gone, mode) | acc 0.766 -> 0.783; F1 0.765 -> 0.770 |
| **Recall lift - tree @ t=0.34** | recall 0.553 -> **0.649**, acc 0.766 -> 0.756 |
| **Recall lift - weighted tree** | recall -> **0.753** (precision 0.486) |
| **Random Forest (3-fold CV) @ t=0.38** | recall 0.649, precision 0.555, F1 0.598, **AUC 0.822** |

## Status & rubric self-check

| Rubric attribute | Weight | Status |
|---|---:|---|
| EDA (stats + visuals) | 15% | ✅ notebook §3 (describe + median/var/range; 5 visual types) |
| Pre-processing & feature selection | 15% | ✅ notebook §4 (impute, redundancy analysis, indexing) |
| Predictive model (Spark MLlib) | 20% | ✅ notebook §5 (tree) + §5b (threshold, class weights, RF + CrossValidator) |
| Notebook clarity | 10% | ✅ markdown narrative + labelled charts (fig01-fig10) |
| Missing-value strategy | 10% | ✅ report §3 + notebook §6 (most important attr + simulate + impute) |
| Interpretation | 30% | ✅ report §4 (effectiveness, who churns, measured recall optimisation) |
| Body word count 900-1,100 | - | re-check after final read; no em-dashes |

## Open decisions / next steps before submission

1. Recall optimisation - DONE (threshold, class weights, cross-validated Random Forest); narrative now
   reports measured lift rather than promises.
2. Export this report to **PDF** and the notebook outputs; zip CSV + .ipynb + PDF for submission.
3. Optional: tune the operating threshold to an explicit business cost ratio (cost of a missed churner
   vs a wasted offer) instead of maximising F1.
4. Confirm the word count sits in 900-1,100 after any edits.

## How to reproduce
- Env: `python3.11 -m pip install --break-system-packages "pyspark==3.5.3" "pandas<2.3" seaborn matplotlib pyarrow ipykernel`; kernel `bda-spark` (Python 3.11, Java 8).
- Build: `python3 notebook/build_nb.py`. Execute: `jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=bda-spark notebook/BDA601FariaLuis_Assessment2.ipynb`.
