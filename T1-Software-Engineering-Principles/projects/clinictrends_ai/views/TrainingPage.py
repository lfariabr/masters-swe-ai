import streamlit as st
from pathlib import Path
import sys
import altair as alt
import pandas as pd
import sklearn
from sklearn.metrics import classification_report

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))
from utils.nlp_analysis import annotate_sentiments

def show_training():
    """Show the training page content."""
    st.title("Training Page")
    st.write("This is the training page.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)  # use your actual file path
        df = df.dropna(subset=["Comment"])
        
        st.write('Data preview')
        st.write(df)

        st.write("---")

        df = annotate_sentiments(df)

        st.write('Data preview with NLP')
        st.write(df)

        st.write("---")
        st.write("Vectorizing data")
        from sklearn.feature_extraction.text import TfidfVectorizer

        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        X = vectorizer.fit_transform(df["Comment"])
        y = df["Sentiment"]

        st.write("Vectorized data")

        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        st.write("Model trained")

        st.write("Model accuracy")
        st.write(model.score(X_test, y_test))

        from sklearn.metrics import classification_report

        y_pred = model.predict(X_test)
        st.write(classification_report(y_test, y_pred))
    
if __name__ == "__main__":
    show_training()