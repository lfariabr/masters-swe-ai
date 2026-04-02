## Concepts Consolidated — Session 2026-03-25

> End-of-day Q&A after completing Task 2 experiments (Z-score, Min-Max, GD, PCA).

---

**Q1: Have we done everything on normalization? Is PCA normalization?**

PCA is not normalization — it's dimensionality reduction / feature transformation. Normalization rescales features; PCA rotates and compresses them into orthogonal components. For the assignment, frame PCA as "feature engineering" not normalization.

Techniques we haven't tried:
- **Log normalization** — useful for skewed distributions (e.g. `engine-size`)
- **Robust scaling** — uses median + IQR instead of mean + std; less sensitive to outliers
- **Label normalization** — scaling `price` itself; this is what would actually fix GradientDescent (proved empirically in T2.3)

---

**Q2 & Q3: Gradient experiments? Does SGD apply here?**

SGD is already what we're doing. Stochastic = using a random subset (batch) per step instead of the full dataset. With `batch_size=16` and 201 samples, each step sees 16 random rows → that's mini-batch SGD. `GradientDescentOptimizer` in TF is SGD when batch < total dataset.

Optimizers tested:

| Optimizer | Config | Result |
|-----------|--------|--------|
| GradientDescentOptimizer | no normalization | NaN — gradients explode |
| AdagradOptimizer | no normalization | ✅ Best — avg_loss 18.7M |
| GradientDescentOptimizer | + Z-score | NaN — label scale still kills it |
| AdagradOptimizer | + Z-score / Min-Max / PCA | Worse than T1 — lr mismatch |

Not yet tried: **Adam** (Adagrad + momentum combined), **RMSProp**, **Momentum GD**. Adam would be the natural next experiment with normalised inputs.

---

**Q4: What about regularization?**

Not applied in this assessment yet. With 201 rows and a DNN, overfitting is a real risk (though our T2 models are underfitting, not overfitting). `DNNRegressor` supports it directly:

```python
tf.estimator.DNNRegressor(
    ...
    dropout=0.2,                        # deactivates 20% of neurons per step
    l1_regularization_strength=0.001,   # Lasso — drives weak weights to zero (feature selection)
    l2_regularization_strength=0.001,   # Ridge — shrinks all weights evenly
)
```

- **L1 (Lasso):** useful here — scatter plots showed `symboling`, `stroke`, `compression-ratio` have weak correlation with price. L1 would zero those out automatically.
- **L2 (Ridge):** safer default. Prevents any single weight dominating.
- **Dropout:** most powerful DNN regulariser; less critical at this dataset size.

---

**Q5: What strand of machine learning is this exactly?**

```
Machine Learning
└── Supervised Learning          ← we have labels (price)
    └── Regression               ← predicting a continuous value ($)
        └── Deep Learning        ← using hidden layers
            └── MLP Regression   ← fully connected feedforward network
                = DNNRegressor
```

Not classification (predicts a category), not clustering (no labels), not reinforcement learning (no agent/environment/reward loop).

---

**Q6: Is the loss function MSE?**

Yes. `average_loss` = MSE (Mean Squared Error).

```
MSE  = mean((prediction − actual)²)   ← penalises large errors heavily
RMSE = √MSE                           ← same units as label ($), human-readable
```

`DNNRegressor` uses MSE by default. Alternative worth knowing: **MAE (Mean Absolute Error)** = `mean(|prediction − actual|)` — less punishing on outliers. A car dataset with a few exotic high-price outliers makes MAE worth considering.

---

**Q7: Anything else on gradients?**

**Gradient clipping** — caps the gradient magnitude before applying the weight update. Directly solves the T2.3 NaN problem without needing label normalization:

```python
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
optimizer = tf.contrib.estimator.clip_gradients_by_norm(optimizer, clip_norm=5.0)
```

This is the cleaner fix for T2.3 — worth a mention in the manual as "what should have been done".

---

**Q8: Learning rate scheduling (the trick from the RL video)?**

What Lex Fridman's DRL lecture showed is **learning rate decay** — start aggressive (fast learning early), reduce over time (fine-tune later). Directly relevant to T2: the models needed a higher lr early on but would benefit from decay as loss approaches convergence.

| Technique | Idea |
|-----------|------|
| Step decay | halve lr every N steps |
| Exponential decay | `lr = lr₀ × e^(−k × step)` |
| Cosine annealing | lr oscillates like a cosine wave — good for escaping plateaus |
| Warm-up + decay | start tiny → ramp up → decay (used in BERT/Transformers) |
| Cyclical LR | bounce between min/max lr — escapes local minima |

In TF1:
```python
lr = tf.train.exponential_decay(
    learning_rate=0.1,       # start high (compensates for small normalised gradients)
    global_step=tf.train.get_global_step(),
    decay_steps=1000,
    decay_rate=0.96          # multiply by 0.96 every 1000 steps
)
optimizer = tf.train.AdagradOptimizer(lr)
```

This is what T2 models actually needed: `lr=0.1` to compensate for small normalised gradients, decaying to `0.01` as loss converges.

---

**Throughline from today's session:**

> Every T2 experiment "failing" vs T1 is not a failure — it's empirical proof of the Adagrad + normalised input interaction. The hyperparameters from T1 were calibrated for unscaled features. Normalization changes the gradient landscape and requires re-calibration. That's not trial and error — that's systematic ML debugging. The manual should frame it this way.