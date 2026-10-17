#!/usr/bin/env python3
"""Small exact audit for the residual macro-occupancy deficiency identity.

Fixed alpha, delta: q is O(max_degree + 1), with a parameter-dependent constant.
This is not a uniform bit-polynomial generator in alpha or delta, and is not
an unrelated-makespan hardness result: the generator returns an OPT=1 schedule.
Run from repository root: python3 tests/audits/unrelated_machines/occupation_induced_edge_deficit.py > NEW_SCRATCH_OUTPUT.json
All arithmetic is Fraction/integer; no random sampling or external dependency.
The independent integer maxflow reads actual tiny eligibility sets and capacities;
it does not enumerate private-job placements or use the graph deficiency formula.
"""
from collections import Counter, deque
from fractions import Fraction
from itertools import product
from math import ceil
import hashlib
import json
from pathlib import Path
import platform

F = Fraction
GRAPHS = {
    'K1': (1, []),
    'K2': (2, [(0, 1)]),
    'P3': (3, [(0, 1), (1, 2)]),
    'K3': (3, [(0, 1), (0, 2), (1, 2)]),
    'K1,4': (5, [(0, v) for v in range(1, 5)]),
}
ALPHAS = (F(1), F(3, 2), F(199, 100))
TINY_BOUND = F(1, 17)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False).encode('utf-8')


def generate(n, edges, alpha, tiny_bound):
    """Return explicit matrix P, an OPT=1 sigma, and exact construction data.

    None means infinity. Rows are machines, columns are labelled tasks. First n
    columns are the unit macros; then private tiny jobs in vertex order; then
    one tiny task per edge, in the supplied edge order. Graph machines precede
    the n outside machines. All finite tiny times are the same positive 1/q.
    """
    alpha, tiny_bound = F(alpha), F(tiny_bound)
    assert n >= 1 and 1 <= alpha < 2 and tiny_bound > 0
    assert all(0 <= u < v < n for u, v in edges)
    assert len(set(edges)) == len(edges)
    max_degree = max(sum(v in e for e in edges) for v in range(n))
    base = 2 * alpha.denominator
    q = base * max(1, ceil(F(1, tiny_bound) / base),
                   ceil(F(max_degree) / (2 - alpha) / base))
    private = q * (alpha - 1)
    assert private.denominator == 1
    private = int(private)
    h = F(1, q)
    assert h <= tiny_bound and max_degree * h <= 2 - alpha
    P = [[F(1)] * n for _ in range(2 * n)]
    sigma = list(range(n, 2 * n))
    for v in range(n):
        for _ in range(private):
            for i in range(2 * n):
                P[i].append(h if i == v else None)
            sigma.append(v)
    for u, v in edges:
        for i in range(2 * n):
            P[i].append(h if i in (u, v) else None)
        sigma.append(u)
    return P, sigma, {'q': q, 'h': h, 'private_per_vertex': private,
                      'max_degree': max_degree}


def verify_schedule(P, sigma):
    """Read the actual matrix, check every labelled task, and sum exact loads."""
    assert P and all(len(row) == len(sigma) for row in P)
    loads = [F(0) for _ in P]
    for j, i in enumerate(sigma):
        assert isinstance(i, int) and 0 <= i < len(P)
        p = P[i][j]
        assert p is not None and p >= 0
        loads[i] += p
    return max(loads, default=F(0))


def complete_sigma(n, edges, private, I, orientation):
    """Complete every macro, private task, and edge task for a fixed occupancy I."""
    # |I| macros go to graph machines; all remaining macros get distinct outside
    # machines. No macro is omitted even if I is empty or smaller than n.
    macro_destinations = sorted(I) + list(range(n, 2 * n - len(I)))
    assert len(macro_destinations) == n
    return (macro_destinations
            + [v for v in range(n) for _ in range(private)]
            + [edge[bit] for edge, bit in zip(edges, orientation)])


def projection_oracle(P, n, edges, private, I, alpha):
    """Enumerate actual edge-job directions; then validate the full sigma in P.

    Private tasks have only their vertex as a finite endpoint, so no other tiny
    placement is possible. Macro identities are interchangeable and all macro
    edges cost one. Outside macro positions are therefore immaterial to loads.
    """
    tested = 0
    for orientation in product((0, 1), repeat=len(edges)):
        tested += 1
        # Every candidate is an actual assignment of every labelled original task;
        # read P and recompute its machine loads without using the independent-set
        # criterion or a compressed capacity formula.
        sigma = complete_sigma(n, edges, private, I, orientation)
        if verify_schedule(P, sigma) <= alpha:
            assert {sigma[j] for j in range(n) if sigma[j] < n} == I
            return True, tested
    return False, tested


def aggregate_actual_tiny_matrix(P, macro_count):
    """Read each actual tiny column once and aggregate its complete eligibility.

    This only parses the explicit input. It never searches private-task placements;
    a whole eligibility group is one source arc with its actual task count.
    """
    groups = Counter()
    finite_times = set()
    for j in range(macro_count, len(P[0])):
        eligibility = tuple(i for i, row in enumerate(P) if row[j] is not None)
        assert eligibility
        finite_times.update(P[i][j] for i in eligibility)
        groups[eligibility] += 1
    if not groups:
        assert not finite_times
        return groups, None
    assert len(finite_times) == 1
    h = finite_times.pop()
    assert h > 0
    return groups, h


def integer_maxflow_throughput(P, macro_count, I, alpha, groups, h):
    """Maximise the number of sent original tiny jobs by grouped integer maxflow.

    The source-to-group capacities are actual input multiplicities. Machine-to-sink
    capacities are floor(c_i/h), where c_i is the actual alpha capacity minus the
    actual unit macro assignment. No independent-set or internal-edge information
    is supplied to this oracle.
    """
    if not groups:
        return 0
    m = len(P)
    macro_destinations = sorted(I) + list(range(macro_count, 2 * macro_count - len(I)))
    assert len(macro_destinations) == macro_count
    residual_capacities = [F(alpha) for _ in P]
    for j, i in enumerate(macro_destinations):
        assert P[i][j] is not None
        residual_capacities[i] -= P[i][j]
    assert all(c >= 0 for c in residual_capacities)
    # Only this generated same-size class is claimed: all c_i/h are integers,
    # so flooring below loses no fractional throughput and integer maxflow equals F.
    assert all((c / h).denominator == 1 for c in residual_capacities)
    machine_units = [int(c // h) for c in residual_capacities]
    grouped = sorted(groups.items())
    source = 0
    machine_start = 1 + len(grouped)
    sink = machine_start + m
    residual = [dict() for _ in range(sink + 1)]

    def add_arc(u, v, capacity):
        assert isinstance(capacity, int) and capacity >= 0
        residual[u][v] = residual[u].get(v, 0) + capacity
        residual[v].setdefault(u, 0)

    for k, (eligibility, count) in enumerate(grouped, start=1):
        add_arc(source, k, count)
        for i in eligibility:
            add_arc(k, machine_start + i, count)
    for i, capacity in enumerate(machine_units):
        add_arc(machine_start + i, sink, capacity)

    value = 0
    while True:
        parent = [-1] * len(residual)
        parent[source] = source
        queue = deque([source])
        while queue and parent[sink] == -1:
            u = queue.popleft()
            for v, capacity in residual[u].items():
                if capacity > 0 and parent[v] == -1:
                    parent[v] = u
                    queue.append(v)
        if parent[sink] == -1:
            break
        path_capacity = None
        v = sink
        while v != source:
            u = parent[v]
            path_capacity = (residual[u][v] if path_capacity is None else
                             min(path_capacity, residual[u][v]))
            v = u
        assert isinstance(path_capacity, int) and path_capacity > 0
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_capacity
            residual[v][u] += path_capacity
            v = u
        value += path_capacity
    # Reverse-check the computed value by its actual residual reachable cut.
    reachable = {source}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v, capacity in residual[u].items():
            if capacity > 0 and v not in reachable:
                reachable.add(v)
                queue.append(v)
    assert sink not in reachable
    cut_capacity = 0
    for k, (eligibility, count) in enumerate(grouped, start=1):
        if source in reachable and k not in reachable:
            cut_capacity += count
        if k in reachable:
            cut_capacity += sum(count for i in eligibility
                                if machine_start + i not in reachable)
    cut_capacity += sum(capacity for i, capacity in enumerate(machine_units)
                        if machine_start + i in reachable)
    assert value == cut_capacity
    return value


def audit_case(name, n, edges, alpha):
    P, opt_sigma, data = generate(n, edges, alpha, TINY_BOUND)
    assert verify_schedule(P, opt_sigma) == 1
    # Any unit macro gives the lower bound OPT >= 1, independently of its machine.
    assert n >= 1 and all(P[i][j] == 1 for i in range(2 * n) for j in range(n))
    serialized_input = {'infinity_encoding': None,
                        'processing_times': [[None if p is None else str(p)
                                              for p in row] for row in P]}
    groups, actual_h = aggregate_actual_tiny_matrix(P, n)
    assert actual_h is None or actual_h == data['h']
    tiny_count = len(P[0]) - n
    assert sum(groups.values()) == tiny_count
    passed_subsets = feasible_subsets = orientation_checks = 0
    maximum_deficiency = 0
    for mask in range(1 << n):
        I = {v for v in range(n) if mask >> v & 1}
        expected = all(not (u in I and v in I) for u, v in edges)
        actual, tested = projection_oracle(P, n, edges,
                                          data['private_per_vertex'], I, alpha)
        assert actual == expected, (name, str(alpha), sorted(I))
        maximum_throughput = integer_maxflow_throughput(P, n, I, alpha,
                                                       groups, actual_h)
        deficiency = tiny_count - maximum_throughput
        internal_edges = sum(u in I and v in I for u, v in edges)
        assert deficiency == internal_edges, (name, str(alpha), sorted(I),
                                               deficiency, internal_edges)
        assert actual == (deficiency == 0)
        maximum_deficiency = max(maximum_deficiency, deficiency)
        passed_subsets += 1
        feasible_subsets += int(actual)
        orientation_checks += tested
    star_note = None
    if name == 'K1,4':
        # In the stable-set projection, adding the centre to the four-leaf set
        # requires removal of all four leaves; general K1,r gives unbounded r.
        leaves = set(range(1, n))
        remaining_with_center = [I for mask in range(1 << (n - 1))
                                 for I in [{v for v in leaves if mask >> (v - 1) & 1}]
                                 if all(not (u in I | {0} and v in I | {0})
                                        for u, v in edges)]
        assert remaining_with_center == [set()]
        star_note = {'leaf_set_size': n - 1,
                     'minimum_leaf_removals_to_add_center': n - 1,
                     'scope': 'finite set-system check; the general K1,r proof gives no fixed p-extendibility'}
    out = {'graph': name, 'vertices': n, 'edges': len(edges),
           'alpha': str(alpha), 'tiny_bound': str(TINY_BOUND),
           'tiny_time': str(data['h']), 'q': data['q'],
           'machines': len(P), 'macros': n, 'jobs': len(opt_sigma),
           'input_sha256': hashlib.sha256(canonical_bytes(serialized_input)).hexdigest(),
           'OPT1_actual_schedule_verified': True,
           'all_occupancy_subsets_checked': passed_subsets,
           'feasible_occupancy_subsets': feasible_subsets,
           'labelled_edge_orientations_checked': orientation_checks,
           'projection_check': 'passed',
           'actual_tiny_eligibility_groups': len(groups),
           'integer_maxflow_subsets_checked': passed_subsets,
           'maximum_observed_deficiency': maximum_deficiency,
           'deficiency_equals_internal_edge_count': 'passed'}
    if star_note is not None:
        out['extendibility_check'] = star_note
    return out


def main():
    cases = [audit_case(name, n, edges, alpha)
             for name, (n, edges) in GRAPHS.items() for alpha in ALPHAS]
    return {'audit': 'stable-set residual macro-occupancy exact deficiency identity',
            'arithmetic': 'Python Fraction and integers',
            'python_version': platform.python_version(),
            'code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'parameters_are_fixed': True,
            'uniform_bit_polynomial_in_alpha_delta_claimed': False,
            'random_sampling': False,
            'scope': 'finite construction and oracle checks; not a makespan hardness result',
            'cases': cases}


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
