"""DLE602 Assessment 1 - Twitter sentiment analysis with an N-Gram language model.

This is the required programming deliverable: a transparent, probabilistic N-Gram
(default bigram) sentiment classifier, implementing the model described by
Zhao, Gui & Zhang (2018) WITHOUT the deep CNN. The same model, preprocessing and
decision rule are applied to two of the paper's five datasets so their outcomes
can be compared (STS-Test, which has a neutral class, and STS-Gold, which does not).

Method
------
1. Train one positive and one negative N-Gram language model from labelled tweets
   (Sentiment140 training sample; this corpus only has positive/negative labels).
2. For each test tweet, build its N-Grams and, per N-Gram, compare the smoothed
   conditional log-probability under the positive vs the negative model.
3. Apply the brief's "one fourth" rule: classify positive if >= 25% of the tweet's
   N-Grams are positive (and outnumber the negative ones), negative by the mirror
   rule, otherwise neutral.

How to run
----------
    # one-off: fetch the datasets first (writes dataset/*.csv)
    python dataset/download.py

    python code/dle602_sentiment_ngram.py \
        --train dataset/sentiment140_train_sample.csv \
        --eval-a dataset/sts_test.csv --eval-a-name STS-Test \
        --eval-b dataset/sts_gold.csv --eval-b-name STS-Gold \
        --ngram 2 --out outputs

How to test
-----------
    python -m py_compile code/dle602_sentiment_ngram.py
    # then run the command above; it writes outputs/comparison_summary.csv and
    # figures, and prints the metrics table. Re-running gives identical numbers
    # (training is pure counting; the only randomness lives in dataset sampling).
"""
from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

# Output classes. Models are trained on positive/negative only; "neutral" is an
# output decision produced by the 25% threshold, never a trained language model.
LABELS = ["negative", "neutral", "positive"]
TRAIN_LABELS = ("negative", "positive")

BOUNDARY_START = "<s>"
BOUNDARY_END = "</s>"
UNK = "<unk>"

# Preprocessing patterns (Twitter-specific normalisation, per the report skeleton).
URL_RE = re.compile(r"https?://\S+|www\.\S+")
MENTION_RE = re.compile(r"@\w+")
# Keep word characters, the hashtag body, and sentiment-bearing punctuation (! ?).
TOKEN_RE = re.compile(r"[a-z0-9']+|[!?]")


@dataclass
class TweetExample:
    text: str
    label: str


# --------------------------------------------------------------------------- #
# Data loading and preprocessing
# --------------------------------------------------------------------------- #
def load_dataset(path: Path) -> list[TweetExample]:
    """Load a tidy ``label,text`` CSV produced by ``dataset/download.py``."""
    examples: list[TweetExample] = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or "text" not in reader.fieldnames:
            raise ValueError(f"{path} must have 'label' and 'text' columns")
        for row in reader:
            label = (row.get("label") or "").strip().lower()
            text = (row.get("text") or "").strip()
            if text:
                examples.append(TweetExample(text=text, label=label))
    if not examples:
        raise ValueError(f"No usable rows found in {path}")
    return examples


def preprocess(text: str) -> list[str]:
    """Normalise tweet text and return tokens.

    Lowercase; replace URLs and @mentions with placeholder tokens so their
    presence is a signal but the exact value is not; strip the leading '#' from
    hashtags but keep the tag word; keep '!' and '?' as sentiment cues.
    """
    text = text.lower()
    text = URL_RE.sub(" <url> ", text)
    text = MENTION_RE.sub(" <user> ", text)
    text = text.replace("#", " ")  # keep hashtag word, drop the symbol
    # Re-protect the placeholder tokens that the tokenizer would otherwise split.
    tokens: list[str] = []
    for chunk in text.split():
        if chunk in ("<url>", "<user>"):
            tokens.append(chunk)
        else:
            tokens.extend(TOKEN_RE.findall(chunk))
    return tokens


def ngrams(tokens: list[str], n: int) -> list[tuple[tuple[str, ...], str]]:
    """Return (context, word) pairs with boundary padding.

    For ``n == 2`` and tokens ``[a, b]`` this yields ``[((<s>,), a), ((a,), b),
    ((b,), </s>)]``. The empty context for ``n == 1`` makes the unigram case fall
    out of the same code path.
    """
    padded = [BOUNDARY_START] * (n - 1) + tokens + [BOUNDARY_END]
    pairs: list[tuple[tuple[str, ...], str]] = []
    for i in range(n - 1, len(padded)):
        context = tuple(padded[i - n + 1 : i])
        pairs.append((context, padded[i]))
    return pairs


# --------------------------------------------------------------------------- #
# Model
# --------------------------------------------------------------------------- #
@dataclass
class Prediction:
    label: str
    pos_hits: int
    neg_hits: int
    total: int


class NGramSentimentModel:
    """Add-k smoothed N-Gram language models for positive and negative classes."""

    def __init__(self, n: int = 2, k: float = 1.0, threshold: float = 0.25,
                 margin: float = 0.0) -> None:
        self.n = n
        self.k = k
        self.threshold = threshold
        self.margin = margin
        self.vocab: set[str] = set()
        self.vocab_size = 0
        self.ngram_counts: dict[str, Counter] = {c: Counter() for c in TRAIN_LABELS}
        self.context_counts: dict[str, Counter] = {c: Counter() for c in TRAIN_LABELS}

    def train(self, examples: list[TweetExample]) -> None:
        self.vocab = {UNK, BOUNDARY_START, BOUNDARY_END}
        tokenised: list[tuple[str, list[str]]] = []
        for ex in examples:
            tokens = preprocess(ex.text)
            tokenised.append((ex.label, tokens))
            self.vocab.update(tokens)
        self.vocab_size = len(self.vocab)
        for label, tokens in tokenised:
            if label not in self.ngram_counts:  # ignore any non pos/neg rows
                continue
            for context, word in ngrams(tokens, self.n):
                self.ngram_counts[label][(context, word)] += 1
                self.context_counts[label][context] += 1

    def _logprob(self, cls: str, context: tuple[str, ...], word: str) -> float:
        """Smoothed conditional log-probability P_cls(word | context)."""
        context = tuple(t if t in self.vocab else UNK for t in context)
        word = word if word in self.vocab else UNK
        ngram_count = self.ngram_counts[cls][(context, word)]
        context_count = self.context_counts[cls][context]
        numerator = ngram_count + self.k
        denominator = context_count + self.k * self.vocab_size
        return math.log(numerator / denominator)

    def classify(self, tokens: list[str]) -> Prediction:
        pairs = ngrams(tokens, self.n)
        total = len(pairs)
        pos_hits = neg_hits = 0
        for context, word in pairs:
            lp_pos = self._logprob("positive", context, word)
            lp_neg = self._logprob("negative", context, word)
            if lp_pos > lp_neg + self.margin:
                pos_hits += 1
            elif lp_neg > lp_pos + self.margin:
                neg_hits += 1
        if total == 0:
            return Prediction("neutral", 0, 0, 0)
        pos_ratio = pos_hits / total
        neg_ratio = neg_hits / total
        if pos_ratio >= self.threshold and pos_hits > neg_hits:
            label = "positive"
        elif neg_ratio >= self.threshold and neg_hits > pos_hits:
            label = "negative"
        else:
            label = "neutral"
        return Prediction(label, pos_hits, neg_hits, total)


# --------------------------------------------------------------------------- #
# Evaluation
# --------------------------------------------------------------------------- #
@dataclass
class Metrics:
    name: str
    n_records: int
    true_counts: Counter
    pred_counts: Counter
    confusion: dict[str, Counter]
    accuracy: float
    macro_f1: float
    errors: list[tuple[str, str, str]]  # (true, pred, text) samples


def evaluate(model: NGramSentimentModel, examples: list[TweetExample],
             name: str, n_errors: int = 5) -> Metrics:
    confusion = {t: Counter() for t in LABELS}
    true_counts: Counter = Counter()
    pred_counts: Counter = Counter()
    correct = 0
    errors: list[tuple[str, str, str]] = []
    for ex in examples:
        pred = model.classify(preprocess(ex.text)).label
        true_counts[ex.label] += 1
        pred_counts[pred] += 1
        confusion[ex.label][pred] += 1
        if pred == ex.label:
            correct += 1
        elif len(errors) < n_errors:
            errors.append((ex.label, pred, ex.text))
    n = len(examples)
    accuracy = correct / n if n else 0.0

    # Macro-F1 across the classes that actually appear in the ground truth.
    f1s: list[float] = []
    for label in LABELS:
        if true_counts[label] == 0:
            continue
        tp = confusion[label][label]
        predicted = sum(confusion[t][label] for t in LABELS)
        precision = tp / predicted if predicted else 0.0
        recall = tp / true_counts[label]
        f1 = (2 * precision * recall / (precision + recall)
              if precision + recall else 0.0)
        f1s.append(f1)
    macro_f1 = sum(f1s) / len(f1s) if f1s else 0.0
    return Metrics(name, n, true_counts, pred_counts, confusion, accuracy,
                   macro_f1, errors)


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def _row(metric: str, *values: object) -> list[str]:
    return [metric, *[str(v) for v in values]]


def write_comparison(metrics: list[Metrics], out_dir: Path) -> Path:
    """Side-by-side metrics CSV across the evaluated datasets."""
    path = out_dir / "comparison_summary.csv"
    header = ["metric", *[m.name for m in metrics]]
    rows = [
        _row("records", *[m.n_records for m in metrics]),
        _row("accuracy", *[f"{m.accuracy:.4f}" for m in metrics]),
        _row("macro_f1", *[f"{m.macro_f1:.4f}" for m in metrics]),
    ]
    for label in LABELS:
        rows.append(_row(f"true_{label}", *[m.true_counts[label] for m in metrics]))
    for label in LABELS:
        rows.append(_row(f"pred_{label}", *[m.pred_counts[label] for m in metrics]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)
    return path


def write_dataset_metrics(metrics: Metrics, out_dir: Path) -> Path:
    """Per-dataset metrics + confusion matrix CSV."""
    slug = metrics.name.lower().replace("-", "_")
    path = out_dir / f"{slug}_metrics.csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["section", "key", "value"])
        writer.writerow(["summary", "records", metrics.n_records])
        writer.writerow(["summary", "accuracy", f"{metrics.accuracy:.4f}"])
        writer.writerow(["summary", "macro_f1", f"{metrics.macro_f1:.4f}"])
        for label in LABELS:
            writer.writerow(["true_count", label, metrics.true_counts[label]])
        for label in LABELS:
            writer.writerow(["pred_count", label, metrics.pred_counts[label]])
        for true_label in LABELS:
            for pred_label in LABELS:
                writer.writerow([
                    "confusion", f"true={true_label}|pred={pred_label}",
                    metrics.confusion[true_label][pred_label],
                ])
    return path


def write_error_examples(metrics: list[Metrics], out_dir: Path) -> Path:
    path = out_dir / "error_examples.txt"
    with open(path, "w", encoding="utf-8") as fh:
        for m in metrics:
            fh.write(f"# {m.name} - sample misclassifications\n")
            for true_label, pred_label, text in m.errors:
                fh.write(f"  true={true_label:<8} pred={pred_label:<8} | {text}\n")
            fh.write("\n")
    return path


def plot_distributions(metrics: list[Metrics], out_dir: Path) -> None:
    """Grouped bar charts of true vs predicted class counts (per dataset)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("  [warn] matplotlib not installed; skipping figures", file=sys.stderr)
        return

    fig, axes = plt.subplots(1, len(metrics), figsize=(6 * len(metrics), 4.5))
    if len(metrics) == 1:
        axes = [axes]
    x = range(len(LABELS))
    for ax, m in zip(axes, metrics):
        true_vals = [m.true_counts[c] for c in LABELS]
        pred_vals = [m.pred_counts[c] for c in LABELS]
        ax.bar([i - 0.2 for i in x], true_vals, width=0.4, label="true",
               color="#4C72B0")
        ax.bar([i + 0.2 for i in x], pred_vals, width=0.4, label="predicted",
               color="#DD8452")
        ax.set_xticks(list(x))
        ax.set_xticklabels(LABELS)
        ax.set_title(f"{m.name}  (acc={m.accuracy:.2f})")
        ax.set_ylabel("tweets")
        ax.legend()
    fig.suptitle("True vs predicted sentiment distribution")
    fig.tight_layout()
    fig.savefig(out_dir / "figures" / "sentiment_distribution.png", dpi=120)
    plt.close(fig)

    for m in metrics:
        _plot_confusion(m, out_dir)


def _plot_confusion(metrics: Metrics, out_dir: Path) -> None:
    import matplotlib.pyplot as plt

    matrix = [[metrics.confusion[t][p] for p in LABELS] for t in LABELS]
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    im = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks(range(len(LABELS)), LABELS)
    ax.set_yticks(range(len(LABELS)), LABELS)
    ax.set_xlabel("predicted")
    ax.set_ylabel("true")
    ax.set_title(f"{metrics.name} confusion matrix")
    for i in range(len(LABELS)):
        for j in range(len(LABELS)):
            ax.text(j, i, matrix[i][j], ha="center", va="center",
                    color="black", fontsize=11)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    slug = metrics.name.lower().replace("-", "_")
    fig.savefig(out_dir / "figures" / f"confusion_{slug}.png", dpi=120)
    plt.close(fig)


def print_report(metrics: list[Metrics]) -> None:
    print("\n=== Results ===")
    header = f"{'metric':<16}" + "".join(f"{m.name:>14}" for m in metrics)
    print(header)
    print(f"{'records':<16}" + "".join(f"{m.n_records:>14}" for m in metrics))
    print(f"{'accuracy':<16}" + "".join(f"{m.accuracy:>14.4f}" for m in metrics))
    print(f"{'macro_f1':<16}" + "".join(f"{m.macro_f1:>14.4f}" for m in metrics))
    for label in LABELS:
        print(f"{'true_' + label:<16}"
              + "".join(f"{m.true_counts[label]:>14}" for m in metrics))
    for label in LABELS:
        print(f"{'pred_' + label:<16}"
              + "".join(f"{m.pred_counts[label]:>14}" for m in metrics))


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_model(train_path: Path, n: int, k: float, threshold: float,
                margin: float) -> NGramSentimentModel:
    train_examples = load_dataset(train_path)
    model = NGramSentimentModel(n=n, k=k, threshold=threshold, margin=margin)
    model.train(train_examples)
    print(f"Trained {n}-gram model on {len(train_examples):,} tweets "
          f"(vocab={model.vocab_size:,}, add-k={k}).")
    return model


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--train", type=Path,
                        default=Path("dataset/sentiment140_train_sample.csv"))
    parser.add_argument("--eval-a", type=Path, default=Path("dataset/sts_test.csv"))
    parser.add_argument("--eval-a-name", default="STS-Test")
    parser.add_argument("--eval-b", type=Path, default=Path("dataset/sts_gold.csv"))
    parser.add_argument("--eval-b-name", default="STS-Gold")
    parser.add_argument("--ngram", type=int, default=2,
                        help="N-Gram order; same value used for both datasets")
    parser.add_argument("--add-k", type=float, default=1.0,
                        help="add-k smoothing constant")
    parser.add_argument("--threshold", type=float, default=0.25,
                        help="the brief's 'one fourth' decision threshold")
    parser.add_argument("--margin", type=float, default=0.0,
                        help="log-prob margin before an N-Gram counts as pos/neg")
    parser.add_argument("--out", type=Path, default=Path("outputs"))
    args = parser.parse_args(argv)

    (args.out / "figures").mkdir(parents=True, exist_ok=True)

    model = build_model(args.train, args.ngram, args.add_k, args.threshold,
                        args.margin)

    metrics = []
    for path, name in ((args.eval_a, args.eval_a_name),
                       (args.eval_b, args.eval_b_name)):
        examples = load_dataset(path)
        metrics.append(evaluate(model, examples, name))

    print_report(metrics)
    write_comparison(metrics, args.out)
    for m in metrics:
        write_dataset_metrics(m, args.out)
    write_error_examples(metrics, args.out)
    plot_distributions(metrics, args.out)
    print(f"\nWrote metrics + figures to {args.out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
