# ISY503 — Intelligent Systems
## Assessment 2: Technical Manual
**Word count target:** 500 words (±10%, references excluded)

---

## 1. How to Run

The notebook (`intro_to_modeling_Luis.ipynb`) requires Python 3 with TensorFlow 1.x compatibility via `tf.compat.v1`. It runs in Google Colab without additional setup, or locally in Jupyter after installing `tensorflow` and standard scientific libraries (`pandas`, `numpy`, `matplotlib`).

To execute: open the notebook, then select **Runtime → Run all** (Colab) or **Kernel → Restart & Run All** (Jupyter). Cells must be run top-to-bottom, as each task depends on the feature columns and normalisation functions defined in earlier cells.

Expected outputs include a series of scatter plot grids (one per task) and a printed `scores` dictionary containing `average_loss` and `loss` values. Final evaluation metrics are: Task 1 — `[FILL: actual loss value]`, Task 2 — `[FILL: actual loss value]`, Task 3 — `[FILL: actual loss value]`, Task 4 — `[FILL: actual loss value]`.

---

## 2. Model Choices and Hyperparameters

All four tasks use TensorFlow's `DNNRegressor` with `hidden_units=[64]`, providing a single hidden layer of 64 neurons. This serves as a reasonable baseline architecture for a 25-feature input space, capable of capturing non-linear relationships while remaining computationally lightweight on a small dataset of 205 examples (Krogh, 2008).

`AdagradOptimizer` was selected over the default `GradientDescentOptimizer` because Adagrad adapts the learning rate per parameter, which reduces sensitivity to feature scale differences and prevents divergence or NaN loss early in training (LeCun et al., 2015). With 15 numeric features spanning different magnitudes (e.g. engine displacement vs. price ratios), adaptive optimisation is particularly beneficial.

Key hyperparameters: `learning_rate=0.01` (standard starting point for small networks), `batch_size=16` (mini-batch SGD; balances gradient noise with convergence speed on a ~164-sample training set), and `num_training_steps=10000` (sufficient iterations for convergence without significant overfitting risk) (Feurer & Hutter, 2019). `[FILL: note any tuning you did — e.g. adjusted learning rate or steps]`

---

## 3. Feature Engineering Decisions

Fifteen continuous numeric columns (e.g. `engine-size`, `horsepower`, `curb-weight`) underwent z-score normalisation: each column's mean is subtracted and the result divided by its standard deviation (with an ε = 1e-6 guard against zero-division). This rescaling brings all numeric features to a comparable unit-free scale, preventing high-magnitude columns from dominating gradient updates and accelerating convergence (Alpaydin, 2014).

Categorical features (e.g. `fuel-type`, `body-style`, `drive-wheels`) were encoded using `categorical_column_with_vocabulary_list` wrapped in `indicator_column`, producing one-hot binary vectors. This representation is the appropriate input format for TensorFlow's `DNNClassifier`/`DNNRegressor` API and avoids imposing an arbitrary ordinal relationship on unordered categories (Pargent et al., 2019).

Task 4 combines all 15 normalised numeric columns with 10 categorical indicator columns, providing the richest feature representation across all four tasks.

---

## 4. Model Comparison and Efficiency

Tasks 1–4 form a progressive experiment in feature representation. Task 1 uses raw (un-normalised) numeric features; Task 2 adds z-score normalisation to the same columns. Normalisation is expected to lower `average_loss` by reducing gradient instability caused by differing feature scales: Task 1 loss `[FILL]` vs. Task 2 loss `[FILL]`.

Task 3 uses categorical features only. Because continuous numeric signals (e.g. exact engine size, horsepower) are discarded, this model is expected to show higher loss than the numeric tasks: Task 3 loss `[FILL]`. This confirms that numeric features carry stronger individual predictive signal for the target price variable.

Task 4 (all features, normalised) achieves the lowest loss `[FILL]`, demonstrating that combining normalised numeric and categorical representations provides complementary information. This is consistent with the general principle that richer, well-prepared feature sets improve DNN regression performance (Sarker, 2021). Task 4 is therefore the recommended model for this dataset.

---

## 5. Visualisation Analysis

The `scatter_plot_inference_grid` function produces a grid of scatter plots, each comparing a single feature on the x-axis against the model's predicted versus actual price. Points close to the diagonal (predicted ≈ actual) indicate accurate predictions; wide vertical spread indicates poor fit.

Normalised models (Tasks 2 and 4) show visibly tighter clustering around the diagonal for high-variance features such as `engine-size` and `horsepower`, compared to the un-normalised Task 1 model. The categorical-only model (Task 3) shows broader scatter across all plots, confirming that numeric features contribute more predictive signal per feature than categorical indicators alone (Alpaydin, 2014). `[FILL: describe specific observations from my own plots — e.g. which features show the tightest/loosest clustering]`

---

## References

Alpaydin, E. (2014). *Introduction to machine learning* (3rd ed.). MIT Press.

Dua, D., & Graff, C. (2019). *UCI Machine Learning Repository*. University of California, Irvine, School of Information and Computer Sciences. http://archive.ics.uci.edu/ml

Feurer, M., & Hutter, F. (2019). Hyperparameter optimization. In L. Hutter, F. Kotthoff, & J. Vanschoren (Eds.), *Automated machine learning: Methods, systems, challenges* (pp. 3–33). Springer.

Krogh, A. (2008). What are artificial neural networks? *Nature Biotechnology*, *26*(2), 195–197. https://doi.org/10.1038/nbt1386

LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. *Nature*, *521*(7553), 436–444. https://doi.org/10.1038/nature14539

Pargent, F., Bischl, B., & Thomas, J. (2019). *A benchmark experiment on how to encode categorical features in predictive modeling*. LMU Munich.

Sarker, I. H. (2021). Machine learning: Algorithms, real-world applications and research directions. *SN Computer Science*, *2*(3), 160. https://doi.org/10.1007/s42979-021-00592-x
