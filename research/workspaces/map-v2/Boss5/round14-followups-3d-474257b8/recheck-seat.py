"""Focused exact arithmetic for the fixed eighteen-label private point.

This independently expands the saved positive masses and checks only the
108-seat budget contribution. It does not import or execute the old audit,
enumerate potential tuples, solve an LP, or certify a complete SPE.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from math import comb, lcm
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rel = "archives/customer-attraction/tools/evidence/potential-menu-joint/replay/potential_menu_joint_private.json"
    raw = (args.repo / rel).read_bytes()
    data = json.loads(raw)
    masses = [(tuple(t), F(v)) for t, v in data["positive_types"]]
    rows = []
    for (mask, d, ell, h), mass in masses:
        assert mass > 0
        for subset in combinations(range(6), d):
            selected = set(subset)
            if ell == 0:
                replies = set()
            elif (ell, h) == (d, d):
                replies = selected
            elif (ell, h) == (6-d, 0):
                replies = set(range(6)) - selected
            else:
                assert (ell, h) == (6, d)
                replies = set(range(6))
            members = {i for i in range(6) if mask & (1 << i)}
            members |= {6+i for i in selected}
            members |= {12+i for i in replies}
            rows.append((frozenset(members), mass / comb(6, d)))
    covers = [{k for k, (members, _) in enumerate(rows) if j in members} for j in range(18)]
    distinct = len({frozenset(c) for c in covers}) == 18
    maxima = [j for j in range(18) if not any(covers[j] < covers[k] for k in range(18))]
    scale = lcm(*(mass.denominator for _, mass in rows))
    actual = set(range(6))
    W = sum((mass for members, mass in rows if members & actual), F(0))
    pay = [sum((mass / len(members & actual) for members, mass in rows if i in members), F(0)) for i in range(6)]
    seats = []
    theme_data = []
    maximal_set = set(maxima)
    for j in maxima:
        size = sum((mass for members, mass in rows if j in members), F(0))
        missing = sum((mass for members, mass in rows
                       if j in members and not (members & actual)
                       and members & maximal_set == {j}), F(0))
        theme_data.append({"label": j, "size": str(size), "missing_private": str(missing)})
        for h in range(1, 7):
            seats.append((missing / h + (size-missing) / 6, j, h))
    seats.sort(key=lambda x: (-x[0], x[1], x[2]))
    total = sum((s[0] for s in seats[:6]), F(0))
    individual = [pay[i] - seats[5-i][0] for i in range(6)]
    lp_B = sum((mass * (F(d, 6) + F(5, 6) * int(mask == 0 and d == 1 and ell == 0))
                for (mask, d, ell, h), mass in masses), F(0))
    lp_individual = [6*u-lp_B for u in pay]
    assert distinct and maxima == list(range(18))
    assert len(masses) == 18 and len(rows) == 117 and len(seats) == 108
    assert W == 1 and scale == 21801574746360
    assert {(j, h) for _, j, h in seats[:6]} == {(j, 1) for j in range(6, 12)}
    assert lp_B == total and all(x >= 0 for x in individual) and W >= total
    assert lp_individual == [6*x for x in individual]
    report = {
        "scope": "fixed private point: eighteen labels, actual A1..A6; seat budget contribution only",
        "source": {"path": rel, "sha256": hashlib.sha256(raw).hexdigest()},
        "old_audit_executed": False,
        "positive_symmetric_types": len(masses), "expanded_types": len(rows),
        "integer_scale": scale, "distinct_covers": distinct, "maximal_labels": maxima,
        "seat_count": len(seats), "W": str(W), "actual_payoffs": list(map(str, pay)),
        "first_six": [{"value": str(v), "label": j, "h": h} for v, j, h in seats[:6]],
        "seventh": {"value": str(seats[6][0]), "label": seats[6][1], "h": seats[6][2]},
        "individual_slacks": list(map(str, individual)), "total_slack": str(W-total),
        "original_lp_B": str(lp_B), "original_lp_six_individual_slacks": list(map(str, lp_individual)),
        "original_lp_total_slack": str(W-lp_B),
        "theme_values": theme_data,
        "all_108_seats": [{"value": str(v), "label": j, "h": h} for v, j, h in seats],
        "proof_count_effect": "none: exact arithmetic replay of one existing fixed point, not a new independent theorem proof"
    }
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["expanded_types", "seat_count", "first_six", "seventh", "individual_slacks", "total_slack", "original_lp_B"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
