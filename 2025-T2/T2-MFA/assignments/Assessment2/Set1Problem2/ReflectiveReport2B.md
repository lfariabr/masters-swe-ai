# Reflective Report 2B – Set 1 Problem 2
- **Overview**: EigenAI project vision and Set 2 implementation    
The second component of EigenAI focused on computing **eigenvalues** and **eigenvectors** for a 2×2 matrix **without using external libraries**.  
After finishing the determinant recursion logic, I wanted to extend the same clarity and interactivity to another essential linear-algebra concept.  
Following discussions with **Dr. James Vakilian**, I structured this challenge not only to produce correct eigenpairs but also to **teach the underlying steps** interactively through EigenAI’s Streamlit interface.

The **EigenAI architecture** remained consistent with Set 1 Problem 1:
- **Frontend / Presentation layer:** Streamlit UI for matrix input, progress animations, and result display.  
- **Logic layer:** Pure-Python solver (`eigen_solver.py`) implementing characteristic-polynomial computation and vector derivation.  
- **Integration:** `set1Problem2.py` connects both layers, displaying tutor-style explanations during execution.  

> *Figure 1: Sequence diagram showing interaction between* `app.py`, `views/set1Problem2.py`, *and* `utils/eigen_solver.py`.

---

- **Mathematical Approach**
The algorithm is grounded in the **characteristic equation** of a 2×2 matrix A = [[a,b],[c,d]]:
\[\det(A − λI) = λ² − (a + d)λ + (ad − bc) = 0\]
Solving this quadratic yields the **eigenvalues (λ₁, λ₂)**.  
Each eigenvector v satisfies \((A − λI)v = 0\), which provides the direction that remains unchanged by the transformation.

The program solves these steps explicitly:
1. Compute **trace (t = a + d)** and **determinant (Δ = ad − bc)**.  
2. Derive **discriminant (t² − 4Δ)**.  
3. Apply a manual **Newton–Raphson square-root** (`my_sqrt`) to avoid math-library dependencies.  
4. Substitute results in the quadratic formula to find both λ values.  
5. For each λ, compute the corresponding eigenvector ratio (e.g., \(y = −((a − λ)/b)x\)).  

This procedure demonstrates mastery of both the **algebraic definition** and the **computational flow** underlying eigen decomposition.

---

- **Programming Methods**
`eigen_solver.py` was developed using the same step-by-step documentation style as `determinant.py`, ensuring readability and instructional value.  
Key functions include:
- `my_sqrt(x)` – Newton–Raphson approximation.  
- `eigenvalues_2x2(A)` – computes λ₁, λ₂.  
- `eigenvector_for_lambda(A, λ)` – solves (A − λI)v = 0 and normalizes v.  
- `eigenpairs(A)` – combines results into (λ, v) tuples.

`set1Problem2.py` integrates this logic into EigenAI’s UI.  
Users input a 2×2 matrix, click **“Compute Eigenpairs”**, and the tutor walks them through three animated steps:
1. Forming (A − λI)  
2. Solving det(A − λI) = 0  
3. Computing eigenvectors  

This aligns with **pedagogical UX principles**, making abstract math transparent and engaging.

> *Figure 2: Sequence diagram illustrating user input, progress bar animation, and eigenpair resolution flow.*

---

- **What Went Right**
- **Consistent modularity** between determinant and eigen modules allowed quick integration.  
- **Manual sqrt implementation** improved understanding of numerical methods.  
- **Tutor-style UI** successfully presented intermediate symbolic steps, supporting learners visually.  
- Maintained **separation of concerns**, simplifying debugging and testing.

---

- **What Went Wrong**
- Early confusion over handling cases where b = 0 or c = 0 (required conditional vector logic).  
- Minor rounding inconsistencies when normalizing eigenvectors.  
- Attempting to generalize to 3×3 matrices exposed the quadratic-formula limitation.

---

- **Uncertainties**
Performance was never the issue here; rather, the uncertainty lies in **extending symbolic solvers** to higher-dimensional cases.  
Future exploration could involve iterative eigenvalue methods such as **Power Iteration** or integrating **NumPy** once external-library use becomes permissible.

---

- **Personal Insight**
Before this project, eigenvalues and eigenvectors felt abstract — I understood their definition but not their behaviour.  
Implementing the solver revealed their **geometric meaning**: certain directions in space remain fixed, merely scaled by λ.  
Developing `my_sqrt` and manually solving quadratic equations gave me a deeper appreciation for how **core AI libraries perform matrix decompositions under the hood**.  
The experience mirrored the principle behind machine learning itself — breaking complexity into small, learnable steps.  
Seeing the Streamlit progress bar narrate each phase felt like bridging the gap between **mathematics, computation, and pedagogy**.

---

- **Conclusion**
Set 1 Problem 2 strengthened my mathematical intuition and numerical reasoning.  
I learned to treat equations not as symbols to memorize but as algorithms to implement.  
This approach is fundamental to AI engineering, where linear algebra underpins models like **PCA**, **SVD**, and **neural-network weight transformations**.  
The EigenAI project thus serves both as a personal milestone and as a reusable educational framework for future MFA501 students.

---

- **References**
- Dash, R. B., & Dalai, D. K. (2008). *Fundamentals of Linear Algebra.* ProQuest Ebook Central.  
- Torrens University Australia (2025). *MFA501 Module Notes – Eigenvalues and Linear Transformations.*  
- EigenAI Project (2025). *GitHub Repository: masters-swe-ai/T2-MFA/projects/eigenai.*  