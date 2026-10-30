#!/usr/bin/env python3
"""单位读出双树：源字面量 LP 的精确见证到实际 5/3 调度。

Input JSON: {"instance": <core explicit leaf schema>,
             "literal_weights": [[y_v0, y_v1], ...]}.
Weights are exact rational strings/integers (Fraction objects are accepted by
the Python API).  This program verifies a GIVEN source-LP witness; it does not
implement or claim an exact polynomial-time LP solver.  It reuses the reviewed
original-P builder, exact load checker and generic matching from
unit_readout_calibrated_cardinality.py, without modifying those frozen bytes.

For k>=2, each variable's maximum-weight rail is selected.  Its active leaf
arity is at most twice the source fractional clause mass.  Inactive jobs stay
at parents; active jobs alone receive incoming-first cardinality slots.  For
k=1, source feasibility supplies the capacitated variable-to-clause matching,
whose selected unary chains are sent all the way down.  No OPT oracle is used.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import sys

import unit_readout_calibrated_cardinality as core

if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)

SOURCE_CLAIMS = ('UM-UNIT-READOUT-STRICT-UNIT-GAP-v1',)


def validate_literal_weights(I, literal_weights):
    """Verify every source row, using complete original rail occurrences."""
    if type(literal_weights) not in (list, tuple) or len(literal_weights) != len(I['roots']):
        raise ValueError('one exact two-weight row per variable required')
    weights = []
    occurrences = []
    clause_mass = [F(0) for _ in I['A']]
    for v, pair in enumerate(literal_weights):
        if type(pair) not in (list, tuple) or len(pair) != 2:
            raise ValueError('two exact literal weights per variable required')
        try:
            row = [core.rational(z) for z in pair]
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError('finite exact rational literal weights required') from exc
        if any(z < 0 or z > 1 for z in row) or sum(row, F(0)) != 1:
            raise ValueError('literal weights must be nonnegative and sum exactly to one')
        weights.append(row)
        counts = [Counter(tree['wiring'].values()) for tree in I['trees'][v]]
        occurrences.append([dict(sorted(c.items())) for c in counts])
        for sign in (0, 1):
            for c, count in counts[sign].items():
                clause_mass[c] += count * row[sign]
    if any(mass > capacity for mass, capacity in zip(clause_mass, I['A'])):
        raise ValueError('source literal-LP clause capacity violated')
    return weights, occurrences, clause_mass


def construct_literal_gap(data, literal_weights):
    I = core.build_instance(data)
    weights, occurrences, source_mass = validate_literal_weights(I, literal_weights)
    majority = [0 if row[0] >= row[1] else 1 for row in weights]
    metadata = {
        'source_claims': SOURCE_CLAIMS,
        'literal_weights': weights,
        'literal_occurrences': occurrences,
        'source_clause_fractional_mass': source_mass,
        'maximum_weight_signs': majority,
        'uniform_bound': F(5, 3),
        'given_witness_only': True,
    }
    # Do not exponentiate k**h, or even iterate h, for empty binary parameters.
    if not I['roots']:
        return core.finish(I, [], F(0), mode='literal-LP-empty', selected_signs=[],
                           leaf_count=None, **metadata)
    k = I['k']
    N = len(I['trees'][0][0]['wiring'])
    jobs = I['jobs']
    sigma = [None if job['kind'] == 'selector' else job['parent'] for job in jobs]
    if k == 1:
        assignment, cut = core.variable_clause_matching(I)
        if assignment is None:
            raise RuntimeError('verified source LP contradicts capacitated Hall cut: ' + repr(cut))
        next_unit = [0 for _ in I['A']]
        signs = []
        selected_paths = []
        for v, c in enumerate(assignment):
            sign = next(sign for sign in (0, 1)
                        if next(iter(I['trees'][v][sign]['wiring'].values())) == c)
            signs.append(sign)
            sigma[v] = I['roots'][v][sign]
            # The explicit unary leaf supplies the complete path, without k**h.
            path = next(iter(I['trees'][v][sign]['wiring']))
            for depth in range(1, I['h'] + 1):
                j = I['path_jobs'][v, sign, path[:depth]]
                job = jobs[j]
                if job['kind'] == 'edge':
                    sigma[j] = job['child']
                else:
                    if next_unit[c] >= I['ranges'][c]['listed_units']:
                        raise RuntimeError('clipped unary clause unit range insufficient')
                    sigma[j] = I['ranges'][c]['start'] + next_unit[c]
                    next_unit[c] += 1
            selected_paths.append({'variable': v, 'sign': sign, 'clause': c,
                                   'path': list(path)})
        return core.finish(I, sigma, F(1), mode='literal-LP-unary-matching',
                           selected_signs=signs, leaf_count=N, r=1,
                           variable_clause_matching=assignment,
                           selected_paths=selected_paths, **metadata)

    r = k // 2
    x = [F(1)]
    for _ in range(I['h']):
        x.append((r - 1 + x[-1]) / k)
    if any(value > F(1, 2) for value in x[1:]):
        raise RuntimeError('active calibration exceeds one half')
    active_arity = [0 for _ in I['A']]
    for v, sign in enumerate(majority):
        for c, count in occurrences[v][sign].items():
            active_arity[c] += count
    if any(F(d) > 2 * mass or F(d) > 2 * a
           for d, mass, a in zip(active_arity, source_mass, I['A'])):
        raise RuntimeError('maximum-weight rounding failed active density bound')

    moving = [j for j, job in enumerate(jobs)
              if job['kind'] == 'selector' or job['sign'] == majority[job['variable']]]
    local_index = {j: i for i, j in enumerate(moving)}
    rows = {}
    column = Counter()

    def put(j, u, mass):
        if mass:
            row = rows.setdefault(u, {})
            row[j] = row.get(j, F(0)) + mass
            column[j] += mass

    for j in moving:
        job = jobs[j]
        if job['kind'] == 'selector':
            put(j, I['roots'][job['variable']][majority[job['variable']]], F(1))
        else:
            t = x[len(job['path'])]
            put(j, job['parent'], 1 - t)
            if job['kind'] == 'edge':
                put(j, job['child'], t)
    clause_mass = []
    for c, ports in enumerate(I['clause_ports']):
        total = active_arity[c] * x[-1]
        clause_mass.append(total)
        if total > I['A'][c]:
            raise RuntimeError('active leaf fractional mass exceeds original capacity')
        unit = 0
        filled = F(0)
        for j in ports:
            if j not in local_index:
                continue
            mass = x[-1]
            while mass:
                if unit >= I['ranges'][c]['listed_units']:
                    raise RuntimeError('clipped clause unit range insufficient')
                take = min(mass, 1 - filled)
                put(j, I['ranges'][c]['start'] + unit, take)
                mass -= take
                filled += take
                if filled == 1:
                    unit += 1
                    filled = F(0)
    if any(column[j] != 1 for j in moving):
        raise RuntimeError('active fractional job column not exactly one')

    slots = []
    adj = [[] for _ in moving]
    B = k - r + 1

    def add_row(u, ordered):
        local = []
        position = F(0)
        for j in ordered:
            mass = rows.get(u, {}).get(j, F(0))
            while mass:
                index = position.numerator // position.denominator
                if index == len(local):
                    s = len(slots)
                    local.append(s)
                    slots.append({'slot': s, 'machine': u, 'fractions': []})
                s = local[index]
                take = min(mass, F(index + 1) - position)
                slots[s]['fractions'].append([j, take])
                if s not in adj[local_index[j]]:
                    adj[local_index[j]].append(s)
                position += take
                mass -= take
        return local, position

    row_cardinality = []
    for u in range(I['internal_count']):
        first = jobs[I['outgoing'][u][0]]
        if first['sign'] != majority[first['variable']]:
            continue
        local, mass = add_row(u, [I['incoming'][u]] + I['outgoing'][u])
        if mass != B or len(local) != B:
            raise RuntimeError('active integer row-cardinality equality failed')
        incoming = I['incoming'][u]
        if any(incoming == j for s in local[1:] for j, _ in slots[s]['fractions']):
            raise RuntimeError('incoming unit job escaped first slot')
        row_cardinality.append({'machine': u, 'mass': mass, 'slots': len(local)})
    for u, row in sorted(rows.items()):
        if u >= I['internal_count']:
            local, mass = add_row(u, sorted(row))
            if mass > 1 or len(local) > 1:
                raise RuntimeError('external unit fractional overload')
    slot_columns = Counter()
    for slot in slots:
        if not 0 < sum((mass for _, mass in slot['fractions']), F(0)) <= 1:
            raise RuntimeError('invalid slot mass')
        for j, mass in slot['fractions']:
            slot_columns[j] += mass
    if any(slot_columns[j] != 1 for j in moving):
        raise RuntimeError('slot job column not exactly one')
    matched = core.covering_matching(adj, len(slots))
    for j, s in zip(moving, matched):
        sigma[j] = slots[s]['machine']
    for v, sign in enumerate(majority):
        if sigma[v] != I['roots'][v][sign]:
            raise RuntimeError('matching changed maximum-weight selector')
    for j, job in enumerate(jobs):
        if j not in local_index and sigma[j] != job['parent']:
            raise RuntimeError('inactive job moved from its original parent')
    bound = F(2) - F(r, k)
    if bound > F(5, 3) or (k % 2 == 0 and bound > F(3, 2)):
        raise RuntimeError('uniform literal-LP gap constant missed')
    return core.finish(I, sigma, bound, mode='literal-LP-active-calibrated',
                       leaf_count=N, r=r, selected_signs=majority,
                       x_by_depth=x, active_leaf_arity=active_arity,
                       clause_fractional_mass=clause_mass,
                       active_internal_row_cardinality=row_cardinality,
                       moving_jobs=moving, moving_job_slots=adj,
                       moving_matching=matched, slots=slots, **metadata)


def audit():
    """Finite exact checks, including a separate physical original-P recount."""
    from itertools import product
    from random import Random
    import hashlib
    import platform
    import time
    started = time.perf_counter()
    rng = Random(1101717)
    counts = Counter()
    histogram = Counter()
    certificates = []

    def check(data, weights, result):
        # Do not use core.actual_loads or its processing_time for this recount.
        loads = Counter()
        assert len(result['jobs']) == len(result['sigma'])
        for job, u in zip(result['jobs'], result['sigma']):
            assert type(u) is int and 0 <= u < result['full_machine_count']
            finite = dict(job['edges'])
            if u in finite:
                value = finite[u]
            elif (job['kind'] == 'port' and job['external']['start'] <= u
                  < job['external']['start'] + job['external']['count']):
                value = F(1)
            else:
                raise AssertionError('assigned unavailable original processing edge')
            loads[u] += value
        C = max(loads.values(), default=F(0))
        assert C == result['makespan'] <= result['bound'] <= F(5, 3)
        assert all(loads[row['machine']] == row['load'] for row in result['listed_loads'])
        assert result['omitted_unit_machine_load'] == 0
        for row in result['clause_ranges']:
            assert row['listed_units'] == min(row['arity'], row['count'])
        assert all(result['sigma'][v] == roots[s]
                   for v, (roots, s) in enumerate(zip(result['roots'], result['selected_signs'])))
        if result['k'] % 2 == 0:
            assert C <= F(3, 2)
        if result['k'] == 1:
            assert C <= 1
        for job in result['jobs']:
            if job['kind'] != 'selector' and job['sign'] != result['selected_signs'][job['variable']]:
                assert result['sigma'][job['job']] == job['parent']
        if 'moving_matching' in result:
            matching = result['moving_matching']
            assert len(matching) == len(set(matching)) == len(result['moving_jobs'])
            assert all(s in row for s, row in zip(matching, result['moving_job_slots']))
        counts['actual_complete_schedules'] += 1
        counts['actual_original_jobs'] += len(result['jobs'])
        counts[result['mode']] += 1
        histogram[str(C)] += 1

    def make(V, k, h, wiring, weights, extra_capacity=None):
        C = max(wiring, default=-1) + 1
        N = len(wiring) // (2 * V) if V else 0
        mass = [F(0) for _ in range(C)]
        for v in range(V):
            for s in (0, 1):
                for c in wiring[(2 * v + s) * N:(2 * v + s + 1) * N]:
                    mass[c] += weights[v][s]
        A = [(m.numerator + m.denominator - 1) // m.denominator for m in mass]
        if extra_capacity:
            for c, extra in extra_capacity.items():
                A[c] += extra
        return core.encode(V, k, h, wiring, A)

    grid = ((1, 1, 1), (1, 1, 4), (2, 1, 2), (1, 2, 1),
            (1, 2, 2), (1, 3, 1), (2, 2, 1))
    choices = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
    for V, k, h in grid:
        # Exhaust every binary-clause wiring in this explicit small grid.
        for wiring in product(range(2), repeat=2 * V * k ** h):
            weight_rows = product(choices if V == 1 else choices[1:4], repeat=V)
            for firsts in weight_rows:
                weights = [[y, 1 - y] for y in firsts]
                data = make(V, k, h, wiring, weights)
                check(data, weights, construct_literal_gap(data, weights))
                counts['exhaustive_wiring_and_weight_cases'] += 1

    for trial in range(160):
        V = rng.randrange(1, 4)
        k = rng.randrange(1, 6)
        h = rng.randrange(1, 4)
        C = rng.randrange(1, 10)
        wiring = [rng.randrange(C) for _ in range(2 * V * k ** h)]
        weights = []
        for _ in range(V):
            denominator = rng.randrange(1, 30)
            first = F(rng.randrange(denominator + 1), denominator)
            weights.append([first, 1 - first])
        data = make(V, k, h, wiring, weights)
        if trial % 23 == 0:
            data['clause_capacities'].append(0)
            data['clause_capacities'].append(10 ** 100 + 151)
        check(data, weights, construct_literal_gap(data, weights))
        counts['random_feasible_source_witnesses'] += 1

    # Biased witnesses can be feasible despite unbounded total d/A: unused
    # rail leaves are not subject to the active-only cardinality constraints.
    for k, h in ((2, 3), (3, 2), (5, 2), (1, 40)):
        N = k ** h
        denominator = 10 * N + 1
        weights = [[F(denominator - 1, denominator), F(1, denominator)]]
        data = core.encode(1, k, h, [0] * N + [1] * N, [N, 1])
        result = construct_literal_gap(data, weights)
        check(data, weights, result)
        if N > 2:
            assert result['clause_ranges'][1]['arity'] > 2 * result['clause_ranges'][1]['count']
            counts['feasible_despite_global_density_failure'] += 1
        certificates.append({'name': 'biased-witness-inactive-density-' + str(k) + '-' + str(h),
                             'instance': data, 'literal_weights': weights, 'result': result})

    # A zero-capacity unused rail, large binary A, and a >4300-digit exact
    # probability are checked without expanding unused machines or capacities.
    denominator = 10 ** 5000 + 151
    huge = 10 ** 100 + 151
    boundary = [
        (core.encode(1, 2, 2, [0] * 4 + [1] * 4, [4, 0]), [[1, 0]]),
        (core.encode(1, 1, 45, [0, 1], [0, huge]), [[0, 1]]),
        (core.encode(1, 2, 1, [0, 0, 1, 1], [huge, huge]),
         [[str(F(denominator - 1, denominator)), str(F(1, denominator))]]),
    ]
    for data, weights in boundary:
        result = construct_literal_gap(data, weights)
        check(data, weights, result)
        counts['exact_binary_and_zero_capacity_boundaries'] += 1
        certificates.append({'name': result['mode'] + '-boundary', 'instance': data,
                             'literal_weights': weights, 'result': result})
    for capacities in ([], [0, huge]):
        data = {'k': huge, 'h': huge, 'variables': [], 'clause_capacities': capacities}
        result = construct_literal_gap(data, [])
        check(data, [], result)
        assert result['leaf_count'] is None and result['makespan'] == 0
        counts['empty_huge_binary_parameters'] += 1

    data = core.encode(1, 2, 1, [0, 0, 1, 1], [1, 1])
    invalid = [('missing-row', data, []), ('short-row', data, [[1]]),
               ('float', data, [[0.5, 0.5]]), ('bool', data, [[True, False]]),
               ('negative', data, [[-1, 2]]), ('over-one', data, [[2, -1]]),
               ('wrong-sum', data, [['1/3', '1/3']]), ('zero-denominator', data, [['1/0', 0]]),
               ('not-a-number', data, [['NaN', 0]]), ('infinity', data, [['Infinity', 0]]),
               ('source-row-overload', data, [[1, 0]]),
               ('zero-capacity-overload', core.encode(1, 1, 1, [0, 0], [0]), [[1, 0]]),
               ('negative-capacity', core.encode(1, 1, 1, [0, 0], [-1]), [[1, 0]]),
               ('float-capacity', core.encode(1, 1, 1, [0, 0], [1.0]), [[1, 0]]),
               ('bool-capacity', core.encode(1, 1, 1, [0, 0], [True]), [[1, 0]])]
    for name, instance, weights in invalid:
        try:
            construct_literal_gap(instance, weights)
        except ValueError:
            counts['invalid_inputs_rejected'] += 1
        else:
            raise AssertionError('invalid exact input accepted: ' + name)
    return {'status': 'passed', 'source_claims': SOURCE_CLAIMS,
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'reused_core_sha256': hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest(),
            'seed': 1101717, 'python': platform.python_version(), 'counts': dict(counts),
            'actual_makespan_histogram': dict(sorted(histogram.items())),
            'full_original_boundary_certificates': certificates,
            'scope': 'Finite exact schedules from given feasible source literal-LP witnesses. '
                     'Every job edge and every actual machine load is recounted separately. '
                     'No exact LP solver, OPT oracle, universal-proof or novelty certification. '
                     'Original-P builder and Hall matcher are reused, not independent.',
            'elapsed_seconds': time.perf_counter() - started}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.input:
        payload = json.loads(Path(args.input).read_text())
        if type(payload) is not dict or set(payload) != {'instance', 'literal_weights'}:
            raise ValueError('exact literal-LP payload keys required')
        result = construct_literal_gap(payload['instance'], payload['literal_weights'])
    else:
        result = audit()
    output = json.dumps(core.jsonable(result), ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with Path(args.output).open('x') as handle:
            handle.write(output)
    else:
        sys.stdout.write(output)
