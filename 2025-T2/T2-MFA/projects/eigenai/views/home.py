import streamlit as st

def display():
    st.title("You've entered the EigenAI portal")

    image_address = "https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/projects/eigenai/assets/eigenAI-header.png?raw=true"
    st.image(image_address, use_container_width=True)
    # st.image("assets/eigenAI-header.png", use_container_width=True)
    # st.caption("🤖 EigenAI says: 'WELCOME TO THE OTHER SIDE, WHERE THE MATHEMATICAL MAGIC BEGINS!'")
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
        👈 **Use the sidebar on your left** to navigate between different sections of the application.

        👇 Read more about the project below.
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

        st.markdown("---")

        st.markdown("### Mentorship and Guidance")
        st.markdown("""
        This project is proudly mentored by **Dr. James Vakilian**, a distinguished lecturer in Mathematics at Torrens University Australia.

        For more information about Dr. Vakilian's work and contributions, you can visit his [LinkedIn profile](https://www.linkedin.com/in/james-v-70183b28/).
        """)
        st.markdown("---")