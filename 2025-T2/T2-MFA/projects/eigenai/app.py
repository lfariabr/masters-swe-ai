import streamlit as st

st.set_page_config(
    page_title="EigenAI Portal",
    layout="centered",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

from views import home, set1Problem1, set1Problem2, set2Problem1, set2Problem2, set3Problem1

# ---- Sidebar Header ----
logo_url = "https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/projects/eigenai/assets/logo2.png?raw=true"
# logo_url = "assets/logo2.png"
st.sidebar.image(logo_url, width="stretch")
st.sidebar.markdown("---")

# ---- Sidebar Menu ----
menu = st.sidebar.radio(
    "📂 Select a screen:", [
    "🌀 Portal",
    
    # Assessment 2A
    "[set1]problem-1",
    "[set1]problem-2",
    
    # Assessment 2B
    "[set2]problem-1",
    "[set2]problem-2",
    
    # Assessment 3
    "ai-problem-set",
], index=0)

# ---- View Routing ----
if menu == "🌀 Portal":
    home.display()

if menu == "[set1]problem-1":
    set1Problem1.display_s1p1()

if menu == "[set1]problem-2":
    set1Problem2.display_s1p2()

if menu == "[set2]problem-1":
    set2Problem1.display_s2p1()

if menu == "[set2]problem-2":
    set2Problem2.display_s2p2()
    
if menu == "ai-problem-set":
    set3Problem1.display_s3p1()

# ---- Footer ----
st.sidebar.markdown("---")
st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/lfariabr)")
st.sidebar.caption("luisfaria.dev")
