import streamlit as st
import sys
import os
from pathlib import Path

# Disable Streamlit's default sidebar navigation
st.set_page_config(
    page_title="ClinicTrends AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

# Import pages
try:
    # Try relative import first
    from views import HomePage, DashboardPage, TranslatePage
except ImportError:
    # Fall back to direct import
    import views.HomePage as HomePage
    import views.DashboardPage as DashboardPage
    import views.TranslatePage as TranslatePage

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
            [" Home", " Dashboard", " Translation"],
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # App info
        st.markdown("""
        **ClinicTrends AI**  
        v1.3.0  
        [GitHub Repo](https://github.com/lfariabr/masters-swe-ai/tree/master/T1-Software-Engineering-Principles/projects)  
        [Documentation](HomePage)
        """)
    
    # Main content based on selection
    if page == " Home":
        HomePage.show_home()
    elif page == " Dashboard":
        DashboardPage.show_dashboard()
    elif page == " Translation":
        TranslatePage.show_translate()

if __name__ == "__main__":
    main()
