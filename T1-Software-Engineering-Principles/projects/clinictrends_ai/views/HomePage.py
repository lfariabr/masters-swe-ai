import streamlit as st

def show_home():
    """Show the home page content."""
    st.title("ClinicTrends AI 🔍")
    
    st.markdown("""
    ## We analyze Your Customer Feedback
    
    We help you analyze:
    - customer feedback throughout the period of your survey (can be yearly, monthly, etc.)
    - measure NPS scores showing who are the promoters, passives and detractors
    - gain insights from customer comments and uses NLP to analyze the sentiment of the comments
    """)
    
    st.markdown("### Read About Our Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 📈 NPS Analysis
        - Calculate Net Promoter Score
        - Track trends over time
        - Filter by store and date
        """)
    
    with col2:
        st.markdown("""
        #### 💬 Sentiment Analysis
        - Analyze customer sentiment
        - Visualize sentiment distribution
        - Generate word clouds
        """)
    
    with col3:
        st.markdown("""
        #### 🗣️ Translation
        - Translate customer feedback
        - Support for multiple languages
        - Batch process CSV files
        """)
    
    st.markdown("---")
    st.markdown("### Get Started")
    st.info("""
    👈 **Use the sidebar on your left** to navigate between different sections of the application.

    Choose from **Dashboard** or **Translation** to begin your analysis.
    """)
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    ClinicTrends AI is part of the Masters in Software Engineering with AI program.
    It's designed to help businesses better understand their customer feedback
    and make data-driven decisions to improve customer satisfaction.
    """)
    st.markdown("---")
    st.markdown("### Mentorship and Guidance")
    st.markdown("""
    This project is proudly mentored by **Dr. Ranju Mandal**, a distinguished lecturer in Cybersecurity at Torrens University Australia and a member of the Centre for Artificial Intelligence and Optimisation. With over six years of post-doctoral research experience in Artificial Intelligence and Big Data Analytics, Dr. Mandal brings a wealth of knowledge and expertise to the ClinicTrends AI project.

    His current research focuses on optimizing deep learning models and applying Transformer-based deep network models, particularly in the context of image and video analysis. Dr. Mandal's mentorship has been instrumental in guiding the project's development, ensuring that it aligns with cutting-edge AI methodologies and industry best practices.

    For more information about Dr. Mandal's work and contributions, you can visit his [research profile](https://research.torrens.edu.au/en/persons/ranju-mandal).
    """)
    st.markdown("---")
    st.markdown("### Group Members")
    st.markdown("""
    | Name | Role | Email | GitHub | LinkedIn |
    | --- | --- | --- | --- | --- |
    | Luis  | Software Engineer | luis.faria@torrens.edu.au | [luisfaria](https://github.com/lfariabr) | [luisfaria](https://linkedin.com/in/lfariabr)
    | Chin  | Software Engineer | chin@torrens.edu.au | [luisfaria](https://github.com/lfariabr) | [luisfaria](https://linkedin.com/in/lfariabr)
    | Chau | Software Engineer | chau@torrens.edu.au | [luisfaria](https://github.com/lfariabr) | [luisfaria](https://linkedin.com/in/lfariabr)
    

    """)

# This makes the function available when the module is imported
__all__ = ['show_home']

if __name__ == "__main__":
    show_home()