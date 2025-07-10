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

## 📈 Development Roadmap

### Phase 1: Foundation (v1.0-1.8) ✅ **COMPLETE**
- ✅ Core Streamlit application architecture
- ✅ Multi-page navigation system
- ✅ 4 ML model implementations
- ✅ Interactive visualization suite
- ✅ Translation capabilities
- ✅ Comprehensive documentation
- ✅ Main interface with file upload and model selection
- ✅ Pytest initial setup

### Phase 2: Intelligence Enhancement (v2.0) 🔄 **IN PROGRESS**
- ✅ Provides sample csv files for enhanced UX
- ✅ Alert system based on NPS and sentiment scores
- ✅ A/B testing framework for model comparison
- 🔄 Model fine-tuning
- 🔄 Advanced feature engineering pipelines
- 🔄 Automated hyperparameter optimization
- 🔄 Real-time model retraining capabilities
- 🔄 Pytest robustness coverage

### Phase 3: Enterprise Integration (v3.0) 📋 **PLANNED**
- 📋 RESTful API development
- 📋 Database integration (PostgreSQL/MongoDB)
- 📋 User authentication & role-based access
- 📋 Advanced security & compliance features

### Phase 4: AI-Powered Insights (v4.0) 🚀 **FUTURE**
- 🚀 GPT-powered natural language insights
- 🚀 Automated report generation
- 🚀 Predictive customer lifetime value modeling
- 🚀 Integration with CRM systems

---

## ✅ Feature Progress

### ✔ Done
**v1.0 breakdown**
#### 🔹 v1.0.0 - `feature/base`
- Streamlit app with Altair, pandas, numpy displaying NPS data

#### 🔹 v1.1.0 - `feature/nlp`
- Adds NLP sentiment analysis, wordcloud visualizations

#### 🔹 v1.2.0 - `feature/refactor`
- Refactors into multi-page app:
  - Adds `views/` and `utils/` structure
  - Creates homepage with project overview
  - Adds a translation page using `deep-translator`
  - Moves business logic into `DashboardPage`
  - Notes Google Sheets translation trick: `=GOOGLETRANSLATE(C2;"pt";"en")`

#### 🔹 v1.3.0 - `feature/deploy`
- Deploys to Streamlit Cloud; integrates Hugging Face pipelines

#### 🔹 v1.4.0 - `feature/training`
- Training/fine-tuning TextBlob (suggested by Dr. Ranju)
- "feat(sep_clinicTrendsAI_v1.4) sets up ground for ML training to increase accuracy"
- "feat(sep_clinicTrendsAI_v1.4) implements training page"
- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment" (done, 19.06)
- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment x trained model +score", looking interesting (done 19.06)
- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment x trained model x transformers". (done 20.06)
- "feat(sep_clinicTrendsAI_v1.4) compare text blob x nps x trained model +comment x trained model x transformers". - pizza graphic... (done 22.06)
- "feat(sep_clinicTrendsAI_v1.4) adds transformers comments+score". (done 25.06)

#### 🔹 v1.5.0 - `feature/score-1-5`
- Add support to chosing between score 1-5 or 1-10

#### 🔹 v1.6.0 - `feature/models-page`
- Adds one page with all available models to be ran and compared versus NPS

#### 🔹 v1.7.0 - `feature/main-page`
- Main interface with file upload and model selection
- Beautiful interface for uploading file and running models

#### 🔹 v1.8.0 - `feature/pytest`
- creates pytest.ini
- add pytest to homepage and models page

#### 🔹 v1.9.0 - `feature/menu-structure`
- Refactor menu structure
- Split ModelTrainer class into a resolver
- Adds 4 models in Model Performance Comparison table
- Add wordcloud to models page
- Add NPS donut chart and monthly NPS trend chart to models page
- Change menu to "Models Page" to "ML Model Comparison"
- Change dashboard to "NPS Analysis"
- Update Pytest coverage

---
**v2.0 breakdown**

#### 🔹 v2.0.0 - `feature/discord-webhook`
- Add discord webhook for alerting when app's used at key pages
- Improve home page experience with st.balloons and interactive click

#### 🔹 v2.1.0 - `feature/alert-system`
- Adds sample csv file for enhanced UXs
- Add alert system for NPS drop detection

#### 🔹 v2.2.0 - `feature/tf-idf-max-features`
- Testing different values for max_features in the TF-IDF vectorizer to find the optimal feature set size for model performance.

#### 🔹 v2.3.0 - `feature/tf-idf-deep-dive`
- Adds notes on tf-idf vectorizer
- Adds comments size statistics
- Updates Models page hiding transformers for the moment while we fine tune tf-idf

---

### 🔧 In Progress

#### 🔸 v2.4.0 - `feature/tbd`
- tbd

### 🗂️ Backlog

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

> “Whether it’s concrete or code, structure is everything.”