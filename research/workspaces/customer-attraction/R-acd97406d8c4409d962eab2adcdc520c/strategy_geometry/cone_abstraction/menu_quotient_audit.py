"""Independent Fraction audit of the complete-strategy outcome-menu quotient.

This is a structural identity check and one strict finite illustration.  It is
not an enumeration of strategy cones and is not a general half-coverage proof.
Only the Python standard library is used; no repository solver is imported.
"""

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def main():
    labels = 2
    players = 4
    histories = tuple(h for d in range(players) for h in product(range(labels), repeat=d))
    policy = {(): 0, (0,): 0, (1,): 0,
              (0, 0): 1, (0, 1): 0, (1, 0): 1, (1, 1): 0}
    # Last mover balances the two disjoint private populations.  This rule is
    # anonymous in prefix counts; each count class has exactly one reply.
    for h in product(range(labels), repeat=3):
        policy[h] = 1 if h.count(0) >= 2 else 0
    assert set(policy) == set(histories)

    def terminal(h):
        h = tuple(h)
        while len(h) < players:
            h += (policy[h],)
        return tuple(h.count(a) for a in range(labels))

    def payoff(a, q):
        return tuple(F(1, sum(q[b] for b in range(labels) if mask & (1 << b)))
                     if mask & (1 << a) else F(0)
                     for mask in range(1, 1 << labels))

    menus = {h: tuple(terminal(h + (a,)) for a in range(labels)) for h in histories}
    rows = {(h, a): tuple(x - y for x, y in zip(payoff(policy[h], terminal(h)),
                                                 payoff(a, terminal(h + (a,)))))
            for h in histories for a in range(labels)}
    # The exact terminal-count menu and the complete payoff-vector menu agree.
    for h in histories:
        for g in histories:
            count_equal = menus[h] == menus[g]
            payoff_equal = all(payoff(a, menus[h][a]) == payoff(a, menus[g][a])
                               for a in range(labels))
            assert count_equal == payoff_equal

    classes = defaultdict(list)
    for h in histories:
        classes[menus[h]].append(h)
    reciprocal_pairs = 0
    decomposition_checks = 0
    for menu, nodes in classes.items():
        representative = nodes[0]
        b = policy[representative]
        selected = {policy[h] for h in nodes}
        for h in nodes:
            a = policy[h]
            assert rows[(h, b)] == tuple(-x for x in rows[(representative, a)])
            reciprocal_pairs += a != b
            for t in range(labels):
                # Gamma_(h,t) = (M(a)-M(b)) + (M(b)-M(t)).
                reconstructed = tuple(x + y for x, y in zip(rows[(h, b)],
                                                             rows[(representative, t)]))
                assert reconstructed == rows[(h, t)]
                decomposition_checks += 1
        for a in selected:
            assert any(policy[h] == a for h in nodes)

    mass = (F(1), F(1), F(1))  # all three formal customer types positive
    comparisons = {str((h, a)): str(dot(row, mass)) for (h, a), row in rows.items()}
    assert all(dot(row, mass) >= 0 for row in rows.values())
    assert rows[((0, 1), 1)] == (F(1, 2), F(-1, 2), F(0))
    assert rows[((1, 0), 0)] == (F(-1, 2), F(1, 2), F(0))
    # Conversely these two inequalities force r_A = r_B.  Every other row is
    # nonnegative at r_A = r_B >= 0, for arbitrary r_AB >= 0.
    for row in rows.values():
        assert row[0] + row[1] >= 0
        assert row[2] == 0
    terminal_classes = defaultdict(set)
    for h in histories:
        if len(h) == players - 1:
            terminal_classes[tuple(h.count(a) for a in range(labels))].add(policy[h])
    assert all(len(actions) == 1 for actions in terminal_classes.values())
    report = {
        "status": "exact structural audit; no general welfare claim",
        "players": players, "labels": labels,
        "ordered_nodes": len(histories), "comparisons_including_self": len(rows),
        "menu_classes": len(classes), "cross_depth_menu_classes":
            sum(len({len(h) for h in nodes}) > 1 for nodes in classes.values()),
        "reciprocal_pairs_checked": reciprocal_pairs,
        "row_decompositions_checked": decomposition_checks,
        "positive_mass": list(map(str, mass)),
        "all_history_SPE": True,
        "strategy_cone_exact": "r_A = r_B >= 0, r_AB >= 0",
        "terminal_tie_space_dimension": 0,
        "outcome_menu_tie_space_dimension": 1,
        "new_early_row": list(map(str, rows[((0, 1), 1)])),
        "comparisons_at_positive_mass": comparisons,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
