"""Verify both frozen fixed-policy certificates, then rebuild their duals directly.

The two original verify commands are executed once each. No build, LP, or
equilibrium search is executed. The additional reconstruction imports no game
library and does not claim a second independent vertex enumeration.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import argparse

ROOT = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_dual_audit(data, expected_instance):
    instance = data["source_instance"]
    assert instance == expected_instance
    p, m = len(instance["topics"]), instance["players"]
    masks = tuple(range(1, 1 << p))
    acts = {}
    for row in data["strategy"]["actions"]:
        h, a = tuple(row["history"]), row["action"]
        assert h not in acts and 0 <= a < p
        acts[h] = a
    required_histories = {h for depth in range(m) for h in product(range(p), repeat=depth)}
    assert set(acts) == required_histories

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (acts[h],))

    def coefficients(labels, chosen):
        return tuple(F(1, sum(bool(mask & (1 << a)) for a in labels))
                     if mask & (1 << chosen) else F(0) for mask in masks)

    comparisons = []
    for h in sorted(required_histories, key=lambda v: (len(v), v)):
        a = acts[h]
        actual = coefficients(terminal(h), a)
        for b in range(p):
            if b == a:
                continue
            alternate = coefficients(terminal(h + (b,)), b)
            gamma = tuple(x - y for x, y in zip(actual, alternate))
            comparisons.append((h, a, b, gamma))
    rows = tuple(sorted({g for _, _, _, g in comparisons if any(g)}))
    index = {row: j for j, row in enumerate(rows)}
    root = terminal(())
    counts = [root.count(a) for a in range(p)]
    assert counts == data["strategy"]["terminal_counts"]
    occupied = sorted(set(root))
    w = tuple(F(any(mask & (1 << a) for a in root)) for mask in masks)
    r = [F(0)] * len(masks)
    for customer in instance["customers"]:
        mask = sum(1 << a for a in set(customer["topics"]))
        if mask:
            r[mask - 1] += F(customer["multiplicity"])

    def dot(a, b):
        return sum((x * y for x, y in zip(a, b)), F(0))

    source_slacks = [dot(g, r) for _, _, _, g in comparisons]
    assert all(x >= 0 for x in source_slacks)
    vertices = tuple(tuple(map(F, z)) for z in data["vertices"])
    assert len(set(vertices)) == len(vertices)
    assert all(len(z) == p and all(0 <= x <= 1 for x in z) for z in vertices)
    required = {(a, j) for a in occupied for j in range(len(vertices))}
    seen = set()
    proof_results = []
    row_uses = Counter()
    for proof in data["proofs"]:
        a, j = proof["topic"], proof["query_index"]
        assert (a, j) in required and (a, j) not in seen
        seen.add((a, j))
        z, beta = vertices[j], F(proof["beta"])
        ell = coefficients(root, a)
        coverage = tuple(min(F(1), sum((z[b] for b in range(p) if mask & (1 << b)), F(0)))
                         for mask in masks)
        tau = sum(z, F(0))
        if data["kind"] == "tstar":
            c = tuple(x - (tau + m - 1) * y for x, y in zip(coverage, ell))
        elif data["kind"] == "price_plus_u":
            c = tuple(x - (tau - 1) * y - v for x, y, v in zip(coverage, ell, w))
        else:
            raise AssertionError("Only the two actually supplied objectives are audited")
        multipliers = {}
        for row_index, value in proof["multipliers"]:
            assert row_index not in multipliers and 0 <= row_index < len(rows)
            value = F(value)
            assert value >= 0
            multipliers[row_index] = value
            row_uses[row_index] += 1
        residual = tuple(beta * w[k] - c[k]
                         - sum((mu * rows[i][k] for i, mu in multipliers.items()), F(0))
                         for k in range(len(masks)))
        assert beta <= 0 and all(x >= 0 for x in residual)
        proof_results.append({
            "topic": a, "query_index": j, "beta": str(beta),
            "multipliers_checked": len(multipliers),
            "exact_residual_by_mask_1_to_15": list(map(str, residual)),
            "source_target_value": str(dot(c, r)),
        })
    assert seen == required
    assert data["row_count"] == len(rows)
    assert data["all_bounds_nonpositive"] is True
    assert data["universal_policy_claim"] is False
    welfare = dot(w, r)
    optimum = max(sum((r[mask - 1] for mask in masks
                       if any(mask & (1 << a) for a in labels)), F(0))
                  for labels in combinations_with_replacement(range(p), m))
    point = []
    for a in occupied:
        u = dot(coefficients(root, a), r)
        values = []
        for z in vertices:
            coverage = sum((r[mask - 1] * min(F(1), sum((z[b] for b in range(p)
                                                       if mask & (1 << b)), F(0)))
                            for mask in masks), F(0))
            values.append(coverage - u * sum(z, F(0)))
        maximum = max(values)
        point.append({"topic": a, "u": str(u), "full_vertex_price": str(maximum),
                      "maximizing_query_indices": [j for j, value in enumerate(values) if value == maximum]})
    actual_u = dot(coefficients(root, root[0]), r)
    root_moves = []
    for a in range(p):
        static = (a,) + root[1:]
        sequential = terminal((a,))
        root_moves.append({"action": a,
                           "static_return_with_other_actions_fixed": str(dot(coefficients(static, a), r)),
                           "sequential_terminal": list(sequential),
                           "sequential_return": str(dot(coefficients(sequential, a), r)),
                           "actual_root_payoff": str(actual_u)})
    return {
        "kind": data["kind"], "source_instance_equal_to_frozen_example": True,
        "ordered_histories": len(required_histories), "nonself_comparisons": len(comparisons),
        "zero_comparison_rows": sum(not any(g) for _, _, _, g in comparisons),
        "distinct_nonzero_rows": len(rows), "mask_order": list(masks),
        "gamma_rows": [list(map(str, g)) for g in rows],
        "comparison_to_row": [
            {"history": list(h), "chosen": a, "alternative": b,
             "row_index": index.get(g), "source_slack": str(dot(g, r))}
            for h, a, b, g in comparisons],
        "proofs": proof_results, "proof_count": len(proof_results),
        "residual_coordinates_checked": len(masks) * len(proof_results),
        "nonzero_multiplier_entries_checked": sum(x["multipliers_checked"] for x in proof_results),
        "beta_counts": dict(sorted(Counter(x["beta"] for x in proof_results).items())),
        "minimum_residual": str(min(F(x) for proof in proof_results
                                    for x in proof["exact_residual_by_mask_1_to_15"])),
        "all_beta_nonpositive": True,
        "source_root_path": list(root), "source_W": str(welfare), "source_OPT": str(optimum),
        "source_point_prices": point, "source_root_deviation_table": root_moves,
        "scope": "Exact independent full-history and residual reconstruction for the same fixed policy; complete vertices are checked by the separately executed original verifier.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("output directory must not already exist")
    out = args.output_dir.resolve()
    out.mkdir(parents=True)
    provenance = read_json(ROOT / "PROVENANCE.json")
    for row in provenance["sources"]:
        path = ROOT / row["retained_path"]
        assert path.stat().st_size == row["bytes"] and sha(path) == row["sha256"]
    programs = []
    audits = []
    with tempfile.TemporaryDirectory(prefix="fixed-policy-originals-", dir=out) as temp:
        stage = Path(temp)
        for row in provenance["sources"]:
            target = stage / row["stage_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / row["retained_path"], target)
        script = stage / "credible/fixed_policy_price_certificate.py"
        expected = read_json(stage / "examples/customer_attraction/worst_pne_welfare_failure.json")
        for kind in ["tstar", "price_plus_u"]:
            relative = "credible/nonPNE_fixed_policy_" + kind + "_exact.json"
            supplied = stage / relative
            before = sha(supplied)
            started = time.monotonic()
            process = subprocess.run([sys.executable, "-E", "-B", str(script),
                                      "verify", "--file", str(supplied)], capture_output=True, cwd=stage)
            elapsed = time.monotonic() - started
            (out / (kind + "-stdout.json")).write_bytes(process.stdout)
            (out / (kind + "-stderr.txt")).write_bytes(process.stderr)
            assert process.returncode == 0, (kind, process.stderr)
            verified = json.loads(process.stdout)
            assert verified["verified"] is True and verified["all_bounds_nonpositive"] is True
            assert verified["maximum_beta"] == "0" and verified["dual_proofs"] == 60
            assert sha(supplied) == before
            data = read_json(supplied)
            audit = independent_dual_audit(data, expected)
            assert audit["ordered_histories"] == verified["source_histories_verified"]
            assert audit["nonself_comparisons"] == verified["source_deviations_verified"]
            assert audit["distinct_nonzero_rows"] == verified["row_count"]
            (out / (kind + "-independent-duals.json")).write_text(
                json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
            audits.append({k: audit[k] for k in [
                "kind", "proof_count", "residual_coordinates_checked",
                "nonzero_multiplier_entries_checked", "beta_counts", "minimum_residual",
                "source_W", "source_OPT", "source_point_prices", "source_root_deviation_table"]})
            programs.append({
                "kind": kind, "code_sha256": sha(script), "certificate_sha256": before,
                "command": ["python3", "-E", "-B", "credible/fixed_policy_price_certificate.py",
                            "verify", "--file", relative],
                "exit_code": process.returncode, "wall_seconds": elapsed,
                "output": verified, "certificate_bytes_unchanged": True,
                "stdout_sha256": sha(out / (kind + "-stdout.json")),
            })
    manifest = {
        "python": platform.python_version(), "original_verify_executions": programs,
        "independent_residual_reconstruction": audits,
        "source_files_hash_checked": len(provenance["sources"]),
        "build_executions": 0, "LP_executions": 0, "SPE_solver_searches": 0,
        "unique_policy_histories": 21, "unique_policy_nonself_comparisons": 63,
        "certificate_count": 2, "proofs_verified": 120, "residual_coordinates_verified": 1800,
        "scope": "The supplied single full-policy cone and its two exact objectives, not arbitrary policies.",
    }
    (out / "replay-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"original_verify_executions": 2, "proofs": 120,
                      "independent_residual_coordinates": 1800,
                      "LP_executions": 0, "SPE_solver_searches": 0}))


if __name__ == "__main__":
    main()
