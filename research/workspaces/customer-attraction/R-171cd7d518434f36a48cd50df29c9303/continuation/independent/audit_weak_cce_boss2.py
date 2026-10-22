"""Direct individual-deviation audit of the low-welfare CCE construction."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json


def utility(profile, player, m):
    # Labels: B=-1, C=0, petals=1,...,K.
    counts = Counter(profile)
    own = profile[player]
    if own == -1:
        return F(2 * (m - 1), counts[-1])
    core_load = m - counts[-1]
    result = F(2, core_load)
    if own > 0:
        result += F(1, counts[own])
    return result


def welfare(profile, m):
    return sum((utility(profile, i, m) for i in range(m)), F(0))


def aggregate_slack(profile, query, m):
    base = welfare(profile, m)
    deviations = F(0)
    for player in range(m):
        alternative = list(profile)
        alternative[player] = query
        deviations += utility(alternative, player, m)
    return base - deviations


def audit(m, k):
    pne = [1] + [-1] * (m - 1)
    assert welfare(pne, m) == 2 * m + 1
    for player in range(m):
        for query in range(-1, k + 1):
            alternative = pne.copy()
            alternative[player] = query
            assert utility(pne, player, m) >= utility(alternative, player, m)
    assert F(2 * m - 1, 2 * m) * welfare(pne, m) < 2 * m
    if m == 2:
        return {"m": m, "K": k, "pne_welfare": 2 * m + 1}
    p1 = F(4, 1) / (m + 6 + F(3 * (m - 1), k))
    p2 = (2 + m * p1) / (2 * m + 2)
    p0 = 1 - p1 - p2
    assert min(p0, p1, p2) >= 0
    states = [(p0, [0] + [-1] * (m - 1)), (p2, [0, 0] + [-1] * (m - 2))]
    states.extend((p1 / k, [petal] + [-1] * (m - 1)) for petal in range(1, k + 1))
    assert sum((p for p, _ in states), F(0)) == 1
    expected = sum((p * welfare(profile, m) for p, profile in states), F(0))
    assert expected == 2 * m + p1
    slacks = []
    for query in range(-1, k + 1):
        slack = sum((p * aggregate_slack(profile, query, m) for p, profile in states), F(0))
        assert slack >= 0
        if query != 0:
            assert slack == 0
        slacks.append(str(slack))
    assert F(2 * m - 1, 2 * m) * expected < 2 * m
    return {"m": m, "K": k, "p1": str(p1), "p2": str(p2), "p0": str(p0), "CCE_welfare": str(expected), "aggregate_slacks": slacks}


def main():
    cases = [(m, k) for m in range(2, 13) for k in range(2, 7)] + [(53, 53), (100, 100)]
    report = {"status": "passed", "cases": [audit(m, k) for m, k in cases], "scope": "Explicit PNE and three-state CCE upper bounds; no optimum or general bridge claim."}
    destination = Path(__file__).with_name("weak_cce_boss2_audit.json")
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "passed", "cases": len(cases), "report": str(destination)}, indent=2))


if __name__ == "__main__":
    main()
