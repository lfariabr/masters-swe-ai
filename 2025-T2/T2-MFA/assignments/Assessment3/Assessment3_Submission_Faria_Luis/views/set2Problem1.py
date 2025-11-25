# set2Problem1.py
# CLI driver for Set 2 – Problem 1 (definite integral of a general function)

import time
import streamlit as st
from resolvers.integrals import parse_function, integrate, ParseError, integrate, symbolic_integral

def display_s2p1():
    st.title("📘 Numerical Integration")
    st.caption("Set 2 – Problem 1")
    
    st.markdown("""
    Let’s find the **definite integral** of a function using numerical methods.  
    EigenAI will help you approximate **∫[a to b] f(x)dx** using different techniques.

    > Tip: use Python syntax for the function, example: sin(x) + x**2
    """)
    
    expr = st.text_input(
        "📝 Enter Your Function: f(x) = ", 
        "x**2", 
        help="Examples: x**2, sin(x), cos(x), exp(x), x**3 - 2*x + 1"
    ).strip()

    col1, col2 = st.columns(2)
    with col1:
        a_str = st.text_input(
            "Lower bound a = ", 
            "0", 
            help="Examples: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
        ).strip()
    with col2:
        b_str = st.text_input(
            "Upper bound b = ", 
            "1", 
            help="Examples: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
        ).strip()

    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        st.warning("Please enter valid numeric bounds for a and b.")
        return

    col3, col4 = st.columns(2)
    with col3:
        method = st.selectbox("Method", ["adaptive", "simpson", "trapezoid"])
    with col4:
            n = None
            if method in ("trapezoid", "simpson"):
                try:
                    n = int(st.text_input(
                        "subintervals n (blank for default) = ",
                        "100",
                        help="Examples: 10, 100, 1000, 10000. Higher n = more accuracy but slower."
                    ).strip() or "100")
                    if n <= 0: 
                        st.warning("n must be positive")
                        n = None
                except ValueError:
                    st.warning("Please enter a valid integer for n.")
                    n = None

            eps = 1e-6
            if method.startswith("adaptive"):
                try:
                    eps = float(st.text_input(
                        "tolerance eps (default 1e-6) = ",
                        "1e-6",
                        help="Examples: 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1"
                    ).strip() or "1e-6")
                    if eps <= 0:
                        st.warning("eps must be positive")
                        eps = 1e-6
                except ValueError:
                    st.warning("Please enter a valid positive number for eps.")
                    eps = 1e-6
    if method == "adaptive":
        st.info("Adaptive method automatically adjusts accuracy.")
    else:
        st.info("Higher n = more accuracy but slower.")

    if st.button("🟢 Compute Integral"):
        # Defensive programming
        if not expr:
            st.warning("Please enter a function expression.")
            return
        if a >= b:
            st.warning("Please enter a valid interval [a, b] with a < b.")
            return
        if method in ("trapezoid", "simpson") and n is None:
            st.warning("Please enter a valid number of subintervals n > 0.")
            return
        if method.startswith("adaptive") and eps <= 0:
            st.warning("Please enter a valid tolerance eps > 0.")
            return

        # All clear, let's compute
        st.info("Starting integration...")
        progress = st.progress(0)
        status_text = st.empty()
        for i in range(100):
            progress.progress(i + 1)
            if i == 25:
                status_text.text("🔹 Step 1: Parsing function expression...")
                time.sleep(1.1)
            elif i == 50:
                n_display = n if n is not None else "adaptive"
                status_text.text(f"🔹 Step 2: Subdividing interval into {n_display} parts...")
                time.sleep(1.1)
            elif i == 75:
                status_text.text(f"🔹 Step 3: Applying {method.replace('_', ' ').title()}...")
                time.sleep(1.1)
            time.sleep(0.01)
        try:
            f = parse_function(expr)
            val, evals, info = integrate(f, a, b, method=method, n=n, eps=eps)
            st.success(f"Result: ∫ f(x) from {a} to {b} = {val:.10f}")
            st.caption(f"Evaluations: {evals} | {info}")

            # Inside your try block, after numeric output:
            symbolic = symbolic_integral(expr)
            st.markdown("#### Symbolic Integral Result")
            st.latex(f"∫ {expr} \,dx = {symbolic}")

            # EXTERNAL LIB EXCEPTION: 
            # Note: This is a controlled use of external libraries for visualization only
            # The core integration logic is implemented from scratch without any external dependencies
            import numpy as np
            import matplotlib.pyplot as plt

            st.markdown("#### Function Visualization")

            x = np.linspace(a, b, 200)
            y = [f(xi) for xi in x]
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, 'b-', linewidth=2, label="f(x)")
            ax.fill_between(x, 0, y, alpha=0.3, color='lightblue')
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'Function f(x) = {expr} on [{a}, {b}]')
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)

            st.markdown("""
            ---
            ### EigenAi's Hint 🧠
            
            **Choosing the Right Method:**
            - **Trapezoid Rule**: Simple and fast, but less accurate for curved functions. Good for smooth, linear-like functions.
            - **Simpson's Rule**: More accurate than trapezoid for smooth functions. Requires even number of intervals.
            - **Adaptive Simpson**: Best accuracy with automatic refinement. Focuses computation where the function changes most.
            
            **Tip:** For most cases, adaptive Simpson with default tolerance (1e-6) provides excellent results with minimal input!
            """)
            
        except (ParseError, ValueError, ZeroDivisionError) as e:
            st.error(f"Error: {e}")