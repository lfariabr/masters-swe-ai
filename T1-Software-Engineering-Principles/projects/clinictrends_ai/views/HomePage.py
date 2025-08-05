import streamlit as st
from utils.alerts import send_discord_message

def show_home():
    """Show the home page content."""
    st.title("ClinicTrends AI 🔍")
    
    
    st.markdown("""
    ### Analyze your Customer Feedback:
    - Visualize data throughout the period of your survey (can be yearly, monthly, etc.)
    - Measure NPS scores showing who are the Promoters, Passives and Detractors
    - Gain insights from customer comments and analyze the sentiment of the comments
    - Experience the power of Machine Learning models to predict NPS scores and summarize customer feedback
    """)

    st.markdown("### Key Features")
        
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ##### 📈 NPS Analysis
        - Calculate Net Promoter Score
        - Track trends over time
        - Filter by store and date
        """)
    
    with col2:
        st.markdown("""
        ##### 💬 Sentiment Analysis
        - Analyze customer sentiment
        - View sentiment distribution
        - Generate word clouds
        """)
    
    with col3:
        st.markdown("""
        ##### 💥 Topic Modeling
        - Analyze customer feedback
        - Have a taste of BERTopic
        - Visualize topics
        """)
    
    with col4:
        st.markdown("""
        ##### 🗣️ Translation
        - Translate customer feedback
        - Support for multiple languages
        - Batch process CSV files
        """)
    
    st.warning("""
        🚀 **Ready to unlock all features?**  
        Click the button below read more about the Project!
        """)
    if st.button("Click me!", key="unlock_features", help="Click to unlock key features", type="secondary", icon="🧪"):
        st.success("Key features unlocked! 🎉")
        send_discord_message("👀 Button to unlock features has been clicked at home.")
        st.balloons()
        
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
        | Name | Role | Email |
        | --- | --- | --- |
        | Luis Faria | Software Engineer | Luis.Faria@Student.Torrens.edu.au |
        | Chau Luong | Software Engineer | Hai.Luong@Student.Torrens.edu.au |
        
        """)

# This makes the function available when the module is imported
__all__ = ['show_home']

if __name__ == "__main__":
    show_home()