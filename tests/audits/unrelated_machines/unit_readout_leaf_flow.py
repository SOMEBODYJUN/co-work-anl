#!/usr/bin/env python3
"""任意密度单位双树：共同真实叶流、整数根及祖先兼容剪枝。

The production constructor uses no OPT/LP oracle or quota-forest enumeration.
It independently implements ordinary integral flow and ancestor extraction.
Original-P validation/building and exact whole-schedule load computation are
reused from unit_readout_calibrated_cardinality (not independent of that model
kernel). Every original job gets an actual machine in sigma; omitted original
unit ranges have exact zero load. The guarantee is 1+2**(-1/h), hence uniformly
below two only for fixed height h. For h=1 the guarantee is exactly 3/2.

Input is the existing explicit k,h,variables,clause_capacities leaf schema.
--input returns the actual complete schedule and exact loads. Without --input,
run only a small collection of boundary/ancestor checks. --output creates a
new JSON file exclusively, preserving frozen outputs.
"""
from collections import Counter, deque
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import sys

import unit_readout_calibrated_cardinality as model

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SOURCE_CLAIMS = ("UM-UNIT-READOUT-FIXED-HEIGHT-APPROX-v1",)
VERSION = "unit-readout-leaf-flow-ancestor-v1"


class IntegralFlow:
    """Deterministic Edmonds--Karp with exact binary integer capacities."""

    def __init__(self):
        self.adjacency = {}
        self.edges = []

    def add(self, u, v, capacity):
        if type(capacity) is not int or capacity < 0:
            raise ValueError("nonnegative exact integer capacity required")
        index = len(self.edges)
        self.adjacency.setdefault(u, []).append(index)
        self.adjacency.setdefault(v, []).append(index + 1)
        self.edges.extend([[u, v, capacity, capacity], [v, u, 0, 0]])
        return index

    def maximum(self, source, sink):
        value = 0
        while True:
            previous = {source: None}
            queue = deque([source])
            while queue and sink not in previous:
                u = queue.popleft()
                for index in self.adjacency.get(u, ()):
                    _, v, remaining, _ = self.edges[index]
                    if remaining and v not in previous:
                        previous[v] = index
                        queue.append(v)
            if sink not in previous:
                return value, set(previous)
            amount, v = None, sink
            while v != source:
                index = previous[v]
                residual = self.edges[index][2]
                amount = residual if amount is None else min(amount, residual)
                v = self.edges[index][0]
            v = sink
            while v != source:
                index = previous[v]
                self.edges[index][2] -= amount
                self.edges[index ^ 1][2] += amount
                v = self.edges[index][0]
            value += amount


def common_leaf_flow(instance, b):
    """Test b distinct actual ports per variable, preserving shared capacity."""
    variables = len(instance["roots"])
    network = IntegralFlow()
    source, sink = ("source",), ("sink",)
    port_edges = {}
    for v in range(variables):
        network.add(source, ("variable", v), b)
    total_ports = sum(instance["arity"])
    for job in instance["jobs"]:
        if job["kind"] != "port":
            continue
        j, v, c = job["job"], job["variable"], job["clause"]
        port_edges[j] = network.add(("variable", v), ("port", j), 1)
        network.add(("port", j), ("clause", c), 1)
    for c, capacity in enumerate(instance["A"]):
        network.add(("clause", c), sink, min(capacity, total_ports))
    value, reachable = network.maximum(source, sink)
    selected = [[] for _ in range(variables)]
    for j, index in port_edges.items():
        if network.edges[index][3] - network.edges[index][2]:
            selected[instance["jobs"][j]["variable"]].append(j)
    if value == b * variables:
        if any(len(row) != b for row in selected):
            raise RuntimeError("source saturation lost equal variable supply")
        return selected, None
    cut = [(u, v, initial) for u, v, residual, initial in network.edges
           if initial and u in reachable and v not in reachable]
    cut_capacity = sum(capacity for u, v, capacity in cut)
    if cut_capacity != value or value >= b * variables:
        raise RuntimeError("flow failure lacks a valid separating cut")
    return None, {"tested_common_supply": b, "flow_value": value,
                  "required_value": b * variables, "cut_capacity": cut_capacity,
                  "cut_source_side": sorted(reachable),
                  "cut_forward_edges": cut}


def largest_common_leaf_flow(instance, leaves_per_tree):
    low, high = 0, 2 * leaves_per_tree + 1
    while high - low > 1:
        middle = (low + high) // 2
        selected, _ = common_leaf_flow(instance, middle)
        if selected is None:
            high = middle
        else:
            low = middle
    selected, _ = common_leaf_flow(instance, low)
    if selected is None:
        raise RuntimeError("zero supply or stored feasible supply was rejected")
    cut = None
    if low < 2 * leaves_per_tree:
        impossible, cut = common_leaf_flow(instance, low + 1)
        if impossible is not None:
            raise RuntimeError("largest common leaf supply was not maximal")
    return low, selected, cut


def floor_integer_root(number, exponent, upper_bound):
    """Exact floor(number**(1/exponent)); no floating-point operation."""
    if type(number) is not int or number < 0 or exponent < 1:
        raise ValueError("nonnegative integer radicand and positive exponent required")
    low, high = 0, upper_bound + 1
    while high - low > 1:
        middle = (low + high) // 2
        if middle**exponent <= number:
            low = middle
        else:
            high = middle
    if not low**exponent <= number < (low + 1)**exponent:
        raise RuntimeError("integer root bracket failed")
    return low


def ancestor_subtree(instance, variable, sign, selected_port_jobs, r):
    """Extract an actual complete-depth r-tree from already-flowed leaves."""
    tree = instance["trees"][variable][sign]
    jobs = instance["jobs"]
    leaves = {tuple(jobs[j]["path"]) for j in selected_port_jobs}
    if any(jobs[j]["variable"] != variable or jobs[j]["sign"] != sign
           or jobs[j]["kind"] != "port" for j in selected_port_jobs):
        raise ValueError("the leaf set belongs to a different original tree")
    good = set(leaves)
    chosen_children = {}
    for path in sorted(tree["children"], key=lambda p: (-len(p), p)):
        children = [path + (digit,) for digit in sorted(tree["children"][path])
                    if path + (digit,) in good]
        if len(children) >= r:
            good.add(path)
            chosen_children[path] = children[:r]
    if () not in good:
        return None
    stack = [((), instance["roots"][variable][sign])]
    active, child_jobs, ports = [], [], []
    while stack:
        path, machine = stack.pop()
        active.append(machine)
        for child_path in chosen_children[path]:
            j = instance["path_jobs"][variable, sign, child_path]
            child_jobs.append(j)
            job = jobs[j]
            if job["kind"] == "edge":
                stack.append((child_path, job["child"]))
            else:
                ports.append(j)
    if len(ports) != r**instance["h"] or not set(ports) <= set(selected_port_jobs):
        raise RuntimeError("ancestor extraction changed its true leaf support")
    return {"variable": variable, "sign": sign,
            "root": instance["roots"][variable][sign],
            "active_internal": active, "selected_child_jobs": child_jobs,
            "selected_ports": ports}


def construct_leaf_flow(data):
    instance = model.build_instance(data)
    dependency = {"model_kernel": Path(model.__file__).name,
                  "model_kernel_sha256": sha256(Path(model.__file__).read_bytes()).hexdigest(),
                  "reused_functions": ["build_instance", "finish", "actual_loads"]}
    if not instance["roots"]:
        return model.finish(instance, [], F(0), source_claims=SOURCE_CLAIMS,
                            mode="leaf-flow-empty", exact_optimum=F(0), b=0, r=0,
                            leaves_per_tree=None, forest=None, software_dependency=dependency)
    k, h = instance["k"], instance["h"]
    leaves_per_tree = len(instance["trees"][0][0]["wiring"])
    if leaves_per_tree != k**h:
        raise RuntimeError("explicit full-tree leaf count disagrees with k,h")
    b, flow_ports, maximality_cut = largest_common_leaf_flow(instance, leaves_per_tree)
    sigma = [job["edges"][0][0] if job["kind"] == "selector" else job["parent"]
             for job in instance["jobs"]]
    ratio = {"exact_expression": "1+2^(-1/h)", "height": h,
             "fixed_height_required_for_uniform_epsilon": True}
    if h == 1:
        ratio["exact_value"] = F(3, 2)
    common = {"source_claims": SOURCE_CLAIMS, "b": b,
              "leaves_per_tree": leaves_per_tree, "flow_selected_port_jobs": flow_ports,
              "flow_maximality_cut": maximality_cut, "approximation_ratio": ratio,
              "software_dependency": dependency}
    if b == 0:
        return model.finish(instance, sigma, F(2), **common,
                            mode="leaf-flow-optimum-two", r=0,
                            exact_optimum=F(2), forest=None)
    m = (b + 1) // 2
    q = floor_integer_root(leaves_per_tree - m, h, k)
    r = k - q
    if not 1 <= r <= k or not (q + 1)**h > leaves_per_tree - m:
        raise RuntimeError("leaf-transversal integer threshold failed")
    forests = []
    selected_ports = []
    for v, port_jobs in enumerate(flow_ports):
        bysign = [[j for j in port_jobs if instance["jobs"][j]["sign"] == sign]
                  for sign in (0, 1)]
        sign = 0 if len(bysign[0]) >= len(bysign[1]) else 1
        if len(bysign[sign]) < m:
            raise RuntimeError("majority sign lost the half supply")
        tree = ancestor_subtree(instance, v, sign, bysign[sign], r)
        if tree is None:
            raise RuntimeError("exact leaf-count guarantee lost ancestor feasibility")
        sigma[v] = tree["root"]
        if instance["jobs"][v]["kind"] != "selector":
            raise RuntimeError("model kernel changed selector indexing")
        for j in tree["selected_child_jobs"]:
            job = instance["jobs"][j]
            if job["kind"] == "edge":
                sigma[j] = job["child"]
        forests.append(tree)
        selected_ports.extend(tree["selected_ports"])
    units_used = [0] * len(instance["A"])
    selected_units = []
    for j in sorted(selected_ports):
        c = instance["jobs"][j]["clause"]
        row = instance["ranges"][c]
        if units_used[c] >= row["listed_units"]:
            raise RuntimeError("subtree leaves exceeded the shared original unit capacity")
        sigma[j] = row["start"] + units_used[c]
        units_used[c] += 1
        selected_units.append(sigma[j])
    if len(set(selected_units)) != len(selected_ports):
        raise RuntimeError("original unit injection repeated a machine")
    forest = {"r": r, "variables": forests,
              "selected_leaf_counts": units_used,
              "selected_unit_machines": sorted(selected_units)}
    return model.finish(instance, sigma, F(2) - F(r, k), **common,
                        mode="leaf-flow-ancestor-pruning", r=r, m=m,
                        floor_root=q, forest=forest)


def audit():
    """A few explicit key examples, not a growing random test campaign."""
    cases = []

    def record(name, data):
        result = construct_leaf_flow(data)
        instance = model.build_instance(data)
        loads = model.actual_loads(instance, result["sigma"])
        assert max(loads.values(), default=F(0)) == result["makespan"]
        assert all(row["load"] == loads.get(row["machine"], F(0))
                   for row in result["listed_loads"])
        assert all(value <= 1 for u, value in loads.items() if u >= instance["internal_count"])
        assert len(result["sigma"]) == len(result["jobs"])
        assert result["omitted_unit_machine_load"] == 0
        cases.append({"name": name, "input": data, "result": result})
        return result

    # The prior 4-machine 5-job actual OPT1 instance. The flow algorithm's
    # prescribed half extraction gives C=3/2; a complete C1 witness is checked.
    data = model.encode(1, 2, 1, [0, 0, 0, 0], [2])
    result = record("h1-actual-ratio-three-halves", data)
    assert result["b"] == 2 and result["r"] == 1 and result["makespan"] == F(3, 2)
    instance = model.build_instance(data)
    witness = [job["edges"][0][0] if job["kind"] == "selector" else job["parent"]
               for job in instance["jobs"]]
    units = 0
    for job in instance["jobs"]:
        if job["kind"] == "port" and job["sign"] == 0:
            witness[job["job"]] = instance["ranges"][0]["start"] + units
            units += 1
    assert max(model.actual_loads(instance, witness).values()) == 1
    cases[-1]["complete_OPT1_witness"] = witness
    cases[-1]["OPT1_lower_reason"] = "the selector has processing time 1 on both original roots"
    result = record("competing-variables-b-zero-exact-two",
                    model.encode(2, 2, 1, [0] * 8, [1]))
    assert result["b"] == 0 and result["exact_optimum"] == 2
    assert result["flow_maximality_cut"]["cut_capacity"] < 2
    result = record("zero-capacity-clause", model.encode(1, 1, 1, [0, 0], [0]))
    assert result["b"] == 0 and result["makespan"] == 2
    # A=0/1 no-pins version of the old 64-open ancestor obstruction.
    from itertools import product
    words = list(product(range(4), repeat=3))
    outside_three_cube = [p for p in words if not all(a < 3 for a in p)]
    open_set = {(0, p) for p in outside_three_cube} | {(1, p) for p in outside_three_cube[:27]}
    wiring = list(range(128))
    capacity = [int((sign, p) in open_set) for sign in (0, 1) for p in words]
    data = model.encode(1, 4, 3, wiring, capacity)
    result = record("sixty-four-open-preserves-real-ancestor-obstruction", data)
    assert result["b"] == 64 and result["r"] == 1 and result["makespan"] == F(7, 4)
    instance = model.build_instance(data)
    for sign in (0, 1):
        available = [job["job"] for job in instance["jobs"] if job["kind"] == "port"
                     and job["sign"] == sign and capacity[job["clause"]]]
        assert ancestor_subtree(instance, 0, sign, available, 2) is None
    result = record("explicit-unary-depth-80", model.encode(1, 1, 80, [0, 0], [1]))
    assert result["makespan"] == 1 and len(result["jobs"]) == 161
    huge = 10**5000 + 151
    result = record("over-4300-decimal-digits-original-capacity",
                    model.encode(1, 1, 1, [0, 0], [str(huge)]))
    assert result["makespan"] == 1 and result["full_machine_count"] == huge + 2
    result = record("empty-before-enormous-binary-height",
                    {"k": "18446744073709551617", "h": str(2**100),
                     "variables": [], "clause_capacities": [0]})
    assert result["makespan"] == 0 and result["dummy_used"]
    return {"status": "passed", "version": VERSION, "source_claims": SOURCE_CLAIMS,
            "script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "counts": {"key_actual_schedules": len(cases), "physical_sigma_enumerations": 0,
                       "quota_forest_oracle_enumerations": 0}, "cases": cases,
            "scope": "Exact finite key implementation checks, not a proof or novelty certification. "
                     "The original-P model/load kernel is reused; integer flow and ancestor extraction "
                     "are independently implemented. No production OPT oracle or external LP solver."}


def main():
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="explicit original unit-readout leaf schema JSON")
    parser.add_argument("--output", help="exclusively create a new exact JSON certificate")
    args = parser.parse_args()
    payload = construct_leaf_flow(json.loads(Path(args.input).read_text())) if args.input else audit()
    text = json.dumps(model.jsonable(payload), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with Path(args.output).open("x") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
