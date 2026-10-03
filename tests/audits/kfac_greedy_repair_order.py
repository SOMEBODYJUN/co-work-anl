"""Independent exact-arithmetic audit of one greedy-repair-order obstruction.

Run: python3 tests/audits/kfac_greedy_repair_order.py
This proves only the displayed finite counterexample, not a universal theorem.
"""

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads(
    (ROOT / "examples/multi_facility/greedy_repair_order_escape.json").read_text()
)
SITES = DATA["sites"]
WEIGHTS = [Fraction(row["weight"]) for row in DATA["clients"]]
ACCESS = [set(row["sites"]) for row in DATA["clients"]]


def weights_at(assignment):
    return {site: sum((WEIGHTS[i] for i, home in enumerate(assignment)
                       if home == site), Fraction(0)) for site in SITES}


def greedy():
    occupancy = {site: 0 for site in SITES}
    assigned = [None] * len(WEIGHTS)
    trace = []
    for _ in range(DATA["k"]):
        totals = weights_at(assigned)
        scores = {}
        for site in SITES:
            if occupancy[site]:
                scores[site] = totals[site] / (occupancy[site] + 1)
            else:
                scores[site] = sum(
                    (WEIGHTS[i] for i in range(len(WEIGHTS))
                     if assigned[i] is None and site in ACCESS[i]), Fraction(0)
                )
        chosen = max(SITES, key=lambda site: scores[site])
        trace.append((chosen, scores[chosen]))
        if occupancy[chosen] == 0:
            for i in range(len(WEIGHTS)):
                if assigned[i] is None and chosen in ACCESS[i]:
                    assigned[i] = chosen
        occupancy[chosen] += 1
    return occupancy, assigned, trace


def conditional_cost(i, site, assigned, occupancy):
    totals = weights_at(assigned)
    own = WEIGHTS[i]
    other = totals[site] - (own if assigned[i] == site else 0)
    return own + other / occupancy[site]


def assert_site_ne(assigned, occupancy):
    for i, home in enumerate(assigned):
        options = [site for site in SITES if occupancy[site] and site in ACCESS[i]]
        if not options:
            assert home is None
            continue
        assert home in options
        current = conditional_cost(i, home, assigned, occupancy)
        assert all(current <= conditional_cost(i, site, assigned, occupancy)
                   for site in options)


def assert_all_transfer_budgets(assigned, occupancy):
    totals = weights_at(assigned)
    occupied = [site for site in SITES if occupancy[site]]
    newly_covered = {
        r: sum((WEIGHTS[i] for i in range(len(WEIGHTS))
                if r in ACCESS[i] and not any(t in ACCESS[i] for t in occupied)),
               Fraction(0))
        for r in SITES if not occupancy[r]
    }
    for source in occupied:
        q = occupancy[source]
        a = totals[source] / q
        members = [i for i, site in enumerate(assigned) if site == source]
        for target in occupied:
            if target == source:
                continue
            orphan_overlap = sum((WEIGHTS[i] for i in members if target in ACCESS[i]),
                                 Fraction(0)) if q == 1 else 0
            assert totals[target] + orphan_overlap <= (occupancy[target] + 1) * a
        for target, new in newly_covered.items():
            orphan_overlap = sum((WEIGHTS[i] for i in members if target in ACCESS[i]),
                                 Fraction(0)) if q == 1 else 0
            assert new + orphan_overlap <= a


def audit():
    q, assigned, trace = greedy()
    assert trace == [
        ("D", Fraction(320)), ("B", Fraction(209)),
        ("C", Fraction(160)), ("D", Fraction(160)),
        ("D", Fraction(320, 3)), ("B", Fraction(209, 2)),
        ("E", Fraction(82)), ("A", Fraction(80)),
    ]
    assert [q[site] for site in SITES] == [1, 1, 2, 1, 3, 0]
    assert [weights_at(assigned)[site] for site in SITES] == [80, 82, 209, 160, 320, 0]

    for i, source, target, old, new in [
        (1, "B", "A", Fraction(241, 2), Fraction(112)),
        (4, "C", "A", Fraction(160), Fraction(152)),
        (6, "D", "B", Fraction(424, 3), Fraction(281, 2)),
        (1, "A", "B", Fraction(152), Fraction(293, 2)),
        (2, "B", "E", Fraction(357, 2), Fraction(178)),
    ]:
        assert assigned[i] == source and target in ACCESS[i]
        assert conditional_cost(i, source, assigned, q) == old
        assert conditional_cost(i, target, assigned, q) == new
        assert new < old
        assigned[i] = target

    assert [weights_at(assigned)[site] for site in SITES] == [120, 178, 165, 120, 268, 0]
    assert_site_ne(assigned, q)
    a = weights_at(assigned)["B"] / q["B"]
    assert a == Fraction(165, 2)

    # After one B facility moves to G, clients 3, 8, 9 are private to B,E,G.
    # For client 2 (weight 96), the conditional costs at those sites are
    # respectively at least 96+81, 96+82, and exactly 96+80. Other clients
    # can only raise the first two costs; no other client can use G.
    assert ACCESS[2] == {"B", "E", "G"}
    assert ACCESS[3] == {"B"} and ACCESS[8] == {"E"} and ACCESS[9] == {"G"}
    assert {i for i, sites in enumerate(ACCESS) if "G" in sites} == {2, 9}
    assert WEIGHTS[3] == 81 and WEIGHTS[8] == 82 and WEIGHTS[9] == 80
    assert WEIGHTS[9] < WEIGHTS[3] and WEIGHTS[9] < WEIGHTS[8]
    forced_deviator = WEIGHTS[2] + WEIGHTS[9]
    assert forced_deviator == 176 and forced_deviator / a == Fraction(32, 15)
    assert forced_deviator > 2 * a

    # A different strict repair is already an NE at the same greedy layout.
    _, good, _ = greedy()
    assert conditional_cost(4, "C", good, q) > conditional_cost(4, "A", good, q)
    good[4] = "A"
    assert_site_ne(good, q)
    assert_all_transfer_budgets(good, q)
    assert weights_at(good)["B"] / q["B"] == Fraction(209, 2)
    print("PASS: greedy trace, two exact on-path NEs, and forced mixed-NE escape 32/15")


if __name__ == "__main__":
    audit()
