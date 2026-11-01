#!/usr/bin/env python3
"""分裂clause容量的双轨三半构造：独立模型、实际全机负载。

Explicit JSON schema is the normalized template's variables/clauses schema,
but clause arity may be <=2*A_c. Every port has rail time 1/K_sign and
external time 1 on EACH of min(A_c,arity) distinct clause-unit machines.
All original eligible edges are output. Binary A_c is never expanded past
its explicit arity. Selectors have time1 on their two distinct rails.

One integer flow is shared by all clauses. No SAT/OPT/LP oracle occurs in
the constructor. Default prints a finite audit JSON to stdout; --input
returns a concrete full sigma; --output exclusively creates a new file.
"""
from __future__ import annotations
from collections import deque
from fractions import Fraction
import re

SOURCE_CLAIMS = ("UM-SPLIT-CAPACITY-DUAL-RAIL-THREE-HALVES-v1",)

def _positive_integer(value):
    if type(value) is int:
        out = value
    elif type(value) is str and re.fullmatch(r"\+?\d+", value):
        out = int(value)
    else:
        raise ValueError("A must be an exact positive integer, not bool or float")
    if out < 1:
        raise ValueError("A must be positive")
    return out


def _validate(variables, clauses):
    if type(variables) not in (list, tuple):
        raise ValueError("variables must be an explicit list")
    variables = list(variables)
    if any(type(v) not in (int, str) for v in variables) \
            or len(set(variables)) != len(variables):
        raise ValueError("variable labels must be distinct integer or string IDs")
    index = {v: i for i, v in enumerate(variables)}
    if type(clauses) not in (list, tuple):
        raise ValueError("clauses must be an explicit list")
    clean, occurrences = [], []
    by_sign = [[[], []] for v in variables]
    for c, clause in enumerate(clauses):
        if type(clause) is not dict or set(clause) != {"A", "ports"}:
            raise ValueError("each clause must contain exactly A and ports")
        A = _positive_integer(clause["A"])
        ports = clause["ports"]
        if type(ports) not in (list, tuple) or len(ports) > 2 * A:
            raise ValueError("explicit clause arity must be at most 2*A")
        row = []
        for local, port in enumerate(ports):
            if type(port) not in (list, tuple) or len(port) != 2:
                raise ValueError("each occurrence is a variable/sign pair")
            label, sign = port
            if type(label) not in (int, str) or label not in index \
                    or type(sign) is not str or sign not in ("+", "-"):
                raise ValueError("unknown variable or noncanonical sign")
            v, s = index[label], 0 if sign == "+" else 1
            o = len(occurrences)
            occurrences.append((v, s, c, local))
            by_sign[v][s].append(o)
            row.append((label, sign))
        clean.append({"A": A, "ports": row})
    return variables, clean, occurrences, by_sign


class _IntegerFlow:
    """Edmonds-Karp with integer capacities and retained parallel-edge handles."""
    def __init__(self):
        self.graph = []

    def node(self):
        self.graph.append([])
        return len(self.graph) - 1

    def edge(self, u, v, capacity):
        edge = [v, len(self.graph[v]), capacity, capacity]
        reverse = [u, len(self.graph[u]), 0, 0]
        self.graph[u].append(edge)
        self.graph[v].append(reverse)
        return u, len(self.graph[u]) - 1

    def amount(self, handle):
        u, position = handle
        edge = self.graph[u][position]
        return edge[3] - edge[2]

    def maxflow(self, source, sink):
        total, augmentations = 0, 0
        while True:
            previous = [None] * len(self.graph)
            previous[source] = (-1, -1)
            queue = deque([source])
            while queue and previous[sink] is None:
                u = queue.popleft()
                for position, edge in enumerate(self.graph[u]):
                    v, reverse, capacity, original = edge
                    if capacity and previous[v] is None:
                        previous[v] = (u, position)
                        queue.append(v)
            if previous[sink] is None:
                return total, augmentations
            capacity, v = None, sink
            while v != source:
                u, position = previous[v]
                current = self.graph[u][position][2]
                capacity = current if capacity is None else min(capacity, current)
                v = u
            if capacity is None or capacity <= 0:
                raise RuntimeError("nonpositive augmenting path")
            v = sink
            while v != source:
                u, position = previous[v]
                edge = self.graph[u][position]
                edge[2] -= capacity
                self.graph[v][edge[1]][2] += capacity
                v = u
            total += capacity
            augmentations += 1


def actual_loads(machines, jobs, sigma):
    """Read every original sparse job edge and compute all actual machine loads."""
    if len(sigma) != len(jobs):
        raise ValueError("one machine ID required per original job")
    loads = [Fraction(0)] * len(machines)
    for j, (job, machine) in enumerate(zip(jobs, sigma)):
        if type(machine) is not int or not 0 <= machine < len(machines):
            raise ValueError("invalid actual machine ID")
        eligible = dict(job["edges"])
        if machine not in eligible:
            raise ValueError("unavailable original job edge")
        loads[machine] += eligible[machine]
    return loads


def construct_split_capacity_dual_rail(variables, clauses):
    """Return all original sparse jobs and a full actual schedule at <=3/2.

    Clauses use distinct unit machines, not one machine at time1/A. The
    variable list is explicit; occurrence degrees are derived. Empty rails,
    unused variables, empty clauses and an empty dummy instance are valid.
    """
    variables, clauses, occurrences, by_sign = _validate(variables, clauses)
    N, C = len(variables), len(clauses)
    degree = [[len(row[0]), len(row[1])] for row in by_sign]
    slots = [min(clause["A"], len(clause["ports"])) for clause in clauses]
    flow = _IntegerFlow()
    source, sink = flow.node(), flow.node()
    clause_node = [flow.node() for c in clauses]
    for c in range(C):
        flow.edge(clause_node[c], sink, slots[c])
    selector_sign, supply = [None] * N, 0
    selected_arc, variable_demand = {}, [0] * N
    fractional_clause = [Fraction(0)] * C
    variable_case = []
    for v, (positive, negative) in enumerate(degree):
        if min(positive, negative) == 0:
            selector_sign[v] = 0 if positive == 0 else 1
            variable_case.append("empty_rail")
            continue
        variable_case.append("two_nonempty_rails")
        total = positive + negative
        variable_demand[v] = total // 2
        supply += variable_demand[v]
        node = flow.node()
        flow.edge(source, node, variable_demand[v])
        local_occurrences = by_sign[v][0] + by_sign[v][1]
        fractional_sum = Fraction(0)
        for local, o in enumerate(local_occurrences):
            c = occurrences[o][2]
            port = flow.node()
            selected_arc[o] = flow.edge(node, port, 1)
            flow.edge(port, clause_node[c], 1)
            # Half each occurrence, then remove the unique excess half when odd.
            fraction = Fraction(0) if total % 2 and local == 0 else Fraction(1, 2)
            fractional_clause[c] += fraction
            fractional_sum += fraction
        if fractional_sum != variable_demand[v]:
            raise RuntimeError("fractional source trimming did not match integer demand")
    for c, clause in enumerate(clauses):
        if not fractional_clause[c] <= Fraction(len(clause["ports"]), 2) <= slots[c]:
            raise RuntimeError("shared fractional clause capacity failed")
    value, augmentations = flow.maxflow(source, sink)
    if value != supply:
        raise RuntimeError("integer full flow missing despite fractional certificate")
    selected_counts = [[0, 0] for v in variables]
    for o, arc in selected_arc.items():
        amount = flow.amount(arc)
        if amount not in (0, 1):
            raise RuntimeError("split occurrence in integral flow")
        v, sign, c, local = occurrences[o]
        selected_counts[v][sign] += amount
    for v, (positive, negative) in enumerate(degree):
        if variable_case[v] == "empty_rail":
            continue
        if sum(selected_counts[v]) != variable_demand[v]:
            raise RuntimeError("variable flow demand was not conserved")
        possible = [sign for sign in (0, 1)
                    if selected_counts[v][sign] >= (degree[v][sign] + 1) // 2]
        if not possible:
            raise RuntimeError("no sign reached its half-degree threshold")
        selector_sign[v] = possible[0]
    external_by_clause = [[] for c in clauses]
    is_external = [False] * len(occurrences)
    for o, (v, sign, c, local) in enumerate(occurrences):
        if o in selected_arc and sign == selector_sign[v] and flow.amount(selected_arc[o]):
            is_external[o] = True
            external_by_clause[c].append(o)
    if any(len(external_by_clause[c]) > slots[c] for c in range(C)):
        raise RuntimeError("discarded opposite-sign flows increased clause demand")
    machines = []
    for v, label in enumerate(variables):
        for sign in (0, 1):
            machines.append({"machine": len(machines), "kind": "rail",
                             "variable": label, "sign": "+" if sign == 0 else "-"})
    clause_machines = []
    for c in range(C):
        ids = []
        for slot in range(slots[c]):
            ids.append(len(machines))
            machines.append({"machine": len(machines), "kind": "clause_unit",
                             "clause": c, "slot": slot})
        clause_machines.append(ids)
    if not machines:
        machines.append({"machine": 0, "kind": "dummy"})
    external_destination = {}
    for c in range(C):
        for o, machine in zip(external_by_clause[c], clause_machines[c]):
            external_destination[o] = machine
    jobs, sigma = [], []
    for v, label in enumerate(variables):
        jobs.append({"job": len(jobs), "kind": "selector", "variable": label,
                     "edges": [[2 * v, Fraction(1)], [2 * v + 1, Fraction(1)]]})
        sigma.append(2 * v + selector_sign[v])
    for o, (v, sign, c, local) in enumerate(occurrences):
        rail = 2 * v + sign
        edges = [[rail, Fraction(1, degree[v][sign])]] + [
            [machine, Fraction(1)] for machine in clause_machines[c]]
        jobs.append({"job": len(jobs), "kind": "port", "variable": variables[v],
                     "sign": "+" if sign == 0 else "-", "clause": c,
                     "occurrence": local, "edges": edges})
        sigma.append(external_destination[o] if is_external[o] else rail)
    loads = actual_loads(machines, jobs, sigma)
    if max(loads) > Fraction(3, 2):
        raise RuntimeError("actual all-machine three-halves bound failed")
    if any(loads[machine] > 1 for ids in clause_machines for machine in ids):
        raise RuntimeError("a clause unit received multiple external jobs")
    return {
        "variables": variables, "clauses": clauses, "rail_degrees": degree,
        "variable_cases": variable_case, "selector_rails": [2 * v + selector_sign[v] for v in range(N)],
        "clause_unit_counts": slots, "clause_machines": clause_machines,
        "machines": machines, "jobs": jobs, "sigma": sigma, "loads": loads,
        "makespan": max(loads), "bound": Fraction(3, 2),
        "flow": {"value": value, "demand": supply, "augmentations": augmentations,
                 "variable_demands": variable_demand, "selected_sign_counts": selected_counts,
                 "fractional_clause_weights": fractional_clause,
                 "actual_external_counts": [len(row) for row in external_by_clause]},
    }


def solve_json_instance(data):
    if type(data) is not dict or set(data) != {"variables", "clauses"}:
        raise ValueError("JSON must contain exactly variables and clauses")
    return construct_split_capacity_dual_rail(data["variables"], data["clauses"])


def audit():
    """Finite full-load checks; sharpness uses exact mode/capacity certificates."""
    from collections import Counter
    import hashlib
    from itertools import product
    from math import prod
    from pathlib import Path
    from random import Random
    import platform
    import time
    started = time.perf_counter()
    counts, cases = Counter(), Counter()
    rng = Random(110729)

    def check_result(result):
        loads = actual_loads(result["machines"], result["jobs"], result["sigma"])
        assert loads == result["loads"] and max(loads) == result["makespan"] <= Fraction(3, 2)
        assert all(loads[m] <= 1 for row in result["clause_machines"] for m in row)
        nports = sum(len(clause["ports"]) for clause in result["clauses"])
        N = len(result["variables"])
        assert sum(result["clause_unit_counts"]) <= nports
        assert len(result["machines"]) == max(1, 2 * N + sum(result["clause_unit_counts"]))
        assert result["flow"]["value"] == result["flow"]["demand"]
        assert result["flow"]["augmentations"] <= result["flow"]["demand"]
        assert [job["job"] for job in result["jobs"]] == list(range(len(result["jobs"])))
        for job in result["jobs"]:
            if job["kind"] == "port":
                assert len(job["edges"]) == 1 + result["clause_unit_counts"][job["clause"]]
                assert all(time == 1 for m, time in job["edges"][1:])
        assert sum(len(job["edges"]) for job in result["jobs"]) <= 2 * N + nports * (1 + nports)

    patterns = ([(0, 0)], [(0, 1)], [(0, 3)], [(1, 0)], [(1, 1)],
                [(1, 2)], [(2, 1)], [(2, 2)], [(1, 3)], [(3, 1)],
                [(0, 2), (1, 1)], [(1, 2), (1, 0)], [(1, 1), (2, 1)])
    for pattern in patterns:
        variables = list(range(len(pattern)))
        literals = [(v, "+" if sign == 0 else "-")
                    for v, pair in enumerate(pattern) for sign in (0, 1)
                    for unused in range(pair[sign])]
        for C in (1, 2, 3):
            for placement in product(range(C), repeat=len(literals)):
                for Ac in product((1, 2, 3), repeat=C):
                    clauses = [{"A": A, "ports": []} for A in Ac]
                    for literal, c in zip(literals, placement):
                        clauses[c]["ports"].append(literal)
                    if any(len(c["ports"]) > 2 * c["A"] for c in clauses):
                        continue
                    result = construct_split_capacity_dual_rail(variables, clauses)
                    check_result(result)
                    counts["exhaustive_split_template_constructions"] += 1
                    cases.update(result["variable_cases"])
    for unused in range(2000):
        variables = list(range(rng.randrange(9)))
        ports = [(v, sign) for v in variables for sign in ("+", "-")
                 for unused in range(rng.randrange(8))]
        rng.shuffle(ports)
        clauses = []
        while ports:
            arity = rng.randrange(1, min(12, len(ports)) + 1)
            clauses.append({"A": (arity + 1) // 2 + rng.randrange(4), "ports": ports[:arity]})
            del ports[:arity]
        for unused in range(rng.randrange(3)):
            clauses.insert(rng.randrange(len(clauses) + 1), {"A": 1, "ports": []})
        result = construct_split_capacity_dual_rail(variables, clauses)
        check_result(result)
        counts["random_split_actual_constructions"] += 1
        cases.update(result["variable_cases"])

    sharp = {"variables": ["x", "y", "z"], "clauses": [
        {"A": 2, "ports": [["x", "+"], ["x", "+"], ["y", "+"]]},
        {"A": 2, "ports": [["x", "-"], ["x", "-"], ["y", "+"]]},
        {"A": 2, "ports": [["y", "-"], ["z", "+"], ["z", "+"]]},
        {"A": 2, "ports": [["y", "-"], ["z", "-"], ["z", "-"]]},
    ]}
    result = solve_json_instance(sharp)
    check_result(result)
    assert len(result["machines"]) == 14 and len(result["jobs"]) == 15
    assert result["rail_degrees"] == [[2, 2]] * 3
    assert result["makespan"] == Fraction(3, 2)
    ports = result["jobs"][3:]
    assert {time for job in result["jobs"] for m, time in job["edges"]} == {Fraction(1, 2), Fraction(1)}
    selector_cuts = []
    for selector_signs in product((0, 1), repeat=3):
        required = [0] * 4
        for job in ports:
            v = sharp["variables"].index(job["variable"])
            sign = 0 if job["sign"] == "+" else 1
            if sign == selector_signs[v]:
                required[job["clause"]] += 1
        violated = [c for c in range(4) if required[c] > result["clause_unit_counts"][c]]
        assert violated
        selector_cuts.append({"selector_signs": list(selector_signs),
                              "forced_external_counts_at_C_le_1": required,
                              "violated_clauses": violated})
    # Exhaust all selector/inside-outside MODES, not physical slot assignments.
    # At C<=1 an external unit slot can receive at most one job. Since every
    # external port of c is eligible on every slot of c, count<=slot_count is
    # exactly the existence condition for the external part of that mode.
    mode_states, feasible_at_one = 0, 0
    for selector_signs in product((0, 1), repeat=3):
        for external_bits in product((0, 1), repeat=12):
            rail_half_load = [0] * 6
            for v, sign in enumerate(selector_signs):
                rail_half_load[2 * v + sign] = 2
            external = [0] * 4
            for job, outside in zip(ports, external_bits):
                if outside:
                    external[job["clause"]] += 1
                else:
                    rail_half_load[job["edges"][0][0]] += 1
            feasible = max(rail_half_load) <= 2 and all(
                external[c] <= result["clause_unit_counts"][c] for c in range(4))
            feasible_at_one += feasible
            mode_states += 1
    assert mode_states == 2 ** 15 and feasible_at_one == 0
    physical_count = prod(len(job["edges"]) for job in result["jobs"])
    assert physical_count == 2 ** 3 * 3 ** 12
    sharp_record = {
        "input": sharp, "machines": 14, "jobs": 15,
        "actual_sigma": result["sigma"], "actual_loads": result["loads"],
        "actual_upper": result["makespan"], "exact_optimum": Fraction(3, 2),
        "lower_certificate": {
            "selector_capacity_cut_patterns": selector_cuts,
            "selector_patterns_checked": 8,
            "inside_outside_modes_checked": mode_states,
            "feasible_modes_at_C_le_1": feasible_at_one,
            "physical_assignments_enumerated": 0,
            "physical_assignment_space_size": physical_count,
            "argument": "Every actual load is a multiple of 1/2. C<3/2 implies C<=1. The exhaustive capacity cuts/modes exclude C<=1; all external jobs of a clause share all its unit slots, so the count test is exact for that threshold. Combined with the actual sigma upper bound, OPT=3/2.",
        },
        "scope": "Repeated occurrences allowed. This is the split-unit-machine model, not the merged normalized clause model.",
    }
    counts["sharp_selector_capacity_patterns"] = 8
    counts["sharp_inside_outside_modes"] = mode_states
    counts["physical_assignments_enumerated"] = 0
    boundaries = (
        {"variables": [], "clauses": []},
        {"variables": [], "clauses": [{"A": 10**120+151, "ports": []}]},
        {"variables": ["unused", "also-unused"], "clauses": []},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [["x", "+"], ["x", "-"]]}]},
        {"variables": ["x"], "clauses": [{"A": 10**120+151, "ports": [["x", "+"], ["x", "-"], ["x", "-"]]}]},
    )
    for data in boundaries:
        check_result(solve_json_instance(data))
        counts["empty_A1_even_arity_giant_A_boundaries"] += 1
    invalid = (
        {"variables": ["x", "x"], "clauses": []},
        {"variables": [True], "clauses": []},
        {"variables": ["x"], "clauses": [{"A": 0, "ports": []}]},
        {"variables": ["x"], "clauses": [{"A": 1.0, "ports": []}]},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [["x", "+"], ["x", "-"], ["x", "-"]]}]},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [["unknown", "+"]]}]},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [["x", 0]]}]},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [["x"]]}]},
    )
    for data in invalid:
        try:
            solve_json_instance(data)
        except ValueError:
            counts["invalid_domains_rejected"] += 1
        else:
            raise AssertionError("invalid split template accepted")
    return {
        "status": "passed", "source_claims": list(SOURCE_CLAIMS),
        "python": platform.python_version(), "seed": 110729,
        "precision": "integer shared maxflow; Fraction all-original-edge actual loads",
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "counts": dict(counts), "variable_case_counts": dict(cases),
        "sharp_repeated_occurrence_instance": sharp_record,
        "runtime_seconds": round(time.perf_counter() - started, 3),
        "limits": "Finite audit is not the general proof. Constructor uses no SAT/OPT/LP. Sharp OPT is certified by an actual sigma plus half-grid/count lower certificate; 2^15 modes are not the 2^3*3^12 physical schedules. No general UM hardness result.",
    }


def _jsonable(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def main():
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="explicit split-capacity template JSON")
    parser.add_argument("--output", help="new result file, exclusive creation")
    args = parser.parse_args()
    if args.input:
        with Path(args.input).open() as handle:
            result = solve_json_instance(json.load(handle))
        payload = {"source_claims": list(SOURCE_CLAIMS), "result": result}
    else:
        payload = audit()
    output = json.dumps(_jsonable(payload), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        with Path(args.output).open("x") as handle:
            handle.write(output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
