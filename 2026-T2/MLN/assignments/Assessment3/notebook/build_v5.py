"""Assemble and export the v5 MLN601 Assessment 3 notebook.

Three ordered steps, run from this directory. They are separate commands on purpose: a rebuild
writes cells with empty outputs, so folding it into --export would discard a completed run.

    1. python3 build_v5.py
    2. JUPYTER_PATH=/opt/homebrew/share/jupyter jupyter nbconvert \
           --to notebook --execute --inplace MLN601FariaLuisBrief3v5.ipynb
    3. python3 build_v5.py --export
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

from nb_cells_v5 import CELLS

HERE = Path(__file__).parent
STEM = "MLN601FariaLuisBrief3v5"
TARGET = HERE / f"{STEM}.ipynb"
EXPORT_DIR = HERE.parent / "exports"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# The exported HTML is sized for a screen, where a wide table simply scrolls. Print has no
# scrollbar, so anything wider than the page is silently clipped: the fix is to let dataframe
# cells wrap, shrink their font, and reclaim the horizontal space taken by execution prompts.
PRINT_CSS = """
<style>
  body, div.output_area pre, pre, code { font-size: 12px !important; }
  div.jp-Cell { page-break-inside: avoid; }
  table { font-size: 11px !important; }
  @page { size: A4; margin: 12mm; }

  /* Long code lines used to run off the right edge and be clipped. Wrapping them keeps the
     cell inside the page instead of widening the whole layout, which is what pushed the
     prompt column across the page when overflow was made visible instead. */
  .jp-InputArea-editor pre, .highlight pre, div.input_area pre, .jp-CodeMirrorEditor pre {
    white-space: pre-wrap !important;
    overflow-wrap: break-word !important;
  }

  /* Wide dataframes: shrink and allow cells to wrap so the last column survives the page. */
  table.dataframe { font-size: 8px !important; }
  table.dataframe th, table.dataframe td {
    padding: 1px 3px !important;
    white-space: normal !important;
    overflow-wrap: break-word !important;   /* never "anywhere": it splits ACTUAL into ACTUA/L */
  }
</style>
"""


def to_cell(kind: str, source: str, index: int) -> dict[str, Any]:
    cell = {"cell_type": kind, "id": f"v5-cell-{index:03d}", "metadata": {},
            "source": source.splitlines(keepends=True)}
    if kind == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def build() -> None:
    cells = [to_cell(kind, source, index) for index, (kind, source) in enumerate(CELLS)]
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    TARGET.write_text(json.dumps(notebook, indent=1))
    print(f"Wrote {TARGET.name}: {len(cells)} cells "
          f"({sum(c['cell_type'] == 'code' for c in cells)} code, "
          f"{sum(c['cell_type'] == 'markdown' for c in cells)} markdown)")


def run(command: Sequence[str]) -> None:
    print("$", " ".join(str(part) for part in command))
    subprocess.run(command, check=True, cwd=HERE)


def require_executed() -> None:
    """Refuse to export a notebook that has not been run.

    build() writes cells with empty outputs by design. Without this check, running --export
    straight after a rebuild would publish a report with no figures, tables or numbers in it,
    and would exit zero while doing so.
    """
    notebook = json.loads(TARGET.read_text())
    code = [c for c in notebook["cells"] if c["cell_type"] == "code"]
    unexecuted = [i for i, c in enumerate(code, 1) if c.get("execution_count") is None]
    failed = [i for i, c in enumerate(code, 1)
              if any(o.get("output_type") == "error" for o in c.get("outputs", []))]
    if unexecuted or failed:
        print(f"Refusing to export {TARGET.name}.", file=sys.stderr)
        if unexecuted:
            print(f"  {len(unexecuted)} of {len(code)} code cells have no execution_count "
                  f"(first: cell {unexecuted[0]}). Run the execute step first.", file=sys.stderr)
        if failed:
            print(f"  code cells with error output: {failed}", file=sys.stderr)
        raise SystemExit(1)
    print(f"{TARGET.name}: {len(code)} code cells executed, no error outputs.")


def export() -> None:
    require_executed()
    env = {**os.environ, "JUPYTER_PATH": "/opt/homebrew/share/jupyter"}
    EXPORT_DIR.mkdir(exist_ok=True)

    subprocess.run(["jupyter", "nbconvert", "--to", "html",
                    "--output-dir", str(EXPORT_DIR), TARGET.name],
                   check=True, cwd=HERE, env=env)

    html_path = (EXPORT_DIR / f"{STEM}.html").resolve()
    html = html_path.read_text()
    if "@page { size: A4" not in html:
        html = html.replace("</head>", f"{PRINT_CSS}</head>", 1)
        html_path.write_text(html)

    # as_uri() guarantees an absolute, percent-encoded URI, which Chrome requires.
    run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=20000",
         f"--print-to-pdf={(EXPORT_DIR / f'{STEM}.pdf').resolve()}",
         html_path.as_uri()])

    subprocess.run(["jupyter", "nbconvert", "--to", "script",
                    "--output-dir", str(EXPORT_DIR), TARGET.name],
                   check=True, cwd=HERE, env=env)

    # nbconvert emits captured images as one enormous base64 comment line; strip it so the
    # submitted .txt stays a readable listing of the code.
    txt_path = EXPORT_DIR / f"{STEM}.txt"
    script_path = EXPORT_DIR / f"{STEM}.py"
    if script_path.exists():
        script_path.replace(txt_path)
    kept = [line.rstrip() for line in txt_path.read_text().splitlines()
            if not re.match(r"^#?\s*(iVBOR|data:image|[A-Za-z0-9+/]{200,}=*$)", line.strip())]
    txt_path.write_text("\n".join(kept) + "\n")

    submission = HERE.parent / "submission"
    for suffix in ("ipynb", "pdf", "txt"):
        source = TARGET if suffix == "ipynb" else EXPORT_DIR / f"{STEM}.{suffix}"
        shutil.copyfile(source, submission / f"MLN601FariaLuisBrief3.{suffix}")
    print(f"Exported and copied into {submission}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--export", action="store_true",
                        help="render HTML/PDF/txt from the ALREADY EXECUTED notebook and "
                             "refresh submission/; does not rebuild, which would discard outputs")
    args = parser.parse_args()
    if args.export:
        export()
    else:
        build()
