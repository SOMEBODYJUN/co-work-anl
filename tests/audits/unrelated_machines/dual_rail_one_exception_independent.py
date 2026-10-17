from fractions import Fraction as F
from collections import deque
from itertools import product
from random import Random
from math import lcm
import json


def construct(N, C, A, rho, ports, exception, arity_slack=1):
    assert type(N) is int and N >= 0 and type(C) is int and C >= 0
    assert type(A) is int and A >= 1 and rho >= 1
    assert arity_slack in (0, 1)
    assert len(exception) == N and all(len(pair) == 2 for pair in exception)
    rail_ports = [[[] for _ in range(2)] for _ in range(N)]
    arity = [0] * C
    for e, (v, rail, clause, w) in enumerate(ports):
        assert 0 <= v < N and rail in (0, 1) and 0 <= clause < C and w >= 0
        rail_ports[v][rail].append(e)
        arity[clause] += 1
    assert all(d <= 2 * A - arity_slack for d in arity)
    for v in range(N):
        for rail in (0, 1):
            ids = rail_ports[v][rail]
            assert sum((ports[e][3] for e in ids), F(0)) <= 1
            if ids and all(rail_ports[v]):
                designated = exception[v][rail]
                assert designated in ids
                assert sum((ports[e][3] for e in ids if e != designated), F(0)) <= rho - 1
            elif not ids:
                assert exception[v][rail] is None
    chosen = [None] * N
    active = []
    for v in range(N):
        empty = [rail for rail in (0, 1) if not rail_ports[v][rail]]
        if empty:
            chosen[v] = empty[0]
        else:
            active.append(v)
    # Binary capacities; no A-fold slot expansion. Each augmenting path
    # carries one due to a source->variable capacity-one edge.
    source = 0
    var_node = {v: 1 + i for i, v in enumerate(active)}
    offset = 1 + len(active)
    sink = offset + C
    graph = [[] for _ in range(sink + 1)]

    def edge(u, v, cap):
        index = len(graph[u])
        graph[u].append([v, cap, len(graph[v])])
        graph[v].append([u, 0, index])
        return index

    vc_edges = {}
    for v in active:
        node = var_node[v]
        edge(source, node, 1)
        candidates = sorted({ports[exception[v][rail]][2] for rail in (0, 1)})
        for clause in candidates:
            vc_edges[v, clause] = edge(node, offset + clause, 1)
    for clause in range(C):
        edge(offset + clause, sink, A)
    augmented = 0
    while True:
        previous = [None] * len(graph)
        previous[source] = (source, 0)
        queue = deque([source])
        while queue and previous[sink] is None:
            u = queue.popleft()
            for j, (v, cap, _) in enumerate(graph[u]):
                if cap and previous[v] is None:
                    previous[v] = (u, j)
                    queue.append(v)
        if previous[sink] is None:
            break
        v = sink
        while v != source:
            u, j = previous[v]
            _, _, back = graph[u][j]
            graph[u][j][1] -= 1
            graph[v][back][1] += 1
            v = u
        augmented += 1
    assert augmented == len(active)
    for v in active:
        selected = [clause for (var, clause), index in vc_edges.items()
                    if var == v and graph[var_node[v]][index][1] == 0]
        assert len(selected) == 1
        chosen[v] = next(rail for rail in (0, 1)
                         if ports[exception[v][rail]][2] == selected[0])
    # Construct the original full matrix and actual integral assignment.
    m = max(1, 2 * N + C)
    n = N + len(ports)
    p = [[None] * n for _ in range(m)]
    sigma = []
    for v in range(N):
        p[2 * v][v] = p[2 * v + 1][v] = F(1)
        sigma.append(2 * v + chosen[v])
    sent = [None] * N
    for v in active:
        sent[v] = exception[v][chosen[v]]
    for e, (v, rail, clause, w) in enumerate(ports):
        j = N + e
        p[2 * v + rail][j] = w
        p[2 * N + clause][j] = F(1, A)
        sigma.append(2 * N + clause if e == sent[v] else 2 * v + rail)
    loads = [F(0)] * m
    for j, i in enumerate(sigma):
        assert p[i][j] is not None
        loads[i] += p[i][j]
    assert max(loads) <= rho
    clause_loads = loads[2 * N:2 * N + C]
    assert all(value <= 1 for value in clause_loads)
    return {'p': p, 'sigma': sigma, 'loads': loads, 'chosen_rails': chosen,
            'sent_exception_ports': sent, 'unit_augmentations': augmented}


def oracle(p):
    denom = 1
    for row in p:
        for value in row:
            if value is not None:
                denom = lcm(denom, value.denominator)
    options = [[(i, int(p[i][j] * denom)) for i in range(len(p)) if p[i][j] is not None]
               for j in range(len(p[0]))]
    best = None
    count = 0
    for assignment in product(*options):
        loads = [0] * len(p)
        for i, w in assignment:
            loads[i] += w
        value = max(loads)
        if best is None or value < best:
            best = value
        count += 1
    return F(best, denom), count


def main():
    rng = Random(202610171745)
    random_cases = augments = full_assignments = exact_cases = 0
    certificates = []
    for case in range(2000):
        N = rng.randrange(8)
        A = [1, 2, 3, 4, 10 ** 100 + 7][case % 5]
        rho = [F(1), F(5, 4), F(3, 2), F(2)][case % 4]
        rail_sizes = [[rng.randrange(4) for _ in range(2)] for _ in range(N)]
        tokens = [(v, rail, j) for v in range(N) for rail in (0, 1)
                  for j in range(rail_sizes[v][rail])]
        bound = 2 * A - (case % 2)
        if tokens:
            C = max(1, (len(tokens) + bound - 1) // bound) + rng.randrange(3)
        else:
            C = rng.randrange(3)
        buckets = [0] * C
        ports = []
        exception = [[None, None] for _ in range(N)]
        for v in range(N):
            for rail in (0, 1):
                count = rail_sizes[v][rail]
                if not count:
                    continue
                raw = [rng.randrange(5) for _ in range(count - 1)]
                allowance = min(F(1), rho - 1)
                remaining = [allowance * F(w, sum(raw) + 1) for w in raw]
                total = sum(remaining, F(0))
                weights = [(1 - total) * F(rng.randrange(5), 4)] + remaining
                exception[v][rail] = len(ports)
                for w in weights:
                    available = [c for c in range(C) if buckets[c] < bound]
                    clause = rng.choice(available)
                    buckets[clause] += 1
                    ports.append((v, rail, clause, w))
        answer = construct(N, C, A, rho, ports, exception, case % 2)
        augments += answer['unit_augmentations']
        random_cases += 1
        if N + len(ports) <= 12:
            best, count = oracle(answer['p'])
            assert best <= max(answer['loads']) <= rho
            full_assignments += count
            exact_cases += 1
    # Exhaustive arbitrary weights and clause identities, including loops.
    for incidence in product(range(2), repeat=4):
        if max(incidence.count(0), incidence.count(1)) > 3:
            continue
        for weights in product((F(0), F(1, 2), F(1)), repeat=4):
            ports = [(e // 2, e % 2, incidence[e], weights[e]) for e in range(4)]
            answer = construct(2, 2, 2, F(1), ports, [[0, 1], [2, 3]])
            best, count = oracle(answer['p'])
            assert best == max(answer['loads']) == 1
            full_assignments += count
            exact_cases += 1
    # Two-clause example; no source satisfiability assertion is needed.
    ports = [(0, 0, 0, F(1)), (0, 1, 1, F(1))]
    unsat = construct(1, 2, 1, F(1), ports, [[0, 1]])
    assert max(unsat['loads']) == 1
    certificates.append({'kind': 'two_clause_one_variable_example', **unsat})
    # Empty-rail variables do not need an exception on their other rail.
    free_ports = [(0, 0, 0, F(1, 3))] * 3
    free = construct(1, 1, 2, F(1), free_ports, [[None, None]])
    assert free['chosen_rails'] == [1] and max(free['loads']) == 1
    certificates.append({'kind': 'empty_rail_without_unneeded_exception', **free})
    # The absence of every machine is normalized by one idle dummy machine.
    empty = construct(0, 0, 1, F(1), [], [])
    assert empty['p'] == [[]] and empty['sigma'] == [] and empty['loads'] == [0]
    certificates.append({'kind': 'empty_gadget_idle_dummy', **empty})
    return {'status': 'passed', 'seed': 202610171745, 'random_cases': random_cases,
            'binary_capacity_unit_augmentations': augments,
            'independent_full_matrix_optimum_cases': exact_cases,
            'full_assignments': full_assignments,
            'arity_tested': '2A-1 and stronger 2A',
            'precision': 'Fraction / exact integer denominator-cleared oracle',
            'certificates': certificates,
            'scope': 'statement-first scratch; no source satisfiability assumption'}


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


if __name__ == '__main__':
    print(json.dumps(main(), default=encode, indent=2))
