"""Independent Fraction replay of a first-step coverage-opportunity failure.

No game solver or LP is imported. The finite count policy below defines an
action at every ordered continuation history, with the fixed past (2,5).
"""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).parent
Q = 6
R = 3
PREFIX = (2, 5)
WEIGHTS = {1: 3, 3: 1, 4: 6, 8: 1, 10: 5,
           16: 3, 18: 1, 21: 1, 38: 2}
POLICY = {
    (0, 0, 0, 0, 0, 0): 2,
    (1, 0, 0, 0, 0, 0): 1,
    (0, 1, 0, 0, 0, 0): 2,
    (0, 0, 1, 0, 0, 0): 1,
    (0, 0, 0, 1, 0, 0): 1,
    (0, 0, 0, 0, 1, 0): 1,
    (0, 0, 0, 0, 0, 1): 1,
    (2, 0, 0, 0, 0, 0): 1,
    (1, 1, 0, 0, 0, 0): 1,
    (1, 0, 1, 0, 0, 0): 1,
    (1, 0, 0, 1, 0, 0): 1,
    (1, 0, 0, 0, 1, 0): 1,
    (1, 0, 0, 0, 0, 1): 1,
    (0, 2, 0, 0, 0, 0): 2,
    (0, 1, 1, 0, 0, 0): 1,
    (0, 1, 0, 1, 0, 0): 0,
    (0, 1, 0, 0, 1, 0): 1,
    (0, 1, 0, 0, 0, 1): 0,
    (0, 0, 2, 0, 0, 0): 1,
    (0, 0, 1, 1, 0, 0): 1,
    (0, 0, 1, 0, 1, 0): 1,
    (0, 0, 1, 0, 0, 1): 1,
    (0, 0, 0, 2, 0, 0): 0,
    (0, 0, 0, 1, 1, 0): 1,
    (0, 0, 0, 1, 0, 1): 1,
    (0, 0, 0, 0, 2, 0): 1,
    (0, 0, 0, 0, 1, 1): 1,
    (0, 0, 0, 0, 0, 2): 1,
}


def counts(h):
    return tuple(h.count(a) for a in range(Q))


def complete(h):
    h = tuple(h)
    while len(h) < R:
        h += (POLICY[counts(h)],)
    return h


def payoff(action, continuation):
    terminal = PREFIX + tuple(continuation)
    return sum((Fraction(w, sum(bool(mask >> a & 1) for a in terminal))
                for mask, w in WEIGHTS.items() if mask >> action & 1), Fraction())


def new_coverage(choices, excluded=()):
    occupied = PREFIX + tuple(excluded)
    return sum(w for mask, w in WEIGHTS.items()
               if not any(mask >> a & 1 for a in occupied)
               and any(mask >> a & 1 for a in choices))


def new_opt(k, excluded=()):
    choices = list(combinations(range(Q), min(k, Q))) if k else [()]
    vals = [(new_coverage(c, excluded), c) for c in choices]
    return max(vals)


def main():
    comparisons = []
    for depth in range(R):
        for h in product(range(Q), repeat=depth):
            a = POLICY[counts(h)]
            actual = complete(h)
            on = payoff(a, actual)
            gaps = []
            for t in range(Q):
                off = payoff(t, complete(h + (t,)))
                gaps.append(on - off)
                assert on >= off, (h, a, t, on, off)
            comparisons.append(dict(history=h, action=a, payoff=str(on),
                                    minimum_gap=str(min(gaps))))
    actual = complete(())
    profits = [payoff(a, actual) for a in actual]
    p = sum(profits, Fraction())
    delta = new_coverage(actual)
    a = actual[0]
    new_a = new_coverage((a,))
    opt_r, opt_topics = new_opt(R)
    opt_tail, tail_topics = new_opt(R - 1, excluded=(a,))
    local_gap = profits[0] + new_a + opt_tail - opt_r
    global_gap = p + delta - opt_r
    assert local_gap == Fraction(-1, 10)
    assert global_gap > 0
    data = dict(
        scope="Exact counterexample to the first-step sufficient condition only; not to P+Delta or half coverage",
        fixed_ordered_prefix=PREFIX, remaining_players=R, topics=Q,
        customer_types=WEIGHTS, customer_count=sum(WEIGHTS.values()),
        policy=[[list(c), a] for c, a in POLICY.items()],
        ordered_nodes=len(comparisons), comparisons=Q * len(comparisons),
        actual_future_path=actual, future_payoffs=[str(x) for x in profits],
        future_profit=str(p), new_coverage=delta, fresh_optimum=opt_r,
        fresh_optimum_topics=opt_topics, first_new_coverage=new_a,
        tail_fresh_optimum=opt_tail, tail_optimum_topics=tail_topics,
        first_step_gap=str(local_gap), whole_candidate_gap=str(global_gap),
        node_audit=comparisons,
    )
    (HERE / "coverage_step_exact_audit.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({k: v for k, v in data.items() if k not in {"policy", "node_audit"}}, indent=2))


if __name__ == '__main__':
    main()
