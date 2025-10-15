"""
# Set 1;
## Problem 2:
Write a program that computes the eigenvalues and eigenvectors 
of a 2x2 matrix without using any external libraries.

Helper:
cd T2-MFA/assignments/Assessment2
python s1p2.py
"""

# Step 1: Represent the matrix using a list of lists
A = [
    [2, 1],
    [1, 2]
]
print(f"Matrix A: {A}")
print("--- end step 1 ---\n")

# Step 2: Tiny helper to check square shape
def shape(A):
    "Return (rows, cols) of matrix A"
    return len(A), (len(A[0]) if A else 0)

def is_square(A):
    "True if A is n x n and all rows have the same length"
    n, m = shape(A)
    if n != m:
        return False
    return all(len(row) == m for row in A)

print(f"Shape of A: {shape(A)}")
print(f"Is A square? {is_square(A)}")
print("--- end step 2 ---\n")

# Step 3: Implement our own sqrt (no math imports)
def my_sqrt(x, tolerance=1e-10):
    "Return square root using Newton–Raphson (no math lib)"
    if x < 0:
        raise ValueError("Cannot compute sqrt of negative number in real domain")
    if x == 0:
        return 0
    guess = x
    while True:
        next_guess = 0.5 * (guess + x / guess)
        if abs(next_guess - guess) < tolerance:
            return next_guess
        guess = next_guess

# Testing the sqrt helper
print(f"√9 = {my_sqrt(9)}")
print("--- end step 3 ---\n")

# Step 4: Compute eigenvalues for a 2x2 matrix
def eigenvalues_2x2(A):
    """
    For A = [[a,b],[c,d]]:
    Characteristic polynomial:
    λ² - (a + d)λ + (ad - bc) = 0
    Solve using quadratic formula.
    """
    n, m = shape(A)
    if not (n == m == 2):
        raise ValueError("Matrix must be 2x2")

    a, b = A[0]
    c, d = A[1]
    tr = a + d                  # trace
    det = a * d - b * c         # determinant
    disc = tr * tr - 4 * det    # discriminant

    if disc < 0:
        raise ValueError("Complex eigenvalues – not supported in this version")

    root = my_sqrt(disc)
    λ1 = (tr + root) / 2
    λ2 = (tr - root) / 2
    return [λ1, λ2]

# Testing eigenvalues
A = [[2, 1],
     [1, 2]]
print(f"Eigenvalues of A: {eigenvalues_2x2(A)}")  # expect [3, 1]
print("--- end step 4 ---\n")

# Step 5: Build (A - λI) and find eigenvectors manually
def subtract_lambda_I(A, lam):
    "Return (A - λI) for a 2x2 matrix"
    return [[A[0][0] - lam, A[0][1]],
            [A[1][0], A[1][1] - lam]]

def eigenvector_for_lambda(A, lam, tolerance=1e-9):
    """
    Solve (A - λI)v = 0.
    For 2x2, only need ratio between x and y:
        (a-λ)x + b y = 0  → y = -((a-λ)/b)x
    """
    a, b = A[0]
    c, d = A[1]
    if abs(b) > tolerance:
        y_over_x = -((a - lam) / b)
        v = [1, y_over_x]
    elif abs(c) > tolerance:
        x_over_y = -((d - lam) / c)
        v = [x_over_y, 1]
    else:
        v = [1, 0]  # fallback
    # Normalize vector for neatness
    mx = max(abs(v[0]), abs(v[1]))
    v = [round(v[0]/mx, 6), round(v[1]/mx, 6)]
    return v

# Step 6: Combine both into eigenpairs
def eigenpairs(A):
    vals = eigenvalues_2x2(A)
    pairs = []
    for lam in vals:
        v = eigenvector_for_lambda(A, lam)
        pairs.append((lam, v))
    return pairs

# Testing final implementation
A = [[2, 1],
     [1, 2]]
for lam, v in eigenpairs(A):
    print(f"λ = {lam},  v = {v}")
print("--- end step 6 ---\n")

# Step 7: More tests
B = [[4, 2],
     [1, 3]]
for lam, v in eigenpairs(B):
    print(f"λ = {lam},  v = {v}")
print("--- end step 7 ---\n")

# Step 8: Extra explanatory note
print("""
Tutor's Note 🧠:
Eigenvalues tell us the **stretching factor** of the transformation.  
Eigenvectors show the **directions** that remain fixed under transformation.  
""")
print("--- end step 8 ---\n")
