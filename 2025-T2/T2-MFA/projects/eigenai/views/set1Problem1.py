import streamlit as st
from resolvers.determinant import determinant, is_square
import time

def display_s1p1():
    st.title("🧩 Determinant (Recursive)")
    st.caption("Set 1 – Problem 1")

    st.markdown("""
    EigenAI will help you calculate the **determinant of any n×n matrix**  
    using the **Laplace (cofactor) expansion** method — step by step.
    """)

    rows = st.number_input("Matrix size (n×n):", 2, 5, 3)
    matrix = []

    for i in range(rows):
        row = st.text_input(f"Row {i+1} (comma separated):", "1,2,3")
        try:
            parsed_row = [float(x.strip()) for x in row.split(",")]
            if len(parsed_row) != rows:
                st.error(f"❌ Row {i+1} must have exactly {rows} values")
                st.stop()
            matrix.append(parsed_row)
        except ValueError:
            st.error(f"❌ Row {i+1} contains non-numeric values")
            st.stop()

    if st.button("🟢 Compute Determinant"):
        st.info("Alright, let’s go step by step...")

        progress = st.progress(0)
        status_text = st.empty()
        for i in range(100):
            progress.progress(i + 1)
            if i == 25:
                status_text.text("🔹 Step 1: Checking if matrix is square...")
                time.sleep(2) # 2s to let user see the progress
            elif i == 50:
                status_text.text("🔹 Step 2: Applying recursive Laplace expansion...")
                time.sleep(2) # 2s to let user see the progress
            elif i == 75:
                status_text.text("🔹 Step 3: Simplifying minors and cofactors...")
                time.sleep(2) # 2s to let user see the progress
            time.sleep(0.02)

        if is_square(matrix): # used to check if the matrix is square and proceed with determinant calculation
            try:
                det_value = determinant(matrix)
                st.success(f"✅ Determinant = {det_value}")
            except ValueError as e:
                st.error(f"❌ Computation failed: {str(e)}")
                st.stop()
            st.markdown("""
            ---
            EigenAi's Hint 🧠:
            The determinant measures how the matrix transforms space:
            - |det(A)| > 1 → expands area/volume.
            - 0 < |det(A)| < 1 → compresses.
            - det(A) = 0 → flattens space (no inverse possible).

            This recursive approach uses Laplace expansion across the first row,
            calling itself on smaller and smaller minors until reaching 2×2 base cases
            """)
        else:
            st.error("⛔ Matrix must be square to compute the determinant.")
