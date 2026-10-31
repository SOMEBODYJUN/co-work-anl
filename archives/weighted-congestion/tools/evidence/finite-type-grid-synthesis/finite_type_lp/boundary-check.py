"""Reproduce the ten diagnostic calls recorded in boundary-check.json.

This is not a second replay of the sixty-case original main program.
The source is loaded without running its __main__ block and is not modified.
"""
from pathlib import Path
import json
import platform
import runpy

import numpy
import scipy

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "sources" / "fecd3d9434b3ccc1b91b--type_count_potential_lp.py"
solve = runpy.run_path(str(SOURCE), run_name="imported")["solve"]
cases = [
    (0, 1, 2, 2), (1, 0, 2, 2), (2, 3, 1, 3),
    (2, 3, 2, 0), (2, 3, 2, 1), (1, 1, 2, 2),
    (2, 2, 2, 2), (1, 1, 2, 3), (2, 2, 2, 3),
    (0, 0, 2, 2),
]
out = {
    "purpose": "Actual calls to the unchanged solve function; edge and empty-grid boundaries only, not a second full main replay",
    "python": platform.python_version(),
    "numpy": numpy.__version__,
    "scipy": scipy.__version__,
    "cases": [],
}
for args in cases:
    try:
        out["cases"].append({"args": args, "result": solve(*args)})
    except Exception as exc:
        out["cases"].append({
            "args": args,
            "exception_type": type(exc).__name__,
            "message": str(exc),
        })
(HERE / "boundary-check.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2) + "\n"
)
