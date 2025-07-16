# ClinicTrends AI 💬📈

## 🔧 Work in Progress

```bash
cd T1-Software-Engineering-Principles/projects/clinictrends_ai
source venv/bin/activate
streamlit run app.py
```

---

## 📈 Roadmap

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
- ✅ Model fine-tuning and reaching accuracy of +80%
- 🔄 Implementing Topic Modeling
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

#### 🔹 v2.4.0 - `feature/tf-idf-iteration-check`
- Added n_iter = model.n_iter_[0] at ModelTrainer.py
- print(f"Iterations until convergence for {model_name}: {n_iter}")
- st.write(f"Iterations until convergence for {model_name}: {n_iter}")

#### 🔹 v2.5.0 - `feature/train-validation-test-split`
- Implement proper three-way split (train/validation/test) for robust model evaluation.
- Adjust current pipeline to avoid tuning on test data.
- Report separate metrics for train, validation, and test sets.

#### 🔹v2.6.0 - `feature/logreg-hyperparam-tuning`
- Expand Logistic Regression tuning:
  - Regularization parameter C
  - Penalty type (L1 vs. L2)
  - Solver selection
  - Multi-class handling (ovr vs multinomial)
- Document best hyperparameter sets.

#### 🔹v2.6.1 - `feature/dynamic-hyperparameter-injection`
- Refactored ModelTrainer.py to support dynamic hyperparameter injection for Logistic Regression.
- Key changes:
  - **find_optimal_features**
    - Changed return value to return the entire `best_params` dictionary from GridSearchCV instead of only `vectorizer__max_features`.
    - Now captures all optimal hyperparameters (e.g. `C`, `solver`, `penalty`, `multi_class`, and `max_iter`) for use in model training.
  - **train_tfidf_model**
    - Injects all hyperparameters dynamically into the Logistic Regression model, replacing previously hardcoded values.
    - `max_iter` is now selected via grid search rather than being fixed.

- Benefits:
  - Eliminates hardcoded model parameters.
  - Enables fully automated tuning of hyperparameters for optimal model performance.

#### 🔹v2.7.0 - `feature/enhanced-model-trainer`
- Split code between ModelTrainer.py and EnhancedModelTrainer.py
- EnhancedModels will display work in progress with model fune tuning, metrics and Topic Modeling
- ModelTrainer will display the current models' metrics and predictions

---

### 🔧 In Progress



### 🗂️ Backlog

#### 🔸 v3.0.0 - `feature/topic-modeling`
- current pipeline: Data ➔ Preprocessing ➔ Sentiment Analysis ➔ Performance Metrics
- suggested pipeline: Data ➔ Preprocessing ➔ Sentiment Analysis ➔ Topic Modeling ➔ Insights ➔ Business Actions
- Study BERTopic
- Read the links Dr. Ranju shared. BERTopic is one of the best modern tools for topic modeling:
  - Handles short texts better than LDA
  - Uses embeddings (e.g. BERT) for semantically richer clusters
  - Generates interpretable topic names.
- Integrate BERTopic into Pipeline
- Map Topics → Business Recommendations. E.g.:
  - “Topic: Delivery delays” → “Improve logistics or communication”
  - “Topic: Website issues” → “Prioritize website performance improvements”
- Cross-Check with Literature
  - Look for papers or blog posts analyzing your dataset. 
  - Dr. Ranju suggests referencing prior works rather than repeating experiments unnecessarily.


#### `feature/model-comparison`
  - Add experiments with alternative models:
    - Support Vector Machine (SVM)
    - Random Forest
  - Compare results to Logistic Regression baseline.
  - Store performance metrics for analysis.

#### `feature/outlier-handling`
  - Identify extremely long comments (e.g. > 200 tokens).
  - Implement:
    - Truncation
    - Or exclusion from training
  - Measure impact on model performance.

#### `feature/benchmark-check`
  - Research published benchmarks or similar projects using this dataset.
  - Compare achieved results against external references.
  - Document potential target metrics for improvement.

- Implement interpretable ML models for NPS prediction (v2.0)
- Fine-tune transformer models for domain-specific sentiment (v2.0)
- Add RESTful API development + authentication (v3.0)
- AI-powered insights (v4.0)

---

> “Whether it’s concrete or code, structure is everything.”