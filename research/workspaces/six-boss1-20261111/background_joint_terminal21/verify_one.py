"""Independent standard-library audit of the saved 21-parameter certificate.

No optimizer/discovery imports. Old AB records are expanded as five literal
triples; all three middle bits are enumerated. Bellman values are obtained
from deterministic paths/cycles, and every occupation equation is exact.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[3]
Z = Q(0)
DISCOUNT = Q(1, 2)
PAIRS = ((0, 0), (0, 1), (1, 0), (1, 1))
MOVES = tuple((last, count) for last in (0, 1) for count in range(4))
PARAMETERS = ['sigma', 'alpha_m', 'alpha_l', 'beta_m', 'beta_l']
PARAMETERS += ['mu_'+label for label in 'ABCDEUVWXY']
PARAMETERS += ['mu_mean_T', 'mu_Z', 'mu_current', 'mu_previous',
               'lambda_AB_price', 'mu_AB_terminal_mean']


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frac(numerator, denominator):
    if numerator == 0:
        return Z
    assert denominator > 0
    return Q(numerator, denominator)


def expanded(record):
    w = record['witness']
    assert w['background'] in (0, 1)
    assert len(w['bits']) == 10 and set(w['bits']) <= {'0', '1'}
    assert len(w['menus']) == 3
    for ell, overlap in w['menus']:
        assert 0 <= ell <= 5 and max(0, w['d']+ell-5) <= overlap <= min(w['d'], ell)
    branches = {}
    for label, length in (('AB', 3), ('AE', 3), ('Sbranch', 4)):
        hist = w['histograms'][label]
        assert len(hist) == 2**length and sum(hist) == 5
        words = []
        for number in range(2**length):
            count = hist[number]
            assert isinstance(count, int) and count >= 0
            word = tuple((number >> (length-1-place)) & 1 for place in range(length))
            words.extend([word]*count)
        assert len(words) == 5 and sum(word[0] for word in words) == w['d']
        branches[label] = words
    bits = tuple(int(c) for c in w['bits'])
    return {'mass': Q(record['mass']), 'b': w['background'], 'bits': bits,
            'comparison': tuple(word[0] for word in branches['AB']),
            'AB': branches['AB'], 'd': w['d']}


def old_ab_numbers(atom):
    old_prefix = atom['b']+atom['bits'][0]+atom['bits'][1]
    prices, revenues, last_bits = [], [], []
    for forced, fourth, fifth in atom['AB']:
        old_last_prefix = old_prefix+forced+fourth
        prices.append(frac(1, old_last_prefix+1))
        revenues.append(frac(fifth, old_last_prefix+fifth))
        last_bits.append(fifth)
    return sum(prices, Z), sum(revenues, Z), Q(sum(last_bits), 5)


def literal_coefficients(atom, previous, current, middle, last):
    """Each entry is an unweighted literal legal term, not H's collapsed formula."""
    background, bits = atom['b'], atom['bits']
    final_load = background+current+sum(middle)+last
    new_last_prefix = background+current+sum(middle)
    actual_last_prefix = background+sum(bits[:4])
    new_last_payoff = frac(last, final_load)
    result = [frac(current, final_load),
              sum((frac(member, actual_last_prefix+1) for member in middle), Z),
              frac(last, actual_last_prefix+1), Q(sum(middle)), Q(last)]
    result += [frac(member, new_last_prefix+1)-new_last_payoff for member in bits]
    result.append(sum((frac(member, new_last_prefix+1)-new_last_payoff
                       for member in atom['comparison']), Z)/5)
    for member in (background, current, previous):
        result.append(frac(member, new_last_prefix+1)-new_last_payoff)
    old_prefix = background+bits[0]+bits[1]
    result.append(sum((frac(last, old_prefix+forced+fourth+1)
                       for forced, fourth, fifth in atom['AB']), Z))
    result.append(sum((frac(fifth, new_last_prefix+1)-new_last_payoff
                       for forced, fourth, fifth in atom['AB']), Z)/5)
    assert len(result) == 21
    return result


def collapsed_cost(atom, weights, previous, current, middle, last):
    b, bits = atom['b'], atom['bits']
    count = sum(middle)
    D, L, ybar = old_ab_numbers(atom)
    final = b+current+count+last
    last_denominator = b+current+count+1
    fixed_price_denominator = b+sum(bits[:4])+1
    M = sum(weights[5:19], Z)
    signed_numerator = weights[0]*current-M*last
    assert final or signed_numerator == 0
    source_minus_queries = signed_numerator/final if final else Z
    static = sum((weights[5+i]*bits[i] for i in range(10)), Z)
    static += weights[15]*Q(atom['d'], 5)+weights[16]*b
    return (source_minus_queries+(weights[3]+weights[1]/fixed_price_denominator)*count
            +(weights[4]+weights[2]/fixed_price_denominator)*last
            +(static+weights[17]*current+weights[18]*previous)/last_denominator
            +weights[19]*last*D
            +weights[20]*(ybar/last_denominator-frac(last, final)))


def path_cycle(cost, successor, start):
    visited, path = {}, []
    at = start
    while at not in visited:
        visited[at] = len(path)
        path.append(at)
        at = successor[at]
    split = visited[at]
    cycle = path[split:]
    repeating = sum((DISCOUNT**i*cost[state] for i, state in enumerate(cycle)), Z)
    repeating /= 1-DISCOUNT**len(cycle)
    prefix = sum((DISCOUNT**i*cost[state] for i, state in enumerate(path[:split])), Z)
    return prefix+DISCOUNT**split*repeating


def exact_bellman(atom, weights):
    raw, edge = {}, {}
    cost_checks = 0
    zero_denominator_checks = 0
    for previous, current in PAIRS:
        for last in (0, 1):
            candidates = []
            for middle in product((0, 1), repeat=3):
                vector = literal_coefficients(atom, previous, current, middle, last)
                cost = sum((weight*coefficient for weight, coefficient in zip(weights, vector)), Z)
                assert cost == collapsed_cost(atom, weights, previous, current, middle, last)
                assert collapsed_cost(atom, [Z]*21, previous, current, middle, last) == 0
                raw[previous, current, middle, last] = cost
                candidates.append(cost)
                cost_checks += 1
                zero_denominator_checks += atom['b']+current+sum(middle)+last == 0
            edge[previous, current, last] = min(candidates)
    policies = []
    for next_bits in product((0, 1), repeat=4):
        costs = [edge[previous, current, next_bits[state]] for state, (previous, current) in enumerate(PAIRS)]
        successor = [2*current+next_bits[state] for state, (previous, current) in enumerate(PAIRS)]
        policies.append(tuple(path_cycle(costs, successor, state) for state in range(4)))
    values = tuple(min(v[state] for v in policies) for state in range(4))
    assert values in policies
    slacks = []
    for (previous, current, middle, last), cost in raw.items():
        slacks.append(cost+DISCOUNT*values[2*current+last]-values[2*previous+current])
    assert min(slacks) >= 0
    for state, (previous, current) in enumerate(PAIRS):
        assert values[state] == min(edge[previous, current, last]+DISCOUNT*values[2*current+last] for last in (0, 1))
    return tuple((1-DISCOUNT)*v for v in values), min(slacks), cost_checks, zero_denominator_checks


def main():
    inputs = json.loads((BASE/'inputs.json').read_text())
    for name, digest in inputs['source_sha256'].items():
        assert sha256(REPO/name) == digest, name
    source_path = REPO/'research/workspaces/six-boss1-20261111/background_reweight/free66_lower_certificate.json'
    source = json.loads(source_path.read_text())
    assert inputs['atoms'] == source['atoms'] and inputs['capacity_mass'] == source['capacity_mass']
    assert inputs['parameter_names'] == PARAMETERS
    assert inputs['source'] == 1 and inputs['theta'] == '1/2' and inputs['initial_pair'] == ['Z', 'Z']
    atoms = [expanded(record) for record in inputs['atoms']]
    assert len(atoms) == 65 and all(atom['mass'] > 0 for atom in atoms)
    result_path = BASE/'single_case_result.json'
    result = json.loads(result_path.read_text())
    assert result['input_sha256'] == sha256(BASE/'inputs.json')
    assert result['source_sha256'] == inputs['source_sha256']
    assert result['case'] == inputs['case'] and result['source'] == 1
    assert result['theta'] == '1/2' and result['initial_pair'] == ['Z', 'Z']
    assert result['remaining'] == 5 and result['middle_count'] == 3
    assert result['parameter_names'] == PARAMETERS and not result['atom_aggregation']
    assert result['atoms'] == 65 and result['lp_variables'] == 281 and result['lp_inequalities'] == 2080
    assert result['lp_equalities'] == 1 and result['lp_calls'] == 1
    weights = list(map(Q, result['parameters']))
    assert len(weights) == 21 and min(weights) >= 0 and sum(weights, Z) == 1
    utilities = [Z]*5
    Uab = Z
    for atom in atoms:
        b, bits, mass = atom['b'], atom['bits'], atom['mass']
        for seat in range(5):
            utilities[seat] += mass*frac(bits[seat], b+sum(bits[:5]))
        Uab += mass*old_ab_numbers(atom)[1]
    K = Q(inputs['capacity_mass'])
    external = [utilities[0], 3*utilities[4], utilities[4], 3*K, K]+[Z]*14+[Uab, Z]
    assert result['actual_tail_utilities'] == list(map(str, utilities))
    assert result['U_AB'] == str(Uab) and result['capacity_mass'] == str(K)
    assert result['budget_coordinates'] == list(map(str, external))
    assert Q(result['capacity_coefficient']) == 3*weights[3]+weights[4]
    total_value, coefficient_total = Z, Z
    literal_checks, zero_checks = 0, 0
    assert len(result['atom_table']) == 65
    for index, (atom, row) in enumerate(zip(atoms, result['atom_table'])):
        assert row['atom_id'] == index and Q(row['mass']) == atom['mass']
        D, L, mean = old_ab_numbers(atom)
        assert [row['D_AB'], row['L_AB'], row['ybar_AB']] == list(map(str, (D, L, mean)))
        psi, min_slack, checked, checked_zero = exact_bellman(atom, weights)
        literal_checks += checked
        zero_checks += checked_zero
        assert row['psi'] == list(map(str, psi)) and Q(row['min_bellman_slack']) == min_slack
        b, bits, mass = atom['b'], atom['bits'], atom['mass']
        initial = psi[3*b]
        assert Q(row['initial_value']) == initial
        coefficient = (weights[0]*frac(bits[0], b+sum(bits[:5]))
                       +(3*weights[1]+weights[2])*frac(bits[4], b+sum(bits[:5]))
                       +weights[19]*L-initial)
        assert Q(row['customer_coefficient']) == coefficient
        total_value += mass*initial
        coefficient_total += mass*coefficient
    slack = sum((weight*term for weight, term in zip(weights, external)), Z)-total_value
    assert Q(result['exact_slack']) == slack
    assert coefficient_total+K*(3*weights[3]+weights[4]) == slack
    residual = list(external)
    occ = result['occupation_certificate']
    assert len(occ['witnesses']) == 65
    equations = 0
    nonzero_occupation_entries = 0
    for index, (atom, row) in enumerate(zip(atoms, occ['witnesses'])):
        assert row['atom_id'] == index and Q(row['mass']) == atom['mass']
        initial = [Q(state == 3*atom['b']) for state in range(4)]
        assert row['initial'] == list(map(str, initial))
        flow = list(map(Q, row['discounted_state_flow']))
        assert len(flow) == 4 and min(flow) >= 0 and sum(flow, Z) == 1
        probabilities = [list(map(Q, vector)) for vector in row['action_probabilities']]
        assert len(probabilities) == 4
        incoming = [Z]*4
        for state, (previous, current) in enumerate(PAIRS):
            probs = probabilities[state]
            assert len(probs) == 8 and min(probs) >= 0 and sum(probs, Z) == 1
            for prob, (last, count) in zip(probs, MOVES):
                occupation = flow[state]*prob
                nonzero_occupation_entries += occupation > 0
                incoming[2*current+last] += occupation
                middle = (1,)*count+(0,)*(3-count)
                coefficients = literal_coefficients(atom, previous, current, middle, last)
                for j, coefficient in enumerate(coefficients):
                    residual[j] -= atom['mass']*occupation*coefficient
        for state in range(4):
            assert flow[state]-DISCOUNT*incoming[state] == (1-DISCOUNT)*initial[state]
            equations += 1
    assert occ['parameter_residuals'] == dict(zip(PARAMETERS, map(str, residual)))
    lower = min(residual)
    assert lower == Q(occ['whole_cone_lower_bound'])
    assert lower <= slack and lower > Q(7, 100)
    assert all(v > Q(7, 100) for v in residual)
    previous = json.loads((REPO/'research/workspaces/six-boss1-20261111/background_reweight/repeated_z_price/single_case_result.json').read_text())
    old_lower = Q(previous['occupation_certificate']['exact_cone_lower_bound'])
    assert slack < old_lower
    report = {'status': 'INDEPENDENT-21-PARAMETER-NONSEPARATION-PASSED',
              'case': inputs['case'], 'result_sha256': sha256(result_path),
              'input_sha256': sha256(BASE/'inputs.json'), 'original_atoms_retained': 65,
              'AB_index_triples_reconstructed': 325, 'atom_aggregation': False,
              'literal_middle_word_cost_and_bellman_checks': literal_checks,
              'zero_terminal_load_checks': zero_checks,
              'zero_parameter_vector_checks': literal_checks,
              'deterministic_next_bit_policies_per_atom': 16,
              'exact_flow_equations': equations,
              'nonzero_occupation_entries': nonzero_occupation_entries,
              'parameter_count': 21, 'all_parameter_residuals': dict(zip(PARAMETERS, map(str, residual))),
              'all_parameter_residuals_float': dict(zip(PARAMETERS, map(float, residual))),
              'whole_cone_lower_bound': str(lower), 'lower_bound_float': float(lower),
              'simple_strict_lower_bound': '7/100',
              'returned_row_slack': str(slack), 'returned_row_slack_float': float(slack),
              'old_19_cone_lower_bound': str(old_lower),
              'strict_improvement_over_entire_normalized_old_19_parameter_family': True,
              'old_19_comparison_scope': 'Only the prescribed sum-of-parameters normalization; no geometric cone noncontainment claim.',
              'certified_improvement_gap_at_least': str(old_lower-slack),
              'certified_improvement_gap_float': float(old_lower-slack),
              'negative_row_found': False, 'not_a_common_realizable_SPE_strategy': True,
              'not_a_global_six_player_half_result': True,
              'source_discount_initial_state_scan': False,
              'all_source_sha256_unchanged': True}
    (BASE/'independent_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('all_parameter_residuals',)}, indent=2))


if __name__ == '__main__':
    main()
