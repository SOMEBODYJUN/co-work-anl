#!/usr/bin/env python3
"""Exact two-sign activation-lift audit, using an explicit small CONFIG gap."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import platform
import json


def matrix_rank(matrix):
    mat = [[F(value) for value in row] for row in matrix]
    row = 0
    for col in range(len(mat[0]) if mat else 0):
        pivot = next((r for r in range(row, len(mat)) if mat[r][col]), None)
        if pivot is None:
            continue
        mat[row], mat[pivot] = mat[pivot], mat[row]
        divisor = mat[row][col]
        mat[row] = [value / divisor for value in mat[row]]
        for r in range(len(mat)):
            if r != row and mat[r][col]:
                multiplier = mat[r][col]
                mat[r] = [a - multiplier * b for a, b in zip(mat[r], mat[row])]
        row += 1
    return row


def check_config(machines, jobs, p, cert, expected):
    marginal = {edge: F(0) for edge in p}
    for machine in machines:
        assert sum((weight for _, weight in cert[machine]), F(0)) == 1
        for config, weight in cert[machine]:
            assert weight >= 0 and len(set(config)) == len(config)
            assert all((machine, job) in p for job in config)
            assert sum((p[machine, job] for job in config), F(0)) <= 1
            for job in config:
                marginal[machine, job] += weight
    assert marginal == expected
    for job in jobs:
        assert sum((value for edge, value in marginal.items() if edge[1] == job), F(0)) == 1


def run():
    m = 4
    cores = [f"C{i}" for i in range(m)]
    colors = {cores[0]: 0, cores[1]: 1, cores[2]: 1, cores[3]: 0}
    original = ["G"] + [f"b{i}{a}" for i in range(2) for a in range(3)]
    pstar = {(cores[i], "G"): F(3, 4) for i in range(2)}
    ystar = {core: [] for core in cores}
    for i in range(2):
        local = [f"b{i}{a}" for a in range(3)]
        for job in local:
            pstar[cores[i], job] = F(1, 4)
            pstar[cores[i + 2], job] = F(3, 4)
            ystar[cores[i]].append((("G", job), F(1, 6)))
            ystar[cores[i + 2]].append(((job,), F(1, 3)))
        ystar[cores[i]].append((tuple(local), F(1, 2)))
    xstar = {edge: F(0) for edge in pstar}
    for core, configs in ystar.items():
        for config, weight in configs:
            for job in config:
                xstar[core, job] += weight
    check_config(cores, original, pstar, ystar, xstar)
    for job in original:
        incident = [core for core in cores if (core, job) in pstar]
        assert len(incident) <= 2 and len({colors[core] for core in incident}) == len(incident)
    ell = {core: sum((pstar[edge] * xstar[edge] for edge in pstar if edge[0] == core), F(0))
           for core in cores}
    support_sum = {core: sum((pstar[edge] for edge in pstar if edge[0] == core), F(0))
                   for core in cores}
    eps = F(4, 5)
    beta = (1 - eps) / 4
    fillers = [f"f{i}" for i in range(m)]

    # One-copy skeleton. Copies are made disjoint later.
    orig_private = {job: f"R_{job}" for job in original}
    filler_private = {filler: f"Q{i}" for i, filler in enumerate(fillers)}
    one_machines = cores + list(orig_private.values()) + list(filler_private.values()) + ["W"]
    one_jobs = original + fillers + ["U"]
    one_p = dict(pstar)
    for job in original:
        one_p[orig_private[job], job] = beta
    for i, filler in enumerate(fillers):
        one_p[cores[i], filler] = ell[cores[i]]
        one_p[filler_private[filler], filler] = beta
    one_p["W", "U"] = F(1)

    def one_point(lam):
        x = {edge: F(0) for edge in one_p}
        for edge in pstar:
            x[edge] = lam * xstar[edge]
        for job in original:
            x[orig_private[job], job] = 1 - lam
        for i, filler in enumerate(fillers):
            x[cores[i], filler] = 1 - lam
            x[filler_private[filler], filler] = lam
        x["W", "U"] = 1
        return x

    # Shared inverse-CDF intervals, separately for each active color.
    atoms = []
    for color in (0, 1):
        active = [core for core in cores if colors[core] == color]
        intervals = {}
        breakpoints = {F(0), F(1)}
        for core in active:
            start = F(0)
            intervals[core] = []
            for config, weight in ystar[core]:
                end = start + weight
                intervals[core].append((start, end, config))
                breakpoints.add(end)
                start = end
            assert start == 1
        ordered = sorted(breakpoints)
        for start, end in zip(ordered, ordered[1:]):
            midpoint = (start + end) / 2
            probability = (end - start) / 2
            selected = {core: next(config for left, right, config in intervals[core]
                                   if left <= midpoint < right) for core in active}
            sigma = {job: orig_private[job] for job in original}
            chosen_jobs = set()
            for core, config in selected.items():
                assert not chosen_jobs.intersection(config)
                chosen_jobs.update(config)
                for job in config:
                    sigma[job] = core
            for i, filler in enumerate(fillers):
                sigma[filler] = filler_private[filler] if cores[i] in active else cores[i]
            sigma["U"] = "W"
            atoms.append((probability, sigma))
    assert len(atoms) == 10 and sum((weight for weight, _ in atoms), F(0)) == 1
    reconstructed = {edge: F(0) for edge in one_p}
    for weight, sigma in atoms:
        loads = {machine: F(0) for machine in one_machines}
        for job, machine in sigma.items():
            loads[machine] += one_p[machine, job]
            reconstructed[machine, job] += weight
        assert max(loads.values()) == 1
    assert reconstructed == one_point(F(1, 2))

    def tagged(copy, value):
        return f"{copy}:{value}"

    copies = ("A", "B")
    machines = [tagged(copy, machine) for copy in copies for machine in one_machines]
    jobs = [tagged(copy, job) for copy in copies for job in one_jobs]
    p = {(tagged(copy, machine), tagged(copy, job)): value
         for copy in copies for (machine, job), value in one_p.items()}

    def two_point(theta):
        result = {}
        for copy, lam in (("A", F(1, 2) + theta), ("B", F(1, 2) - theta)):
            result.update({(tagged(copy, machine), tagged(copy, job)): value
                           for (machine, job), value in one_point(lam).items()})
        return result

    x0 = two_point(F(0))
    true_two = {edge: F(0) for edge in p}
    for weight, sigma in atoms:
        loads = {machine: F(0) for machine in machines}
        for copy in copies:
            for job, machine in sigma.items():
                edge = (tagged(copy, machine), tagged(copy, job))
                loads[edge[0]] += p[edge]
                true_two[edge] += weight
        assert max(loads.values()) == 1
    assert true_two == x0

    direction = {edge: F(0) for edge in p}
    for copy, sign in (("A", F(1)), ("B", F(-1))):
        for edge in pstar:
            direction[tagged(copy, edge[0]), tagged(copy, edge[1])] = sign * xstar[edge]
        for job in original:
            direction[tagged(copy, orig_private[job]), tagged(copy, job)] = -sign
        for i, filler in enumerate(fillers):
            direction[tagged(copy, cores[i]), tagged(copy, filler)] = -sign
            direction[tagged(copy, filler_private[filler]), tagged(copy, filler)] = sign
    for job in jobs:
        assert sum((d for edge, d in direction.items() if edge[1] == job), F(0)) == 0
    protected = [tagged(copy, core) for copy in copies for core in cores
                 if support_sum[core] > 1 - eps]
    for core in protected:
        assert sum((p[edge] * d for edge, d in direction.items() if edge[0] == core), F(0)) == 0
    step_records = {}
    for sign in (F(1), F(-1)):
        bounds = [(1 - x0[edge]) / (sign * d) if sign * d > 0
                  else x0[edge] / (-sign * d)
                  for edge, d in direction.items() if d]
        maximum = min(bounds)
        assert maximum == F(1, 2)
        endpoint = {edge: x0[edge] + sign * maximum * direction[edge] for edge in p}
        assert endpoint == two_point(sign / 2)
        step_records[str(sign)] = str(maximum)

    path_samples = (F(-1, 2), F(-1, 4), F(0), F(1, 4), F(1, 2))
    for theta in path_samples:
        expected = two_point(theta)
        cert = {}
        for copy, lam in (("A", F(1, 2) + theta), ("B", F(1, 2) - theta)):
            for i, core in enumerate(cores):
                cert[tagged(copy, core)] = [
                    (tuple(tagged(copy, job) for job in config), lam * weight)
                    for config, weight in ystar[core]
                ] + [((tagged(copy, fillers[i]),), 1 - lam)]
            for job in original:
                cert[tagged(copy, orig_private[job])] = [((tagged(copy, job),), 1 - lam), ((), lam)]
            for filler in fillers:
                cert[tagged(copy, filler_private[filler])] = [((tagged(copy, filler),), lam), ((), 1 - lam)]
            cert[tagged(copy, "W")] = [((tagged(copy, "U"),), F(1))]
        check_config(machines, jobs, p, cert, expected)
        for copy in copies:
            for core in cores:
                machine = tagged(copy, core)
                load = sum((p[edge] * expected[edge] for edge in p if edge[0] == machine), F(0))
                assert load == ell[core]
                if abs(theta) < F(1, 2):
                    excess = sum((p[edge] * (1 - expected[edge]) for edge in p
                                  if edge[0] == machine and 0 < expected[edge] < 1), F(0))
                    assert excess == support_sum[core]

    alive_variables = [edge for edge in p if 0 < x0[edge] < 1]
    alive_jobs = [job for job in jobs if not job.endswith(":U")]
    matrix = [[F(edge[1] == job) for edge in alive_variables] for job in alive_jobs]
    matrix += [[p[edge] if edge[0] == core else F(0) for edge in alive_variables] for core in protected]
    exact_rank = matrix_rank(matrix)
    assert (len(alive_variables), len(alive_jobs), len(protected), exact_rank) == (58, 22, 8, 30)
    assert len(alive_variables) - exact_rank == 28

    eligible = [[core for core in cores if (core, job) in pstar] for job in original]
    optimum = None
    count = 0
    for assignment in product(*eligible):
        count += 1
        loads = {core: F(0) for core in cores}
        for job, core in zip(original, assignment):
            loads[core] += pstar[core, job]
        value = max(loads.values())
        optimum = value if optimum is None else min(optimum, value)
    assert count == 128 and optimum == F(5, 4)
    endpoint_values = {"positive": str(max(F(1), optimum)), "negative": str(max(F(1), optimum))}
    assert all(F(value) > 2 - eps for value in endpoint_values.values())
    return {
        "status": "all Fraction checks passed",
        "epsilon": str(eps), "beta": str(beta),
        "bipartition": {str(color): [core for core in cores if colors[core] == color] for color in (0, 1)},
        "half_activation_true_optimal_atoms": len(atoms),
        "two_copy_optimal_atoms": len(atoms), "two_copy_OPT": "1",
        "N": len(alive_variables), "J": len(alive_jobs), "P": len(protected),
        "rank": exact_rank, "nullity": len(alive_variables) - exact_rank,
        "maximum_steps_by_sign": step_records,
        "full_CONFIG_theta_samples_checked": [str(theta) for theta in path_samples],
        "original_assignments_enumerated": count, "original_exact_OPT": str(optimum),
        "endpoint_exact_completion_values": endpoint_values,
        "scope": "Both signs of one specified direction fail; different direction selection and support reopening remain outside the claim.",
    }


if __name__ == "__main__":
    result = run()
    result["python_version"] = platform.python_version()
    result["arithmetic"] = "fractions.Fraction; exact explicit finite seed"
    result["command"] = "python3 tests/audits/unrelated_machines/configuration_activation_two_sign.py"
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, indent=2))
