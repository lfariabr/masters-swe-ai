# 🎥 Set 2 Problem 1 — Numerical Integration (Final Script)

## [00:00–00:20] Introduction
Hi, this is Luis Faria, and this is the demonstration for Set 2 Problem 1: Numerical Integration.  
In this part of the assessment, EigenAI computes definite integrals using three methods I implemented manually:  
**Trapezoid Rule**, **Simpson’s Rule**, and **Adaptive Simpson**.  
Everything is coded from scratch in pure Python—no numerical libraries.

---

## [00:20–01:10] Demo 1 — Trapezoid Rule (f(x) = x²)
I'll start with a simple polynomial:  
**f(x) = x²**, from **0 to 1**, using **n = 50 sub-intervals**.

The exact integral is:
∫₀¹ x² dx = 1/3 ≈ **0.33333333**

*(Type into the app: x**2, a=0, b=1, n=50, method=Trapezoid)*

You can see EigenAI computes a value very close to 0.3333.  
This matches the expected result, showing that the trapezoid rule works well for smooth curves.

---

## [01:10–02:00] Demo 2 — Simpson’s Rule (f(x) = x³)
Now I’ll switch to **Simpson’s Rule**, using the function:  
**f(x) = x³**, with **a=0**, **b=1**, **n=50**.

The exact integral is:
∫₀¹ x³ dx = 1/4 = **0.25**

*(Type: x**3, a=0, b=1, n=50, method=Simpson)*

Simpson converges much faster than the trapezoid method, so we get high precision—very close to 0.25, even with a modest number of subdivisions.

---

## [02:00–03:00] Demo 3 — Adaptive Simpson (f(x) = sin(x))
For the adaptive method, I’ll use something more curved:  
**f(x) = sin(x)** from **0 to π**.

The exact integral is:
∫₀^π sin(x) dx = **2**

*(Type: sin(x), a=0, b=3.14159, method=adaptive)*

Adaptive Simpson automatically increases subdivisions where the curve bends more.  
This gives very high accuracy with fewer function evaluations compared to fixed-step methods.

---

## [03:00–04:10] Error Handling Demo
Now I’ll show a few robustness checks I implemented:

### Invalid function
If I type something invalid, like: