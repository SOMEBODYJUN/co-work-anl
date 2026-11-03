"""Three exact regressions for one general formula; no instance/policy sweep."""

from fractions import Fraction as F
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver


def strf(value):
    return str(F(value))


def check(m, a, b):
    pairs = [(e, k) for e in range(m) for k in range(m - 1)]
    coverage = [
        {("economic", e, j) for j in range(a)}
        | {("bank", k, j) for j in range(b)}
        for e, k in pairs
    ]
    instance = Instance.from_topic_sets(coverage, players=m)
    solver = ExactSPESolver(instance)
    path = tuple(pairs.index((0, k)) for k in range(m - 1)) + (
        pairs.index((1, 0)),
    )
    utilities = instance.player_payoffs(path)
    menus = [solver.threshold(instance.counts(path[:i])) for i in range(m - 1)]
    assert menus[1:] == [F(a) + F(b, 2)] * (m - 2)
    root_floor = F(a, m - 1) + F(b, 2)
    assert menus[0] >= root_floor
    threshold = F(2 * a * (m - 2), m - 1)
    if b >= threshold:
        assert menus[0] == root_floor
    counts = instance.counts(path, terminal=True)
    W = instance.welfare(counts)
    OPT = instance.optimal_welfare()
    assert W == 2 * a + (m - 1) * b
    assert OPT == m * a + (m - 1) * b
    signed = [menus[i] - utilities[i] for i in range(m - 1)]
    positive = [max(x, F(0)) for x in signed]
    negative = [max(-x, F(0)) for x in signed]
    C = 2 * sum(positive) - sum(negative) + max(positive) + max(negative)
    budget = 2 * W - OPT + C
    if b <= threshold:
        lower = F(a) * (m - 1 + F(1, m - 1)) + F(b, 2)
        assert budget >= lower > 0
    else:
        lower = F((m + 1) * b, 2) + F(2 * a, m - 1)
        assert budget == lower > 0
    # Last BR, including bank alternatives and all legal economic choices.
    prefix = instance.counts(path[:-1])
    last_best = max(
        instance.topic_payoff(t, tuple(q + (j == t) for j, q in enumerate(prefix)))
        for t in range(instance.topic_count)
    )
    assert utilities[-1] == last_best
    return {
        "m": m,
        "a": a,
        "b": b,
        "regime": "below" if b < threshold else "threshold" if b == threshold else "above",
        "menus": list(map(strf, menus)),
        "target_utilities": list(map(strf, utilities)),
        "signed_defects": list(map(strf, signed)),
        "W": W,
        "OPT": OPT,
        "B_plus_C": strf(budget),
        "analytic_lower": strf(lower),
        "last_BR": True,
    }


if __name__ == "__main__":
    # Three sides of the same algebraic breakpoint; these do not form a search.
    results = [check(4, 3, b) for b in (2, 4, 6)]
    output = {
        "scope": "Implementation regression only; arbitrary-m argument is analytic.",
        "cases": results,
    }
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))
