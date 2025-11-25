# integrals.py
# Numerical integration without external libraries.
# Methods: composite trapezoid, composite Simpson, adaptive Simpson.
# Safe parsing of f(x) strings via a restricted math namespace.

import math
from typing import Callable, Tuple, Optional

_ALLOWED = {
    k: getattr(math, k) for k in dir(math)
    if not k.startswith("_")
}
_ALLOWED.update({
    "abs": abs,
    "min": min,
    "max": max
})

class ParseError(Exception):
    pass

def parse_function(expr: str) -> Callable[[float], float]:
    """
    Parse a user expression like 'sin(x) + x**2' into f(x).
    Only names in _ALLOWED and the variable 'x' are permitted.
    """
    expr = expr.strip()
    if not expr:
        raise ParseError("Empty function expression.")
    def f(x: float) -> float:
        local = {"x": x}
        return eval(expr, {"__builtins__": {}}, {**_ALLOWED, **local})
    # quick sanity check
    try:
        _ = f(0.0)
    except (NameError, SyntaxError, TypeError, ZeroDivisionError, AttributeError) as e:
        raise ParseError(f"Invalid function: {e}") from e
    return f

def trapezoid(f: Callable[[float], float], a: float, b: float, n: int) -> Tuple[float,int]:
    if n <= 0: 
        raise ValueError("trapezoid: n must be >= 1")
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    evals = 2
    for i in range(1, n):
        s += f(a + i*h); evals += 1
    return s * h, evals

def simpson(f: Callable[[float], float], a: float, b: float, n: int) -> Tuple[float,int]:
    if n < 2: raise ValueError("simpson: n must be >= 2 (even).")
    if n % 2 == 1: n += 1  # enforce even
    h = (b - a) / n
    s = f(a) + f(b)
    evals = 2
    # odd indices
    odd_sum = 0.0
    for i in range(1, n, 2):
        odd_sum += f(a + i*h); evals += 1
    # even indices
    even_sum = 0.0
    for i in range(2, n, 2):
        even_sum += f(a + i*h); evals += 1
    return (h/3.0) * (s + 4*odd_sum + 2*even_sum), evals

def _simpson_single(f: Callable[[float], float], a: float, b: float) -> Tuple[float,int]:
    c = (a + b) / 2.0
    fa, fb, fc = f(a), f(b), f(c)
    evals = 3
    return (b - a) * (fa + 4*fc + fb) / 6.0, evals

def adaptive_simpson(
    f: Callable[[float], float],
    a: float,
    b: float,
    eps: float = 1e-6,
    max_depth: int = 20
) -> Tuple[float,int,str]:
    """
    Adaptive Simpson with error estimate. Returns (value, evals, reason).
    """
    evals_total = 0

    def recurse(a,b,eps,depth,S,fa,fb,fc) -> Tuple[float,int,bool]:
        nonlocal evals_total
        c = (a + b) / 2.0
        left_mid  = (a + c) / 2.0
        right_mid = (c + b) / 2.0
        fL = f(left_mid); fR = f(right_mid)
        evals_total += 2

        Sleft  = (c - a) * (fa + 4*fL + fc) / 6.0
        Sright = (b - c) * (fc + 4*fR + fb) / 6.0
        if abs(Sleft + Sright - S) <= 15*eps or depth <= 0:
            return Sleft + Sright + (Sleft + Sright - S)/15.0, 0, True
        # Recurse
        val_left, _, okL = recurse(a,c,eps/2.0,depth-1,Sleft,fa,fc,fL)
        val_right, _, okR = recurse(c,b,eps/2.0,depth-1,Sright,fc,fb,fR)
        return val_left + val_right, 0, okL and okR

    # initial Simpson on [a,b]
    c = (a+b)/2.0
    fa, fb, fc = f(a), f(b), f(c)
    evals_total += 3
    S = (b - a) * (fa + 4*fc + fb) / 6.0
    val, _, ok = recurse(a,b,eps,max_depth,S,fa,fb,fc)
    reason = "tolerance reached" if ok else "max depth reached"
    return val, evals_total, reason

def integrate(
    func: Callable[[float], float],
    a: float,
    b: float,
    method: str = "adaptive",
    n: Optional[int] = None,
    eps: float = 1e-6,
    max_depth: int = 20
) -> Tuple[float,int,str]:
    if a == b:
        return 0.0, 1, "zero-length interval"
    if method == "trapezoid":
        if n is None: n = 100
        val, evals = trapezoid(func, a, b, n)
        return val, evals, f"trapezoid with n={n}"
    elif method == "simpson":
        if n is None: n = 100  # will be made even inside
        val, evals = simpson(func, a, b, n)
        return val, evals, f"simpson with n={n if n%2==0 else n+1}"
    elif method in ("adaptive", "adaptive_simpson"):
        val, evals, why = adaptive_simpson(func, a, b, eps=eps, max_depth=max_depth)
        return val, evals, f"adaptive_simpson: {why}, eps={eps}"
    else:
        raise ValueError("Unknown method. Use 'trapezoid', 'simpson', or 'adaptive'.")

# EXTERNAL LIB EXCEPTION:
# Used only for symbolic integration; core numerical methods are implemented from scratch
# The sympy library is used here solely for symbolic computation, not for numerical integration
from sympy import Expr, symbols, integrate as sy_integrate, sympify, SympifyError
from typing import Union

def symbolic_integral(expr_str: str) -> Union[Expr, str]:
    """
    Return the symbolic integral expression and its evaluated result.
    
    Args:
        expr_str (str): String representation of the mathematical expression to integrate
        
    Returns:
        sympy expression or str: The symbolic integral result, or error message
    """
    try:
        x = symbols('x')
        expr = sympify(expr_str)
        symbolic_result = sy_integrate(expr, x)
        return symbolic_result
    except (SympifyError, ValueError, TypeError) as e:
        return f"Could not compute symbolic integral: {e}"