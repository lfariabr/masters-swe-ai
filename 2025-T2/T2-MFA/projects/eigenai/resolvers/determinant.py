"""
# Set 1;
## Problem 1:
Write a program based on a recursive function 
to calculate the determinant of a nxn general matrix.

Helper:
cd T2-MFA/assignments/Assessment2
python s1p1.py
"""

# Step 1: Represent the matrix using a list of lists
A = [
    [1, 2, 3],
    [0, 1, 4],
    [5, 6, 0]
]
print(f"Matrix A: {A}")
print("--- end step 1 ---\n")

# Step 2: Tiny helpers
def shape(A):
    "Return (rows, cols) of matrix A."
    return len(A), (len(A[0]) if A else 0)

def is_square(A):
    "True if A is n x n and all rows have the same length."
    n, m = shape(A)
    if n != m:
        return False
    return all(len(row) == m for row in A)

print(f"Shape of A: {shape(A)}")
print(f"Is A square? {is_square(A)}")
print("--- end step 2 ---\n")

# Step 3: Build a minor by removing 1 row and 1 column
def minor_matrix(A, drop_row, drop_col):
    "Return the minor of A by removing row 'drop_row' and column 'drop_col'."
    n = len(A)
    return [
        [A[i][j] for j in range(n) if j != drop_col]
        for i in range(n) if i != drop_row
    ]

# Testing minor extraction
M = minor_matrix(A, 0, 1)  # remove row0, col1 from A
print(f"Minor (drop row 0, col 1): {M}")
print("--- end step 3 ---\n")

# Step 4: Determinant base cases
def determinant(A):
    "Determinant via Laplace expansion (recursive)."
    if not is_square(A):
        raise ValueError("⛔ Determinant is defined only for square matrices.")

    n, _ = shape(A)

    # Base cases
    if n == 0:
        return 1   # det([]) = 1 by convention
    if n == 1:
        return A[0][0]
    if n == 2:
        return A[0][0]*A[1][1] - A[0][1]*A[1][0]

    # Recursive case
    total = 0
    sign = 1  # starts positive for column 0, alternates each step
    for j in range(n):
        a_0j = A[0][j]
        if a_0j != 0:
            M = minor_matrix(A, 0, j)
            sub_det = determinant(M)
            total += sign * a_0j * sub_det
        sign = -sign
    return total

# Testing base cases for validation
print(f"Determinant of [7]: {determinant([[7]])}")                      # expect 7
print(f"Determinant of [[1,2],[3,4]]: {determinant([[1,2],[3,4]])}")    # expect -2
print("--- end step 4 ---\n")

# Step 5: Recursive demonstration with known examples
A = [
    [1, 2, 3],
    [0, 4, 5],
    [1, 0, 6]
]
print(f"Matrix A: {A}")
print(f"det(A) = {determinant(A)}")  # expected: 22

B = [
    [2, 1, 3],
    [1, 0, 2],
    [4, 1, 8]
]
print(f"Matrix B: {B}")
print(f"det(B) = {determinant(B)}")  # expected: -1
print("--- end step 5 ---\n")

# Step 6: Extra explanatory note
print("""
Tutor's Note 🧠:
The determinant measures how the matrix transforms space:
- |det(A)| > 1 → expands area/volume.
- 0 < |det(A)| < 1 → compresses.
- det(A) = 0 → flattens space (no inverse possible).

This recursive approach uses Laplace expansion across the first row,
calling itself on smaller and smaller minors until reaching 2×2 base cases.
""")
print("--- end step 6 ---\n")
