import streamlit as st

def display():
    st.title("You've entered the EigenAI portal")

    image_address = "https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/projects/eigenai/assets/eigenAI-header.png?raw=true"
    # image_address = "assets/eigenAI-header.png"
    st.image(image_address, width="stretch")
    st.markdown(
    """
    <div style="
        background-color:#1E1E1E;
        border-left: 5px solid #00FFFF;
        padding: 1rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-radius: 8px;
    ">
    <p style="font-size: 1.1rem; color:#E0E0E0; font-style: italic;">
    🤖 <b>EigenAI says:</b><br>
    “Welcome to the other side, where the mathematical magic begins.”
    </p>
    </div>
    """,
    unsafe_allow_html=True
    )
    
    if st.button("⚡ Reveal SuperPowers"):
        st.balloons()
        
        st.info("""
        👈 **Use the sidebar on your left** to navigate between sections of the application.
        
        👇 or **Read More** about the project below.
        """)
        st.markdown("---")
        
        st.markdown("### Key Features")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            with st.container(border=True):
                st.markdown("# 🧩")
                st.markdown("###### Set1Problem1")
                st.markdown("Calculate determinants recursively")

        with col2:
            with st.container(border=True):
                st.markdown("# 🧠")
                st.markdown("###### Set1Problem2")
                st.markdown("Computes eigenvalues and eigenvectors")

        with col3:
            with st.container(border=True):
                st.markdown("# 📘")
                st.markdown("###### Set2Problem1")
                st.markdown("Integration Concepts - To be Done")

        with col4:
            with st.container(border=True):
                st.markdown("# 📗")
                st.markdown("###### Set2Problem2")
                st.markdown("RRBF Gradient Calculator - To be Done")
        
        with st.container(border=True):
            st.markdown("# 🎓")
            st.markdown("###### AI Problem Set")
            st.markdown("My implementation of an AI algorithm to reconstruct a binary image from a 2D array representation using advanced reconstruction techniques.")

        st.markdown("---")

        st.markdown("### Mentorship and Guidance")
        st.markdown("""
        This project is proudly mentored by **Dr. James Vakilian**, a distinguished lecturer in Mathematics at Torrens University Australia.

        For more information about Dr. Vakilian's work and contributions, you can visit his [Dr. Vakilian's Profile](https://www.linkedin.com/in/james-v-70183b28/).
        """)
        st.markdown("---")

        st.markdown("""
        EigenAI is a project part of the Masters' in Software Engineering and Artificial Intelligence at Torres University;
        
        Designed to help students better understand math concepts teached at the Core Subject *Mathematical Foundations of Artificial Intelligence*.
        """)
        
        st.markdown("[![Torrens University](https://img.shields.io/badge/Torrens-%23eb5f24.svg?&style=for-the-badge&logo=Torrens-University-Australia&logoColor=white)](https://www.torrens.edu.au/courses/technology/master-of-software-engineering-artificial-intelligence-advanced)")

        st.markdown("---")
        st.markdown("""
        *Built with ❤️ and rigorous engineering principles by EigenAI team*

        **"Whether it’s concrete or code, structure is everything."**
        """)