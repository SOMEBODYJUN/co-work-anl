"""Exact finite audit of the frozen price attack, separate from its LP oracle.

No LP is solved here. Every saved action and every run record is consumed.
The 13-player and replicated-block calculations check pricing, not new SPEs.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "source-root"))
from customer_attraction import Instance, StrategyCertificate, verify_certificate


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    best = json.loads((HERE / "original/price_m5p7_best.json").read_text())
    run = json.loads((HERE / "original/price_m5p7_run.json").read_text())
    instance = Instance.from_dict(best["instance"])
    certificate = StrategyCertificate.from_dict(best["strategy"])
    verified = verify_certificate(instance, certificate)
    verified.assert_valid()
    m, p = instance.players, instance.topic_count
    expected = {h for d in range(m) for h in itertools.product(range(p), repeat=d)}
    assert set(certificate.actions) == expected
    assert certificate.actions[()] == 6
    assert all(a == 0 for h, a in certificate.actions.items() if h)

    # Independent direct unit-customer evaluator. No Instance payoff or solver.
    customers = [(set(c["topics"]), c["multiplicity"])
                 for c in best["instance"]["customers"]]
    checked = 0
    min_gap = None
    def utility(leaf, action):
        return sum((Q(n, sum(t in interest for t in leaf))
                    for interest, n in customers if action in interest), Q())
    def walk(h):
        nonlocal checked, min_gap
        if len(h) == m:
            return h
        leaves = [walk(h + (a,)) for a in range(p)]
        chosen = certificate.actions[h]
        own = utility(leaves[chosen], chosen)
        for a, leaf in enumerate(leaves):
            if a == chosen:
                continue
            gap = own - utility(leaf, a)
            assert gap >= 0
            min_gap = gap if min_gap is None else min(min_gap, gap)
            checked += 1
        return leaves[chosen]
    leaf = walk(())
    assert leaf == (6, 0, 0, 0, 0)
    welfare = sum(n for interest, n in customers if any(a in interest for a in leaf))
    utilities = [utility(leaf, a) for a in leaf]
    v = min(utilities)
    z = list(map(Q, best["z"]))
    value = sum((n * min(Q(1), sum((z[a] for a in interest), Q()))
                 for interest, n in customers), Q()) - v * sum(z)
    assert (welfare, v, value) == (1, Q(1, 5), Q(4, 5))
    assert str(value / welfare) == best["B_lower_bound_over_W"]
    assert instance.optimal_welfare() == best["OPT"] == best["W"] == 1

    # All run data fields are inspected; no missing endpoint is reconstructed.
    assert run["parameters"] == best["parameters"]
    assert len(run["records"]) == run["cones"] == 38
    steps, keys, exact_values, proposals, row_sizes = [], [], [], [], []
    for row in run["records"]:
        assert set(row) == {"step", "root_counts", "topic", "cone_sha256", "rows", "rounds"}
        assert len(row["root_counts"]) == p and sum(row["root_counts"]) == m
        assert row["root_counts"][row["topic"]] > 0
        assert len(row["cone_sha256"]) == 64 and row["rows"] > 0
        assert len(row["rounds"]) == 4
        steps.append(row["step"]); keys.append(row["cone_sha256"]); row_sizes.append(row["rows"])
        for item in row["rounds"]:
            assert set(item) == {"proposal_B_over_W", "exact_feasible_portfolio_over_W"}
            exact = Q(item["exact_feasible_portfolio_over_W"])
            proposal = item["proposal_B_over_W"]
            assert 0 <= exact <= Q(4, 5) and proposal <= 0.8 + 1e-12
            exact_values.append(exact); proposals.append(proposal)
    assert len(set(steps)) == len(set(keys)) == 38
    assert set(range(40)) - set(steps) == {18, 22}
    assert len(exact_values) == 152 and max(exact_values) == Q(4, 5)
    assert run["best_exact_B_lower_over_W"] == "4/5"

    # Exact primal / residual-packing certificates for the old 36-customer packet.
    labels = ("A", "B", "T", "D", "E", "P")
    types = [({"A"}, 2), ({"B"}, 2), ({"T"}, 1), ({"T", "D"}, 1),
             ({"T", "E"}, 1), ({"A", "D", "E"}, 3), ({"B", "D", "E"}, 1), ({"P"}, 25)]
    packet = []
    for price, portfolio, lam, answer in [
        (Q(5, 2), {"A", "B", "T", "P"}, [2, 2, Q(1, 2), 1, 1, Q(1, 2), Q(1, 2), Q(5, 2)], 26),
        (Q(3), {"D", "P"}, [2, 2, 1, 1, 1, 1, 1, 3], 24),
    ]:
        assert all(0 <= k <= n for k, (_, n) in zip(lam, types))
        loads = {a: sum((Q(k) for k, (interest, _) in zip(lam, types) if a in interest), Q()) for a in labels}
        assert all(load <= price for load in loads.values())
        primal = sum(n for interest, n in types if interest & portfolio) - price * len(portfolio)
        upper = 36 - sum(lam)
        assert primal == upper == answer
        packet.append({"price": str(price), "value": str(primal), "lambda": list(map(str, lam)), "topic_loads": {a: str(k) for a, k in loads.items()}})

    # One replicated block. The group permutes the labels transitively.
    block = [(set((a, b)), 1) for a in range(3) for b in range(3, 6)]
    block += [(set(i + j), 3) for i in itertools.combinations(range(3), 2)
              for j in itertools.combinations(range(3, 6), 2)]
    assert Counter(len(interest) for interest, _ in block) == {2: 9, 4: 9}
    assert sum(n for _, n in block) == 36
    assert [sum(n for interest, n in block if a in interest) for a in range(6)] == [21] * 6
    at10 = [sum((n * min(Q(1), len(interest) * q) for interest, n in block), Q()) - 60 * q
            for q in (Q(0), Q(1, 4), Q(1, 2))]
    assert at10 == [0, Q(33, 2), Q(6)]

    result = {
        "scope": "Saved best full-history SPE and exact pricing arithmetic; no universal theorem; no independent LP reimplementation",
        "primary_sha256": {x.name: digest(x) for x in sorted((HERE / "original").iterdir())},
        "canonical_verifier": {"valid": verified.valid, "checked_histories": verified.checked_histories, "checked_deviations": verified.checked_deviations, "terminal_history": leaf},
        "independent_unit_customer_check": {"comparisons": checked, "minimum_gap": str(min_gap), "actions": len(certificate.actions), "depth_counts": dict(sorted(Counter(map(len, certificate.actions)).items())), "W": welfare, "OPT": 1, "actual_payoffs": list(map(str, utilities)), "feasible_value": str(value)},
        "frozen_run": {"cones": len(keys), "rounds": len(exact_values), "skipped_requested_steps": [18, 22], "exact_max": str(max(exact_values)), "float_max": max(proposals), "row_count_range": [min(row_sizes), max(row_sizes)], "counts_by_exact_value": dict(sorted(Counter(map(str, exact_values)).items()))},
        "thirteen_player_primal_and_packing": packet,
        "replicated_block_price10_breakpoint_values": list(map(str, at10)),
        "limitations": ["Other 151 rounds do not save their customer endpoint, rational portfolio, or full strategy; logged exact fields are historical records.", "The selected occupied topic is minimum only in the seed; subsequent LPs do not preserve minimum-price inequalities.", "No 13-player or replicated-block SPE graft is reverified by this script."]
    }
    out = HERE / "audit.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
