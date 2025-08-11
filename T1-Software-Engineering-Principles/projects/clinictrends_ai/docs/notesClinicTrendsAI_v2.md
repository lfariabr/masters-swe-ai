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
- ✅ Automated hyperparameter optimization
- ✅ Implementing Topic Modeling
- ✅ Advanced feature engineering pipelines
    - ✅ Adds MLPipeline to NPSPage for centralized visualization
    - ✅ Adds TopicModelingPage for business insights
- 🔄 Pytest robustness coverage

### Phase 3: Enterprise Integration (v3.0) 📋 **TBD**
- 📋 Real-time model retraining capabilities
- 📋 RESTful API development
- 📋 Database integration (PostgreSQL/MongoDB)
- 📋 User authentication & role-based access
- 📋 Advanced security & compliance features

### Phase 4: AI-Powered Insights (v4.0) 🚀 **TBD**
- 🚀 GPT-powered natural language insights
- 🚀 Automated report generation
- 🚀 Predictive customer lifetime value modeling
- 🚀 Integration with CRM systems

---
## ✅ Feature Progress

### ✔ Done
**v2.0 breakdown**

#### 🟢 v2.0.0 - `feature/discord-webhook`
- Add discord webhook for alerting when app's used at key pages
- Improve home page experience with st.balloons and interactive click

#### 🟢 v2.1.0 - `feature/alert-system`
- Adds sample csv file for enhanced UXs
- Add alert system for NPS drop detection

#### 🟢 v2.2.0 - `feature/tf-idf-max-features`
- Testing different values for max_features in the TF-IDF vectorizer to find the optimal feature set size for model performance.

#### 🟢 v2.3.0 - `feature/tf-idf-deep-dive`
- Adds notes on tf-idf vectorizer
- Adds comments size statistics
- Updates Models page hiding transformers for the moment while we fine tune tf-idf

#### 🟢 v2.4.0 - `feature/tf-idf-iteration-check`
- Added n_iter = model.n_iter_[0] at ModelTrainer.py
- print(f"Iterations until convergence for {model_name}: {n_iter}")
- st.write(f"Iterations until convergence for {model_name}: {n_iter}")

#### 🟢 v2.5.0 - `feature/train-validation-test-split`
- Implement proper three-way split (train/validation/test) for robust model evaluation.
- Adjust current pipeline to avoid tuning on test data.
- Report separate metrics for train, validation, and test sets.

#### 🟢v2.6.0 - `feature/logreg-hyperparam-tuning`
- Expand Logistic Regression tuning:
  - Regularization parameter C
  - Penalty type (L1 vs. L2)
  - Solver selection
  - Multi-class handling (ovr vs multinomial)
- Document best hyperparameter sets.

#### 🟢v2.6.1 - `feature/dynamic-hyperparameter-injection`
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

#### 🟢v2.6.2 - `feature/meeting-with-dr-ranju`
- current pipeline: Data ➔ Preprocessing ➔ Sentiment Analysis ➔ Performance Metrics
- suggested pipeline: Data ➔ Preprocessing ➔ Sentiment Analysis ➔ Topic Modeling ➔ Insights ➔ Business - Study BERTopic (BERT + clustering), Sci-kit Learn (LDA, NMF, LSA) and Gensim (LDA, LSI)
- Read the links Dr. Ranju shared. BERTopic is one of the best modern tools for topic modeling:
  - Handles short texts better than LDA
  - Uses embeddings (e.g. BERT) for semantically richer clusters
  - Generates interpretable topic names.
  - Useful Links:
    - https://www.linkedin.com/pulse/topic-modeling-uncovering-hidden-themes-text-mohamed-chizari-y1w2e/
    - https://wellsr.com/python/topic-modeling-with-bert-using-python-bertopic-library/?utm_source=chatgpt.com
    - https://www.datacamp.com/tutorial/what-is-topic-modeling?utm_source=chatgpt.com
    - https://hackernoon.com/nlp-tutorial-topic-modeling-in-python-with-bertopic-372w35l9

> **Note:** Paused here to refactor pages and model class before integrating BERTopic to pipeline

#### 🟢v2.7.0 - `feature/enhanced-model-trainer`
- Split code between ModelTrainer.py and EnhancedModelTrainer.py
- EnhancedModels will display work in progress with model fune tuning, metrics and Topic Modeling
- ModelTrainer will display the current models' metrics and predictions

#### 🟢 v2.8.0 - `feature/topic-modeling`
- Integrate BERTopic into Pipeline
  - created BERTopicModel.py
  - `pip install bertopic` + `pip install sentence-transformers` + `pip install umap-learn plotly`
  - add streamlit Page TopicModelingPage
  - writes doc of what needs to be done yet (share with Dr. Ranju)

#### 🟢 v2.8.1 - `feature/refactor-about-and-nps-views`
- separation of concerns and easy maintenance

#### 🟢 v2.8.2 - `feature/refactor-models-views`
**part 1:**
- start project.... I'm pausing now to focus on Frontend CSS Challenge a little bit. Might be inspirational to think about user experience to bring here.
- got back here after a couple of minutes... found an interesting library, i'll test
- created `appClinicTrendsAi.md` for instructions on how to run the app
- imported import streamlit_shadcn_ui as ui - DISCONTINUED
- adds tabs to models page for enhanced exp

**part 2:**
- drilling down functions from `ModelsPage.py` to `utils.visualizations`

**part 3:**
- drilling down more functions from `ModelsPage.py` and `NPSPage.py` to `utils.visualizations`
- separation of concerns for review crosstab analysis, heatmaps and metrics in `utils.crosstab_analysis`

#### 🟢 v2.8.3 - `feature/refactor-enhanced-models-views`
**part 1:**
- reorganizing `EnhancedModels.py` page with tabs and expanders

**part 2:**
- better naming from `EnhancedModelsPage.py` to `MLExperimentsPage.py`
- adds flow diagram [ModelTrainer_ClassDiagram](T1-Software-Engineering-Principles/projects/clinictrends_ai/docs/diagrams/ModelTrainer_ClassDiagram.png) mapping out object relationships

#### 🟢 v2.8.4 - `feature/refactor-model-trainer`
**part 1:**
- reading again feature 1 and 2 to get context fresh
- reviewing **EXACTLY** what function `train_tfidf_model` does
- thinknig that maybe 2.8.1 should split into coliumns instead of tabs - maybe back to this later
- read diagram again and write my understanding of the functions there (#TODO this can easily became a dev.to article on my learning journey!)

**train_idf_model** <> my notes
***intro***
for starters, this beast is the responsible for making sure the model is an animal, ready to receive the data and return the SHARPEST model it possibly can handle. 
the received data is gonna face a series of cuts that will return a high accuracy model able to predict the sentiment of the received comments, no matter how FAT/COMPLEX they arrive.
> ***Fun Fact: this function is the personal trainer with a motherfucking knife in the teeths, living on the grip of life, ape shit, to get after it.***

***parameters***
- self: ?!
- df: preprocessed and filtered user's csv dataframe + annotated sentiment
- feature_column: comment column
- target_column: sentiment column (target that we want to predict)
- model_name: unique id for the model
- score_column: optional column containing numerical scores to use as additional features

***key change***
- target_column changed from "Sentiment" to "NPS Type" to align with the business logic

#### 🟢 v2.8.5 - `feature/sprint-review`
- Split what will be done in the next 3 weeks and what COULD be done on the future

#### 🟢 v2.8.6 - `feature/google-maps-api`
- Checking Streamlit's new top nav (it was not worth it... i already have "st.sidebar", which might be conflicting) - 15m
- Google Maps API Page for grabbing reviews from places

#### 🟢 v3.0.0 - week 9 - `feature/complete-bertopic-integration`
***part 1*** v3.0.0
- added BERTopic to `MLPipeline.py` together with model_trainer (1, 2, 3 and 4)
- Complete BERTopic integration into full pipeline
- Map discovered topics to actionable business recommendations:
  - "Topic: Delivery delays" → "Improve logistics or communication"
  - "Topic: Website issues" → "Prioritize website performance improvements"
- Add topic visualization and interpretation to UI
- Document topic-to-action mapping framework

***part 2*** v3.0.1
- organize `MLPipeline.py` so that we can actually plug to `NPSPage.py`
- during my process of thinking MLPipeline, I think that it is confusing to display 4 models tab for the final user, 
- so now we run all of them in parallel, display the "Model Performance Overview" and "Detailed Performance Metrics" straight forward

***part 3*** v3.0.2
- before, I opted to first integrate Step1 into `MLPipeline.py`... getting closer!
- iterating, was able to put train models in there...
- dealt with comprehensive error handling on `utils.visualizations.py`
- Added spinner to `NPSPage.py` to display progress while training models
- When we click "🚀 Train All ML Models":
  - Step 1: Data Preprocessing & Sentiment Analysis
    - Annotate sentiments using TextBlob
    - Convert scores to NPS categories (Promoter/Passive/Detractor)
    - Create "NPS Type" column for model training
  - Step 2: Multi-Model Training
    - Train Model 1: Comment-Based Classification
    - Train Model 2: Comment-Score Fusion
    - Train Model 3: Transformer-Enhanced (with graceful error handling)
    - Train Model 4: Hybrid Transformer-Score Integration
    - Display performance metrics and visualizations

#### 🟢 v3.1.0 - week 10 part 1 - `feature/topic-modeling-to-pipeline`
- worked on `MLPipeline.py` Step 2: Topic Modeling & Discovery, fine tunning UX before plugging to `NPSPage.py`
- def `display_topic_results`: organized col1 and col2 info display
- def `generate_business_insights`: displaying 15 topics upfront and full table in expander
- def `color_nps`: adjusted to match NPS 9-10, 7-8 and below 6
- def `generate_recommendations`: break it down into:
  - Topic Performance Analysis: display 15 topics with performance metrics
  - Actionable Recommendations: display 5 positive, 5 negative topics
  - Detailed view of comments for each topic for raw download
  - Strategic Insights: final recommendations based on processed data
- Integrate BERTopic into Pipeline (Add Topic Modeling to Pipeline)
- Map Topics → Business Recommendations. E.g.:
  - “Topic: Delivery delays” → “Improve logistics or communication”
  - “Topic: Website issues” → “Prioritize website performance improvements”
- add fine tuned topic modeling to `NPSPage.py`

#### 🟢 v3.2.0 - week 10 part 2 - `feature/sprint-review`
- fine tune web form: https://forms.gle/uiJ2vFgoqZP4uvUx5
- draw a PPT to display on the meeting with a "FOR DUMMIES" version of the ClinicTrendsAI
  - from PM to SWE focused on ML engineering
  - Data from PC & curiosity that people actually WRITE their feelings on the internet
  - 80% of accuracy reached, do we have similar cases to that? what's the input and take based on that?
  - who is the profile of the user who I assume replied
- grab tiktok data and run a quick comparison with Canario's tiktok viral (tiktok vs profile)
- check with Dr. Ranju if we can invite outsiders for the presentation of the app
- names like Samir, Andre, Anao, Rica, Sibelius, Ciro, Will, Lace, Dr Atif, Dr Ranju, Dr Nandine

#### 🟢 v3.3.0 - week 11 - `feature/benchmark-validation`
- Research published benchmarks using similar datasets
- Compare achieved results against external references
- Document target metrics for improvement
- Cross-check with literature (as Dr. Ranju suggested)
- Compiled files can be found [here](./T1-Software-Engineering-Principles/projects/clinictrends_ai/docs/references)

#### 🟢 v3.4.0 - week 11 - `feature/checkpoint-dr-ranju`
- Top 15 Topics by Comment Volume table now displays Avg_Score, NPS_Score and Avg_Confidence with rounded values
- ***the reason .round(2) or .round(1) was not showing in the table is because st.dataframe with a pandas Styler ignores Python’s native rounding for display and instead uses its own formatting logic.***
- removed Avg_score column from the table as it wasn't being helpful
- ***Example: If 3 people gave 9, 7, and 8 for Topic A, the Avg_Score = (9 + 7 + 8) / 3 = 8.0.***
- adds model 2 accuracy to generate_biz_insights
- adjusted sentiment distribution area to have graphic side by side with word cloud from comments
- created a function to clean Topic Modeling names
```python
def clean_topic_name(name: str, *, lower: bool = True) -> str:
    """Turn '12_service_great_excellent_good' → 'service great excellent good'."""
    if pd.isna(name):
        return name
    s = str(name).strip()
    s = re.sub(r'^\s*-?\d+_?', '', s)   # drop leading numeric id like 0_, 12_, -1_
    s = s.replace('_', ' ')             # underscores → spaces
    s = re.sub(r'\s+', ' ', s).strip()  # collapse spaces
    return s.lower() if lower else s
```
- added accuracy of model per topic at `Top 15 Topics by Comment Volume`
- refactored `Actionable Recommendations` to be more compact
- improved `Topic Analysis Results`, `Business Insights` and `Model Performance Overview`
- adjusted sidebar to be visible and switched to v3.4.0

---

### 🔧 In Progress

#### ▫️ v3.5.0 - week 11 - `feature/robust-testing-coverage`
- Expand pytest coverage for new topic modeling features
- Add integration tests for end-to-end pipeline
- Performance testing for large datasets
- Error handling validation

---

### 🗂️ Backlog

#### Hotfixes
- ***think about new logo***
- ***google maps api, think what to do with it***
- Pitch Deck (`feature/pitch-deck`)

#### Future
- Start saving data from pipeline flow (preprocessing, sentiment analysis, topic modeling, insights, business actions, id, date, allow user to input "company name", "country")
- Implement interpretable ML models for NPS prediction
- Fine-tune transformer models for domain-specific sentiment
- Add RESTful API development + authentication
- AI-powered insights
- `feature/model-comparison`
  - Add experiments with alternative models:
    - Support Vector Machine (SVM)
    - Random Forest
  - Store performance metrics for analysis.

---

> “Whether it’s concrete or code, structure is everything.”