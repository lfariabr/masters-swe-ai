# **Does NPS Really Predict Revenue in Healthcare Clinics? I Spent 12 Weeks Finding Out.**

**Tags:** #dataanalytics #python #healthcare #machinelearning #research

---

## **1. Why I Questioned NPS in Healthcare (The Origin Story)**

For 6+ years grinding in Brazilian aesthetic healthcare clinics, I saw NPS treated like gospel:

> **Everyone worshipped NPS.
> But no one could prove it actually linked to revenue.**

Every month:
Dashboards. Meetings. Bonuses. Marketing decisions.
All based on one metric: the **Net Promoter Score**.

No clinician, manager, or exec could point to data linking patient "loyalty" to the bottom line. That gap haunted me – and sparked my Master's deep dive at Torrens University Australia, under **Prof. Dr. Bushra Naeem** (ICT R&D expert in digital transformation).
Research Methodologies (*REM502*)'s structure turned this frustration into rigorous research:

- **Assessment 1 (Critical Literature Review)**: We had to dissect 12+ studies and pinpoint gaps. I zeroed in on NPS's unproven link to financials – literature screamed "patient experience matters" (e.g., Godovykh & Pizam, 2023), but nothing validated revenue correlation in healthcare. This nailed the "knowledge gap" (emotion detection, sentiment-to-outcomes, NPS weaknesses) and set my direction: Test it empirically.
- **Assessment 2 (Research Tools & Methodologies)**: Building on A1's gap, this formalized my hunch into science. I crafted RQs (e.g., "Does NPS correlate with revenue growth?"), hypotheses (H1: Positive link), and a quantitative toolkit (Python pipeline for correlation/regression). It bridged intuition to method – like designing an ML experiment before coding.
- **Assessment 3 (Full Research Proposal)**: The capstone synthesized everything into a publication-ready plan. A1's gap + A2's methods became a pragmatic-positivist design, ethics framework, and ICT software flow. It's not just academic – it's a blueprint for production BI systems.

![Mermaid Markdown showing A1-A3 sequence](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kh28yj2bnip2yfobtycb.png)

---

## **2. What the Research Says (And What’s Missing)**

I reviewed **12+ peer-reviewed studies** across patient experience, NPS methodology, loyalty theory, and AI-based feedback systems.

### **What we KNOW**

* Patient experience improves loyalty (Godovykh & Pizam, 2023)
* NPS is widely used but criticized (Dawes, 2024)
* AI sentiment analysis is technically strong (Alkhnbashi et al., 2024)
* Patient feedback predicts operational quality (Shankar & Yip, 2024)
* Emotions affect engagement (Angelis et al., 2024)

![Conceptual model of NPS-revenue pathway](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bhn1x75cyaskkz5qosfi.png)

### **What NO ONE HAS DONE**

❌ validate whether **NPS statistically predicts revenue in healthcare**
❌ test whether higher NPS tracks with monthly business performance
❌ evaluate NPS using real clinic financial data
❌ build evidence-based decision frameworks for healthcare executives

**So that’s the gap. And that became my research question.**

![Gap between NPS adoption and validation](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q8v2xbsxfv94mg022bhw.png)

---

## **3. The Dataset (27,000 Survey Responses, 36 Months)**

Thanks to **Pro-Corpo Estética**, a healthcare group in Brazil, I got access to:

### **Dataset Structure**

* 27,000+ NPS survey responses
* Monthly revenue for multiple clinics
* 36 months of data (2022–2025)
* Aggregated by clinic + year-month
* Fully anonymized and LGPD/GDPR compliant

### **Why this dataset is gold**

It allows testing the assumption everyone makes:

> **“When NPS goes up, revenue should go up too.”**
> But does it *actually* happen?

Time to find out.

---

## **4. The Data Pipeline (Python + Pandas + Statsmodels)**

Here’s the workflow I built:

```
Raw CSV  
→ Cleaning & Missing Values  
→ Outlier Detection  
→ Aggregation (clinic-month)  
→ Derived Metrics (revenue growth %, lagged NPS)  
→ Correlation Tests  
→ Regression Modelling  
→ Visualizations / Dashboard  
```

![Software design flow diagram](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/joaf579i7m6wlxk6756j.png)

### **Code Example: Correlation Analysis**

```python
import pandas as pd
from scipy.stats import pearsonr, spearmanr

df = pd.read_csv("clinic_nps_revenue_clean.csv")

# Calculate revenue growth
df['revenue_growth'] = df.groupby('clinic')['revenue'].pct_change() * 100

# Pearson Correlation
pearson_r, pearson_p = pearsonr(
    df['nps_score'].dropna(),
    df['revenue_growth'].dropna()
)

print(f"Pearson r = {pearson_r:.3f}, p = {pearson_p:.4f}")
```

![Preliminary Pearson correlation matrix](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qau7rjd4amywamsv75f5.png)

![Correlation heatmap](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/aqan4vaajbsu44xquzmo.png)

### **Planned Models**

* Pearson + Spearman correlation
* Linear regression (with lagged variables)
* K-means clustering (clinic behavior patterns)
* Visual dashboards (Streamlit)

---

## **5. So… Does NPS Predict Revenue? (3 Possible Scenarios)**

This is the part everyone asks.

**I built a decision-impact framework**:

![Decision framework based on correlation strength](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2xr4n04620yx0q71ecoy.png)

---

### **Scenario 1 — Strong Correlation (r > 0.7)**

**NPS is a valid business KPI.**
→ Simple tracking systems are enough
→ Clinics can justify current investment
→ NPS becomes a leading indicator for finance teams

---

### **Scenario 2 — Moderate Correlation (0.3 < r < 0.7)**

**NPS is useful but incomplete.**
→ Combine NPS with sentiment, emotional analysis
→ Invest in smarter AI-driven tools
→ Good for trend detection, not forecasting

---

### **Scenario 3 — Weak/No Correlation (r < 0.3)**

**NPS is NOT a reliable indicator of revenue.**
→ Clinics must rethink their measurement strategy
→ Use richer qualitative + NLP models
→ Consider alternative satisfaction metrics

---

Whichever outcome occurs, the research will **finally provide evidence**, not assumptions.

![Example Scatter plot of NPS vs Revenue](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2yqw7lmtnurbvopexcuw.png)

---

## **6. Code + Architecture for Engineers**

This project is structured like a mature ML pipeline:

```
research_project/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_preprocessing.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_correlation.ipynb
│   └── 04_regression.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── analysis.py
│   ├── models.py
│   └── visualization.py
│
└── streamlit_app/
    └── dashboard.py
```

It mirrors real-world data engineering pipelines used in BI, ML, and healthcare analytics.

---

## **7. What This Means for Healthcare & AI**

### **Short version:**

You can’t build AI systems on shaky assumptions.

If NPS ≠ revenue, then:

* AI sentiment systems need rethinking
* Dashboards should emphasize different KPIs
* Marketing & retention strategies must pivot
* Budget allocation may change dramatically

If NPS = revenue, then:

* NPS becomes a validated financial lever
* Clinics can forecast demand using survey data
* AI models can be trained on validated correlations

In both cases, **ICT R&D gains a validated foundation**.

---

## **8. Explore the Research**

- [Assessment 1: Critical Literature Review](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-REM/assignments/Assessment1/REM502_Faria_L_Assessment_1_Critical-Literature-Review.pdf)
- [Assessment 2: Research Tools and Methodologies](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-REM/assignments/Assessment2/REM502_Faria_L_Assessment_2_Research-Tools-and-Methodologies.pdf)
- [Assessment 3: Full Research Proposal](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-REM/assignments/Assessment3/REM502_Faria_L_Assessment_3_Research-Proposal.pdf)
- [Presentation Slides](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-REM/assignments/Assessment3/REM502_Faria_L_Assessment_3.pdf)

---

## **9. What’s Next (Phase 2 & 3)**

### **Phase 2 – Extended Analysis**

* More complex regression (ARIMA, lag models)
* Business segmentation via clustering
* Qualitative coding of text comments
* Publish as interactive Streamlit app

### **Phase 3 – Publication Pathway**

* Submit to *International Journal of Market Research*
* Present at ACIS Conference
* Develop predictive model for revenue forecasting
* Integrate into **ClinicTrends AI v3**

---

## **10. Key Takeaways**

* NPS is widely used but poorly validated.
* Healthcare lacks evidence-based KPI frameworks.
* 27K+ real-world data points allow statistical validation.
* ICT R&D + ML pipelines can settle long-standing assumptions.
* This study builds the foundation for smarter healthcare analytics.

---

## **11. Let’s Connect**

If you're working with healthcare data, KPIs, BI dashboards, or ML pipelines — I’d love to connect.

- **LinkedIn:** [linkedin.com/in/lfariabr](https://www.linkedin.com/in/lfariabr/)  
- **GitHub:** [github.com/lfariabr](https://github.com/lfariabr)  
- **Portfolio:** [luisfaria.dev](https://luisfaria.dev)

---

## Final Note

This isn’t just a research assignment — it’s a problem the healthcare industry has ignored for years.
If the link between NPS and revenue exists, we’ll finally quantify it.
If it doesn’t, we’ll stop wasting money on metrics that don’t matter.

Either way, **data wins**.