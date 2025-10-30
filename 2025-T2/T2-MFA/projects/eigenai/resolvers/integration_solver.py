"""
# Set 2;
## Problem 1:
Write a program to calculate the Integral of a general function

Helper:
cd T2-MFA/assignments/Assessment2
python s2p1.py
"""

# Step 1: Parse and evaluate mathematical expressions safely
def safe_eval(expr, x_val):
    """
    Safely evaluate a mathematical expression at a given x value.
    Supports: +, -, *, /, **, sin, cos, tan, exp, log, sqrt
    """
    import math
    
    # Create a safe namespace with math functions
    safe_dict = {
        'x': x_val,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'ln': math.log,
        'sqrt': math.sqrt,
        'pi': math.pi,
        'e': math.e,
        '__builtins__': {}  # Prevent access to built-in functions
    }
    
    try:
        # Replace common notations
        expr = expr.replace('^', '**')  # x^2 → x**2
        expr = expr.replace('ln', 'log')  # ln(x) → log(x)
        
        result = eval(expr, safe_dict)
        return float(result)
    except Exception as e:
        raise ValueError(f"Could not evaluate '{expr}' at x={x_val}: {str(e)}")


# Step 2: Riemann Sum (Left, Right, Midpoint)
def riemann_sum(f_expr, a, b, n, method='midpoint'):
    """
    Calculate integral using Riemann sum approximation.
    
    Methods:
    - 'left': Left endpoint rule
    - 'right': Right endpoint rule  
    - 'midpoint': Midpoint rule (most accurate for simple functions)
    
    Args:
        f_expr: String expression like "x**2" or "sin(x)"
        a, b: Integration bounds [a, b]
        n: Number of subdivisions
        method: 'left', 'right', or 'midpoint'
    """
    if n <= 0:
        raise ValueError("Number of subdivisions must be positive")
    if a >= b:
        raise ValueError("Lower bound 'a' must be less than upper bound 'b'")
    
    dx = (b - a) / n  # Width of each rectangle
    total = 0
    
    for i in range(n):
        if method == 'left':
            x_i = a + i * dx
        elif method == 'right':
            x_i = a + (i + 1) * dx
        else:  # midpoint
            x_i = a + (i + 0.5) * dx
        
        total += safe_eval(f_expr, x_i)
    
    return total * dx


# Step 3: Trapezoidal Rule (better approximation)
def trapezoidal_rule(f_expr, a, b, n):
    """
    Calculate integral using Trapezoidal rule.
    More accurate than Riemann sums for smooth functions.
    
    Formula: ∫f(x)dx ≈ (dx/2)[f(x₀) + 2f(x₁) + 2f(x₂) + ... + 2f(xₙ₋₁) + f(xₙ)]
    """
    if n <= 0:
        raise ValueError("Number of subdivisions must be positive")
    if a >= b:
        raise ValueError("Lower bound 'a' must be less than upper bound 'b'")
    
    dx = (b - a) / n
    
    # First and last terms
    total = safe_eval(f_expr, a) + safe_eval(f_expr, b)
    
    # Middle terms (multiplied by 2)
    for i in range(1, n):
        x_i = a + i * dx
        total += 2 * safe_eval(f_expr, x_i)
    
    return (dx / 2) * total


# Step 4: Simpson's Rule (even better for smooth functions)
def simpsons_rule(f_expr, a, b, n):
    """
    Calculate integral using Simpson's 1/3 rule.
    Most accurate for polynomial and smooth functions.
    
    Formula: ∫f(x)dx ≈ (dx/3)[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + f(xₙ)]
    
    Note: n must be even for Simpson's rule
    """
    if n <= 0:
        raise ValueError("Number of subdivisions must be positive")
    if n % 2 != 0:
        raise ValueError("Simpson's rule requires an even number of subdivisions")
    if a >= b:
        raise ValueError("Lower bound 'a' must be less than upper bound 'b'")
    
    dx = (b - a) / n
    
    # First and last terms
    total = safe_eval(f_expr, a) + safe_eval(f_expr, b)
    
    # Odd indices: multiply by 4
    for i in range(1, n, 2):
        x_i = a + i * dx
        total += 4 * safe_eval(f_expr, x_i)
    
    # Even indices: multiply by 2
    for i in range(2, n, 2):
        x_i = a + i * dx
        total += 2 * safe_eval(f_expr, x_i)
    
    return (dx / 3) * total


# Step 5: Main integration function with method selection
def integrate(f_expr, a, b, n=1000, method='simpson'):
    """
    Calculate definite integral ∫[a to b] f(x)dx
    
    Args:
        f_expr: Function as string (e.g., "x**2", "sin(x)", "exp(x)")
        a: Lower bound
        b: Upper bound
        n: Number of subdivisions (default: 1000)
        method: 'riemann_left', 'riemann_right', 'riemann_mid', 'trapezoidal', 'simpson'
    
    Returns:
        Approximate value of the integral
    """
    if method == 'riemann_left':
        return riemann_sum(f_expr, a, b, n, 'left')
    elif method == 'riemann_right':
        return riemann_sum(f_expr, a, b, n, 'right')
    elif method == 'riemann_mid':
        return riemann_sum(f_expr, a, b, n, 'midpoint')
    elif method == 'trapezoidal':
        return trapezoidal_rule(f_expr, a, b, n)
    elif method == 'simpson':
        # Ensure n is even for Simpson's
        if n % 2 != 0:
            n += 1
        return simpsons_rule(f_expr, a, b, n)
    else:
        raise ValueError(f"Unknown method: {method}")


# Step 6: Helper to get method comparison
def compare_methods(f_expr, a, b, n=100):
    """
    Compare all integration methods for the same function.
    Returns a dictionary of results.
    """
    results = {}
    
    methods = [
        'riemann_left',
        'riemann_right', 
        'riemann_mid',
        'trapezoidal',
        'simpson'
    ]
    
    for method in methods:
        try:
            results[method] = integrate(f_expr, a, b, n, method)
        except Exception as e:
            results[method] = f"Error: {str(e)}"
    
    return results


# Testing
if __name__ == "__main__":
    # Test case 1: ∫[0 to 1] x² dx = 1/3 ≈ 0.333...
    print("Test 1: ∫[0 to 1] x² dx")
    result = integrate("x**2", 0, 1, n=1000, method='simpson')
    print(f"Result: {result:.6f} (Expected: 0.333333)")
    
    # Test case 2: ∫[0 to π] sin(x) dx = 2
    import math
    print("\nTest 2: ∫[0 to π] sin(x) dx")
    result = integrate("sin(x)", 0, math.pi, n=1000, method='simpson')
    print(f"Result: {result:.6f} (Expected: 2.000000)")
    
    # Test case 3: Compare methods
    print("\nTest 3: Comparing methods for ∫[0 to 1] x² dx")
    comparison = compare_methods("x**2", 0, 1, n=100)
    for method, value in comparison.items():
        print(f"{method:20s}: {value}")