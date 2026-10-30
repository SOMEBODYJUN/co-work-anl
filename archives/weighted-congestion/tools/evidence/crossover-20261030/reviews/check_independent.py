#!/usr/bin/env python3
"""Independent reconstruction of the seven-pair auxiliary/scaled games.

This does not import the construction author's verification code or evidence.
The scalar limit and finite polynomial games have separate implementations.
Run from any directory; --write stores this review's reproducible JSON beside
this script. All comparisons that determine verdicts use rational arithmetic.
"""
from fractions import Fraction as Q
from itertools import product
import argparse
import json
from pathlib import Path
import sys

sys.set_int_max_str_digits(0)
MASKS = ("0101", "0112", "1022", "1100", "1120", "1122", "1211")
AMPLITUDES = tuple(map(Q, ("49/100", "11/10", "49/100", "3/5", "1/50", "3/100", "1")))
STATES = tuple(product((0, 1), repeat=4))
WITNESSES = (2, 2, 3, 0, 3, 2, 3, 1)


if not __debug__:
    raise RuntimeError('Run without -O: exact verification requires assertions')


def flip(s, i):
    return s[:i] + (1-s[i],) + s[i+1:]


def witness(s):
    canonical = s if s[0] == 0 else tuple(1-bit for bit in s)
    return WITNESSES[4*canonical[1]+2*canonical[2]+canonical[3]]


def auxiliary_coefficients(s):
    """Four cost vectors in the formal independent variables a,...,g."""
    vectors = [[0]*7 for _ in range(4)]
    for j, mask in enumerate(MASKS):
        support = tuple(i for i, digit in enumerate(mask) if digit != "0")
        # The resource orientation chosen by each supported player.
        orientations = {i: s[i] ^ (int(mask[i])-1) for i in support}
        if j < 6:
            if len(set(orientations.values())) == 1:
                for i in support:
                    vectors[i][j] = 1
        else:
            for i in support:
                if orientations[i] == orientations[0]:
                    vectors[i][j] = 1
    return vectors


def auxiliary_costs(s):
    return tuple(sum((c*t for c, t in zip(v, AMPLITUDES)), Q(0))
                 for v in auxiliary_coefficients(s))


def finite_costs(s, m):
    weights = (Q(1), Q(1, 10*m), Q(1, 20*m), Q(1, 50*m))
    result = [Q(0)]*4
    for j, mask in enumerate(MASKS):
        support = tuple(i for i, digit in enumerate(mask) if digit != "0")
        capacity = sum((weights[i] for i in support), Q(0))
        resource_users = [[], []]
        for i in support:
            resource_users[s[i] ^ (int(mask[i])-1)].append(i)
        for users in resource_users:
            load = sum((weights[i] for i in users), Q(0))
            fee = AMPLITUDES[j] * (load/capacity)**(2 if j == 6 else 32*m*m)
            for i in users:
                result[i] += fee
    return tuple(result)


def qs(x):
    return f"{x.numerator}/{x.denominator}"


def formal(v):
    return "+".join(ch for ch, k in zip("abcdefg", v) if k) or "0"


def analyze(cost_function, full=False):
    costs = {s: cost_function(s) for s in STATES}
    rows = []
    best_ratios = []
    margins = []
    for s in STATES:
        current = costs[s]
        deviation = tuple(costs[flip(s, i)][i] for i in range(4))
        # Zero-cost cases are checked before taking any ratio.
        assert all(x > 0 for x in current + deviation)
        ratios = tuple(c/d for c, d in zip(current, deviation))
        best = max(Q(1), *ratios)
        i = witness(s)
        margin = current[i] - 2*deviation[i]
        best_ratios.append(best)
        margins.append(margin)
        row = {"state": "".join(map(str, s)), "witness_player_zero_based": i,
               "witness_strict_margin_positive": margin > 0}
        if full:
            row.update({"current_costs": list(map(qs, current)),
                        "flip_costs": list(map(qs, deviation)),
                        "flip_ratios": list(map(qs, ratios)),
                        "witness_margin_at_alpha_2": qs(margin),
                        "best_ratio": qs(best)})
        rows.append(row)
    beta = min(best_ratios)
    return {"best_equilibrium_factor": qs(beta),
            "best_equilibrium_factor_decimal_informational": float(beta),
            "minimizing_states": [row["state"] for row, value in zip(rows, best_ratios) if value == beta],
            "all_costs_and_flip_costs_positive": True,
            "strict_2_obstruction_all_states": beta > 2,
            "selected_witnesses_strict_all_states": min(margins) > 0,
            "minimum_selected_witness_margin_at_2": qs(min(margins)),
            "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    limit = analyze(auxiliary_costs, full=True)
    assert Q(limit["best_equilibrium_factor"]) == Q(100, 49)
    assert Q(limit["minimum_selected_witness_margin_at_2"]) == Q(1, 50)
    assert limit["selected_witnesses_strict_all_states"]
    formal_rows = []
    expected_pairs = (("g", "e"), ("b+g", "c+e+f"),
                      ("a+g", "c+f"), ("c+d+e+f+g", "g"),
                      ("g", "a"), ("g", "c"),
                      ("b+g", "a+c"), ("a+g", "d+e+f"))
    for s, pair in zip(STATES[:8], expected_pairs):
        i = witness(s)
        actual = (formal(auxiliary_coefficients(s)[i]),
                  formal(auxiliary_coefficients(flip(s, i))[i]))
        assert actual == pair
        formal_rows.append({"state": "".join(map(str, s)), "player": i,
                            "current": actual[0], "flip": actual[1]})
    finite = {str(m): analyze(lambda s, m=m: finite_costs(s, m)) for m in (1, 2, 3)}
    assert not finite["1"]["strict_2_obstruction_all_states"]
    assert not finite["2"]["strict_2_obstruction_all_states"]
    assert finite["3"]["selected_witnesses_strict_all_states"]
    # For every m>=20, rho^(32m^2)<(3/8)^10, delta<=17/(50m),
    # q<=289/(10000m^2). These three upper bounds decrease in m.
    error_at_20 = Q(17, 1000)+Q(289, 2000000)+Q(112, 25)*Q(3, 8)**10
    assert error_at_20 < Q(1, 50)
    evidence = {"auxiliary_limit": limit, "formal_witnesses": formal_rows,
                "finite_checks": finite,
                "all_integer_m_at_least_20": {
                    "witness_margin_lower_bound": qs(Q(1, 50)-error_at_20),
                    "error_upper_bound": qs(error_at_20),
                    "minimum_degree": 12800}}
    if args.write:
        Path(__file__).with_name("independent_evidence.json").write_text(json.dumps(evidence, indent=2)+"\n")
    print(json.dumps({"auxiliary_factor": limit["best_equilibrium_factor"],
                      "auxiliary_minimum_margin_at_2": limit["minimum_selected_witness_margin_at_2"],
                      "finite_m1_to_m3_factors_informational": {
                          m: row["best_equilibrium_factor_decimal_informational"] for m, row in finite.items()},
                      "uniform_all_m_at_least_20_margin_lower_bound": qs(Q(1, 50)-error_at_20)}, indent=2))


if __name__ == "__main__":
    main()
