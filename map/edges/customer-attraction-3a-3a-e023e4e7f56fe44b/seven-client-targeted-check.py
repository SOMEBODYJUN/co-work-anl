"""One fixed seven-client check; no search, LP, or normative solver import.

The already-proved CA-EXACT-PURE-SPE-ALL recurrence computes the complete set
of attainable terminal counts at each count state. Equal-count ordered nodes
share this set only; certificate expansion below separately visits every
ordered child, so no anonymous policy constraint is imposed.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import product
import json

P, M = 4, 5
TYPES = ((frozenset((1,)), 2),
         (frozenset((0, 1, 2)), 4),
         (frozenset((2, 3)), 1))
PATH = (1, 1, 1, 2, 0)


def child(k, a):
    return tuple(v + (j == a) for j, v in enumerate(k))


def count(h):
    return tuple(h.count(a) for a in range(P))


def payoff(c, a):
    assert c[a] > 0
    return sum((Fraction(n, sum(c[b] for b in likes))
                for likes, n in TYPES if a in likes), Fraction(0))


def welfare(c):
    return sum(n for likes, n in TYPES if sum(c[b] for b in likes) > 0)


@lru_cache(None)
def outcomes(k):
    if sum(k) == M:
        return frozenset((k,))
    children = tuple(outcomes(child(k, a)) for a in range(P))
    minima = tuple(min(payoff(c, a) for c in children[a]) for a in range(P))
    gate = max(minima)
    kept = frozenset(c for a in range(P) for c in children[a]
                     if payoff(c, a) >= gate)
    assert kept
    return kept


def minima_at(k):
    return tuple(min(payoff(c, a) for c in outcomes(child(k, a)))
                 for a in range(P))


def local_certificate(prefix, first, target):
    """Expand a local SPE attaining the gate, over all ordered descendants."""
    actions = {}

    def expand(h, wanted, forced=None):
        if len(h) == M:
            assert count(h) == wanted
            return
        k = count(h)
        gate = max(minima_at(k))
        good = [a for a in range(P)
                if wanted in outcomes(child(k, a)) and payoff(wanted, a) >= gate]
        a = min(good) if forced is None else forced
        assert a in good
        actions[h] = a
        for b in range(P):
            nxt = wanted if b == a else min(
                outcomes(child(k, b)), key=lambda c: (payoff(c, b), c))
            expand(h + (b,), nxt)

    expand(prefix, target, first)
    # This is a definition-level check of this one expanded local strategy.
    @lru_cache(None)
    def finish(h):
        return count(h) if len(h) == M else finish(h + (actions[h],))

    comparisons = 0
    for h, a in sorted(actions.items()):
        chosen = payoff(finish(h), a)
        for b in range(P):
            assert chosen >= payoff(finish(h + (b,)), b)
            comparisons += 1
    root_leaf = finish(prefix)
    assert payoff(root_leaf, first) == max(minima_at(count(prefix)))
    return {
        "first_action": first,
        "terminal_counts": list(root_leaf),
        "first_payoff": str(payoff(root_leaf, first)),
        "ordered_histories": len(actions),
        "comparisons_including_self": comparisons,
        "actions": [{"history": list(h), "action": a}
                    for h, a in sorted(actions.items())],
    }


def run():
    root = outcomes((0,) * P)
    rows = []
    total = Fraction(0)
    for i in range(M):
        h, k = PATH[:i], count(PATH[:i])
        mins = minima_at(k)
        gate = max(mins)
        assert mins == (Fraction(4, 5), Fraction(13, 10),
                        Fraction(13, 10), Fraction(1, 2))
        # Select an argmax-min child and a leaf attaining its minimum.
        a = min(a for a in range(P) if mins[a] == gate)
        target = min(outcomes(child(k, a)), key=lambda c: (payoff(c, a), c))
        cert = local_certificate(h, a, target)
        rows.append({
            "ordered_prefix": list(h), "prefix_counts": list(k),
            "path_action": PATH[i], "gate": str(gate),
            "child_minima": {str(a): str(v) for a, v in enumerate(mins)},
            "child_attainers": {
                str(a): list(min(outcomes(child(k, a)),
                                 key=lambda c: (payoff(c, a), c)))
                for a in range(P)},
            "local_minimum_spe_certificate": cert,
        })
        total += gate
    opt = max(welfare(count(h)) for h in product(range(P), repeat=M))
    ws = sorted({welfare(c) for c in root})
    assert total == Fraction(13, 2) and ws == [7] and opt == 7
    final_k = count(PATH[:-1])
    last_values = {str(a): str(payoff(child(final_k, a), a)) for a in range(P)}
    assert last_values["0"] == "4/5" and last_values["1"] == "13/10"
    return {
        "status": "PASS_ONE_FIXED_INPUT_EXACT_FRACTION_CHECK",
        "scope": "One specified input; no random search, LP, or general budget proof.",
        "semantics": "Complete attainable count sets; ordered certificate children expanded independently.",
        "instance": {"topics": [str(a) for a in range(P)], "players": M,
                     "customers": [{"topics": sorted(b), "multiplicity": n} for b, n in TYPES]},
        "path": list(PATH), "sum_M": str(total), "optimum": opt,
        "root_outcome_count": len(root),
        "root_outcomes": [list(c) for c in sorted(root)],
        "root_welfares": ws, "count_states": outcomes.cache_info().currsize,
        "rows": rows, "last_action_payoffs": last_values,
        "path_last_action_is_best_response": False,
        "ordered_local_histories_checked": sum(r["local_minimum_spe_certificate"]["ordered_histories"] for r in rows),
        "ordered_local_comparisons_including_self": sum(r["local_minimum_spe_certificate"]["comparisons_including_self"] for r in rows),
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
