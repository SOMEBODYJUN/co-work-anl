#!/usr/bin/env python3
"""Independent exact audit of terminal tie quotient lifts and their obstruction.

Reconstructs every payoff from ordered terminal histories; imports neither the
model, a solver, nor another audit. The default is print-only. --output creates
one new report exclusively and never overwrites frozen evidence.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def execute(strategy, history):
    while len(history) < 3:
        history += (strategy[history],)
    return history


def payoff(mask, action, final):
    if not (mask >> action) & 1:
        return F(0)
    return F(1, sum((mask >> label) & 1 for label in final))


def incentive(strategy, history, deviation):
    final = execute(strategy, history)
    alternative = execute(strategy, history + (deviation,))
    return tuple(
        payoff(mask, strategy[history], final)
        - payoff(mask, deviation, alternative)
        for mask in range(1, 8)
    )


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), F(0))


def combination(rows, weights):
    return tuple(
        sum((weight * rows[row][coordinate] for row, weight in weights.items()), F(0))
        for coordinate in range(7)
    )


def subtract(left, right):
    return tuple(a - b for a, b in zip(left, right))


def audit():
    original = {(): 2, (0,): 2, (1,): 1, (2,): 0}
    replies = (2, 2, 1, 2, 2, 2, 2, 1, 1)
    leaves = tuple(product(range(3), repeat=2))
    original.update({history: replies[3 * history[0] + history[1]] for history in leaves})
    histories = tuple(history for depth in range(3) for history in product(range(3), repeat=depth))
    keys = tuple((history, action) for history in histories for action in range(3))
    counts = lambda history: tuple(history.count(action) for action in range(3))
    representatives = {}
    for history in leaves:
        representatives.setdefault(counts(history), history)
    original_final = execute(original, ())
    representatives[counts(original_final[:-1])] = original_final[:-1]
    canonical = dict(original)
    for history in leaves:
        canonical[history] = original[representatives[counts(history)]]
    assert original_final == (2, 0, 2)
    assert execute(canonical, ()) == original_final
    assert tuple(history for history in leaves if canonical[history] != original[history]) == ((0, 2), (2, 1))

    rows = {key: incentive(original, *key) for key in keys}
    normalized_rows = {key: incentive(canonical, *key) for key in keys}
    clients = (F(0), F(0), F(1), F(1), F(0), F(1), F(0))
    slacks = {key: dot(row, clients) for key, row in rows.items()}
    assert min(slacks.values()) >= 0
    assert len(slacks) == 39

    def transfer(leaf, incumbent):
        values = []
        for mask in range(1, 8):
            load = sum((mask >> action) & 1 for action in leaf)
            numerator = ((mask >> incumbent) & 1) * (
                ((mask >> original[leaf]) & 1) - ((mask >> canonical[leaf]) & 1)
            )
            values.append(F(numerator, load * (load + 1)) if numerator else F(0))
        return tuple(values)

    errors = {}
    identity_count = reciprocal_count = 0
    ties = {}
    uncovered_count = 0
    for leaf in leaves:
        representative = representatives[counts(leaf)]
        tie = rows[leaf, canonical[leaf]]
        reciprocal = rows[representative, original[leaf]]
        assert tie == tuple(-entry for entry in reciprocal)
        reciprocal_count += 7
        ties[leaf] = tie
        assert dot(tie, clients) == 0
        joint = combination(
            {(leaf, action): transfer(leaf, action) for action in set(leaf)},
            {(leaf, action): F(leaf.count(action)) for action in set(leaf)},
        )
        for coordinate, mask in enumerate(range(1, 8)):
            load = sum((mask >> action) & 1 for action in leaf)
            uncovered = tie[coordinate] if load == 0 else F(0)
            assert joint[coordinate] == tie[coordinate] - uncovered
            old_cover = int(any((mask >> action) & 1 for action in leaf + (original[leaf],)))
            new_cover = int(any((mask >> action) & 1 for action in leaf + (canonical[leaf],)))
            assert new_cover - old_cover == -uncovered
            uncovered_count += 1

    for key in keys:
        history, deviation = key
        if len(history) < 2:
            target = execute(original, history)[:-1]
            source = execute(original, history + (deviation,))[:-1]
            errors[key] = subtract(transfer(target, original[history]), transfer(source, deviation))
            transformed = tuple(a + b for a, b in zip(rows[key], errors[key]))
        else:
            representative = representatives[counts(history)]
            transformed = tuple(a + b for a, b in zip(rows[key], rows[representative, original[history]]))
        assert transformed == normalized_rows[key]
        identity_count += 7

    cover = tuple(F(int(any((mask >> action) & 1 for action in original_final))) for mask in range(1, 8))
    optimum_comparator = tuple(F(1) for _ in range(7))
    target = tuple(2 * a - b for a, b in zip(cover, optimum_comparator))
    assert target == (1, -1, 1, 1, 1, 1, 1)
    assert dot(cover, clients) == dot(optimum_comparator, clients) == 3

    # Both examples use the same natural target 2c-o and the same three rows.
    early_keys = (((0,), 0), ((2,), 1), ((2,), 2))
    expected_canonical_rows = (
        (F(-1, 2), 0, F(-1, 2), F(1, 2), 0, F(1, 2), 0),
        (1, -1, 0, 0, F(1, 3), F(-1, 3), 0),
        (1, 0, 1, F(-1, 2), F(-1, 6), F(-1, 3), 0),
    )
    assert tuple(normalized_rows[key] for key in early_keys) == expected_canonical_rows

    good_weights = dict(zip(early_keys, map(F, (2, 1, 1))))
    good_r = subtract(target, combination(normalized_rows, good_weights))
    assert good_r == (0, 0, 1, F(1, 2), F(5, 6), F(2, 3), 1)
    assert min(good_r) >= 0
    good_error = combination(errors, good_weights)
    good_s = tuple(a + b for a, b in zip(good_r, good_error))
    assert good_s == (0, F(-1, 2), F(1, 2), F(-1, 2), F(1, 2), F(2, 3), 1)
    assert min(good_s) < 0
    # -2*tau_AC + 3*tau_CB is paid by the two actual reciprocal rows.
    signed_tie = tuple(-2 * a + 3 * b for a, b in zip(ties[(0, 2)], ties[(2, 1)]))
    corrected_r = subtract(good_s, signed_tie)
    assert corrected_r == (0, 0, 0, 0, F(4, 3), F(2, 3), 1)
    assert min(corrected_r) >= 0
    lifted_good = dict(good_weights)
    lifted_good[((2, 0), 1)] = F(2)
    lifted_good[((2, 1), 2)] = F(3)
    assert combination(rows, lifted_good) == subtract(target, corrected_r)
    assert all(weight >= 0 for weight in lifted_good.values())

    bad_weights = dict(zip(early_keys, map(F, (4, 1, 2))))
    bad_r = subtract(target, combination(normalized_rows, bad_weights))
    assert bad_r == (0, 0, 1, 0, 1, 0, 1)
    assert min(bad_r) >= 0
    bad_error = combination(errors, bad_weights)
    assert bad_error == (0, F(-1, 2), F(-1, 2), -2, F(-2, 3), 0, 0)
    bad_s = tuple(a + b for a, b in zip(bad_r, bad_error))
    assert bad_s == (0, F(-1, 2), F(1, 2), -2, F(1, 3), 0, 1)
    assert bad_s == subtract(target, combination(rows, bad_weights))
    assert dot(bad_s, clients) == F(-3, 2)
    assert dot(combination(rows, bad_weights), clients) == F(9, 2)
    # Every structural terminal tie vanishes on a valid nonnegative witness;
    # therefore no signed combination of them can yield nonnegative bad_s.
    assert all(dot(tie, clients) == 0 for tie in ties.values())

    def render_vector(vector):
        return [str(entry) for entry in vector]

    return {
        "status": "PASS",
        "model": "three unit players; three unit clients of types AB, C, BC; all ordered histories",
        "root": list(original_final),
        "W": "3",
        "OPT_3": "3",
        "original_SPE_comparisons": len(slacks),
        "all_type_transformation_identities": identity_count,
        "all_type_reciprocal_identities": reciprocal_count,
        "all_type_uncovered_decompositions": uncovered_count,
        "type_order": ["A", "B", "AB", "C", "AC", "BC", "ABC"],
        "strict_quotient_lift": {
            "normalized_early_weights": ["2", "1", "1"],
            "normalized_r": render_vector(good_r),
            "raw_r_plus_E": render_vector(good_s),
            "signed_tie_coefficients_AC_CB": ["-2", "3"],
            "corrected_r": render_vector(corrected_r),
            "added_original_terminal_rows": [
                {"history": [2, 0], "deviation": 1, "weight": "2"},
                {"history": [2, 1], "deviation": 2, "weight": "3"},
            ],
        },
        "fixed_lift_obstruction": {
            "normalized_early_weights": ["4", "1", "2"],
            "normalized_r": render_vector(bad_r),
            "raw_r_plus_E": render_vector(bad_s),
            "separating_unit_client_masses": render_vector(clients),
            "all_original_SPE_slacks_nonnegative": True,
            "all_structural_terminal_ties_zero": True,
            "separating_dot_product": "-3/2",
            "preserved_original_early_payment": "9/2",
            "natural_target_value": "3",
        },
        "scope": "Exact finite certificates and an obstruction to preserving a given normalized certificate's early weights; neither a half-coverage counterexample nor a universal certificate constructor.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Exclusively create a new JSON report")
    args = parser.parse_args()
    rendered = json.dumps(audit(), indent=2) + "\n"
    if args.output is not None:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
    print(rendered, end="")
