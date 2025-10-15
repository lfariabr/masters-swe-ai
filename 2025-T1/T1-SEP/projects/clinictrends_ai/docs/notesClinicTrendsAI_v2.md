## **v2.0 breakdown**

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
- adds flow diagram [ModelTrainer_ClassDiagram](T1-SEP/projects/clinictrends_ai/docs/diagrams/ModelTrainer_ClassDiagram.png) mapping out object relationships

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

---

> “Whether it’s concrete or code, structure is everything.”