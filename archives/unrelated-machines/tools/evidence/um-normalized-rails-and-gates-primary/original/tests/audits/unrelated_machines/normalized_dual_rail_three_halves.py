#!/usr/bin/env python3
"""归一化双轨模板的联合整数流与实际三半界。

Input is an explicit variable list and explicit clauses. Each variable has
one selector eligible on its two distinct rails at time 1. Each true port
occurrence has rail time 1/K, where K is its sign-rail's actual occurrence
degree, and clause time 1/A_c. Clause A_c is a positive integer and its
actual arity is at most 2*A_c-1. Repeated occurrences are separate jobs.
No preload or background jobs are introduced. Empty rails and unused
variables are allowed. If there are no machines, one empty dummy is used.

JSON --input example:
 {"variables":["x"],
  "clauses":[{"A":2,"ports":[["x","+"],["x","-"]]}]}

All jobs and their sparse original eligible edges, the full actual sigma,
and all machine loads are returned. The constructor uses no SAT, OPT, LP
or rounding oracle. A single integer flow shares all clause capacities.
Default command prints a finite exact audit JSON to stdout. --output uses
exclusive creation, so an existing file is never overwritten.
"""
from __future__ import annotations

from collections import deque
from fractions import Fraction
import re

SOURCE_CLAIMS = ("UM-NORMALIZED-DUAL-RAIL-UNIVERSAL-THREE-HALVES-v1",)


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
        if type(ports) not in (list, tuple) or len(ports) > 2 * A - 1:
            raise ValueError("explicit clause arity must be at most 2*A-1")
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


def construct_normalized_dual_rail(variables, clauses):
    """Construct every actual job placement with global makespan at most 3/2.

    K is always derived from actual occurrences; there is no guessed,
    compressed or externally supplied K. Selectors are explicit per item
    of the variable list. Clause and rail machines are pairwise distinct.
    Degree>=2 rails and degree-(1,1) exceptions use ONE common integer
    flow, with shared clause capacities floor(3*A_c/2).
    """
    variables, clauses, occurrences, by_sign = _validate(variables, clauses)
    N, C = len(variables), len(clauses)
    degree = [[len(row[0]), len(row[1])] for row in by_sign]
    flow = _IntegerFlow()
    source, sink = flow.node(), flow.node()
    clause_node = [flow.node() for c in clauses]
    clause_capacity = [(3 * clause["A"]) // 2 for clause in clauses]
    for c, node in enumerate(clause_node):
        flow.edge(node, sink, clause_capacity[c])
    selector_sign, variable_case = [None] * N, [None] * N
    exceptional_arcs, port_arcs = {}, {}
    fractional_clause, supply = [Fraction(0)] * C, 0
    for v, (positive, negative) in enumerate(degree):
        if min(positive, negative) == 0:
            selector_sign[v] = 0 if positive == 0 else 1
            variable_case[v] = "empty_rail"
        elif max(positive, negative) >= 2:
            selected = 0 if positive >= 2 else 1
            selector_sign[v], variable_case[v] = selected, "heavy_rail"
            rail = flow.node()
            K = degree[v][selected]
            flow.edge(rail, sink, K // 2)
            if Fraction(K, 4) > K // 2:
                raise RuntimeError("heavy-rail fractional capacity failed")
            for o in by_sign[v][selected]:
                c = occurrences[o][2]
                port = flow.node()
                flow.edge(source, port, 1)
                supply += 1
                port_arcs[o] = (flow.edge(port, rail, 1),
                                flow.edge(port, clause_node[c], 1))
                fractional_clause[c] += Fraction(3, 4)
        else:
            if (positive, negative) != (1, 1):
                raise RuntimeError("unclassified rail degrees")
            variable_case[v] = "one_one"
            node = flow.node()
            flow.edge(source, node, 1)
            supply += 1
            for sign in (0, 1):
                o = by_sign[v][sign][0]
                c = occurrences[o][2]
                exceptional_arcs[o] = flow.edge(node, clause_node[c], 1)
                fractional_clause[c] += Fraction(1, 2)
    for c, clause in enumerate(clauses):
        if not fractional_clause[c] <= Fraction(3 * len(clause["ports"]), 4) \
                <= clause_capacity[c]:
            raise RuntimeError("joint fractional clause certificate failed")
    value, augmentations = flow.maxflow(source, sink)
    if value != supply:
        raise RuntimeError("integer full flow missing despite fractional certificate")
    port_machine = [None] * len(occurrences)
    for v in range(N):
        if variable_case[v] == "empty_rail":
            for sign in (0, 1):
                for o in by_sign[v][sign]:
                    port_machine[o] = 2 * v + sign
        elif variable_case[v] == "heavy_rail":
            selected = selector_sign[v]
            for o in by_sign[v][selected]:
                rail_arc, clause_arc = port_arcs[o]
                into_rail, into_clause = flow.amount(rail_arc), flow.amount(clause_arc)
                if (into_rail, into_clause) not in ((1, 0), (0, 1)):
                    raise RuntimeError("port was split or lost in integral readout")
                port_machine[o] = 2 * v + selected if into_rail else 2 * N + occurrences[o][2]
            for o in by_sign[v][1 - selected]:
                port_machine[o] = 2 * v + 1 - selected
        else:
            selected_ports = [o for sign in (0, 1) for o in by_sign[v][sign]
                              if flow.amount(exceptional_arcs[o]) == 1]
            if len(selected_ports) != 1:
                raise RuntimeError("(1,1) variable did not select exactly one occurrence")
            picked = selected_ports[0]
            selector_sign[v] = occurrences[picked][1]
            for sign in (0, 1):
                o = by_sign[v][sign][0]
                port_machine[o] = 2 * N + occurrences[o][2] if o == picked else 2 * v + sign
    machines = []
    for v, label in enumerate(variables):
        for sign in (0, 1):
            machines.append({"machine": len(machines), "kind": "rail",
                             "variable": label, "sign": "+" if sign == 0 else "-"})
    for c, clause in enumerate(clauses):
        machines.append({"machine": len(machines), "kind": "clause", "clause": c})
    if not machines:
        machines.append({"machine": 0, "kind": "dummy"})
    jobs, sigma = [], []
    for v, label in enumerate(variables):
        jobs.append({"job": len(jobs), "kind": "selector", "variable": label,
                     "edges": [[2 * v, Fraction(1)], [2 * v + 1, Fraction(1)]]})
        sigma.append(2 * v + selector_sign[v])
    for o, (v, sign, c, local) in enumerate(occurrences):
        jobs.append({"job": len(jobs), "kind": "port", "variable": variables[v],
                     "sign": "+" if sign == 0 else "-", "clause": c, "occurrence": local,
                     "edges": [[2 * v + sign, Fraction(1, degree[v][sign])],
                               [2 * N + c, Fraction(1, clauses[c]["A"])]]})
        sigma.append(port_machine[o])
    loads = actual_loads(machines, jobs, sigma)
    if max(loads) > Fraction(3, 2):
        raise RuntimeError("actual full-machine three-halves bound failed")
    return {
        "variables": variables, "clauses": clauses, "rail_degrees": degree,
        "variable_cases": variable_case,
        "selector_rails": [2 * v + selector_sign[v] for v in range(N)],
        "machines": machines, "jobs": jobs, "sigma": sigma, "loads": loads,
        "makespan": max(loads), "bound": Fraction(3, 2),
        "flow": {"value": value, "demand": supply, "augmentations": augmentations,
                 "clause_capacities": clause_capacity,
                 "fractional_clause_weights": fractional_clause},
    }


def solve_json_instance(data):
    if type(data) is not dict or set(data) != {"variables", "clauses"}:
        raise ValueError("JSON must contain exactly variables and clauses")
    return construct_normalized_dual_rail(data["variables"], data["clauses"])


def audit():
    """Finite tests and exact small optima; no oracle is called by constructor."""
    from collections import Counter
    import hashlib
    from itertools import product
    from math import lcm
    from pathlib import Path
    from random import Random
    import platform
    import time
    started = time.perf_counter()
    counts, cases = Counter(), Counter()
    rng = Random(110723)

    def check_result(result):
        actual = actual_loads(result["machines"], result["jobs"], result["sigma"])
        assert actual == result["loads"] and max(actual) == result["makespan"] <= Fraction(3, 2)
        assert [job["job"] for job in result["jobs"]] == list(range(len(result["jobs"])))
        assert all(len(job["edges"]) == 2 for job in result["jobs"])
        assert result["flow"]["value"] == result["flow"]["demand"]
        assert result["flow"]["augmentations"] <= result["flow"]["demand"]

    def oracle(result):
        # Full actual assignment enumeration, clearing denominators exactly.
        den = 1
        for job in result["jobs"]:
            for machine, time in job["edges"]:
                den = lcm(den, time.denominator)
        choices = [[(machine, int(time * den)) for machine, time in job["edges"]]
                   for job in result["jobs"]]
        best, states = None, 0
        for allocation in product(*choices):
            loads = [0] * len(result["machines"])
            for machine, time in allocation:
                loads[machine] += time
            cost = max(loads)
            best = cost if best is None else min(best, cost)
            states += 1
        counts["test_only_exact_assignment_states"] += states
        return Fraction(best, den), states

    def clauses_from(pattern, assignment, Ac):
        literals = [(v, "+" if sign == 0 else "-")
                    for v, pair in enumerate(pattern) for sign in (0, 1)
                    for unused in range(pair[sign])]
        rows = [{"A": A, "ports": []} for A in Ac]
        for literal, clause in zip(literals, assignment):
            rows[clause]["ports"].append(literal)
        return rows

    patterns = ([(0, 0)], [(0, 1)], [(0, 3)], [(1, 0)], [(1, 1)],
                [(1, 2)], [(2, 1)], [(2, 2)], [(1, 3)], [(3, 1)],
                [(0, 2), (1, 1)], [(1, 2), (1, 0)], [(1, 1), (2, 1)])
    for pattern in patterns:
        nports = sum(sum(pair) for pair in pattern)
        variables = list(range(len(pattern)))
        for C in (1, 2, 3):
            for assignment in product(range(C), repeat=nports):
                for Ac in product((1, 2, 3), repeat=C):
                    clauses = clauses_from(pattern, assignment, Ac)
                    if any(len(c["ports"]) > 2 * c["A"] - 1 for c in clauses):
                        continue
                    result = construct_normalized_dual_rail(variables, clauses)
                    check_result(result)
                    counts["exhaustive_template_constructions"] += 1
                    cases.update(result["variable_cases"])
                    if C <= 2 and len(pattern) + nports <= 7:
                        optimum, states = oracle(result)
                        assert optimum <= result["makespan"]
                        counts["exhaustive_actual_optima"] += 1
    for unused in range(2000):
        variables = list(range(rng.randrange(9)))
        ports = [(v, sign) for v in variables for sign in ("+", "-")
                 for unused in range(rng.randrange(8))]
        rng.shuffle(ports)
        clauses = []
        while ports:
            arity = rng.randrange(1, min(12, len(ports)) + 1)
            clauses.append({"A": (arity + 2) // 2 + rng.randrange(4), "ports": ports[:arity]})
            del ports[:arity]
        for unused in range(rng.randrange(3)):
            clauses.insert(rng.randrange(len(clauses) + 1), {"A": 1, "ports": []})
        result = construct_normalized_dual_rail(variables, clauses)
        check_result(result)
        counts["random_unbalanced_heterogeneous_clause_constructions"] += 1
        cases.update(result["variable_cases"])

    sharp = {"variables": ["x", "y", "z"], "clauses": [
        {"A": 2, "ports": [["x", "+"], ["x", "+"], ["y", "+"]]},
        {"A": 2, "ports": [["x", "-"], ["x", "-"], ["y", "+"]]},
        {"A": 2, "ports": [["y", "-"], ["z", "+"], ["z", "+"]]},
        {"A": 2, "ports": [["y", "-"], ["z", "-"], ["z", "-"]]},
    ]}
    sharp_result = solve_json_instance(sharp)
    check_result(sharp_result)
    optimum, states = oracle(sharp_result)
    assert len(sharp_result["machines"]) == 10 and len(sharp_result["jobs"]) == 15
    assert sharp_result["rail_degrees"] == [[2, 2]] * 3
    assert optimum == sharp_result["makespan"] == Fraction(3, 2) and states == 2 ** 15
    parent_sigma = [0, 2, 4] + [job["edges"][0][0] if job["sign"] == "-" else job["edges"][1][0]
                                           for job in sharp_result["jobs"][3:]]
    parent_loads = actual_loads(sharp_result["machines"], sharp_result["jobs"], parent_sigma)
    assert parent_loads[6:] == [Fraction(3, 2), Fraction(1, 2), Fraction(1), Fraction(0)]
    counts["repeated_occurrence_sharp_actual_optimum"] += 1
    sharp_record = {"input": sharp, "machines": 10, "jobs": 15,
                    "exact_optimum": optimum, "all_assignment_states": states,
                    "constructed_sigma": sharp_result["sigma"],
                    "constructed_loads": sharp_result["loads"],
                    "explicit_positive_external_sigma": parent_sigma,
                    "explicit_positive_external_loads": parent_loads,
                    "scope": "Repeated occurrences are allowed; no distinct-variable-clause sharpness claim."}

    boundaries = (
        {"variables": [], "clauses": []},
        {"variables": [], "clauses": [{"A": 1, "ports": []}, {"A": 10**120+151, "ports": []}]},
        {"variables": ["unused", "also-unused"], "clauses": []},
        {"variables": [0, 1], "clauses": [{"A": 1, "ports": [[0, "+"]]},
                                               {"A": 1, "ports": [[0, "-"]]},
                                               {"A": 10**120+151, "ports": [[1, "-"], [1, "-"], [1, "-"]]}]},
        {"variables": ["x"], "clauses": [{"A": "2", "ports": [["x", "+"], ["x", "-"]]}]},
    )
    for data in boundaries:
        check_result(solve_json_instance(data))
        counts["empty_zero_degree_A1_giant_integer_boundaries"] += 1
    invalid = (
        {"variables": ["x", "x"], "clauses": []},
        {"variables": [True], "clauses": []},
        {"variables": [1.0], "clauses": []},
        {"variables": "x", "clauses": []},
        {"variables": ["x"], "clauses": [{"A": 0, "ports": []}]},
        {"variables": ["x"], "clauses": [{"A": 1.0, "ports": []}]},
        {"variables": ["x"], "clauses": [{"A": True, "ports": []}]},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [["x", "+"], ["x", "-"]]}]},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [["unknown", "+"]]}]},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [["x", 0]]}]},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [["x"]]}]},
        {"variables": ["x"], "clauses": [{"A": 1, "ports": [], "extra": 0}]},
    )
    for data in invalid:
        try:
            solve_json_instance(data)
        except ValueError:
            counts["invalid_domains_rejected"] += 1
        else:
            raise AssertionError("invalid template accepted")
    return {
        "status": "passed", "source_claims": list(SOURCE_CLAIMS),
        "python": platform.python_version(), "seed": 110723,
        "precision": "integer maxflow and Fraction actual loads",
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "counts": dict(counts), "variable_case_counts": dict(cases),
        "sharp_repeated_occurrence_instance": sharp_record,
        "runtime_seconds": round(time.perf_counter() - started, 3),
        "limits": "Finite audit checks implementation. General three-halves proof is the shared-capacity fractional certificate plus integer flow. Only this normalized template is covered, not arbitrary dual-rail gadgets or general UM hardness. Novelty is not certified.",
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
    parser.add_argument("--input", help="explicit normalized-template JSON")
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
