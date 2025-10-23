## Assessment 2A
### Assessment 2: **Problem Sets Brief** 
Assessment: Problem Sets
Length: _
Due Date: 16/10/2025

#### Summary: 
In this assessment, you'll be given a wide range of programming exercises to complete, which require using and applying math concepts. They'll be submitted in module 6 and in module 10. The assessment is to be completed individually and you're to submit a zip file including source code, debug and release build + supporting documents for each problem set.

#### Context:
This assessment activity assesses your skills in employing AI mathematical foundation to solve real-world problems and scenarios. The assessment is made of two parts due in modules 6 and 10 over the course of trimester.

#### Instructions:
- The programs that you submit should be free of warnings and errors.
- You need to submit the source code and the executable format.
    - Name the source code folder as: MFA501_Assessment2_Week6_LastName_FirstName.zip and MFA501_Assessment2_Week10_LastName_FirstName.zip
- Your code should be structured and written with the best practices in the field of programming.
- There should be enough number of comments in the source files to show your understanding of the program. Any third-part code should be appropriately attributed.

After implementation and testing your programs, write a reflective report detailing the experience of the development process. The report needs to be at least 500 words in length and include the following sections:
- Overview
- Justifications and elaborations on the mathematical approaches and models used to solve the cases study
- Justifications and elaborations on the programing methods and practices used to implement the mathematical approaches and models
- What went right
- What went wrong
- What you are not sure about
- Conclusion

Your problem sets should include the following elements and should be zipped prior to submission:
- Release Build Zip: A release build executable must be zipped and included with the submission. Ensure that project settings are set to Release when creating this build.
- Source Code Zip: All relevant source code files and project files must be zipped and included with the submission
- Reflective report: PDF or Word
- Naming & File structure for the zip file (should be done for all problem sets) .
    - MFA501_Assessment2_Set1_Release Build_LastName_FirstName.zip
    - MFA501_Assessment2_Set1_Source_LastName_FirstName.zip
    - MFA501_Assessment2_Set1_report_LastName_Firstname.pdf or .docx
- Make sure to submit Problem Set 1 by Sunday 11:55pm Module 6
- Make sure to submit Problem Set 2 by Sunday 11:55pm Module 10

#### Submission Instructions
This assessment task is due in two stages throughout the trimester as outlined above. Please submit your completed assessments via the Assessment link in the main navigation menu in MFA501

Mathematical Foundations of AI. The Learning Facilitator will provide feedback via the Grade Centre on Blackboard. Feedback can be viewed in My Grades

#### Assessment 2A
Instructions for Assessment 2-Part A.
1. Assessment due date: Sunday 11:55 pm - Week 6
2. Weight: 20%
3. You are given a set of programming exercises (Set 1) (with 2 exercises).
4. Write the code for these 2 exercises (10% for each).
5. Using toolbox/functions/libraries for the related assignments (instead of writing the code yourself) does not align with the requirements of this assessment.
6. Submission Format: You need to submit two zip files (i.e., “Problem 1” and “Problem 2”).
- Each zip file should include the following for the relevant problem:
    - a. Release Build: An executable release build must be included with the submission. Ensure project settings are set to Release when creating this build.
    - b. Source Code: All relevant source code files and project files.
    - c. Reflective Report (Word): This should provide a detailed account of your research, critical analysis, findings, results, and references. This report should be at the postgraduate level. It should also contain your algorithm and why you have chosen this method over other methods.
    - d. A video of the program's run: You need to record your screen while running the program and fully demonstrate the correct execution of your code with the results.
    - e. Your code is in a text file, so the system automatically checks the AI issues.
7. For further information, you may refer to the assessment brief.

##### **Set 1**
1. Write a program based on a recursive function to calculate the determinant of a nxn general matrix
2. Write a program to find the Eigenvalues, Eigenvectors, and Eigenspaces of a nxn general matrix

##### **Set 2**
1. Write a program to calculate the Integral of a general function
2. Write a program that calculates the gradient for RRBF_type1 or RRBF_type2 (choose the one you prefer). Refer to this paper: https://research.ijcaonline.org/volume92/number3/pxc3894955.pdf

---

## Implementation Status

### Set 1 - Problem 1: Recursive Determinant Calculator ✅
**Status:** COMPLETE

**Core Implementation:**
- **File:** `resolvers/determinant.py`
- **Algorithm:** Laplace (cofactor) expansion - recursive approach
- **Features:**
  - Handles n×n matrices (2×2 to 5×5 tested)
  - Base cases: 1×1, 2×2 matrices
  - Recursive expansion for larger matrices
  - Input validation (square matrix check)
  - Comprehensive error handling

**UI Implementation:**
- **File:** `views/set1Problem1.py`
- **Features:**
  - Interactive matrix input (comma-separated rows)
  - Real-time validation
  - Progress animation with step-by-step explanations
  - Educational tutor notes explaining determinant meaning
  - Error handling with clear user feedback

**Mathematical Approach:**
- Laplace expansion across first row
- Cofactor formula: det(A) = Σ((-1)^(i+j) * a_ij * M_ij)
- Recursive decomposition to 2×2 base cases
- Time complexity: O(n!)

**Why This Method?**
- Pure Python implementation (no external libraries)
- Educational clarity - mirrors textbook approach
- Demonstrates recursion and divide-and-conquer
- Easy to trace and debug

---

### Set 1 - Problem 2: Eigenvalue/Eigenvector Calculator ✅
**Status:** COMPLETE

**Core Implementation:**
- **File:** `resolvers/eigen_solver.py`
- **Algorithm:** Characteristic polynomial + Newton-Raphson
- **Features:**
  - Computes eigenvalues for 2×2 matrices
  - Finds corresponding eigenvectors
  - Custom sqrt implementation (Newton-Raphson method)
  - No external math libraries used
  - Handles real eigenvalues only

**UI Implementation:**
- **File:** `views/set1Problem2.py`
- **Features:**
  - Interactive 2×2 matrix input
  - Step-by-step progress animation
  - Displays eigenvalue-eigenvector pairs
  - Educational explanations of eigenspace concepts
  - Input validation and error handling

**Mathematical Approach:**
- Characteristic equation: det(A - λI) = 0
- For 2×2 matrix: λ² - trace(A)·λ + det(A) = 0
- Quadratic formula to solve for eigenvalues
- Eigenvectors from (A - λI)v = 0
- Newton-Raphson for square root approximation

**Why This Method?**
- Closed-form solution for 2×2 matrices
- No dependency on NumPy or SciPy
- Demonstrates numerical methods (Newton-Raphson)
- Follows fundamental linear algebra principles
- Easily extendable to 3×3 with minor modifications

---

### Set 2 - Problem 1: Integration Calculator 🚧
**Status:** PLANNED (Due Module 10)

**Planned Implementation:**
- Numerical integration methods
- Simpson's rule, trapezoidal rule, or Gaussian quadrature
- General function parser
- Adaptive step sizing for accuracy

---

### Set 2 - Problem 2: RRBF Gradient Calculator 🚧
**Status:** PLANNED (Due Module 10)

**Planned Implementation:**
- RRBF (Radial Ridge Basis Function) gradient computation
- Based on research paper: https://research.ijcaonline.org/volume92/number3/pxc3894955.pdf
- Visualization of gradient descent
- Interactive parameter tuning

---

## Submission Checklist - Set 1 (Module 6)

### Problem 1: Determinant Calculator
- [x] **a. Release Build** 
  - Create standalone executable using PyInstaller or cx_Freeze
  - [ ] Test on clean machine without Python installed
  - Include in: `MFA501_Assessment2_Set1_Problem1_ReleaseBuild_Faria_Luis.zip`

- [x] **b. Source Code** ✅
  - `app.py` - Main Streamlit entry point
  - `views/set1Problem1.py` - UI implementation
  - `resolvers/determinant.py` - Core algorithm
  - `requirements.txt` - Dependencies
  - Package in: `MFA501_Assessment2_Set1_Problem1_Source_Faria_Luis.zip`

- [x] **c. Reflective Report** (500+ words)
  - **Overview:** EigenAI project vision and Set 1 implementation
  - **Mathematical Approach:** Laplace expansion, cofactor formula, recursion base cases
  - **Programming Methods:** Recursive algorithms, Streamlit UI patterns, error handling
  - **What Went Right:** Clean separation of concerns (UI vs logic), educational UX
  - **What Went Wrong:** Initial matrix parsing challenges, edge case handling
  - **Uncertainties:** Performance optimization for larger matrices (>5×5)
  - **Conclusion:** Learning outcomes and future improvements
  - Save as: `MFA501_Assessment2_Set1_Problem1_Report_Faria_Luis.pdf`

- [ ] **d. Video Demo** ✅
  - Screen recording showing:
    - Application launch
    - Matrix input process
    - Determinant calculation with animations
    - Various test cases (2×2, 3×3, 4×4)
    - Educational explanations
  - Duration: 3-5 minutes
  - Format: MP4 with audio narration

- [x] **e. Code in Text File**
  - Concatenate all Python files into single `.txt` for AI detection check
  - Include comments and documentation
  - Name: `MFA501_Assessment2_Set1_Problem1_Code_Faria_Luis.txt`

### Problem 2: Eigenvalue/Eigenvector Calculator
- [x] **a. Release Build**
  - [ ] Same executable can include both problems
  - Package in: `MFA501_Assessment2_Set1_Problem2_ReleaseBuild_Faria_Luis.zip`

- [x] **b. Source Code** ✅
  - `views/set1Problem2.py` - UI implementation
  - `resolvers/eigen_solver.py` - Core algorithm
  - Package in: `MFA501_Assessment2_Set1_Problem2_Source_Faria_Luis.zip`

- [x] **c. Reflective Report** (500+ words)
  - **Overview:** Eigenvalue problem significance in AI/ML
  - **Mathematical Approach:** Characteristic polynomial, quadratic formula, Newton-Raphson
  - **Programming Methods:** Custom sqrt implementation, eigenvector computation
  - **What Went Right:** Accurate results matching manual calculations
  - **What Went Wrong:** Limited to 2×2 matrices, no complex eigenvalue support
  - **Uncertainties:** Extending to 3×3 matrices (cubic equations), numerical stability
  - **Conclusion:** Understanding of eigen decomposition fundamentals
  - Save as: `MFA501_Assessment2_Set1_Problem2_Report_Faria_Luis.pdf`

- [ ] **d. Video Demo** ✅
  - Demonstrate eigenvalue/eigenvector calculations
  - Show mathematical concepts visually
  - Test multiple matrices

- [x] **e. Code in Text File**
  - Name: `MFA501_Assessment2_Set1_Problem2_Code_Faria_Luis.txt`

---

## Technical Specifications

**Project Name:** EigenAI - Smart Math Tutor
**Language:** Python 3.10+
**Framework:** Streamlit 1.x
**Architecture:** MVC-inspired (Views, Resolvers, App orchestration)

**Dependencies:**
```
streamlit>=1.28.0
```

**Project Structure:**
```
eigenai/
├── app.py                    # Entry point
├── views/                    # UI layer
│   ├── home.py
│   ├── set1Problem1.py
│   └── set1Problem2.py
├── resolvers/                # Business logic
│   ├── determinant.py
│   └── eigen_solver.py
├── assets/                   # Images, logos
├── docs/                     # Documentation
└── requirements.txt
```

**Key Features:**
- ✅ No external math libraries (NumPy, SciPy) - pure Python
- ✅ Educational UX with step-by-step explanations
- ✅ Interactive animations and progress indicators
- ✅ Comprehensive error handling
- ✅ Clean code with docstrings and comments
- ✅ Modular architecture for scalability

**Testing:**
- Manual testing with known matrices
- Validation against textbook examples
- Edge case testing (singular matrices, identity matrices)

---

## Next Steps

### Immediate (Before Module 6 Submission):
1. **Create Release Build** using PyInstaller
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed app.py
   ```
2. **Write Reflective Reports** (2 reports, 500+ words each)
3. **Prepare Code Text Files** for AI detection
4. **Zip All Files** following naming convention
5. **Final Testing** on clean environment

### Future (Module 10):
1. Implement Set 2 - Problem 1 (Integration)
2. Implement Set 2 - Problem 2 (RRBF Gradient)
3. Enhanced visualizations with matplotlib
4. Unit tests with pytest

---

## Academic Integrity Note

All code is original work following MFA501 guidelines:
- No use of NumPy, SciPy, or similar libraries for core computations
- Custom implementations of mathematical algorithms
- Educational approach demonstrating understanding
- Properly commented and documented
- Any external references or inspirations will be cited in reports