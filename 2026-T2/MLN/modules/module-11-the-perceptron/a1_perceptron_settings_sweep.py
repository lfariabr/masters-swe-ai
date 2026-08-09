"""
Activity 1 - Perceptron Settings: reproducible hyperparameter sweep.

Reuses the *exact* Perceptron class from
`a1_MLN601_Module11_perceptron_with_visualization.ipynb` (Fariello, Harvard)
so the numbers here match the notebook. We only add the experiment harness.

What it answers (the three forum questions):
  1. What are the best perceptron settings?  -> the sweep table below.
  2. Which settings had the greater effect on classification?
  3. Any other observations?

How to run:
    python3 a1_perceptron_settings_sweep.py
Outputs:
    - a printed results table (real convergence numbers)
    - a1_perceptron_settings_sweep.png (errors-per-epoch comparison)

Env: Homebrew python3.14, numpy/pandas/sklearn/matplotlib (system, no venv).
"""

import json
import os

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

HERE = os.path.dirname(os.path.abspath(__file__))
NB = os.path.join(HERE, "a1_MLN601_Module11_perceptron_with_visualization.ipynb")

# ---------------------------------------------------------------------------
# 1. Pull the Perceptron class straight out of the notebook (no re-typing).
#    Run every code cell EXCEPT the final three (75-77), which actually train
#    and plot; we want the class definition + attached methods only.
# ---------------------------------------------------------------------------
def load_perceptron_class():
    nb = json.load(open(NB))
    ns = {"np": np, "pd": pd, "plt": plt}
    skip = {75, 76, 77}  # the "run it" cells
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code" or i in skip:
            continue
        src = "".join(cell["source"])
        if src.startswith("from sklearn.datasets import load_iris"):
            continue  # we load our own data below
        exec(src, ns)  # noqa: S102 - trusted local notebook
    return ns["Perceptron"]


Perceptron = load_perceptron_class()


# ---------------------------------------------------------------------------
# 2. Data. Notebook task: Iris, first 100 rows (setosa vs versicolor),
#    features = sepal length (col 0) + petal length (col 2), labels -1/+1.
#    This pair is LINEARLY SEPARABLE. We also build the HARD pair
#    (versicolor vs virginica) to show the no-convergence case.
# ---------------------------------------------------------------------------
iris = load_iris()
df = pd.DataFrame(np.c_[iris["data"], iris["target"]],
                  columns=iris["feature_names"] + ["target"])

# Separable pair: setosa (0) vs versicolor (1)
sep_labels = np.where(df.iloc[0:100, 4].values == 0, -1, 1)
sep_samples = df.iloc[0:100, [0, 2]].values

# Hard pair: versicolor (1) vs virginica (2) -> overlapping -> NOT separable
hard_labels = np.where(df.iloc[50:150, 4].values == 1, -1, 1)
hard_samples = df.iloc[50:150, [0, 2]].values


def run(samples, labels, lr, n_iter, init, seed=1):
    """Train once and report (converged?, epoch, final_errors, weights)."""
    np.random.seed(seed)  # so random-init runs are reproducible
    p = Perceptron(samples, labels)
    p.train(learning_rate=lr, num_iterations=n_iter, weight_values=init)
    hist = p.misclassifications
    converged = hist[-1] == 0
    epoch = len(hist) if converged else None
    return converged, epoch, hist[-1], p.weights.copy(), hist


# ---------------------------------------------------------------------------
# 3. THE SWEEP. Vary learning rate and initial weights on the separable pair.
# ---------------------------------------------------------------------------
learning_rates = [0.0001, 0.001, 0.01, 0.1, 1.0]
inits = {"zeros (0.0)": 0.0, "random [-1,1] (seed=1)": None}

print("=" * 74)
print("SWEEP A - separable pair (setosa vs versicolor), num_iterations=50")
print("=" * 74)
print(f"{'init':<26}{'lr':>10}{'converged':>12}{'epoch':>8}{'final_err':>11}")
print("-" * 74)
rows = []
for init_name, init_val in inits.items():
    for lr in learning_rates:
        conv, epoch, ferr, w, hist = run(sep_samples, sep_labels, lr, 50, init_val)
        rows.append((init_name, lr, conv, epoch, ferr, w, hist))
        print(f"{init_name:<26}{lr:>10}{str(conv):>12}"
              f"{('-' if epoch is None else epoch):>8}{ferr:>11}")

# ---------------------------------------------------------------------------
# 4. num_iterations effect (does raising the cap help once it converges?)
# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("SWEEP B - num_iterations cap (separable pair, lr=0.01, zero init)")
print("=" * 74)
print(f"{'num_iterations':>16}{'converged':>12}{'epoch':>8}{'final_err':>11}")
print("-" * 47)
for n_iter in [1, 2, 3, 5, 10, 50, 500]:
    conv, epoch, ferr, w, hist = run(sep_samples, sep_labels, 0.01, n_iter, 0.0)
    print(f"{n_iter:>16}{str(conv):>12}"
          f"{('-' if epoch is None else epoch):>8}{ferr:>11}")

# ---------------------------------------------------------------------------
# 5. The linear-separability caveat: same settings on the HARD pair.
# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("SWEEP C - NOT-separable pair (versicolor vs virginica), 50 epochs")
print("=" * 74)
print(f"{'lr':>10}{'converged':>12}{'epoch':>8}{'final_err':>11}{'errs (last 8 epochs)':>28}")
print("-" * 69)
for lr in [0.01, 0.1, 1.0]:
    conv, epoch, ferr, w, hist = run(hard_samples, hard_labels, lr, 50, 0.0)
    tail = ",".join(str(h) for h in hist[-8:])
    print(f"{lr:>10}{str(conv):>12}"
          f"{('-' if epoch is None else epoch):>8}{ferr:>11}{tail:>28}")

# ---------------------------------------------------------------------------
# 6. Figure: errors-per-epoch, separable (zeros vs random) + not-separable.
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))

_, _, _, _, h_zero = run(sep_samples, sep_labels, 0.01, 50, 0.0)
axes[0].bar(range(1, len(h_zero) + 1), h_zero, color=(0.2, 0.4, 0.6, 0.75))
axes[0].set_title("Separable + zero init\n(converges fast)")

_, _, _, _, h_rand = run(sep_samples, sep_labels, 0.01, 50, None)
axes[1].bar(range(1, len(h_rand) + 1), h_rand, color=(0.2, 0.6, 0.4, 0.75))
axes[1].set_title("Separable + random init\n(converges, more epochs)")

_, _, _, _, h_hard = run(hard_samples, hard_labels, 0.01, 50, 0.0)
axes[2].bar(range(1, len(h_hard) + 1), h_hard, color=(0.7, 0.3, 0.3, 0.75))
axes[2].set_title("NOT separable\n(never settles - oscillates)")

for ax in axes:
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Misclassifications")
fig.suptitle("Perceptron settings: what actually moves convergence", fontsize=13)
fig.tight_layout()
out_png = os.path.join(HERE, "a1_perceptron_settings_sweep.png")
fig.savefig(out_png, dpi=110, bbox_inches="tight")
print(f"\nSaved figure -> {out_png}")
