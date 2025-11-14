[00:00-00:30] Introduction
"Hello, this is Luis Faria demonstrating Set 2 Problem 2: RRBF Type 1 Gradient Calculator.
Implements recurrent radial basis function with manual gradient computation
for training via gradient descent."

[00:30-01:30] Demo 1: Training on sin(x)
- Set: 3 neurons, learning rate 0.05, 100 epochs
- Click "Train Model"
- Show: Error decreasing over epochs
- Point out: "Converged from 0.5 to 0.0027 error"

[01:30-02:30] Demo 2: Visualization
- Show: Model Prediction vs Actual graph
- Point out: "RBF neurons learned to approximate sine wave"
- Show: Weight evolution table

[02:30-03:30] Demo 3: Different hyperparameters
- Try: 5 neurons, learning rate 0.01
- Show: "More neurons = better fit, slower training"

[03:30-04:30] Demo 4: Mathematical explanation
- Point to gradient formulas in UI
- Explain: "Manual partial derivatives, no autograd"
- Show: Recurrent feedback in activation

[04:30-05:00] Conclusion
"Pure Python implementation of neural learning dynamics.
Gradients computed from first principles.
Thank you."