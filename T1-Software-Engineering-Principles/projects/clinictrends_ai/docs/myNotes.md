# ClinicTrends AI 💬📈

**Proactive Customer Satisfaction Dashboard for Aesthetic Clinics**

ClinicTrends AI is a lightweight, open-source analytics dashboard built with Streamlit that helps businesses analyze and predict Net Promoter Score (NPS) trends using real-time data, natural language processing, and machine learning.

It is designed for small to medium-sized businesses that need actionable insights from customer feedback—without the complexity or cost of enterprise software.

---

## 📦 Project Details

| Key       | Value            |
|-----------|------------------|
| **Name**  | ClinicTrends AI  |
| **Version** | 1.6.0          |
| **Stack** | Python, Streamlit, pandas, numpy, altair, textblob, deep-translator, transformers |
| **Goal**  | Analyze customer feedback and predict Net Promoter Score (NPS) trends using real-time data, natural language processing, and machine learning |


## 🔧 Getting Started

### ▶️ Run the Project

```bash
cd T1-Software-Engineering-Principles/projects/clinictrends_ai
source venv/bin/activate
streamlit run app.py
```

---

## 🧠 Key Features

- 📊 Interactive NPS analytics with Altair
- 🧾 CSV file upload and data preprocessing with pandas
- 💬 Sentiment analysis using TextBlob + wordcloud generation
- 🔄 Deep-translator integration for automatic translation
- 🤖 Planned: ML-powered predictions using Hugging Face pipelines

---

## ✅ Feature Progress

### ✔ Done
#### 🔹 v1.0.0 - `feature/clinic-trends-ai-base`
- Streamlit app with Altair, pandas, numpy displaying NPS data

#### 🔹 v1.1.0 - `feature/clinic-trends-ai-nlp`
- Adds NLP sentiment analysis, wordcloud visualizations

#### 🔹 v1.2.0 - `feature/clinic-trends-ai-refactor`
- Refactors into multi-page app:
  - Adds `views/` and `utils/` structure
  - Creates homepage with project overview
  - Adds a translation page using `deep-translator`
  - Moves business logic into `DashboardPage`
  - Notes Google Sheets translation trick: `=GOOGLETRANSLATE(C2;"pt";"en")`

#### 🔹 v1.3.0 - `feature/clinic-trends-ai-deploy`
- Deploys to Streamlit Cloud; integrates Hugging Face pipelines

#### 🔹 v1.4.0 - `feature/clinic-trends-ai-training`
- Training/fine-tuning TextBlob (suggested by Dr. Ranju)
- "feat(sep_clinicTrendsAI_v1.4) sets up ground for ML training to increase accuracy"
- "feat(sep_clinicTrendsAI_v1.4) implements training page"
- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment" (done, 19.06)
- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment x trained model +score", looking interesting (done 19.06)
- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment x trained model x transformers". (done 20.06)
- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment x trained model x transformers". - pizza graphic... (done 22.06)
- "feat(sep_clinicTrendsAI_v1.4) adds transformers comments+score". (done 25.06)

#### 🔹 v1.5.0 - `feature/clinic-trends-ai-score-1-5`
- Add support to chosing between score 1-5 or 1-10

#### 🔹 v1.6.0 - `feature/clinic-trends-ai-models-page`
- Adds one page with all available models to be ran and compared versus NPS

#### 🔹 v1.7.0 - `feature/clinic-trends-ai-main-page`
- Main interface with file upload and model selection
- Beautiful interface for uploading file and running models

---

### 🔧 In Progress

#### 🔸 v1.8.0 - `feature/clinic-trends-ai-tbd`
- tbd

---

### 🗂️ Backlog

- Add Pytest coverage 
- Add automated alert system for NPS drop detection (v2.0)
- Implement interpretable ML models for NPS prediction (v2.0)
- Fine-tune transformer models for domain-specific sentiment (v2.0)
- Add RESTful API development + authentication (v3.0)
- AI-powered insights (v4.0)

---

## 🧪 Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: pandas, numpy
- **Visualization**: Altair, wordcloud
- **NLP**: TextBlob, Hugging Face Transformers, deep-translator
- **Deployment**: Streamlit Cloud

---

## 🤝 Contributors

- Luis Faria  
- Jing Feng Chin  
- Luong Hai Chau  

Project for SEP401 – Software Engineering Principles @ Torrens University

---

## 📅 Version Control Roadmap

| Version | Modules            | Status         |
|---------|---------------------|----------------|
| 1.0.0   | Modules 1–4         | ✅ Done        |
| 2.0.0   | Modules 5–8         | 🔥 In Progress |
| 3.0.0   | Modules 9–12        | 🕐 Not started |

---

## 🧠 Insights & Learning

This project explores practical applications of:
- Software engineering planning and version control
- Data visualization and business storytelling
- Sentiment analysis and language translation
- ML pipelines for text classification and trend prediction

# Inspirational Quote based on Tech Stack and Projects' Goals

---

> “Whether it’s concrete or code, structure is everything.”