import streamlit as st
from resolvers.integration_solver import integrate, compare_methods
import time
import math

def display_s2p1():
    st.title("📘 Numerical Integration")
    st.caption("Set 2 – Problem 1")

    st.info("This section will visualize the numerical integration methods for approximating definite integrals.")
    
    # st.markdown("""
    # Let's calculate the **definite integral** of a function using numerical methods.  
    # EigenAI will help you approximate **∫[a to b] f(x)dx** using different techniques.
    # """)
    
    # # Function input
    # st.subheader("📝 Enter Your Function")
    # function = st.text_input(
    #     "Function f(x):", 
    #     "x**2",
    #     help="Examples: x**2, sin(x), cos(x), exp(x), x**3 - 2*x + 1"
    # )
    
    # # Integration bounds
    # col1, col2 = st.columns(2)
    # with col1:
    #     a = st.number_input("Lower bound (a):", value=0.0, format="%.4f")
    # with col2:
    #     b = st.number_input("Upper bound (b):", value=1.0, format="%.4f")
    
    # # Number of subdivisions
    # n = st.slider("Number of subdivisions (n):", min_value=10, max_value=10000, value=1000, step=10)
    
    # # Method selection
    # method = st.selectbox(
    #     "Integration method:",
    #     [
    #         'simpson',
    #         'trapezoidal', 
    #         'riemann_mid',
    #         'riemann_left',
    #         'riemann_right'
    #     ],
    #     format_func=lambda x: {
    #         'simpson': "Simpson's Rule (Most Accurate)",
    #         'trapezoidal': 'Trapezoidal Rule',
    #         'riemann_mid': 'Riemann Sum (Midpoint)',
    #         'riemann_left': 'Riemann Sum (Left)',
    #         'riemann_right': 'Riemann Sum (Right)'
    #     }[x]
    # )
    
    # # Compute button
    # if st.button("🟢 Compute Integral"):
        
    #     # Input validation
    #     if a >= b:
    #         st.error("❌ Lower bound must be less than upper bound!")
    #         st.stop()
        
    #     st.info("Starting integration...")
    #     progress = st.progress(0)
    #     status_text = st.empty()
        
    #     for i in range(100):
    #         progress.progress(i + 1)
    #         if i == 25:
    #             status_text.text("🔹 Step 1: Parsing function expression...")
    #             time.sleep(1.5)
    #         elif i == 50:
    #             status_text.text(f"🔹 Step 2: Subdividing interval into {n} parts...")
    #             time.sleep(1.5)
    #         elif i == 75:
    #             status_text.text(f"🔹 Step 3: Applying {method.replace('_', ' ').title()}...")
    #             time.sleep(1.5)
    #         time.sleep(0.01)
        
    #     status_text.text("🔹 Step 4: Computing result...")
        
    #     try:
    #         # Compute integral
    #         result = integrate(function, a, b, n, method)
            
    #         st.success(f"✅ Computation complete!")
            
    #         # Display result
    #         st.markdown(f"""
    #         ### Result
    #         ∫[{a} to {b}] ({function}) dx ≈ **{result:.8f}**
            
    #         - Method: {method.replace('_', ' ').title()}
    #         - Subdivisions: {n}
    #         - Width of each subdivision: Δx = {(b-a)/n:.6f}
    #         """)
            
    #         # Show comparison
    #         if st.checkbox("📊 Compare with other methods"):
    #             st.subheader("Method Comparison")
    #             comparison = compare_methods(function, a, b, n)
                
    #             for m, val in comparison.items():
    #                 if isinstance(val, (int, float)):
    #                     st.write(f"**{m.replace('_', ' ').title()}:** {val:.8f}")
    #                 else:
    #                     st.write(f"**{m.replace('_', ' ').title()}:** {val}")
            
    #         # Educational hints
    #         st.markdown("""
    #         ---
    #         **EigenAi's Hint: 🧠**
            
    #         **What's happening here?**
    #         - We're approximating the area under the curve f(x) from a to b
    #         - The interval [a,b] is divided into n equal parts
    #         - Each method uses different sampling points to estimate the area
            
    #         **Method accuracy (best to worst for smooth functions):**
    #         1. **Simpson's Rule** - Uses parabolic approximation (O(1/n⁴) error)
    #         2. **Trapezoidal Rule** - Uses linear approximation (O(1/n²) error)
    #         3. **Riemann Sums** - Uses rectangular approximation (O(1/n) error)
            
    #         **Key insight:** 
    #         Integration is the reverse of differentiation!
    #         - Derivative = instantaneous rate of change
    #         - Integral = accumulated change over an interval
            
    #         **Real-world applications:**
    #         - Area/volume calculations
    #         - Distance from velocity (physics)
    #         - Total cost from marginal cost (economics)
    #         - Probability distributions (statistics)
    #         """)
            
    #     except ValueError as e:
    #         st.error(f"❌ Computation failed: {str(e)}")
    #         st.warning("""
    #         **Common issues:**
    #         - Invalid function syntax (try: x**2 instead of x^2)
    #         - Division by zero in the interval
    #         - Undefined values (like log of negative numbers)
    #         """)
    #         st.stop()
    
    # # Examples section
    # with st.expander("📚 Example Functions to Try"):
    #     st.markdown("""
    #     **Polynomials:**
    #     - `x**2` on [0, 1] → Exact: 1/3 ≈ 0.333333
    #     - `x**3` on [0, 2] → Exact: 4
        
    #     **Trigonometric:**
    #     - `sin(x)` on [0, 3.14159] → Exact: 2
    #     - `cos(x)` on [0, 1.5708] → Exact: 1
        
    #     **Exponential:**
    #     - `exp(x)` on [0, 1] → Exact: e - 1 ≈ 1.718282
    #     - `exp(-x**2)` on [0, 1] → (Gaussian function)
        
    #     **Complex:**
    #     - `x**3 - 2*x + 1` on [0, 2]
    #     - `1/(1 + x**2)` on [0, 1] → Exact: π/4 ≈ 0.785398
    #     - `sqrt(x)` on [0, 4] → Exact: 16/3 ≈ 5.333333
    #     """)