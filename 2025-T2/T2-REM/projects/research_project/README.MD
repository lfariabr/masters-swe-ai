# Does NPS Really Predict Revenue in Healthcare Clinics? I Spent 12 Weeks Finding Out.

The Dataset (27,000 Survey Responses, 36 Months)

Thanks to **Pro-Corpo Estética**, a healthcare group in Brazil, I got access to:

## Dataset Structure

* 27,000+ NPS survey responses
* Monthly revenue for multiple clinics
* 36 months of data (2022–2025)
* Aggregated by clinic + year-month
* Fully anonymized and LGPD/GDPR compliant

## Why this dataset is gold

It allows testing the assumption everyone makes:

> **“When NPS goes up, revenue should go up too.”**
> But does it *actually* happen?

Time to find out.

---

## The Data Pipeline (Python + Pandas + Statsmodels)

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

## Code + Architecture for Engineers

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