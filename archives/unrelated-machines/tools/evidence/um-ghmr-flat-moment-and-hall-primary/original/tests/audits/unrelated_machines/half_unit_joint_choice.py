#!/usr/bin/env python3
"""半窗唯一小端归约：独立大匹配、实际调度及3DM精确枚举。

No repository imports. Integer half-units and Fraction capacities only.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import platform
import random

DELTAS = (F(0), F(1, 3), F(49, 100), F(1, 2))


def build(q, triples):
    if not isinstance(q, int) or q < 0:
        raise ValueError('q must be a nonnegative integer')
    triples = tuple(tuple(t) for t in triples)
    if any(len(t) != 3 or any(not isinstance(e, int) or not 0 <= e < q for e in t)
           for t in triples):
        raise ValueError('each triple must have one valid element per part')
    s = len(triples)
    machines = ([('R', x) for x in range(q)] + [('S', a) for a in range(s)]
                + [('Y', y) for y in range(q)] + [('Z', z) for z in range(q)]
                + [('dummy', 0)])
    jobs = []
    for x in range(q):
        big = tuple(q+a for a, t in enumerate(triples) if t[0] == x)
        for copy in range(3):
            jobs.append((x, big, ('activation', x, copy)))
    for a, (_, y, z) in enumerate(triples):
        jobs.append((q+a, (q+s+y,), ('incidence_y', a)))
        jobs.append((q+a, (q+s+q+z,), ('incidence_z', a)))
    assert len(machines) == s+3*q+1
    assert len(jobs) == 3*q+2*s
    return tuple(machines), tuple(jobs)


def source_oracle(q, triples):
    """Enumerate indexed triple subsets; duplicated values stay distinct."""
    states = 0
    target = set(range(q))
    for chosen in combinations(range(len(triples)), q):
        states += 1
        if all({triples[a][d] for a in chosen} == target for d in range(3)):
            return chosen, states
    return None, states


def big_selection_oracle(m, jobs, delta):
    """Enumerate H, starting from all forced small assignments.

    Selecting a big edge replaces one small unit with two units at its target.
    The occupied bit mask enforces the machine side of the matching. Pruning
    subtracts every still movable small unit, hence remains a true lower bound.
    No 3DM-specific constraint is used.
    """
    capacity = 2*(1+delta)
    initial = [0]*m
    for small, _, _ in jobs:
        initial[small] += 1
    suffix = [[0]*m for _ in range(len(jobs)+1)]
    for index in range(len(jobs)-1, -1, -1):
        suffix[index] = suffix[index+1].copy()
        small, big, _ = jobs[index]
        if big:
            suffix[index][small] += 1
    states = 0

    @lru_cache(None)
    def choose(index, loads, occupied):
        nonlocal states
        states += 1
        if any(loads[i]-suffix[index][i] > capacity for i in range(m)):
            return None
        if index == len(jobs):
            return ()
        small, big, _ = jobs[index]
        tail = choose(index+1, loads, occupied)
        if tail is not None:
            return (None,) + tail
        for machine in big:
            if occupied >> machine & 1:
                continue
            after = list(loads)
            after[small] -= 1
            after[machine] += 2
            tail = choose(index+1, tuple(after), occupied | (1 << machine))
            if tail is not None:
                return (machine,) + tail
        return None

    witness = choose(0, tuple(initial), 0)
    return witness, states


def scheduling_oracle(m, jobs, delta):
    """Full assignment search from processing vectors, with no matching rule."""
    capacity = 2*(1+delta)
    choices = tuple(((small, 1),) + tuple((i, 2) for i in big)
                    for small, big, _ in jobs)
    states = 0

    @lru_cache(None)
    def assign(index, loads):
        nonlocal states
        states += 1
        if index == len(choices):
            return ()
        for machine, length in choices[index]:
            if loads[machine]+length > capacity:
                continue
            after = list(loads)
            after[machine] += length
            tail = assign(index+1, tuple(after))
            if tail is not None:
                return (machine,) + tail
        return None

    witness = assign(0, (0,)*m)
    return witness, states


def verify_big_witness(m, jobs, delta, witness):
    loads = [0]*m
    used = set()
    assert len(witness) == len(jobs)
    for (small, big, _), selected in zip(jobs, witness):
        if selected is None:
            loads[small] += 1
        else:
            assert selected in big and selected not in used
            used.add(selected)
            loads[selected] += 2
    assert max(loads, default=0) <= 2*(1+delta)


def verify_schedule(m, jobs, delta, witness):
    loads = [0]*m
    assert len(witness) == len(jobs)
    for (small, big, _), machine in zip(jobs, witness):
        assert machine == small or machine in big
        loads[machine] += 1 if machine == small else 2
    assert max(loads, default=0) <= 2*(1+delta)


def all_small_boundary(m, jobs):
    loads = [0]*m
    for small, _, _ in jobs:
        loads[small] += 1
    assert max(loads, default=0) <= 3
    return loads


def cases():
    for q in range(3):
        universe = list(product(range(q), repeat=3))
        for mask in range(1 << len(universe)):
            yield f'exhaustive_q{q}_mask{mask}', q, [t for a, t in enumerate(universe) if mask >> a & 1], 'exhaustive_all_families'
    restricted = [(0,0,0), (1,1,1), (2,2,2), (0,1,2), (1,2,0), (2,0,1)]
    for mask in range(1 << len(restricted)):
        yield f'q3_restricted_mask{mask}', 3, [t for a, t in enumerate(restricted) if mask >> a & 1], 'exhaustive_restricted_families'
    explicit = [
        ('duplicate_yes', 1, [(0,0,0), (0,0,0)]),
        ('duplicate_no_isolated', 2, [(0,0,0)]*3),
        ('duplicate_q2_yes', 2, [(0,0,0), (1,1,1), (1,1,1)]),
        ('q3_no_triples', 3, []),
        ('q3_isolated_x', 3, [(0,0,0), (1,1,1), (1,2,2)]),
        ('q3_isolated_y', 3, [(0,0,0), (1,1,1), (2,1,2)]),
        ('q3_isolated_z', 3, [(0,0,0), (1,1,1), (2,2,1)]),
        ('q3_all_available_triples', 3, list(product(range(3), repeat=3))),
        ('q3_cover_all_vertices_but_no_perfect', 3, [(0,0,0), (1,1,1), (2,2,1), (2,1,2)]),
    ]
    for name, q, triples in explicit:
        yield name, q, triples, 'explicit_boundary'
    rng = random.Random(20261016)
    universe = list(product(range(3), repeat=3))
    for r in range(30):
        yield f'q3_seeded_{r}', 3, rng.sample(universe, rng.randrange(1, 10)), 'seeded_sample'


def run():
    rows = []
    totals = Counter()
    for name, q, triples, category in cases():
        machines, jobs = build(q, triples)
        source, source_states = source_oracle(q, triples)
        expected = source is not None
        totals['source_states'] += source_states
        totals['instances'] += 1
        totals['yes_3dm'] += expected
        totals[category] += 1
        results = []
        for delta in DELTAS:
            big, big_states = big_selection_oracle(len(machines), jobs, delta)
            schedule, schedule_states = scheduling_oracle(len(machines), jobs, delta)
            target = expected if delta < F(1,2) else True
            assert (big is not None) == target, (name, delta, 'big', target)
            assert (schedule is not None) == target, (name, delta, 'schedule', target)
            if big is not None:
                verify_big_witness(len(machines), jobs, delta, big)
                verify_schedule(len(machines), jobs, delta, schedule)
            totals['big_selection_states'] += big_states
            totals['scheduling_states'] += schedule_states
            totals['delta_queries'] += 1
            results.append({'delta': str(delta), 'A_delta': big is not None,
                            'full_schedule': schedule is not None,
                            'big_selection_states': big_states,
                            'scheduling_states': schedule_states})
        small_loads = all_small_boundary(len(machines), jobs)
        rows.append({'name': name, 'category': category, 'q': q, 'triples': triples,
                     'machines': len(machines), 'jobs': len(jobs), 'perfect_3dm': expected,
                     'perfect_triple_indices': source, 'OPT_le_1': results[0]['full_schedule'],
                     'all_small_makespan': str(F(max(small_loads, default=0),2)),
                     'queries': results})
    # Show that the interface's delta>=0 hypothesis cannot be dropped.
    machines, jobs = build(1, [(0,0,0)])
    negative, _ = scheduling_oracle(len(machines), jobs, F(-1,4))
    assert negative is None
    assert source_oracle(1, [(0,0,0)])[0] is not None
    return {'schema_version': 1, 'audit': 'independent half-window unique-small 3DM',
            'status': 'all exact checks passed',
            'arithmetic': 'integer half-units and fractions.Fraction; no floating point',
            'repository_imports': [], 'python_version': platform.python_version(),
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'seed': 20261016, 'delta_values': list(map(str, DELTAS)),
            'totals': dict(totals),
            'range': {'all_q0_families': 1, 'all_q1_families': 2, 'all_q2_families': 256,
                      'q3_restricted_universe_size': 6, 'all_q3_restricted_families': 64,
                      'q3_seeded_instances': 30, 'explicit_boundary_cases': 9},
            'boundary_findings': {
                'fractional_residual': 'Unique small endpoint and job mass 1 force each unmatched job entirely onto that endpoint.',
                'q_zero': 'Dummy added uniformly, m=s+3q+1; q=0 has no jobs and every oracle says YES.',
                'delta_half': 'All jobs may stay small; source load 3/2, triple load 1, element and dummy load 0.',
                'negative_delta': 'Use delta in [0,1/2); q=1 perfect instance fails at delta=-1/4.',
                'duplicates': 'Triples indexed; duplicates have separate machines and preserve source truth.',
                'available_edges': 'Only stated finite edges are available, times 1/2 and 1. No zero processing time occurs.',
                'T_zero': 'Not asserted by this fixed T=1 reduction.'},
            'scope': 'Finite exhaustive corroboration and boundary checks, not the universal reduction proof or an independent proof of classical 3DM NP-completeness.',
            'instances': rows}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(encoded+'\n')
        print(json.dumps({'status': result['status'], 'totals': result['totals'], 'output': str(args.output)}, ensure_ascii=False, indent=2))
    else:
        print(encoded)
