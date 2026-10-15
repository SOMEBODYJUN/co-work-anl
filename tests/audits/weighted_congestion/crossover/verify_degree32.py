#!/usr/bin/env python3
"""Independent literal Fraction verifier for the specified 14-resource game.

No solver, cached coefficient matrix, or candidate-search code is used.
By default recompute and compare frozen JSON. --generate NEW_DIRECTORY writes
new evidence and refuses any existing output directory.
"""
from fractions import Fraction as Q
from itertools import product
import json
import argparse
from pathlib import Path

if not __debug__:
    raise RuntimeError("Verification must not be run with -O")

WEIGHTS = (Q(1), Q(1, 10), Q(1, 20), Q(1, 50))
MASKS = (
    (0, 1, 0, 1), (0, 1, 1, 2), (1, 0, 2, 2),
    (1, 1, 0, 0), (1, 1, 2, 0), (1, 1, 2, 2), (1, 2, 1, 1),
)
COEFFICIENTS = (127, 231, 145, 139, 28, 41, 289)
STATES = tuple(product((0, 1), repeat=4))
THRESHOLD = Q(9, 5)


def complement_mask(mask):
    return tuple(0 if label == 0 else 3 - label for label in mask)


def opposite(state, player):
    return state[:player] + (1 - state[player],) + state[player + 1:]


def costs(state, degree=32, limiting=False):
    """Construct both resources of every pair and recompute all their loads.

    In fixed-weight limit mode only the six degree-d terms are replaced by
    their exact d -> infinity limit; the seventh pair stays quadratic.
    """
    result = [Q(0), Q(0), Q(0), Q(0)]
    for pair_index, representative in enumerate(MASKS):
        for mask in (representative, complement_mask(representative)):
            capacity = sum((WEIGHTS[i] for i in range(4) if mask[i] != 0), Q(0))
            users = [i for i in range(4) if mask[i] == state[i] + 1]
            load = sum((WEIGHTS[i] for i in users), Q(0))
            if pair_index == 6:
                latency = Q(COEFFICIENTS[pair_index]) * (load / capacity) ** 2
            elif limiting:
                latency = Q(COEFFICIENTS[pair_index]) if load == capacity else Q(0)
            else:
                latency = Q(COEFFICIENTS[pair_index]) * (load / capacity) ** degree
            for i in users:
                result[i] += latency
    return tuple(result)


def improvement_ratio(current, deviation):
    # None denotes +infinity. 0/0 imposes no obstruction for alpha >= 1.
    if deviation == 0:
        return None if current > 0 else Q(1)
    return current / deviation


def ratio_key(value):
    return (1, Q(0)) if value is None else (0, value)


def rational(value):
    return None if value is None else f"{value.numerator}/{value.denominator}"


def analyze(degree=32, limiting=False, full=False):
    records = []
    factors = {}
    for state in STATES:
        current = costs(state, degree, limiting)
        # Each unilateral move receives its own fresh literal load computation.
        deviations = tuple(costs(opposite(state, i), degree, limiting)[i] for i in range(4))
        ratios = tuple(improvement_ratio(current[i], deviations[i]) for i in range(4))
        best_player = max(range(4), key=lambda i: ratio_key(ratios[i]))
        raw_factor = ratios[best_player]
        factor = None if raw_factor is None else max(Q(1), raw_factor)
        factors[state] = factor
        assert current == costs(tuple(1 - bit for bit in state), degree, limiting)
        item = {
            "state": "".join(map(str, state)),
            "witness_player_zero_based": best_player,
            "witness_ratio": rational(raw_factor) if full else None,
            "witness_ratio_decimal_informational": float(raw_factor) if raw_factor is not None else "infinity",
            "strictly_above_9_over_5": current[best_player] > THRESHOLD * deviations[best_player],
            "all_costs_positive": all(x > 0 for x in current),
            "all_deviation_costs_positive": all(x > 0 for x in deviations),
        }
        if full:
            item.update({
                "current_costs_exact": list(map(rational, current)),
                "deviation_costs_exact": list(map(rational, deviations)),
                "all_flip_ratios_exact": list(map(rational, ratios)),
                "witness_strict_margin_exact": rational(current[best_player] - THRESHOLD * deviations[best_player]),
            })
        records.append(item)
    minimum = min(factors.values(), key=ratio_key)
    return {
        "degree": "fixed-weight d -> infinity" if limiting else degree,
        "best_equilibrium_factor_exact": rational(minimum) if full or limiting else None,
        "best_equilibrium_factor_decimal_informational": float(minimum) if minimum is not None else "infinity",
        "minimizing_states": ["".join(map(str, s)) for s in STATES if factors[s] == minimum],
        "all_states_strictly_above_9_over_5": all(r["strictly_above_9_over_5"] for r in records),
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", type=Path, metavar="NEW_DIRECTORY")
    args = parser.parse_args()
    if args.generate is not None and args.generate.exists():
        parser.error("--generate requires a directory that does not exist")
    assert improvement_ratio(Q(0), Q(0)) == 1
    assert improvement_ratio(Q(1), Q(0)) is None
    assert improvement_ratio(Q(0), Q(1)) == 0
    certificate = analyze(32, full=True)
    assert certificate["all_states_strictly_above_9_over_5"]
    assert certificate["minimizing_states"] == ["0110", "1001"]
    assert all(r["all_costs_positive"] and r["all_deviation_costs_positive"] for r in certificate["records"])
    fixed_limit = analyze(limiting=True, full=True)
    assert not fixed_limit["all_states_strictly_above_9_over_5"]
    scans = []
    for degree in (1, 2, 4, 8, 16, 24, 31, 32, 33, 40, 48, 64, 128, 256):
        result = analyze(degree)
        scans.append({key: value for key, value in result.items() if key != "records"})
    degree40 = analyze(40, full=True)
    assert Q(degree40["best_equilibrium_factor_exact"]) < THRESHOLD
    assert degree40["minimizing_states"] == ["0111", "1000"]
    artifacts = {
        "degree32_certificate.json": certificate,
        "fixed_degree_scan.json": scans,
        "degree40_failure_certificate.json": degree40,
        "fixed_weight_limit_certificate.json": fixed_limit,
    }
    if args.generate is not None:
        args.generate.mkdir(parents=True, exist_ok=False)
        for name, data in artifacts.items():
            with (args.generate / name).open("x") as handle:
                handle.write(json.dumps(data, indent=2) + "\n")
    else:
        frozen = Path(__file__).resolve().parent
        for name, data in artifacts.items():
            assert json.loads((frozen / name).read_text()) == data, name
    print(json.dumps({
        "degree32_factor": certificate["best_equilibrium_factor_decimal_informational"],
        "degree32_minimizers": certificate["minimizing_states"],
        "degree32_strict_9_over_5_all_states": True,
        "fixed_weight_limit_factor_exact": fixed_limit["best_equilibrium_factor_exact"],
        "fixed_weight_limit_factor_decimal": fixed_limit["best_equilibrium_factor_decimal_informational"],
        "fixed_weight_limit_minimizers": fixed_limit["minimizing_states"],
        "zero_boundary_policy_checked": True,
        "frozen_evidence_compared": args.generate is None,
    }, indent=2))


if __name__ == "__main__":
    main()
