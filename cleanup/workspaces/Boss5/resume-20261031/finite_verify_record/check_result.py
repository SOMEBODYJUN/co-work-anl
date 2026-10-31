"""Read-only source audit plus isolated replay of the frozen finite result.

This independent audit is not an infinite-domain proof.  It writes only inside
this agent's finite_verify_record workspace.
"""
from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import platform
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SOURCES = BASE / "sources"
FROZEN = SOURCES / "ddcab84081659b17abfa--verify_universal.json"
PROGRAM = SOURCES / "7439aa6018b0b8ea7499--verify_universal.py"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    owned = json.loads((BASE / "owned.json").read_text())
    metadata = next(row for row in owned if row["id"] == "ddcab84081659b17abfa")
    assert FROZEN.stat().st_size == metadata["size"] == 500
    assert sha(FROZEN) == metadata["sha256"]
    blob = subprocess.run(
        ["git", "cat-file", "-p", metadata["blob"]],
        cwd=HERE, check=True, capture_output=True,
    ).stdout
    assert blob == FROZEN.read_bytes()
    (HERE / "source-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    run_dir = HERE / "isolated-replay"
    run_dir.mkdir(exist_ok=True)
    copied = run_dir / "verify_universal.py"
    shutil.copyfile(PROGRAM, copied)
    run = subprocess.run(
        [sys.executable, str(copied)], cwd=run_dir,
        capture_output=True, check=False,
    )
    (run_dir / "stdout.txt").write_bytes(run.stdout)
    (run_dir / "stderr.txt").write_bytes(run.stderr)
    assert run.returncode == 0
    generated = run_dir / "verify_universal.json"
    assert generated.read_bytes() == FROZEN.read_bytes()
    assert json.loads(run.stdout) == json.loads(FROZEN.read_text())

    # Independent direct marginal formulas, rather than replaying p(v)-p(u).
    def light_quadratic(k, l):
        return Q(1) + Q(3*l, 4*(k+2*l+1)**2)

    def heavy_quadratic(k, l):
        return Q(2) - Q(5*k, 4*(k+2*l+2)**2)

    families = {
        "quadratic_w1": (light_quadratic, Q(1)),
        "quadratic_w2": (heavy_quadratic, Q(59, 32)),
        "affine_w1": (lambda k, l: Q(1), Q(1)),
        "affine_w2": (lambda k, l: Q(2), Q(59, 32)),
        "constant_w1": (lambda k, l: Q(1), Q(1)),
        "constant_w2": (lambda k, l: Q(2), Q(59, 32)),
    }
    summary = {}
    total = 0
    frozen = json.loads(FROZEN.read_text())
    alpha = Q(frozen["alpha"])
    for name, (fn, scale) in families.items():
        records = [(fn(k, l), k, l) for k in range(101) for l in range(101)]
        lo = min(value for value, _, _ in records)
        hi = max(value for value, _, _ in records)
        assert [str(lo), str(hi)] == frozen["extrema"][name]
        assert all(scale <= value <= alpha * scale for value, _, _ in records)
        summary[name] = {
            "checks": len(records),
            "minimum": str(lo), "maximum": str(hi),
            "minimum_first_witness": next([k, l] for value, k, l in records if value == lo),
            "maximum_first_witness": next([k, l] for value, k, l in records if value == hi),
            "minimum_count": sum(value == lo for value, _, _ in records),
            "maximum_count": sum(value == hi for value, _, _ in records),
            "scale": str(scale), "allowed_upper": str(alpha * scale),
        }
        total += len(records)
    assert total == frozen["finite_checks"] == 61206
    report = {
        "source_id": metadata["id"],
        "source_size": FROZEN.stat().st_size,
        "source_sha256": sha(FROZEN),
        "source_matches_inventory_blob": True,
        "python": platform.python_version(),
        "program_sha256": sha(PROGRAM),
        "isolated_replay_exit_code": run.returncode,
        "isolated_replay_sha256": sha(generated),
        "replay_matches_frozen_bytes": True,
        "stdout_matches_frozen_json_values": True,
        "independent_direct_formula_checks": total,
        "start_grid": "integer k,l in [0,100]",
        "light_endpoint": "(k+1,l), so k may be 101",
        "heavy_endpoint": "(k,l+1), so l may be 101",
        "starting_total_load_range": [0, 300],
        "light_joined_total_load_range": [1, 301],
        "heavy_joined_total_load_range": [2, 302],
        "maximum_global_populations_sufficient_for_all_checked_edges": [101, 101],
        "not_a_full_101_by_101_population_grid": True,
        "families": summary,
        "light_upper_slack": str(alpha - Q(13, 12)),
        "universal_domain_proved_by_this_audit": False,
        "limits": "No random inputs or LP calls; this replay verifies a finite grid only. The infinite_proof field is an unexecuted textual reference, not a proof file embedded in the JSON.",
    }
    (HERE / "independent-result-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
