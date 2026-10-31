"""Independent exact boundary audit; does not import the canonical audit."""
from fractions import Fraction as F
from collections import defaultdict
import hashlib
import json
from pathlib import Path


def verify(name, p, y, T, K):
    m = len(p)
    jobs = sorted(set().union(*(r.keys() for r in p)))
    for i in range(m):
        assert sum(w for _, w in y[i]) == 1
        for C, w in y[i]:
            assert w >= 0 and len(set(C)) == len(C)
            assert all(j in p[i] for j in C)
            assert sum(p[i][j] for j in C) <= T
    assert all(sum(w for row in y for C, w in row if j in C) == 1 for j in jobs)

    zeros = {j: next(i for i in range(m) if p[i].get(j) == 0)
             for j in jobs if any(p[i].get(j) == 0 for i in range(m))}
    remaining = [j for j in jobs if j not in zeros]
    reduced = []
    for row in y:
        weights = defaultdict(F)
        for C, w in row:
            weights[tuple(j for j in C if j not in zeros)] += w
        reduced.append([(C, w) for C, w in weights.items() if w])
    assert all(len(C) <= K for row in reduced for C, w in row if w > 0)
    x = [{j: sum(w for C, w in reduced[i] if j in C) for j in remaining}
         for i in range(m)]
    assert all(sum(x[i][j] for i in range(m)) == 1 for j in remaining)
    adj = defaultdict(list)
    envelopes = []
    slot_counts = []
    for i in range(m):
        order = sorted((j for j in remaining if x[i][j] > 0),
                       key=lambda j: (-p[i][j], j))
        pos = F(0)
        intervals = {}
        for j in order:
            assert p[i][j] > 0 and p[i][j] <= T
            intervals[j] = (pos, pos + x[i][j])
            pos += x[i][j]
        assert pos <= K
        q = (pos.numerator + pos.denominator - 1) // pos.denominator
        slot_counts.append(q)
        envelope = F(0)
        for s in range(q):
            touching = [j for j in order
                        if max(F(s), intervals[j][0]) < min(F(s + 1), intervals[j][1])]
            assert touching
            envelope += max(p[i][j] for j in touching)
            for j in touching:
                adj[j].append((i, s))
        envelopes.append(envelope)
    ratio = F(1) if K == 1 else 2 - F(1, K ** (K - 1))
    assert all(e <= ratio * T for e in envelopes)
    order = sorted(remaining, key=lambda j: len(adj[j]))
    count = 0
    max_makespan = F(0)
    loads = [F(0)] * m
    used = set()

    def search(t):
        nonlocal count, max_makespan
        if t == len(order):
            assert all(loads[i] <= envelopes[i] for i in range(m))
            value = max(loads, default=F(0))
            assert value <= ratio * T
            count += 1
            max_makespan = max(max_makespan, value)
            return
        j = order[t]
        for slot in adj[j]:
            if slot not in used:
                i, _ = slot
                used.add(slot)
                loads[i] += p[i][j]
                search(t + 1)
                loads[i] -= p[i][j]
                used.remove(slot)
    search(0)
    assert count > 0
    return {'case': name, 'T': str(T), 'K': K,
            'jobs_before': len(jobs), 'zero_jobs_removed': len(zeros),
            'remaining_jobs': len(remaining), 'row_slot_counts': slot_counts,
            'row_envelopes': [str(e) for e in envelopes],
            'all_covering_matchings_checked': count,
            'maximum_matching_makespan': str(max_makespan),
            'exact_coverage_before_and_after': True}


def run():
    cases = []
    cases.append(verify('empty_T0_K1', [{}, {}], [[((), F(1))], [((), F(1))]], F(0), 1))
    cases.append(verify('K1_nontrivial_ties',
                        [{'a': F(1), 'b': F(1)}, {'a': F(1), 'b': F(3, 5)}],
                        [[(('a',), F(1, 2)), (('b',), F(1, 2))],
                         [(('a',), F(1, 2)), (('b',), F(1, 2))]], F(1), 1))
    cases.append(verify('all_zero_T0_deleted_large_original_config',
                        [{'z0': F(0), 'z1': F(0)}, {'z0': F(0), 'z1': F(0)}],
                        [[(('z0', 'z1'), F(1))], [((), F(1))]], F(0), 1))
    cases.append(verify('zero_edge_job_positive_elsewhere_and_duplicate_merge',
                        [{'z': F(0), 'a': F(1)}, {'z': F(1)}],
                        [[(('z', 'a'), F(1, 2)), (('a',), F(1, 2))],
                         [(('z',), F(1, 2)), ((), F(1, 2))]], F(1), 1))
    T = F(2 ** 91 + 17, 2 ** 127 - 1)
    eta = F(1, 2 ** 149 + 37)
    big = 2 ** 173 + 23
    cases.append(verify('K1_large_processing_and_weight_denominators',
                        [{'a': T * (1 - F(1, big)), 'b': T},
                         {'a': T, 'b': T * (1 - F(2, big))}],
                        [[(('a',), eta), (('b',), 1 - eta)],
                         [(('a',), 1 - eta), (('b',), eta)]], T, 1))
    eta = F(1, 2 ** 191 + 51)
    p = [{'B': T, 'a': T / 2, 'b': T / 2},
         {'B': T}, {'a': T}, {'b': T}]
    y = [[(('B',), eta), (('a', 'b'), 1 - eta)],
         [(('B',), 1 - eta), ((), eta)],
         [(('a',), eta), ((), 1 - eta)],
         [(('b',), eta), ((), 1 - eta)]]
    cases.append(verify('K2_tiny_positive_interval_and_exact_integer_boundary', p, y, T, 2))
    assert F(cases[-1]['maximum_matching_makespan']) == F(3, 2) * T
    frozen_path = Path(__file__).resolve().parents[3] / 'evidence/runs/unrelated_machines/bounded_configuration_cardinality_audit.json'
    frozen = json.loads(frozen_path.read_text())
    canonical_cases = []
    for item in frozen['cases']:
        k = item['K']
        sizes = {'B': F(1), 'A': F(1, 2) if k < 4 else F(3, 8),
                 'C': F(1, 3), 'D': F(1, 4)}
        jobs = sorted(item['central_marginals'])
        central_p = {j: sizes[j[0]] for j in jobs}
        p = [central_p] + [{j: F(1)} for j in jobs]
        y = [[(tuple(C['jobs']), F(C['weight'])) for C in item['central_configs']]]
        y += [[((j,), 1 - F(item['central_marginals'][j])),
               ((), F(item['central_marginals'][j]))] for j in jobs]
        result = verify(f'canonical_K{k}_all_matching_reconstruction', p, y, F(1), k)
        assert F(result['maximum_matching_makespan']) == F(item['actual_matching_load'])
        canonical_cases.append(result)
    return {'arithmetic': 'fractions.Fraction, exhaustive covering matchings',
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'cases': cases, 'canonical_cases_independently_reconstructed': canonical_cases}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
