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
├── 🚀 app.py                    # Streamlit application orchestrator
├── ✅ tests/                    # Unit tests
├── 📊 docs/                     # IEEE standards documentation
├── 📱 views/                     # Presentation layer (MVC pattern)
├── 🧠 utils/                   # Business logic & core algorithms
└── 🎨 public/                   # Static assets & branding
```

---

## 🧠 Machine Learning Architecture

### Multi-Model Ensemble Approach

ClinicTrends AI implements **4 distinct ML pipelines** for comprehensive sentiment analysis:

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

*Note: Transformer-based models have been integrated for experimentation and performance benchmarking but were not part of the original MVP scope defined in the IEEE SRS.*

### Performance Benchmarking Framework

```python
def collect_metrics(y_true, y_pred, model_name):
    """Comprehensive model evaluation with industry-standard metrics"""
    metrics = {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_recall_fscore_support(y_true, y_pred)[0].mean(),
        "Recall": precision_recall_fscore_support(y_true, y_pred)[1].mean(),
        "F1-Score": precision_recall_fscore_support(y_true, y_pred)[2].mean()
    }
    return metrics
```
---

## 📈 Future Roadmap

### Phase 2: Intelligence Enhancement (v2.0) 🔄 **IN PROGRESS**
- ✅ A/B testing framework for model comparison
- ✅ Model fine-tuning and reaching accuracy of +80%
- ✅ Automated hyperparameter optimization
- 🔥 Implementing Topic Modeling
- 🔄 Advanced feature engineering pipelines
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

## 🔗 Resources & Links

- 🌐 **[Live Demo](https://sep-torrens-dr-ranju-group-1.streamlit.app/)**: Interactive application showcase
- 📚 **[Documentation](docs/)**: Comprehensive technical specifications
- 🎥 **[Demo Video](https://youtube.com/demo)**: Walkthrough of key features (in progress)

---

*Built with ❤️ and rigorous engineering principles by the ClinicTrends AI team*

**"Whether it’s concrete or code, structure is everything."**