"""Replay one frozen actual-prefix audit in an isolated, byte-checked layout.

The original exact BI is run once. No controller, random discovery, LP, or
ordered-policy certificate is produced. The independent unit-type loop checks
the six displayed terminal payoffs, not their SPE membership or minimax status.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import math
import platform
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = (Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else
        next(parent for parent in HERE.parents if (parent / "cleanup/inventory.jsonl").is_file()))
EV = ROOT / "archives/customer-attraction/tools/evidence"
R = "research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1"
CODE = EV / "bigint-interval-bi-and-controller-cone-primary/source-root" / R / "research_1"
SAVED_REPORT = EV / "diagonal-seed-materialization-boss3/related/seed18_Rdiag_actual_prefix_audit.json"
FILES = {
    "e6866c6c6c9f1ec30857": HERE / "source.json" if (HERE / "source.json").is_file() else SAVED_REPORT,
    "9536369246be24174433": EV / "menu-price-and-prescribed-prefix-audits-primary/frozen-inputs/9536369246be24174433-audit_seed_actual_prefix.py",
    "e3b91330bfecffa97610": CODE / "bigint_controller_attack.py",
    "faa31af555920b59561d": CODE / "full18_cone_attack.py",
    "40f4176105c101f8cea8": EV / "diagonal-seed-materialization-boss3/original/seed18_Rdiag.json",
}


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def run_original(inventory):
    with tempfile.TemporaryDirectory(prefix="rdiag-replay-", dir=HERE) as temporary:
        run = Path(temporary)
        code = run / "research_1"
        seed_dir = run / "research_5"
        code.mkdir()
        seed_dir.mkdir()
        for id_ in ("9536369246be24174433", "e3b91330bfecffa97610", "faa31af555920b59561d"):
            shutil.copyfile(FILES[id_], code / inventory[id_]["path"].rsplit("/", 1)[1])
        shutil.copyfile(FILES["40f4176105c101f8cea8"], seed_dir / "seed18_Rdiag.json")
        argv = [sys.executable, str(code / "audit_seed_actual_prefix.py"), "../research_5/seed18_Rdiag.json", "replayed_Rdiag"]
        begin = time.monotonic()
        proc = subprocess.run(argv, cwd=run, capture_output=True, text=True, timeout=120,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        elapsed = time.monotonic() - begin
        (HERE / "stdout.txt").write_text(proc.stdout)
        (HERE / "stderr.txt").write_text(proc.stderr)
        assert proc.returncode == 0, proc.stderr
        report_path = code / "replayed_Rdiag_actual_prefix_audit.json"
        regenerated = json.loads(report_path.read_text())
        shutil.copyfile(report_path, HERE / "regenerated-report.json")
    return regenerated, proc, elapsed, argv, run


def main():
    inventory = {}
    for line in (ROOT / "cleanup/inventory.jsonl").open():
        row = json.loads(line)
        if row["id"] in FILES:
            inventory[row["id"]] = row
    checks = []
    for id_, source in FILES.items():
        raw = source.read_bytes()
        meta = inventory[id_]
        assert len(raw) == meta["size"]
        assert hashlib.sha256(raw).hexdigest() == meta["sha256"]
        checks.append({**meta, "reused_path": str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else str(source)})
    historical = json.loads(FILES["e6866c6c6c9f1ec30857"].read_text())
    assert SAVED_REPORT.read_bytes() == FILES["e6866c6c6c9f1ec30857"].read_bytes()
    regenerated, proc, elapsed, argv, run = run_original(inventory)
    new_math = {k: v for k, v in regenerated.items() if k != "seconds"}
    old_math = {k: v for k, v in historical.items() if k != "seconds"}
    assert new_math == old_math

    # Direct exact arithmetic on all unit-customer types, without importing BI.
    seed = json.loads(FILES["40f4176105c101f8cea8"].read_text())
    assert seed["players"] == 6 and len(seed["topics"]) == 18
    types = []
    for row in seed["customers"]:
        assert isinstance(row["multiplicity"], int) and row["multiplicity"] > 0
        assert row["topics"] == sorted(set(row["topics"]))
        assert all(isinstance(t, int) and 0 <= t < 18 for t in row["topics"])
        assert sum(6 <= t < 12 for t in row["topics"]) == 1
        types.append((frozenset(row["topics"]), row["multiplicity"]))
    assert len({interest for interest, _ in types}) == len(types) == 252
    total = sum(count for _, count in types)

    def payoff(counts, action):
        return sum((Fraction(n, sum(counts[a] for a in interest))
                    for interest, n in types if action in interest), Fraction())

    direct = []
    target = historical["old_actual_counts"]
    for record in historical["checks"]:
        d = record["depth"]
        action = seed["topics"].index(record["best_security_action_label"])
        terminal = record["floor_minimizing_terminal_counts"]
        assert len(terminal) == 18 and sum(terminal) == 6
        assert all(terminal[j] >= int(j < d) for j in range(18))
        assert terminal[action] >= int(action < d) + 1
        u, floor = payoff(target, d) / total, payoff(terminal, action) / total
        assert str(u) == record["actual_player_u_over_total"]
        assert str(floor) == record["SPE_security_floor_over_total"]
        assert str(floor - u) == record["strict_floor_gap_over_total"]
        direct.append({"depth": d, "u": str(u), "displayed_floor_terminal_payoff": str(floor), "gap": str(floor-u)})
    welfare = sum(n for interest, n in types if interest.intersection(range(6)))
    assert str(Fraction(welfare, total)) == historical["old_actual_welfare_over_total"]
    import numpy
    import scipy
    result = {
        "status": "passed",
        "source_files": checks,
        "historical_report_byte_identical_to_existing_preservation": True,
        "environment": {"python": platform.python_version(), "numpy": numpy.__version__, "scipy": scipy.__version__},
        "invocation": {"argv": argv, "cwd": str(run), "exit_code": proc.returncode, "stderr_empty": not proc.stderr, "elapsed_seconds": elapsed},
        "all_mathematical_report_fields_exactly_equal": True,
        "only_ignored_report_field": "seconds",
        "historical_seconds": historical["seconds"],
        "new_report_seconds": regenerated["seconds"],
        "unit_total": str(total), "customer_types_completely_consumed": len(types),
        "direct_terminal_payoff_checks": direct,
        "root_terminal_count_states": math.comb(23, 6),
        "decision_count_states": math.comb(23, 5),
        "scope": "One frozen 18-topic six-player input, all exact set-valued BI levels and six prescribed prefixes. Original solver replay, not an independent second BI implementation or an explicit full ordered-policy certificate. No controller/LP/discovery."
    }
    dump(HERE / "verification.json", result)
    print(json.dumps({"status": "passed", "all_mathematical_fields_equal": True, "seconds": elapsed}))


if __name__ == "__main__":
    main()
