#!/usr/bin/env python3
"""Independent exact translations of two existing complete-SPE obstructions.

Does not import the kernel implementation, canonical solver or SPE verifier.
"""

from fractions import Fraction as F
from itertools import combinations_with_replacement
import json


def audit(name, labels, blocks, root, replies, optimum):
    clients = [frozenset(signature) for signature, size in blocks
               for _ in range(size)]

    def payoff(path, i):
        return sum((F(1, sum(topic in client for topic in path))
                    for client in clients if path[i] in client), F(0))

    def coverage(path):
        return sum(any(topic in client for topic in path) for client in clients)

    actual = (root, replies[root])
    comparisons = 0
    for first in labels:
        chosen = (first, replies[first])
        for second in labels:
            assert payoff(chosen, 1) >= payoff((first, second), 1)
            comparisons += 1
    for first in labels:
        assert payoff(actual, 0) >= payoff((first, replies[first]), 0)
        comparisons += 1
    pairs = {pair: coverage(pair)
             for pair in combinations_with_replacement(labels, 2)}
    opt = max(pairs.values())
    assert {frozenset(pair) for pair, value in pairs.items() if value == opt} == {
        frozenset(optimum)}
    W = coverage(actual)
    rows = []
    for comparison in (optimum, tuple(reversed(optimum))):
        chi = D = R_last = R_add = S = F(0)
        # The two comparison topics are disjoint; hence O=B=C=0.
        assert not any(all(t in client for t in optimum) for client in clients)
        for i, topic in enumerate(comparison):
            branch = ((topic, replies[topic]) if i == 0 else (actual[0], topic))
            S += payoff(actual, i) - payoff(branch, i)
            for client in clients:
                if topic not in client:
                    continue
                c = sum(t in client for t in actual)
                z = int(actual[i] in client)
                true_denominator = sum(t in client for t in branch)
                static_denominator = c + 1 - z
                chi += 1 - F(1, static_denominator)
                D += F(1, static_denominator) - F(1, true_denominator)
                R_last += F(1, static_denominator)
                R_add += F(1, c + 1)
        assert chi == opt - R_last
        assert opt == W + chi + D - S
        assert S == 0
        assert D > S
        rows.append({"comparison": comparison, "chi": str(chi), "A": str(S),
                     "D": str(D), "R_last": str(R_last), "R_add": str(R_add),
                     "true_capacity_W_minus_chi": str(W - chi)})
    full_tax = sum((F(c, c + 1) for client in clients
                    for c in [sum(t in client for t in actual)] if c), F(0))
    return {"name": name, "clients": len(clients), "actual": actual,
            "comparisons": comparisons, "W": W, "OPT": opt,
            "full_tax": str(full_tax),
            "full_tax_bridge_margin": str(W + full_tax - opt), "orders": rows}


small = audit("existing_PFR_OPT_14", tuple("ABTSQR"), [
    ("S", 2), ("SQ", 1), ("T", 2), ("TR", 1), ("B", 2),
    ("BR", 1), ("BQ", 1), ("ASQR", 2), ("ATQR", 2)],
    "A", dict(zip("ABTSQR", "BQQRRQ")), tuple("TS"))
assert small["W"] == 8 and small["OPT"] == 10
assert {r["chi"] for r in small["orders"]} == {"1"}
assert {r["D"] for r in small["orders"]} == {"1"}

family = []
for k in range(3, 9):
    row = audit(f"existing_omission_family_k{k}", tuple("ABTQRS"), [
        ("A", 4*k-2), ("ARS", 2*k), ("B", 5*k-2), ("BRS", 2*k-2),
        ("BTRS", 1), ("BQRS", 1), ("T", 3*k-1), ("Q", 3*k-1),
        ("TR", 2*k-1), ("TS", 2*k-1), ("QR", 2*k-1), ("QS", 2*k-1)],
        "A", dict(zip("ABTQRS", "BSRSSR")), tuple("TQ"))
    assert row["W"] == 13*k-4 and row["OPT"] == 14*k-4
    for order in row["orders"]:
        assert F(order["chi"]) == F(1, 2)
        assert F(order["D"]) == k-F(1, 2)
        assert F(order["R_add"]) == 14*k-5
        assert F(order["R_last"]) == 14*k-F(9, 2)
        assert F(order["R_add"]) > row["W"]
    family.append(row)

print(json.dumps({"status": "pass; translations only; Q-CAG-HALF OPEN",
                  "PFR_OPT_14": small, "omission_family": family}, indent=2))
