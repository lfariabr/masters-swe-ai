import streamlit as st
from utils.eigen_solver import eigenpairs
import time

def display_s1p2():
    st.title("🧠 Set 1 – Problem 2: Eigenvalues & Eigenvectors")

    st.markdown("""
    Let’s find the **eigenvalues (λ)** and **eigenvectors** of your 2×2 matrix.  
    M.A.T.E. will walk you through the **characteristic equation** and the logic step-by-step.
    """)

    matrix = []
    for i in range(2):
        row = st.text_input(f"Row {i+1} (comma separated):", "2,1" if i == 0 else "1,2")
        matrix.append([float(x.strip()) for x in row.split(",")])

    if st.button("🧩 Compute Eigenpairs"):
        st.info("Starting eigenvalue analysis...")
        progress = st.progress(0)
        status_text = st.empty()

        for i in range(100):
            progress.progress(i + 1)
            if i == 25:
                status_text.text("🔹 Step 1: Forming (A − λI)")
                time.sleep(2)
            elif i == 50:
                status_text.text("🔹 Step 2: Solving det(A − λI) = 0 → characteristic polynomial")
                time.sleep(2)
            elif i == 75:
                status_text.text("🔹 Step 3: Finding eigenvectors from (A − λI)x = 0")
            time.sleep(0.02)

        pairs = eigenpairs(matrix)

        st.success("✅ Computation complete!")
        for lam, vec in pairs:
            st.write(f"**λ = {lam}**, Eigenvector → {vec}")

        st.markdown("""
        ---
        **Tutor’s Note:**  
        Eigenvectors show the *directions* that remain fixed under transformation.  
        Eigenvalues tell how much those directions are *stretched, shrunk, or flipped*.
        """)
