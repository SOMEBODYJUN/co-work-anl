"""Independent finite replay of the three R-275 direct_global records.

This checker intentionally reports only floating point/finite diagnostics.  It
does not assert a universal Q-CAG-HALF claim and does not replace a complete
Fraction SPE certificate.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cone_check() -> dict:
    cone_mod = load_module("cone_floor_attack", SRC / "cone_floor_attack.py")
    with (SRC / "cone_best.json").open() as fh:
        rec = json.load(fh)
    f = cone_mod.Cone(int(rec["p"]), int(rec["n"]))
    weights = np.asarray(rec["weights"], dtype=float)
    f.setup(weights)
    target = tuple(int(x) for x in rec["target"])
    target_id = f.ids[target]
    # Populate the continuation sets and their thresholds exactly as the
    # source program does before asking for a target-specific policy.
    f.R((0,) * int(rec["p"]))
    gamma, nodes = f.policy(target_id)
    stored = [(tuple(row["h"]), int(row["a"])) for row in rec["policy"]]
    generated = [(tuple(h), int(v[0])) for h, v in nodes.items()]
    support = tuple(int(x) for x in rec["support"])
    support_row = (f.M[:, support].sum(axis=1) > 0).astype(float)
    normalization = float(support_row @ weights)
    action = int(rec["a"])
    objective = float(f.coefs[target_id, action] @ weights)
    residual = gamma @ weights
    mismatch_count = sum(a != b for a, b in zip(stored, generated))
    return {
        "record": "cone_best.json",
        "p": int(rec["p"]),
        "n": int(rec["n"]),
        "target": list(target),
        "target_id": int(target_id),
        "policy_nodes": len(stored),
        "policy_reconstructed_nodes": len(generated),
        "policy_matches": stored == generated,
        "policy_mismatch_count": int(mismatch_count),
        "support": list(support),
        "support_normalization": normalization,
        "stored_ratio": float(rec["ratio"]),
        "recomputed_ratio": 2 * int(rec["n"]) * objective,
        "objective": objective,
        "gamma_rows": int(len(gamma)),
        "minimum_gamma_weighted_residual": float(residual.min()),
        "maximum_gamma_weighted_residual": float(residual.max()),
        # The stored policy is tie-sensitive: reloading the decimal JSON can
        # select a different legal tied child while preserving the same
        # target, normalization, and nonnegative cone residuals.  Equality is
        # diagnostic rather than a certificate of byte-identical replay.
        "finite_cone_values_check": bool(
            abs(normalization - 1.0) < 1e-8 and residual.min() >= -1e-7
        ),
    }


def floor_check() -> dict:
    mod = load_module("floor_scan", SRC / "floor_scan.py")
    with (SRC / "floor_best.json").open() as fh:
        rec = json.load(fh)
    f = mod.Fast(int(rec["p"]), int(rec["n"]))
    weights = np.asarray(rec["weights"], dtype=float)
    ratio, value, optimum, covered = f.run(weights)
    return {
        "record": "floor_best.json",
        "p": int(rec["p"]),
        "n": int(rec["n"]),
        "weight_coordinates": int(len(weights)),
        "stored_ratio": float(rec["ratio"]),
        "recomputed_ratio": float(ratio),
        "stored_v": float(rec["v"]),
        "recomputed_v": float(value),
        "stored_opt": int(rec["opt"]),
        "recomputed_opt": int(optimum),
        "stored_c": list(rec["c"]),
        "recomputed_c": list(covered),
        "finite_floor_replay_matches": bool(
            abs(ratio - float(rec["ratio"])) < 1e-9
            and abs(value - float(rec["v"])) < 1e-8
            and int(optimum) == int(rec["opt"])
            and list(covered) == list(rec["c"])
        ),
    }


def main() -> None:
    report = {"cone": cone_check(), "floor": floor_check()}
    report["all_finite_value_checks_pass"] = bool(
        report["cone"]["finite_cone_values_check"]
        and report["floor"]["finite_floor_replay_matches"]
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
