# ClinicTrends AI 💬📈

**Proactive Customer Satisfaction Dashboard for Aesthetic Clinics**

ClinicTrends AI is a lightweight, open-source analytics dashboard built with Streamlit that helps businesses analyze and predict Net Promoter Score (NPS) trends using real-time data, natural language processing, and machine learning.

It is designed for small to medium-sized businesses that need actionable insights from customer feedback—without the complexity or cost of enterprise software.

---

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

## 🚀 Version History

### ✅ Done
- **v1.0.0** – Streamlit app with Altair, pandas, numpy displaying NPS data (2025-06-08)
- **v1.1.0** – Adds NLP sentiment analysis, wordcloud visualizations (2025-06-10)
- **v1.2.0** – Refactors into multi-page app:
  - Adds `views/` and `utils/` structure
  - Creates homepage with project overview
  - Adds a translation page using `deep-translator`
  - Moves business logic into `DashboardPage`
  - Notes Google Sheets translation trick: `=GOOGLETRANSLATE(C2;"pt";"en")`
- **v1.3.0** – Deploys to Streamlit Cloud; integrates Hugging Face pipelines

### 🚧 In Progress
- **v1.4.0** – Training/fine-tuning TextBlob (suggested by Dr. Ranju)
--- "feat(sep_clinicTrendsAI_v1.4) sets up ground for ML training to increase accuracy"
--- "feat(sep_clinicTrendsAI_v1.4) implements training page"
--- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment" (done, 19.06)
--- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment x trained model +score", looking interesting (done 19.06)
--- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment x trained model +score x transformers". (to be done)


### 📝 Backlog
- **v1.5.0** – Hotfix: add support to chosing between score 1-5 or 1-10
- **v1.6.0** – Fine-tune transformer models for domain-specific sentiment
- **v1.7.0** – Add automated alert system for NPS drop detection
- **v1.8.0** – Implement interpretable ML models for NPS prediction

---

## 🧪 Tech Stack

- **Frontend**: Streamlit
- **Data Processing**: pandas, numpy
- **Visualization**: Altair, wordcloud
- **NLP**: TextBlob, Hugging Face Transformers, deep-translator
- **Deployment**: Streamlit Cloud

---

## 👨‍🔬 Authors

- Luis Guilherme de Barros Andrade Faria  
- Jing Feng Chin  
- Luong Hai Chau  

Project for SEP401 – Software Engineering Principles @ Torrens University

---

## 🧠 Insights & Learning

This project explores practical applications of:
- Software engineering planning and version control
- Data visualization and business storytelling
- Sentiment analysis and language translation
- ML pipelines for text classification and trend prediction
