"""New exact check of retained raw matrices and historical path certificates.

Does not import the historical constructors; exhaustive only on these fixtures.
"""
from fractions import Fraction as F
from heapq import heappop, heappush
from itertools import product
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parent / "original"


def read(path):
    return json.loads((ROOT / path).read_text())


def loads(matrix, assignment):
    result = [F(0)] * len(matrix)
    for j, i in enumerate(assignment):
        assert matrix[i][j] is not None
        result[i] += matrix[i][j]
    return result


def minimax(states, costs, start, goal, batch=1):
    distance = {start: costs[start]}
    todo = [(costs[start], start)]
    while todo:
        height, state = heappop(todo)
        if distance[state] != height:
            continue
        if state == goal:
            return height
        for other in states:
            if not 1 <= sum(a != b for a, b in zip(state, other)) <= batch:
                continue
            proposed = max(height, costs[other])
            if other not in distance or proposed < distance[other]:
                distance[other] = proposed
                heappush(todo, (proposed, other))
    raise AssertionError("target unreachable")


def check(name, sigma_field, tau, order, certificate):
    source = read("examples/unrelated_machines/" + name + ".json")
    matrix = [[None if x is None else F(x) for x in row]
              for row in source["processing_times"]]
    sigma, tau = tuple(source[sigma_field]), tuple(tau)
    T, C = F(source["T"]), F(source["C"])
    U = max(2*T, C + T/2)
    n = len(sigma)
    assert max(loads(matrix, sigma)) == C
    assert max(loads(matrix, tau)) == T
    assert all(matrix[i][j] <= T for j, i in enumerate(sigma))
    options = [[i for i in range(len(matrix)) if matrix[i][j] is not None]
               for j in range(n)]
    states = list(product(*options))
    costs = {state: max(loads(matrix, state)) for state in states}
    optimum = min(costs.values())
    assert optimum == T
    current, trace = list(sigma), [loads(matrix, sigma)]
    assert sorted(order) == list(range(n))
    for j in order:
        current[j] = tau[j]
        trace.append(loads(matrix, current))
    assert tuple(current) == tau
    peak = max(max(row) for row in trace)
    best = minimax(states, costs, sigma, tau)
    assert best == peak
    result = {"case": name, "actual_assignments": len(states),
              "OPT": str(optimum), "direct_order": order,
              "actual_trace": trace, "direct_peak": str(peak),
              "single_move_minimax": str(best), "U": str(U)}
    if name == "permanent_buffer_priority_deadlock":
        assert trace == [[F(x) for x in row] for row in certificate["good_load_trace"]]
        assert peak == F(certificate["good_peak"])
        fixed, target_in = [F(0)] * len(matrix), [F(0)] * len(matrix)
        for j in range(n):
            if sigma[j] == tau[j]:
                fixed[sigma[j]] += matrix[sigma[j]][j]
            else:
                target_in[tau[j]] += matrix[tau[j]][j]
        h = [max(F(0), a+b-U) for a, b in zip(trace[0], target_in)]
        assert h == list(map(F, certificate["h"]))
        terminal = list(sigma)
        for j in certificate["priority_order"]:
            terminal[j] = tau[j]
        term_load = loads(matrix, terminal)
        assert term_load == list(map(F, certificate["priority_terminal_loads"]))
        remaining_peaks = []
        for j in range(n):
            if terminal[j] == tau[j]:
                continue
            moved = terminal.copy()
            moved[j] = tau[j]
            remaining_peaks.append(max(loads(matrix, moved)))
        assert remaining_peaks == list(map(F, certificate["all_remaining_step_peaks"]))
        assert min(remaining_peaks) > U
        result.update({"h": h, "terminal_loads": term_load,
                       "remaining_step_peaks": remaining_peaks})
    else:
        expected_trace = [[F(x) for x in row["loads"]] for row in certificate["direct_path"]]
        assert trace == expected_trace
        assert peak == F(certificate["U"]) == U
        batch = int(source["batch_budget"])
        first = min(cost for state, cost in costs.items()
                    if 1 <= sum(a != b for a, b in zip(sigma, state)) <= batch)
        batched = minimax(states, costs, sigma, tau, batch)
        assert first == batched == U
        result.update({"batch_budget": batch, "first_batch_minimum": str(first),
                       "batch_minimax": str(batched)})
    return result


def main():
    priority = read("evidence/certificates/unrelated_machines/permanent_buffer_priority_deadlock.json")
    priority_input = read("examples/unrelated_machines/permanent_buffer_priority_deadlock.json")
    transient = read("evidence/certificates/unrelated_machines/transient_peak_two_job_cycle.json")
    results = [
        check("permanent_buffer_priority_deadlock", "sigma", priority_input["tau"],
              priority["good_order"], priority),
        check("transient_peak_two_job_cycle", "initial_assignment",
              transient["target_assignment"], [0, 2, 4, 1, 3, 5], transient),
    ]
    print(json.dumps({"status": "passed", "kind": "new curation replay",
                      "arithmetic": "Fraction/integer", "results": results,
                      "scope": "These two exact input matrices only; universal proofs remain separate."},
                     ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
