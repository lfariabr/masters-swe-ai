# 🔍 ClinicTrends AI
## Intelligent Customer Satisfaction Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red.svg)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5+-orange.svg)](https://scikit-learn.org)
[![Transformers](https://img.shields.io/badge/🤗%20Transformers-4.52+-yellow.svg)](https://huggingface.co/transformers)
[![Version](https://img.shields.io/badge/Version-1.9.0-brightgreen.svg)](CHANGELOG.md)

> **ML-powered analytics platform that transforms customer feedback into actionable business intelligence through advanced NLP, predictive modeling, and real-time sentiment analysis.**

---

## 🎯  What is ClinicTrends AI?

Traditional customer surveys are reactive and manual. ClinicTrends AI provides:
- 📊 Interactive NPS analytics with Altair
- 🧾 CSV file upload and data preprocessing with pandas
- 💬 Sentiment analysis using TextBlob + wordcloud generation
- 🔄 Deep-translator integration for automatic translation
- 🤖 ML-powered predictions using Hugging Face pipelines + custom trained models

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** with pip package manager
- **Virtual environment** 
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### Installation & Launch
```bash
# Navigate to project directory
cd T1-Software-Engineering-Principles/projects/clinictrends_ai

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Launch application
streamlit run app.py
```

---

## 🏗️ System Architecture

ClinicTrends AI implements a **modular, microservices-inspired architecture** following software engineering best practices:

```
ClinicTrends AI/
├── 🚀 app.py                # Entry point (Streamlit orchestration)
├── 📱 views/                # Presentation layer (UI screens)
│   ├── HomePage.py
│   ├── NPSPage.py
│   ├── TranslatePage.py
├── ⚙️ resolvers/            # Application layer (Controllers, pipeline logic)
│   ├── ModelTrainer.py
│   ├── BERTopicModel.py
│   ├── pipeline_controller.py  # New split (from EnhancedMLPipeline)
├── 🧳 utils/                # Domain layer (Preprocessing, NLP, viz, alerts)
│   ├── preprocessing.py
│   ├── nlp_analysis.py
│   ├── visualizations.py
├── 🎨 public/               # Static assets
├── 🧪 tests/                # Unit test suite
├── 📊 docs/                 # IEEE documentation & specs
└── 📚 requirements.txt
```

---

## 🧠 Machine Learning Architecture

### Multi-Model Ensemble Approach

ClinicTrends AI implements **4 distinct ML pipelines** and **Topic Modeling** for comprehensive sentiment analysis and business insights:

#### **Model 1: Comment-Based Classification**
```python
# TfidfVectorizer + LogisticRegression on Comment text
Pipeline: Raw Comments → TF-IDF Vectorization → Logistic Regression → Sentiment Classification
Features: 5,000 TF-IDF features with English stop-word filtering
Performance: Optimized for text-only sentiment detection
```

#### **Model 2: Enhanced Comment-Score Fusion**
```python
# TfidfVectorizer + LogisticRegression on Comment + NPS Score
Pipeline: Comments + Scores → Feature Fusion → TF-IDF → Classification
Innovation: Combines textual and numerical features for improved accuracy
Use Case: Holistic sentiment analysis incorporating quantitative feedback
```

#### **Model 3: Transformer-Enhanced Classification**
```python
# Hugging Face Transformers + Custom Training
Pipeline: Comments → DistilBERT → Fine-tuned Classification → Ensemble Prediction
Technology: State-of-the-art transformer models (DistilBERT-base-uncased)
Advantage: Context-aware sentiment understanding with transfer learning
```

#### **Model 4: Hybrid Transformer-Score Integration (Prototype)**
```python
# Advanced fusion of Transformers + Numerical Features
Pipeline: Comments + Scores → Transformer Encoding → Feature Fusion → Classification
Innovation: Combines transformer embeddings with numerical NPS data
Result: Highest accuracy through multi-modal learning approach
```

#### **Topic Modeling**
```python
# BERTopic + Custom Training
Pipeline: Comments → BERTopic → Topic Modeling → Business Insights
Technology: State-of-the-art topic modeling (BERTopic)
Advantage: Discover latent themes and patterns in customer feedback
```

---

## 📈 ClinicTrends AI Roadmap

### Phase 1: Foundation (v1.0-1.8) ✅ **COMPLETE**
- ✅ Core Streamlit application architecture
- ✅ Multi-page navigation system
- ✅ Translation capabilities via Deep-translator
- ✅ Sentiment Analysis using TextBlob + wordcloud generation
- ✅ 4 Machine Learning model implementations
- ✅ Pytest initial setup

### Phase 2: Intelligence Enhancement (v2.0) 🔄 **IN PROGRESS**
- ✅ A/B testing framework for model comparison
- ✅ Model fine-tuning and reaching accuracy of +80%
- ✅ Automated hyperparameter optimization
- ✅ Implemented Topic Modeling with BERTopic
- ✅ Advanced feature engineering pipelines
    - ✅ Successful implementation of Machine Learning Pipeline (4 models) to NPSPage
    - ✅ Added Topic Modeling to Machine Learning Pipeline
- 🔄 Pytest robustness coverage
- 🔄 ClinicTrends AI Pitch Deck

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

## 🔗 Resources & Links

- 🌐 **[Live Demo](https://sep-torrens-dr-ranju-group-1.streamlit.app/)**: Interactive application showcase
- 📚 **[Documentation](docs/)**: Comprehensive technical specifications
- 🎥 **[Demo Video](https://youtube.com/demo)**: Walkthrough of key features (in progress)

---

*Built with ❤️ and rigorous engineering principles by the ClinicTrends AI team*

**"Whether it’s concrete or code, structure is everything."**