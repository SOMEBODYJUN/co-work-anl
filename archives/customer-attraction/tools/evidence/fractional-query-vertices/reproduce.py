"""Replay the two original exact enumerators and audit the saved query inputs.

No optimizer, SPE library, or floating LP is executed. Frozen files are read only.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations_with_replacement, permutations, product
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def semantic_report(value):
    return {k: v for k, v in value.items() if k != "seconds"}


def check_selected(saved, vertices):
    selected = saved["selected"]
    instance, certificate = selected["instance"], selected["certificate"]
    p, m = len(instance["topics"]), instance["players"]
    units = []
    for client in instance["customers"]:
        count = client["multiplicity"]
        assert isinstance(count, int) and count >= 0
        units.extend([frozenset(client["topics"])] * count)
    actions = {}
    for row in certificate["actions"]:
        h, a = tuple(row["history"]), row["action"]
        assert h not in actions and 0 <= a < p
        actions[h] = a
    histories = {h for depth in range(m) for h in product(range(p), repeat=depth)}
    assert set(actions) == histories

    def terminal(h):
        while len(h) < m:
            h += (actions[h],)
        return h

    def payoff(h, a):
        return sum((F(1, sum(t in interests for t in h))
                    for interests in units if a in interests), F(0))

    comparisons = 0
    minimum_slack = None
    for h in sorted(histories, key=lambda x: (len(x), x)):
        a = actions[h]
        value = payoff(terminal(h + (a,)), a)
        for b in range(p):
            if b == a:
                continue
            slack = value - payoff(terminal(h + (b,)), b)
            assert slack >= 0, (h, a, b, slack)
            comparisons += 1
            minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
    actual = terminal(())
    counts = [actual.count(a) for a in range(p)]
    assert counts == certificate["terminal_counts"]
    topic = selected["attacked_topic"]
    assert counts[topic] > 0
    u = payoff(actual, topic)
    welfare = sum(any(a in interests for a in actual) for interests in units)
    optimum = max(sum(any(a in interests for a in labels) for interests in units)
                  for labels in combinations_with_replacement(range(p), m))
    z = tuple(map(F, selected["z"]))

    def price(query):
        coverage = sum((min(F(1), sum((query[a] for a in interests), F(0)))
                        for interests in units), F(0))
        return coverage - u * sum(query, F(0))

    bz = price(z)
    best = max(map(price, vertices))
    physical = len({frozenset(i for i, interests in enumerate(units) if a in interests)
                    for a in range(p)})
    assert F(selected["u"]) == u
    assert selected["W"] == welfare and selected["OPT"] == optimum
    assert F(selected["Bz"]) == bz
    assert F(selected["Bz_minus_W"]) == bz - welfare
    assert F(selected["Bz_plus_u_minus_W"]) == bz + u - welfare
    assert selected["histories"] == len(histories)
    assert selected["deviations"] == comparisons
    assert selected["physical_topics"] == physical
    assert z in vertices
    assert saved["universal_result"] is False
    return {
        "players": m, "labels": p, "unit_customers": len(units),
        "physical_customer_sets": physical,
        "root_path": list(actual), "terminal_counts": counts,
        "all_ordered_histories_checked": len(histories),
        "actual_nonself_deviations_checked": comparisons,
        "minimum_exact_slack": str(minimum_slack),
        "u": str(u), "W": welfare, "OPT": optimum,
        "selected_z": list(map(str, z)), "selected_Bz": str(bz),
        "full_vertex_price_at_saved_point": str(best),
        "point_B_plus_u_minus_W": str(best + u - welfare),
        "policy_cone_LP_not_executed_or_certified": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        parser.error("output directory must not already exist")
    out = args.output_dir.resolve()
    out.mkdir(parents=True)
    source_manifest = read_json(ROOT / "PROVENANCE.json")
    for item in source_manifest["sources"]:
        path = ROOT / item["retained_path"]
        assert path.stat().st_size == item["bytes"]
        assert digest(path) == item["sha256"]
    records = []
    with tempfile.TemporaryDirectory(prefix="original-programs-", dir=out) as temp:
        stage = Path(temp)
        code_paths = ["credible/fractional_query_vertices.py",
                      "independent/audit_fractional_price_vertices.py"]
        for relative in code_paths:
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / "frozen" / relative, target)
        tasks = [
            ("vertices", code_paths[0], "credible/query_vertices_p5_exact.json",
             ["--topics", "5", "--output", str(stage / "credible/query_vertices_p5_exact.json")]),
            ("independent", code_paths[1], "independent/fractional_price_vertex_implementation_audit.json", []),
        ]
        for label, code, report, options in tasks:
            command = [sys.executable, "-E", "-B", str(stage / code), *options]
            started = time.monotonic()
            process = subprocess.run(command, cwd=stage, capture_output=True)
            elapsed = time.monotonic() - started
            (out / (label + "-stdout.txt")).write_bytes(process.stdout)
            (out / (label + "-stderr.txt")).write_bytes(process.stderr)
            assert process.returncode == 0, (label, process.returncode, process.stderr)
            generated = stage / report
            archived = ROOT / "frozen" / report
            new = read_json(generated)
            old = read_json(archived)
            assert semantic_report(new) == semantic_report(old), label
            destination = out / (label + "-report.json")
            shutil.copyfile(generated, destination)
            records.append({
                "program": code, "program_sha256": digest(stage / code),
                "command": ["python3", "-E", "-B", code] + (
                    ["--topics", "5", "--output", report] if label == "vertices" else []),
                "exit_code": process.returncode, "wall_seconds": elapsed,
                "old_report_sha256": digest(archived), "new_report_sha256": digest(destination),
                "full_report_bytes_equal": archived.read_bytes() == generated.read_bytes(),
                "all_fields_other_than_seconds_equal": True,
                "excluded_fields": ["seconds"],
                "old_seconds": old["seconds"], "new_seconds": new["seconds"],
            })
    exact = read_json(ROOT / "frozen/credible/query_vertices_p5_exact.json")
    vertices = {tuple(map(F, row)) for row in exact["vertices"]}
    assert len(vertices) == 260 and len(exact["vertices"]) == 260
    assert len({tuple(map(F, row)) for row in exact["sorted_patterns"]}) == 27
    comparisons = []
    old_check = read_json(ROOT / "frozen/credible/query_enumeration_audit.json")
    for row in old_check["checks"]:
        path = ROOT / "frozen/credible" / row["file"]
        assert digest(path) == row["sha256"]
        saved = read_json(path)
        proposed = {x for pattern in saved["query_patterns"]
                    for x in permutations(tuple(map(F, pattern)))}
        assert proposed == vertices
        assert row["query_set_matches_exact"] and row["query_count"] == 260
        assert row["LP_upper_bound_proven"] is False
        assert saved["queries"] == 260
        assert all(record["queries"] == 260 for record in saved["records"])
        comparisons.append({
            "file": row["file"], "sha256": digest(path),
            "expanded_query_sets_exactly_equal": True, "vertices": 260,
            "historical_floating_policy_records": len(saved["records"]),
            "historical_records_retained_not_reoptimized": True,
            "saved_point_audit": check_selected(saved, vertices),
        })
    report = {
        "scope": "Original exact enumerator replays, old query-set identity, and exact saved-point strategy checks; no LP or universal SPE claim.",
        "python": platform.python_version(), "original_program_executions": records,
        "old_query_reports": comparisons, "optimizer_runs": 0,
        "second_implementation_full_p5_enumerations": 0,
        "source_files_hash_checked": len(source_manifest["sources"]),
    }
    (out / "replay-manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"program_replays": len(records), "old_query_sets_equal": len(comparisons),
                      "saved_histories_checked": sum(r["saved_point_audit"]["all_ordered_histories_checked"] for r in comparisons),
                      "actual_deviations_checked": sum(r["saved_point_audit"]["actual_nonself_deviations_checked"] for r in comparisons),
                      "optimizer_runs": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
