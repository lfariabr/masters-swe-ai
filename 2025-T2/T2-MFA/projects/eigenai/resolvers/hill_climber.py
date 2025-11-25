# hill_climber.py
# Reusable Hill Climbing Algorithm
# Pure Python implementation - no external libraries

from typing import List, Tuple, Callable, Any, Optional
import time
import random

class HillClimberResult:
    """
    Container for hill climbing results.
    """
    def __init__(self):
        self.initial_state: Any = None
        self.final_state: Any = None
        self.initial_cost: int = 0
        self.final_cost: int = 0
        self.iterations: int = 0
        self.cost_history: List[int] = []
        self.improvements: int = 0
        self.plateau_count: int = 0
        self.stop_reason: str = ""
        self.best_move_history: List[Tuple[int, int]] = []  # Track which pixels were flipped
        # Performance benchmarking
        self.execution_time: float = 0.0
        self.neighbors_evaluated: int = 0
        self.cost_evaluations: int = 0


class HillClimber:
    """
    Reusable Hill Climbing algorithm implementation.
    
    Hill Climbing Algorithm:
    1. Start with an initial state
    2. Evaluate all neighbors
    3. Move to the best neighbor if it improves cost
    4. Repeat until no improvement or stopping condition met
    
    Stopping Conditions:
    - Cost reaches zero (perfect solution)
    - Maximum iterations reached
    - Plateau limit reached (no improvement for N iterations)
    """
    
    def __init__(
        self,
        cost_function: Callable[[Any], int],
        neighbor_function: Callable[[Any], List[Tuple[Any, Any]]],
        max_iterations: int = 1000,
        plateau_limit: int = 50,
        use_stochastic: bool = False,
        sample_size: int = 100
    ):
        """
        Initialize Hill Climber with problem-specific functions.
        
        Args:
            cost_function: Function that takes a state and returns its cost (lower is better)
            neighbor_function: Function that takes a state and returns list of (neighbor, move_info)
            max_iterations: Maximum number of iterations before stopping
            plateau_limit: Stop if no improvement for this many iterations
            use_stochastic: If True, sample random neighbors when count > sample_size
            sample_size: Max neighbors to evaluate per iteration (stochastic mode)
        """
        self.cost_function = cost_function
        self.neighbor_function = neighbor_function
        self.max_iterations = max_iterations
        self.plateau_limit = plateau_limit
        self.use_stochastic = use_stochastic
        self.sample_size = sample_size
        
    def solve(self, initial_state: Any, verbose: bool = False) -> HillClimberResult:
        """
        Run hill climbing algorithm starting from initial_state.
        
        Args:
            initial_state: Starting state for the search
            verbose: If True, print progress information
            
        Returns:
            HillClimberResult: Object containing results and statistics
        """
        result = HillClimberResult()
        result.initial_state = initial_state
        
        # Initialize
        current_state = initial_state
        start_time = time.time()
        current_cost = self.cost_function(current_state)
        result.initial_cost = current_cost
        result.cost_history = [current_cost]
        # Count the initial cost evaluation as well
        result.cost_evaluations += 1

        plateau_counter = 0
        iteration = 0

        if current_cost == 0:
            result.final_state = current_state
            result.final_cost = current_cost
            result.iterations = iteration
            result.plateau_count = plateau_counter
            result.stop_reason = "Found optimal solution (cost = 0)"
            result.execution_time = time.time() - start_time
            return result
        
        if verbose:
            print("Starting Hill Climbing:")
            print(f"  Initial cost: {current_cost}")
            print(f"  Max iterations: {self.max_iterations}")
            print(f"  Plateau limit: {self.plateau_limit}")
            print()
        
        # Main hill climbing loop
        while iteration < self.max_iterations:
            iteration += 1
            
            # Generate all neighbors
            neighbors = self.neighbor_function(current_state)
            
            if not neighbors:
                result.stop_reason = "No neighbors generated"
                break
            
            # Find best neighbor
            best_neighbor = None
            best_cost = current_cost
            best_move = None
            
            # Stochastic sampling: if enabled and neighbors > threshold, sample randomly
            if self.use_stochastic and len(neighbors) > self.sample_size:
                neighbors_to_eval = random.sample(neighbors, self.sample_size)
                if verbose and iteration == 1:
                    print(f"  Using stochastic sampling: {self.sample_size} of {len(neighbors)} neighbors")
            else:
                neighbors_to_eval = neighbors
            
            for neighbor, move_info in neighbors_to_eval:
                result.neighbors_evaluated += 1
                neighbor_cost = self.cost_function(neighbor)
                result.cost_evaluations += 1
                
                if neighbor_cost < best_cost:
                    best_cost = neighbor_cost
                    best_neighbor = neighbor
                    best_move = move_info
            
            # Check if we found an improvement
            if best_neighbor is None:
                # No improvement found - we're at a local optimum
                plateau_counter += 1
                result.cost_history.append(current_cost)
                
                if verbose and iteration % 100 == 0:
                    print(f"  Iteration {iteration}: Cost={current_cost}, Plateau={plateau_counter}")
                
                # Check plateau limit
                if plateau_counter >= self.plateau_limit:
                    result.stop_reason = f"Plateau reached (no improvement for {plateau_counter} iterations)"
                    break
                    
            else:
                # Improvement found - move to better neighbor
                current_state = best_neighbor
                current_cost = best_cost
                result.cost_history.append(current_cost)
                result.improvements += 1
                result.best_move_history.append(best_move)
                
                # Reset plateau counter
                plateau_counter = 0
                
                if verbose and (iteration % 100 == 0 or current_cost == 0):
                    print(f"  Iteration {iteration}: Cost={current_cost} (improvement!)")
                
                # Check if we reached optimal solution
                if current_cost == 0:
                    result.stop_reason = "Optimal solution found (cost = 0)"
                    break
        
        # Check if we hit max iterations
        if iteration >= self.max_iterations and not result.stop_reason:
            result.stop_reason = f"Maximum iterations reached ({self.max_iterations})"
        
        # Store final results
        result.final_state = current_state
        result.final_cost = current_cost
        result.iterations = iteration
        result.plateau_count = plateau_counter
        result.execution_time = time.time() - start_time
        
        if verbose:
            print()
            print("Hill Climbing Complete:")
            print(f"  Stop reason: {result.stop_reason}")
            print(f"  Iterations: {result.iterations}")
            print(f"  Improvements: {result.improvements}")
            print(f"  Final cost: {result.final_cost}")
            print(f"  Cost reduction: {result.initial_cost - result.final_cost}")
            print(f"  Execution time: {result.execution_time:.4f} seconds")
            print(f"  Neighbors evaluated: {result.neighbors_evaluated}")
            print(f"  Cost evaluations: {result.cost_evaluations}")
        
        return result