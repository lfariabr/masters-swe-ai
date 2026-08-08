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
from pathlib import Path

from nb_cells_v5 import CELLS

HERE = Path(__file__).parent
STEM = "MLN601FariaLuisBrief3v5"
TARGET = HERE / f"{STEM}.ipynb"
EXPORT_DIR = HERE.parent / "exports"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# The exported HTML defaults to a size that pushes wide tables off the printed page.
PRINT_CSS = """
<style>
  body, div.output_area pre, pre, code { font-size: 12px !important; }
  div.jp-Cell { page-break-inside: avoid; }
  table { font-size: 11px !important; }
  @page { size: A4; margin: 12mm; }
</style>
"""


def to_cell(kind, source, index):
    cell = {"cell_type": kind, "id": f"v5-cell-{index:03d}", "metadata": {},
            "source": source.splitlines(keepends=True)}
    if kind == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def build():
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


def run(command):
    print("$", " ".join(str(part) for part in command))
    subprocess.run(command, check=True, cwd=HERE)


def export():
    env = {**os.environ, "JUPYTER_PATH": "/opt/homebrew/share/jupyter"}
    EXPORT_DIR.mkdir(exist_ok=True)

    subprocess.run(["jupyter", "nbconvert", "--to", "html",
                    "--output-dir", str(EXPORT_DIR), TARGET.name],
                   check=True, cwd=HERE, env=env)

    html_path = EXPORT_DIR / f"{STEM}.html"
    html = html_path.read_text()
    if "@page { size: A4" not in html:
        html = html.replace("</head>", f"{PRINT_CSS}</head>", 1)
        html_path.write_text(html)

    run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=20000",
         f"--print-to-pdf={EXPORT_DIR / f'{STEM}.pdf'}",
         f"file://{html_path}"])

    subprocess.run(["jupyter", "nbconvert", "--to", "script",
                    "--output-dir", str(EXPORT_DIR), TARGET.name],
                   check=True, cwd=HERE, env=env)

    # nbconvert emits captured images as one enormous base64 comment line; strip it so the
    # submitted .txt stays a readable listing of the code.
    txt_path = EXPORT_DIR / f"{STEM}.txt"
    script_path = EXPORT_DIR / f"{STEM}.py"
    if script_path.exists():
        script_path.replace(txt_path)
    kept = [line for line in txt_path.read_text().splitlines()
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
