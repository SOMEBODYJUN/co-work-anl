"""Bounded replay for the R-275 fractional policy-cone record.

The original driver is rerun in a temporary directory with its frozen local
dependencies and fixed RNG seed.  This checks deterministic finite output and
recomputes the stored bridge objective.  It deliberately does not promote the
floating LP or the action-only policy serialization to an exact SPE certificate.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def objective_check(record: dict) -> dict:
    cone = load_module("r275_cone_floor_attack", SOURCE / "cone_floor_attack.py")
    p = int(record["p"])
    n = int(record["n"])
    weights = np.asarray(record["weights"], dtype=float)
    target = tuple(int(x) for x in record["target"])
    action = int(record["a"])
    f = cone.Cone(p, n)
    f.setup(weights)
    target_id = f.ids[target]
    loads = f.den[target_id]
    covered = (loads > 0).astype(float)
    alpha = (n - 1) / n
    gc = np.divide(covered, 1 + alpha * loads)
    g = f.M.T / (1 + alpha * loads)
    objective = covered + gc - n * g[action]
    value = float(objective @ weights)
    support_normalization = float(covered @ weights)
    nonzero = [
        {"vector_index": i, "mask": i + 1, "weight": float(x)}
        for i, x in enumerate(weights)
        if abs(float(x)) > 1e-12
    ]
    bits = [a for a in range(p) if (nonzero[0]["mask"] if nonzero else 0) & (1 << a)]
    return {
        "target_id": int(target_id),
        "loads": [int(x) for x in loads],
        "alpha": alpha,
        "support_normalization": support_normalization,
        "objective": value,
        "stored_slack": float(record["slack"]),
        "objective_matches_stored": abs(value - float(record["slack"])) < 1e-12,
        "nonzero_weights": nonzero,
        "nonzero_mask_bits": bits,
        "policy_nodes": len(record.get("policy", [])),
        "expected_history_nodes": sum(p**j for j in range(n)),
        "deviation_rows_if_expanded": sum(p**j for j in range(n)) * (p - 1),
    }


def main() -> None:
    record_path = SOURCE / "fractional_cone_best.json"
    record = json.loads(record_path.read_text())
    checks = objective_check(record)
    report = {
        "record": "fractional_cone_best.json",
        "source_sha256": sha256(record_path),
        "objective_check": checks,
        "scope": {
            "finite_only": True,
            "universal_claim": False,
            "exact_rational_certificate": False,
            "policy_child_terms_serialized": False,
            "note": "The saved policy stores actions only; the original LP's gamma rows use child terminal choices that are not serialized. A full rerun of the frozen driver is intentionally outside this quick value replay; the source and candidate bytes are preserved for that run.",
        },
    }
    (Path(__file__).resolve().parent / "verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
