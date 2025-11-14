[00:00-00:30] Introduction
"Hello, this is Luis Faria demonstrating Set 2 Problem 1: Numerical Integration.
EigenAI computes definite integrals using three methods implemented from scratch:
Trapezoid, Simpson, and Adaptive Simpson."

[00:30-01:30] Demo 1: Basic polynomial
- Enter: x**2, bounds [0,1]
- Method: Simpson, n=100
- Show result: 0.333333 (exact: 1/3)
- Point out: "9+ decimal places of accuracy"

[01:30-02:30] Demo 2: Trigonometric
- Enter: sin(x), bounds [0, 3.14159]
- Method: Adaptive Simpson
- Show result: ~2.000000
- Point out: "Only 15 function evaluations vs 100 for fixed method"

[02:30-03:30] Demo 3: Method comparison
- Check "Show Method Comparison"
- Run benchmark
- Point out: "Simpson more accurate than trapezoid for same n"

[03:30-04:30] Demo 4: Error handling
- Try invalid function: "xyz"
- Try invalid bounds: a=5, b=2
- Show: "Robust error messages guide user"

[04:30-05:00] Conclusion
"All methods validated against known analytical results.
Pure Python implementation, no NumPy dependency.
Thank you."