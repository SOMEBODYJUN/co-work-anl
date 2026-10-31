"""Independent exact finite audit of the state/dummy resource-distortion bridge.

This implements no restricted Santa Claus approximation algorithm.  It independently
enumerates full original schedules and full auxiliary allocations on tiny inputs.
"""

from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
import hashlib
import json


def case_audit(groups, resource_count, rows, alphas=(F(41, 10), F(7))):
    # State rows are explicit resource coefficient vectors; zeros remain jobs.
    state_group = [g for g, count in enumerate(groups) for _ in range(count)]
    states = len(rows)
    assert states == sum(groups) and resource_count >= 0
    assert all(len(row) == resource_count and sum(row) <= 1 for row in rows)
    assert all(p >= 0 for row in rows for p in row)
    common = prod(p.denominator for row in rows for p in row)
    times = [[int(p * common) for p in row] for row in rows]
    state_sets = [[s for s, g1 in enumerate(state_group) if g1 == g]
                  for g in range(len(groups))]
    jobs = []
    for group in state_sets:
        jobs.append([(s, common) for s in group])
    incidence_index = {}
    for state, row in enumerate(times):
        for resource, value in enumerate(row):
            incidence_index[state, resource] = len(jobs)
            jobs.append([(state, value), (states + resource, common)])

    optimum = None
    for choices in product(*jobs):
        loads = [0] * (states + resource_count)
        for machine, value in choices:
            loads[machine] += value
        peak = max(loads, default=0)
        if optimum is None or peak < optimum:
            optimum = peak
    assert common <= optimum <= 2 * common

    intrinsic = []
    distortion = F(1)
    for resource in range(resource_count):
        positive = [times[state][resource] for state in range(states)
                    if times[state][resource] > 0]
        intrinsic.append(min(positive) if positive else None)
        if positive:
            distortion = max(distortion, F(max(positive), min(positive)))

    # Gift = (kind, label, integer value, interested state indices).
    gifts = []
    for resource, value in enumerate(intrinsic):
        if value is not None:
            gifts.append(("resource", resource, value,
                          [state for state in range(states)
                           if times[state][resource] > 0]))
    for state, row in enumerate(times):
        baseline = common - sum(row)
        if baseline:
            gifts.append(("baseline", state, baseline, [state]))
    for group, group_states in enumerate(state_sets):
        for index in range(len(group_states) - 1):
            gifts.append(("dummy", (group, index), common, group_states))

    allocations = []
    santa_optimum = 0
    for recipients in product(*(gift[3] for gift in gifts)):
        utility = [0] * states
        for gift, recipient in zip(gifts, recipients):
            utility[recipient] += gift[2]
        quality = min(utility)
        santa_optimum = max(santa_optimum, quality)
        allocations.append((recipients, quality))

    deficit = F(2 * common - optimum, common)
    assert F(santa_optimum, common) >= deficit / distortion
    accepted = {str(alpha): 0 for alpha in alphas}
    worst_ratio = {str(alpha): F(0) for alpha in alphas}
    for recipients, quality in allocations:
        has_dummy = set()
        resources_at_state = [[] for _ in range(states)]
        for gift, recipient in zip(gifts, recipients):
            if gift[0] == "dummy":
                has_dummy.add(recipient)
            elif gift[0] == "resource":
                resources_at_state[recipient].append(gift[1])
        selected = [next(state for state in group if state not in has_dummy)
                    for group in state_sets]
        # Reconstruct every original job: incidence defaults to its private end.
        schedule = [None] * len(jobs)
        for group, state in enumerate(selected):
            schedule[group] = (state, common)
        for state, row in enumerate(times):
            for resource, value in enumerate(row):
                schedule[incidence_index[state, resource]] = (state, value)
        for state in selected:
            for resource in resources_at_state[state]:
                schedule[incidence_index[state, resource]] = (states + resource, common)
        assert all(pair in legal for pair, legal in zip(schedule, jobs))
        loads = [0] * (states + resource_count)
        for machine, value in schedule:
            loads[machine] += value
        peak = max(loads, default=0)
        assert peak <= 2 * common - quality
        for alpha in alphas:
            if F(quality) >= F(santa_optimum) / alpha:
                key = str(alpha)
                accepted[key] += 1
                assert F(peak, common) <= 2 - deficit / (alpha * distortion)
                assert F(peak, optimum) <= 2 - 1 / (alpha * distortion)
                worst_ratio[key] = max(worst_ratio[key], F(peak, optimum))
    return {
        "schedules": prod(len(job) for job in jobs),
        "allocations": len(allocations),
        "accepted": accepted,
        "worst_ratio": worst_ratio,
        "kappa": distortion,
        "optimum": F(optimum, common),
        "deficit": deficit,
    }


def main():
    counts = {"instances": 0, "original_schedules": 0, "santa_allocations": 0}
    accepted = {"41/10": 0, "7": 0}
    worst_ratio = {"41/10": F(0), "7": F(0)}
    maximum_kappa = F(1)
    optimum_values = set()
    rows = [row for row in product((F(0), F(1, 2), F(1)), repeat=2)
            if sum(row) <= 1]
    specifications = [((2, 2), 2, grid) for grid in product(rows, repeat=4)]
    # Additional exact rational tests: empty resource sets, singleton states,
    # unused resources, baselines close to 1, extreme heterogeneous denominators.
    specifications.extend([
        ((1,), 0, ((),)),
        ((2, 1), 0, ((), (), ())),
        ((1, 1), 2, ((F(0), F(0)), (F(0), F(0)))),
        ((2, 1), 2, ((F(1, 3), F(2, 3)),
                      (F(1, 6), F(1, 3)), (F(1, 2), F(1, 7)))),
        ((2, 2), 2, ((F(1, 104729), F(1, 100003)),
                      (F(1, 99991), F(0)),
                      (F(1, 524287), F(1, 999983)),
                      (F(0), F(1, 2147483647)))),
    ])
    for groups, resources, grid in specifications:
        result = case_audit(groups, resources, grid)
        counts["instances"] += 1
        counts["original_schedules"] += result["schedules"]
        counts["santa_allocations"] += result["allocations"]
        maximum_kappa = max(maximum_kappa, result["kappa"])
        optimum_values.add(str(result["optimum"]))
        for alpha in accepted:
            accepted[alpha] += result["accepted"][alpha]
            worst_ratio[alpha] = max(worst_ratio[alpha], result["worst_ratio"][alpha])
    report = {
        "status": "all exact finite checks passed",
        "scope": "1296 complete 2-group/2-state/2-resource half-integer matrices, plus five boundaries",
        "counts": counts,
        "approximate_allocations_decoded": accepted,
        "worst_observed_ratios": {key: str(value) for key, value in worst_ratio.items()},
        "maximum_kappa": str(maximum_kappa),
        "original_optimum_values": sorted(optimum_values),
        "not_implemented": "Neither external restricted Santa Claus approximation backend",
        "limitations": "Finite checks do not establish universal mathematics or backend runtime.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
