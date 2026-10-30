#!/usr/bin/env python3
"""Replay the unchanged triad verifier and independently read both literal fixtures."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def literal_check(author):
    fixture = json.loads((ROOT / "original/examples/weighted_congestion/decision_methods/quadratic_triad.json").read_text())
    names = list(fixture["resources"])
    coefficients = [tuple(map(F, fixture["resources"][e])) for e in names]
    weights = tuple(F(p["weight"]) for p in fixture["players"])
    strategies = tuple(tuple(frozenset(names.index(e) for e in action) for action in p["strategies"])
                       for p in fixture["players"])
    old = json.loads((ROOT / "related/examples/weighted_congestion/template_certificates/exact_fixtures.json").read_text())["games"][0]
    assert weights == tuple(map(F, old["weights"]))
    assert coefficients == [tuple(map(F, c)) for c in old["fees"]]
    assert strategies == tuple(tuple(frozenset(a) for a in ss) for ss in old["strategies"])
    masks = [[sum(1 << bit for bit, action in enumerate(strategies[i]) if e in action)
              for i in range(3)] for e in range(6)]
    assert masks == [r["mask"] for r in author["resources"]]

    def costs(state):
        selected = [strategies[i][state[i]] for i in range(3)]
        loads = [sum((weights[i] for i in range(3) if e in selected[i]), F(0)) for e in range(6)]
        fees = [sum((a * loads[e] ** k for k, a in enumerate(c)), F(0)) for e, c in enumerate(coefficients)]
        return tuple(sum((fees[e] for e in action), F(0)) for action in selected)

    table = []
    for state in product((0, 1), repeat=3):
        current = costs(state)
        after = []
        for i in range(3):
            target = list(state)
            target[i] ^= 1
            after.append(costs(target)[i])
        assert all(c > 0 for c in (*current, *after))
        ratios = [a / b for a, b in zip(current, after)]
        factor = max(F(1), *ratios)
        source = next(row for row in author["states"] if row["profile"] == list(state))
        assert [str(x) for x in current] == [d["current"] for d in source["deviations"]]
        assert [str(x) for x in after] == [d["after"] for d in source["deviations"]]
        assert [str(x) for x in ratios] == [d["ratio"] for d in source["deviations"]]
        assert str(factor) == source["factor"]
        assert ratios.index(max(ratios)) == source["attacker"]
        table.append({"state": list(state), "current": list(map(str, current)), "after": list(map(str, after)),
                      "ratios": list(map(str, ratios)), "factor": str(factor),
                      "selected_53_over_50_margin": str(current[source["attacker"]] - F(53, 50) * after[source["attacker"]])})
    threshold = min(F(row["factor"]) for row in table)
    assert threshold == F(286, 267)
    endpoints = [row["state"] for row in table if all(F(a) <= threshold * F(b) for a, b in zip(row["current"], row["after"]))]
    assert endpoints == author["endpoint_PNE"] == [[0, 1, 0], [1, 0, 1]]
    assert all(F(row["selected_53_over_50_margin"]) > 0 for row in table)
    cycle = [(0, 1, 0), (1, 1, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1), (0, 1, 1), (0, 1, 0)]
    edges = []
    for a, b in zip(cycle, cycle[1:]):
        movers = [i for i in range(3) if a[i] != b[i]]
        assert len(movers) == 1
        i = movers[0]
        ratio = costs(a)[i] / costs(b)[i]
        assert ratio >= threshold
        edges.append({"from": list(a), "to": list(b), "player": i, "ratio": str(ratio)})
    assert [e["player"] for e in edges] == [0, 1, 2, 0, 1, 2]
    return {"status": "passed", "arithmetic": "Fraction only", "author_imported": False,
            "fixture_same_as_old_53_over_50_example": True, "states": table, "different_unilateral_deviations": 24,
            "threshold": str(threshold), "endpoint_PNE": endpoints, "literal_cycle": edges,
            "threshold_minus_19_over_18": str(threshold - F(19, 18)),
            "threshold_minus_16_over_15": str(threshold - F(16, 15)),
            "scope": "Internal migration replay of one existing game; not an independently discovered construction or general bound."}


def main():
    if not __debug__:
        raise RuntimeError("Do not run with -O")
    for entry in json.loads((ROOT / "provenance.json").read_text())["sources"]:
        assert hashlib.sha256((ROOT / "original" / entry["path"]).read_bytes()).hexdigest() == entry["sha256"]
    target = ROOT / "replay/author"
    target.mkdir(parents=True, exist_ok=True)
    script = ROOT / "original/tests/audits/weighted_congestion/quadratic_triad/verify.py"
    shutil.copy2(script, target / "verify.py")
    command = [sys.executable, "verify.py"]
    run = subprocess.run(command, cwd=target, text=True, capture_output=True)
    (target / "stdout.txt").write_text(run.stdout)
    (target / "stderr.txt").write_text(run.stderr)
    assert run.returncode == 0, run.stderr
    author = json.loads((target / "verification.json").read_text())
    frozen = json.loads((ROOT / "original/evidence/runs/weighted_congestion/quadratic_triad/verification.json").read_text())
    differences = [] if author == frozen else [{"frozen": frozen, "replay": author}]
    assert not differences, "author frozen output mismatch"
    independent = literal_check(author)
    (ROOT / "replay/literal-fixture-check.json").write_text(json.dumps(independent, ensure_ascii=False, indent=2) + "\n")
    report = {"status": "passed", "python": sys.version.split()[0], "command": command, "exit_code": run.returncode,
              "source_sha256": hashlib.sha256(script.read_bytes()).hexdigest(), "frozen_report_differences": differences,
              "literal_fixture_check": "passed; 8 states, 24 deviations, endpoint and six cycle edges"}
    (ROOT / "replay-comparison.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
