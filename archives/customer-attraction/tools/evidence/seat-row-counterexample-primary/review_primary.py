"""One finite source replay and an independent full-history certificate review.

Does not import/run any LP, random probe, or independent_seat_assets entry.
The certificate checker below uses only the standard library and the JSON input.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "original/research/workspaces/customer-attraction/R-c99d11e5cc394080a36a00845811d71a"
OUT = ROOT / "review-001"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(instance, certificate):
    topics, players = len(instance["topics"]), instance["players"]
    actions = {}
    for item in certificate["actions"]:
        assert set(item) == {"history", "action"}
        h, a = tuple(item["history"]), item["action"]
        assert h not in actions
        assert type(a) is int and 0 <= a < topics
        assert all(type(x) is int and 0 <= x < topics for x in h)
        actions[h] = a
    expected = {h for depth in range(players) for h in product(range(topics), repeat=depth)}
    assert set(actions) == expected
    values = {}
    checked = deviations = 0
    minimum = None

    def pay(counts, action):
        key = counts, action
        if key not in values:
            values[key] = sum((F(c["multiplicity"], sum(counts[j] for j in c["topics"]))
                               for c in instance["customers"] if action in c["topics"]), F())
        return values[key]

    def walk(h):
        nonlocal checked, deviations, minimum
        if len(h) == players:
            return tuple(h.count(j) for j in range(topics)), h
        branches = [walk(h + (a,)) for a in range(topics)]
        chosen = actions[h]
        terminal, terminal_path = branches[chosen]
        current = pay(terminal, chosen)
        checked += 1
        for a, (other, _) in enumerate(branches):
            if a == chosen:
                continue
            slack = current - pay(other, a)
            assert slack >= 0, (h, a, slack)
            minimum = slack if minimum is None else min(minimum, slack)
            deviations += 1
        return terminal, terminal_path

    terminal, path = walk(())
    assert terminal == tuple(certificate["terminal_counts"])
    return {"valid": True, "checked_histories": checked, "checked_deviations": deviations,
            "minimum_ic_slack": str(minimum), "terminal_counts": list(terminal),
            "terminal_history": list(path), "root_payoff": str(pay(terminal, path[0])),
            "history_depth_counts": dict(sorted(Counter(map(len, actions)).items())),
            "all_prescribed_actions": sorted(set(actions.values()))}


def main():
    start = time.perf_counter()
    OUT.mkdir(exist_ok=True)
    manifest = json.loads((ROOT / "source-manifest.json").read_text())
    before = {x["path"]: digest(ROOT / "original" / x["path"]) for x in manifest}
    assert all(before[x["path"]] == x["sha256"] for x in manifest)
    obj = json.loads((SOURCE / "seat_row_counterexample_certificate.json").read_text())
    assert set(obj) == {"instance", "certificate", "verification"}
    result = verify(obj["instance"], obj["certificate"])
    for key, value in obj["verification"].items():
        assert result[key] == value
    assert result["all_prescribed_actions"] == [0]
    assert result["terminal_counts"] == [6, 0, 0, 0, 0, 0, 0]
    source_six = json.loads((SOURCE / "diagnostics/verify_seat_row_counterexample.json").read_text())
    assert source_six == {"status": "exact_pass", "checked_histories": 19608,
                          "checked_deviations": 117648, "root_payoff": "1",
                          "invalid_seat_row_k1_rhs": "6", "welfare": 6, "optimum": 11}
    two_instance = {"topics": ["B0", "B1"], "players": 2,
                    "customers": [{"topics": [0], "multiplicity": 2},
                                  {"topics": [1], "multiplicity": 1}]}
    two_cert = {"terminal_counts": [1, 1], "actions": [
        {"history": [], "action": 1}, {"history": [0], "action": 0},
        {"history": [1], "action": 0}]}
    two = verify(two_instance, two_cert)
    route = two["terminal_history"]
    k = 1 + sum(a == 0 for a in route[1:])
    two.update({"root_route": route, "topic_j": 0, "correct_future_repetitions": k - 1,
                "correct_k": k, "correct_route_seat_rhs": str(F(2, k)),
                "old_hardcoded_rhs": "2", "conclusion": "correct row is equality; old report is not a route-row counterexample"})
    assert two["root_payoff"] == two["correct_route_seat_rhs"] == "1"
    old_two = json.loads((SOURCE / "diagnostics/verify_route_seat_n2.json").read_text())
    assert old_two == {"status": "exact_pass", "checked_histories": 3,
                       "checked_deviations": 3, "root_path": [1, 0],
                       "root_payoff": "1", "route_seat_rhs": "2", "welfare": 3, "optimum": 3}
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "dependencies")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = [sys.executable, str(SOURCE / "exhaustive_m6_small.py")]
    t0 = time.perf_counter()
    run = subprocess.run(argv, cwd=OUT, env=env, capture_output=True, text=True, timeout=60)
    elapsed = time.perf_counter() - t0
    (OUT / "finite-screen-stdout.txt").write_text(run.stdout)
    (OUT / "finite-screen-stderr.txt").write_text(run.stderr)
    assert run.returncode == 0, run.stderr
    screen = json.loads((OUT / "exhaustive_m6_small_report.json").read_text())
    old = json.loads((SOURCE / "exhaustive_m6_small_report.json").read_text())
    assert [{k: v for k, v in x.items() if k != "elapsed_seconds"} for x in screen] == [
        {k: v for k, v in x.items() if k != "elapsed_seconds"} for x in old]
    # Read the complete diagnostic index as navigation, not its 259 referenced files.
    lines = (SOURCE / "diagnostics/m6files_index.txt").read_text().splitlines()
    assert len(lines) == len(set(lines)) == 259 and all(lines)
    after = {x["path"]: digest(ROOT / "original" / x["path"]) for x in manifest}
    assert before == after
    report = {"status": "passed", "six_person_full_certificate": result,
              "two_person_correction": two, "finite_screen_report_matches_except_timing": True,
              "source_files": len(manifest), "source_hashes_unchanged": True,
              "index_lines": len(lines), "index_referenced_files_read_by_this_entry": 0,
              "original_finite_screen_argv": argv, "original_finite_screen_cwd": str(OUT),
              "original_finite_screen_exit": run.returncode,
              "original_finite_screen_elapsed_seconds": elapsed,
              "total_elapsed_seconds": time.perf_counter() - start,
              "execution_scope": "one new independent certificate entry and one original finite-screen subprocess; zero original certificate entries, LP, random search or seat-asset replay"}
    (OUT / "review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
