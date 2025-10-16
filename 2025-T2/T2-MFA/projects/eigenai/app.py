import streamlit as st

st.set_page_config(
    page_title="EigenAI Portal",
    layout="centered",
    page_icon="🤖",
    initial_sidebar_state="expanded"
)

from views import home, set1Problem1, set1Problem2, set2Problem1, set2Problem2

# ---- Sidebar Header ----
logo_url = "https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/projects/eigenai/assets/logo2.png?raw=true"
st.sidebar.image(logo_url, use_container_width=True)
st.sidebar.markdown("---")

# ---- Sidebar Menu ----
menu = st.sidebar.radio(
    "📂 Select a screen:", [
    "🌀 Portal",
    "🧩 set1-problem1",
    "🧠 set1-problem2",
    "📘 set2-problem1",
    "📗 set2-problem2",
], index=0)

# ---- View Routing ----
if menu == "🌀 Portal":
    home.display()

if menu == "🧩 set1-problem1":
    set1Problem1.display_s1p1()

if menu == "🧠 set1-problem2":
    set1Problem2.display_s1p2()

if menu == "📘 set2-problem1":
    set2Problem1.display_s2p1()

if menu == "📗 set2-problem2":
    set2Problem2.display_s2p2()

# ---- Footer (Optional) ----
st.sidebar.markdown("---")
st.sidebar.caption("luisfaria.dev")