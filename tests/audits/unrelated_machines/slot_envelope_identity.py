#!/usr/bin/env python3
"""Small exact audit of the ST slot-envelope identities.

This script is self-contained. It reads no repository, credentials, or network
resources. Its only optional output is the requested JSON certificate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform


def floor_q(value: F) -> int:
    return value.numerator // value.denominator


def ceil_q(value: F) -> int:
    return -((-value.numerator) // value.denominator)


def validate_row(p: list[F], x: list[F]) -> None:
    assert len(p) == len(x)
    assert all(value >= 0 for value in p)
    assert all(p[t] >= p[t + 1] for t in range(len(p) - 1))
    assert all(0 <= value <= 1 for value in x)


def slot_geometry(p: list[F], x: list[F]) -> dict:
    """Build positive intersections and maxima directly, without prefix formula."""
    validate_row(p, x)
    total = sum(x, F(0))
    slot_count = ceil_q(total)
    maxima = [F(0) for _ in range(slot_count)]
    occupants: list[list[int]] = [[] for _ in range(slot_count)]
    intersections = []
    left = F(0)
    for task, mass in enumerate(x):
        right = left + mass
        for slot in range(slot_count):
            overlap = min(right, F(slot + 1)) - max(left, F(slot))
            if overlap > 0:
                occupants[slot].append(task)
                maxima[slot] = max(maxima[slot], p[task])
                intersections.append(
                    {"task": task + 1, "slot": slot + 1, "overlap": overlap}
                )
        left = right
    assert left == total
    assert all(occupants)
    return {
        "slot_count": slot_count,
        "slot_maxima": maxima,
        "slot_occupants": occupants,
        "intersections": intersections,
        "envelope": sum(maxima, F(0)),
    }


def prefix_formula(p: list[F], x: list[F]) -> dict:
    """Independent telescoping expression, without constructing slot edges."""
    cumulative = F(0)
    prefixes = []
    ceilings = []
    terms = []
    for task, mass in enumerate(x):
        cumulative += mass
        ceiling = ceil_q(cumulative)
        next_size = p[task + 1] if task + 1 < len(p) else F(0)
        prefixes.append(cumulative)
        ceilings.append(ceiling)
        terms.append((p[task] - next_size) * ceiling)
    return {
        "prefixes": prefixes,
        "ceilings": ceilings,
        "terms": terms,
        "envelope": sum(terms, F(0)),
    }


def floor_chain_at(x: list[F], offset: F) -> list[int]:
    assert 0 <= offset < 1
    left_floor = floor_q(offset)
    cumulative = F(0)
    selected = []
    for mass in x:
        cumulative += mass
        right_floor = floor_q(cumulative + offset)
        selected.append(right_floor - left_floor)
        left_floor = right_floor
    return selected


def exact_floor_chain(p: list[F], x: list[F], envelope: F) -> dict:
    """Compute all offset atoms and also inspect every included breakpoint."""
    validate_row(p, x)
    prefixes = []
    cumulative = F(0)
    breakpoints = {F(0), F(1)}
    for mass in x:
        cumulative += mass
        prefixes.append(cumulative)
        fraction = cumulative - floor_q(cumulative)
        if fraction:
            breakpoints.add(1 - fraction)
    points = sorted(breakpoints)
    marginals = [F(0) for _ in x]
    atoms = []
    for left, right in zip(points, points[1:]):
        assert left < right
        midpoint = (left + right) / 2
        selected = floor_chain_at(x, midpoint)
        assert all(value in (0, 1) for value in selected)
        weight = right - left
        load = sum((size * bit for size, bit in zip(p, selected)), F(0))
        assert load <= envelope
        selected_prefix = 0
        for task, bit in enumerate(selected):
            selected_prefix += bit
            assert selected_prefix <= ceil_q(prefixes[task])
            marginals[task] += weight * bit
        atoms.append(
            {
                "offset_interval": [left, right],
                "weight": weight,
                "selected_tasks": [j + 1 for j, bit in enumerate(selected) if bit],
                "load": load,
            }
        )
    assert sum((atom["weight"] for atom in atoms), F(0)) == 1
    assert marginals == x
    assert len(atoms) <= len(x) + 1

    endpoint_checks = []
    for offset in points[:-1]:  # Offset 1 is outside the half-open domain.
        selected = floor_chain_at(x, offset)
        assert all(value in (0, 1) for value in selected)
        load = sum((size * bit for size, bit in zip(p, selected)), F(0))
        assert load <= envelope
        for task in range(len(x)):
            assert sum(selected[: task + 1]) <= ceil_q(prefixes[task])
        endpoint_checks.append(
            {"offset": offset, "selected_tasks": [j + 1 for j, bit in enumerate(selected) if bit], "load": load}
        )
    return {
        "breakpoints": points,
        "atoms": atoms,
        "marginals": marginals,
        "endpoint_checks": endpoint_checks,
        "passed": True,
    }


def row_case(name: str, p: list[F], x: list[F], expected: F) -> dict:
    geometry = slot_geometry(p, x)
    formula = prefix_formula(p, x)
    assert geometry["envelope"] == formula["envelope"] == expected
    linear_load = sum((size * mass for size, mass in zip(p, x)), F(0))
    defect = F(0)
    for task, prefix in enumerate(formula["prefixes"]):
        next_size = p[task + 1] if task + 1 < len(p) else F(0)
        defect += (p[task] - next_size) * (ceil_q(prefix) - prefix)
    assert expected - linear_load == defect
    chain = exact_floor_chain(p, x, expected)
    return {
        "name": name,
        "p": p,
        "x": x,
        "capacity": expected,
        "geometry": geometry,
        "prefix_formula": formula,
        "linear_load": linear_load,
        "ceiling_defect": defect,
        "floor_chain": chain,
        "passed": True,
    }


def audit_epigraph_section_difference() -> dict:
    p = [F(1)]
    capacity = F(1, 2)
    at_zero = slot_geometry(p, [F(0)])["envelope"]
    at_one = slot_geometry(p, [F(1)])["envelope"]
    at_half = slot_geometry(p, [F(1, 2)])["envelope"]
    mixed_x = F(1, 2) * 0 + F(1, 2) * 1
    mixed_height = F(1, 2) * at_zero + F(1, 2) * at_one
    assert (at_zero, at_one, at_half) == (0, 1, 1)
    assert mixed_x == mixed_height == capacity
    assert at_half > capacity
    return {
        "p": p,
        "capacity": capacity,
        "sublevel_set": "{0}: every x>0 has ceil(x)=1>B",
        "sublevel_convex_hull": "{0}",
        "epigraph_vertices": [{"weight": F(1, 2), "x": F(0), "height": at_zero}, {"weight": F(1, 2), "x": F(1), "height": at_one}],
        "convex_epigraph_point": {"x": mixed_x, "height": mixed_height},
        "envelope_at_mixed_x": at_half,
        "point_in_fixed_capacity_sublevel_convex_hull": False,
        "point_in_convex_epigraph_capacity_section": True,
        "passed": True,
    }


def loads_of_assignment(p: list[list[F]], assignment: tuple[int, ...]) -> list[F]:
    """Recompute loads from the original matrix and actual chosen machines."""
    loads = [F(0) for _ in p]
    for task, machine in enumerate(assignment):
        loads[machine] += p[machine][task]
    return loads


def audit_two_machine_global() -> dict:
    p = [[F(3, 5), F(2, 5), F(3, 10)] for _ in range(2)]
    x = [[F(1, 2), F(1, 2), F(1)], [F(1, 2), F(1, 2), F(0)]]
    assert all(sum((row[j] for row in x), F(0)) == 1 for j in range(3))
    rows = [slot_geometry(p_i, x_i) for p_i, x_i in zip(p, x)]
    envelopes = [row["envelope"] for row in rows]
    assert envelopes == [F(9, 10), F(3, 5)]

    # Exhaust all eight original assignments, independently of x and slot graph.
    enumerated = []
    opt = None
    for assignment in product(range(2), repeat=3):
        loads = loads_of_assignment(p, assignment)
        makespan = max(loads)
        opt = makespan if opt is None else min(opt, makespan)
        enumerated.append({"assignment": [i + 1 for i in assignment], "loads": loads, "makespan": makespan})
    assert len(enumerated) == 8 and opt == F(7, 10)

    # Build the actual task-slot graph from direct geometric intersections.
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(3)]
    for machine, row in enumerate(rows):
        for slot, occupants in enumerate(row["slot_occupants"]):
            for task in occupants:
                adjacency[task].append((machine, slot))
    matched: dict[tuple[int, int], int] = {}

    def augment(task: int, visited: set[tuple[int, int]]) -> bool:
        for slot in adjacency[task]:
            if slot in visited:
                continue
            visited.add(slot)
            previous = matched.get(slot)
            if previous is None or augment(previous, visited):
                matched[slot] = task
                return True
        return False

    for task in range(3):
        assert augment(task, set())
    assert len(matched) == 3
    assignment = [-1] * 3
    slot_witness = []
    for (machine, slot), task in sorted(matched.items()):
        assert assignment[task] == -1
        assert (machine, slot) in adjacency[task]
        assignment[task] = machine
        slot_witness.append({"machine": machine + 1, "slot": slot + 1, "task": task + 1})
    assert all(machine >= 0 for machine in assignment)
    actual_loads = loads_of_assignment(p, tuple(assignment))
    assert all(load <= bound for load, bound in zip(actual_loads, envelopes))
    assert max(actual_loads) == opt

    # Integral optimum is itself a common envelope state attaining OPT.
    integral_x = [[F(int(assignment[j] == i)) for j in range(3)] for i in range(2)]
    integral_envelopes = [slot_geometry(p_i, x_i)["envelope"] for p_i, x_i in zip(p, integral_x)]
    assert integral_envelopes == actual_loads
    return {
        "p": p,
        "x": x,
        "envelopes": envelopes,
        "assignment_enumeration": enumerated,
        "exact_OPT": opt,
        "slot_matching": slot_witness,
        "ST_assignment": [i + 1 for i in assignment],
        "independently_recomputed_ST_loads": actual_loads,
        "integral_OPT_envelopes": integral_envelopes,
        "passed": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    q = 10**20 + 39
    cases = [
        ("hand_fractional_certificate", [F(3, 5), F(2, 5), F(3, 10)], [F(1, 2), F(1, 2), F(1)], F(9, 10)),
        ("empty_row", [], [], F(0)),
        ("zero_times_capacity_zero", [F(0), F(0), F(0)], [F(2, 3), F(1), F(1, 7)], F(0)),
        ("zero_mass", [F(3, 2), F(1), F(1, 3)], [F(0), F(0), F(0)], F(0)),
        ("integer_prefixes", [F(7, 5), F(7, 5), F(1, 5), F(0)], [F(1), F(0), F(1), F(1)], F(8, 5)),
        ("ties_and_zero_coordinate", [F(3, 4), F(3, 4), F(1, 4), F(0)], [F(1, 2), F(0), F(1, 2), F(1)], F(3, 4)),
        ("multiple_third_prefixes", [F(5, 6), F(2, 3), F(1, 6)], [F(2, 3), F(2, 3), F(2, 3)], F(3, 2)),
        ("large_denominator", [F(1), F(1, 2), F(1, 17), F(0)], [F(1, q), F(q - 1, q), F(1, q), F(q - 1, q)], F(18, 17)),
    ]
    result = {
        "claim": "UM-ST-ENVELOPE-CONFIG-IDENTITY-v1",
        "scope": "Eight custom exact boundary cases and two small certificates; not a general proof or general optimizer.",
        "python_version": platform.python_version(),
        "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "row_case_count": len(cases),
        "row_cases": [row_case(*case) for case in cases],
        "epigraph_section_difference": audit_epigraph_section_difference(),
        "two_machine_global_certificate": audit_two_machine_global(),
        "passed": True,
    }
    serialized = json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n"
    if args.output is None:
        print(serialized, end="")
        return
    args.output.write_text(serialized, encoding="utf-8")
    print(json.dumps({"passed": True, "row_cases": len(cases), "global_assignments": 8, "exact_OPT": "7/10", "output": str(args.output), "script_sha256": result["script_sha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
