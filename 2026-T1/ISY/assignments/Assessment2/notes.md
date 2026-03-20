# Assessment 2 — Study Notes
> Session: 2026-03-18 | Notebook: `intro_to_modeling_Luis.ipynb`

> claude --resume 8dfd9e3d-ab3c-4db3-ac16-03fd5715851e

---

## TL;DR

- Task 0: data cleaning done — `'?'` values handled, imputation strategy in place
- Task 1: baseline model runs but doesn't learn — flat loss, predicting mean price (~$13k) for everything
- Root cause: unscaled features → Task 2 fix is normalization, not hyperparameter tuning
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
2. ✅ Task 1: baseline — prove the raw model fails
3. 🕐 Task 2: add normalization — model should converge
4. 🕐 Task 3+: hyperparameter experiments on a model that actually works

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
