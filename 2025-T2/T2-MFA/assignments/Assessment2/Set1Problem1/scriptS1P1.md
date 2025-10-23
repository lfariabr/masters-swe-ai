# 🎥 VIDEO 1 — Problem 1: Determinant of a Matrix

- Files: determinant.py and set1Problem1.py
- Length: ≤ 5 minutes
- Goal: Show recursive determinant logic and demonstrate a test case.

---

## 🧩 1. INTRO (0:00–0:30)

“Hi, my name is Luis Faria, and this is my demonstration for Assessment 2A – Problem 1.
In this problem, I wrote a Python program to calculate the determinant of a matrix using recursion.
I’ll quickly walk through my code and explain how it works step by step.”

## ⚙️ 2. EXPLAIN determinant.py (0:30–2:30)

Open file and scroll through it while speak.
We'll have something like this:

```python
def determinant(matrix):
    # Base case for 2x2 matrix
    if len(matrix) == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    
    det = 0
    for c in range(len(matrix)):
        minor = [row[:c] + row[c+1:] for row in (matrix[1:])]
        det += ((-1)**c) * matrix[0][c] * determinant(minor)
    return det
```

> “This function is called determinant().
> It receives a matrix represented as a list of lists in Python — for example [[1, 2], [3, 4]].

> The first thing I do is handle the base case, which is when the matrix is 2×2.
> In that case, I just use the standard determinant formula ad - bc.”

Then scroll down and point to the recursive part:

> “If the matrix is larger than 2×2, I start with a variable det = 0.
> Then I loop through each column c in the first row.
> For each column, I use this list comprehension:

```python
minor = [row[:c] + row[c+1:] for row in (matrix[1:])]
```

> That line creates the minor matrix by removing the first row and the current column c.
> Then, I multiply three things together:
1.	`(-1)**c` — the cofactor sign alternates with each column,
2.	`matrix[0][c]` — the element from the first row,
3.	and the `determinant` of the minor — found by calling the same function recursively.”

Show the final line:

> “The total determinant is the sum of all these products.
> This recursive pattern continues until all minors are 2×2 matrices.”

## 🧮 3. OPEN set1Problem1.py (2:30–3:30)

Show driver file — it likely looks like this:

```python
from determinant import determinant

matrix = [
    [6, 1, 1],
    [4, -2, 5],
    [2, 8, 7]
]

print("Matrix:")
for row in matrix:
    print(row)
print("Determinant:", determinant(matrix))
```

> “Here, I import the determinant() function and define a 3×3 matrix.
> I print the matrix to make it clear what’s being calculated, and then I call the function and print the determinant result.”

## 4. RUN THE PROGRAM (3:30–4:30)

Run in terminal:
`python set1Problem1.py`

> “When I run this script, it prints the matrix and then the determinant value.
> For this 3×3 example, the determinant is -306.

> That negative value means the transformation represented by this matrix flips orientation in space — it’s invertible but changes direction.”
> Extra: “If I test another matrix, like [[1,2,3],[4,5,6],[7,8,9]], I’ll get zero as the determinant, which means it’s singular — it can’t be inverted.”

## 🧾 5. WRAP-UP (4:30–5:00)

> “So, in this problem, I implemented a recursive algorithm that calculates determinants for matrices of any size.
> It demonstrates understanding of recursion, matrix minors, and cofactor expansion — which are the foundation for more advanced linear algebra applications used in AI, like solving systems or computing eigenvalues in the next problem.”