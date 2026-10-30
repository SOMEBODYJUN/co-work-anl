"""Exact fixed-instance audit of nested-anchor list repair and its limit.

Run: python3 tests/audits/kfac_nested_anchor.py
This is a finite arithmetic audit, not a proof of the universal theorem.
"""

import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / "examples/multi_facility/greedy_nested_anchor.json").read_text())
SITES = DATA["sites"]
WEIGHT = [F(client["weight"]) for client in DATA["clients"]]


def totals(assignment):
    return {site: sum((WEIGHT[i] for i, a in enumerate(assignment) if a == site), F(0))
            for site in SITES}


def greedy(access):
    q = {site: 0 for site in SITES}
    assignment = [None] * len(access)
    trace = []
    for _ in range(DATA["k"]):
        w = totals(assignment)
        scores = {site: w[site] / (q[site] + 1) if q[site] else
                  sum((WEIGHT[i] for i, a in enumerate(assignment)
                       if a is None and site in access[i]), F(0))
                  for site in SITES}
        selected = max(SITES, key=lambda site: scores[site])
        assert list(scores.values()).count(scores[selected]) == 1
        trace.append((selected, scores[selected]))
        if not q[selected]:
            for i, a in enumerate(assignment):
                if a is None and selected in access[i]:
                    assignment[i] = selected
        q[selected] += 1
    return q, assignment, trace


def list_repair(q, access):
    assignment = SITES[:3] + [None, None]
    for i in (3, 4):
        w = totals(assignment)
        choice = min((site for site in SITES if site in access[i]),
                     key=lambda site: (w[site] / q[site], SITES.index(site)))
        assignment[i] = choice
    return assignment


def improving_moves(q, access, assignment):
    w = totals(assignment)
    return [(i, source, target, (w[source] - WEIGHT[i]) / q[source],
             w[target] / q[target])
            for i, source in enumerate(assignment)
            for target in SITES if target != source and target in access[i]
            if (w[source] - WEIGHT[i]) / q[source] > w[target] / q[target]]


def audit():
    access = [set(client["sites"]) for client in DATA["clients"]]
    expected_trace = [("H", F(143)), ("M", F(80)), ("H", F(143, 2)),
                      ("H", F(143, 3)), ("L", F(41)), ("M", F(40))]
    q, start, trace = greedy(access)
    assert trace == expected_trace
    assert [q[site] for site in SITES] == [3, 2, 1]
    assert start == ["H", "M", "L", "H", "H"]
    good = list_repair(q, access)
    assert good == ["H", "M", "L", "M", "L"]
    assert [totals(good)[site] for site in SITES] == [135, 85, 44]
    assert improving_moves(q, access, good) == []
    assert F(143 - 5, 3) > F(80, 2)  # Range certificate (17R) fails.

    reversed_access = [set(options) for options in access]
    reversed_access[3], reversed_access[4] = reversed_access[4], reversed_access[3]
    q2, start2, trace2 = greedy(reversed_access)
    assert q2 == q and start2 == start and trace2 == trace
    bad = list_repair(q2, reversed_access)
    assert bad == ["H", "M", "L", "M", "M"]
    assert [totals(bad)[site] for site in SITES] == [135, 88, 41]
    assert improving_moves(q2, reversed_access, bad) == [(3, "M", "L", F(83, 2), F(41))]
    bad[3] = "L"
    assert [totals(bad)[site] for site in SITES] == [135, 83, 46]
    assert improving_moves(q2, reversed_access, bad) == []
    print("PASS: nested-anchor NE, range separation, reverse-order list obstruction")


if __name__ == "__main__":
    audit()
