# Assessment 2 — Study Notes
> Session: 2026-03-18 | Notebook: `intro_to_modeling_Luis.ipynb`

> claude --resume 8dfd9e3d-ab3c-4db3-ac16-03fd5715851e

---

## TL;DR

- Task 0: data cleaning done — `'?'` values handled, imputation strategy in place
- Task 1: fixed with `AdagradOptimizer` — avg_loss dropped from ~62M → ~10.8M (~83% reduction), RMSE ~$3,290
- Root cause of original failure: unscaled features → optimizer divergence → model predicting mean for everything
- Scatter plots confirmed which features actually correlate with price

---

## Task 0 — Data Preparation

**Problem:** Several numeric columns were stored as `object` dtype because the CSV uses `'?'` as a placeholder for missing values. Affected columns: `normalized-losses`, `bore`, `stroke`, `horsepower`, `peak-rpm`, `price`.

**Fix applied in cell-16:**
```python
# Convert '?' → NaN via errors='coerce'
pd.to_numeric(car_data[col], errors='coerce')

# Drop rows where LABEL (price) is missing — can't train without it
car_data = car_data[car_data['price'].notna() & (car_data['price'] > 0)].copy()

# Impute missing FEATURES with column mean — keep the row, fill the gap
car_data[col].fillna(col_mean)
```

**Why this matters:**
- Dropping `price=NaN` rows: ~16 cars affected. No label = useless for training.
- Imputing features with mean: preserves the row. Dropping all rows with any `'?'` would waste too much data from a 205-row dataset.
- Change applies to `car_data` directly → all tasks (1–4) inherit clean data automatically.

---

## Task 1 — Baseline Model (un-normalized)

### What the training loop does

```python
for _ in range(num_print_statements):
    model.train(...)   # trains for chunk of steps
    scores = model.evaluate(...)  # evaluates on full dataset
    print(scores)
```

Each iteration trains + evaluates. 10 iterations × 1000 steps = 10,000 total steps. This lets you watch loss evolve over time.

### Results summary

| Step | avg_loss | RMSE | prediction/mean |
|------|----------|------|-----------------|
| 1,000 | 62,975,160 | ~$7,936 | $13,572 |
| 5,000 | 62,894,080 | ~$7,931 | $13,436 |
| 10,000 | 62,869,690 | ~$7,929 | $13,039 |

- `label/mean = $13,207` — actual average car price
- `prediction/mean ≈ $13,000–13,800` — model predicts near-mean for everything
- RMSE ~$7,930 on a $13,207 average = **~60% error**
- **Loss is flat** — model is not learning

### Why it fails (the mean baseline trap)

The model found the laziest solution: predict the average price (~$13k) for every input. This minimises loss without learning any real patterns. It's the ML equivalent of answering "C" to every multiple choice question.

**Root cause — unscaled features:**
```
weight:    2,000 – 4,000   ← huge numbers
peak-rpm:  4,000 – 6,500   ← huge numbers
bore:      2.5 – 4.0        ← tiny numbers
stroke:    2.0 – 4.0        ← tiny numbers
```

Gradient descent updates all weights with the same learning rate. Large-magnitude features dominate gradients and the optimizer goes in circles. Small features barely move.

### Scatter plot observations

Features that showed a clear diagonal pattern (strong correlation with price):
- **Positive:** `engine-size`, `horsepower`, `weight`, `length`, `wheel-base` — bigger/heavier = more expensive
- **Negative:** `highway-mpg`, `city-mpg` — fuel-efficient = cheaper (econoboxes vs performance cars)
- **Weak/flat:** `symboling`, `stroke`, `compression-ratio` — scattered, low predictive value

### Solution for Task 1
Since we are explicitly told not to use normalization, we replaced GradientDescentOptimizer with AdagradOptimizer. Adagrad adapts the learning rate per parameter, which reduces sensitivity to feature scale differences and prevents divergence or NaN loss early in training. With 15 numeric features spanning different magnitudes (e.g. engine displacement vs. price ratios), adaptive optimization is particularly beneficial.

#### Results after Task 1 changes

`label/mean` is fixed at **$13,207** throughout.

| Step | avg_loss | prediction/mean |
|------|----------|-----------------|
| 1,000 | 15,046,353 | $13,599 |
| 2,000 | 13,564,830 | $14,004 |
| 3,000 | 12,317,929 | $12,702 |
| 5,000 | 11,341,380 | $13,204 |
| 8,000 | 11,028,722 | $13,474 |
| 10,000 | **10,822,464** | $13,157 |

**vs GradientDescentOptimizer:**

| | GradientDescent | Adagrad |
|---|---|---|
| Final avg_loss | ~62,900,000 | **10,822,464** |
| Behaviour | Predicting mean every time | Actually learning |
| RMSE | ~$7,929 | **~$3,290** |

> ~83% reduction in loss. The model is no longer lazy.
---

## What's next — Task 2 (TODO)

### The real fix: Normalization (not just hyperparameters)

Hyperparameter tuning (learning rate, layers, batch size) is tweaking. The model is **fundamentally broken** by scale differences. Fix that first.

**Z-score normalization:**
```python
x_normalized = (x - mean) / std_deviation
```

After normalization, all features live in ~(−2, +2). Gradients are balanced. The optimizer can learn which features matter.

### Expected outcome after Task 2
- Loss should start **decreasing** meaningfully (not flat)
- Model should pick up on `engine-size`, `horsepower`, `weight` etc. as dominant predictors
- RMSE should drop significantly below $7,930

### Task progression
1. ✅ Task 0: clean the data
2. ✅ Task 1: fix optimizer → model learns (avg_loss ~10.8M, RMSE ~$3,290)
3. 🕐 Task 2: add normalization → expect further loss reduction
4. 🕐 Task 3+: categorical features + combined model

---

## Key concepts to remember

| Term | Plain English |
|------|---------------|
| MSE (`average_loss`) | Mean of (prediction − actual)² — hard to interpret directly |
| RMSE | √MSE — same units as the label (dollars). Easier to read. |
| Mean baseline | Model predicts the dataset mean for every input. Lazy but valid. Red flag if your model doesn't beat this. |
| Feature normalization | Rescale all inputs to same range so gradients are balanced |
| Imputation | Filling in missing values (with mean, median, etc.) instead of dropping rows |
| `errors='coerce'` | pandas: if conversion fails, return NaN instead of crashing |
