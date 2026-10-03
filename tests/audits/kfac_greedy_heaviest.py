"""Exact independent check: largest-improving-weight site repair can exceed 2.

Run: python3 tests/audits/kfac_greedy_heaviest.py
This is a finite counterexample, not a statement about every greedy occupancy.
"""

import json
from fractions import Fraction as F
from pathlib import Path

import kfac_greedy_repair_order as check


def main():
    path = Path(__file__).resolve().parents[2] / "examples/multi_facility/greedy_heaviest_escape.json"
    check.DATA = json.loads(path.read_text())
    check.SITES = check.DATA["sites"]
    check.WEIGHTS = [F(row["weight"]) for row in check.DATA["clients"]]
    check.ACCESS = [set(row["sites"]) for row in check.DATA["clients"]]
    q, assigned, trace = check.greedy()
    assert trace == [
        ("D", F(320)), ("B", F(216)), ("D", F(160)),
        ("C", F(155)), ("B", F(108)), ("D", F(320, 3)),
        ("E", F(82)), ("A", F(80)),
    ]
    assert [q[s] for s in check.SITES] == [1, 1, 2, 1, 3, 0]
    assert [check.weights_at(assigned)[s] for s in check.SITES] == [80, 82, 216, 155, 320, 0]

    expected = [
        (1, "B", "A", F(255, 2), F(119)),
        (6, "D", "B", F(424, 3), F(281, 2)),
        (4, "C", "A", F(155), F(154)),
        (1, "A", "B", F(154), F(307, 2)),
        (2, "B", "E", F(182), F(178)),
    ]
    for i, source, target, old, new in expected:
        improving = []
        for j, home in enumerate(assigned):
            if home is None:
                continue
            for alt in check.SITES:
                if not q[alt] or alt == home or alt not in check.ACCESS[j]:
                    continue
                if check.conditional_cost(j, alt, assigned, q) < check.conditional_cost(j, home, assigned, q):
                    improving.append((check.WEIGHTS[j], j, alt))
        assert improving
        assert len({j for w, j, _ in improving if w == max(x[0] for x in improving)}) == 1
        assert (check.WEIGHTS[i], i, target) == max(improving)
        assert assigned[i] == source
        assert check.conditional_cost(i, source, assigned, q) == old
        assert check.conditional_cost(i, target, assigned, q) == new
        assert new < old
        assigned[i] = target
    check.assert_site_ne(assigned, q)
    assert [check.weights_at(assigned)[s] for s in check.SITES] == [115, 178, 172, 120, 268, 0]

    # At B -> G, private 81,82,80 force the 96 customer strictly to G in
    # every mixed NE, exactly as in the first independent audit.
    assert check.ACCESS[2] == {"B", "E", "G"}
    assert {j for j, sites in enumerate(check.ACCESS) if "G" in sites} == {2, 9}
    assert [check.WEIGHTS[j] for j in (3, 8, 9)] == [81, 82, 80]
    a = check.weights_at(assigned)["B"] / q["B"]
    assert a == F(86)
    assert (check.WEIGHTS[2] + check.WEIGHTS[9]) / a == F(88, 43) > 2

    _, good, _ = check.greedy()
    assert check.conditional_cost(4, "A", good, q) < check.conditional_cost(4, "C", good, q)
    good[4] = "A"
    check.assert_site_ne(good, q)
    check.assert_all_transfer_budgets(good, q)
    assert [check.weights_at(good)[s] for s in check.SITES] == [115, 82, 216, 120, 320, 0]
    print("PASS: unique largest-weight improvement path fails 2 at 88/43; another NE retains all budgets")


if __name__ == "__main__":
    main()
