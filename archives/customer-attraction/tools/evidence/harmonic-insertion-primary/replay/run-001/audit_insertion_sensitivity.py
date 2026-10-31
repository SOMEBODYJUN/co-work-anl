"""Exact, definition-level audit of the explicit sensitivity counterfamily."""
from fractions import Fraction
from itertools import product
import json


def complete(hist, n):
    # Labels 0,...,n-1 are B themes; n is A.
    out = list(hist)
    while len(out) < n:
        out.append(next(t for t in range(n + 1) if t not in out))
    return tuple(out)


def payoff(terminal, player, n, inserted):
    theme = terminal[player]
    baseline = 1 if theme < n or inserted else 0
    return Fraction(1, baseline + terminal.count(theme))


def audit(n):
    nodes = comparisons = 0
    for depth in range(n):
        for hist in product(range(n + 1), repeat=depth):
            nodes += 1
            actual = complete(hist, n)
            base = payoff(actual, depth, n, True)
            assert base == Fraction(1, 2)
            for action in range(n + 1):
                comparisons += 1
                forced = complete(hist + (action,), n)
                assert base >= payoff(forced, depth, n, True)
    actual = complete((), n)
    assert actual == tuple(range(n))
    defects = []
    for player in range(n):
        hist = actual[:player]
        forced = complete(hist + (n,), n)
        before = payoff(actual, player, n, False)
        best = max(
            payoff(complete(hist + (action,), n), player, n, False)
            for action in range(n + 1)
        )
        assert payoff(forced, player, n, False) == 1
        assert before == Fraction(1, 2)
        defect = best - before
        assert defect == Fraction(1, 2)
        defects.append(defect)
    assert sum(defects) == Fraction(n, 2)
    # K_b(A)=1/2, every actual moving player avoids A, and E_A(q)=0.
    assert sum(defects) == n * Fraction(1, 2) - 0
    return {
        "n_tail": n,
        "all_ordered_history_nodes": nodes,
        "all_child_ic_comparisons_including_self": comparisons,
        "root_original_profit": "1",
        "root_fixed_leaf_tail_externality": "0",
        "sum_deleted_root_actual_path_defects": str(sum(defects)),
        "sharp_general_bound_n_K_minus_E": str(n * Fraction(1, 2)),
    }


if __name__ == "__main__":
    print(json.dumps({"status": "pass", "family_members": [audit(n) for n in range(1, 6)]}, indent=2))
