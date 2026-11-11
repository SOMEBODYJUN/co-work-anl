"""Independent standard-library check of the one full 19-parameter cone.

Does not import solve_one. Bellman values use deterministic path/cycle sums;
costs are reconstructed from three literal middle bits. Occupation flow gives
a lower bound for every globally normalized nonnegative parameter vector.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
THETA = F(1, 2)
STATES = tuple(product((0, 1), repeat=2))
ACTIONS = tuple(product((0, 1), range(4)))
NAMES = ['sigma', 'alpha_m', 'alpha_l', 'beta_m', 'beta_l']+[f'mu_{c}' for c in 'ABCDEUVWXY']+['mu_mean_T', 'mu_Z', 'mu_current', 'mu_previous']
ZERO = F(0)


def frac(n, d):
    assert d or not n
    return F(n, d) if n else ZERO


def literal_features(key, previous, current, last, middle):
    b, bits, d = key
    p = b
    ell = b+sum(bits[i] for i in range(4))
    load = p+current+sum(middle)+last
    den = p+current+sum(middle)+1
    terminal = frac(last, load)
    out = [frac(current, load), sum((frac(t, ell+1) for t in middle), ZERO),
           frac(last, ell+1), F(sum(middle)), F(last)]
    out += [frac(bit, den)-terminal for bit in bits]
    comparison_bits = (1,)*d+(0,)*(5-d)
    out += [sum((frac(t, 5*den) for t in comparison_bits), ZERO)-terminal,
            frac(b, den)-terminal, frac(current, den)-terminal, frac(previous, den)-terminal]
    return out


def direct_cost(key, params, previous, current, last, middle):
    b, bits, d = key
    p = b
    ell = b+sum(bits[:4])
    s = sum(middle)
    M = sum(params[5:], ZERO)
    static = sum((params[5+i]*bits[i] for i in range(10)), ZERO)+params[15]*F(d, 5)+params[16]*b
    numerator = params[0]*current-M*last
    z = p+current+s+last
    assert z or numerator == 0
    return ((numerator/z if z else ZERO)+(params[3]+params[1]/(ell+1))*s+
            (params[4]+params[2]/(ell+1))*last+
            (static+params[17]*current+params[18]*previous)/(p+current+s+1))


def path_cycle_value(cost, successor, start):
    seen, path = {}, []
    state = start
    while state not in seen:
        seen[state] = len(path)
        path.append(state)
        state = successor[state]
    begin = seen[state]
    cycle = path[begin:]
    cyc = sum((THETA**j*cost[s] for j, s in enumerate(cycle)), ZERO)/(1-THETA**len(cycle))
    return sum((THETA**j*cost[s] for j, s in enumerate(path[:begin])), ZERO)+THETA**begin*cyc


def check_bellman(key, params):
    all_costs, edge = {}, {}
    comparisons = 0
    for a, t, c in product((0, 1), repeat=3):
        choices = []
        for middle in product((0, 1), repeat=3):
            cost = direct_cost(key, params, a, t, c, middle)
            ft = literal_features(key, a, t, c, middle)
            assert cost == sum((w*v for w, v in zip(params, ft)), ZERO)
            all_costs[a, t, c, middle] = cost
            choices.append(cost)
            comparisons += 1
        edge[a, t, c] = min(choices)
    candidates = []
    for policy in product((0, 1), repeat=4):
        costs = [edge[a, t, policy[s]] for s, (a, t) in enumerate(STATES)]
        next_state = [2*t+policy[s] for s, (a, t) in enumerate(STATES)]
        candidates.append(tuple(path_cycle_value(costs, next_state, s) for s in range(4)))
    V = tuple(min(row[s] for row in candidates) for s in range(4))
    assert V in candidates
    slacks = [v+THETA*V[2*t+c]-V[2*a+t] for (a, t, c, middle), v in all_costs.items()]
    assert min(slacks) >= 0
    for state, (a, t) in enumerate(STATES):
        assert V[state] == min(edge[a, t, c]+THETA*V[2*t+c] for c in (0, 1))
    psi = tuple((1-THETA)*v for v in V)
    for t in (0, 1):
        difference = psi[2+t]-psi[t]
        assert (1-THETA)*params[-1]/(key[0]+t+4) <= difference <= (1-THETA)*params[-1]/(key[0]+t+1)
    return psi, min(slacks), comparisons


def main():
    inputs = json.loads((HERE/'inputs.json').read_text())
    for name, expected in inputs['source_sha256'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == expected
    point = json.loads((HERE.parent/'free66_lower_certificate.json').read_text())
    result_path = HERE/'single_case_result.json'
    result = json.loads(result_path.read_text())
    assert result['parameter_names'] == NAMES and result['source'] == 1 and result['theta'] == '1/2'
    assert result['remaining'] == 5 and result['initial_pair'] == ['Z', 'Z']
    params = list(map(F, result['parameters']))
    assert len(params) == 19 and min(params) >= 0 and sum(params, ZERO) == 1
    masses = defaultdict(F)
    utilities = [ZERO]*5
    for atom in point['atoms']:
        w = atom['witness']
        key = w['background'], tuple(map(int, w['bits'])), w['d']
        mass = F(atom['mass'])
        assert mass > 0
        masses[key] += mass
        b, bits, d = key
        for i in range(5):
            utilities[i] += mass*frac(bits[i], b+sum(bits[:5]))
    K = F(point['capacity_mass'])
    budget = [utilities[0], 3*utilities[4], utilities[4], 3*K, K]+[ZERO]*14
    assert result['budget_coordinates'] == list(map(str, budget))
    psi_sum = ZERO
    checked = 0
    seen = set()
    for row in result['type_table']:
        key = row['background'], tuple(map(int, row['bits'])), row['d']
        assert key in masses and key not in seen and F(row['mass']) == masses[key]
        seen.add(key)
        psi, minimum, count = check_bellman(key, params)
        checked += count
        assert row['psi'] == list(map(str, psi)) and F(row['min_bellman_slack']) == minimum
        b, bits, d = key
        assert F(row['initial_value']) == psi[3*b]
        coeff = params[0]*frac(bits[0], b+sum(bits[:5]))+(3*params[1]+params[2])*frac(bits[4], b+sum(bits[:5]))-psi[3*b]
        assert F(row['customer_coefficient']) == coeff
        psi_sum += masses[key]*psi[3*b]
    assert seen == set(masses)
    slack = sum((w*v for w, v in zip(params, budget)), ZERO)-psi_sum
    assert F(result['exact_slack']) == slack
    occ = result['occupation_certificate']
    residual = list(budget)
    seen = set()
    flow_equations = 0
    for row in occ['occupation_witnesses']:
        key = row['background'], tuple(map(int, row['bits'])), row['d']
        assert key in masses and key not in seen and F(row['mass']) == masses[key]
        seen.add(key)
        probabilities = [list(map(F, r)) for r in row['action_probabilities']]
        flow = list(map(F, row['discounted_state_flow']))
        initial = [F(s == 3*key[0]) for s in range(4)]
        assert row['initial'] == list(map(str, initial))
        assert min(flow) >= 0 and sum(flow, ZERO) == 1
        incoming = [ZERO]*4
        for state, (a, t) in enumerate(STATES):
            probs = probabilities[state]
            assert len(probs) == 8 and min(probs) >= 0 and sum(probs, ZERO) == 1
            for probability, (c, s) in zip(probs, ACTIONS):
                mass = flow[state]*probability
                incoming[2*t+c] += mass
                middle = (1,)*s+(0,)*(3-s)
                ft = literal_features(key, a, t, c, middle)
                for j in range(19):
                    residual[j] -= masses[key]*mass*ft[j]
        for state in range(4):
            assert flow[state]-THETA*incoming[state] == (1-THETA)*initial[state]
            flow_equations += 1
    assert seen == set(masses)
    assert occ['all_parameter_residuals'] == {n: str(v) for n, v in zip(NAMES, residual)}
    lower = min(residual)
    assert F(occ['exact_cone_lower_bound']) == lower and lower <= slack
    assert lower > F(7, 100)
    report = {'status': 'INDEPENDENT-19-PARAMETER-NONSEPARATION-PASSED',
              'case': result['case'], 'result_sha256': hashlib.sha256(result_path.read_bytes()).hexdigest(),
              'positive_projected_types': len(masses), 'literal_middle_word_bellman_checks': checked,
              'deterministic_next_bit_policies_per_type': 16, 'exact_flow_equations': flow_equations,
              'parameter_count': 19, 'returned_row_slack': str(slack), 'returned_row_slack_float': float(slack),
              'whole_parameter_cone_lower_bound': str(lower), 'lower_bound_float': float(lower),
              'simple_strict_lower_bound': '7/100', 'negative_row_found': False,
              'not_a_global_background_half_result': True, 'not_a_common_SPE_strategy': True}
    (HERE/'independent_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
