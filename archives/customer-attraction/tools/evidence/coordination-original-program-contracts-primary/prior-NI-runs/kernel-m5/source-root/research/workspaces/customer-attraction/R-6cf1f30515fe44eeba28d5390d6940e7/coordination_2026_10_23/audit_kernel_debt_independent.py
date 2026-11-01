"""Replay supplied SPEs directly from unit-customer incidence; no solver imports.

m5 checks every ordered node and only excludes fixed-pivot double writes.
m8 checks the entire declared count-policy state space and excludes every
response-update/compress-before-advance route, including pivot changes.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "merge_br_credit_certificate.json"


def audit_five():
    data = json.loads(SOURCE.read_text())
    m = 5
    topics = tuple(frozenset((i, m + i)) for i in range(m)) + (frozenset(range(m)),)
    assert data["m"] == m and tuple(map(frozenset, data["topics"])) == topics
    actions = {tuple(r["counts"]): r["action"] for r in data["policy"]}

    def count(h):
        c = Counter(h)
        return tuple(c[i] for i in range(6))

    @lru_cache(None)
    def finish(h):
        if len(h) == m:
            return h
        return finish(h + (actions[count(h)],))

    def payoff(z, action):
        return sum((Q(1, sum(x in topics[a] for a in z)) for x in topics[action]), Q(0))

    nodes = comparisons = 0
    for depth in range(m):
        for h in product(range(6), repeat=depth):
            nodes += 1
            z = finish(h)
            current = z[depth]
            value = payoff(z, current)
            for deviation in range(6):
                alt = finish(h + (deviation,))
                assert value >= payoff(alt, deviation), (h, current, deviation)
                comparisons += 1

    path = finish(())
    assert path == (5, 5, 5, 4, 3)
    welfare = len(frozenset().union(*(topics[a] for a in path)))
    assert welfare == 7
    # Covering y_i needs A_i, so OPT=10 has the unique multiset A_0,...,A_4.
    assert all(sum(m + i in t for t in topics) == 1 for i in range(m))
    assert len(frozenset().union(*topics[:m])) == 10
    root_slacks = []
    for pivot in range(m):
        h = (pivot,) * 4
        reply = actions[count(h)]
        assert reply == 5
        for old in range(m):
            if old != pivot:
                slack = payoff(h + (reply,), reply) - payoff(h + (old,), old)
                assert slack == Q(11, 5)
                root_slacks.append(slack)

    # A standard fixed-pivot double write must use two such rows initially.
    standard_min = 2 * min(root_slacks)
    half_headroom = 2 * welfare - 10
    assert standard_min == Q(22, 5) > half_headroom == 4

    # Broader replacement operations can change pivot to the newly written R.
    # Start [A0,A1,A2,A3,A4], write A0->R using pivot A1, then
    # write A1->A4 using pivot R: the second row has exactly zero slack.
    rclone = (5,) * 4
    rreply = actions[count(rclone)]
    assert rreply == 4
    second = payoff(rclone + (rreply,), rreply) - payoff(rclone + (1,), 1)
    assert second == 0
    extended_root = [5, 4, 2, 3, 4]
    assert len(set(extended_root)) < len(extended_root)

    out = {
        "status": "PASS",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "ordered_nodes": nodes,
        "exact_deviation_comparisons": comparisons,
        "actual_path": list(path),
        "actual_payoffs": [str(payoff(path, a)) for a in path],
        "W": welfare,
        "OPT": 10,
        "initial_optimal_source_multiset_unique": True,
        "initial_nonpivot_A_to_R_slack": "11/5",
        "standard_fixed_pivot_first_merge_BR_slack": str(standard_min),
        "half_BR_headroom": half_headroom,
        "standard_interface_violation_at_least": str(standard_min-half_headroom),
        "expanded_pivot_route_second_slack": str(second),
        "expanded_route_after_two_updates": extended_root,
        "expanded_route_root_slack": "11/5",
        "scope": "Standard fixed-pivot double-write sufficient condition fails; arbitrary replacement routes are not excluded."
    }
    (BASE / "kernel_debt_independent_audit.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=2))


def audit_eight():
    source = BASE / "merge_br_credit_m8_certificate.json"
    data = json.loads(source.read_text())
    m, q = 8, 9
    topics = tuple(frozenset((i, m + i)) for i in range(m)) + (frozenset(range(m)),)
    assert data["m"] == m and tuple(map(frozenset, data["topics"])) == topics
    actions = {tuple(row["counts"]): row["action"] for row in data["policy"]}

    def compositions(total, width):
        if width == 1:
            yield (total,)
        else:
            for first in range(total + 1):
                for rest in compositions(total-first, width-1):
                    yield (first,) + rest

    expected = {c for depth in range(m) for c in compositions(depth, q)}
    assert set(actions) == expected and len(actions) == 11440

    def child(c, a):
        return c[:a] + (c[a]+1,) + c[a+1:]

    @lru_cache(None)
    def finish(c):
        if sum(c) == m:
            return c
        assert 0 <= actions[c] < q
        return finish(child(c, actions[c]))

    @lru_cache(None)
    def payoff(z, action):
        return sum((Q(1, sum(z[a] for a in range(q) if x in topics[a]))
                    for x in topics[action]), Q(0))

    comparisons = 0
    for c in expected:
        value = payoff(finish(c), actions[c])
        for a in range(q):
            assert value >= payoff(finish(child(c, a)), a), (c, a)
            comparisons += 1
    assert comparisons == 102960
    c = (0,)*q
    path = []
    for _ in range(m):
        path.append(actions[c])
        c = child(c, path[-1])
    assert path == [8,8,8,8,8,8,7,6]
    welfare = len(frozenset().union(*(topics[a] for a in path)))
    assert welfare == 10
    # Every y_i occurs only in A_i. Hence covering all 16 needs exactly all A_i.
    assert all(sum(m+i in topic for topic in topics) == 1 for i in range(m))
    root_slacks = []
    for pivot in range(m):
        clone = tuple(7 if a == pivot else 0 for a in range(q))
        assert actions[clone] == 8
        best = payoff(child(clone, 8), 8)
        assert best == Q(57, 8)
        for old in range(m):
            if old != pivot:
                slack = best-payoff(child(clone, old), old)
                assert slack == Q(41, 8)
                root_slacks.append(slack)
    headroom = 2*welfare-16
    assert min(root_slacks) > headroom == 4
    out = {
        "status": "PASS",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "m": m,
        "complete_count_policy_states": len(expected),
        "exact_deviation_comparisons": comparisons,
        "ordered_history_coverage": "Every ordered history uses its count-policy action. Its every deviated child has the same count transition and replayed payoff; all count states were checked.",
        "actual_path": path,
        "actual_payoffs": [str(payoff(c, a)) for a in path],
        "W": welfare,
        "OPT": 16,
        "unique_optimal_source_multiset": list(range(m)),
        "first_response_update_BR_slack": "41/8",
        "half_BR_headroom": headroom,
        "interface_violation_at_least": "9/8",
        "scope": "All routes starting from an optimal m-list, using genuine clone-response updates and duplicate deletion before each actual-prefix advance, even with arbitrary pivot changes or additional finite updates."
    }
    (BASE / "kernel_debt_m8_independent_audit.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if sys.argv[1:] == ["--m8"]:
        audit_eight()
    elif not sys.argv[1:] or sys.argv[1:] == ["--m5"]:
        audit_five()
    else:
        raise SystemExit("Use --m5 or --m8; no parameter search is implemented.")
