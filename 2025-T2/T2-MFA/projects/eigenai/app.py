import streamlit as st

st.set_page_config(
    page_title="EigenAI MFA501 Smart Tutor",
    page_icon="🎓",
    layout="wide"
)

st.title("Welcome to EigenAI's app")

st.image("assets/eigenAI.png", use_container_width=True)

st.markdown("""
### Your **Mathematical solver** for MFA501  
Built to help Torrens University students master mathematical foundations of AI step by step.

""")

if st.button("⚡ Reveal SuperPowers"):
    st.balloons()
    st.success("Navigate through the sidebar to start your assessment journey 🚀")
    # st.image("assets/intro_bg.png", use_container_width=True)

    st.markdown("""
    #### 👋 What can you do here?
    - Explore recursive determinant and eigenvalue problems interactively  
    - Learn how to think through each computation  
    - Understand mathematical logic behind your code  

    Use the sidebar or bottom navigation to explore:
    1. Set 1 – Problem 1: Determinant  
    2. Set 1 – Problem 2: Eigenvalues/Eigenvectors  
    3. Set 2 – Problem 1: Integration  
    4. Set 2 – Problem 2: RRBF Gradient  
    """)

    st.markdown("---")
