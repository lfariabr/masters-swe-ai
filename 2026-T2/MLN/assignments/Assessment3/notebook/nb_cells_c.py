"""v3 cells, part C: Deployment and lessons, appendices, integrity, references."""

from nb_cells_a import md, co

EVAL_READ = md("""
### 5.3 What the evaluation establishes

Protocol A cleared its declared bar comfortably. Gradient Boosting explains daily demand across
2011 and 2012 to within about 384 rentals on the configuration the ablation selected, roughly
8% of mean daily demand, a 74% improvement on the mean baseline. As a benchmark answer to "which
model performs best on this dataset", that is the answer, and Table 5.7 records it as exactly
that and nothing more.

Protocol B failed both of its gates, and the decision rule that fired is the third row of the
table declared in Section 1.5: **the naive baseline wins and machine learning is rejected for
day-ahead forecasting.** The wording matters. This is not "the improvement was not material".
The best model was 23.5% worse than a trailing seven-day average, and the paired test over 366
days puts the probability of that gap arising from sampling noise at effectively nil, with the
caveat that autocorrelated daily errors make the p-value indicative rather than exact.

Three things make this a finding rather than a failure.

First, it is **mechanistic, not mysterious**. Table 5.3 shows the ensembles cannot produce a
number above their training ceiling while half of 2012 sits above it, so their failure was
determined before any hyperparameter was chosen.

Second, it is **specific about what would change the answer**. The ablation shows the
forecasting signal these models can use comes almost entirely from recent demand, and the naive
rule already uses recent demand directly and without error. A model earns its place here only
by adding something the rolling mean lacks, and one year of history does not supply it.

Third, it **survived a fair fight**. The models were given autoregressive features, cyclical
encoding, tuning inside the training year, and the same dates as the baseline. The naive rule
won anyway.
""")

DEPLOY = md("""
## 6. Deployment and Lessons Learned

### 6.1 What I would actually put into production

The honest recommendation from this study is a two-part system, and only one part is a model.

**For day-ahead demand planning, deploy the trailing seven-day mean.** It produced the lowest
error of anything tested, it is essentially unbiased across a year of 64% growth, it needs no
training, no retraining and no feature pipeline, and any operator can reproduce it from a
dashboard. Recommending a model I have just measured to be 23.5% worse would be recommending
the more impressive-sounding option rather than the better one.

**For demand explanation and scenario analysis, use the Protocol A Gradient Boosting model.**
It answers a different and genuinely useful question: how much of the variation in daily demand
is attributable to temperature, season, day type and elapsed time. That supports capacity
planning conversations and marketing analysis. It does not support a claim about tomorrow, and
Table 5.7 says so on its face.

### 6.2 Deployment requirements, regardless of which component is running

- **Out-of-domain weather detection.** `weathersit` category 4 never appears in the training
  data. With `handle_unknown="ignore"` an unseen category encodes identically to the reference
  category, so a severe-weather day would be silently scored as if it were clear. The supported
  domain must be recorded alongside the model and validated at the input boundary, with
  out-of-domain days escalated to human review rather than predicted.
- **Error monitoring against the naive rule.** Whatever runs in production should be scored
  daily against the rolling seven-day mean. The day the model stops beating it is the day it
  should be retired, and this study shows that day can be the first one.
- **Multi-year history before any trend claim.** Two years is one repetition. The trend feature
  that helped under Protocol A and hurt under Protocol B is the concrete demonstration: with a
  single growth curve there is no way to tell a durable trend from a one-off level shift.
- **The forecast-versus-observed weather gap.** This dataset contains observed weather. A
  production system would receive forecast weather, which carries its own error that this study
  cannot measure and that would make every Protocol B number reported here optimistic.

### 6.3 Lessons learned

**The split defines the claim.** The same data, the same five models and the same metric
produce MAE 384 under one split and 1,628 under another. Neither number is wrong; they answer
different questions. The mistake would have been to report the flattering one and describe it
in forecasting language, which is what a random split over a time series quietly invites.

**A feature is not good or bad on its own.** Elapsed time gave the best result in this notebook
and one of the worst, from the same column, decided entirely by whether the model was asked to
interpolate or to extrapolate. Feature selection without a protocol attached is not a
meaningful activity.

**Model class beats tuning when the class is wrong.** Linear Regression outperformed two tuned
ensembles under Protocol B, not by being more accurate but by being able to extrapolate at all.
No grid search over trees could have closed that gap.

**Baselines have to be strong enough to lose to.** Had I benchmarked against the constant mean,
as the first version of this project did, every model would have looked like a success. The
naive rules cost almost nothing to compute and they changed the entire conclusion.

**Declaring criteria in advance is what makes a negative result reportable.** The gates in
Section 1 were fixed before any v3 model ran, so this report can state a rejection plainly
instead of retrofitting a threshold the winner happens to clear. That said, the criteria were
set after the earlier version had already surfaced the naive baselines, which is weaker than a
blind pre-registration, and Section 1.6 says so rather than claiming more independence than the
process had.

### 6.4 Future work

Aggregating the hourly file to build intra-day features, adding public-holiday and event
calendars, testing models built for extrapolation such as gradient boosting on differenced
targets or an explicit trend-plus-seasonality decomposition, and above all obtaining more than
two years of history so that a seasonal pattern can be separated from a growth curve.
""")

APPENDIX_A = md("""
---

## Appendix A - Glossary

| Term | Meaning in this report |
|---|---|
| **MAE** | Mean absolute error, average size of the miss in rentals per day. The brief's primary metric and the one used for every gate. |
| **MSE / RMSE** | Mean squared error and its root. Squaring punishes large misses, so RMSE rises above MAE when errors are uneven. |
| **R-squared** | Share of variance explained. Negative means the model predicts worse than the mean of the evaluated period. |
| **Interpolation** | Predicting inside the range and period the model was trained on. |
| **Extrapolation** | Predicting outside it, which tree ensembles structurally cannot do. |
| **Day-ahead horizon** | Running the model at the close of day D to predict day D+1, with all counts up to D known. |
| **Autoregressive feature** | An input built from the target's own past, such as yesterday's count. |
| **Causal construction** | Building such a feature so its window ends strictly before the target day. |
| **Naive baseline** | A rule needing no model: yesterday's count, last week's count, or a trailing mean. |
| **TimeSeriesSplit** | Cross-validation with expanding windows that never lets a fold train on data later than it validates. |
| **Cyclical encoding** | Mapping a calendar value to a sine and cosine pair, defined for values never seen in training. |
| **SHAP** | Additive attribution of a prediction to its features, preferred here to impurity importance, which is biased towards continuous variables. |
| **Wilcoxon signed-rank** | Non-parametric paired test used here on daily absolute errors. |

## Appendix B - Proposed operational deployment

```mermaid
flowchart LR
    A["Nightly job, 22:00<br/>day D closes"] --> B["Read demand history<br/>through day D"]
    B --> C["Rolling 7-day mean<br/>= day D+1 forecast"]
    B --> D["Protocol A model<br/>explanation and scenarios"]
    C --> E{"weathersit forecast<br/>in supported domain?"}
    E -->|"1, 2 or 3"| F["Publish forecast<br/>to staffing and fleet"]
    E -->|"4 or unknown"| G["Escalate to<br/>human review"]
    F --> H["Next morning:<br/>score yesterday's forecast"]
    H --> I{"Still beating<br/>the naive rule?"}
    I -->|no| J["Retire the component"]
```

The forecasting path deliberately contains no learned model. The learned model sits on the
explanation branch, where a random split can support its claims.
""")

REPRO = co('''
# Reproducibility - the exact environment these numbers came from
import sys, sklearn, scipy, matplotlib
print("Python      :", sys.version.split()[0])
for mod in (np, pd, sklearn, scipy, matplotlib, sns, shap):
    print(f"{mod.__name__:12s}:", mod.__version__)
print("RANDOM_STATE:", RANDOM_STATE)
print("Rows modelled:", len(model_df), "| Protocol A test:", len(Xa_te),
      "| Protocol B confirmation:", len(test_2012))
''')

CLOSING = md("""
---

## Academic Integrity Declaration

I declare that this submission is my own work. All sources of information, ideas and code have
been acknowledged. The dataset is publicly available from the UCI Machine Learning Repository.
The analysis, modelling decisions, interpretation and written commentary are my own.

## Statement of Acknowledgement

Analysis was performed in Python with pandas, NumPy, scikit-learn, SciPy, SHAP, Matplotlib and
Seaborn. I used an AI assistant (Anthropic Claude) as a study and review aid: to challenge my
experimental design, to check that my measured claims matched my output tables, and to review
drafting for clarity. All modelling decisions, the two-protocol design, the declared gates and
decision rules, the interpretation of every result and the final recommendation are my own, and
every number reported here is produced by the code in this notebook.

## References

Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5-32.
https://doi.org/10.1023/A:1010933404324

Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R.
(2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS Inc.

Fanaee-T, H., & Gama, J. (2014). Event labeling combining ensemble detectors and background
knowledge. *Progress in Artificial Intelligence, 2*, 113-127.
https://doi.org/10.1007/s13748-013-0040-3

Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *Annals of
Statistics, 29*(5), 1189-1232. https://doi.org/10.1214/aos/1013203451

Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.).
OTexts. https://otexts.com/fpp3/

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions.
*Advances in Neural Information Processing Systems, 30*, 4765-4774.

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... &
Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning
Research, 12*, 2825-2830.

Shaukat, K., Luo, S., & Varadharajan, V. (2024). A novel machine learning approach for
detecting first-time-appeared malware. *Engineering Applications of Artificial Intelligence,
131*, 107801. https://doi.org/10.1016/j.engappai.2023.107801

Strobl, C., Boulesteix, A.-L., Zeileis, A., & Augustin, T. (2007). Bias in random forest
variable importance measures. *BMC Bioinformatics, 8*, 25.
https://doi.org/10.1186/1471-2105-8-25

University of California, Irvine. (n.d.). *Bike Sharing Dataset* [Data set]. UCI Machine
Learning Repository. https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset

Wilcoxon, F. (1945). Individual comparisons by ranking methods. *Biometrics Bulletin, 1*(6),
80-83. https://doi.org/10.2307/3001968
""")

CELLS_C = [EVAL_READ, DEPLOY, APPENDIX_A, REPRO, CLOSING]
