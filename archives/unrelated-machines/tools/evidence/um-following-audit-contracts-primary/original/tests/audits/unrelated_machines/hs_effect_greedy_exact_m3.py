"""Exact real-moment test of full-HS and rank-one-state effect greedies.

Three identical machines, one unit big, eight quarter-size small jobs.
Latent probability space: all 210 actual makespan-one schedules, uniform.
V1 contains constants and all assignment indicators. No pseudo-moments or
near-flat proof is imported. Every operator and score uses Fraction arithmetic.
"""
from fractions import Fraction as F
from itertools import combinations
from math import gcd, lcm
import json


def actual_optimal_schedules():
    schedules = []
    for big in range(3):
        other = [i for i in range(3) if i != big]
        for subset in combinations(range(1, 9), 4):
            chosen = set(subset)
            schedule = (big,) + tuple(other[0] if j in chosen else other[1] for j in range(1, 9))
            schedules.append(schedule)
    assert len(set(schedules)) == len(schedules) == 210
    for schedule in schedules:
        assert actual_loads(schedule) == [F(1)] * 3
    return schedules


def actual_loads(schedule):
    result = [F(0)] * 3
    for j, machine in enumerate(schedule):
        result[machine] += F(1) if j == 0 else F(1, 4)
    return result


def primitive_integer_vector(vector):
    denominator = lcm(*(x.denominator for x in vector))
    integers = [int(x * denominator) for x in vector]
    divisor = gcd(*integers)
    return [x // divisor for x in integers]


def orthogonal_integer_basis(schedules):
    raw = [[1] * len(schedules)]
    for j in range(9):
        for machine in range(2):
            raw.append([int(schedule[j] == machine) for schedule in schedules])
    basis, norms = [], []
    for feature in raw:
        vector = list(map(F, feature))
        for previous, norm in zip(basis, norms):
            coefficient = sum(x * y for x, y in zip(vector, previous)) / norm
            if coefficient:
                vector = [x - coefficient * y for x, y in zip(vector, previous)]
        if not any(vector):
            continue
        integer = primitive_integer_vector(vector)
        basis.append(integer)
        norms.append(sum(x * x for x in integer))
    assert len(basis) == 17
    assert basis[0] == [1] * len(schedules)
    assert all(sum(x * y for x, y in zip(basis[i], basis[j])) == 0
               for i in range(len(basis)) for j in range(i))
    return basis, norms


def effects(schedules, basis, norms):
    d = len(basis)
    output = []
    for j in range(9):
        job = []
        for machine in range(3):
            subset = [a for a, schedule in enumerate(schedules) if schedule[j] == machine]
            moment = [[sum(basis[u][a] * basis[v][a] for a in subset) for v in range(d)] for u in range(d)]
            operator = [[F(moment[u][v], norms[u]) for v in range(d)] for u in range(d)]
            assert all(norms[u] * operator[u][v] == norms[v] * operator[v][u] for u in range(d) for v in range(d))
            job.append(operator)
        output.append(job)
    # Exact job partitions and exact row load identities, not just inequalities.
    for j in range(9):
        assert all(sum(output[j][machine][u][v] for machine in range(3)) == int(u == v)
                   for u in range(d) for v in range(d))
    for machine in range(3):
        assert all(sum((F(1) if j == 0 else F(1, 4)) * output[j][machine][u][v] for j in range(9)) == int(u == v)
                   for u in range(d) for v in range(d))
    return output


def multiply(A, B):
    d = len(A)
    answer = [[F(0) for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for k in range(d):
            if A[i][k]:
                for j in range(d):
                    if B[k][j]:
                        answer[i][j] += A[i][k] * B[k][j]
    return answer


def hs_squared(A, norms):
    return sum(F(norms[i], norms[j]) * A[i][j] ** 2 for i in range(len(A)) for j in range(len(A)))


def hs_greedy(operators, norms, order):
    d = len(norms)
    K = [[F(int(i == j)) for j in range(d)] for i in range(d)]
    assignment = [None] * 9
    history = []
    for j in order:
        candidates = [multiply(A, K) for A in operators[j]]
        scores = [hs_squared(candidate, norms) for candidate in candidates]
        ties = [i for i in range(3) if scores[i] == max(scores)]
        chosen = ties[0]
        assignment[j] = chosen
        K = candidates[chosen]
        history.append({"job": j, "scores": list(map(str, scores)), "maximizers": ties,
                        "chosen": chosen, "strict_gap": str(scores[chosen] - max(v for i, v in enumerate(scores) if i != chosen))})
    return {"assignment_in_original_job_order": assignment,
            "actual_loads": list(map(str, actual_loads(assignment))), "history": history,
            "final_K_HS_squared": str(hs_squared(K, norms))}


def state_greedy(operators, norms, order):
    # Coordinate of constant vector is (1,0,...). G=diag(norms)/210.
    state = [F(1)] + [F(0)] * (len(norms) - 1)
    assignment = [None] * 9
    history = []
    for j in order:
        candidates = [[sum(A[i][v] * state[v] for v in range(len(norms))) for i in range(len(norms))]
                      for A in operators[j]]
        scores = [sum(F(norms[i], 210) * candidate[i] ** 2 for i in range(len(norms))) for candidate in candidates]
        ties = [i for i in range(3) if scores[i] == max(scores)]
        chosen = ties[0]
        assignment[j] = chosen
        state = candidates[chosen]
        history.append({"job": j, "scores": list(map(str, scores)), "maximizers": ties,
                        "chosen": chosen, "strict_gap": str(scores[chosen] - max(v for i, v in enumerate(scores) if i != chosen))})
    return {"assignment_in_original_job_order": assignment,
            "actual_loads": list(map(str, actual_loads(assignment))), "history": history,
            "final_state_G_norm_squared": str(sum(F(norms[i], 210) * state[i] ** 2 for i in range(len(norms))))}


def audit():
    schedules = actual_optimal_schedules()
    basis, norms = orthogonal_integer_basis(schedules)
    operators = effects(schedules, basis, norms)
    d = len(norms)
    defect = F(0)
    for job in operators:
        for A in job:
            defect += sum(A[i][i] for i in range(d)) - sum(A[i][j] * A[j][i] for i in range(d) for j in range(d))
    assert defect == 66
    order = list(range(9))
    full = hs_greedy(operators, norms, order)
    state = state_greedy(operators, norms, order)
    assert full["assignment_in_original_job_order"] == [0] + [1] * 8
    assert full["actual_loads"] == ["1", "2", "0"]
    assert full["history"][0]["maximizers"] == [0, 1, 2]
    assert full["history"][1]["maximizers"] == [1, 2]
    assert all(row["maximizers"] == [1] for row in full["history"][2:])
    return {"instance": "3 identical machines, big 1, 8 small 1/4", "true_optimum": "1",
            "latent_actual_schedules": 210, "latent_distribution": "uniform 1/210",
            "V1_dimension": d, "orthogonal_basis_integer_norms": norms,
            "job_partition_identity_verified": True, "row_load_identity_verified": True,
            "full_trace_defect": str(defect), "job_order": order,
            "full_HS_greedy": full, "rank_one_state_greedy": state,
            "arithmetic": "Fraction/integer only", "scope": "input order big first, labels ascending on exact ties; not an all-order impossibility"}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
