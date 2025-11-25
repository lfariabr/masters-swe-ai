import streamlit as st
from resolvers.eigen_solver import eigenpairs
import time

def display_s1p2():
    st.title("🧠 Eigenvalues & Eigenvectors")
    st.caption("Set 1 – Problem 2")

    st.markdown("""
    Let’s find the **eigenvalues (λ)** and **eigenvectors** of your 2×2 matrix.  
    EigenAI will walk you through the **characteristic equation** and the logic step-by-step.
    """)

    matrix = []
    try:
        for i in range(2):
            row = st.text_input(f"Row {i+1} (comma separated):", "2,1" if i == 0 else "1,2")
            parsed_row = [float(x.strip()) for x in row.split(",")]
            if len(parsed_row) != 2:
                st.error(f"❌ Row {i+1} must have exactly 2 values")
                st.warning("⚠️ This tool is optimized for 2×2 matrices. "
                "Larger matrices require iterative algorithms like QR decomposition.")
                st.stop()
            matrix.append(parsed_row)
    except ValueError:
        st.error(f"❌ Invalid input format. Please enter numeric values separated by commas.")
        st.stop()

    if st.button("🟢 Compute Eigenpairs"):
        st.info("Starting eigenvalue analysis...")
        progress = st.progress(0)
        status_text = st.empty()

        for i in range(100):
            progress.progress(i + 1)
            if i == 25:
                status_text.text("🔹 Step 1: Forming (A − λI)")
                time.sleep(2) # 2s to let user see the progress
            elif i == 50:
                status_text.text("🔹 Step 2: Solving det(A − λI) = 0 → characteristic polynomial")
                time.sleep(2) # 2s to let user see the progress
            elif i == 75:
                status_text.text("🔹 Step 3: Finding eigenvectors from (A − λI)x = 0")
                time.sleep(2) # 2s to let user see the progress
            time.sleep(0.02)
            
        try:
            pairs = eigenpairs(matrix)
            st.success("✅ Computation complete!")
            for lam, vec in pairs:
                st.write(f"**λ = {lam}**, Eigenvector → {vec}")

        except ValueError:
            st.error(f"❌ Computation failed")
            st.stop()
                
        st.markdown("""
        ---
        ***EigenAi's Hint: 🧠** 

        Eigenvectors show the *directions* that remain fixed under transformation.  
        Eigenvalues tell how much those directions are *stretched, shrunk, or flipped*.
        """)
