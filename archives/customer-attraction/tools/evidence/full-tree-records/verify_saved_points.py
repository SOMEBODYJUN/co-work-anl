"""Exact direct checks of saved points; no solver, MILP, LP or search replay."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import platform
import time


BASE = Path(__file__).resolve().parent
NAMES = [
    "small_model_check.json",
    "m3p4_alltree_price_plus_u.json",
    "m3p6_alltree_weakfloor.json",
    "m3p6_alltree_weakfloor_hull_distinct.json",
    "m4p5_alltree_tstar.json",
    "m4p5_alltree_tstar_hull_distinct.json",
]


def serial(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(v) for v in value]
    return value


def dimensions(data):
    """Count rows from the separately read current code; do not build its model."""
    p, m, z = data["p"], data["m"], data["queries"]
    n = 2**p - 1
    histories = sum(p**depth for depth in range(m))
    terminal_count = lambda depth: comb(m - depth + p - 1, p - 1)
    binaries = (
        p * (histories - 1)
        + sum(p**depth * terminal_count(depth) for depth in range(1, m - 1))
        + z
    )
    variables = n + 1 + binaries
    consistency = 0 if m == 1 else (
        p + sum(
            p**depth * p * terminal_count(depth) for depth in range(1, m - 1)
        )
    )
    incentive = (p - 1) * comb(m + p - 2, p - 1) + sum(
        p**depth * p * (p - 1) * comb(m - depth + p - 2, p - 1)**2
        for depth in range(1, m)
    )
    constraints = (
        1 + p + histories - 1
        + sum(p**depth for depth in range(1, m - 1))
        + consistency + incentive + z + 1
    )
    if data.get("root_hull", False) and m > 1:
        variables += p * terminal_count(1) * n
        constraints += p * n + p * terminal_count(1) + p - 1
    if data.get("min_pairwise_physical_distance_per_total", 0):
        constraints += comb(p, 2)
    actual = {"variables": variables, "binaries": binaries, "constraints": constraints}
    recorded = {key: data[key] for key in actual}
    assert recorded["variables"] == variables and recorded["binaries"] == binaries
    delta = constraints - recorded["constraints"]
    assert delta == (0 if data.get("root_hull", False) else p)
    return {
        "recorded": recorded,
        "current_code_combinatorial_count": actual,
        "current_minus_recorded_rows": delta,
        "missing_option_fields_use_current_defaults_for_comparison_only": True,
        "current_model_builds": 0,
        "historical_code_version_identified": False,
    }


def verify(data, name):
    p, m = data["p"], data["m"]
    result = {"source_file": name, "dimensions": dimensions(data)}
    if "candidate" not in data:
        assert name == "m4p5_alltree_tstar_hull_distinct.json"
        assert data["status"] == 1
        result.update({
            "candidate_present": False,
            "stored_floating_gap_present": "floating_gap" in data,
            "stored_floating_upper_bound_present": "floating_upper_bound" in data,
            "scope": "Time-limited record without a candidate; no infeasibility claim.",
        })
        return result, None
    c = data["candidate"]
    instance, strategy = c["instance"], c["strategy"]
    assert len(instance["topics"]) == p and instance["players"] == m
    units = []
    blocks = []
    for row in instance["customers"]:
        assert type(row["multiplicity"]) is int and row["multiplicity"] > 0
        likes = frozenset(row["topics"])
        assert likes <= set(range(p))
        units.extend([likes] * row["multiplicity"])
        blocks.append((likes, row["multiplicity"]))
    assert units
    actions = {}
    for row in strategy["actions"]:
        history = tuple(row["history"])
        assert history not in actions
        assert type(row["action"]) is int and 0 <= row["action"] < p
        actions[history] = row["action"]
    required = {
        h for depth in range(m) for h in product(range(p), repeat=depth)
    }
    assert actions.keys() == required
    assert actions[()] == data["root_action"]

    def continuation(prefix):
        history = tuple(prefix)
        while len(history) < m:
            history += (actions[history],)
        return history

    def utility(terminal, player):
        action = terminal[player]
        return sum(
            (F(1, sum(a in likes for a in terminal))
             for likes in units if action in likes),
            F(0),
        )

    rows = []
    positive = zero = 0
    for h in sorted(required, key=lambda x: (len(x), x)):
        terminal = continuation(h)
        actual_u = utility(terminal, len(h))
        deviations = []
        for action in range(p):
            if action == actions[h]:
                continue
            alternative = continuation(h + (action,))
            alternate_u = utility(alternative, len(h))
            slack = actual_u - alternate_u
            assert slack >= 0, (name, h, action, slack)
            positive += int(slack > 0)
            zero += int(slack == 0)
            deviations.append({
                "action": action, "terminal": alternative,
                "utility": alternate_u, "slack": slack,
            })
        rows.append({
            "history": h, "action": actions[h],
            "actual_terminal": terminal, "actual_utility": actual_u,
            "nonself_deviations": deviations,
        })
    terminal = continuation(())
    counts = [terminal.count(a) for a in range(p)]
    assert counts == data["root"] == strategy["terminal_counts"]
    payoffs = tuple(utility(terminal, i) for i in range(m))
    welfare = sum(bool(set(terminal) & likes) for likes in units)
    portfolios = []
    for labels in combinations(range(p), min(p, m)):
        value = sum(bool(set(labels) & likes) for likes in units)
        portfolios.append({"labels": labels, "coverage": value})
    optimum = max(row["coverage"] for row in portfolios)
    topic_sets = [frozenset(i for i, likes in enumerate(units) if a in likes) for a in range(p)]
    physical = len(set(topic_sets))
    distances = [
        {"labels": (a, b), "normalized_distance": F(len(topic_sets[a] ^ topic_sets[b]), len(units))}
        for a, b in combinations(range(p), 2)
    ]
    z = tuple(F(x) for x in c["query"])
    assert len(z) == p and all(x >= 0 for x in z)
    cover = sum(
        (min(F(1), sum((z[a] for a in likes), F(0))) for likes in units),
        F(0),
    )
    tau, u = sum(z), payoffs[0]
    if data["kind"] == "tstar":
        gap = cover - (m - 1 + tau) * u
    elif data["kind"] == "price_plus_u":
        gap = cover - (tau - 1) * u - welfare
    elif data["kind"] == "weakfloor":
        assert all(x in (0, 1) for x in z) and 1 <= tau <= m
        gap = cover - (2*m - 1) * u
    else:
        raise AssertionError(data["kind"])
    assert F(c["gap"]) == gap and F(c["gap_per_total"]) == gap / len(units)
    assert F(c["u"]) == u and c["W"] == welfare and c["OPT"] == optimum
    assert c["physical_topics"] == physical
    assert c["histories"] == len(rows) and c["deviations"] == positive + zero
    assert c["accepted_counterexample"] == (gap > 0 and physical == p)
    assert sum(payoffs) == welfare
    # These particular inputs are disjoint positive populations with duplicate
    # labels within each population. Their unrestricted price separates by block.
    assert all(likes for likes, _ in blocks)
    assert all(not (a[0] & b[0]) for a, b in combinations(blocks, 2))
    v = min(payoffs)
    price = sum((max(F(count) - v, F(0)) for _, count in blocks), F(0))
    minimizers = [i for i, value in enumerate(payoffs) if value == v]
    bridge_points = []
    for i in minimizers:
        excess = sum((max(value - v, F(0)) for value in payoffs[i+1:]), F(0))
        bridge_points.append({
            "player_one_based": i + 1, "price": price,
            "later_excess": excess, "W_plus_excess_minus_price": welfare + excess - price,
        })
    minimum_distance = min(row["normalized_distance"] for row in distances)
    threshold = data.get("min_pairwise_physical_distance_per_total")
    result.update({
        "candidate_present": True, "unit_customers": len(units),
        "full_histories_checked": len(rows), "nonself_deviations_checked": positive + zero,
        "strict_comparisons": positive, "ties": zero,
        "actual_ordered_path": terminal, "terminal_counts": counts, "payoffs": payoffs,
        "welfare": welfare, "optimal_coverage": optimum,
        "optimal_portfolios": [row["labels"] for row in portfolios if row["coverage"] == optimum],
        "physical_topics": physical, "all_pair_distances": distances,
        "minimum_normalized_distance": minimum_distance,
        "stored_distance_threshold": threshold,
        "candidate_satisfies_stored_distance": None if threshold is None else minimum_distance >= F(str(threshold)),
        "query": z, "query_mass": tau, "fractional_coverage": cover,
        "exact_gap": gap, "gap_per_total": gap / len(units),
        "global_minimum_payoff": v,
        "analytic_disjoint_blocks_full_price": price,
        "weaker_candidate_point_checks": bridge_points,
        "canonical_solver_reruns": 0, "optimizer_calls": 0,
    })
    return result, {"source_file": name, "nodes": rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", type=Path, required=True)
    output = ap.parse_args().output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    provenance = json.loads((BASE / "PROVENANCE.json").read_text())
    for row in provenance["sources"]:
        data = (BASE / row["retained_path"]).read_bytes()
        assert len(data) == row["bytes"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"], row["source_id"]
    console = (BASE / "original/audit_console.txt").read_bytes()
    audit = (BASE / "../full-history-selection/original/credible2/full_tree_milp_audit.json").read_bytes()
    assert console == audit
    records = []
    for name in NAMES:
        data = json.loads((BASE / "original" / name).read_text())
        record, all_nodes = verify(data, name)
        records.append(record)
        if all_nodes is not None:
            (output / (name.removesuffix(".json") + "-all-comparisons.json")).write_text(
                json.dumps(serial(all_nodes), ensure_ascii=False, indent=2) + "\n"
            )
    report = {
        "python": platform.python_version(),
        "wall_seconds": time.monotonic() - started,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_hashes_checked": len(provenance["sources"]),
        "saved_candidate_records": sum(x["candidate_present"] for x in records),
        "full_histories_checked": sum(x.get("full_histories_checked", 0) for x in records),
        "nonself_deviations_checked": sum(x.get("nonself_deviations_checked", 0) for x in records),
        "audit_console_identical_to_prior_frozen_report": True,
        "historical_audit_executions_repeated": 0,
        "historical_discovery_executions_repeated": 0,
        "LP_or_MILP_calls": 0,
        "canonical_solver_calls": 0,
        "records": records,
        "scope": "Five saved exact single points and one no-incumbent record; no full-cone or global optimum claim.",
    }
    assert report["saved_candidate_records"] == 5
    assert report["full_histories_checked"] == 266
    assert report["nonself_deviations_checked"] == 1120
    (output / "verification.json").write_text(
        json.dumps(serial(report), ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(serial({k: v for k, v in report.items() if k != "records"}), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
