#!/usr/bin/env python3
"""Rebuild only the recorded BANK-EDGE counterexample; write JSON to stdout.

The canonical exact solver retains every pure SPE terminal outcome at each
count state. This does not impose a common continuation on ordered histories
with equal counts. No frozen input, certificate, or output file is modified.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
import sys


REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from customer_attraction.exact import ExactSPESolver  # noqa: E402
from customer_attraction.model import Instance  # noqa: E402


SOURCE_PATHS = (
    "examples/customer_attraction/root_tax_failure.json",
    "evidence/certificates/customer_attraction/root_tax_failure.json",
    "research/current/customer_attraction/root_tax_counterexample.md",
    "customer_attraction/exact.py",
)


def rebuild() -> dict:
    instance = Instance.from_dict(json.loads((REPO / SOURCE_PATHS[0]).read_text()))
    assert instance.players == 4 and instance.topic_count == 6
    solver = ExactSPESolver(instance)
    states = []
    exact_values = []

    for old_a_count in range(4):
        prefix = (old_a_count, 0, 0, 0, 0, 0)
        remaining = instance.players - old_a_count
        outcomes = solver.outcomes(prefix)
        # All old players chose A, but use the full definition sum_a b_a U_a.
        old_returns = [
            (
                sum(
                    (
                        prefix[action] * instance.topic_payoff(action, terminal)
                        for action in range(instance.topic_count)
                    ),
                    Fraction(0),
                ),
                terminal,
            )
            for terminal in outcomes
        ]
        minimum_old_return = min(value for value, _ in old_returns)

        completion_values = []
        for completion in combinations_with_replacement(
            range(instance.topic_count), remaining
        ):
            terminal = tuple(
                prefix[action] + completion.count(action)
                for action in range(instance.topic_count)
            )
            completion_values.append((instance.welfare(terminal), completion))
        maximum_coverage = max(value for value, _ in completion_values)
        threshold = solver.threshold(prefix)
        psi = maximum_coverage - minimum_old_return
        exact_values.append((maximum_coverage, minimum_old_return, psi, threshold))

        states.append(
            {
                "prefix_counts": prefix,
                "remaining": remaining,
                "M": str(threshold),
                "V": maximum_coverage,
                "E": str(minimum_old_return),
                "Psi": str(psi),
                "R": sorted(outcomes),
                "Emin_leaves": [
                    terminal
                    for value, terminal in old_returns
                    if value == minimum_old_return
                ],
                "Vmax_completions": [
                    completion
                    for value, completion in completion_values
                    if value == maximum_coverage
                ],
            }
        )

    assert exact_values == [
        (61, Fraction(0), Fraction(61), Fraction(9)),
        (61, Fraction(9), Fraction(52), Fraction(9)),
        (51, Fraction(18), Fraction(33), Fraction(9)),
        (41, Fraction(27), Fraction(14), Fraction(11)),
    ]
    violations = []
    for old_a_count in (1, 2):
        drop = exact_values[old_a_count][2] - exact_values[old_a_count + 1][2]
        budget = 2 * exact_values[old_a_count][3]
        assert drop == 19 and budget == 18 and drop > budget
        violations.append(
            {
                "prefix_A_count": old_a_count,
                "action": "A",
                "drop": str(drop),
                "2M": str(budget),
                "excess": str(drop - budget),
            }
        )

    result = {
        "claim": "BANK-EDGE potential inequality fails; not Q-CAG-HALF counterexample",
        "date": "2026-10-25",
        "input": instance.to_dict(),
        "source_sha256": {
            path: hashlib.sha256((REPO / path).read_bytes()).hexdigest()
            for path in SOURCE_PATHS
        },
        "states": states,
        "violating_edges": violations,
        "verification_scope": (
            "Finite exact full-SPE outcome enumeration by canonical solver; "
            "analytic proof of these state values is in companion markdown."
        ),
    }
    # Normalize tuples to JSON arrays before optional equality checking.
    return json.loads(json.dumps(result))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-reference",
        action="store_true",
        help="also compare every reconstructed field with the saved companion JSON",
    )
    args = parser.parse_args()
    result = rebuild()
    if args.check_reference:
        reference = Path(__file__).with_name("credible_bank_edge_counterexample.json")
        expected = json.loads(reference.read_text())
        # Sets below have no mathematical ordering; normalize their presentation.
        for record in (result, expected):
            for state in record["states"]:
                state["Emin_leaves"].sort()
        assert result == expected, "reconstructed data or source hashes differ"
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
