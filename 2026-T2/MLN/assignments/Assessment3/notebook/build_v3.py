"""Assemble MLN601FariaLuisBrief3v3.ipynb from the cell modules plus the reusable v2 EDA cells.

Run:  python3 build_v3.py
Then: jupyter nbconvert --to notebook --execute --inplace MLN601FariaLuisBrief3v3.ipynb
"""
import json
from pathlib import Path

from nb_cells_a import CELLS_A_HEAD, CELLS_A_TAIL
from nb_cells_b import CELLS_B
from nb_cells_c import CELLS_C

HERE = Path(__file__).parent
V2 = HERE / "MLN601FariaLuisBrief3v2.ipynb"
V3 = HERE / "MLN601FariaLuisBrief3v3.ipynb"

# The exploratory cells carry Luis's own readings of each plot and are kept verbatim,
# with figure filenames re-pointed from v2 to v3.
EDA_RANGE = range(10, 24)


def to_cell(kind, source):
    cell = {"cell_type": kind, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def main():
    v2 = json.loads(V2.read_text())
    eda = []
    for i in EDA_RANGE:
        c = json.loads(json.dumps(v2["cells"][i]))       # deep copy
        c["source"] = [line.replace("v2_", "v3_") for line in c["source"]]
        c.pop("id", None)
        if c["cell_type"] == "code":
            c["outputs"], c["execution_count"] = [], None
        eda.append(c)

    cells = ([to_cell(k, s) for k, s in CELLS_A_HEAD]
             + eda
             + [to_cell(k, s) for k, s in CELLS_A_TAIL]
             + [to_cell(k, s) for k, s in CELLS_B]
             + [to_cell(k, s) for k, s in CELLS_C])

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    V3.write_text(json.dumps(nb, indent=1))
    print(f"Wrote {V3.name}: {len(cells)} cells "
          f"({sum(c['cell_type'] == 'code' for c in cells)} code, "
          f"{sum(c['cell_type'] == 'markdown' for c in cells)} markdown)")


if __name__ == "__main__":
    main()
