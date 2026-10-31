#!/usr/bin/env python3
"""占用拟阵最优基面维数的独立有限精确审计。

Only the finite core lemma is tested: for every enumerated weight-exposed
face of a transversal base polytope, the number of nonconstant coordinates
is at most twice its affine dimension.  This is not a full implementation
or test of the fixed-sink scheduling algorithm, and is not a general proof.

Run from the repository root with no arguments.  Results go to stdout;
existing frozen evidence is never overwritten by this script.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
from fractions import Fraction
from pathlib import Path


def exact_rank(rows: list[tuple[int, ...]]) -> int:
    """Rank over Q by Fraction elimination, independent of numerical LP."""
    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [value / divisor for value in matrix[pivot_row]]
        for row in range(pivot_row + 1, len(matrix)):
            multiplier = matrix[row][column]
            if multiplier:
                matrix[row] = [
                    value - multiplier * pivot_value
                    for value, pivot_value in zip(matrix[row], matrix[pivot_row])
                ]
        pivot_row += 1
    return pivot_row


def covering_bases(
    homes: int, macros: int, adjacency: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """Enumerate all home sets of size macros that cover every macro."""
    bases: list[tuple[int, ...]] = []
    for subset in itertools.combinations(range(homes), macros):
        if any(
            all(adjacency[job * homes + assignment[job]] for job in range(macros))
            for assignment in itertools.permutations(subset)
        ):
            bases.append(tuple(int(home in subset) for home in range(homes)))
    return bases


def main() -> None:
    presentations = 0
    faces = 0
    nontrivial_faces = 0
    equality_faces = 0
    for homes in range(1, 5):
        for macros in range(min(2, homes) + 1):
            for adjacency in itertools.product((0, 1), repeat=homes * macros):
                bases = covering_bases(homes, macros, adjacency)
                if not bases:
                    continue
                presentations += 1
                for weights in itertools.product((-1, 0, 1), repeat=homes):
                    costs = [
                        sum(value * weight for value, weight in zip(base, weights))
                        for base in bases
                    ]
                    best = min(costs)
                    vertices = [base for base, cost in zip(bases, costs) if cost == best]
                    differences = [
                        tuple(value - first for value, first in zip(base, vertices[0]))
                        for base in vertices[1:]
                    ]
                    dimension = exact_rank(differences)
                    changing = sum(
                        len({base[home] for base in vertices}) > 1
                        for home in range(homes)
                    )
                    if changing > 2 * dimension:
                        raise AssertionError(
                            {
                                "homes": homes,
                                "macros": macros,
                                "adjacency": adjacency,
                                "weights": weights,
                                "dimension": dimension,
                                "changing_coordinates": changing,
                                "vertices": vertices,
                            }
                        )
                    faces += 1
                    nontrivial_faces += dimension > 0
                    equality_faces += dimension > 0 and changing == 2 * dimension

    # Independent count check: for q=1, exclude the empty row; for q=2,
    # Hall fails when one row is empty or both nonempty rows have the same
    # singleton neighbor.  The overlap of the two empty-row events is counted
    # once.  This checks the enumeration totals without reusing matchings.
    expected_presentations = 0
    expected_faces = 0
    for homes in range(1, 5):
        count = 1 + (2**homes - 1)
        if homes >= 2:
            count += 4**homes - 2 ** (homes + 1) + 1 - homes
        expected_presentations += count
        expected_faces += count * 3**homes
    assert presentations == expected_presentations == 304
    assert faces == expected_faces == 20760
    source = Path(__file__).read_bytes()
    report = {
        "audit": "occupation_base_face_independent",
        "arithmetic": "exact fractions.Fraction Gaussian elimination over Q",
        "domain": {
            "homes": [1, 2, 3, 4],
            "macros": "0 <= macros <= min(2, homes)",
            "adjacency": "all 0/1 macro-by-home matrices; skip no-covering-matching cases",
            "home_weights": [-1, 0, 1],
        },
        "transversal_presentations": presentations,
        "exposed_faces_with_multiplicity": faces,
        "nontrivial_faces_with_multiplicity": nontrivial_faces,
        "positive_dimension_equality_faces_with_multiplicity": equality_faces,
        "violations": 0,
        "claim_checked": "nonconstant coordinates <= 2 * affine face dimension",
        "limitations": [
            "Finite core-lemma enumeration only; not a universal proof.",
            "No private-task DP, heavy-home enumeration, budgeted LP, or scheduling output is tested.",
            "No claim about all possible real weight vectors or larger transversal presentations.",
        ],
        "python": platform.python_version(),
        "script_sha256": hashlib.sha256(source).hexdigest(),
        "status": "finite_checks_passed",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
