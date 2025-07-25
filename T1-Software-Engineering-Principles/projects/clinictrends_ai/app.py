import streamlit as st
import sys
import os
from pathlib import Path

# Disable Streamlit's default sidebar navigation
st.set_page_config(
    page_title="ClinicTrends AI",
    page_icon="🤖",
    layout="wide", # centered
    initial_sidebar_state="collapsed"
)

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

# Import pages
try:
    from views import (
        HomePage,
        NPSPage,
        TranslatePage,
        ModelsPage,
        EnhancedModels,
        TopicModelingPage
    )

except ImportError:
    import views.HomePage as HomePage
    import views.NPSPage as NPSPage
    import views.TranslatePage as TranslatePage
    import views.ModelsPage as ModelsPage
    import views.MLExperimentsPage as MLExperimentsPage
    import views.TopicModelingPage as TopicModelingPage

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
            ["About",
             "NPS Analysis",
             "ML Models",
             "Topic Modeling",
             "Translation",
             "ML Experiments 🧪",             
            ],
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # App info
        st.markdown("""
        **ClinicTrends AI**   
        ##### An open source AI-powered tool for analyzing customer feedback and trends.
        - **Version:** 2.7.0
        - **GitHub:** [clinictrends_ai](https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Software-Engineering-Principles/projects/clinictrends_ai)  
        """)
    
    # Main content based on selection
    if page == "About":
        HomePage.show_home()
    elif page == "NPS Analysis":
        NPSPage.show_dashboard()
    elif page == "ML Models":
        ModelsPage.show_models()
    elif page == "ML Experiments 🧪":
        MLExperimentsPage.show_enhanced_models()
    elif page == "Topic Modeling":
        TopicModelingPage.show_topic_modeling()
        
    elif page == "Translation":
        TranslatePage.show_translate()
        
if __name__ == "__main__":
    main()