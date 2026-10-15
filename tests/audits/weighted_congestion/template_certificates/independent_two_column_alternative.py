#!/usr/bin/env python3
"""Independent exact audit of the finite matrix alternative in two columns.

Exhaust all 819 matrices with 1, 2, or 3 rows, two columns, and entries in
{-1, 0, 1}. The primal uses strict one-dimensional interval intersection;
the dual uses rational vertex enumeration. No LP status or floating point.
Default is stdout only; --output uses exclusive creation.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys


def primal_two_columns(matrix):
    """Solve B(t, 1-t)>0 for 0<=t<=1, retaining strict endpoints."""
    lower, upper = Q(0), Q(1)
    lower_strict = upper_strict = False
    for first, second in matrix:
        slope = first - second
        if slope == 0:
            if second <= 0:
                return None
        elif slope > 0:
            bound = -second / slope
            if bound > lower:
                lower, lower_strict = bound, True
            elif bound == lower:
                lower_strict = True
        else:
            bound = -second / slope
            if bound < upper:
                upper, upper_strict = bound, True
            elif bound == upper:
                upper_strict = True
    if lower > upper or (lower == upper and (lower_strict or upper_strict)):
        return None
    parameter = (lower + upper) / 2
    return (parameter, 1 - parameter)


def square_solve(rows, rhs):
    """Rational Gauss-Jordan elimination; skip nonunique square systems."""
    dimension = len(rhs)
    augmented = [list(row) + [value] for row, value in zip(rows, rhs)]
    assert len(augmented) == dimension
    assert all(len(row) == dimension + 1 for row in augmented)
    for column in range(dimension):
        pivot = next((index for index in range(column, dimension)
                      if augmented[index][column]), None)
        if pivot is None:
            return None
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for index in range(dimension):
            if index != column:
                scale = augmented[index][column]
                augmented[index] = [left - scale * right for left, right
                                    in zip(augmented[index], augmented[column])]
    return tuple(row[-1] for row in augmented)


def dual_vertex(matrix):
    """Enumerate vertices of lambda>=0, sum lambda=1, B^T lambda<=0."""
    row_count = len(matrix)
    inequalities = [tuple(-Q(index == coordinate) for index in range(row_count))
                    for coordinate in range(row_count)]
    inequalities += [tuple(matrix[index][column] for index in range(row_count))
                     for column in range(2)]
    for active in combinations(inequalities, row_count - 1):
        candidate = square_solve(
            [tuple([Q(1)] * row_count), *active],
            [Q(1)] + [Q(0)] * (row_count - 1))
        if candidate is not None and all(
                sum(left * right for left, right in zip(row, candidate)) <= 0
                for row in inequalities):
            return candidate
    return None


def audit():
    counts = {"primal": 0, "dual": 0, "dual_all_columns_equal_zero": 0}
    records = []
    for row_count in (1, 2, 3):
        for entries in product(map(Q, (-1, 0, 1)), repeat=2 * row_count):
            matrix = tuple(entries[2 * index:2 * index + 2]
                           for index in range(row_count))
            primal = primal_two_columns(matrix)
            dual = dual_vertex(matrix)
            assert (primal is None) != (dual is None), (matrix, primal, dual)
            if primal is not None:
                assert all(value >= 0 for value in primal) and sum(primal) == 1
                assert all(sum(value * coefficient for value, coefficient
                               in zip(primal, row)) > 0 for row in matrix)
                counts["primal"] += 1
                certificate = primal
                kind = "primal"
            else:
                assert all(value >= 0 for value in dual) and sum(dual) == 1
                expectations = tuple(sum(dual[index] * matrix[index][column]
                                         for index in range(row_count))
                                     for column in range(2))
                assert all(value <= 0 for value in expectations)
                counts["dual"] += 1
                counts["dual_all_columns_equal_zero"] += all(
                    value == 0 for value in expectations)
                certificate = dual
                kind = "dual"
            records.append({"matrix": [[str(value) for value in row] for row in matrix],
                            "kind": kind, "certificate": list(map(str, certificate))})
    total = sum(3 ** (2 * row_count) for row_count in (1, 2, 3))
    assert len(records) == total == counts["primal"] + counts["dual"]
    certificate_payload = json.dumps(records, sort_keys=True, separators=(",", ":"))
    return {
        "schema_version": 1,
        "status": "PASS",
        "arithmetic": "fractions.Fraction; no tolerance",
        "parameters": {"row_counts": [1, 2, 3], "column_count": 2,
                       "entry_set": [-1, 0, 1], "enumeration": "exhaustive"},
        "matrices_exactly_checked": total,
        "counts": counts,
        "alternatives_exclusive_and_exhaustive": True,
        "ordered_certificate_stream_sha256": hashlib.sha256(
            certificate_payload.encode()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": sys.version.split()[0],
        "limitations": "Finite exact cross-check; not a proof for arbitrary matrices or the WC target."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    payload = json.dumps(audit(), ensure_ascii=False, indent=2) + "\n"
    if arguments.output is not None:
        with arguments.output.open("x") as destination:
            destination.write(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
