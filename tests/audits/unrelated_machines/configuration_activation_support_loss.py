#!/usr/bin/env python3
"""Exact finite audit of the CONFIG-preserving activation lift."""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import platform
import json


def validate_config(machines, jobs, p, cert, expected):
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
    original = ["G"] + [f"b{i}{a}" for i in range(2) for a in range(3)]
    pstar = {(cores[i], "G"): F(3, 4) for i in range(2)}
    ystar = {machine: [] for machine in cores}
    for i in range(2):
        local = [f"b{i}{a}" for a in range(3)]
        for job in local:
            pstar[cores[i], job] = F(1, 4)
            pstar[cores[i + 2], job] = F(3, 4)
            ystar[cores[i]].append((("G", job), F(1, 6)))
            ystar[cores[i + 2]].append(((job,), F(1, 3)))
        ystar[cores[i]].append((tuple(local), F(1, 2)))
    xstar = {edge: F(0) for edge in pstar}
    for machine, configs in ystar.items():
        for config, weight in configs:
            for job in config:
                xstar[machine, job] += weight
    validate_config(cores, original, pstar, ystar, xstar)
    assert all(value > 0 for value in xstar.values())
    ell = {machine: sum((pstar[edge] * xstar[edge] for edge in pstar
                         if edge[0] == machine), F(0)) for machine in cores}
    total_support = {machine: sum((pstar[edge] for edge in pstar
                                   if edge[0] == machine), F(0)) for machine in cores}
    assert [ell[machine] for machine in cores] == [F(7, 8), F(7, 8), F(3, 4), F(3, 4)]

    eligible = [[machine for machine in cores if (machine, job) in pstar]
                for job in original]
    opt_star = None
    assignment_count = 0
    for chosen in product(*eligible):
        assignment_count += 1
        loads = {machine: F(0) for machine in cores}
        for job, machine in zip(original, chosen):
            loads[machine] += pstar[machine, job]
        value = max(loads.values())
        opt_star = value if opt_star is None else min(opt_star, value)
    assert assignment_count == 128 and opt_star == F(5, 4)

    eps = F(4, 5)
    beta = (1 - eps) / 4
    fillers = [f"f{i}" for i in range(m)]
    r = {job: f"R_{job}" for job in original}
    q = {fillers[i]: f"Q{i}" for i in range(m)}
    machines = cores + list(r.values()) + list(q.values()) + ["W"]
    jobs = original + fillers + ["U"]
    p = dict(pstar)
    for job in original:
        p[r[job], job] = beta
    for i, filler in enumerate(fillers):
        p[cores[i], filler] = ell[cores[i]]
        p[q[filler], filler] = beta
    p["W", "U"] = F(1)
    assert len(machines) == 2 * m + len(original) + 1
    assert len(jobs) == len(original) + m + 1

    def point(lam):
        x = {edge: F(0) for edge in p}
        for edge in pstar:
            x[edge] = lam * xstar[edge]
        for job in original:
            x[r[job], job] = 1 - lam
        for i, filler in enumerate(fillers):
            x[cores[i], filler] = 1 - lam
            x[q[filler], filler] = lam
        x["W", "U"] = 1
        return x

    x0 = point(F(1, m))
    reconstructed = {edge: F(0) for edge in p}
    atom_count = 0
    atom_weight_sum = F(0)
    for active, core in enumerate(cores):
        for config, weight in ystar[core]:
            atom_count += 1
            probability = weight / m
            atom_weight_sum += probability
            sigma = {job: core if job in config else r[job] for job in original}
            sigma.update({filler: q[filler] if i == active else cores[i]
                          for i, filler in enumerate(fillers)})
            sigma["U"] = "W"
            loads = {machine: F(0) for machine in machines}
            for job, machine in sigma.items():
                assert (machine, job) in p
                loads[machine] += p[machine, job]
                reconstructed[machine, job] += probability
            assert max(loads.values()) == 1
    assert atom_count == 14 and atom_weight_sum == 1 and reconstructed == x0

    checked_path = []
    for lam in (F(1, 4), F(1, 2), F(3, 4), F(1)):
        x = point(lam)
        cert = {}
        for i, core in enumerate(cores):
            cert[core] = [(config, lam * weight) for config, weight in ystar[core]]
            cert[core].append(((fillers[i],), 1 - lam))
        for job in original:
            cert[r[job]] = [((job,), 1 - lam), ((), lam)]
        for filler in fillers:
            cert[q[filler]] = [((filler,), lam), ((), 1 - lam)]
        cert["W"] = [(("U",), F(1))]
        validate_config(machines, jobs, p, cert, x)
        for core in cores:
            assert sum((p[edge] * x[edge] for edge in p if edge[0] == core), F(0)) == ell[core]
        if lam < 1:
            alive = [edge for edge in p if 0 < x[edge] < 1]
            for core in cores:
                excess = sum((p[edge] * (1 - x[edge]) for edge in alive
                              if edge[0] == core), F(0))
                assert excess == total_support[core] > 1 - eps
            for machine in list(r.values()) + list(q.values()):
                excess = sum((p[edge] * (1 - x[edge]) for edge in alive
                              if edge[0] == machine), F(0))
                assert excess <= beta < 1 - eps
        checked_path.append(str(lam))

    direction = {edge: F(0) for edge in p}
    for edge in pstar:
        direction[edge] = xstar[edge]
    for job in original:
        direction[r[job], job] = -1
    for i, filler in enumerate(fillers):
        direction[cores[i], filler] = -1
        direction[q[filler], filler] = 1
    for job in jobs:
        assert sum((d for edge, d in direction.items() if edge[1] == job), F(0)) == 0
    for core in cores:
        assert sum((p[edge] * d for edge, d in direction.items() if edge[0] == core), F(0)) == 0
    bounds = [(1 - x0[edge]) / d if d > 0 else x0[edge] / (-d)
              for edge, d in direction.items() if d]
    maximum_step = min(bounds)
    assert maximum_step == 1 - F(1, m)
    endpoint = {edge: x0[edge] + maximum_step * direction[edge] for edge in p}
    assert endpoint == point(F(1))
    for job in original:
        assert endpoint[r[job], job] == 0
    for i, filler in enumerate(fillers):
        assert endpoint[cores[i], filler] == 0
        assert endpoint[q[filler], filler] == 1
    initial_n = sum(0 < value < 1 for value in x0.values())
    initial_j = len(original) + m
    protected = sum(total_support[core] > 1 - eps for core in cores)
    assert initial_n == len(pstar) + len(original) + 2 * m
    assert initial_n - initial_j - protected == len(pstar)
    endpoint_opt = max(F(1), opt_star)
    assert endpoint_opt == F(5, 4) > 2 - eps

    return {
        "status": "all Fraction checks passed",
        "epsilon": str(eps), "beta": str(beta),
        "original_core_machines": m, "original_jobs": len(original),
        "original_support_edges": len(pstar),
        "original_CONFIG_threshold": "1", "original_exact_OPT": str(opt_star),
        "original_full_assignments_enumerated": assignment_count,
        "lifted_machines": len(machines), "lifted_jobs": len(jobs),
        "lifted_OPT": "1", "explicit_optimal_atoms_checked": atom_count,
        "CONFIG_path_parameters_checked": checked_path,
        "initial_N": initial_n, "initial_J": initial_j, "initial_P": protected,
        "initial_count_slack": initial_n - initial_j - protected,
        "maximal_pivot_step": str(maximum_step),
        "endpoint_exact_completion_OPT": str(endpoint_opt),
        "scope": "One specified support-deleting pivot; no claim all pivot rules fail or endpoint has full column rank.",
        "seed_processing": {f"{machine}:{job}": str(value)
                            for (machine, job), value in pstar.items()},
        "seed_CONFIG": {machine: [{"jobs": list(config), "weight": str(weight)}
                                   for config, weight in configs]
                        for machine, configs in ystar.items()},
    }


if __name__ == "__main__":
    result = run()
    result["python_version"] = platform.python_version()
    result["arithmetic"] = "fractions.Fraction; exhaustive original seed assignments only"
    result["command"] = "python3 tests/audits/unrelated_machines/configuration_activation_support_loss.py"
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, indent=2))
