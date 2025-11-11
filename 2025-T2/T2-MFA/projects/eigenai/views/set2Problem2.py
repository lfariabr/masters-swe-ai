import streamlit as st
import math
import time
from resolvers.rrbf import RRBFType1

def display_s2p2():
    st.title("📗 RRBF Gradient")
    st.caption("Set 2 – Problem 2")
    
    st.markdown("""
    Let's train a **Recurrent Radial Basis Function (RRBF) network** and compute gradients manually.  
    EigenAI will help you understand how the RRBF network learns using gradient descent.

    > **What is RRBF?** A neural network with radial basis activation functions that uses 
    > recurrent connections between neurons. Gradients are computed manually using the chain rule.
    """)

    # --- Input section with validation ---
    col1, col2 = st.columns(2)
    with col1:
        try:
            n = int(st.text_input("Number of neurons", "5", help="Recommended: 3-10"))
            if n <= 0:
                st.warning("Number of neurons must be positive")
                return
        except ValueError:
            st.warning("Please enter a valid integer for neurons")
            return
            
        try:
            eta = float(st.text_input("Learning rate (η)", "0.01", help="Typical: 0.001 - 0.1"))
            if eta <= 0:
                st.warning("Learning rate must be positive")
                return
        except ValueError:
            st.warning("Please enter a valid number for learning rate")
            return
    
    with col2:
        try:
            epochs = int(st.text_input("Training epochs", "200", help="Recommended: 100-500"))
            if epochs <= 0:
                st.warning("Epochs must be positive")
                return
        except ValueError:
            st.warning("Please enter a valid integer for epochs")
            return
            
        try:
            range_val = float(st.text_input("X range (±range)", "3.14", help="Example: 3.14 = [-π, π]"))
            if range_val <= 0:
                st.warning("Range must be positive")
                return
        except ValueError:
            st.warning("Please enter a valid number for range")
            return

    # Test input OUTSIDE button
    st.markdown("---")
    try:
        test_x = float(st.text_input("🧪 Test x value (after training)", "1.0", help="Enter any value to test prediction"))
    except ValueError:
        test_x = 1.0

    if st.button("🟢 Train RRBF Network"):
        # Validation
        if n <= 0 or eta <= 0 or epochs <= 0 or range_val <= 0:
            st.error("All inputs must be positive numbers")
            return

        # --- Data generation ---
        st.info("Generating training data from sin(x)...")
        
        # Enforce minimum range to avoid empty dataset:
        # When 0 < range_val < 0.1, int(-10*range_val) == int(10*range_val) == 0
        # This produces range(0, 0) which is empty!
        # Also ensures we have at least some data to train on.
        effective_range = max(range_val, 0.1)
        if range_val < 0.1:
            st.warning(f"⚠️ Range too small ({range_val:.3f}). Using minimum range of 0.1 instead.")
        
        # Compute integer bounds and ensure they span at least 1 unit
        # This guarantees at least one sample even with very small ranges
        # and prevents empty dataset generation.
        lower_bound = int(-10 * effective_range)
        upper_bound = int(10 * effective_range)
        if lower_bound >= upper_bound:
            upper_bound = lower_bound + 1  # Fallback: ensure at least 1 sample
        
        X = [x * 0.1 for x in range(lower_bound, upper_bound)]
        Y = [math.sin(x) for x in X]
        
        # Guard: Explicit check for empty dataset
        # This should never happen due to our bounds logic, but just in case...
        if not X or len(X) == 0:
            st.error(
                f"❌ Failed to generate training data. "
                f"Range bounds [{lower_bound}, {upper_bound}) produced {len(X)} samples. "
                f"Please increase the range value to ≥ 0.1."
            )
            return
        
        st.caption(f"✅ Generated {len(X)} training samples from [{X[0]:.2f}, {X[-1]:.2f}]")

        # --- Progress animation ---
        progress = st.progress(0)
        status_text = st.empty()
        
        # Initialize network
        status_text.text("🔹 Step 1: Initializing RRBF network...")
        time.sleep(0.5)
        progress.progress(20)
        net = RRBFType1(n_neurons=n, eta=eta)
        
        # Training with progress
        status_text.text(f"🔹 Step 2: Training for {epochs} epochs...")
        time.sleep(0.5)
        progress.progress(40)
        
        try:
            # Track error over epochs for visualization
            error_history = []
            for epoch in range(epochs):
                total_err = 0
                for x, y in zip(X, Y, strict=True):
                    err, _ = net.backward(x, y)
                    total_err += abs(err)
                avg_err = total_err / len(X)
                error_history.append(avg_err)
                
                # Update progress
                if epoch % max(1, epochs // 10) == 0:
                    progress.progress(40 + int(50 * epoch / epochs))
            
            status_text.text("🔹 Step 3: Generating predictions...")
            progress.progress(95)
            time.sleep(0.5)
            progress.progress(100)
            status_text.text("✅ Training complete!")
            time.sleep(0.5)
            status_text.empty()
            progress.empty()

            # --- Results ---
            st.markdown("---")
            st.subheader("📊 Training Summary")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Final Avg Error", f"{error_history[-1]:.6f}")
            with col_b:
                st.metric("Training Samples", len(X))
            with col_c:
                st.metric("Epochs Completed", epochs)

            st.subheader("⚙️ Final Neuron Parameters")
            for i in range(n):
                st.markdown(
                    f"- **Neuron {i+1}:** "
                    f"w = `{net.weights[i]:.4f}`, m = `{net.centers[i]:.4f}`, σ = `{net.sigmas[i]:.4f}`"
                )

            # --- Test prediction ---
            st.markdown("---")
            st.subheader("🧪 Test Prediction")
            y_pred, _ = net.forward(test_x)
            y_actual = math.sin(test_x)
            col_test1, col_test2, col_test3 = st.columns(3)
            with col_test1:
                st.metric("Input x", f"{test_x:.4f}")
            with col_test2:
                st.metric("Predicted y", f"{y_pred:.6f}")
            with col_test3:
                st.metric("Actual sin(x)", f"{y_actual:.6f}")
            
            error_pct = abs(y_pred - y_actual) / (abs(y_actual) + 1e-10) * 100
            if error_pct < 5:
                st.success(f"✅ Excellent! Error: {error_pct:.2f}%")
            elif error_pct < 15:
                st.info(f"Good approximation. Error: {error_pct:.2f}%")
            else:
                st.warning(f"Moderate error: {error_pct:.2f}%. Try more epochs or neurons.")

            # EXTERNAL LIB EXCEPTION: Visualization
            # Note: matplotlib used only for visualization, core RRBF is pure Python
            import numpy as np
            import matplotlib.pyplot as plt

            st.markdown("---")
            st.subheader("📈 Training Progress")
            
            # Error over epochs
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.plot(error_history, 'b-', linewidth=2)
            ax1.set_xlabel('Epoch')
            ax1.set_ylabel('Average Error')
            ax1.set_title('Training Error Over Time')
            ax1.grid(True, alpha=0.3)
            st.pyplot(fig1)

            # Predictions vs Actual
            st.subheader("📊 Model Predictions vs Actual")
            X_test = np.linspace(-range_val, range_val, 100)
            Y_pred = [net.forward(x)[0] for x in X_test]
            Y_actual = [math.sin(x) for x in X_test]
            
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            ax2.plot(X_test, Y_actual, 'g-', linewidth=2, label='Actual sin(x)', alpha=0.7)
            ax2.plot(X_test, Y_pred, 'r--', linewidth=2, label='RRBF Prediction')
            ax2.scatter([test_x], [y_pred], color='red', s=100, zorder=5, label=f'Test point ({test_x:.2f})')
            ax2.set_xlabel('x')
            ax2.set_ylabel('y')
            ax2.set_title(f'RRBF Network Approximation of sin(x) with {n} neurons')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            st.pyplot(fig2)

            st.markdown("""
            ---
            ### EigenAi's Hint 🧠

            **Understanding RRBF Gradients:**
            - **Radial Basis Functions**: Each neuron responds most strongly to inputs near its center (m)
            - **Gradient Descent**: Computes ∂Error/∂w, ∂Error/∂m, ∂Error/∂σ using chain rule
            - **Manual Implementation**: No libraries used—pure calculus and Python!
            
            **Key Parameters:**
            - **w (weights)**: Output contribution of each neuron
            - **m (centers)**: Where each neuron is most active
            - **σ (spread/sigma)**: How wide each neuron's activation is
            
            **Why This Matters in AI:**
            - RBF networks are used in function approximation, time series prediction, and control systems
            - Understanding manual gradient computation is crucial for implementing custom neural architectures
            - This is the foundation of how backpropagation works in deep learning!
            """)
            
        except Exception as e:
            st.error(f"Training failed: {str(e)}")
            st.exception(e)
        