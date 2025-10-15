import streamlit as st

st.set_page_config(
    page_title="EigenAI",
    layout="centered",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

from views import home, set1Problem1, set1Problem2, set2Problem1, set2Problem2

# st.title("Concierge Tool")
# st.markdown("Use the tool below to update your availability process.")

# ---- Sidebar Header ----
logo_url = "https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/projects/eigenai/assets/logo.jpg?raw=true"
st.sidebar.image(logo_url, use_container_width=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "📂 Select a screen:", [
    "🏠 Home",
    "📅 Set 1 - Problem 1",
    "📅 Set 1 - Problem 2",
    "📅 Set 2 - Problem 1",
    "📅 Set 2 - Problem 2",
], index=0)

# ---- View Routing ----
if menu == "🏠 Home":
    home.display()

if menu == "📅 Set 1 - Problem 1":
    set1Problem1.display_s1p1()

if menu == "📅 Set 1 - Problem 2":
    set1Problem2.display_s1p2()

if menu == "📅 Set 2 - Problem 1":
    set2Problem1.display_s2p1()

if menu == "📅 Set 2 - Problem 2":
    set2Problem2.display_s2p2()

# ---- Footer (Optional) ----
st.sidebar.markdown("---")
st.sidebar.caption("luisfaria.dev")