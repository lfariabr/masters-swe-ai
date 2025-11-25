# constructor.py
# Binary Image Reconstruction Problem for Hill Climbing
# Pure Python implementation - no external libraries

import random
from typing import List, Tuple

# ========================================
# TARGET IMAGES (10x10 Binary Matrices)
# ========================================

# Pattern 1: Circle/Ring shape (SIMPLE - smooth cost landscape)
TARGET_IMAGE_SIMPLE = [
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
]

# Pattern 2: Checkerboard (COMPLEX - more local optima, harder to optimize)
TARGET_IMAGE_COMPLEX = [
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
]

# Default target (for backwards compatibility)
TARGET_IMAGE = TARGET_IMAGE_SIMPLE


def get_target_image(use_complex: bool = False) -> List[List[int]]:
    """
    Get the target image based on complexity preference.
    
    Args:
        use_complex: If True, return complex checkerboard pattern.
                     If False, return simple circle pattern.
    
    Returns:
        List[List[int]]: The selected target image matrix
    """
    return TARGET_IMAGE_COMPLEX if use_complex else TARGET_IMAGE_SIMPLE

# ========================================
# STATE REPRESENTATION
# ========================================

def create_random_state(rows: int = 10, cols: int = 10) -> List[List[int]]:
    """
    Generate a random 10x10 binary matrix as initial state.
    Each pixel is randomly 0 or 1.
    
    Returns:
        List[List[int]]: A 10x10 matrix with random binary values
    """
    return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]


def copy_state(state: List[List[int]]) -> List[List[int]]:
    """
    Create a deep copy of the state matrix.
    
    Args:
        state: The matrix to copy
        
    Returns:
        List[List[int]]: A new matrix with same values
    """
    return [row[:] for row in state]


# ========================================
# COST FUNCTION (OBJECTIVE FUNCTION)
# ========================================

def calculate_cost(state: List[List[int]], target: List[List[int]] = TARGET_IMAGE) -> int:
    """
    Calculate the Hamming distance between current state and target.
    Cost = Number of mismatched pixels.
    
    Mathematical formulation:
        cost = Σᵢ Σⱼ |state[i][j] - target[i][j]|
    
    Args:
        state: Current image matrix
        target: Target image matrix (default: TARGET_IMAGE)
        
    Returns:
        int: Number of pixels that don't match (0 = perfect match)
    """
    # Optional: validating shapes before computing cost
    is_valid, msg = validate_state(state)
    if not is_valid:
        raise ValueError(f"Invalid state: {msg}")
        
    cost = 0
    rows = len(target)
    cols = len(target[0]) if rows > 0 else 0
    
    for i in range(rows):
        for j in range(cols):
            if state[i][j] != target[i][j]:
                cost += 1
    
    return cost


# ========================================
# NEIGHBOR GENERATION
# ========================================

def generate_neighbors(state: List[List[int]]) -> List[Tuple[List[List[int]], Tuple[int, int]]]:
    """
    Generate all possible neighbors by flipping one pixel at a time.
    For a 10x10 matrix, this produces 100 neighbors.
    
    Mathematical formulation:
        For each position (i,j):
            neighbor[i][j] = 1 - state[i][j]  (flip bit)
            neighbor[k][l] = state[k][l]      (keep all other bits)
    
    Args:
        state: Current state matrix
        
    Returns:
        List of tuples (neighbor_state, (row, col))
        where (row, col) is the pixel that was flipped
    """
    neighbors = []
    rows = len(state)
    cols = len(state[0]) if rows > 0 else 0
    
    for i in range(rows):
        for j in range(cols):
            # Create a copy and flip one pixel
            neighbor = copy_state(state)
            neighbor[i][j] = 1 - neighbor[i][j]  # Flip: 0→1 or 1→0
            neighbors.append((neighbor, (i, j)))
    
    return neighbors


# ========================================
# STATE UTILITIES
# ========================================

def format_state_text(state: List[List[int]]) -> str:
    """
    Format state as text grid for display.
    Uses █ for 1 and ░ for 0 for better visualization.
    
    Args:
        state: Matrix to format
        
    Returns:
        str: Formatted string representation
    """
    lines = []
    for row in state:
        line = "".join(["█" if pixel == 1 else "░" for pixel in row])
        lines.append(line)
    return "\n".join(lines)


def format_state_simple(state: List[List[int]]) -> str:
    """
    Format state as simple 0/1 text grid.
    
    Args:
        state: Matrix to format
        
    Returns:
        str: Formatted string with 0s and 1s
    """
    lines = []
    for row in state:
        line = " ".join([str(pixel) for pixel in row])
        lines.append(line)
    return "\n".join(lines)


def states_equal(state1: List[List[int]], state2: List[List[int]]) -> bool:
    """
    Check if two states are identical.
    
    Args:
        state1: First matrix
        state2: Second matrix
        
    Returns:
        bool: True if matrices are identical
    """
    if len(state1) != len(state2):
        return False
    
    for i in range(len(state1)):
        if len(state1[i]) != len(state2[i]):
            return False
        for j in range(len(state1[i])):
            if state1[i][j] != state2[i][j]:
                return False
    
    return True


# ========================================
# VALIDATION
# ========================================

def validate_state(state: List[List[int]]) -> Tuple[bool, str]:
    """
    Validate that a state is a proper 10x10 binary matrix.
    
    Args:
        state: Matrix to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not state:
        return False, "State is empty"
    
    if len(state) != 10:
        return False, f"Expected 10 rows, got {len(state)}"
    
    for i, row in enumerate(state):
        if len(row) != 10:
            return False, f"Row {i} has {len(row)} columns, expected 10"
        
        for j, pixel in enumerate(row):
            if pixel not in (0, 1):
                return False, f"Pixel ({i},{j}) has value {pixel}, expected 0 or 1"
    
    return True, "Valid"