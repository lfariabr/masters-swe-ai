# 🎥 Set 2 – Problem 2 Video Script (RRBF Gradient)

[00:00–00:20] **Introduction**
Hi, this is Luis Faria, and this is my demonstration for *Set 2 – Problem 2*, where I implemented a Recurrent Radial Basis Function network — an RRBF — entirely in pure Python, without NumPy or machine-learning libraries.  
This tool is integrated into the EigenAI interface and computes gradients manually using the chain rule.

---

[00:20–01:00] **Setting Up the Network**
To start the demonstration, I’ll configure the RRBF network with:

- **5 neurons**  
- **200 training epochs**  
- **Learning rate η = 0.01**  
- **X-range = ±3.14**  
- Then I test the model at **x = 0.5** after training.

These parameters match the default example and give a smooth training curve.

Now I press **“Train RRBF Network”**.

---

[01:00–02:00] **Training Summary Output**
After training completes, the interface shows a full **Training Summary**.

You can see:

- **Final average error:** around `0.046654`  
- **Training samples:** 62  
- **Epochs completed:** 200  

This confirms that the model successfully converged using my manually-coded gradient descent routine.

---

[02:00–03:00] **Neuron Parameter Breakdown**
Next, the tool prints the **final parameters** for every neuron:

- Each neuron has an updated **weight (w)**, **center (m)**, and **spread (σ)**.
- These values evolve during training based purely on the gradients I calculated manually —  
  `dError/dw`, `dError/dm`, and `dError/dσ`.

For example:
- Neuron 1 ends up with something like `w = 0.8431`, `m = 1.1322`, `σ = 1.0844`.
- And similar updates happen for the remaining neurons.

This confirms that the recurrent radial basis layer is learning how to approximate the function.

---

[03:00–04:00] **Testing the Network**
Now I scroll down to the **Test Prediction** section.

The test input is:  
- **x = 0.50**

The model predicts:
- **Predicted y ≈ 0.494147**

The actual value of sin(0.5) is:
- **0.479426**

So the error is approximately **3%**, which is excellent for a tiny neural network trained with manually-computed gradients.

The UI highlights this with a green success message.

---

[04:00–04:40] **Training Progress Visualization**
Below this, you can see the training error plot:

- Error starts around ~0.52  
- Drops sharply in the first 20–30 epochs  
- Converges smoothly toward ~0.046  

This graph demonstrates that the gradient descent implementation is stable and the learning rate η = 0.01 is appropriate.

---

[04:40–05:10] **Model Prediction vs Actual Function**
Finally, the interface shows a full comparison plot:

- Green curve: **actual sin(x)**
- Red dashed curve: **RRBF prediction**
- Red dot: the **test point (0.50)**

The RRBF curve closely tracks sin(x) across the entire range, confirming that the network successfully learned the underlying mapping.

---

[05:10–05:30] **Conclusion**
To wrap up:  
- The entire RRBF model — forward pass, gradients, weight updates, and training loop — was implemented manually.  
- No NumPy, no machine-learning libraries, strictly raw Python and math.  
- The UI enhances interpretability through parameter displays, prediction validation, and visualization.

Thank you for watching.