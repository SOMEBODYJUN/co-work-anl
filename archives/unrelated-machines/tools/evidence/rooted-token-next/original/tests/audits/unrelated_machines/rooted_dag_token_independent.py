"""Frozen-body attack: compressed selector bridge, exact independent oracles.

This script imports no repository code. It enumerates all DAGs on <=4 vertices
ordered topologically, and every demand choice in {0 if sink,1,d,d+1,HUGE}.
All legal schedules, all rooted trees, the forward construction for every tree,
and every threshold feasibility equivalence are checked using Fraction.
"""

from fractions import Fraction as F
from itertools import product
import json
import platform

HUGE = (1 << 127) + 17


def all_trees(children, demand, root=0):
    n = len(children)
    pred = [[] for _ in range(n)]
    for v, row in enumerate(children):
        for w in row:
            pred[w].append(v)
    assert not pred[root]
    other = [v for v in range(n) if v != root]
    result = []
    for choices in product(*([None] + pred[v] for v in other)):
        par = [None] * n
        for v, parent in zip(other, choices):
            par[v] = parent
        selected = {root} | {v for v in other if par[v] is not None}
        if any(par[v] not in selected for v in selected - {root}):
            continue
        degree = [0] * n
        for v in selected - {root}:
            degree[par[v]] += 1
        value = min([F(1)] + [F(degree[v], demand[v]) for v in selected if demand[v] > 0])
        result.append((value, par, selected, degree))
    return result


def forward(children, demand, root, tree):
    alpha, parents, _, _ = tree
    n = len(children)
    old_children = [[] for _ in range(n)]
    for v in range(n):
        if parents[v] is not None:
            old_children[parents[v]].append(v)
    tree_children = [[] for _ in range(n)]
    selected = {root}
    frontier = [root]
    while frontier:
        v = frontier.pop()
        tree_children[v] = old_children[v][:demand[v]]
        assert len(tree_children[v]) <= min(demand[v], len(children[v]))
        if demand[v] > 0:
            assert len(tree_children[v]) >= alpha * demand[v]
        selected.update(tree_children[v])
        frontier.extend(tree_children[v])
    loads = [F(0)] * n
    loads[root] = 1
    for v in range(n):
        if demand[v] > 0:
            loads[v] += 1 - F(len(tree_children[v]), demand[v])
        for w in tree_children[v]:
            loads[w] += 1
    assert max(loads) <= 2 - alpha


def all_schedules(children, demand, root, beta):
    n = len(children)
    jobs = [(v, a) for v in range(n) for a in range(min(demand[v], len(children[v])))]
    domains = [[v] + children[v] for v, _ in jobs]
    initial = [F(0)] * n
    initial[root] = 1
    for v in range(n):
        if demand[v] > 0:
            q = min(demand[v], len(children[v]))
            initial[v] += 1 - F(q, demand[v])
    opt = None
    count = decoded = 0
    for dest in product(*domains):
        loads = initial.copy()
        sent = [[] for _ in range(n)]
        incoming = [[] for _ in range(n)]
        for (v, _), w in zip(jobs, dest):
            if w == v:
                loads[v] += F(1, demand[v])
            else:
                loads[w] += 1
                sent[v].append(w)
                incoming[w].append(v)
        c = max(loads)
        opt = c if opt is None else min(opt, c)
        count += 1
        if c < 2:
            assert all(len(x) <= 1 for x in incoming)
            assert incoming[root] == []
            selected = {root}
            frontier = [root]
            while frontier:
                v = frontier.pop()
                for w in sent[v]:
                    assert w not in selected
                    selected.add(w)
                    frontier.append(w)
            ratios = [F(1)]
            for v in selected:
                if demand[v] > 0:
                    assert loads[v] == 2 - F(len(sent[v]), demand[v])
                    ratios.append(F(len(sent[v]), demand[v]))
            b = min(ratios)
            assert 2 - c <= b <= beta
            decoded += 1
    assert opt == 2 - beta
    return count, decoded


def audit_instance(children, demand, root=0):
    trees = all_trees(children, demand, root)
    beta = max(tree[0] for tree in trees)
    for tree in trees:
        forward(children, demand, root, tree)
    schedules, decoded = all_schedules(children, demand, root, beta)
    gamma = {F(1)}
    for v in range(len(children)):
        for h in range(1, min(demand[v], len(children[v])) + 1):
            gamma.add(F(h, demand[v]))
    if beta > 0:
        assert beta in gamma
    assert len(gamma) <= 1 + sum(map(len, children))
    for tau in gamma:
        scaled = [0 if k == 0 else (tau.numerator * k + tau.denominator - 1) // tau.denominator for k in demand]
        scaled_trees = all_trees(children, scaled, root)
        scaled_beta = max(tree[0] for tree in scaled_trees)
        assert (scaled_beta == 1) == (tau <= beta)
        for new_tree in scaled_trees:
            new_b, _, selected, degree = new_tree
            old_b = min([F(1)] + [F(degree[v], demand[v]) for v in selected if demand[v] > 0])
            assert old_b >= tau * new_b
    return len(trees), schedules, decoded, len(gamma), beta


def main():
    graphs = instances = trees = schedules = decoded = thresholds = 0
    boundary = {"zero_beta": 0, "unit_beta": 0, "intermediate_beta": 0,
                "huge_demand_instances": 0, "deadend_instances": 0}
    for n in range(1, 5):
        possible_edges = [(v, w) for v in range(n) for w in range(v + 1, n)]
        for bits in product((0, 1), repeat=len(possible_edges)):
            children = [[] for _ in range(n)]
            for yes, (v, w) in zip(bits, possible_edges):
                if yes:
                    children[v].append(w)
            graphs += 1
            choices = []
            for row in children:
                d = len(row)
                choices.append(sorted({1, d, d + 1, HUGE} - ({0} if d else set())))
            for demand in product(*choices):
                nt, ns, nd, ng, beta = audit_instance(children, demand)
                trees += nt
                schedules += ns
                decoded += nd
                thresholds += ng
                instances += 1
                boundary["zero_beta" if beta == 0 else "unit_beta" if beta == 1 else "intermediate_beta"] += 1
                boundary["huge_demand_instances"] += HUGE in demand
                boundary["deadend_instances"] += any(demand[v] > 0 and not children[v] for v in range(n))
    # Arbitrary root index, unreachable component, and mixed huge demand.
    extra = [
        ([[1], [], [3], []], [HUGE, 0, 1, 0], 2),
        ([[], [2, 3], [], []], [HUGE, 2, 0, 0], 1),
        ([[1], [], []], [1, HUGE, 0], 0),
    ]
    for children, demand, root in extra:
        audit_instance(children, demand, root)
    print(json.dumps({"python": platform.python_version(), "arithmetic": "Fraction",
                      "huge_demand": str(HUGE), "huge_demand_bits": HUGE.bit_length(),
                      "graphs": graphs, "instances": instances,
                      "rooted_trees_checked": trees,
                      "legal_schedules_checked": schedules,
                      "schedules_below_2_decoded": decoded,
                      "threshold_equivalences_checked": thresholds,
                      "additional_root_and_deadend_cases": len(extra),
                      "boundary_counts": boundary}, indent=2))


if __name__ == "__main__":
    main()
