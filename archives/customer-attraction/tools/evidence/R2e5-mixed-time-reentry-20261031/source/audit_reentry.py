"""Definition-level Fraction audit; no CAG model, BI solver, or LP imports."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json


def terminal(k, m, actions, prefix=()):
    h = tuple(prefix)
    while len(h) < m:
        h += (actions[h],)
    return h


def payoff(topics, z, actor):
    return sum((F(1, sum(x in topics[a] for a in z))
                for x in topics[z[actor]]), F(0))


def check_spe(topics, actions, m):
    comparisons = 0
    minimum = None
    for depth in range(m):
        for h in product(range(len(topics)), repeat=depth):
            actual = terminal(len(topics), m, actions, h)
            u = payoff(topics, actual, depth)
            for a in range(len(topics)):
                dev = terminal(len(topics), m, actions, h + (a,))
                slack = u - payoff(topics, dev, depth)
                assert slack >= 0, (h, a, slack)
                minimum = slack if minimum is None else min(minimum, slack)
                comparisons += 1
    return {"decision_histories": len(actions),
            "all_action_comparisons": comparisons, "minimum_slack": str(minimum)}


def reenter(topics, actions, m, schedule, forced):
    h = ()
    forced = dict(zip(schedule, forced))
    for i in range(m):
        h += (forced[i] if i in forced else actions[h],)
    return h


def endpoint_set(topics, actions, m, schedule):
    return {reenter(topics, actions, m, schedule, forced)
            for forced in product(range(len(topics)), repeat=len(schedule))}


def query_price(topics, query, z):
    return sum((F(1, 1 + sum(x in topics[a] for a in z))
                for x in topics[query]), F(0))


def psi(topics, actions, m, schedule, query):
    return min(query_price(topics, query, z)
               for z in endpoint_set(topics, actions, m, schedule))


def main():
    k1 = (frozenset({"a1", "a2"}), frozenset({"b1"}))
    k2 = (frozenset({"c1", "c2"}), frozenset({"d1", "d2"}))
    s1 = {(): 1, (0,): 0, (1,): 0}
    s2 = {(): 0, (0,): 1, (1,): 0}
    components = [(k1, s1), (k2, s2)]
    product_labels = list(product(range(2), repeat=2))
    prod_topics = tuple(k1[a] | k2[b] for a, b in product_labels)
    prod_actions = {}
    for depth in range(2):
        for h in product(range(4), repeat=depth):
            projected = [tuple(product_labels[a][j] for a in h) for j in range(2)]
            choice = tuple(components[j][1][projected[j]] for j in range(2))
            prod_actions[h] = product_labels.index(choice)

    all_games = components + [(prod_topics, prod_actions)]
    checks = [check_spe(t, s, 2) for t, s in all_games]
    vectors = [[psi(t, s, 2, (i,), 0) for i in range(2)] for t, s in all_games]
    assert vectors == [[F(2, 3), F(1)], [F(1), F(2, 3)], [F(5, 3), F(5, 3)]]
    separate = sum((min(row) for row in vectors[:2]), F(0))
    synchronized = min(vectors[2])
    assert (separate, synchronized) == (F(4, 3), F(5, 3))

    nested_checks = 0
    for topics, actions in all_games:
        schedules = [j for d in range(3) for j in combinations(range(2), d)]
        sets = {j: endpoint_set(topics, actions, 2, j) for j in schedules}
        for j in schedules:
            for jj in schedules:
                if set(j) <= set(jj):
                    assert sets[j] <= sets[jj]
                    nested_checks += 1
        assert sets[(0, 1)] == set(product(range(len(topics)), repeat=2))
    double = psi(prod_topics, prod_actions, 2, (0, 1), 0)
    assert double == F(4, 3)

    # Check the exact synchronized product identity for every query topic and J.
    product_identity_checks = 0
    for schedule in [(), (0,), (1,), (0, 1)]:
        for q, (q1, q2) in enumerate(product_labels):
            lhs = psi(prod_topics, prod_actions, 2, schedule, q)
            rhs = psi(k1, s1, 2, schedule, q1) + psi(k2, s2, 2, schedule, q2)
            assert lhs == rhs
            product_identity_checks += 1

    report = {
        "scope": "Two specified complete unit-customer SPE and their product only; no universal bridge or half proof.",
        "customers": [len(set().union(*t)) for t, _ in all_games],
        "SPE_checks": checks,
        "actual_profiles": [list(terminal(len(t), 2, s)) for t, s in all_games],
        "fixed_pure_query_single_reentry_vectors": [[str(v) for v in row] for row in vectors],
        "sum_component_best_times": str(separate),
        "product_synchronized_best_time": str(synchronized),
        "product_two_reentries": str(double),
        "endpoint_nesting_checks": nested_checks,
        "product_identity_checks": product_identity_checks,
        "all_checks_passed": True,
    }
    target = Path(__file__).with_name("audit_reentry.json")
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
