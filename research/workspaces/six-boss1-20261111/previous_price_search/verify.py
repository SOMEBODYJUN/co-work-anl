#!/usr/bin/env python3
"""Independent Fraction-only replay of previous-theme price search artifacts.

No optimizer or discovery module is imported.  Deterministic policy values are
computed by path/cycle sums rather than matrix inverses.  Negative rows include
the entire Boolean domain (via the exact count statistic) and all old columns.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as Q
import gzip
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE.parent
POINT = RUN/'peer_augmented_lp/augmented_lp_exact.json'
MATRIX = RUN/'peer_augmented_lp/exact_matrix.json.gz'
POINT_SHA = 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'
MATRIX_SHA = '6ebf5f2f10843c5cee74391d057fe545449fb45a4e72f18d665e2a00258b6ea9'
NAMES = ['sigma', 'alpha_m', 'alpha_l', 'beta_m', 'beta_l']+[f'mu_A{i}' for i in range(1, 7)]+['mu_mean_T', 'mu_current', 'mu_previous']
STATES = tuple(product((0, 1), repeat=2))
Z = Q(0)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode()


def ratio(n, d):
    assert d or n == 0
    return Q(n, d) if d else Z


def components(bits, comparisons, source, previous, current, final, middle):
    p = sum(bits[j] for j in range(source-1))
    ell = sum(bits[j] for j in range(5))
    s = sum(middle)
    terminal = ratio(final, p+current+s+final)
    denominator = p+current+s+1
    out = [ratio(current, p+current+s+final), Q(s, ell+1), Q(final, ell+1), Q(s), Q(final)]
    out.extend(Q(bit, denominator)-terminal for bit in bits)
    out.extend((sum((Q(bit, 6*denominator) for bit in comparisons), Z)-terminal,
                Q(current, denominator)-terminal, Q(previous, denominator)-terminal))
    return tuple(out)


def direct_cost(bits, comparisons, source, weights, previous, current, final, middle):
    p = sum(bits[:source-1])
    ell = sum(bits[:5])
    s = sum(middle)
    M = sum(weights[5:], Z)
    static = sum((weights[5+i]*bits[i] for i in range(6)), Z)
    static += weights[11]*sum(comparisons)/6
    numerator = weights[0]*current-M*final
    denominator = p+current+s+final
    fraction = numerator/denominator if denominator else Z
    assert denominator or numerator == 0
    return (fraction + (weights[3]+weights[1]/(ell+1))*s +
            (weights[4]+weights[2]/(ell+1))*final +
            (static+weights[12]*current+weights[13]*previous)/(p+current+s+1))


def policy_value(cost, next_states, theta, start):
    path, positions = [], {}
    state = start
    while state not in positions:
        positions[state] = len(path)
        path.append(state)
        state = next_states[state]
    cut = positions[state]
    cycle = path[cut:]
    cycle_value = sum((theta**j*cost[s] for j, s in enumerate(cycle)), Z)/(1-theta**len(cycle))
    return sum((theta**j*cost[s] for j, s in enumerate(path[:cut])), Z)+theta**cut*cycle_value


def bellman(bits, d, source, weights, theta):
    comparisons = (1,)*d+(0,)*(6-d)
    middle_words = tuple(product((0, 1), repeat=5-source))
    edge = {}
    all_costs = {}
    for previous, current, final in product((0, 1), repeat=3):
        costs = []
        for middle in middle_words:
            cost = direct_cost(bits, comparisons, source, weights, previous, current, final, middle)
            feature_value = sum((w*c for w, c in zip(weights, components(bits, comparisons, source, previous, current, final, middle))), Z)
            assert cost == feature_value
            costs.append(cost)
            all_costs[previous, current, final, sum(middle)] = cost
        edge[previous, current, final] = min(costs)
    candidates = []
    for decisions in product((0, 1), repeat=4):
        next_states = [2*current+decisions[s] for s, (previous, current) in enumerate(STATES)]
        cost = [edge[previous, current, decisions[s]] for s, (previous, current) in enumerate(STATES)]
        candidates.append(tuple(policy_value(cost, next_states, theta, s) for s in range(4)))
    assert len(candidates) == 16
    value = tuple(min(candidate[s] for candidate in candidates) for s in range(4))
    assert value in candidates
    slacks = {}
    for previous, current, final in product((0, 1), repeat=3):
        for middle in middle_words:
            s = sum(middle)
            slack = all_costs[previous, current, final, s]+theta*value[2*current+final]-value[2*previous+current]
            assert slack >= 0
            slacks[previous, current, final, s] = slack
    for state, (previous, current) in enumerate(STATES):
        assert value[state] == min(edge[previous, current, final]+theta*value[2*current+final] for final in (0, 1))
    psi = tuple((1-theta)*v for v in value)
    p, k = sum(bits[:source-1]), 7-source
    for current in (0, 1):
        price = psi[2+current]-psi[current]
        assert (1-theta)*weights[13]/(p+current+k-1) <= price <= (1-theta)*weights[13]/(p+current+1)
    return psi, slacks


def read_point():
    assert digest(POINT) == POINT_SHA and digest(MATRIX) == MATRIX_SHA
    data = json.loads(POINT.read_text())
    matrix = json.loads(gzip.decompress(MATRIX.read_bytes()))
    assert data['original_columns'] == matrix['original_columns'] == 4849
    assert len(data['columns']) == len(matrix['columns']) == 15593
    assert len(matrix['rows']) == data['verified_rows'] == 19621
    assert [{key: value for key, value in col.items() if key != 'weight'} for col in data['columns']] == matrix['columns']
    masses = defaultdict(Q)
    hist = []
    for j, col in enumerate(data['columns'][:4849]):
        if col['kind'] != 'hist':
            continue
        bits = tuple(int(character) for character in col['actual_bits'])
        words = [word for word, count in zip(product((0, 1), repeat=3), col['hist']) for _ in range(count)]
        assert len(words) == 6
        d = sum(word[0] for word in words)
        assert d == col['d']
        mass = Q(col['weight'])
        assert mass >= 0
        hist.append((j, bits, d, mass))
        masses[bits, d] += mass
    masses = {key: mass for key, mass in masses.items() if mass}
    utilities = [sum((mass*ratio(bits[i], sum(bits)) for _, bits, _, mass in hist), Z) for i in range(6)]
    K = sum((Q(col['weight']) for col in data['columns'] if col['kind'] == 'K'), Z)
    assert sum(utilities, Z) == Q(data['W'])
    return data, hist, masses, utilities, K


def verify_flow(record, masses, utilities, K):
    source, seed, theta = record['source'], record['seed'], Q(record['theta'])
    certificate = record['occupation_certificate']
    actions = list(product((0, 1), range(6-source)))
    assert certificate['actions_c_s'] == [list(x) for x in actions]
    middle_n = 5-source
    residue = [utilities[source-1], middle_n*utilities[5], utilities[5], middle_n*K, K]+[Z]*9
    seen = {}
    for witness in certificate['occupation_witnesses']:
        bits, d = tuple(map(int, witness['actual_bits'])), witness['d']
        key = bits, d
        mass = Q(witness['mass'])
        assert key in masses and key not in seen and mass == masses[key] > 0
        seen[key] = mass
        probabilities = [list(map(Q, row)) for row in witness['action_probabilities']]
        flows = list(map(Q, witness['discounted_state_flow']))
        initial = [Z]*4
        for membership in (1,)*d+(0,)*(6-d):
            initial[2*membership+bits[seed-1]] += Q(1, 6)
        assert list(map(Q, witness['initial_distribution'])) == initial
        assert len(probabilities) == len(flows) == 4
        assert min(flows) >= 0 and sum(flows, Z) == 1
        incoming = [Z]*4
        comparisons = (1,)*d+(0,)*(6-d)
        for state, (previous, current) in enumerate(STATES):
            row = probabilities[state]
            assert len(row) == len(actions) and min(row) >= 0 and sum(row, Z) == 1
            for probability, (final, middle_count) in zip(row, actions):
                occupation = flows[state]*probability
                incoming[2*current+final] += occupation
                middle = (1,)*middle_count+(0,)*(middle_n-middle_count)
                coefficients = components(bits, comparisons, source, previous, current, final, middle)
                for j, coefficient in enumerate(coefficients):
                    residue[j] -= mass*occupation*coefficient
        for state in range(4):
            assert flows[state]-theta*incoming[state] == (1-theta)*initial[state]
    assert seen == masses
    assert certificate['all_parameter_residuals'] == {name: str(value) for name, value in zip(NAMES, residue)}
    lower = min(residue)
    active_lower = min(value for j, value in enumerate(residue) if not (source == 5 and j in (1, 3)))
    assert lower == Q(certificate['exact_cone_lower_bound'])
    assert active_lower == Q(certificate['active_parameter_lower_bound'])
    assert certificate['nonseparation_certified'] == (lower >= 0)
    assert certificate['all_flow_equations_exact']
    return lower, active_lower, 4*len(seen)


def verify_case(record, data, hist, masses, utilities, K):
    assert record['success']
    assert record['point_sha256'] == POINT_SHA and record['matrix_sha256'] == MATRIX_SHA
    assert record['parameter_names'] == NAMES
    source, seed, theta = record['source'], record['seed'], Q(record['theta'])
    assert 1 <= source <= 5 and 1 <= seed <= 6 and 0 <= theta < 1
    weights = tuple(map(Q, record['parameters_full']))
    assert len(weights) == 14 and min(weights) >= 0 and sum(weights, Z) == 1
    if source == 5:
        assert weights[1] == weights[3] == 0
    cache = {}
    def values(bits, d):
        if (bits, d) not in cache:
            cache[bits, d] = bellman(bits, d, source, weights, theta)
        return cache[bits, d][0]
    def initial_value(bits, d):
        psi = values(bits, d)
        # This is a sum over six genuine Boolean memberships, not a state d/6.
        return sum((psi[2*bit+bits[seed-1]] for bit in (1,)*d+(0,)*(6-d)), Z)/6
    row = [Z]*15593
    row[0] = (5-source)*weights[3]+weights[4]
    for j, bits, d, mass in hist:
        row[j] = weights[0]*ratio(bits[source-1], sum(bits))+((5-source)*weights[1]+weights[2])*ratio(bits[5], sum(bits))-initial_value(bits, d)
    sparse = [[i, str(value)] for i, value in enumerate(row) if value]
    assert sparse == record['coefficients']
    assert sha256(canonical(sparse)).hexdigest() == record['sparse_row_sha256']
    assert all(row[j] == 0 for j in range(4849, 15593))
    assert record['original_column_count'] == 4849 and record['auxiliary_column_count'] == 10744
    assert record['total_column_count'] == 15593 and record['auxiliary_coefficients'] == 'all zero'
    exact_slack = sum((value*Q(col['weight']) for value, col in zip(row, data['columns'])), Z)
    assert exact_slack == Q(record['exact_slack'])
    lower, active_lower, flow_equations = verify_flow(record, masses, utilities, K)
    assert lower <= exact_slack
    full_domain = 'general_types' in record
    assert exact_slack >= 0 or full_domain
    literal_assignments = 0
    if full_domain:
        general = record['general_types']
        assert len(general) == record['general_type_count'] == 448
        assert sha256(canonical(general)).hexdigest() == record['general_types_sha256']
        seen = set()
        for item in general:
            bits, d = tuple(map(int, item['actual_bits'])), item['d']
            assert (bits, d) not in seen
            seen.add((bits, d))
            psi = values(bits, d)
            initial = initial_value(bits, d)
            coefficient = weights[0]*ratio(bits[source-1], sum(bits))+((5-source)*weights[1]+weights[2])*ratio(bits[5], sum(bits))-initial
            assert list(map(Q, item['psi_four_states'])) == list(psi)
            assert Q(item['initial_average']) == initial
            assert Q(item['base']) == psi[bits[seed-1]]
            assert Q(item['previous_price']) == psi[2+bits[seed-1]]-psi[bits[seed-1]]
            assert Q(item['coefficient']) == coefficient
        assert seen == set(product(product((0, 1), repeat=6), range(7)))
        middle_words = tuple(product((0, 1), repeat=5-source))
        for bits in product((0, 1), repeat=6):
            for comparisons in product((0, 1), repeat=6):
                d = sum(comparisons)
                psi, slacks = cache[bits, d]
                literal_average = sum((psi[2*membership+bits[seed-1]] for membership in comparisons), Z)/6
                assert literal_average == initial_value(bits, d)
                for previous, current, final in product((0, 1), repeat=3):
                    for middle in middle_words:
                        # The formula depends on the literal middle word only
                        # through its integer sum; each word is still visited.
                        assert slacks[previous, current, final, sum(middle)] >= 0
                        literal_assignments += 1
        assert literal_assignments == 2**(6+6+3+5-source)
        assert record['full_original_coefficients'] == list(map(str, row[:4849]))
        assert record['full_original_coefficients_sha256'] == sha256(canonical(record['full_original_coefficients'])).hexdigest()
    return {'case_id': record['case_id'], 'exact_slack': str(exact_slack),
            'independent_bellman_types': len(cache), 'stationary_policies_per_type': 16,
            'complete_boolean_domain_checked': full_domain,
            'literal_assignments_checked_via_exact_integer_count': literal_assignments,
            'original_coefficients_checked': 4849, 'auxiliary_zero_coefficients_checked': 10744,
            'occupation_flow_equations_checked': flow_equations,
            'exact_cone_lower_bound': str(lower), 'active_parameter_lower_bound': str(active_lower),
            'nonseparation_certified': lower >= 0, 'negative_row_verified': exact_slack < 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    folder, output = args.input_dir.resolve(), args.output.resolve()
    assert folder.is_relative_to(HERE) and output.is_relative_to(HERE)
    manifest = json.loads((folder/'manifest.json').read_text())
    assert manifest['point_sha256'] == POINT_SHA and manifest['matrix_sha256'] == MATRIX_SHA
    data, hist, masses, utilities, K = read_point()
    audit = {'scope': 'Independent Fraction-only policy-cycle and occupation-flow replay. No optimizer or discovery imports.',
             'point_sha256': POINT_SHA, 'matrix_sha256': MATRIX_SHA,
             'manifest_sha256': digest(folder/'manifest.json'), 'verifier_sha256': digest(__file__), 'cases': []}
    started = time.monotonic()
    for item in manifest['result_files']:
        path = folder/item['file']
        assert path.parent == folder and digest(path) == item['sha256']
        record = json.loads(path.read_text())
        result = verify_case(record, data, hist, masses, utilities, K)
        audit['cases'].append(result)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps({'verified': result['case_id'], 'negative': result['negative_row_verified'],
                          'cone_nonseparation': result['nonseparation_certified'],
                          'full_boolean': result['complete_boolean_domain_checked']}), flush=True)
    assert len(audit['cases']) == len(manifest['cases_requested'])
    audit.update(case_count=len(audit['cases']), negative_rows=sum(c['negative_row_verified'] for c in audit['cases']),
                 exact_nonseparation_certificates=sum(c['nonseparation_certified'] for c in audit['cases']),
                 seconds=time.monotonic()-started, all_checks_passed=True)
    output.write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({key: audit[key] for key in ('case_count', 'negative_rows', 'exact_nonseparation_certificates', 'seconds', 'all_checks_passed')}), flush=True)


if __name__ == '__main__':
    main()
