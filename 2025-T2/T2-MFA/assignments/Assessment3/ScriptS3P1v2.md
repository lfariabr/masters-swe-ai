# Set 3 – Problem 1 Video Script (Hill Climbing – Final Version)

## 00:00–00:25 – Introduction

Hi, this is Luis Faria, and this is my demonstration for Assessment 3 – Set 3, Problem 1.

In this problem I implemented a Hill Climbing algorithm, in pure Python, to reconstruct a 10×10 binary image. The solution is integrated into my EigenAI Streamlit app, but all core logic is written without NumPy, SciPy or any ML toolbox – just plain Python and math.

---

## 00:25–01:00 – Problem Overview

The challenge is:

- We have a fixed 10×10 binary *target image*.
- We start from a random 10×10 binary matrix.
- At each step, we flip a single pixel to create a neighbour.
- We measure how good the image is using a *cost function*.
- Hill climbing always moves to the best neighbour it can find.
- We stop when:
  - the cost reaches 0 (perfect match), or
  - we hit a plateau (no improvement after several steps), or
  - we hit the maximum number of iterations.

In other words, this is a small but very clear example of local search and greedy optimization.

---

## 01:00–01:35 – Showing the UI and Configuration Options

On the screen you can see my Streamlit page for Set 3 – Problem 1.

At the top, there's a **Configuration** expander with two key options:

- **Pattern Complexity**: Choose between Simple (Circle) or Complex (Checkerboard) patterns. The complex pattern creates local optima, making it harder for hill climbing.
- **Stochastic Sampling**: Enable this to sample only 50 random neighbors per iteration instead of evaluating all 100, demonstrating the speed vs. accuracy trade-off.

For this demo, I'll use the **Simple Circle pattern** with **full neighbor evaluation**.

Below the config, the app displays:

- the **target image** using block characters (1 as solid block, 0 as empty), and  
- the **10×10 binary matrix** so the structure is clear.

Then we have the standard algorithm parameters:

- **Max iterations**, **plateau limit**, and **random seed** for reproducibility.

This is the pattern the algorithm has to reconstruct starting from random noise.

---

## 01:35–02:20 – Running a Demo (Main Run)

Now I’ll run the hill climbing algorithm on the “Circle” pattern.

I’ll keep:

- Max Iterations = 1000
- Plateau Limit = 100
- Random Seed = some fixed value so the run is reproducible.

Then I click **“Run Hill Climbing Algorithm”**.

The app:

1. Generates a random 10×10 starting image.
2. Computes the **initial cost** – usually around 50 mismatched pixels.
3. Runs hill climbing, repeatedly:
   - generating neighbour states by flipping single pixels,
   - evaluating the cost,
   - and keeping the best neighbour if it improves the solution.

When the run finishes, the results panel updates.

---

## 02:20–03:10 – Reading the Results and Visuals

Here are the results for this run:

- Initial Cost: for example 48
- Final Cost: 0 – meaning perfect reconstruction
- Iterations: for example 147
- Improvements: same number as iterations, so every step was an improvement

The **Performance Metrics** section shows:

- Execution Time: typically under 0.03 seconds
- Neighbors Evaluated: around 14,700 (all 100 neighbors × 147 iterations)
- Cost Evaluations: same as neighbors evaluated plus the initial evaluation

Below the metrics, a **configuration summary** confirms which settings were used: Simple Circle pattern with Full Evaluation mode.

Then I show:

- the **initial random image** and its cost,
- the **final optimized image**, which now visually matches the target,
- and the **cost progression plot**.

The plot shows the cost starting high and then stepping down until it reaches 0. This makes the optimisation process very easy to understand for someone learning hill climbing.

This is one of the "cool features": the user is not only told the result, they can *see* how the algorithm improves the image over time.

---

## 03:10–04:10 – Quick Code Walkthrough

Now I’ll briefly show how the code is structured.

First, in `constructor.py` I define the problem:

- I create the **target matrix**.
- I define the **cost function** as a Hamming distance:
  it simply counts how many pixels differ between the current state and the target.
- I define how to generate **neighbours** by flipping one bit at a time.

Then in `hill_climber.py` I have a **general HillClimber class**:

- It receives:
  - an initial state,
  - a cost function,
  - and a neighbour generator.
- In the main `run()` method, it:
  - evaluates the current cost,
  - generates neighbours,
  - picks the best neighbour that improves the cost,
  - updates the current state,
  - and records the cost history.

This is a pure Python implementation: lists of lists for the matrix, loops for neighbours and cost, and no external numerical libraries.

Finally, in `set3Problem1.py` I build the Streamlit UI that:

- collects user parameters,
- calls the hill climber,
- and renders:
  - the initial and final matrices,
  - the cost stats,
  - and the cost vs iteration plot.

---

## 04:10–05:00 – Wrap-Up and AI Context

To wrap up:

- The algorithm successfully reconstructs a 10×10 binary image, starting from random, using only local search and a simple Hamming distance cost.
- The implementation includes **two key enhancements**:
  - **Pattern complexity selector**: Demonstrates algorithm limitations with the checkerboard pattern that creates local optima.
  - **Stochastic sampling**: Shows the trade-off between computational efficiency and solution quality.
- The code is cleanly separated into:
  - a **problem constructor** (target patterns, cost, neighbours),
  - a **generic hill climbing engine** with optional stochastic sampling,
  - and a **Streamlit view** for interaction and visualisation.
- Everything is implemented in **pure Python**, respecting the assessment constraints.

Conceptually, this small example connects to bigger AI ideas:  
hill climbing is a basic building block for local search, optimisation, and heuristic methods that appear in areas such as scheduling, planning, and also in the intuition behind gradient-based methods. The enhancements demonstrate real-world considerations like scalability and problem complexity.

This concludes my demonstration for Assessment 3 – Set 3, Problem 1.