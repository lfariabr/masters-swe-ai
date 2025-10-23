# 🎥 VIDEO 2 — Problem 2: Eigenvalues and Eigenvectors

- **Files:** `eigen_solver.py` and `set1Problem2.py`
- **Length:** ≤ 5 minutes
- **Goal:** Demonstrate how the program calculates eigenvalues and eigenvectors, and explain their meaning.

---

## 🧩 1. INTRO (0:00–0:30)

“Hi, my name is **Luis Faria**, and this is my demonstration for **Assessment 2A – Problem 2**.  
In this task, I created a Python program that calculates the **eigenvalues** and **eigenvectors** of a matrix using NumPy.  
I’ll go through the logic of the function first and then show a practical example using a 2×2 matrix.”

---

## ⚙️ 2. EXPLAIN `eigen_solver.py` (0:30–2:15)

Show and explain:

```python
import numpy as np

def eigen_solver(matrix):
    values, vectors = np.linalg.eig(matrix)
    return values, vectors
```

> “This file defines the function eigen_solver.
> It imports the NumPy library — a powerful tool for numerical and matrix operations in Python.

> Inside the function, I call np.linalg.eig(matrix), which computes both eigenvalues and eigenvectors of any square matrix.

> The function returns two outputs:
1.	values → the eigenvalues, which represent how much a transformation stretches or compresses a vector;
2.	vectors → the eigenvectors, which are the directions that remain unchanged except for scaling.

> If we think of a 2D matrix as transforming a shape, the eigenvectors show the directions that don’t rotate — they only scale.”

⸻

## 🧠 3. BRIEF MATH CONNECTION (2:15–2:45)

> “Mathematically, this comes from the equation A·v = λ·v,
where A is the matrix, v is the eigenvector, and λ (lambda) is the eigenvalue.

> This concept is widely used in AI and data science — for example, in Principal Component Analysis (PCA), which finds dominant directions of variance in data.”

⸻

## 🧮 4. OPEN set1Problem2.py (2:45–3:45)

```python
import numpy as np
from eigen_solver import eigen_solver

matrix = np.array([
    [4, 2],
    [1, 3]
])

values, vectors = eigen_solver(matrix)

print("Matrix:\n", matrix)
print("\nEigenvalues:\n", values)
print("\nEigenvectors:\n", vectors)
```

> “Here, I import the function from eigen_solver.py and create a 2×2 matrix.
I then call the function to get both eigenvalues and eigenvectors, and print the results neatly.

> The chosen matrix isn’t diagonal, so NumPy solves the characteristic equation det(A − λI) = 0 internally — which connects back to what we implemented in Problem 1.”

⸻

## ▶️ 5. RUN THE PROGRAM (3:45–4:30)

Run in terminal:
`python set1Problem2.py`

> “When I run this file, the program displays the matrix, followed by its eigenvalues and eigenvectors.

> For this example, the eigenvalues are roughly 5 and 2, which means one direction scales by 5 and another by 2.
The eigenvectors below correspond to these values — they define the stable directions that remain proportional when the transformation is applied.

> If I test a diagonal matrix like [[2, 0], [0, 3]], the eigenvalues are simply [2, 3], and the eigenvectors form an identity matrix — meaning the transformation scales directly along each axis.”

⸻

## 🧾 6. WRAP-UP (4:30–5:00)

> “To wrap up, this program demonstrates how to use NumPy’s linalg.eig to compute eigenvalues and eigenvectors of any square matrix.
It builds directly on Problem 1’s foundation — determinants and the characteristic equation — and connects to real-world applications in AI, such as feature extraction and data compression in PCA.

> Thanks for watching!”