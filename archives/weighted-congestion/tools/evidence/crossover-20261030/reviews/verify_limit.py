#!/usr/bin/env python3
"""Exact checks for the separately authored four-player scaling interface.

Default: recompute and compare frozen limit_evidence JSON. To generate:
--generate NEW_DIRECTORY (an existing directory is rejected).
This code is evidence for finite calculations and rational error bounds; the
general convergence and coefficient feasibility proof is in limit_family.md.
"""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys

if not __debug__:
    raise RuntimeError("Verification must not be run with -O")
sys.set_int_max_str_digits(0)

MASKS = (
    (0, 1, 0, 1), (0, 1, 1, 2), (1, 0, 2, 2), (1, 1, 0, 0),
    (1, 1, 2, 0), (1, 1, 2, 2), (1, 2, 1, 1),
)
ORIGINAL = tuple(map(F, (127, 231, 145, 139, 28, 41, 289)))
RETUNED = (F(49, 100), F(11, 10), F(49, 100), F(3, 5), F(1, 50), F(3, 100), F(1))
STATES = tuple(product((0, 1), repeat=4))
TEMPLATE_WITNESSES = (2, 2, 3, 0, 3, 2, 3, 1)


def flip(state, i):
    result = list(state)
    result[i] = 1 - result[i]
    return tuple(result)


def literal_costs(state, coefficients, m=None):
    """m=None means the limit with vanishing small weights and d*w_small->inf."""
    weights = (F(1), F(1, 10*m), F(1, 20*m), F(1, 50*m)) if m is not None else None
    degree = 32*m*m if m is not None else None
    result = [F(0)]*4
    for j, representative in enumerate(MASKS):
        for mask in (representative, tuple(3-label if label else 0 for label in representative)):
            users = tuple(i for i in range(4) if mask[i] == state[i] + 1)
            if m is None:
                active = (0 in users) if j == 6 else all(mask[i] == 0 or i in users for i in range(4))
                fee = coefficients[j] if active else F(0)
            else:
                capacity = sum((weights[i] for i in range(4) if mask[i] != 0), F(0))
                load = sum((weights[i] for i in users), F(0))
                fee = coefficients[j]*(load/capacity)**(2 if j == 6 else degree)
            for i in users:
                result[i] += fee
    return tuple(result)


def witness_for(state):
    canonical = state if state[0] == 0 else tuple(1-bit for bit in state)
    index = 4*canonical[1] + 2*canonical[2] + canonical[3]
    return TEMPLATE_WITNESSES[index]


def qstring(value):
    return f"{value.numerator}/{value.denominator}"


def analyze(coefficients, alpha, m=None, full=False):
    current = {state: literal_costs(state, coefficients, m) for state in STATES}
    assert all(cost > 0 for vector in current.values() for cost in vector)
    rows = []
    factors = {}
    margins = []
    for state in STATES:
        alternatives = tuple(literal_costs(flip(state, i), coefficients, m)[i] for i in range(4))
        assert all(x > 0 for x in alternatives)
        ratios = tuple(current[state][i]/alternatives[i] for i in range(4))
        factor = max(F(1), *ratios)
        factors[state] = factor
        witness = witness_for(state)
        margin = current[state][witness] - alpha*alternatives[witness]
        margins.append(margin)
        assert current[state] == current[tuple(1-bit for bit in state)]
        row = {
            "state": "".join(map(str, state)),
            "template_witness_player_zero_based": witness,
            "max_flip_ratio_decimal_informational": float(factor),
            "template_witness_strict_alpha_margin_positive": margin > 0,
        }
        if full:
            row.update({
                "costs_exact": list(map(qstring, current[state])),
                "deviation_costs_exact": list(map(qstring, alternatives)),
                "flip_ratios_exact": list(map(qstring, ratios)),
                "template_witness_alpha_margin_exact": qstring(margin),
            })
        rows.append(row)
    best = min(factors.values())
    data = {
        "m": m,
        "degree": 32*m*m if m is not None else "scaled-weight limit",
        "coefficients_exact": list(map(qstring, coefficients)),
        "comparison_alpha_exact": qstring(alpha),
        "best_equilibrium_factor_decimal_informational": float(best),
        "best_equilibrium_factor_exact": qstring(best) if full else None,
        "minimizing_states": ["".join(map(str, state)) for state in STATES if factors[state] == best],
        "strict_alpha_obstruction_all_states": best > alpha,
        "template_witnesses_strict_all_states": all(margin > 0 for margin in margins),
        "all_current_and_deviation_costs_positive": True,
    }
    if full:
        data.update({"minimum_template_witness_margin_exact": qstring(min(margins)), "records": rows})
    return data


def rational_uniform_bound(coefficients, alpha, m):
    limiting = analyze(coefficients, alpha, full=True)
    delta = F(limiting["minimum_template_witness_margin_exact"])
    assert delta > 0
    exponent_floor = (64*m)//117
    # exp(-64*m/117) < (3/8)^floor(64*m/117), since e > 8/3.
    error_bound = sum(coefficients[:6]) * F(3, 8)**exponent_floor + 17*coefficients[6]/(50*m)
    margin_bound = delta - (1+alpha)*error_bound
    assert margin_bound > 0
    return {
        "coefficients_exact": list(map(qstring, coefficients)),
        "alpha_exact": qstring(alpha),
        "all_integer_m_at_least": m,
        "degree_at_first_m": 32*m*m,
        "minimum_limit_witness_margin_exact": qstring(delta),
        "rational_uniform_cost_error_bound_at_first_m": qstring(error_bound),
        "rational_uniform_strict_margin_lower_bound": qstring(margin_bound),
        "exponent_floor": exponent_floor,
        "strict_bound_proved_by_rational_comparison": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", type=Path, metavar="NEW_DIRECTORY")
    args = parser.parse_args()
    if args.generate is not None and args.generate.exists():
        parser.error("--generate requires a directory that does not exist")
    original_limit = analyze(ORIGINAL, F(9, 5), full=True)
    retuned_limit = analyze(RETUNED, F(2), full=True)
    assert F(original_limit["best_equilibrium_factor_exact"]) == F(65, 34)
    assert F(retuned_limit["best_equilibrium_factor_exact"]) == F(100, 49)
    assert original_limit["template_witnesses_strict_all_states"]
    assert retuned_limit["template_witnesses_strict_all_states"]
    original_scans = [analyze(ORIGINAL, F(9, 5), m) for m in range(1, 13)]
    assert all(row["strict_alpha_obstruction_all_states"] for row in original_scans)
    retuned_scans = [analyze(RETUNED, F(2), m) for m in range(1, 4)]
    retuned_m3 = analyze(RETUNED, F(2), 3, full=True)
    assert retuned_m3["strict_alpha_obstruction_all_states"]
    assert retuned_m3["template_witnesses_strict_all_states"]
    bounds = [rational_uniform_bound(ORIGINAL, F(9, 5), 13), rational_uniform_bound(RETUNED, F(2), 52)]
    artifacts = {
        "scaled_limits.json": {"original_coefficients": original_limit, "retuned_coefficients": retuned_limit},
        "finite_scans.json": {"original_coefficients": original_scans, "retuned_coefficients": retuned_scans},
        "retuned_m3_certificate.json": retuned_m3,
        "uniform_bounds.json": bounds,
    }
    if args.generate is not None:
        args.generate.mkdir(parents=True, exist_ok=False)
        for name, data in artifacts.items():
            with (args.generate/name).open("x") as handle:
                handle.write(json.dumps(data, indent=2) + "\n")
    else:
        frozen = Path(__file__).resolve().parent / "limit_evidence"
        for name, data in artifacts.items():
            assert json.loads((frozen/name).read_text()) == data, name
    print(json.dumps({
        "original_scaled_limit_factor_exact": "65/34",
        "retuned_scaled_limit_factor_exact": "100/49",
        "retuned_m3_degree": 288,
        "retuned_m3_factor_decimal": retuned_m3["best_equilibrium_factor_decimal_informational"],
        "retuned_m3_strict_2_obstruction": True,
        "original_all_m_positive_9_over_5": "m=1..12 exact checks plus uniform proof m>=13",
        "retuned_uniform_strict_2_obstruction": "all integer m>=52",
        "frozen_evidence_compared": args.generate is None,
    }, indent=2))


if __name__ == "__main__":
    main()
