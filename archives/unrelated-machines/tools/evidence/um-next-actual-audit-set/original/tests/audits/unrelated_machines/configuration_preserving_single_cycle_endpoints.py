#!/usr/bin/env python3
"""Exact finite audits of the all-parameter circuit construction.

No enumeration of all full schedules is claimed. Endpoint lower-bound checks
enumerate selected-label export sets and use independent unit-job matching.
"""

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations
import json
import hashlib
import platform
from pathlib import Path



def rref_null(rows, ncols):
    a = [[Q(v) for v in row] for row in rows]
    pivots = []
    row = 0
    for col in range(ncols):
        pivot = next((r for r in range(row, len(a)) if a[r][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [v / scale for v in a[row]]
        for r in range(len(a)):
            if r != row and a[r][col]:
                scale = a[r][col]
                a[r] = [u - scale * v for u, v in zip(a[r], a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    free = [j for j in range(ncols) if j not in pivots]
    if len(free) != 1:
        return len(pivots), None
    d = [Q(0)] * ncols
    d[free[0]] = 1
    for r, col in enumerate(pivots):
        d[col] = -a[r][free[0]]
    return len(pivots), d


def construct(D):
    assert D >= 3 and D % 2 == 1
    L, N = D + 2, D * (D + 2)
    p = {}
    for c in (0, 1):
        for a in range(L):
            p[('K', c, a), ('U', c)] = Q(1)
    for t in range(N):
        a, j = t % L, t % D
        for c in (0, 1):
            job = ('F', c, a, j)
            p[('K', c, a), job] = Q(1, D)
            p[('G', c, t), job] = Q(1)
        for machine in (('G', 0, t), ('G', 1, t), ('Q', a)):
            p[machine, ('H', t)] = Q(1)
        for machine in (('G', 1, t), ('G', 0, (t + 1) % N), ('Z', t)):
            p[machine, ('E', t)] = Q(1)
    return L, N, p


def base_atom(D, L, N):
    a = {('U', 0): ('K', 0, D), ('U', 1): ('K', 1, D + 1)}
    for t in range(N):
        label, col = t % L, t % D
        block, offset = divmod(t, L)
        for c in (0, 1):
            a['F', c, label, col] = ('G', c, t) if label == D + c else ('K', c, label)
        if offset == block:
            a['H', t] = ('Q', label)
        elif block < offset < D or offset == D + 1:
            a['H', t] = ('G', 0, t)
        else:
            a['H', t] = ('G', 1, t)
        if offset == D:
            a['E', t] = ('Z', t)
        elif block <= offset < D:
            a['E', t] = ('G', 1, t)
        else:
            a['E', t] = ('G', 0, (t + 1) % N)
    return a


def rotate_job(job, q, D, L, N):
    if job[0] == 'U':
        return job
    if job[0] == 'F':
        _, c, a, j = job
        return ('F', c, (a + q) % L, (j + q) % D)
    return (job[0], (job[1] + q) % N)


def rotate_machine(machine, q, D, L, N):
    if machine[0] == 'K':
        _, c, a = machine
        return ('K', c, (a + q) % L)
    if machine[0] == 'G':
        _, c, t = machine
        return ('G', c, (t + q) % N)
    if machine[0] == 'Q':
        return ('Q', (machine[1] + q) % L)
    return ('Z', (machine[1] + q) % N)


def schedule_loads(p, assignment):
    loads = defaultdict(Q)
    for job, machine in assignment.items():
        assert (machine, job) in p
        loads[machine] += p[machine, job]
    return loads


def unit_matching(jobs, allowed):
    owners = {}

    def augment(job, visited):
        for machine in allowed[job]:
            if machine in visited:
                continue
            visited.add(machine)
            if machine not in owners or augment(owners[machine], visited):
                owners[machine] = job
                return True
        return False

    return all(augment(job, set()) for job in jobs)


def check_configurations(p, machines, jobs, cert, expected):
    marginal = {edge: Q(0) for edge in p}
    count = 0
    assert set(cert) == machines
    for machine, configurations in cert.items():
        assert sum((weight for configuration, weight in configurations), Q(0)) == 1
        for configuration, weight in configurations:
            count += 1
            assert weight >= 0 and len(set(configuration)) == len(configuration)
            assert all((machine, job) in p for job in configuration)
            assert sum((p[machine, job] for job in configuration), Q(0)) <= 1
            for job in configuration:
                marginal[machine, job] += weight
    assert marginal == expected
    assert all(sum((weight for (machine, j0), weight in marginal.items() if j0 == job), Q(0)) == 1
               for job in jobs)
    return count


def endpoint_witness(D, L, N, sign):
    bad = 0 if sign == 1 else 1
    easy = 1 - bad
    a = {('U', c): ('K', c, 0) for c in (0, 1)}
    for t in range(N):
        label, col = t % L, t % D
        for c in (0, 1):
            exported = label == 0 and (c == easy or col == 0)
            a['F', c, label, col] = ('G', c, t) if exported else ('K', c, label)
        a['H', t] = ('Q', label) if label == 0 and col == 0 else ('G', bad, t)
        easy_target_t = t if sign == 1 else (t + 1) % N
        a['E', t] = ('Z', t) if easy_target_t % L == 0 else ('G', easy, easy_target_t)
    return a


def audit(D):
    L, N, p = construct(D)
    jobs = {job for machine, job in p}
    machines = {machine for machine, job in p}
    assert len(jobs) == 4 * N + 2
    assert len(machines) == 3 * N + 3 * L
    assert len(p) == 10 * N + 2 * L
    assert len({(t % L, t % D) for t in range(N)}) == N
    for (machine, job), size in p.items():
        rotated = (rotate_machine(machine, 1, D, L, N), rotate_job(job, 1, D, L, N))
        assert p[rotated] == size
    base = base_atom(D, L, N)
    assert set(base) == jobs
    assert max(schedule_loads(p, base).values()) == 1
    hard_A = sum(machine[0:2] == ('G', 0) for job, machine in base.items() if job[0] == 'H')
    hard_B = sum(machine[0:2] == ('G', 1) for job, machine in base.items() if job[0] == 'H')
    assert hard_A == hard_B == D * (D + 1) // 2
    edge_counts = Counter()
    for q in range(N):
        atom = {rotate_job(job, q, D, L, N): rotate_machine(machine, q, D, L, N)
                for job, machine in base.items()}
        assert set(atom) == jobs
        loads = schedule_loads(p, atom)
        assert max(loads.values()) == 1
        assert all(loads[('G', c, t)] == 1 for c in (0, 1) for t in range(N))
        for job, machine in atom.items():
            edge_counts[machine, job] += 1
    x = {edge: Q(edge_counts[edge], N) for edge in p}
    assert all(0 < v < 1 for v in x.values())
    gamma, rho = Q(L - 1, 2 * L), Q(L - 1, L)
    d = {edge: Q(0) for edge in p}
    for t in range(N):
        label, col = t % L, t % D
        for c in (0, 1):
            assert x[('K', c, label), ('U', c)] == Q(1, L)
            assert x[('K', c, label), ('F', c, label, col)] == rho
            assert x[('G', c, t), ('F', c, label, col)] == Q(1, L)
        assert x[('G', 0, t), ('H', t)] == x[('G', 1, t), ('H', t)] == gamma
        assert x[('Q', label), ('H', t)] == Q(1, L)
        assert x[('G', 1, t), ('E', t)] == x[('G', 0, (t + 1) % N), ('E', t)] == gamma
        assert x[('Z', t), ('E', t)] == Q(1, L)
        d[('G', 0, t), ('H', t)] = 1
        d[('G', 1, t), ('H', t)] = -1
        d[('G', 1, t), ('E', t)] = 1
        d[('G', 0, (t + 1) % N), ('E', t)] = -1
    C = [edge for edge in p if d[edge]]
    assert len(C) == 4 * N
    assert min((1 - x[e]) / d[e] if d[e] > 0 else -x[e] / d[e] for e in C) == gamma
    assert min(x[e] / d[e] if d[e] > 0 else (x[e] - 1) / d[e] for e in C) == gamma
    # Independent graph propagation: degree-two connected support; every proper
    # subset loses its kernel propagation. Exact matrix rank also computed D<=5.
    adjacency = defaultdict(list)
    for index, (machine, job) in enumerate(C):
        adjacency['m', machine].append(index)
        adjacency['j', job].append(index)
    assert all(len(es) == 2 for es in adjacency.values())
    reached, queue = set(), [next(iter(adjacency))]
    while queue:
        vertex = queue.pop()
        if vertex in reached:
            continue
        reached.add(vertex)
        for index in adjacency[vertex]:
            machine, job = C[index]
            queue.extend((('m', machine), ('j', job)))
    assert len(reached) == 4 * N
    matrix_rank = None
    if D <= 5:
        rows = [[Q(int(('m', machine) == vertex or ('j', job) == vertex)) for machine, job in C]
                for vertex in adjacency]
        matrix_rank, null = rref_null(rows, len(C))
        assert matrix_rank == 4 * N - 1 and null is not None and all(null)
    sample_thetas = (-gamma, -gamma / 2, Q(0), gamma / 2, gamma)
    explicit_configurations_checked = 0
    for theta in sample_thetas:
        z = {edge: x[edge] + theta * d[edge] for edge in p}
        coverage = defaultdict(Q)
        row_load = defaultdict(Q)
        excess = defaultdict(Q)
        for (machine, job), weight in z.items():
            assert 0 <= weight < 1
            coverage[job] += weight
            row_load[machine] += p[machine, job] * weight
            if weight:
                excess[machine] += p[machine, job] * (1 - weight)
        assert all(coverage[job] == 1 for job in jobs)
        # Full explicit CONFIG certificate: two configurations per rail,
        # singleton/empty distributions on every unit-only row.
        for machine in machines:
            if machine[0] == 'K':
                _, c, label = machine
                assert z[machine, ('U', c)] == Q(1, L)
                port_jobs = [('F', c, label, j) for j in range(D)]
                assert all(z[machine, job] == rho for job in port_jobs)
                assert sum(p[machine, job] for job in port_jobs) == 1
                assert row_load[machine] == 1
            else:
                assert all(size == 1 for (m0, job), size in p.items() if m0 == machine)
                assert sum(weight for (m0, job), weight in z.items() if m0 == machine) <= 1
        cert = {}
        for machine in machines:
            if machine[0] == 'K':
                _, c, label = machine
                cert[machine] = [((('U', c),), Q(1, L)),
                                 (tuple(('F', c, label, j) for j in range(D)), rho)]
            else:
                cert[machine] = [((job,), weight) for (m0, job), weight in z.items() if m0 == machine]
                total = sum((weight for configuration, weight in cert[machine]), Q(0))
                cert[machine].append(((), 1 - total))
        explicit_configurations_checked += check_configurations(p, machines, jobs, cert, z)
        eps = Q(2, D)
        assert all(excess[machine] > 1 - eps for machine in machines)
        if theta in (-gamma, gamma):
            sign = 1 if theta == gamma else -1
            witness = endpoint_witness(D, L, N, sign)
            assert set(witness) == jobs
            assert all(z[machine, job] > 0 for job, machine in witness.items())
            assert max(schedule_loads(p, witness).values()) == 2 - Q(1, D)
    # Independent unit-matching oracle for selected-label exported port sets.
    # This checks the exact contention underpinning the lower bound, not all
    # original complete assignments.
    matching_cases = 0
    hard_jobs = [('H', t) for t in range(N)]
    t_by_pair = {(t % L, t % D): t for t in range(N)}
    subsets = [set(comb) for count in range(D + 1) for comb in combinations(range(D), count)] if D <= 9 else [set(), {0}, {0, 1}, set(range(D))]
    for sign in (-1, 1):
        bad = 0 if sign == 1 else 1
        for cols in subsets:
            forbidden = {('G', bad, t_by_pair[0, col]) for col in cols}
            allowed = {('H', t): [machine for machine in (('G', bad, t), ('Q', t % L)) if machine not in forbidden]
                       for t in range(N)}
            assert unit_matching(hard_jobs, allowed) == (len(cols) <= 1)
            matching_cases += 1
    return {'D': D, 'L': L, 'N': N, 'machines': len(machines), 'jobs': len(jobs),
            'finite_edges': len(p), 'true_optimal_atoms': N,
            'base_hard_A_count': hard_A, 'base_hard_B_count': hard_B,
            'initial_C_edge': str(gamma), 'max_box_steps': [str(gamma), str(gamma)],
            'circuit_support': len(C), 'exact_matrix_rank_if_run': matrix_rank,
            'circuit_connected_degree_two_graph': True,
            'config_sample_thetas': [str(t) for t in sample_thetas],
            'explicit_configurations_checked': explicit_configurations_checked,
            'global_endpoint_upper': str(2 - Q(1, D)),
            'selected_label_hard_matching_checks': matching_cases,
            'selected_label_all_export_subsets_enumerated': D <= 9}


if __name__ == '__main__':
    runs = [audit(D) for D in (3, 5, 7)]
    repo_root = Path(__file__).resolve().parents[3]
    canonical = repo_root / 'research/current/unrelated_machines/configuration_preserving_elimination_support_loss.md'
    result = {
        'status': 'all Fraction checks passed',
        'claim_id': 'UM-CONFIG-PRESERVING-CIRCUIT-TWO-SIGN-SUPPORT-LOSS-v1',
        'scope': 'exact finite audits; no full scheduling enumeration or general proof claim',
        'arithmetic': 'fractions.Fraction; exact finite inputs and certificates',
        'command': 'python3 tests/audits/unrelated_machines/configuration_preserving_single_cycle_endpoints.py',
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'canonical_sha256': hashlib.sha256(canonical.read_bytes()).hexdigest(),
        'runs': runs,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
