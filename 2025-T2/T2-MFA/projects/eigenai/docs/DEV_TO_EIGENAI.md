---
title: "Building EigenAI: Teaching Math Foundations of AI Through Interactive Code"
published: true
description: "An interactive Streamlit app teaching linear algebra, calculus, and optimization algorithms for AI education through hands-on Python implementations"
tags: machinelearning, python, streamlit, ai
cover_image: https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/projects/eigenai/assets/eigenAI-header.png?raw=true
---

# Building EigenAI: Teaching Math Foundations of AI Through Interactive Code

**From determinants to hill climbing algorithms—how I turned academic math into an interactive learning platform.**

> *"Whether it's concrete or code, structure is everything."*

---

## 🎓 The Challenge: Making Math "Click"

As a self-taught software engineer transitioning from 10+ years in project management, I enrolled in **MFA501 – Mathematical Foundations of Artificial Intelligence** at Torrens University Australia under [Dr. James Vakilian](https://au.linkedin.com/in/james-v-70183b28). The subject covered everything from linear algebra to optimization algorithms—the mathematical backbone of modern AI applications in:

- **Machine Learning** (model training, optimization)
- **Natural Language Processing** (text embeddings, transformations)
- **Computer Vision** (image processing, feature extraction)
- **Speech Recognition** (signal processing, pattern matching)

But here's the problem: **abstract math doesn't stick unless you build something with it.**

So instead of just solving problems on paper, I built **[EigenAI](https://eigen-ai.streamlit.app/)** — an interactive Streamlit app that teaches mathematical concepts through live computation, step-by-step explanations, and real-time visualizations.

> **Can we make eigenvalues, gradients, and hill climbing algorithms as intuitive as playing with Legos?**

![Lego Wallpaper](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nzx8b9m0691khi325dlo.png)

That question drove the entire project.

---

## 🤖 What Is EigenAI?

![EigenAI taking a coffee getting ready to teach](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kit7ysi5jp0fjo7uy72g.png)

**EigenAI** (playing on "eigenvalues" and "AI foundations") is a web-based educational platform that implements core mathematical concepts from AI foundations. It's structured around **four assessments** that progressively build complexity, with the app implementing the three case study assessments (2A, 2B, 3):

### **The 12-Week Journey**

The subject covered 12 progressive modules:

| Week | Topic | Overview |
|------|-------|----------|
| Weeks 1-5 | Linear Algebra Foundations | Sets, vectors, matrices, transformations, eigenvalues |
| Weeks 6-9 | Calculus & Optimization | Derivatives, integrals, hill climbing, simulated annealing, genetic algorithms |
| Weeks 10-12 | Probability, Statistics & Logic | Foundations for AI reasoning and decision-making |

> ***Note: Module 6 taught by [Dr. Niusha Shafiabady](https://www.niushashafiabady.com/)***

---

### **Assessment 1: Linear Algebra Fundamentals** *(Online Quiz)*
- ✅ Matrix operations (addition, multiplication, transpose)  
- ✅ Vector operations (magnitude, unit vectors, dot product, cross product)  
- ✅ Systems of equations (elimination, Gaussian elimination)  
- ✅ Linear transformations (stretching, reflection, projection)  

**The Challenge:** 60-minute timed quiz covering Modules 1-2 foundational concepts—no coding, pure mathematical understanding.

**Why It Matters:** These fundamentals are the building blocks for understanding how data flows through neural networks and ML algorithms.

> *Note: Assessment 1 was a quiz-only assessment. The EigenAI app implements the three case study assessments (2A, 2B, 3) that required coding solutions.*

---

### **Assessment 2A: Determinants & Eigenvalues** *(Case Study)*
- ✅ Recursive determinant calculation for n×n matrices  
- ✅ Eigenvalue and eigenvector computation (2×2 matrices)  
- ✅ Step-by-step mathematical notation using SymPy  
- ✅ Input validation and error handling  

**The Challenge:** Implement cofactor expansion from scratch—no NumPy allowed for core logic, only pure Python.

**Why It Matters:** Eigenvalues and eigenvectors are the foundation of:
- **PCA (Principal Component Analysis)** — dimensionality reduction for large datasets
- **Eigenfaces** — facial recognition algorithms
- **Feature compression** — reducing computational cost in ML models

Understanding determinants reveals why singular matrices break these algorithms.

---

### **Assessment 2B: Calculus & Neural Networks** *(Case Study)*
- ✅ Numerical integration (Trapezoid, Simpson's Rule, Adaptive Simpson)  
- ✅ RRBF (Recurrent Radial Basis Function) gradient computation  
- ✅ Manual backpropagation without TensorFlow/PyTorch  
- ✅ Comparative analysis of integration methods with error bounds  

**The Challenge:** Compute gradients by hand for a recurrent network—feel the chain rule in your bones.

**Why It Matters:** Before using `model.fit()`, you should understand what `.backward()` actually does.

---

### **Assessment 3: AI Optimization Algorithms** *(Case Study)*
- ✅ Hill Climbing algorithm for binary image reconstruction  
- ✅ Stochastic sampling variant (speed vs. accuracy trade-off)  
- ✅ Pattern complexity selector (simple vs. complex cost landscapes)  
- ✅ Real-time cost progression visualization  

**The Challenge:** Reconstruct a 10×10 binary image from random noise using only local search—no global optimization, no backtracking.

**Why It Matters:** Hill climbing is the foundation of gradient descent, simulated annealing, and evolutionary algorithms. If you understand local optima here, you understand why neural networks get stuck.

> **💡 Key Insight from Module 6 ([Dr. Niusha Shafiabady](https://www.niushashafiabady.com/)):**
> 
> Hill climbing can get stuck in local optima with no guarantee of finding the global optimum. The cure?
> - **Random restarts** (try multiple starting points)
> - **Random mutations** (introduce noise)
> - **Probabilistic acceptance** (simulated annealing)
> 
> This limitation explains why modern AI uses ensemble methods and stochastic optimization.

---

## 🗓️ Project Timeline & Results

| Month | Assessment | Status |
|-------|------------|--------|
| October 2025 | Linear Algebra Quiz | **72.5% (C)** |
| October 2025 | Determinants & Eigenvalues | **82% (D)** |
| November 2025 | Integrals & RRBF | **84% (D)** |
| December 2025 | Hill Climbing | Awaiting results

**Total Duration:** 12 weeks of intensive mathematical foundations for AI

---

## 🏗️ Technical Architecture

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Streamlit | Interactive UI with zero JavaScript |
| **Core Logic** | Pure Python 3.10+ | Type-hinted, no NumPy in algorithms |
| **Math Rendering** | SymPy + matplotlib | LaTeX-quality equations |
| **Deployment** | Streamlit Cloud | One-click deploy from GitHub |
| **Version Control** | Git + GitHub | Full project history since commit 1 |

### **Why Pure Python for Core Logic?**

The assessment required implementing algorithms **without numerical libraries** to demonstrate understanding of the underlying math. This constraint forced me to:

- Write cofactor expansion from scratch (not just `np.linalg.det()`)
- Implement Simpson's Rule manually (not just `scipy.integrate.quad()`)
- Build hill climbing with custom neighbor generation (not just `scipy.optimize.minimize()`)

**Result:** Deep understanding of how these algorithms actually work under the hood.

---

## 🗝️ Key Features & Lessons Learned

### **1. Modular Architecture That Scales**

```
eigenai/
├── app.py                    # Main Streamlit entry point
├── views/                    # UI components (one per assessment)
│   ├── set1Problem1.py      # Determinants UI
│   ├── set1Problem2.py      # Eigenvalues UI
│   ├── set2Problem1.py      # Integration UI
│   ├── set2Problem2.py      # RRBF UI
│   └── set3Problem1.py      # Hill Climbing UI
└── resolvers/                # Pure Python algorithms
    ├── determinant.py
    ├── eigen_solver.py
    ├── integrals.py
    ├── rrbf.py
    ├── hill_climber.py
    └── constructor.py
```

**Lesson Learned:** Separating algorithm logic from UI made testing 10x easier. When debugging the cost function, the UI stayed unchanged. When improving visualizations, the core math stayed untouched.

**Iterative Development:** EigenAI evolved through 23+ versions:

| Version | Milestone |
|---------|----------|
| v0.0.1 | Streamlit setup, assets, pages |
| v0.1.0 | ✅ Assessment 2A submission |
| v0.1.8 | Added Hill Climbing Binary Image Reconstruction |
| v0.2.0 | ✅ Assessment 2B submission (Integration + RRBF) |
| v0.2.4 | Added stochastic sampling to Hill Climber |
| v0.2.6 | Added complex pattern selector |
| v0.3.0 | ✅ Assessment 3 submission (Hill Climbing Algorithm) |

> Each assessment pushed the app forward—turning coursework into production-ready features. Detailed [`CHANGELOG.md`](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/projects/eigenai/docs/changelog.md)

---

### **2. Hill Climbing: When "Good Enough" Is Good Enough**

The most fascinating part was implementing **Hill Climbing** for image reconstruction:

**The Problem:**
- Start with a random 10×10 binary image (noise)
- Target: A circle pattern (100 pixels to match)
- Cost function: Hamming distance (count mismatched pixels)
- Neighborhood: Flip one pixel at a time (100 neighbors per state)

**The Algorithm:**
```python
while cost > 0 and iterations < max_iterations:
    neighbors = generate_all_100_neighbors(current_state)
    best_neighbor = min(neighbors, key=cost_function)
    
    if cost(best_neighbor) >= cost(current_state):
        break  # Stuck at local optimum
    
    current_state = best_neighbor
    iterations += 1
```

**Results:**
- Simple pattern (circle): **100% success rate**, avg 147 iterations
- Complex pattern (checkerboard): **85% success rate**, gets stuck in local optima
- Stochastic sampling (50 neighbors): **95% success**, 2x faster

**The Insight:** Hill climbing works beautifully on smooth cost landscapes but fails on complex ones.

**This limitation explains why modern AI uses:**
- **Simulated annealing** — allows temporary cost increases (probabilistic acceptance)
- **Genetic algorithms** — explores multiple paths simultaneously (population-based)
- **Gradient descent with momentum** — escapes shallow local minima (velocity-based)

---

### **3. Stochastic Sampling: The Speed vs. Accuracy Trade-Off**

One enhancement I added beyond requirements was **stochastic hill climbing**:

Instead of evaluating all 100 neighbors, randomly sample 50.

**Trade-offs:**
- ⚡ **Speed:** 2x faster per iteration
- ⚠️ **Accuracy:** May miss optimal move 5% of the time
- 📊 **Final cost:** Avg 0.5 pixels worse than full evaluation

**Real-world application:** When you have 10,000 neighbors (e.g., 100×100 image), evaluating all is impractical. Stochastic sampling becomes mandatory.

---

## KPIs

For the hill climbing implementation, I tracked:

| Metric | Simple Pattern | Complex Pattern |
|--------|---------------|-----------------|
| **Initial Cost** | ~50 mismatched pixels | ~50 mismatched pixels |
| **Final Cost** | 0 (perfect) | 0-8 (may get stuck) |
| **Iterations** | ~147 | ~500 (hits plateau limit) |
| **Time** | <0.03s | <0.2s |
| **Neighbors Evaluated** | ~14,700 | ~50,000 |
| **Success Rate** | 100% | 85% |

**Key Takeaway:** Problem structure matters more than algorithm sophistication. A simple greedy search beats complex methods on convex problems.

---

## 💥 Insights

This project transformed my understanding of AI math:

| Before | After |
|--------|-------|
| "Eigenvalues are λ where det(A - λI) = 0" (memorized formula) | Built cofactor expansion recursively, **saw** how determinants break down |
| "Gradient descent minimizes loss" (vague intuition) | Computed RRBF gradients by hand, **felt** the chain rule propagate |
| "Hill climbing gets stuck in local optima" (heard in lectures) | Watched hill climbing fail on checkerboards, **understood** why cost landscape matters |

This transformation from abstract concepts to concrete understanding has fundamentally changed how I approach AI problems: I now see the math not as a collection of formulas, but as a toolkit of interconnected ideas that I can manipulate and reason about directly.

The hands-on experience has given me a deep, intuitive grasp of the mathematical foundations that underpin modern AI, enabling me to approach complex problems with both confidence and clarity, and to think about optimization and machine learning as **algorithms to apply** and **mathematical principles** that I can understand and leverage in practice.

---

## ❓ What's Next for EigenAI?

**Module 6 introduced three optimization paradigms:**
- ✅ **Hill Climbing** (implemented in Assessment 3)
- 🕐 **Simulated Annealing** (probabilistic escape from local optima)
- 🕐 **Genetic Algorithms** (population-based evolutionary search)

**Upcoming v0.4.X+ features:**

**Enhanced Optimization Suite:**
- Simulated Annealing comparison (temperature schedules, acceptance probability)
- Genetic Algorithm variant (crossover, mutation, selection operators)
- A* Search for pathfinding (admissible heuristics)
- Q-Learning demo (reinforcement learning basics)

**Platform Enhancements:**
- **Authentication** — user login and progress tracking
- **LLM Integration** — GPT-4 powered step-by-step explanations with rate limiting
- **Custom Agent Framework** — Built from the ground-up using knowledge graphs and reasoning for problem-solving
- **Supabase BaaS** — cloud storage for user data and solutions
- **Backend Framework** — FastAPI or Flask for RESTful API
- **Weekly Digest** — agentic integration for learning analytics
- **Test Coverage** — comprehensive unit testing with pytest
- **Security Enhancements** — input sanitization, HTTPS enforcement

---

## Try It Out

If you want to explore EigenAI:

- **🌍 Live Demo:** [eigen-ai.streamlit.app](https://eigen-ai.streamlit.app/)
- 📋 [Assessment 2A, S1P1, Determinants, Reflective Report](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment2/Set1Problem1/MFA501_Assessment2_Set1Problem1_report_Faria_Luis.pdf)
- 📹 [Assessment 2A, S1P1, Determinants, Video Demo](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment2/Set1Problem1/MFA501_Assessment2_Set1Problem1_video_Faria_Luis.mp4)
- 📋 [Assessment 2A, S1P2, Eigenvalues, Reflective Report](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment2/Set1Problem2/MFA501_Assessment2_Set1Problem2_report_Faria_Luis.pdf)
- 📹 [Assessment 2A, S1P2, Eigenvalues, Video Demo](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment2/Set1Problem2/MFA501_Assessment2_Set1Problem2_video_Faria_Luis.mp4)
- 📋 [Assessment 2B, S2P1, Integrals, Reflective Report](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment2/Set2Problem1/MFA501_Assessment2B_Set1_report_Faria_Luis.pdf)
- 📹 [Assessment 2B, S2P1, Integrals, Video Demo](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment2/Set2Problem1/MFA501_Assessment2B_Set1_demo_Faria_Luis.mp4)
- 📋 [Assessment 2B, S2P2, RRBF, Reflective Report](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment2/Set2Problem2/MFA501_Assessment2B_Set2_report_Faria_Luis.pdf)
- 📹 [Assessment 2B, S2P2, RRBF, Video Demo](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment2/Set2Problem2/MFA501_Assessment2B_Set2_demo_Faria_Luis.mp4)
- 📋 [Assessment 3, Hill Climbing, Reflective Report](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment3/Set3Problem1/MFA501_Assessment3_report_Faria_Luis.pdf)
- 📹 [Assessment 3, Hill Climbing, Video Demo](https://github.com/lfariabr/masters-swe-ai/blob/master/2025-T2/T2-MFA/assignments/Assessment3/Set3Problem1/MFA501_Assessment3_demo_Faria_Luis.mp4)
- 🤖 [EigenAi Source Code](https://github.com/lfariabr/masters-swe-ai/tree/master/2025-T2/T2-MFA/projects/eigenai)

---

## Let's Connect!

Building EigenAI has been the perfect bridge between mathematical theory and practical software engineering. If you're:

- Learning AI/ML foundations
- Building educational tools
- Passionate about making math accessible
- Interested in optimization algorithms

I’d love to connect:

- **LinkedIn:** [linkedin.com/in/lfariabr](https://www.linkedin.com/in/lfariabr/)  
- **GitHub:** [github.com/lfariabr](https://github.com/lfariabr)  
- **Portfolio:** [luisfaria.dev](https://luisfaria.dev)

---

## References & Further Reading

**Academic Sources:**
- Strang, G. (2016). *Introduction to linear algebra* (5th ed.). Wellesley-Cambridge Press.
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep learning*. MIT Press.
- Nocedal, J., & Wright, S. (2006). *Numerical optimization*. Springer.

**Project Tech:**
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SymPy Symbolic Math](https://docs.sympy.org/)
- [Python Type Hints (PEP 484)](https://peps.python.org/pep-0484/)

---

**Tags:** #machinelearning #python #streamlit #ai #mathematics #optimization #hillclimbing #education

---

*Built with ☕ and calculus by [Luis Faria](https://luisfaria.dev)  
Student @ Torrens University Australia | MFA501 | Dec 2025*