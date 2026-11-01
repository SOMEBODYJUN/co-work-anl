"""Independent exact audit of SA and the alpha=1 entrant bridge.

Standard library only. The input is a closed strategy automaton; its expected
path, desired outcomes and discovery statistics are not used for verification.
"""
from fractions import Fraction as F
from functools import lru_cache
import argparse
import gzip
import json
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = ROOT / "research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz"


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def main():
    packet = json.loads(gzip.decompress(SOURCE.read_bytes()))
    instance = packet["instance"]
    topics = instance["topics"]
    m, p = instance["players"], len(topics)
    # Expand the multiset into different unit customers before every utility
    # calculation; no weighted-customer convention is needed.
    customers = tuple(frozenset(c["topics"])
                      for c in instance["customers"]
                      for _ in range(c["multiplicity"]))
    assert all(type(c["multiplicity"]) is int and c["multiplicity"] > 0
               for c in instance["customers"])
    denominator = lcm(*range(1, m + 1))

    @lru_cache(None)
    def payoffs(q):
        result = [0] * p
        for interests in customers:
            load = sum(q[a] for a in interests)
            if load:
                amount = denominator // load
                for a in interests:
                    result[a] += amount
        return tuple(result)

    def welfare(q):
        return sum(any(q[a] for a in interests) for interests in customers)

    nodes = packet["nodes"]
    root = packet["root"]
    visited = set()
    order = []
    stack = [root]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        node = nodes[v]
        q = tuple(node["counts"])
        assert len(q) == p and all(type(x) is int and x >= 0 for x in q)
        depth = sum(q)
        assert depth <= m
        order.append(v)
        if depth == m:
            assert node.get("terminal") is True and "children" not in node
        else:
            assert len(node["children"]) == p and 0 <= node["action"] < p
            for a, child in enumerate(node["children"]):
                target = list(q)
                target[a] += 1
                assert 0 <= child < len(nodes)
                assert nodes[child]["counts"] == target
                stack.append(child)
    assert len(visited) == len(nodes)
    assert nodes[root]["counts"] == [0] * p

    terminal = {}
    comparisons = 0
    min_slack = None
    for v in sorted(order, key=lambda w: sum(nodes[w]["counts"]), reverse=True):
        node = nodes[v]
        if sum(node["counts"]) == m:
            terminal[v] = tuple(node["counts"])
            continue
        action = node["action"]
        terminal[v] = terminal[node["children"][action]]
        actual = payoffs(terminal[v])[action]
        for a, child in enumerate(node["children"]):
            slack = actual - payoffs(terminal[child])[a]
            assert slack >= 0, (v, a, slack)
            min_slack = slack if min_slack is None else min(min_slack, slack)
            comparisons += 1

    path = []
    current = root
    while sum(nodes[current]["counts"]) < m:
        action = nodes[current]["action"]
        path.append(action)
        current = nodes[current]["children"][action]
    q = terminal[root]
    W = welfare(q)
    static = []
    for query in range(p):
        value = F(0)
        for original, number in enumerate(q):
            changed = list(q)
            if number:
                changed[original] -= 1
                changed[query] += 1
                value += number * F(payoffs(tuple(changed))[query], denominator)
        direct = F(0)
        for interests in customers:
            if query in interests:
                load = sum(q[a] for a in interests)
                direct += F(m + 1, load + 1) if load else m
        assert direct == value
        static.append(value)
    entrant = [sum((F(1, 1 + sum(q[a] for a in B))
                    for B in customers if query in B), F(0))
               for query in range(p)]
    G = sum((F(1, 1 + sum(q[a] for a in B))
             for B in customers if any(q[a] for a in B)), F(0))
    M = max(entrant)
    alpha0 = F(m - 1, m)
    alpha0_G = sum((1 / (1 + alpha0 * sum(q[a] for a in B))
                    for B in customers if any(q[a] for a in B)), F(0))
    alpha0_T = sum((1 / (1 + alpha0 * sum(q[a] for a in B))
                   for B in customers if 2 in B), F(0))
    opt = -1
    opt_min_static = None
    opt_max_static = None
    optimal_vectors = 0
    best_tuple = None
    worst_tuple = None
    enumerated = 0
    for comparison in compositions(m, p):
        enumerated += 1
        coverage = welfare(comparison)
        average = sum((comparison[a] * static[a] / m for a in range(p)), F(0))
        if coverage > opt:
            opt = coverage
            opt_min_static = opt_max_static = average
            optimal_vectors = 1
            best_tuple = comparison
            worst_tuple = comparison
        elif coverage == opt:
            optimal_vectors += 1
            if average > opt_max_static:
                opt_max_static = average
                worst_tuple = comparison
            if average < opt_min_static:
                opt_min_static = average
                best_tuple = comparison
    bound = F(m + 1, m) * W
    assert q == (2, 1, 0, 0, 0, 10) and W == 33 and opt == 36
    assert static == [F(70, 3), F(21), F(39), F(34), F(34), F(350, 11)]
    assert static[2] - bound == F(45, 13)
    assert M == 3 and G == F(359, 66) and m * M - W - G == F(37, 66)
    assert alpha0 == F(12, 13) and alpha0_T == 3
    assert m * alpha0_T - W - alpha0_G == F(29481, 123025)
    assert best_tuple == (1, 10, 1, 0, 0, 1) and opt_min_static == F(10037, 429)
    assert worst_tuple == (1, 1, 10, 0, 0, 1) and opt_max_static == F(15383, 429)
    assert opt_max_static - bound == F(137, 429)
    report = {
        "source": str(SOURCE.relative_to(ROOT)),
        "status": "Exact independent complete-history SPE and arithmetic audit passed",
        "method": "Unit-customer expansion, closed action-edge induction, reverse terminal evaluation; no project model or solver import",
        "players": m, "unit_customers": len(customers), "automaton_nodes": len(nodes),
        "checked_comparisons_including_self": comparisons,
        "minimum_SPE_slack": str(F(min_slack, denominator)),
        "path": [topics[a] for a in path], "terminal_counts": q,
        "W": W, "OPT": opt, "half_slack": 2 * W - opt,
        "static_D_by_topic": {a: str(v) for a, v in zip(topics, static)},
        "SA_bound": str(bound),
        "SA_violations": {a: str(v - bound) for a, v in zip(topics, static) if v > bound},
        "alpha1_entrant_by_topic": {a: str(v) for a, v in zip(topics, entrant)},
        "alpha1_M": str(M), "alpha1_G": str(G),
        "alpha1_bridge_violation": str(m * M - W - G),
        "alpha0": str(alpha0), "alpha0_G": str(alpha0_G),
        "alpha0_T": str(alpha0_T),
        "alpha0_T_bridge_violation": str(m * alpha0_T - W - alpha0_G),
        "optimal_count_vectors": optimal_vectors, "count_vectors_enumerated": enumerated,
        "minimum_optimal_combination_average_D": str(opt_min_static),
        "maximum_optimal_combination_average_D": str(opt_max_static),
        "minimum_average_optimal_counts": best_tuple,
        "maximum_average_optimal_counts": worst_tuple,
        "maximum_average_SA_violation": str(opt_max_static - bound),
        "scope": "Per-query SA and alpha=1 actual entrant bridge are false; half and the existence of an optimal-combination average SA remain unrefuted by this instance"
    }
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        raise FileExistsError(args.output)
    report = main()
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output is not None:
        args.output.write_text(rendered)
    print(rendered, end="")
