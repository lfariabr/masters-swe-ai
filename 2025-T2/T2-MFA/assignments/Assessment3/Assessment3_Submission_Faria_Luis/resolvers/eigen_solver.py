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

# Step 3: Implement our own sqrt (no math imports)
def my_sqrt(x, tolerance=1e-10, max_iterations=100):
    """
    Newton-Raphson square root approximation.
    Typically converges in 5-6 iterations.
    Max iterations: 100 (prevents infinite loops))
    """
    if x < 0:
        raise ValueError("Cannot compute sqrt of negative number in real domain")
    if x == 0:
        return 0
    
    # Better initial guess
    guess = x / 2 if x >= 1 else x

    for _ in range(max_iterations):
        next_guess = 0.5 * (guess + x / guess)
        if abs(next_guess - guess) < tolerance:
            return next_guess
        guess = next_guess
    # If we get here, means didn't converege, so just return best guess
    return guess

# Step 4: Compute eigenvalues for a 2x2 matrix
def eigenvalues_2x2(A):
    """
    For A = [[a,b],[c,d]]:
    Characteristic polynomial: λ² - (a + d)λ + (ad - bc) = 0
    Solve using quadratic formula.
    """
    if not is_square(A):
        raise ValueError("Matrix must be square")
    
    n, m = shape(A)
    if not (n == m == 2):
        raise ValueError(f"Matrix must be 2x2, got {n}x{m}")
    
    # Validate all elements are numbers
    try:
        a, b = float(A[0][0]), float(A[0][1])
        c, d = float(A[1][0]), float(A[1][1])
    except (ValueError, TypeError, IndexError):
        raise ValueError("Matrix must contain valid numeric values")
    
    tr = a + d                  # trace
    det = a * d - b * c         # determinant
    disc = tr * tr - 4 * det    # discriminant

    if disc < 0:
        raise ValueError(
            f"Complex eigenvalues detected (discriminant={disc:.4f}). "
            "This version only supports real eigenvalues."
        )

    root = my_sqrt(disc)
    λ1 = (tr + root) / 2
    λ2 = (tr - root) / 2
    return [λ1, λ2]

# Step 5: Build (A - λI) and find eigenvectors manually
def subtract_lambda_I(A, lam):
    "Return (A - λI) for a 2x2 matrix"
    return [[A[0][0] - lam, A[0][1]],
            [A[1][0], A[1][1] - lam]]

def eigenvector_for_lambda(A, lam, tolerance=1e-9):
    """
    Solve (A - λI)v = 0 for 2x2 matrix.
    
    Edge cases handled:
    - b ≈ 0: Use alternative formula via c
    - b ≈ 0 and c ≈ 0: Diagonal matrix, return standard basis
    - Near-zero denominators: Use epsilon checks
    """
    a, b = A[0]
    c, d = A[1]

    # Handle different cases
    if abs(b) > tolerance:
        # Standard case: y = -((a-λ)/b)x
        v = [1.0, -((a - lam) / b)]
    elif abs(c) > tolerance:
        # Alternative when b ≈ 0
        v = [-((d - lam) / c), 1.0]
    else:
        # Diagonal matrix case
        v = [1.0, 0.0]
    
    # Normalize to unit vector (L2 norm)
    magnitude = my_sqrt(v[0]**2 + v[1]**2)
    if magnitude > tolerance:
        v = [v[0]/magnitude, v[1]/magnitude]
    
    return v

# Step 6: Combine both into eigenpairs
def eigenpairs(A):
    vals = eigenvalues_2x2(A)
    pairs = []
    for lam in vals:
        v = eigenvector_for_lambda(A, lam)
        pairs.append((lam, v))
    return pairs