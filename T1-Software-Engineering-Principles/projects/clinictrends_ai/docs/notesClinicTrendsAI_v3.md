## **v3.0 breakdown**

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

### Phase 2: Intelligence Enhancement (v2.0) ✅ **COMPLETE**
- ✅ Provides sample csv files for enhanced UX
- ✅ Alert system based on NPS and sentiment scores
- ✅ A/B testing framework for model comparison
- ✅ Model fine-tuning and reaching accuracy of +80%
- ✅ Automated hyperparameter optimization
- ✅ Implementing Topic Modeling

### Phase 3: Machine Learning Pipeline (v3.0) ✅ **COMPLETE**
- ✅ Advanced feature engineering pipelines
    - ✅ Adds MLPipeline to NPSPage for centralized visualization
    - ✅ Adds TopicModelingPage for business insights
- ✅ Pytest robustness coverage

### Phase 4: Enterprise Integration (v4.0) 📋 **PLANNED**
- 📋 Real-time model retraining capabilities
- 📋 RESTful API development
- 📋 Database integration (PostgreSQL/MongoDB)
- 📋 User authentication & role-based access
- 📋 Advanced security & compliance features

### Phase 5: AI-Powered Insights (v5.0) 🚀 **PLANNED**
- 🚀 GPT-powered natural language insights
- 🚀 Automated report generation
- 🚀 Predictive customer lifetime value modeling
- 🚀 Integration with CRM systems

---

## ✅ Feature Progress

### ✔ Done
**v3.0 breakdown**

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

#### 🟢 v3.5.0 - week 11 - `feature/robust-testing-coverage`
- Expand pytest coverage for new topic modeling features
- Error handling validation

---

### 🔧 In Progress

- ***thinking about new logo and working on pitch deck***

---

### 🗂️ Backlog

#### Future
- Google Maps/TikTok API for getting reviews
- OpenAI API for getting insights
- Start saving data from pipeline flow associated with input "company name", "country"
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