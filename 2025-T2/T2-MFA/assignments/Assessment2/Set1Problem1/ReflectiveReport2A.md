# Reflective Report 2A – Set 1 Problem 1
- **Overview:** EigenAI project vision and Set 1 implementation

The idea of developing **EigenAI** emerged after a discussion with my lecturer, **Dr. James Vakilian**, where it was emphasized that the project should not only perform the requested calculations but also provide an interactive environment allowing any user to input their own matrices and obtain results dynamically.

From that conversation, I envisioned creating a **smart learning assistant** that combines theory and computation — a web application where students can experiment with mathematical operations while visualizing the process through a clear, guided interface.

My approach was to build **EigenAI**, a modular web system where users could input matrices, trigger determinant or eigenvalue computations, and observe step-by-step explanations of the results.  

I chose **Streamlit** for the frontend because of its simplicity and interactive capabilities, allowing rapid UI development integrated with **pure Python** logic on the backend.  

The project follows a **layered architecture**:  
- **Presentation layer:** Streamlit interface (user input, progress animations, and results visualization).  
- **Business logic layer:** Custom Python functions implementing the determinant calculation.  
- **Persistence layer:** Streamlit’s in-memory session state (lightweight storage for user inputs and temporary data).  

This structure reflects the **Software Engineering Principles** I learned in the previous term — separation of concerns, modularity, and maintainability.

> *Figure 1: Sequence diagram illustrating the interaction between* `app.py`, *sidebar/menu, views, and resolvers/utils modules.*

- **Mathematical Approach:** 
The determinant algorithm relies on the **Laplace (cofactor) expansion** and **recursive decomposition**.  
At its core, the determinant expresses how a matrix transforms space — whether it scales, compresses, or collapses it.  
The recursive algorithm expands along the first row of the matrix and repeatedly removes one row and one column to compute the **minor matrices**, alternating signs (+/−) in each recursive call.

The computation stops when it reaches the **base cases**:
- For 1×1 → det = A₀₀  
- For 2×2 → det = (ad − bc)

The final determinant is the cumulative sum of the scaled minors.  
This approach reflects both the **mathematical definition** and a **divide-and-conquer programming pattern**, mirroring how AI systems recursively solve sub-problems in optimization or neural-network computations.

- **Programming Methods:** 
The determinant logic is implemented in `determinant.py` with the following key functions:
- `shape(A)` and `is_square(A)` to validate inputs.  
- `minor_matrix(A, drop_row, drop_col)` to construct sub-matrices.  
- `determinant(A)` to compute recursively.

These functions were integrated with the **Streamlit** UI (`set1Problem1.py`) where users enter values row by row.  
Upon submission, the system runs the determinant logic, updates a **progress bar (`st.progress()`)**, and displays results with step explanations.

> *Figure 2: Sequence diagram showing the flow between* `views/set1Problem1.py` *and* `resolvers/determinant.py` *modules.*

Error handling was added for:
- Non-square matrices,  
- Empty input fields,  
- Invalid numeric values.  

This makes the system resilient and user-friendly — essential characteristics for an educational tool.

- **What Went Right:** 
- Clear separation between **UI** and **logic**, allowing independent testing.  
- **Educational user experience**: users can learn through interaction rather than passive observation.  
- **Streamlit Cloud** provided a lightweight and accessible deployment environment for showcasing both **Set 1** and **Set 2** problems.

- **What Went Wrong:** 
- Initial difficulty parsing comma-separated inputs into matrix lists.  
- Minor bugs appeared with matrices containing negative or floating-point numbers.  
- Recursive stack usage grows quickly for matrices larger than 6×6, limiting performance.  

- **Uncertainties:** 
I am still exploring **performance optimizations** for larger matrices.  
Future versions might introduce **memoization** or transition the logic to **NumPy** (for matrix slicing efficiency) — although for the current assessment, only pure Python was allowed.

- **Personal Insight:**
Initially, the determinant felt like a purely mechanical process.  
However, once I implemented the recursive expansion, its **elegance and structure** became clear — each minor matrix represents a smaller window into the overall geometry of transformation.  

Writing the algorithm manually forced me to **think like the computer** while **reasoning like a mathematician**, bridging intuition and formal logic.  
This was my first time designing a recursive mathematical function for an educational platform, and the sense of seeing it come alive visually through Streamlit was deeply satisfying.

- **Conclusion:** 
This project solidified my understanding of both **recursion** and **matrix algebra** as essential building blocks in Artificial Intelligence.  
It reinforced the link between theoretical math and real-world software design — where algorithms are not just abstract proofs but functional components of intelligent systems.  
In future iterations, I plan to optimize the determinant solver and extend EigenAI with visual graph explanations for matrix transformations.

- **References:**
- Dash, R. B., & Dalai, D. K. (2008). *Fundamentals of Linear Algebra*. ProQuest Ebook Central.  
- Torrens University Australia (2025). *MFA501 Module Notes – Linear Transformations and Matrix Operations*.  
- EigenAI Project (2025). *GitHub Repository: masters-swe-ai/T2-MFA/projects/eigenai*.  