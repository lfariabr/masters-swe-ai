# Exec Project
```
cd T1-Software-Engineering-Principles/projects/clinictrends_ai
source venv/bin/activate
streamlit run app.py
```

# projects version control

## clinictrends_ai

### done
v1.0.0 - app with streamlit + altair + pandas + numpy displaying NPS data - 2025_06_08
v1.1.0 - adds nlp analysis + wordcloud + sentiment analysis - 2025_06_10
v1.2.0 - refactor app.py to use pages
-- uses views and utils folders
--- adds home page with project details
--- adds translation page using deep-translator (learns about Google Translate API)
--- moves biz logic to DashboardPage
-- learns how to translate on gsheets `=GOOGLETRANSLATE(C2;"pt";"en")`
v1.3.0 - deploy project on streamlitcloud + adding Pipeline Transformers from Hugging Face's Library

### in progress
v1.4.0 - explore training TextBlob (Dr. Ranju's suggestion) - WTF...

### backlog
v1.5.0 - try to fine tune transformers


