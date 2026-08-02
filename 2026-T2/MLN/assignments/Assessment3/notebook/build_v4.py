"""Assemble the v4 MLN601 Assessment 3 notebook from versioned cell modules.

Run from this directory:
    python3 build_v4.py
    jupyter nbconvert --to notebook --execute --inplace MLN601FariaLuisBrief3v4.ipynb
"""

import json
from pathlib import Path

from nb_cells_v4_a import CELLS_A
from nb_cells_v4_b import CELLS_B
from nb_cells_v4_c import CELLS_C

HERE = Path(__file__).parent
TARGET = HERE / "MLN601FariaLuisBrief3v4.ipynb"


def to_cell(kind, source, index):
    cell = {"cell_type": kind, "id": f"v4-cell-{index:03d}", "metadata": {},
            "source": source.splitlines(keepends=True)}
    if kind == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def main():
    cells = [to_cell(kind, source, index)
             for index, (kind, source) in enumerate(CELLS_A + CELLS_B + CELLS_C)]
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


if __name__ == "__main__":
    main()
