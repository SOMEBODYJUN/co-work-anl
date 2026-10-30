#!/usr/bin/env python3
"""Small exact audit for the fixed-direction two-state Hall criterion.

This is deliberately a finite check of the matching equivalence, not a
solver for rail selection or a proof of the scheduling target.
"""
from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product
import json
from pathlib import Path


def hall_ok(incidence: tuple[tuple[int, ...], ...], demand: tuple[int, ...], labels: tuple[int, ...]) -> bool:
    for mask in range(1 << len(labels)):
        subset = [labels[i] for i in range(len(labels)) if mask & (1 << i)]
        neighborhood = {
            resource
            for resource, endpoints in enumerate(incidence)
            if any(label in subset for label in endpoints)
        }
        if sum(demand[label] for label in subset) > len(neighborhood):
            return False
    return True


def matching_ok(incidence: tuple[tuple[int, ...], ...], demand: tuple[int, ...], labels: tuple[int, ...]) -> bool:
    choices = [
        (None,) + tuple(label for label in endpoints if label in labels)
        for endpoints in incidence
    ]
    for assignment in product(*choices):
        used = defaultdict(int)
        for label in assignment:
            if label is not None:
                used[label] += 1
        if all(used[label] >= demand[label] for label in labels):
            return True
    return False


def main() -> None:
    labels = (0, 1, 2)
    incidence_types = tuple(
        endpoints
        for size in (1, 2)
        for endpoints in combinations(labels, size)
    )
    checked = 0
    for pattern in product(range(len(incidence_types)), repeat=4):
        incidence = tuple(incidence_types[index] for index in pattern)
        for demand in product(range(3), repeat=3):
            for mask in range(1 << len(labels)):
                chosen = tuple(label for i, label in enumerate(labels) if mask & (1 << i))
                if hall_ok(incidence, demand, chosen) != matching_ok(incidence, demand, chosen):
                    raise AssertionError((incidence, demand, chosen))
                checked += 1
    result = {
        "incidence_patterns": len(incidence_types) ** 4,
        "fixed_direction_instances": checked,
        "criterion": "Hall subset inequalities iff injective resource payment",
        "finite_check_only": True,
    }
    out = Path(__file__).resolve().parents[3] / "evidence/runs/unrelated_machines/two_state_quota_hall_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
