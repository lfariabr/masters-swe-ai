# Exploring the Relationship between Net Promoter Score and Revenue Growth in Healthcare Clinics

Tags: #research, #machinelearning, #healthcare, #nps, #dataanalytics, #python

## A Master's Research Journey: Validating Healthcare's Most Popular Metric

*From Critical Literature Review to Full Research Proposal — A trimester-long investigation into whether Net Promoter Score actually predicts revenue in healthcare clinics.*

---

## The Question That Started It All

During my 6+ years working for aesthetic healthcare clinics across Brazil, I witnessed firsthand how **Net Promoter Score (NPS)** became the golden metric. Every meeting, every dashboard, every strategic decision seemed to revolve around those magic numbers: *Promoters (9-10), Passives (7-8), Detractors (0-6)*.

But here's the uncomfortable truth I kept noticing:

> **No one had ever proven that NPS actually correlates with revenue growth in healthcare.**

Sure, we *assumed* higher NPS meant more revenue. We *believed* patient satisfaction drove financial performance. But where was the empirical evidence?

That question became the foundation of my Master's research at **Torrens University Australia**, under the expert guidance of **Prof. Dr. Bushra Naeem**, a distinguished researcher in digital transformation and ICT methodologies.

---

## Assessment 1: Critical Literature Review 
> Finding the Gap

### What We Discovered

I conducted a systematic literature review analyzing 12+ peer-reviewed studies across six key themes:

1. **Patient Experience Frameworks** (Godovykh & Pizam, 2023)
2. **NPS Evolution and Critique** (Reichheld, 2003; Dawes, 2024)
3. **Loyalty Programs & Information Systems** (Cahya et al., 2025)
4. **AI-Enabled Sentiment Analysis** (Alkhnbashi et al., 2024; Xiao et al., 2022)
5. **Emotional Engagement** (Angelis et al., 2024)
6. **Healthcare-Specific Feedback Analytics** (Shankar & Yip, 2024)

### The Knowledge Gap

Three converging gaps emerged:

**1. Metric Validation Gap**  
NPS guides resource allocation in healthcare despite never being empirically tested as a predictor of clinic-level financial performance.

**2. Business Intelligence Gap**  
Patient feedback analytics inform operational improvements and AI sentiment analysis proves technically feasible, yet neither connects to measurable financial outcomes.

**3. ICT Foundation Gap**  
AI sentiment systems presume sentiment-to-performance correlations that remain statistically unverified, risking investment in systems optimizing wrong outcomes.

### Key Finding

**Zero studies** have quantitatively validated the NPS-revenue relationship in healthcare contexts. This isn't just an academic curiosity — it's a $50,000+ annual investment decision for clinics adopting expensive feedback systems like Medallia or Qualtrics.

---

## Assessment 2: Research Tools and Methodologies
> Designing the Study

### Research Questions

Based on the identified gap, I formulated two precise research questions:

- **RQ1:** To what extent is Net Promoter Score correlated with monthly revenue growth in healthcare clinics?  
- **RQ2:** Can NPS trends predict short-term revenue fluctuations?

### Hypotheses

- **H0:** No significant correlation exists between NPS and revenue (r < 0.3 or p > 0.05)
- **H1:** NPS is positively correlated with revenue growth (r > 0.3, p < 0.05)

### Methodology: Quantitative Correlational Design

- **Philosophical Orientation:** Pragmatic-Positivist paradigm (Morgan, 2014)

**Why Quantitative?** R: The research questions are relational, not exploratory. We need statistical evidence, not narrative insights.

### The Dataset

- **Source:** Pro-Corpo Estética (Brazilian healthcare group)  
- **Size:** ~27,000 aggregated NPS survey responses  
- **Timeline:** 36 months (2022-2025)  
- **Scope:** Multiple clinic branches across Brazil

**Data Structure:**
- Clinic ID / Store name
- Month & Year
- Average NPS score (0-10 scale)
- Monthly revenue (BRL)
- Number of responses per month

### Analytical Pipeline

```python
# 1. Data Cleaning & Preparation
- Remove duplicates
- Handle missing values (interpolation for isolated gaps)
- Outlier detection (>3 SD flagged for validation)
- Create derived variables: Revenue Growth %, Lagged NPS (t-1, t-2)

# 2. Statistical Analysis
- Descriptive Statistics (mean, SD, distribution)
- Pearson + Spearman Correlation (strength & direction)
- Linear Regression (predictive capacity with temporal lags)
- K-means Clustering (clinic behavioral segmentation)

# 3. Validation
- Cross-validation by clinic and year
- Temporal, spatial, and methodological triangulation
```

### Tools & Technologies

| Component | Technology |
|-----------|------------|
| Data Processing | Python (Pandas, NumPy) |
| Statistical Analysis | SciPy, Statsmodels, Scikit-learn |
| Visualization | Matplotlib, Seaborn, Streamlit |
| Documentation | Jupyter Notebooks |
| Version Control | Git/GitHub |

### Ethics & Governance

- ✓ **Anonymized Data:** Aggregated at clinic-month level  
- ✓ **Institutional Consent:** Signed approval from Pro-Corpo  
- ✓ **Legal Compliance:** LGPD (Brazil) + GDPR + Australian Privacy Act (1988)  
- ✓ **Researcher Reflexivity:** Documented as former collaborator

---

## Assessment 3: Research Proposal
> The Full Picture

### Conceptual Framework

**Assumed Pathway (Never Validated):**

```
Patient       NPS         Loyalty        Revenue
Experience  → Score   →  Intent    →?→  Growth
   ✓            ✓          ✓        ?
                                    ↑
                                BROKEN LINK
```

This study tests whether the "?" is actually a validated connection.

### Expected Contributions & Decision Framework

Regardless of statistical outcome, this research provides actionable intelligence:

**Scenario 1: Strong Correlation ✅ (r > 0.7, p < 0.05)**  
- **Validate NPS** as strategic KPI  
- Simple tracking systems sufficient  
- Cost-effective patient monitoring justified

**Scenario 2: Moderate Correlation ⚠️ (0.3 < r < 0.7, p < 0.05)**  
- **Partial validation** — NPS provides some signal  
- Justify investment in AI sentiment enhancement  
- Richer feedback dimensions needed

**Scenario 3: Weak/No Correlation ❌ (r < 0.3 or p > 0.05)**  
- **Challenge NPS validity** in healthcare  
- Redirect to NLP-based alternatives  
- Capture nuanced emotional/experiential data

### Software Design Flow (ICT R&D Framework)

The research follows evidence-based system design principles (Wohlin & Runeson, 2021):

1. **Data Import Layer:** CSV ingestion with validation
2. **Cleaning Pipeline:** Pandas-based transformation with logging
3. **Aggregation Engine:** Clinic-month grouping with temporal features
4. **Statistical Module:** Correlation + Regression + Clustering
5. **Visualization Layer:** Interactive Streamlit dashboard
6. **Export Module:** Results, visualizations, reports

---

## Timeline: From Proposal to Publication

**Phase 1: Assessment 3 Execution (12 Weeks)**

- **Weeks 1-2:** Literature refinement & problem definition  
- **Weeks 3-4:** Ethics clearance & data acquisition  
- **Weeks 5-6:** Data cleaning & preparation  
- **Weeks 7-8:** Descriptive & correlation analysis  
- **Weeks 9-10:** Regression modeling & validation  
- **Week 11:** Results interpretation & draft writing  
- **Week 12:** Final report + presentation (Due: Dec 3, 2025)

**Phase 2: Analysis Deepening (8 Weeks)**

- Extended statistical analysis (sensitivity, time-series)
- Qualitative validation (500 text comments from NPS surveys)
- Streamlit dashboard prototype development
- Industry benchmarking (healthcare vs. retail)

**Phase 3: Publication Pathway (20 Weeks)**

**Target Journals:**
- *International Journal of Market Research*
- *Journal of Healthcare Management*

**Target Conferences:**
- Australian Conference on Information Systems (ACIS)
- Healthcare Management Conference

**Milestones:**
- Journal draft preparation (3000-4000 words)
- Peer review cycle (2 rounds expected)
- Conference presentation (15-min talk + poster)
- Final publication & knowledge dissemination

---

## Technical Implementation

### Code Architecture

```python
# Project Structure
research_proposal/
├── data/
│   ├── raw/                    # Original Pro-Corpo dataset
│   ├── processed/              # Cleaned & aggregated data
│   └── results/                # Statistical outputs
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_correlation.ipynb
│   ├── 04_regression.ipynb
│   └── 05_clustering.ipynb
├── src/
│   ├── preprocessing.py        # Data cleaning functions
│   ├── statistical_analysis.py # Correlation & regression
│   ├── clustering.py           # K-means implementation
│   └── visualization.py        # Plotting functions
├── streamlit_app/
│   └── dashboard.py            # Interactive dashboard
├── tests/
│   └── test_preprocessing.py   # Unit tests
└── docs/
    ├── Assessment1_Lit_Review.md
    ├── Assessment2_Methodology.md
    └── Assessment3_Full_Proposal.md
```

### Sample Code: Correlation Analysis

```python
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv('data/processed/clinic_nps_revenue.csv')

# Aggregate by clinic-month
df_agg = df.groupby(['clinic_id', 'year_month']).agg({
    'nps_score': 'mean',
    'revenue_brl': 'sum',
    'response_count': 'sum'
}).reset_index()

# Calculate revenue growth percentage
df_agg['revenue_growth'] = df_agg.groupby('clinic_id')['revenue_brl'].pct_change() * 100

# Create lagged variables for temporal analysis
df_agg['nps_lag1'] = df_agg.groupby('clinic_id')['nps_score'].shift(1)
df_agg['nps_lag2'] = df_agg.groupby('clinic_id')['nps_score'].shift(2)

# Pearson Correlation (assumes linear relationship)
r_pearson, p_pearson = pearsonr(
    df_agg['nps_score'].dropna(), 
    df_agg['revenue_growth'].dropna()
)

# Spearman Correlation (non-parametric, handles outliers)
r_spearman, p_spearman = spearmanr(
    df_agg['nps_score'].dropna(), 
    df_agg['revenue_growth'].dropna()
)

print(f"Pearson r: {r_pearson:.3f}, p-value: {p_pearson:.4f}")
print(f"Spearman ρ: {r_spearman:.3f}, p-value: {p_spearman:.4f}")

# Visualization: Scatterplot with regression line
plt.figure(figsize=(10, 6))
sns.regplot(x='nps_score', y='revenue_growth', data=df_agg, 
            scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('NPS Score vs. Revenue Growth (%)')
plt.xlabel('Average NPS Score (0-10)')
plt.ylabel('Monthly Revenue Growth (%)')
plt.tight_layout()
plt.savefig('results/nps_revenue_correlation.png', dpi=300)
plt.show()
```

### Sample Code: Regression Model

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_squared_error

# Prepare features (lagged NPS) and target (revenue growth)
X = df_agg[['nps_score', 'nps_lag1', 'nps_lag2']].dropna()
y = df_agg.loc[X.index, 'revenue_growth']

# Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Build linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation metrics
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"R² Score: {r2:.3f}")
print(f"RMSE: {rmse:.2f}%")
print(f"\nModel Coefficients:")
for feature, coef in zip(['NPS (t)', 'NPS (t-1)', 'NPS (t-2)'], model.coef_):
    print(f"  {feature}: {coef:.4f}")

# Cross-validation (5-fold)
cv_scores = cross_val_score(model, X, y, cv=5, 
                            scoring='r2')
print(f"\nCross-Validation R² (mean): {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
```

---

## Academic Rigor & Quality Assurance

### Literature Foundation

- ✓ **12+ peer-reviewed sources** (2022-2025)  
- ✓ **APA 7th referencing** throughout  
- ✓ **Critical synthesis** via literature comparison table  
- ✓ **Gap identification** grounded in systematic review

### Methodological Transparency

- ✓ **Philosophical paradigm** explicitly stated  
- ✓ **Rationale** for quantitative over qualitative approach  
- ✓ **Limitations** acknowledged (single organization, omitted variables)  
- ✓ **Triangulation** across temporal, spatial, methodological dimensions

### Reproducibility

- ✓ **Full dataset documentation** (Appendix A)  
- ✓ **Code excerpts** with transparent preprocessing steps  
- ✓ **Version control** for all analysis scripts  
- ✓ **Open science principles** (results will be shared post-publication)

---

## Explore the Research

**Academic Submissions:**
- [Assessment 1: Critical Literature Review](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-REM/assignments/Assessment1/REM502_Faria_L_Assessment_1_Critical-Literature-Review.pdf)
- [Assessment 2: Research Tools and Methodologies](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-REM/assignments/Assessment2/REM502_Faria_L_Assessment_2_Research-Tools-and-Methodologies.pdf)
- [Assessment 3: Full Research Proposal](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-REM/assignments/Assessment3/REM502_Faria_L_Assessment_3_Research-Proposal.pdf)
- [Presentation Slides](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-REM/assignments/Assessment3/REM502_Faria_L_Assessment_3.pdf)

**Related Projects:**
- [ClinicTrends AI – Sentiment Analysis Platform](https://dev.to/lfariaus/clinictrends-ai-transforming-customer-feedback-into-intelligent-insights-47en)
- [Portfolio: All Master's Projects](https://github.com/lfariabr/masters-swe-ai)

---

## Next Steps & Future Research

#### Immediate (Assessment 3 Submission)

- [X] Finalize statistical analysis (Week 9-10)
- [X] Complete written report (2,500 words)
- [X] Design presentation slides (5-7 minutes)
- [X] Submit by Dec 3, 2025

#### Short-Term (Phase 2)

- [ ] Build interactive Streamlit dashboard
- [ ] Conduct qualitative validation on text comments
- [ ] Publish findings on personal blog/LinkedIn
- [ ] Present at Torrens University research showcase

#### Long-Term (Phase 3)

- [ ] Submit journal article to *International Journal of Market Research*
- [ ] Present at ACIS Conference (2026)
- [ ] Extend research to Phase 2: AI sentiment analysis
- [ ] Develop predictive model for revenue forecasting
- [ ] Integrate findings into ClinicTrends AI v3.0

---

## Key Takeaways

**For Researchers:**  
This study demonstrates how ICT R&D methodologies bridge academic rigor with real-world business problems. Quantitative validation is about proving correlations and building evidence-based foundations for future AI systems.

**For Healthcare Professionals:**  
Before investing $50K+ annually in patient feedback systems, ask one question: *"Has anyone proven this metric predicts what I care about?"* This research provides that validation framework.

**For Software Engineers:**  
Data science is about asking the right questions first. This research journey shows how critical literature review, methodological rigor, and statistical validation create the foundation for truly intelligent systems.

---

## Supervisor & Acknowledgments

**Research Supervisor:**  
- **Prof. Dr. Bushra Naeem**  
- *Senior Lecturer, Research Methodologies*  
- Torrens University Australia

**Industry Partner:**  
- **Pro-Corpo Estética**  
- *Healthcare Group, Brazil*  
- For providing anonymized dataset and institutional consent

**Academic Context:**  
- REM502 – Research Methodologies  
- Trimester 2, 2025  
- Master of Software Engineering (Artificial Intelligence)

---

## Let's Connect

If you're working on similar research, interested in healthcare analytics, or passionate about evidence-based AI systems, I'd love to connect:

- **LinkedIn:** [linkedin.com/in/lfariabr](https://www.linkedin.com/in/lfariabr/)  
- **GitHub:** [github.com/lfariabr](https://github.com/lfariabr)  
- **Portfolio:** [luisfaria.dev](https://luisfaria.dev)