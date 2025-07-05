import streamlit as st
import sys
import os
from pathlib import Path

# Disable Streamlit's default sidebar navigation
st.set_page_config(
    page_title="ClinicTrends AI",
    page_icon="🤖",
    layout="wide", # centered
    initial_sidebar_state="expanded"
)

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

# Import pages
try:
    from views import (
        HomePage,
        NPSPage,
        TranslatePage,
        TrainingPage,
        TrainingPage2,
        TrainingPage3,
        TrainingPage4,
        ModelsPage
    )

except ImportError:
    import views.HomePage as HomePage
    import views.NPSPage as NPSPage
    import views.TranslatePage as TranslatePage
    import views.TrainingPage as TrainingPage
    import views.TrainingPage2 as TrainingPage2
    import views.TrainingPage3 as TrainingPage3
    import views.TrainingPage4 as TrainingPage4
    import views.ModelsPage as ModelsPage

def main():
    # Sidebar with logo and navigation - this will be our only sidebar
    with st.sidebar:
        # Logo and title
        try:
            logo_path = Path(__file__).parent / "public" / "clinictrends_logo_200x200.svg"
            logo = str(logo_path) if logo_path.exists() else None
        except Exception as e:
            st.warning(f"Could not load logo: {e}")
            logo = None 
        
        if logo:
            st.image(logo, width=200)
        
        st.markdown("---")
        
        # Navigation menu
        st.markdown("### Navigation")
        
        # Page selection
        page = st.radio(
            "",
            ["Home",
             "NPS Analysis",
             "ML Model Comparison",

             # Training
             # "Training - CM1", # TfidfVectorizer + LogisticRegression @ 'Comment' column.
             # "Training - CM2", # TfidfVectorizer + LogisticRegression @ 'CommentScore' column.
             # "Training - CM3", # TfidfVectorizer + LogisticRegression @ 'Comment' column + Hugging Face Transformers.
             # "Training - CM4", # TfidfVectorizer + LogisticRegression @ 'CommentScore' column + Hugging Face Transformers.

             # Additional
             "Translation",
            ],
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # App info
        st.markdown("""
        **ClinicTrends AI**   
        ##### An open source AI-powered tool for analyzing customer feedback and trends.
        - **Version:** 2.1.0
        - **GitHub:** [clinictrends_ai](https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Software-Engineering-Principles/projects/clinictrends_ai)  
        """)
    
    # Main content based on selection
    if page == "Home":
        HomePage.show_home()
    elif page == "NPS Analysis":
        NPSPage.show_dashboard()
    elif page == "ML Model Comparison":
        ModelsPage.show_models()


    elif page == "Training - CM1":
        TrainingPage.show_training()
    elif page == "Training - CM2":
        TrainingPage2.show_training2()
    elif page == "Training - CM3":
        TrainingPage3.show_training3()
    elif page == "Training - CM4":
        TrainingPage4.show_training4()
    
    elif page == "Translation":
        TranslatePage.show_translate()
        
if __name__ == "__main__":
    main()
