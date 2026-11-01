#!/usr/bin/env python3
"""从真实样本函数独立核验一阶压缩矩的贪心碰撞。

默认只写stdout。输入为canonical实际P、T、有限真实调度及正有理权重；
不读取主核验的算子、分解、浮点scores或预测rank。精确Gram--Schmidt
直接在样本函数空间构造正交基，再逐样本乘指示函数并正交投影。
大于20任务时只输出选择与最小归一化严格评分差摘要，避免巨大分数。
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import platform
import tempfile
import sys

F = Fraction


def inner(a, b, weights):
    return sum((w * x * y for w, x, y in zip(weights, a, b)), F())


def orthogonal_span(generators, weights):
    """Return an unnormalized orthogonal basis; no matrix inversion is used."""
    basis = []
    norms = []
    for original in generators:
        residual = list(original)
        for vector, norm in zip(basis, norms):
            coefficient = inner(original, vector, weights) / norm
            residual = [x - coefficient * y for x, y in zip(residual, vector)]
        norm = inner(residual, residual, weights)
        if norm:
            assert norm > 0
            basis.append(residual)
            norms.append(norm)
    for h, vector in enumerate(basis):
        assert all(inner(vector, basis[k], weights) == 0 for k in range(h))
    return basis, norms


def small_interval(value, digits=40):
    """A rigorously enclosing rational interval with bounded output size."""
    scale = 10 ** digits
    low = value.numerator * scale // value.denominator
    previous_limit = sys.get_int_max_str_digits() if hasattr(sys, 'get_int_max_str_digits') else None
    try:
        if previous_limit is not None:
            sys.set_int_max_str_digits(0)
        exact_hash = hashlib.sha256(str(value).encode()).hexdigest()
    finally:
        if previous_limit is not None:
            sys.set_int_max_str_digits(previous_limit)
    return {'exact_fraction_sha256': exact_hash, 'lower': f'{low}/{scale}', 'upper': f'{low+1}/{scale}',
            'numerator_bits': abs(value.numerator).bit_length(),
            'denominator_bits': value.denominator.bit_length(),
            'strictly_positive': value > 0}


def parse_time(value):
    if value is None or (isinstance(value, str) and value.lower() in ('inf', 'infinity', '∞')):
        return None
    result = F(value)
    assert result >= 0
    return result


def audit(path, *, order_override=None):
    raw = path.read_bytes()
    data = json.loads(raw)
    machines = data['machines']
    jobs = data['jobs']
    target = F(data['target'])
    assert isinstance(machines, int) and machines >= 1
    assert isinstance(jobs, int) and jobs >= 0
    assert target >= 0
    processing = [[parse_time(x) for x in row] for row in data['processing_times']]
    assert len(processing) == machines and all(len(row) == jobs for row in processing)
    assert all(any(processing[i][j] is not None for i in range(machines)) for j in range(jobs))
    atoms = [tuple(a['assignment']) for a in data['distribution']]
    weights = [F(a['weight']) for a in data['distribution']]
    assert len(atoms) == len(weights) >= 1
    assert len(set(atoms)) == len(atoms)
    assert all(w > 0 for w in weights)
    assert all(len(atom) == jobs and all(isinstance(i, int) and 0 <= i < machines for i in atom)
               for atom in atoms)
    order = data['job_order'] if order_override is None else list(order_override)
    assert sorted(order) == list(range(jobs))
    total_weight = sum(weights, F())
    weights = [w / total_weight for w in weights]
    atom_makespans = []
    for atom in atoms:
        loads = [F()] * machines
        for j, i in enumerate(atom):
            assert processing[i][j] is not None
            loads[i] += processing[i][j]
        assert max(loads) <= target
        atom_makespans.append(max(loads))
    lower_bound = max((min(processing[i][j] for i in range(machines)
                           if processing[i][j] is not None) for j in range(jobs)), default=F())
    one = [F(1)] * len(atoms)
    literals = {(i, j): [F(atom[j] == i) for atom in atoms]
                for i in range(machines) for j in range(jobs)}
    # Deduplicating equal literal functions does not change their exact linear span.
    generators = list(map(list, dict.fromkeys(tuple(v) for v in [one] + list(literals.values()))))
    basis, norms = orthogonal_span(generators, weights)

    def project(function):
        coefficients = [inner(function, vector, weights) / norm
                        for vector, norm in zip(basis, norms)]
        return [sum((coefficient * vector[h]
                     for coefficient, vector in zip(coefficients, basis)), F())
                for h in range(len(atoms))]

    assert all(project(function) == function for function in generators)
    zero = [F()] * len(atoms)
    assert project(zero) == zero
    state = one
    true_prefix = [True] * len(atoms)
    choices = []
    steps = []
    all_strict = True
    minimum_gap = None
    minimum_gap_job = None
    for job in order:
        state_norm = inner(state, state, weights)
        assert state_norm > 0
        images = [list(zero) for _ in range(machines)]
        active = [i for i in range(machines) if any(literals[i, job])]
        assert active
        # Projection linearity: the final active image is state minus the others.
        for machine in active[:-1]:
            images[machine] = project([x * y for x, y in zip(literals[machine, job], state)])
        last = active[-1]
        images[last] = [value - sum((images[i][h] for i in active[:-1]), F())
                        for h, value in enumerate(state)]
        scores = []
        for machine in range(machines):
            raw_product = [x * y for x, y in zip(literals[machine, job], state)]
            image = images[machine]
            error = [x - y for x, y in zip(raw_product, image)]
            assert all(inner(error, vector, weights) == 0 for vector in basis)
            score = inner(image, image, weights)
            assert score <= inner(raw_product, raw_product, weights)
            scores.append(score)
        assert [sum(values, F()) for values in zip(*images)] == state
        selected = max(range(machines), key=lambda machine: scores[machine])
        competitors = [score for machine, score in enumerate(scores) if machine != selected]
        gap = scores[selected] - max(competitors) if competitors else scores[selected]
        if order_override is None:
            assert gap > 0
        all_strict = all_strict and gap > 0
        assert scores[selected] > 0
        normalized_gap = gap / state_norm
        if minimum_gap is None or normalized_gap < minimum_gap:
            minimum_gap = normalized_gap
            minimum_gap_job = job
        choices.append(selected)
        state = images[selected]
        true_prefix = [live and atom[job] == selected
                       for live, atom in zip(true_prefix, atoms)]
        if jobs <= 20:
            steps.append({'job': job, 'machine': selected,
                          'scores': [str(score) for score in scores],
                          'strict_margin': str(gap),
                          'true_prefix_atoms': sum(true_prefix),
                          'projected_state': [str(value) for value in state]})
    assignment = dict(zip(order, choices))
    loads = [sum((processing[machine][job] for job in range(jobs)
                  if assignment[job] == machine), F()) for machine in range(machines)]
    if order_override is None and 'expected_assignment' in data:
        assert choices == [data['expected_assignment'][job] for job in order]
    if order_override is None and 'expected_loads' in data:
        assert loads == [F(value) for value in data['expected_loads']]
    result = {'arithmetic': 'fractions.Fraction; sample-space orthogonal projection',
              'python_version': platform.python_version(),
              'input_sha256': hashlib.sha256(raw).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'atoms': len(atoms), 'dimension': len(basis),
              'unique_generator_functions': len(generators),
              'm': machines, 'n': jobs, 'T': str(target),
              'all_atom_makespans_equal_T': all(value == target for value in atom_makespans),
              'optimality_certified_by_single_job': lower_bound == target,
              'single_job_lower_bound': str(lower_bound),
              'all_winners_strict': all_strict,
              'choices_in_job_order': choices, 'loads': [str(value) for value in loads],
              'makespan': str(max(loads)),
              'true_prefix_atoms_after_all_jobs': sum(true_prefix),
              'scope': 'Only supplied finite true-distribution witnesses and explicitly enumerated orders.'}
    if minimum_gap is not None:
        result['minimum_normalized_margin'] = small_interval(minimum_gap)
        result['minimum_normalized_margin_job'] = minimum_gap_job
    if jobs <= 20:
        result['steps'] = steps
    return result


def self_checks():
    """Reproducible boundary inputs and finite scalar formula checks, not a proof."""
    common = {'machines': 1, 'jobs': 1, 'target': '0',
              'processing_times': [['0']],
              'distribution': [{'assignment': [0], 'weight': '1'}],
              'job_order': [0], 'expected_assignment': [0], 'expected_loads': ['0']}
    large_denominator = 2 ** 211 + 23
    accepted = [
        ('empty', {'machines': 1, 'jobs': 0, 'target': '0',
                   'processing_times': [[]],
                   'distribution': [{'assignment': [], 'weight': '1'}],
                   'job_order': [], 'expected_assignment': [], 'expected_loads': ['0']}),
        ('zero', common),
        ('unavailable', {'machines': 2, 'jobs': 1, 'target': '1/3',
                         'processing_times': [['inf'], ['1/3']],
                         'distribution': [{'assignment': [1], 'weight': '7/11'}],
                         'job_order': [0], 'expected_assignment': [1],
                         'expected_loads': ['0', '1/3']}),
        ('large-denominator', {'machines': 2, 'jobs': 1,
                               'target': f'1/{large_denominator}',
                               'processing_times': [[f'1/{large_denominator}'],
                                                    ['1000000000000000000000']],
                               'distribution': [{'assignment': [0],
                                                 'weight': '1/99999999999999999989'}],
                               'job_order': [0], 'expected_assignment': [0],
                               'expected_loads': [f'1/{large_denominator}', '0']})]
    rejected = []
    for name, field, value in [
            ('negative-processing', 'processing_times', [['-1']]),
            ('zero-weight', 'distribution', [{'assignment': [0], 'weight': '0'}]),
            ('false-feasibility', 'processing_times', [['1']])]:
        bad = dict(common)
        bad[field] = value
        rejected.append((name, bad))
    boundary_results = []
    with tempfile.TemporaryDirectory(prefix='projection_boundary_', dir=Path.cwd()) as directory:
        root = Path(directory)
        for name, data in accepted:
            path = root / (name + '.json')
            path.write_text(json.dumps(data))
            result = audit(path)
            assert result['optimality_certified_by_single_job']
            boundary_results.append({'case': name, 'accepted': True,
                                     'dimension': result['dimension'],
                                     'makespan': result['makespan']})
        for name, data in rejected:
            path = root / (name + '.json')
            path.write_text(json.dumps(data))
            try:
                audit(path)
            except AssertionError:
                boundary_results.append({'case': name, 'rejected': True})
            else:
                raise AssertionError(name + ' improperly accepted')
    transitions = 0
    conditional_probabilities = 0
    for k in range(2, 65):
        eta = F(1, k * 2 ** (k + 1))
        probabilities = [F(1, 2 ** (k + 1))] + [F(1, 2 ** s) + eta
                                                       for s in range(1, k + 1)]
        assert sum(probabilities, F()) == 1
        assert all(value > 0 for value in probabilities)
        assert probabilities[1] > F(1, 2)
        for t in range(1, k):
            q = [F(1, 2) + eta / (8 * probabilities[t]) if s == t
                 else 1 - eta / (8 * probabilities[t + 1]) if s == t + 1
                 else eta / 16 for s in range(k + 1)]
            assert all(0 < value < 1 for value in q)
            assert q[t] > F(1, 2)
            assert probabilities[t + 1] == probabilities[t] / 2 + eta / 2
            current_mass = probabilities[t] * q[t]
            next_mass = probabilities[t + 1] * q[t + 1]
            other_mass = sum((probabilities[s] * q[s] for s in range(k + 1)
                              if s != t + 1), F())
            assert current_mass == probabilities[t] / 2 + eta / 8
            assert next_mass == probabilities[t] / 2 + 3 * eta / 8
            assert next_mass - other_mass >= 3 * eta / 16
            transitions += 1
            conditional_probabilities += len(q)
    helper_counts = [0, 1, 2, 7, 100, 10 ** 12]
    capacity_pairs = 0
    for k in range(2, 65):
        for helpers in helper_counts:
            nonfixed = k + helpers
            small = F(1, 2 * k * nonfixed)
            heavy = 1 - helpers * small
            assert 0 < small <= 1 and 0 < heavy <= 1
            assert heavy + helpers * small == 1
            assert nonfixed * small == F(1, 2 * k) < 1
            output = k * heavy + helpers * small
            assert output == k - (k - 1) * helpers * small
            assert output > k - F(1, 2)
            capacity_pairs += 1
    return {'boundary_inputs': boundary_results,
            'event_probability_scalars': {'k_min': 2, 'k_max': 64, 'k_count': 63,
                                           'transitions_checked': transitions,
                                           'conditional_probabilities_checked': conditional_probabilities,
                                           'checks': 'sum p=1; all p,q positive; q<1; both strict majorities; next-minus-others >= 3eta/16'},
            'positive_three_machine_algebra': {'k_min': 2, 'k_max': 64,
                                               'helper_counts': helper_counts,
                                               'parameter_pairs_checked': capacity_pairs,
                                               'checks': 'positive rational times; row-load upper bounds; output identity and >k-1/2',
                                               'scope': 'Only algebra at the displayed parameter pairs; no assertion every helper count is produced by event repetition.'},
            'scope': 'Finite reproducible checks; no replacement for the universal event-chain proof.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, nargs='?')
    parser.add_argument('--all-orders', action='store_true',
                        help='also enumerate all task orders; ties choose smallest machine index')
    parser.add_argument('--self-check', action='store_true',
                        help='run reproducible boundary inputs and finite scalar parameter checks')
    args = parser.parse_args()
    if args.input is None and (not args.self_check or args.all_orders):
        parser.error('an input is required unless --self-check is used alone')
    result = audit(args.input) if args.input is not None else {
        'arithmetic': 'fractions.Fraction',
        'python_version': platform.python_version(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if args.all_orders:
        assert result['n'] <= 8, 'all-orders is only intended for the small finite witness'
        records = []
        makespans = {}
        for order in itertools.permutations(range(result['n'])):
            check = audit(args.input, order_override=order)
            value = check['makespan']
            makespans[value] = makespans.get(value, 0) + 1
            records.append({'order': list(order), 'makespan': value,
                            'choices_in_order': check['choices_in_job_order'],
                            'all_winners_strict': check['all_winners_strict']})
        result['all_orders'] = {'tie_rule': 'smallest machine index',
                                'count': len(records),
                                'makespan_counts': makespans,
                                'records': records}
    if args.self_check:
        result['self_checks'] = self_checks()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
