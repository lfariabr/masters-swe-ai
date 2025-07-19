# AWS Solutions Architect Forage Challenge

## 🔧 Work in Progress

```bash
cd T1-Extra/aws
```
---

## 📈 Roadmap

### Task 1: Web Application Hosting 🔥 **IN PROGRESS**
- [X] Cross check ArchitectureDiagram.png with the task document (**Luis**)
- [X] Review AWS service descriptions in the task document
- [X] Analyze the client scenario and requirements
- [X] Write a summary of the client scenario to match understanding or even writing a debriefing context (**Luis**)
> "The client represents a brand that is growing consistently and is having some problems with the high demand: slow website during peak periods and server crashes due to memory overflow. The client is also experiencing some downtime during deployments and doesn't have a disaster recovery plan. 
We need to sedign an architecture that addresses these issues for their application which is a SPA React Application backed by Python and Flask, with PostgreSQL as a database. It all runs off a single AWS EC2 instance currently (t3.medium, 4GB of RAM)."
- [X] Draw a draft for the task thought process (**Luis**)
- [X] Draft the email to Lilly, including:
  - [X] Architecture diagram reference
  - [X] Explanation of each AWS component
  - [X] Rationale for service choices
  - [X] Addressing client pain points (scalability, downtime, etc.)
- [X] Verify that the architecture diagram and the drafted solution are fully aligned
- [ ] Proofread and finalize the email draft

### Task 2: Lorem Ipsum dolor sit amet (v2.0) ✅ **COMPLETE**
- ✅ Provides sample csv files for enhanced UX
- 🔥 Implementing Topic Modeling
- 🔄 Advanced feature engineering pipelines

### Task 3: Lorem Ipsum dolor sit amet (v3.0) 📋 **PLANNED**
- 📋 RESTful API development

### Task 4: Lorem Ipsum dolor sit amet (v4.0) 🚀 **FUTURE**
- 🚀 GPT-powered natural language insights

---

## ✅ Feature Progress

### ✔ Done
**v1.0 breakdown**
#### 🔹 v1.0.0 - `feature/base`
- Streamlit app with Altair, pandas, numpy displaying NPS data

---

### 🔧 In Progress
### 🗂️ Backlog

#### 🔸 v2.8.0 - `feature/topic-modeling`
- current pipeline: Data ➔ Preprocessing ➔ Sentiment Analysis ➔ Performance Metrics
- suggested pipeline: Data ➔ Preprocessing ➔ Sentiment Analysis ➔ Topic Modeling ➔ Insights ➔ Business Actions
- Study BERTopic (BERT + clustering), Sci-kit Learn (LDA, NMF, LSA) and Gensim (LDA, LSI)
- Read the links Dr. Ranju shared. BERTopic is one of the best modern tools for topic modeling:
  - Handles short texts better than LDA
  - Uses embeddings (e.g. BERT) for semantically richer clusters
  - Generates interpretable topic names.
  - Useful Links:
    - https://www.linkedin.com/pulse/topic-modeling-uncovering-hidden-themes-text-mohamed-chizari-y1w2e/
    - https://wellsr.com/python/topic-modeling-with-bert-using-python-bertopic-library/?utm_source=chatgpt.com
    - https://www.datacamp.com/tutorial/what-is-topic-modeling?utm_source=chatgpt.com
    - https://hackernoon.com/nlp-tutorial-topic-modeling-in-python-with-bertopic-372w35l9
- Integrate BERTopic into Pipeline
- Map Topics → Business Recommendations. E.g.:
  - “Topic: Delivery delays” → “Improve logistics or communication”
  - “Topic: Website issues” → “Prioritize website performance improvements”
- Cross-Check with Literature
  - Look for papers or blog posts analyzing your dataset. 
  - Dr. Ranju suggests referencing prior works rather than repeating experiments unnecessarily.

---

> “Whether it’s concrete or code, structure is everything.”