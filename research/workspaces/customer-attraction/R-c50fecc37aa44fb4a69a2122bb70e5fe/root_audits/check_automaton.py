"""Independent definition-level checker for an acyclic pure-strategy automaton.

No game package, equilibrium solver, discovery code, or floating point is used.
Each observed action has a successor. Unfolding those edges defines a strategy
on every ordered history, including histories sharing a count vector.
"""
from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path


def check(packet):
    instance = packet["instance"]
    p = len(instance["topics"])
    m = instance["players"]
    assert type(m) is int and m >= 1 and p >= 1
    customers = []
    for row in instance["customers"]:
        n = row["multiplicity"]
        interest = frozenset(row["topics"])
        assert type(n) is int and n >= 0
        assert all(type(a) is int and 0 <= a < p for a in interest)
        customers.extend([interest] * n)
    nodes = packet["nodes"]
    assert nodes and 0 <= packet["root"] < len(nodes)
    assert nodes[packet["root"]]["counts"] == [0] * p
    reached = set()
    decisions = comparisons = 0

    @lru_cache(None)
    def values(q):
        # Literal sums over different unit customers, not compressed type rows.
        result = [F(0) for _ in range(p)]
        for interest in customers:
            load = sum(q[a] for a in interest)
            if load:
                for a in interest:
                    if q[a]:
                        result[a] += F(1, load)
        return tuple(result)

    @lru_cache(None)
    def visit(index):
        nonlocal decisions, comparisons
        assert type(index) is int and 0 <= index < len(nodes)
        reached.add(index)
        node = nodes[index]
        q = tuple(node["counts"])
        assert len(q) == p and all(type(x) is int and x >= 0 for x in q)
        total = sum(q)
        assert total <= m
        if total == m:
            assert node.get("terminal") is True
            assert "children" not in node and "action" not in node
            return q
        assert not node.get("terminal", False)
        chosen = node["action"]
        assert type(chosen) is int and 0 <= chosen < p
        assert len(node["children"]) == p
        children = []
        for action, target in enumerate(node["children"]):
            assert type(target) is int and 0 <= target < len(nodes)
            wanted = tuple(q[a] + int(a == action) for a in range(p))
            assert tuple(nodes[target]["counts"]) == wanted
            children.append(visit(target))
        actual = children[chosen]
        incumbent = values(actual)[chosen]
        for action, outcome in enumerate(children):
            assert incumbent >= values(outcome)[action], (index, action)
            comparisons += 1
        if "desired" in node:
            assert actual == tuple(node["desired"])
        decisions += 1
        return actual

    root_q = visit(packet["root"])
    assert reached == set(range(len(nodes))), "unreachable extra certificate nodes"
    if "expected_terminal_counts" in packet:
        assert root_q == tuple(packet["expected_terminal_counts"])
    path = []
    at = packet["root"]
    while sum(nodes[at]["counts"]) < m:
        action = nodes[at]["action"]
        path.append(action)
        at = nodes[at]["children"][action]
    if "expected_path" in packet:
        assert path == packet["expected_path"]
    loads = [sum(root_q[a] for a in interest) for interest in customers]
    welfare = sum(load > 0 for load in loads)
    assert sum(root_q[a] * values(root_q)[a] for a in range(p)) == welfare
    # Enumerate subsets rather than count tuples: repeated themes add no cover.
    optimal = max(sum(bool(interest.intersection(a for a in range(p)
                       if mask & (1 << a))) for interest in customers)
                  for mask in range(1 << p) if mask.bit_count() <= m)
    alpha = F(m - 1, m)
    query = tuple(sum((F(1, 1 + alpha * load)
                       for interest, load in zip(customers, loads) if a in interest), F(0))
                  for a in range(p))
    M = max(query)
    G = sum((F(1, 1 + alpha * load) for load in loads if load), F(0))
    # Exact always-valid coverage inequality with the actual fractional tax.
    assert optimal <= m * M + welfare - G
    return {"status": "PASS", "unit_customers": len(customers), "players": m,
            "topics": p, "automaton_nodes": len(nodes), "decision_nodes": decisions,
            "comparisons_including_self": comparisons, "path": path,
            "counts": list(root_q), "payoff_per_topic": list(map(str, values(root_q))),
            "W": welfare, "OPT": optimal, "alpha": str(alpha),
            "fractional_queries": list(map(str, query)), "M": str(M), "G_C": str(G),
            "mM_minus_W_minus_G": str(m * M - welfare - G),
            "half_slack": 2 * welfare - optimal}


def self_checks():
    empty = {"instance": {"topics": ["empty"], "players": 1, "customers": []},
             "root": 0, "nodes": [{"counts": [0], "action": 0, "children": [1]},
                                  {"counts": [1], "terminal": True}]}
    assert check(empty)["W"] == 0
    boundary = {"instance": {"topics": ["A", "B"], "players": 1,
                              "customers": [{"topics": [0], "multiplicity": 1},
                                            {"topics": [1], "multiplicity": 2}]},
                "root": 0,
                "nodes": [{"counts": [0, 0], "action": 1, "children": [1, 2]},
                          {"counts": [1, 0], "terminal": True},
                          {"counts": [0, 1], "terminal": True}]}
    assert check(boundary)["OPT"] == 2
    bad = copy.deepcopy(boundary)
    bad["nodes"][0]["action"] = 0
    try:
        check(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError("profitable one-player deviation was accepted")
    bad = copy.deepcopy(boundary)
    bad["nodes"][0]["children"] = [2, 2]
    try:
        check(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError("wrong observed-action transition was accepted")
    return {"empty_customer_boundary": "PASS", "one_player_boundary": "PASS",
            "profitable_deviation_rejected": "PASS", "incorrect_edge_rejected": "PASS"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    raw = args.packet.read_bytes()
    packet = json.loads(gzip.decompress(raw) if args.packet.suffix == ".gz" else raw)
    result = {"scope": "One fixed full-history pure SPE; no general half theorem",
              "packet_sha256": hashlib.sha256(raw).hexdigest(),
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "self_checks": self_checks(), "audit": check(packet)}
    if args.output:
        with args.output.open("x") as stream:
            json.dump(result, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
