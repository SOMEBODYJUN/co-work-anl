"""Independent exact audit of the two-customer sparse-rent SPE family."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json


def allowed(q, a, b):
    if a >= q:
        return (1,)
    if b >= q:
        return (0,)
    return (0, 1)


def policy(q, history):
    a, b = history.count(0), history.count(1)
    actions = allowed(q, a, b)
    return actions[0] if len(actions) == 1 or not history else 1


def finish(q, history):
    h = tuple(history)
    while len(h) < 2 * q:
        h += (policy(q, h),)
    return h


def payoff(history, player):
    return F(1, history.count(history[player]))


def audit_histories(q):
    nodes = comparisons = 0
    for depth in range(2 * q):
        for history in product((0, 1), repeat=depth):
            prescribed = policy(q, history)
            base = finish(q, history + (prescribed,))
            base_value = payoff(base, depth)
            for action in (0, 1):
                deviation = finish(q, history + (action,))
                assert base_value >= payoff(deviation, depth)
                comparisons += 1
            nodes += 1
    actual = finish(q, ())
    assert actual == (0,) + (1,) * q + (0,) * (q - 1)
    assert actual.count(0) == actual.count(1) == q
    return {"q": q, "ordered_nodes": nodes, "true_comparisons": comparisons}


def audit_all_ties(q):
    @lru_cache(None)
    def endpoints(a, b):
        if a + b == 2 * q:
            return frozenset(((a, b),))
        result = set()
        for action in allowed(q, a, b):
            result.update(endpoints(a + (action == 0), b + (action == 1)))
        return frozenset(result)

    states = checks = 0
    for depth in range(2 * q):
        for a in range(depth + 1):
            b = depth - a
            possibilities = {}
            for action in (0, 1):
                ends = endpoints(a + (action == 0), b + (action == 1))
                possibilities[action] = [F(1, e[action]) for e in ends]
            for prescribed in allowed(q, a, b):
                for alternative in (0, 1):
                    assert min(possibilities[prescribed]) >= max(possibilities[alternative])
                    checks += 1
            if a < q and b < q:
                assert endpoints(a, b) == frozenset(((q, q),))
            states += 1
    return {"q": q, "count_states": states, "all_tie_checks": checks}


def audit_rent(q):
    path = (0,) + (1,) * q + (0,) * (q - 1)
    total = F(0)
    slot_weights = {}
    for j in range(1, q):
        prefix = path[:j]
        future_position = q + 1 + j  # one-based
        future = (path[future_position - 1],)
        value = sum(
            F(prefix.count(x)) * (
                F(1, 1 + prefix.count(x))
                - F(1, 1 + prefix.count(x) + future.count(x))
            )
            for x in (0, 1)
        )
        assert value == F(1, 6)
        assert future_position > j
        theta = F(1, j)
        total += theta * value
        slot_weights[future_position] = slot_weights.get(future_position, F(0)) + j * theta
    gamma = max(slot_weights.values())
    harmonic = sum((F(1, j) for j in range(1, q)), F(0))
    assert gamma == 1 and total == harmonic / 6
    return {"q": q, "W": 2, "Gamma": str(gamma), "weighted_rent": str(total)}


def main():
    report = {
        "status": "passed",
        "ordered_history_audits": [audit_histories(q) for q in range(2, 6)],
        "all_tie_state_audits": [audit_all_ties(q) for q in range(2, 13)],
        "rent_audits": [audit_rent(q) for q in range(2, 31)],
        "scope": "Finite exact checks; general SPE and divergence are proved in the companion note.",
    }
    destination = Path(__file__).with_name("sparse_spe_rent_audit.json")
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "ordered_comparisons": sum(r["true_comparisons"] for r in report["ordered_history_audits"]), "all_tie_checks": sum(r["all_tie_checks"] for r in report["all_tie_state_audits"]), "report": str(destination)}, indent=2))


if __name__ == "__main__":
    main()
