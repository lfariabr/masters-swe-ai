"""DLE602 Assessment 1 - bias/variance sweep over the N-Gram hyperparameters.

A small analysis harness that *reuses* the model in ``dle602_sentiment_ngram.py``
(it imports the class, it does not modify it) to make the bias-variance trade-off
tangible on the real Assessment 1 data:

  * ``--add-k`` (smoothing strength) is the regularization dial. Small k trusts the
    training counts (low bias, high variance -> overfitting); large k washes the
    counts toward uniform (high bias -> underfitting).
  * ``n`` (N-Gram order) is the capacity dial. Higher n = more context but sparser
    counts, so it overfits sooner and needs more smoothing.

For every (n, k) we record accuracy on a *training* sample (how well the model fits
data it has seen) and on STS-Test / STS-Gold (unseen data). The gap between train
and test accuracy is the overfitting signature; the inverted-U of test accuracy vs
k is the bias-variance curve.

Key efficiency point: in the model, ``k`` is only used at *classify* time, never at
*train* time (training is pure counting). So we train once per N-Gram order and
sweep k by mutating ``model.k`` - no retraining.

How to run
----------
    # from the Assessment1 directory (datasets already downloaded):
    python code/bias_variance_sweep.py

    # or point at explicit paths / change the grid:
    python code/bias_variance_sweep.py --train dataset/sentiment140_train_sample.csv \
        --eval-a dataset/sts_test.csv --eval-b dataset/sts_gold.csv \
        --out outputs/bias_variance --train-sample 5000

How to test
-----------
    python -m py_compile code/bias_variance_sweep.py
    # then run the command above; it writes outputs/bias_variance/sweep.csv and
    # figures/bias_variance.png. Results are deterministic for a fixed --train-sample
    # (the only sampling is a fixed-stride slice of the training set).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

# Reuse the Assessment 1 model without touching it.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dle602_sentiment_ngram import (  # noqa: E402
    NGramSentimentModel,
    evaluate,
    load_dataset,
)

# The grid. k spans four orders of magnitude so both failure modes are visible.
NGRAM_ORDERS = (1, 2, 3)
ADD_K_VALUES = (0.001, 0.01, 0.1, 1.0, 5.0, 25.0)


def train_accuracy_sample(examples, stride):
    """Take a deterministic, evenly-spaced slice of the training set.

    Used to estimate how well the model fits data it was trained on, without
    re-scoring all 80k tweets for every grid point.
    """
    return examples[::stride]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--train", type=Path,
                        default=Path("dataset/sentiment140_train_sample.csv"))
    parser.add_argument("--eval-a", type=Path, default=Path("dataset/sts_test.csv"))
    parser.add_argument("--eval-a-name", default="STS-Test")
    parser.add_argument("--eval-b", type=Path, default=Path("dataset/sts_gold.csv"))
    parser.add_argument("--eval-b-name", default="STS-Gold")
    parser.add_argument("--threshold", type=float, default=0.25)
    parser.add_argument("--train-sample", type=int, default=5000,
                        help="approx. #training tweets used to estimate train accuracy")
    parser.add_argument("--out", type=Path, default=Path("outputs/bias_variance"))
    args = parser.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "figures").mkdir(parents=True, exist_ok=True)

    print("Loading data ...")
    train_examples = load_dataset(args.train)
    eval_a = load_dataset(args.eval_a)
    eval_b = load_dataset(args.eval_b)
    stride = max(1, len(train_examples) // max(1, args.train_sample))
    train_eval = train_accuracy_sample(train_examples, stride)
    print(f"  train={len(train_examples):,}  train-sample={len(train_eval):,}  "
          f"{args.eval_a_name}={len(eval_a):,}  {args.eval_b_name}={len(eval_b):,}")

    rows: list[dict] = []
    for n in NGRAM_ORDERS:
        # Train ONCE per N-Gram order (counting does not depend on k).
        model = NGramSentimentModel(n=n, k=1.0, threshold=args.threshold)
        model.train(train_examples)
        print(f"\nn={n}: trained (vocab={model.vocab_size:,}); sweeping add-k ...")
        for k in ADD_K_VALUES:
            model.k = k  # the only thing classify() needs
            acc_train = evaluate(model, train_eval, "train").accuracy
            m_a = evaluate(model, eval_a, args.eval_a_name)
            m_b = evaluate(model, eval_b, args.eval_b_name)
            gap = acc_train - m_a.accuracy
            rows.append({
                "n": n, "add_k": k,
                "acc_train": round(acc_train, 4),
                "acc_test_a": round(m_a.accuracy, 4),
                "f1_test_a": round(m_a.macro_f1, 4),
                "acc_test_b": round(m_b.accuracy, 4),
                "f1_test_b": round(m_b.macro_f1, 4),
                "train_minus_test_a": round(gap, 4),
            })
            print(f"  k={k:<7} train={acc_train:.3f}  "
                  f"{args.eval_a_name}={m_a.accuracy:.3f}  "
                  f"{args.eval_b_name}={m_b.accuracy:.3f}  gap={gap:+.3f}")

    csv_path = args.out / "sweep.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote {csv_path}")

    _plot(rows, args, args.out / "figures" / "bias_variance.png")
    return 0


def _plot(rows: list[dict], args, png_path: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  [warn] matplotlib not installed; skipping figure", file=sys.stderr)
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Panel A (the money shot): capacity dial. At a fixed, sensible k, sweep the
    # N-Gram order and plot train vs test accuracy. Train climbs toward 1.0 while
    # test falls = the textbook overfitting signature (variance exploding).
    k_focus = 1.0
    by_n = [r for r in rows if r["add_k"] == k_focus]
    by_n.sort(key=lambda r: r["n"])
    ns = [r["n"] for r in by_n]
    tr = [r["acc_train"] for r in by_n]
    te_a = [r["acc_test_a"] for r in by_n]
    te_b = [r["acc_test_b"] for r in by_n]
    ax1.plot(ns, tr, "o-", color="#C44E52", linewidth=2,
             label="train accuracy (data it has seen)")
    ax1.plot(ns, te_b, "s-", color="#4C72B0", linewidth=2,
             label=f"test accuracy ({args.eval_b_name})")
    ax1.plot(ns, te_a, "^--", color="#6FA8DC", linewidth=1.5,
             label=f"test accuracy ({args.eval_a_name})")
    ax1.fill_between(ns, te_b, tr, color="#C44E52", alpha=0.10)
    for x, hi, lo in zip(ns, tr, te_b):
        ax1.annotate(f"gap\n{hi - lo:+.2f}", (x, (hi + lo) / 2),
                     ha="center", va="center", fontsize=8, color="#8B0000")
    ax1.set_xticks(ns)
    ax1.set_xticklabels([f"n={n}\n{'unigram' if n==1 else 'bigram' if n==2 else 'trigram'}"
                         for n in ns])
    ax1.set_xlabel(f"N-Gram order = model capacity  (add-k fixed at {k_focus})")
    ax1.set_ylabel("accuracy")
    ax1.set_ylim(0.35, 1.02)
    ax1.set_title("Capacity dial (the overfitting picture):\n"
                  "more capacity → memorises training, generalises worse")
    ax1.legend(loc="center left", fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel B: the regularization dial. For the chosen bigram, sweep add-k and
    # show train vs test - the finer knob once capacity is fixed.
    n_focus = 2
    sub = [r for r in rows if r["n"] == n_focus]
    sub.sort(key=lambda r: r["add_k"])
    ks = [r["add_k"] for r in sub]
    ax2.plot(ks, [r["acc_train"] for r in sub], "o-", color="#C44E52",
             label="train accuracy")
    ax2.plot(ks, [r["acc_test_b"] for r in sub], "s-", color="#4C72B0",
             label=f"test accuracy ({args.eval_b_name})")
    ax2.set_xscale("log")
    ax2.set_xlabel("add-k smoothing  (small = less regularization  →  large = more)")
    ax2.set_ylabel("accuracy")
    ax2.set_ylim(0.35, 1.02)
    ax2.set_title(f"Regularization dial: n={n_focus} bigram\n"
                  "smoothing is the finer knob once capacity is set")
    ax2.legend(loc="center left", fontsize=9)
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Assessment 1 N-Gram model - regularization in action",
                 fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(png_path, dpi=120)
    plt.close(fig)
    print(f"Wrote {png_path}")


if __name__ == "__main__":
    raise SystemExit(main())
