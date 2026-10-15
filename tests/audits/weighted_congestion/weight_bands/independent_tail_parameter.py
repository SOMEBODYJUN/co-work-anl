#!/usr/bin/env python3
"""Exact ordered-partition audit for the two-weight tail-parameter obstruction.

Only one potential resource is used. There is one player of weight H >= 1
and K = ceil(H**2) players of weight 1. All ordered nonempty partitions,
modulo permutations of the equal-weight players, are enumerated exactly.
This checks a certificate parameter, not nonexistence of equilibria.
"""

import argparse
import hashlib
from fractions import Fraction
import json
import platform
from pathlib import Path


def compositions(n):
    if n == 0:
        yield ()
    else:
        for k in range(1, n + 1):
            for rest in compositions(n - k):
                yield (k,) + rest


def ordered_types(k):
    """A group is (number of light players, indicator of the heavy player)."""
    for comp in compositions(k):
        base = [(count, 0) for count in comp]
        for j in range(len(base)):
            result = base.copy()
            result[j] = (result[j][0], 1)
            yield result
        for j in range(len(base) + 1):
            yield base[:j] + [(0, 1)] + base[j:]


def parameter(parts, heavy, degree):
    later_load = Fraction(0)
    answer = Fraction(0)
    for light_count, has_heavy in reversed(parts):
        assert light_count > 0 or has_heavy == 1
        minimum = Fraction(1) if light_count else heavy
        maximum = heavy if has_heavy else Fraction(1)
        value = maximum / minimum * (1 + later_load / minimum) ** degree
        answer = max(answer, value)
        later_load += light_count + has_heavy * heavy
    return answer


def exact_audit():
    inputs = {
        "heavy_weights": ["1", "3/2", "2", "3"],
        "light_weight": "1",
        "light_count_rule": "ceil(H^2)",
        "degrees": [1, 2, 5],
        "resource_count": 1,
        "enumeration": "all ordered nonempty partitions modulo equal-light permutations",
    }
    records = []
    for heavy_string in inputs["heavy_weights"]:
        heavy = Fraction(heavy_string)
        square = heavy * heavy
        count = -(-square.numerator // square.denominator)
        types = list(ordered_types(count))
        encoded = {tuple(parts) for parts in types}
        assert len(encoded) == len(types), "duplicate group types"
        for parts in types:
            assert sum(group[0] for group in parts) == count
            assert sum(group[1] for group in parts) == 1
        for degree in inputs["degrees"]:
            best = min(parameter(parts, heavy, degree) for parts in types)
            all_in_one = parameter([(count, 1)], heavy, degree)
            assert best == heavy
            assert all_in_one == heavy
            records.append({
                "H": str(heavy),
                "K": count,
                "d": degree,
                "ordered_type_count": len(types),
                "exact_minimum_parameter": str(best),
                "all_in_one_parameter": str(all_in_one),
            })
    return {
        "audit": "two_weight_ordered_partition_tail_parameter",
        "python": platform.python_version(),
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "seed": None,
        "arithmetic": "fractions.Fraction; no tolerance, seed, or floating arithmetic",
        "inputs": inputs,
        "record_count": len(records),
        "records": records,
        "result": "passed",
        "scope": "finite exact checks only; general sharp lower bound requires the three-case proof",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="create a new JSON file; refuse overwrite")
    args = parser.parse_args()
    report = json.dumps(exact_audit(), ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(report, end="")
    else:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(report)


if __name__ == "__main__":
    main()
