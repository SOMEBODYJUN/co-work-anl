#!/usr/bin/env python3
"""Frozen implementation attack using independent exhaustive machine cycles.

Run from any directory, supplying --repo when this script is outside the repo:
  python3 cyclic_frozen_independent_crosscheck.py --repo /path/to/repo

All arithmetic is Fraction. Prints a new record to stdout and writes no files.
This imports only the implementation being attacked; the direct oracle below
does not call its cycle predicate, SCC routine, DP, or all-bundles oracle.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import permutations, product
import json
from pathlib import Path
import platform
from random import Random
import sys


def independent_direct(menu, m, margin):
    by_pair = {}
    for arc in menu:
        by_pair.setdefault((arc.source, arc.target), []).append(arc)
    for length in range(2, m + 1):
        for order in permutations(range(m), length):
            if order[0] != min(order):
                continue
            choices = [by_pair.get((order[i], order[(i + 1) % length]), [])
                       for i in range(length)]
            for chosen in product(*choices):
                if all(chosen[i].arrival <=
                       chosen[(i + 1) % length].removal - margin
                       for i in range(length)) and any(
                           chosen[i].arrival < chosen[(i + 1) % length].removal
                           for i in range(length)):
                    return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path,
                        default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    source = (args.repo / 'tests/audits/unrelated_machines/cyclic_batch_repair.py').resolve()
    if not source.is_file():
        parser.error('Cannot locate reviewed source; supply --repo explicitly.')
    source_bytes = source.read_bytes()
    spec = importlib.util.spec_from_file_location('frozen_reviewed_cyclic_batch', source)
    implementation = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = implementation
    spec.loader.exec_module(implementation)
    rng = Random(613516)
    comparisons = positives = 0
    margins = (F(0), F(1, 5), F(7, 6))
    per_machine = []
    for m in range(2, 5):
        local_comparisons = local_positives = 0
        for _ in range(1000):
            menu = [implementation.Arc(u, v, (), F(rng.randrange(13), 5),
                                       F(rng.randrange(13), 5))
                    for u in range(m) for v in range(m) if u != v
                    for _ in range(rng.randrange(3))]
            for margin in margins:
                expected = independent_direct(menu, m, margin)
                actual = implementation.extract_cycle(menu, margin)
                comparisons += 1
                local_comparisons += 1
                assert expected == (actual is not None)
                if actual is None:
                    continue
                positives += 1
                local_positives += 1
                assert len({menu[i].source for i in actual}) == len(actual)
                assert all(menu[actual[i]].target ==
                           menu[actual[(i + 1) % len(actual)]].source and
                           menu[actual[i]].arrival <=
                           menu[actual[(i + 1) % len(actual)]].removal - margin
                           for i in range(len(actual)))
                assert any(menu[actual[i]].arrival <
                           menu[actual[(i + 1) % len(actual)]].removal
                           for i in range(len(actual)))
        per_machine.append({'m': m, 'menu_count': 1000,
                            'comparisons': local_comparisons,
                            'positive_comparisons': local_positives})
    # Detect concurrent modification of the implementation during this run.
    assert source.read_bytes() == source_bytes
    record = {
        'status': 'passed',
        'python': platform.python_version(),
        'arithmetic': 'fractions.Fraction',
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'reviewed_relative_source': 'tests/audits/unrelated_machines/cyclic_batch_repair.py',
        'reviewed_source_sha256': hashlib.sha256(source_bytes).hexdigest(),
        'seed': 613516,
        'machine_range_inclusive': [2, 4],
        'menus_per_machine_count': 1000,
        'weight_numerators': list(range(13)),
        'weight_denominator': 5,
        'arcs_per_ordered_distinct_pair': 'independent rng.randrange(3)',
        'margin_values': list(map(str, margins)),
        'independent_frozen_menu_comparisons': comparisons,
        'positive_comparisons': positives,
        'per_machine_count': per_machine,
        'limitations': [
            'Finite exact sampling is not a proof of the general extraction theorem.',
            'Synthetic Arc weights are nonnegative rational scalars and need not arise from one scheduling instance.',
            'Only extract_cycle is attacked; this record does not audit the DP or full optimizer.',
        ],
    }
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
