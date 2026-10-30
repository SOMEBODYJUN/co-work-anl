#!/usr/bin/env python3
"""Replay all original main computations while preserving the frozen output."""
from pathlib import Path
import json
import runpy
root = Path(__file__).resolve().parent
module = runpy.run_path(str(root / "original/tests/audits/weighted_congestion/quadratic_source/verify.py"))
report = {"claim_id": "WC-R1-SOURCE-D2-ENVELOPE v1", "date_utc": "2026-10-14",
          "exact": module["exact_checks"](), "rational_grid": module["rational_grid"](),
          "numerical": module["numerical_exploration"]()}
(root / "quadratic-source-replay.json").write_text(json.dumps(report, indent=2) + "\n")
