# Predicting Telecommunications Customer Churn

*BDA601 Big Data and Analytics - Assessment 2 - Visualisation and Model Development (v3)*

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
| Predictive model building (Spark MLlib) | 20% | Notebook §5 + §5b-§5c (recall + cost operating point) |
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
tree in Apache Spark's MLlib (Apache Spark, 2024). The decision tree was chosen for interpretability:
each split reads as a business rule a retention team can act on, while still capturing non-linear
interactions. I then optimised the model for recall and tuned its operating point to an explicit
business cost (§4.3-§4.4).

## 2. Data preparation and exploratory analysis

Exploratory analysis (notebook §3) produced both statistical summaries (central tendency and
dispersion) and five visual representations - class-balance bar, histograms, box plots, a correlation
heatmap and a pair plot. Three findings shaped the modelling. First, the target is **imbalanced**:
only 26.5% of customers churn, so a model that blindly predicts "no churn" already scores 73.5%
accuracy. Second, **tenure and contract type** separate churners most clearly - churn is concentrated
in the first months of low-tenure, month-to-month customers. Third, `tenure` and `TotalCharges` are
strongly correlated (r = 0.825), a redundancy noted for feature selection. Cleaning addressed one
anomaly: 11 `TotalCharges` values were blank, all for brand-new customers with `tenure = 0`; these
were imputed with the median. `customerID` was dropped, leaving 14 predictors, string-indexed and
assembled into a feature vector for the model.

## 3. Handling missing values

The decision tree identified **`Contract`** as the single most important attribute (importance 0.43,
ahead of `tenure` at 0.18 and `TechSupport` at 0.10). Because this one attribute carries most of the
model's signal, simply deleting rows with a missing contract would discard a large, non-random slice
of customers and bias the sample toward complete records. To test a more realistic scenario I
simulated heavy missingness - randomly removing 30% of `Contract` values - and then **imputed the
mode** ("Month-to-month"), since `Contract` is categorical and the mode is the statistically
defensible single-value replacement. Re-fitting the model on the imputed data left performance
essentially intact: test accuracy moved
from 0.766 to 0.783 and F1 from 0.765 to 0.770. The slight *rise* is itself informative - because the
mode "Month-to-month" coincides with the dominant churn signal, imputation pushed the tree harder
onto that split rather than degrading it. This is partly an artefact of injecting the majority,
high-churn category, and it masks genuine information loss. A real deployment should therefore prefer
a subtler strategy: the decision tree's own handling of gaps, which sends a missing row down every
branch as fractional instances weighted by the training split (Witten et al., 2017), so the
replacement reflects each customer rather than the global mode.

## 4. Interpretation of the churn analysis

### 4.1 Effectiveness

On the held-out test set the baseline tree classified **76.6%** of customers correctly, with F1 0.765
and AUC 0.732 - but against the 73.5% base rate it beats the naive "predict everyone stays" model by
only three percentage points. More importantly for a retention use case, the **churn-class recall is
just 55.3%** - of 376 churners it caught 208 and missed 168. Accuracy is therefore a misleading
headline: with imbalanced classes, a high
accuracy hides poor performance on the minority class the business cares about. Churn-class precision
is 56.4%, so the false positives are retention offers wasted on stayers - a cheaper error than letting
a real churner walk. This baseline is **only partially satisfactory**: missing nearly half of all
churners is too leaky for targeting retention spend, so recall, not accuracy, is what I optimise next.

### 4.2 Who is churning

The feature importances and the tree's top splits agree. The customers most likely to churn are on
**month-to-month contracts** (the root split,
and by far the strongest driver), have **low tenure**, lack **technical support**, and tend to pay by
**electronic check** with **paperless billing**. In short, churn concentrates among newer,
low-commitment customers not locked in by a longer contract or value-added services, while customers
on one- or two-year contracts with longer tenure rarely leave. This suggests where retention effort
pays off: converting month-to-month customers to longer terms and bundling tech support early.

### 4.3 Improving the model - especially recall

Rather than leave these as recommendations, I implemented and measured three standard remedies on the
held-out test set, keeping the interpretable tree as the headline model (Table 1). First, **tuning the
decision threshold** from 0.5 to 0.34 on validation lifted recall from 0.553 to **0.649** at almost no
cost to accuracy - the cheapest win, since it changes only the cut-off. AUC stays 0.732: a threshold
re-balances precision against recall but cannot improve how the model *ranks* customers. Second,
**class weighting** by inverse frequency pushed recall highest, to **0.753**, at a real precision cost
(0.486). Third, a **Random Forest** selected by 3-fold cross-validation lifted AUC to **0.822** - a
genuine gain in ranking quality - reaching recall 0.649 at the best precision-recall balance (F1 0.598)
when tuned to 0.38. Because it ranks churners best, the Random Forest is the model I carry forward to
set an operating point in §4.4.

| Model | Threshold | Accuracy | Precision (churn) | Recall (churn) | F1 (churn) | AUC |
|---|---:|---:|---:|---:|---:|---:|
| Decision tree (baseline) | 0.50 | 0.766 | 0.564 | 0.553 | 0.558 | 0.732 |
| Decision tree (tuned) | 0.34 | 0.756 | 0.536 | **0.649** | 0.587 | 0.732 |
| Weighted tree | 0.50 | 0.721 | 0.486 | **0.753** | 0.591 | 0.743 |
| Random Forest (CV) | 0.50 | 0.788 | 0.635 | 0.487 | 0.551 | **0.822** |
| Random Forest (tuned) | 0.38 | 0.766 | 0.555 | **0.649** | 0.598 | **0.822** |

*Table 1. Recall-focused model comparison on the test set (notebook §5b, `fig09`-`fig10`).*

### 4.4 Choosing the operating point by business cost

Maximising F1 treats a missed churner and a wasted offer as equally costly, but they are not: a false
negative forfeits a customer's future value, while a false positive costs only the incentive, and
acquiring a replacement runs about five times the cost of retention (EMC Education Services, 2015).
Setting `cost(FN) = 5 x cost(FP)` and minimising expected cost on the validation set drives the Random
Forest threshold down to **0.20** (Table 2, `fig11`). Recall then climbs to **0.832** (catching 313 of
376 churners, missing only 63 against the baseline's 168) at a precision of 0.452. Whether that wide
net is worth its 380 false positives is a budget question, not a modelling
one; the framework makes the operating point explicit and defensible rather than leaving it at an
arbitrary 0.5.

| | Predicted stay | Predicted churn |
|---|---:|---:|
| **Actual stay** | 648 (TN) | 380 (FP) |
| **Actual churn** | 63 (FN) | 313 (TP) |

*Table 2. Confusion matrix of the deployed Random Forest at the cost-optimal threshold t = 0.20 (notebook §5c, `fig11`).*

## 5. Conclusion

The Spark MLlib decision tree predicts churn modestly above the base rate and, more valuably, explains
it: short-tenure, month-to-month customers without tech support are the flight risk. Given the class
imbalance, churn recall, not raw accuracy, is the right yardstick. Optimising for it delivered
measurable gains, from threshold tuning (recall 0.649) to class weighting (0.753) to a cross-validated
Random Forest (AUC 0.822). Framing the cut-off as a 5:1 cost of a missed churner versus a wasted offer
then sets a defensible operating point that catches 83% of churners. The tree remains the explanation
a retention team can act on; the cost-tuned Random Forest is the model I would deploy for scoring.

---

# References

Apache Spark. (2024). *MLlib: Classification and regression*. https://spark.apache.org/docs/latest/ml-classification-regression.html

EMC Education Services. (2015). *Data science and big data analytics: Discovering, analyzing, visualizing and presenting data*. John Wiley & Sons.

Kaggle. (2020). *Telco customer churn - IBM sample data sets*. https://www.kaggle.com/blastchar/telco-customer-churn

Marr, B. (2021). *Data strategy: How to profit from a world of big data, analytics and artificial intelligence* (2nd ed.). Kogan Page.

Witten, I. H., Frank, E., Hall, M. A. & Pal, C. J. (2017). *Data mining: Practical machine learning tools and techniques* (4th ed.). Morgan Kaufmann.

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
| Baseline confusion (TN, FP, FN, TP) | 867, 161, 168, 208 |
| Most important attribute | Contract (0.43), tenure (0.18), TechSupport (0.10) |
| Missing-value test (Contract, 30% gone, mode) | acc 0.766 -> 0.783; F1 0.765 -> 0.770 |
| Recall lift - tree @ t=0.34 | recall 0.553 -> **0.649**, acc 0.766 -> 0.756 |
| Recall lift - weighted tree | recall -> **0.753** (precision 0.486) |
| Random Forest (3-fold CV) @ t=0.38 | recall 0.649, precision 0.555, F1 0.598, **AUC 0.822** |
| **Cost operating point (RF, 5:1), t=0.20** | recall **0.832**, precision 0.452; confusion 648, 380, 63, 313 |

## Status & rubric self-check

| Rubric attribute | Weight | Status |
|---|---:|---|
| EDA (stats + visuals) | 15% | ✅ notebook §3 (describe + median/var/range; 5 visual types) |
| Pre-processing & feature selection | 15% | ✅ notebook §4 (impute, redundancy analysis, indexing) |
| Predictive model (Spark MLlib) | 20% | ✅ notebook §5 (tree) + §5b (threshold, class weights, RF + CV) + §5c (cost operating point) |
| Notebook clarity | 10% | ✅ markdown narrative + labelled charts (fig01-fig11) |
| Missing-value strategy | 10% | ✅ report §3 + notebook §6 (most important attr + simulate + impute) |
| Interpretation | 30% | ✅ report §4 (effectiveness, who churns, recall optimisation, cost operating point) |
| Body word count 900-1,100 | - | re-check after final read; no em-dashes |

## Open decisions / next steps before submission

1. Recall optimisation - DONE (threshold, class weights, cross-validated Random Forest).
2. Business-cost operating point - DONE (§4.4 + notebook §5c: 5:1 FN:FP, confusion matrix at t=0.20).
3. Model-based / fractional-instance imputation framing - DONE (§3, Witten §6.1 reference).
4. Export this report to **PDF** and the notebook outputs; zip CSV + .ipynb + PDF for submission.
5. Confirm the word count sits in 900-1,100 after any edits.

## How to reproduce
- Env: `python3.11 -m pip install --break-system-packages "pyspark==3.5.3" "pandas<2.3" seaborn matplotlib pyarrow ipykernel`; kernel `bda-spark` (Python 3.11, Java 8).
- Build: `python3 notebook/build_nb.py`. Execute: `jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=bda-spark notebook/BDA601FariaLuis_Assessment2.ipynb`.
