import sys
from pathlib import Path

# Add parent directory to path so we can import from project root
sys.path.insert(0, str(Path(__file__).parent.parent))

from resolvers.eigen_solver import eigenpairs

def test_eigensolver():
    """
    Test cases mentioned in the reflective report.
    """
    test_cases = [
        {
            'name': 'Identity matrix',
            'matrix': [[1, 0], [0, 1]],
            'expected_eigenvalues': [1, 1]
        },
        {
            'name': 'Diagonal matrix',
            'matrix': [[3, 0], [0, 5]],
            'expected_eigenvalues': [5, 3]
        },
        {
            'name': 'Symmetric matrix',
            'matrix': [[2, 1], [1, 2]],
            'expected_eigenvalues': [3, 1]
        },
        {
            'name': 'Zero matrix',
            'matrix': [[0, 0], [0, 0]],
            'expected_eigenvalues': [0, 0]
        },
        {
            'name': 'Scaling matrix',
            'matrix': [[4, 0], [0, 4]],
            'expected_eigenvalues': [4, 4]
        }
    ]
    
    print("Running test cases from reflective report...\n")
    for test in test_cases:
        print(f"Testing: {test['name']}")
        print(f"  Matrix: {test['matrix']}")
        
        pairs = eigenpairs(test['matrix'])
        computed_vals = sorted([p[0] for p in pairs], reverse=True)
        expected_vals = sorted(test['expected_eigenvalues'], reverse=True)
        
        # Check within tolerance
        tolerance = 1e-9
        assert len(computed_vals) == len(expected_vals), (
            f"Eigenvalue count mismatch: expected {len(expected_vals)}, got {len(computed_vals)}"
        )
        matches = all(abs(c - e) < tolerance for c, e in zip(computed_vals, expected_vals))
        assert matches, f"Expected {expected_vals}, got {computed_vals}"
        print(f"  ✓ PASSED: λ = {computed_vals}")
        
# Run tests if executed directly
if __name__ == "__main__":
    test_eigensolver()