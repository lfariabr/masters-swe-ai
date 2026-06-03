"""Download and normalise the two DLE602 Assessment 1 Twitter sentiment datasets.

Both datasets are among the five used by Zhao, Gui & Zhang (2018) and are the only
two that ship as *full tweet text* (no Twitter-API hydration, no login):

  * Stanford Twitter Sentiment (Sentiment140) -- training corpus + STS-Test test set.
      https://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip   (~81 MB)
  * STS-Gold (Stanford Twitter Sentiment Gold) -- 2034 tweets.
      https://raw.githubusercontent.com/pollockj/world_mood/master/sts_gold_v03/sts_gold_tweet.csv

Raw downloads land in dataset/_raw/ (git-ignored). The script writes three tidy,
UTF-8, ``label,text`` CSVs that ARE committed so the project clones-and-runs:

  * sentiment140_train_sample.csv  balanced sample (default 40k neg + 40k pos)
  * sts_test.csv                   498 tweets, 3 classes (neg / neutral / pos)
  * sts_gold.csv                   2034 tweets, 2 classes (neg / pos)

How to run:
    python dataset/download.py            # download + build everything (idempotent)
    python dataset/download.py --force     # re-download and rebuild
    python dataset/download.py --per-class 25000   # smaller training sample

How to test:
    Re-run; it skips work already done. Confirm the three CSVs exist with the
    row counts printed in the summary (~80000 / 498 / 2034).
"""
from __future__ import annotations

import argparse
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "_raw"

SENTIMENT140_ZIP_URL = "https://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip"
STS_GOLD_URL = (
    "https://raw.githubusercontent.com/pollockj/world_mood/master/"
    "sts_gold_v03/sts_gold_tweet.csv"
)

# Sentiment140 polarity codes -> human-readable label.
POLARITY_MAP = {0: "negative", 2: "neutral", 4: "positive"}
SENTIMENT140_COLS = ["polarity", "id", "date", "query", "user", "text"]

TRAIN_CSV = "training.1600000.processed.noemoticon.csv"
TEST_CSV = "testdata.manual.2009.06.14.csv"

SEED = 42


def _download(url: str, dest: Path) -> Path:
    """Download ``url`` to ``dest`` unless it already exists."""
    if dest.exists():
        print(f"  [skip] {dest.name} already present ({dest.stat().st_size:,} bytes)")
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  [get ] {url}")
    with urllib.request.urlopen(url, timeout=120) as resp:  # noqa: S310 (trusted URLs)
        data = resp.read()
    dest.write_bytes(data)
    print(f"  [save] {dest.name} ({len(data):,} bytes)")
    return dest


def build_sentiment140(per_class: int, force: bool) -> None:
    """Download the Stanford zip and write the training sample + STS-Test."""
    zip_path = RAW / "trainingandtestdata.zip"
    _download(SENTIMENT140_ZIP_URL, zip_path)

    with zipfile.ZipFile(zip_path) as zf:
        train_bytes = zf.read(TRAIN_CSV)
        test_bytes = zf.read(TEST_CSV)

    # --- STS-Test: keep all 498 rows (includes the neutral class) ---
    test_out = HERE / "sts_test.csv"
    if force or not test_out.exists():
        test_df = pd.read_csv(
            io.BytesIO(test_bytes), encoding="latin-1", header=None,
            names=SENTIMENT140_COLS,
        )
        _write_labelled(test_df, test_out)
    else:
        print(f"  [skip] {test_out.name} already present")

    # --- Training sample: balanced per-class draw from the 1.6M corpus ---
    train_out = HERE / "sentiment140_train_sample.csv"
    if force or not train_out.exists():
        train_df = pd.read_csv(
            io.BytesIO(train_bytes), encoding="latin-1", header=None,
            names=SENTIMENT140_COLS,
        )
        parts = []
        for code in (0, 4):  # 0=neg, 4=pos (training corpus has no neutral)
            grp = train_df[train_df["polarity"] == code]
            parts.append(grp.sample(n=min(per_class, len(grp)), random_state=SEED))
        # concat then shuffle so the two classes interleave in the written file
        sampled = pd.concat(parts).sample(frac=1.0, random_state=SEED)
        _write_labelled(sampled, train_out)
    else:
        print(f"  [skip] {train_out.name} already present")


def build_sts_gold(force: bool) -> None:
    """Download STS-Gold and write the normalised label,text CSV."""
    raw_path = RAW / "sts_gold_tweet.csv"
    _download(STS_GOLD_URL, raw_path)

    out = HERE / "sts_gold.csv"
    if not force and out.exists():
        print(f"  [skip] {out.name} already present")
        return
    # STS-Gold is ';'-separated and quoted: "id";"polarity";"tweet"
    df = pd.read_csv(raw_path, sep=";", quotechar='"')
    df = df.rename(columns={"tweet": "text"})
    _write_labelled(df, out)


def _write_labelled(df: pd.DataFrame, dest: Path) -> None:
    """Map polarity codes to labels and write a tidy ``label,text`` CSV."""
    df = df.copy()
    df["label"] = df["polarity"].map(POLARITY_MAP)
    df = df.dropna(subset=["label", "text"])
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"] != ""]
    out = df[["label", "text"]]
    out.to_csv(dest, index=False, encoding="utf-8")
    dist = out["label"].value_counts().to_dict()
    print(f"  [write] {dest.name}: {len(out):,} rows  {dist}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--per-class", type=int, default=40000,
        help="tweets per class in the training sample (default 40000)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="rebuild the normalised CSVs even if they already exist",
    )
    args = parser.parse_args(argv)

    print("DLE602 Assessment 1 - dataset download")
    print("Sentiment140 (training sample + STS-Test):")
    build_sentiment140(args.per_class, args.force)
    print("STS-Gold:")
    build_sts_gold(args.force)
    print("Done. Raw downloads kept in dataset/_raw/ (git-ignored).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
