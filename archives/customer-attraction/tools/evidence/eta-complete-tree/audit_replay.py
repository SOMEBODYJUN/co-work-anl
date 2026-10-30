"""Reconcile frozen outputs and reproduce the four finite star formula rows.

The original generator/auditor are preserved unchanged in source/. This new
supplement verifies provenance and equality, not an independent proof of BI.
Run original programs first; commands are given in the accompanying resource.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def main():
    manifest = read(ROOT / "source-manifest.json")
    for row in manifest:
        data = (ROOT / "source" / Path(row["path"]).name).read_bytes()
        assert len(data) == row["size"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
    compared = []
    for name in ("eta_dp_audit.json", "six_star_eta.json", "two_stars_six_eta.json"):
        assert read(ROOT / "source" / name) == read(ROOT / "replay" / name), name
        compared.append(name)

    spec = importlib.util.spec_from_file_location("eta_complete_tree_original",
                                                 ROOT / "source" / "eta_complete_tree.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    Tree = module.Tree
    rows = []
    for m in range(3, 7):
        # Clear class-level caches between instances, including reported counts.
        for name in ("cov", "pay", "outcomes", "threshold", "optimum",
                     "envelope", "path_best"):
            getattr(Tree, name).cache_clear()
        instance = {
            "players": m,
            "topics": ["B"] + ["L" + str(j) for j in range(1, m + 1)],
            "customers": [
                row for j in range(1, m + 1) for row in (
                    {"topics": [j], "multiplicity": m - 1},
                    {"topics": [0, j], "multiplicity": m},
                )
            ],
        }
        tree = Tree(instance)
        outcomes = tree.outcomes(tree.zero)
        all_b = (m,) + (0,) * m
        one_leaf = [tuple([m - 1] + [int(j == a) for j in range(1, m + 1)])
                    for a in range(1, m + 1)]
        assert outcomes == frozenset([all_b] + one_leaf)
        all_b_eta = tree.path_best(tree.zero, all_b)
        leaf_eta = max(tree.path_best(tree.zero, q) for q in one_leaf)
        defect = max(tree.path_best(tree.zero, q) - 2 * tree.cov(q)
                     + tree.optimum(tree.zero) for q in outcomes)
        assert all_b_eta == m
        assert leaf_eta == m + Fraction(m - 2, m - 1)
        assert defect == 0
        rows.append({
            "m": m,
            "complete_SPE_root_count_outcomes": len(outcomes),
            "all_B_eta": str(all_b_eta),
            "max_one_leaf_eta": str(leaf_eta),
            "max_defect": str(defect),
        })
    assert rows == read(ROOT / "source" / "star_formula_check.json")["rows"]
    report = {
        "status": "PASS",
        "source_files_hash_checked": len(manifest),
        "original_replay_full_json_equal": compared,
        "star_formula_rows_equal": rows,
        "scope": (
            "Exact reconciliation plus a newly supplied finite replayer for m=3..6; "
            "reuses the original Tree optimizer and does not replace the analytic proof."
        ),
    }
    path = ROOT / "replay" / "semantic-reconciliation.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
