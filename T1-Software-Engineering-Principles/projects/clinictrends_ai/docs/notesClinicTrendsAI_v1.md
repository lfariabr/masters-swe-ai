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