Reflective Report 2B, S2-P1
Design and Creative Technologies
Torrens University, Australia


Student: Luis Guilherme de Barros Andrade Faria - A00187785
Subject Code: MFA501
Subject Name: Mathematical Foundations of Artificial Intelligence
Assessment No.: 2B
Title of Assessment: Reflective Report, Set 2, Problem 1
Lecturer: Dr. James Vakilian
Date: Nov 2025


Copyright © 2025 by Luis G B A Faria



Permission is hereby granted to make and distribute verbatim copies of this document provided the copyright notice and this permission notice are preserved on all copies.




Table of Contents
1.	Introduction and Overview	3
2.	Mathematical Approach	5
3.	Programming Methods	6
3.1.	Testing and Results	9
4.	What Went Right	9
5.	What Went Wrong	10
6.	Personal Insight	10
7.	Conclusion	11
8.	References	13














1.	Introduction and Overview
This stage of EigenAI pivots from linear algebra, where we understood how data is arranged, to calculus, the language of change, by analyzing and studying data evolution or improvement, computing gradients, and optimizing loss functions, with the challenge of computing the definite integral of a general real-valued function f(x) on [a, b]. Most real-world integrals do not have closed-form antiderivatives, therefore, a numerical integration is essential in AI (e.g. normalizing constants, area/likelihood approximations, etc). 
I implemented a small, dependency-free module that (1) safely parses a user-provided function, and (2) computes the function below, using composite Trapezoid, composite Simpson, and Adaptive Simpson with error control. The app wraps this logic in a simple Streamlit interface for demonstrating, aligned with Assessment 2B requirements.
 
Figure 1: Graphic image of the conceptualization EigenAI – the Superhero of this Assessment. Image concept built using Gemini 2.5 Flash Image (Nano Banana)
The EigenAI architecture remained consistent with v1.0.0 conceptualization:
•	Frontend / Presentation layer: Streamlit UI for function input, method selection, progress animations, and result display
•	Business logic layer: Pure-Python integration module (`integrals.py`) implementing trapezoid, Simpson, and adaptive Simpson methods
•	Integration: `set2Problem1.py` connects both layers, displaying educational explanations during execution  
 
Figure 2: Sequence diagram illustrating the interaction between `app.py`, sidebar/menu, views, and resolvers/utils modules.
Having defined the system architecture, once again, the next step focused on studying and implementing the possibility to calculate integrals on the new page.
2.	Mathematical Approach

The **Fundamental Theorem of Calculus** states that if F(x) is an antiderivative of f(x), then:

∫[a to b] f(x)dx = F(b) - F(a)

However, many functions don't have closed-form antiderivatives (e.g., e^(-x²), sin(x)/x), requiring **numerical approximation**.

**2.1 Composite Trapezoid Rule**

Approximates the area under f(x) by dividing [a,b] into n subintervals and summing trapezoid areas:

∫[a to b] f(x)dx ≈ (h/2)[f(a) + 2∑f(xᵢ) + f(b)]

where h = (b-a)/n and xᵢ = a + ih.

- **Pros**: Simple, fast (O(n) evaluations)
- **Cons**: Less accurate for highly curved functions (error ~ O(h²))

**2.2 Composite Simpson's Rule**

Uses parabolic interpolation for better accuracy:

∫[a to b] f(x)dx ≈ (h/3)[f(a) + 4∑f(x_odd) + 2∑f(x_even) + f(b)]

where n must be even.

- **Pros**: More accurate for smooth functions (error ~ O(h⁴))
- **Cons**: Requires even n, still struggles with discontinuities

**2.3 Adaptive Simpson**

Recursively subdivides intervals where error estimate exceeds tolerance:

|S_whole - (S_left + S_right)| ≤ 15ε

If error is too large, split [a,b] at midpoint and recurse.

- **Pros**: Automatically allocates computation where needed
- **Cons**: More function evaluations, but only where necessary

**Relevance to AI**

Numerical integration is crucial for:
- **Gradient descent**: Computing loss function improvements
- **Probabilistic models**: Normalizing distributions, computing expectations
- **Reinforcement learning**: Evaluating value functions
- **Neural networks**: Approximating continuous outputs

The adaptive approach mirrors how modern AI systems allocate compute—focusing resources where uncertainty is highest.
3.	Programming Methods
(replace/increment).The determinant logic is implemented in `determinant.py` with the following key functions:
•	`shape(A)` and `is_square(A)` to validate inputs.  
•	`minor_matrix(A, drop_row, drop_col)` to construct sub-matrices.  
•	`determinant(A)` to compute recursively.
These functions were integrated with the Streamlit UI (`set1Problem1.py`) where users enter values row by row.  Upon submission, the system runs the determinant logic, updates a progress bar (`st.progress()`), and displays results with step explanations.
I have also added error handling for the following cases:
•	Non-square matrices,  
•	Empty input fields,  
•	Invalid numeric values.
 
Figure 5: Sequence diagram showing the flow between `views/set2Problem1.py` and `resolvers/integrals.py`. 
This makes the system resilient and user-friendly, essential characteristics for an educational tool.
3.1.	Testing and Results
The implementation was validated against known test cases:
Matrix Size	Test Case	Method	Expected Det	Computed Det	Status
x^2	[0,1]	Simpson	1/3 = 0.333333	0.333333	Pass
sin x	[0, π]	Adaptive Simpson	2	2.000000	Pass
e^x	[0,1]	Adaptive Simpson	e – 1 ≈ 1.7182818	1.718282	Pass
    x		[-1,1]	Trapezoid	1
All test cases passed successfully, confirming the correctness of ? implementation on EigenAi.
4.	What Went Right
It was awesome to simply take advantage of the modular design of EigenAI and implement the new visuals to Presentation layer and Integrals.py to business logic.
The interactive experience letting users input their functions and see the result of each computation through progress bars and animations looks cool and the tool was able to keep transforming abstract calculus into something tangible.
Finally, deploying through Streamlit Cloud proved to be an effective showcase environment with a quick setup, browser-based access, and no dependency issues. This allowed me to focus on code logic and design rather than infrastructure, a valuable lesson in balancing practicality with functionality (replace/increment).
5.	What Went Wrong

The primary challenge was refreshing my understanding of how integrals and derivatives complement each other:
- **Derivative**: Measures instantaneous rate of change (slope)
- **Integral**: Accumulates total change (area under curve)
- **Connection**: They are inverse operations via the Fundamental Theorem of Calculus

**Technical Challenges:**
- **Poorly behaved functions**: Discontinuities or singularities (e.g., 1/x at x=0) caused evaluation errors. Solution: Added input validation and error messages guiding users to avoid problematic intervals
- **Simpson's even-n requirement**: Initially caused confusion when users entered odd n. Solution: Implemented automatic adjustment with clear messaging
- **Adaptive depth limits**: Very oscillatory functions (e.g., sin(100x)) hit max recursion depth. Solution: Added max_depth parameter and informative warning messages
- **Function parsing security**: Initial implementation used unrestricted `eval()`, creating code injection risk. Solution: Implemented restricted namespace allowing only math functions
6.	Personal Insight
Implementing adaptive refinement made the error–work trade-off concrete. It mirrors ML “focus” ideas—allocate compute where the function is complex.
To make things more tangible, I mapped and understood the following sorts of applications to make it easier for me to grasp: (replace/increment).
Concept	Description	Formulas (If Any)	Conceptualization	Real World Application
Integrals				
Derivatives				
Limits				
Eigenvalues				
Eigenvectors				
Matrices				
Determinants				

7.	Conclusion

This project solidified my understanding of numerical integration as a foundational tool in AI and machine learning. By implementing three methods from scratch—trapezoid, Simpson, and adaptive Simpson—I gained practical insight into the **accuracy-efficiency trade-off** that permeates all computational mathematics.

**Key Takeaways:**
1. **Pure implementation matters**: Building without libraries forces deep understanding of algorithmic mechanics
2. **Adaptive methods mirror AI thinking**: Allocating compute where uncertainty is highest is a universal optimization principle
3. **User experience in education**: Interactive tools make abstract math tangible and engaging
4. **Security in parsing**: Safe expression evaluation is critical when accepting user input

**Future Enhancements:**
- Add visualization: Plot f(x) and shade integrated area
- Implement Monte Carlo integration for comparison
- Support multivariable integrals (double/triple integrals)
- Add Gaussian quadrature for higher accuracy
- Integrate with eigenvalue problems (computing matrix functionals)

This project reinforced the link between theoretical calculus and real-world AI systems, where numerical methods enable learning algorithms to function when analytical solutions are unavailable.

 
Statement of Acknowledgment
I acknowledge that I have used the following AI tool(s) in the creation of this report:
•	OpenAI ChatGPT (GPT-5): Used to assist with outlining, refining structure, improving clarity of academic language, and supporting APA 7th referencing conventions.

I confirm that the use of the AI tool has been in accordance with the Torrens University Australia Academic Integrity Policy and TUA, Think and MDS’s Position Paper on the Use of AI. I confirm that the final output is authored by me and represents my own critical thinking, analysis, and synthesis of sources. I take full responsibility for the final content of this report. 
8.	References
Dash, R. B., & Dalai, D. K. (2008). Fundamentals of linear algebra. ProQuest Ebook Central.  
Golub, G. H., & Van Loan, C. F. (2013). Matrix computations (4th ed.). Johns Hopkins University Press.
Goodfellow, I., Bengio, Y., Courville, A., & Bengio, Y. (2016). Deep learning (Vol. 1, No. 2). MIT press.
Lay, D. C., S. R., & McDonald, J.J (2015). Linear algebra and its applications (5th ed.). Pearson.
Strang, G. (2016). Introduction to linear algebra (5th ed.). Wellesley-Cambridge Press.
Streamlit, Inc. (2025). Streamlit documentation. Retrieved from https://docs.streamlit.io/
Torrens University Australia (2025). MFA501 Module notes – linear transformations and matrix operations.
Vakilian, J. (2025). MFA501 Mathematical foundations of artificial intelligence. Torrens University Australia.
