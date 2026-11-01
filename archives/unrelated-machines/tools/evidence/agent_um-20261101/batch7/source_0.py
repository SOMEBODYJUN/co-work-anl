#!/usr/bin/env python3
"""Statement-first independent finite audit; no candidate/production imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import platform
import random


def relation(machine_count, auxiliary, ports, signs, threshold):
    loads = set()
    options = [[i for i, p in enumerate(row) if p is not None] for row in auxiliary]
    for assignment in product(*options):
        vector = [F(0)] * machine_count
        for j, i in enumerate(assignment):
            vector[i] += auxiliary[j][i]
        loads.add(tuple(vector))
    feasible = set()
    for bits in product((0, 1), repeat=len(ports)):
        inward = [F(0)] * machine_count
        for bit, sign, (machine, p) in zip(bits, signs, ports):
            if bit == sign:
                inward[machine] += p
        if any(all(a + b <= threshold for a, b in zip(inward, vector))
               for vector in loads):
            feasible.add(bits)
    return feasible


def check_relation(feasible, ports, signs):
    k = len(ports)
    for bits in feasible:
        internal = [j for j in range(k) if bits[j] == signs[j]]
        for choices in product((False, True), repeat=len(internal)):
            relaxed = list(bits)
            for j, turn_out in zip(internal, choices):
                if turn_out:
                    relaxed[j] = 1 - signs[j]
            assert tuple(relaxed) in feasible
        for j, (_, p) in enumerate(ports):
            if p == 0:
                flipped = list(bits)
                flipped[j] ^= 1
                assert tuple(flipped) in feasible
    if (0,) * k in feasible and (1,) * k in feasible:
        a = sum(s == 0 for s in signs)
        assert len(feasible) >= 2 ** a + 2 ** (k - a) - 1
        positive_a = sum(p > 0 and s == 0 for (_, p), s in zip(ports, signs))
        positive_b = sum(p > 0 and s == 1 for (_, p), s in zip(ports, signs))
        zero = sum(p == 0 for _, p in ports)
        assert len(feasible) >= 2 ** zero * (2 ** positive_a + 2 ** positive_b - 1)
        if k >= 2:
            mixed_neighbors = [x for x in feasible if x not in ((0,) * k, (1,) * k)
                               and (sum(x) == 1 or sum(x) == k - 1)]
            assert mixed_neighbors
        return True
    return False


def uniform_machine_matching(machine_times, eligible, threshold):
    """Independent unit-slot matching for the row-uniform scheduling claim."""
    n = len(eligible)
    capacity = [n if t == 0 else min(n, int(threshold / t)) for t in machine_times]
    slots = [(i, h) for i, cap in enumerate(capacity) for h in range(cap)]
    occupied = {}
    def augment(job, visited):
        for slot in slots:
            if slot[0] not in eligible[job] or slot in visited:
                continue
            visited.add(slot)
            if slot not in occupied or augment(occupied[slot], visited):
                occupied[slot] = job
                return True
        return False
    for job in range(n):
        if not augment(job, set()):
            return None
    assignment = [None] * n
    for (machine, _), job in occupied.items():
        assignment[job] = machine
    assert all(machine is not None for machine in assignment)
    return assignment


def registered_private_host_schedules():
    """Read the actual registered input and reconstruct complete assignments."""
    path = (Path(__file__).resolve().parents[3] / 'examples' /
            'unrelated_machines' / 'signed_one_job_port_sharp_profiles.json')
    data = json.loads(path.read_text())
    sharp, threshold = data['sharp'], F(data['T'])
    internal = sharp['internal_machines']
    external = sharp['external_machines']
    assert len(set(internal + external)) == len(internal + external)
    index = {machine: i for i, machine in enumerate(internal)}
    auxiliary = []
    for edges in sharp['internal_jobs']:
        row = [None] * len(internal)
        for machine, time in edges:
            row[index[machine]] = F(time)
        auxiliary.append(row)
    ports = [(index[p['internal_machine']], F(p['internal_time']))
             for p in sharp['ports']]
    signs = [p['incoming_bit'] for p in sharp['ports']]
    profiles = relation(len(internal), auxiliary, ports, signs, threshold)
    assert len(profiles) == sharp['predicted_strict_profiles']
    certificates = []
    auxiliary_options = [[(machine, F(time)) for machine, time in edges]
                         for edges in sharp['internal_jobs']]
    for bits in sorted(profiles):
        for selected in product(*auxiliary_options):
            allocation = list(selected)
            for bit, sign, port in zip(bits, signs, sharp['ports']):
                if bit == sign:
                    allocation.append((port['internal_machine'], F(port['internal_time'])))
                else:
                    allocation.append((port['external_machine'], F(port['external_time'])))
            loads = {machine: F(0) for machine in internal + external}
            for machine, time in allocation:
                loads[machine] += time
            if all(time <= threshold for time in loads.values()):
                assert len(allocation) == len(auxiliary) + len(ports)
                certificates.append({'profile': list(bits),
                                     'assignment': [machine for machine, _ in allocation],
                                     'all_machine_loads': [str(loads[machine])
                                                           for machine in internal + external]})
                break
        else:
            raise AssertionError(('private-host extension missing', bits))
    return {'path': str(path.relative_to(Path(__file__).resolve().parents[3])),
            'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'complete_schedule_count': len(certificates),
            'complete_schedules': certificates}


def audit():
    rng = random.Random(2026101807)
    counts = {'random_internal_instances': 0, 'two_full_state_random_cases': 0,
              'sharp_signed_counts': 0, 'sharp_zero_refinements': 0,
              'negative_controls': 0, 'boundary_cases': 0,
              'uniform_machine_matching_cases': 0,
              'pcsp_weight_substitutions': 0,
              'pcsp_rho_substitutions': 0}
    grid = [F(0), F(1, 3), F(2, 3), F(1)]
    for _ in range(450):
        m = rng.randrange(1, 4)
        k = rng.randrange(7)
        auxiliary = []
        for j in range(rng.randrange(5)):
            row = [rng.choice(grid) if rng.randrange(5) else None for i in range(m)]
            if all(p is None for p in row):
                row[rng.randrange(m)] = rng.choice(grid)
            auxiliary.append(row)
        ports = [(rng.randrange(m), rng.choice(grid)) for j in range(k)]
        signs = [rng.randrange(2) for j in range(k)]
        threshold = rng.choice([F(0), F(1), F(4, 3)])
        feasible = relation(m, auxiliary, ports, signs, threshold)
        counts['two_full_state_random_cases'] += check_relation(feasible, ports, signs)
        if threshold == 0 and (0,) * k in feasible and (1,) * k in feasible:
            assert len(feasible) == 2 ** k
        counts['random_internal_instances'] += 1
    for k in range(11):
        balanced = 2 ** (k // 2) + 2 ** ((k + 1) // 2) - 1
        assert min(2 ** a + 2 ** (k - a) - 1 for a in range(k + 1)) == balanced
        for a in range(k + 1):
            b = k - a
            ports = ([(0, F(1, a)) for _ in range(a)]
                     + [(1, F(1, b)) for _ in range(b)])
            signs = [0] * a + [1] * b
            feasible = relation(2, [[F(1), F(1)]], ports, signs, F(1))
            assert len(feasible) == 2 ** a + 2 ** b - 1
            assert check_relation(feasible, ports, signs)
            counts['sharp_signed_counts'] += 1
    for k in range(9):
        for zero in range(k + 1):
            for a in range(k - zero + 1):
                b = k - zero - a
                ports = ([(0, F(0))] * zero
                         + [(0, F(1, a)) for _ in range(a)]
                         + [(1, F(1, b)) for _ in range(b)])
                signs = [j % 2 for j in range(zero)] + [0] * a + [1] * b
                feasible = relation(2, [[F(1), F(1)]], ports, signs, F(1))
                assert len(feasible) == 2 ** zero * (2 ** a + 2 ** b - 1)
                assert check_relation(feasible, ports, signs)
                counts['sharp_zero_refinements'] += 1
    # Explicit zero-threshold case: every port is zero and all states survive.
    assert len(relation(2, [[F(0), F(0)]], [(0, F(0))] * 4,
                        [0, 0, 1, 1], F(0))) == 16
    counts['boundary_cases'] += 1
    assert relation(1, [], [], [], F(0)) == {()}
    counts['boundary_cases'] += 1
    # If each port may choose two internal machines, two crossed orientations
    # give exact equality at strict T=1 and weak rho*T=3/2.
    equality = {(0, 0), (1, 1)}
    for cap in (F(1), F(3, 2)):
        feasible = set()
        for x, y in product((0, 1), repeat=2):
            machines = [x, 1 - y]
            if all(machines.count(i) <= cap for i in range(2)):
                feasible.add((x, y))
        assert feasible == equality
        counts['negative_controls'] += 1
    # If there is one internal and one external common machine, counting the
    # external load restores the same equality, while its internal projection
    # retains the third all-outside state.
    projected = relation(1, [], [(0, F(1)), (0, F(1))], [0, 1], F(1))
    assert projected == {(0, 0), (1, 0), (1, 1)}
    counts['negative_controls'] += 1
    for cap in (F(1), F(3, 2)):
        joint = set()
        for x, y in product((0, 1), repeat=2):
            internal_load = int(x == 0) + int(y == 1)
            external_load = 2 - internal_load
            if internal_load <= cap and external_load <= cap:
                joint.add((x, y))
        assert joint == equality
        counts['negative_controls'] += 1
    # Independently compare capacity matching to every actual task assignment.
    for _ in range(250):
        m = rng.randrange(1, 4)
        n = rng.randrange(6)
        machine_times = [rng.choice([F(0), F(1, 3), F(1), F(2)]) for i in range(m)]
        eligible = [tuple(sorted(rng.sample(range(m), rng.randrange(1, min(2, m) + 1))))
                    for j in range(n)]
        threshold = rng.choice([F(0), F(1), F(4, 3)])
        truth = False
        for assignment in product(*eligible):
            loads = [F(0)] * m
            for machine in assignment:
                loads[machine] += machine_times[machine]
            if all(value <= threshold for value in loads):
                truth = True
                break
        got = uniform_machine_matching(machine_times, eligible, threshold)
        assert (got is not None) == truth
        if got is not None:
            loads = [F(0)] * m
            for job, machine in enumerate(got):
                assert machine in eligible[job]
                loads[machine] += machine_times[machine]
            assert all(value <= threshold for value in loads)
        counts['uniform_machine_matching_cases'] += 1
    # Primary-paper theorem conditions, evaluated on weight sets rather than
    # exponentially enumerated Boolean strings.  These finite substitutions
    # check the manuscript's algebra; they do not reprove the PCSP theorem.
    for A in range(2, 41):
        d = 2 * A - 1
        S = set(range(A + 1))
        odd = {w for w in range(d + 1) if w % 2}
        even = set(range(d + 1)) - odd
        needed_majority = (set(range(d + 1)) &
                           set(range(2 * min(S) - d + 1, 2 * max(S))))
        for B in range(A, 2 * A - 1):
            T = set(range(B + 1))
            parity = (S <= odd <= T) or (S <= even <= T)
            majority = needed_majority <= T
            alternating = len(S) == 1 and set(range(1, d)) <= T
            assert not parity and not majority and not alternating
            counts['pcsp_weight_substitutions'] += 1
    for rho in sorted({F(a, b) for b in range(1, 11) for a in range(b, 2 * b)}):
        A = max(2, int(1 / (2 - rho)) + 1)
        B = int(rho * A)
        assert A > 1 / (2 - rho) and A <= B <= 2 * A - 2
        counts['pcsp_rho_substitutions'] += 1
    return {'status': 'pass', 'counts': counts, 'seed': 2026101807,
            'python': platform.python_version(),
            'registered_private_host': registered_private_host_schedules(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope': ('independent finite actual-allocation/internal-capacity audit; '
                      'no normative imports; PCSP checks are theorem substitutions only; '
                      'no general scheduling hardness claim')}


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
