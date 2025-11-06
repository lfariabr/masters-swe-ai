# set2Problem1.py
# CLI driver for Set 2 – Problem 1 (definite integral of a general function)

import streamlit as st
from resolvers.integrals import parse_function, integrate
import time

def display_s2p1():
    st.title("📘 Numerical Integration")
    st.caption("Set 2 – Problem 1")
    
    st.markdown("""
    Let’s find the **definite integral** of a function using numerical methods.  
    EigenAI will help you approximate **∫[a to b] f(x)dx** using different techniques.

    > Tip: use Python syntax for the function, example: sin(x) + x**2
    """)
    
    expr = st.text_input("f(x) = ").strip()
    col1, col2 = st.columns(2)
    with col1:
        a_str = st.text_input("Lower bound a =", "0")
    with col2:
        b_str = st.text_input("Upper bound b =", "1")
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        st.warning("Please enter valid numeric bounds for a and b.")
        return

    method = st.selectbox("Method", ["adaptive", "simpson", "trapezoid"])

    n = None
    if method in ("trapezoid", "simpson"):
        try:
            n = int(st.text_input("subintervals n (blank for default) = ").strip() or "0")
            if n <= 0: n = None
        except:
            n = None

    eps = 1e-6
    if method.startswith("adaptive"):
        try:
            eps = float(st.text_input("tolerance eps (default 1e-6) = ").strip() or "1e-6")
        except:
            eps = 1e-6

    if st.button("🟢 Compute Integral"):
        st.info("Starting integration...")
        progress = st.progress(0)
        status_text = st.empty()
        for i in range(100):
            progress.progress(i + 1)
            if i == 25:
                status_text.text("🔹 Step 1: Parsing function expression...")
                time.sleep(1.5)
            elif i == 50:
                status_text.text(f"🔹 Step 2: Subdividing interval into {n} parts...")
                time.sleep(1.5)
            elif i == 75:
                status_text.text(f"🔹 Step 3: Applying {method.replace('_', ' ').title()}...")
                time.sleep(1.5)
            time.sleep(0.01)
        try:
            f = parse_function(expr)
            val, evals, info = integrate(f, a, b, method=method, n=n, eps=eps)
            st.success(f"Result: ∫ f(x) from {a} to {b} = {val:.10f}")
            st.caption(f"Evaluations: {evals} | {info}")
        except Exception as e:
            st.error(f"Error: {e}")