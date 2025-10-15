import streamlit as st

def display():
    st.title("You've entered the EigenAI portal")

    image_address = "https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/projects/eigenai/assets/eigenAI-header.png?raw=true"
    st.image(image_address, use_container_width=True)
    st.caption("🤖 EigenAI says: WELCOME TO THE OTHER SIDE, WHERE THE MATHEMATICAL MAGIC BEGINS!")
    
    if st.button("⚡ Reveal SuperPowers"):
        st.balloons()
        
        st.info("""
        👈 **Use the sidebar on your left** to navigate between different sections of the application.

        Choose from **Set 1** or **Set 2** to begin your analysis.
        """)
        st.markdown("---")
        
        st.markdown("### About")
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

        st.markdown("### Mentorship and Guidance")
        st.markdown("""
        This project is proudly mentored by **Dr. James Vakilian**, a distinguished lecturer in Mathematics at Torrens University Australia.

        For more information about Dr. Vakilian's work and contributions, you can visit his [LinkedIn profile](https://www.linkedin.com/in/james-v-70183b28/).
        """)
        st.markdown("---")