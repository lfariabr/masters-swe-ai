import streamlit as st
from utils.determinant import determinant, is_square
import time

st.title("🧩 Set 1 – Problem 1: Determinant (Recursive)")

st.markdown("""
M.A.T.E. will help you calculate the **determinant of any n×n matrix**  
using the **Laplace (cofactor) expansion** method — step by step.
""")

rows = st.number_input("Matrix size (n×n):", 2, 5, 3)
matrix = []

for i in range(rows):
    row = st.text_input(f"Row {i+1} (comma separated):", "1,2,3")
    matrix.append([float(x.strip()) for x in row.split(",")])

if st.button("✨ Compute Determinant"):
    st.info("Alright, let’s go step by step...")

    progress = st.progress(0)
    status_text = st.empty()
    for i in range(100):
        progress.progress(i + 1)
        if i == 25:
            status_text.text("🔹 Step 1: Checking if matrix is square...")
            time.sleep(2)
        elif i == 50:
            status_text.text("🔹 Step 2: Applying recursive Laplace expansion...")
            time.sleep(2)
        elif i == 75:
            status_text.text("🔹 Step 3: Simplifying minors and cofactors...")
        time.sleep(0.02)

    if is_square(matrix):
        det_value = determinant(matrix)
        st.success(f"✅ Determinant = {det_value}")
        st.markdown("""
        ---
        **Tutor’s Explanation:**  
        The determinant tells us the *scaling factor* of the transformation described by this matrix.  
        A zero determinant means the matrix squashes space into a lower dimension.
        """)
    else:
        st.error("⛔ Matrix must be square to compute the determinant.")
