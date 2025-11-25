import streamlit as st
import time
from resolvers.constructor import (
    create_random_state, calculate_cost, generate_neighbors, 
    get_target_image, TARGET_IMAGE, format_state_text, format_state_simple
)
from resolvers.hill_climber import HillClimber

def display_s3p1():
    st.title("🎓 Hill Climbing Algorithm")
    st.caption("Assessment 3 - AI Problem Set")
    
    st.markdown("""
    **Objective:** Reconstruct a 10×10 binary image using Hill Climbing algorithm.
    
    > *HC is a local search algorithm that iteratively moves to better neighboring* 
    > *states until no improvement can be made. Here, we start with a random binary* 
    > *image and flip **one pixel at a time** to minimize the difference from the target.*
    """)
    
    with st.expander("*⚙️ Configuration*"):
        use_complex = st.checkbox(
            "🔥 Use Complex Pattern",
            value=False,
            help="Use checkerboard pattern instead of circle (creates local optima challenges)"
        )
    
        use_stochastic = st.checkbox(
            "⚡ Enable Stochastic Sampling",
            value=False,
            help="Sample random neighbors instead of evaluating all (faster but may miss optimal moves)"
        )
        
        if use_stochastic:
            sample_size = st.slider(
                "🎲 Sample Size (neighbors per iteration)",
                min_value=10,
                max_value=100,
                value=50,
                step=10,
                help="Number of neighbors to evaluate per iteration (out of 100 total)"
            )
        else:
            sample_size = 100
    
    # Get selected target image
    target_image = get_target_image(use_complex=use_complex)
    
    # --- Display Target Image --
    pattern_name = "Complex (Checkerboard)" if use_complex else "Simple (Circle)"
    st.write(f"🎯 Target Image: {pattern_name}")
    st.caption("This is the pattern we're trying to reconstruct")
    
    col_target1, col_target2 = st.columns(2)
    with col_target1:
        st.markdown("**Text Representation:**")
        st.code(format_state_text(target_image), language="text")
    
    with col_target2:
        st.markdown("**Binary Matrix:**")
        st.code(format_state_simple(target_image), language="text")
    
    # --- Algorithm Parameters ---
    st.markdown("---")
    st.markdown("##### Algorithm Parameters")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        try:
            max_iter = int(st.text_input("Max Iterations", "1000", help="Stop after this many iterations"))
            if max_iter <= 0:
                st.warning("Max iterations must be positive")
                return
        except ValueError:
            st.warning("Please enter a valid integer")
            return
    
    with col2:
        try:
            plateau_limit = int(st.text_input("Plateau Limit", "100", help="Stop if no improvement for N iterations"))
            if plateau_limit <= 0:
                st.warning("Plateau limit must be positive")
                return
        except ValueError:
            st.warning("Please enter a valid integer")
            return
    
    with col3:
        seed = st.text_input("Random Seed (optional)", "", help="Leave empty for random start")
        if seed:
            try:
                import random
                random.seed(int(seed))
            except ValueError:
                st.warning("Seed must be an integer")
        
    # --- Run Hill Climbing ---
    if st.button("🟢 Run Hill Climbing Algorithm"):
        
        # Progress animation
        progress = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Generate random initial state
        status_text.text("🔹 Step 1: Generating random initial state...")
        time.sleep(0.3)
        progress.progress(10)
        
        initial_state = create_random_state()
        initial_cost = calculate_cost(initial_state, target_image)
        
        st.info(f"✅ Generated random 10×10 binary image (initial cost: {initial_cost}/100 mismatched pixels)")
        
        # Step 2: Initialize Hill Climber
        status_text.text("🔹 Step 2: Initializing Hill Climbing algorithm...")
        time.sleep(0.3)
        progress.progress(20)
        
        # Wrap cost function to use selected target
        def cost_fn(state):
            return calculate_cost(state, target_image)
        
        climber = HillClimber(
            cost_function=cost_fn,
            neighbor_function=generate_neighbors,
            max_iterations=max_iter,
            plateau_limit=plateau_limit,
            use_stochastic=use_stochastic,
            sample_size=sample_size
        )
        
        # Step 3: Run algorithm
        status_text.text(f"🔹 Step 3: Running Hill Climbing (max {max_iter} iterations)...")
        progress.progress(30)
        
        try:
            result = climber.solve(initial_state, verbose=False)
            
            # Simulate progress updates
            progress.progress(90)
            time.sleep(0.3)
            status_text.text("✅ Hill Climbing complete!")
            progress.progress(100)
            time.sleep(0.5)
            status_text.empty()
            progress.empty()
            
            # --- Display Results ---
            st.markdown("---")
            st.markdown("##### Results")
            
            # Metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Iterations", result.iterations)
            with col_m2:
                st.metric("Improvements", result.improvements)
            with col_m3:
                st.metric("Initial Cost", result.initial_cost)
            with col_m4:
                improvement_pct = ((result.initial_cost - result.final_cost) / result.initial_cost * 100) if result.initial_cost > 0 else 0
                st.metric("Final Cost", result.final_cost, delta=f"-{improvement_pct:.1f}%", delta_color="inverse")
            
            with st.container(border=True):
                st.markdown("#### Performance Metrics")
                col_performance1, col_performance2, col_performance3 = st.columns(3)
                with col_performance1:
                    st.metric("Execution Time", f"{result.execution_time:.4f} s")
                with col_performance2:
                    st.metric("Neighbors Evaluated", result.neighbors_evaluated)
                with col_performance3:
                    st.metric("Cost Evaluations", result.cost_evaluations)

            config_info = f"**Configuration:** {pattern_name} | {'Stochastic' if use_stochastic else 'Full'} Evaluation"
            if use_stochastic:
                config_info += f" ({sample_size} neighbors/iter)"
            st.caption(config_info)

            # Stop reason
            if result.final_cost == 0:
                st.success(f"🎉 **Perfect reconstruction!** {result.stop_reason}")
            elif improvement_pct > 90:
                st.success(f"✅ **Excellent result!** {result.stop_reason}")
            elif improvement_pct > 70:
                st.info(f"👍 **Good result.** {result.stop_reason}")
            else:
                st.warning(f"⚠️ **Moderate result.** {result.stop_reason}")
            
            # --- Initial vs Final Comparison ---
            st.markdown("---")
            st.markdown("##### Initial vs Final State")
            
            col_init, col_final = st.columns(2)
            
            with col_init:
                st.caption("📍 Initial State (Random)")
                st.markdown(f"**Cost:** {result.initial_cost} mismatched pixels")
                st.code(format_state_text(result.initial_state), language="text")
                with st.expander("View as binary matrix"):
                    st.code(format_state_simple(result.initial_state), language="text")
            
            with col_final:
                st.caption("✨ Final State (Optimized)")
                st.markdown(f"**Cost:** {result.final_cost} mismatched pixels")
                st.code(format_state_text(result.final_state), language="text")
                with st.expander("View as binary matrix"):
                    st.code(format_state_simple(result.final_state), language="text")
            
            # --- Error Progression Plot ---
            st.markdown("---")
            st.markdown("##### Cost Progression")
            
            # EXTERNAL LIB EXCEPTION: Matplotlib for visualization only
            # Core algorithm is pure Python
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(result.cost_history, 'b-', linewidth=2, label='Cost (mismatched pixels)')
            ax.axhline(y=0, color='g', linestyle='--', linewidth=1, label='Perfect match')
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Cost (Hamming Distance)')
            ax.set_title(f'Hill Climbing Progress: {result.initial_cost} → {result.final_cost} mismatched pixels')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_ylim(bottom=-5, top=max(result.cost_history) + 5)
            st.pyplot(fig)
            
            # Statistics
            st.caption(f"**Algorithm Stats:** {result.iterations} iterations, {result.improvements} improvements made")
            
            # --- Educational Hints ---
            st.markdown("""
            ---
            ### EigenAI's Hint 🧠
            
            **Understanding Hill Climbing:**
            - **Local Search**: Explores neighboring states to find improvements
            - **Greedy Strategy**: Always moves to the best neighbor (steepest ascent)
            - **No Backtracking**: Once moved, never returns to previous states
            
            **Key Concepts:**
            - **State Space**: All possible 10×10 binary images (2¹⁰⁰ states!)
            - **Cost Function**: Hamming distance = Σᵢⱼ |current[i][j] - target[i][j]|
            - **Neighborhood**: 100 neighbors (one per pixel flip)
            - **Local Optimum**: State where no single pixel flip improves cost
            
            **Why This Matters in AI:**
            - **Foundation of optimization**: Used in neural networks, planning, scheduling
            - **Trade-off**: Fast but may get stuck in local optima (vs. global search)
            - **Real applications**: Image processing, TSP, protein folding, game AI
            
            **Limitations:**
            - Cannot escape local optima (consider Simulated Annealing for that!)
            - No guarantee of finding global optimum
            - Performance depends on initial state and cost landscape
            """)
            
        except Exception as e:
            st.error(f"Algorithm failed: {e!s}")
            st.exception(e)