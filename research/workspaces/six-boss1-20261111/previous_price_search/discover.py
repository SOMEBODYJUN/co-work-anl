#!/usr/bin/env python3
"""Direct OPT6 pricing through the previous-theme four-state interface.

The static actual/mean-comparison menu and current seed precede the priced
previous label.  The mean comparison count enters only literal-index averages.
One budget funds the entire discounted orbit.  Numerical discovery is followed
by exact rational policy enumeration and occupation-flow certificates.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import gzip
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

sys.dont_write_bytecode = True
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
POINT = RUN / 'peer_augmented_lp/augmented_lp_exact.json'
MATRIX = RUN / 'peer_augmented_lp/exact_matrix.json.gz'
POINT_SHA = 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'
MATRIX_SHA = '6ebf5f2f10843c5cee74391d057fe545449fb45a4e72f18d665e2a00258b6ea9'
NAMES = ('sigma', 'alpha_m', 'alpha_l', 'beta_m', 'beta_l') + tuple(
    f'mu_A{i}' for i in range(1, 7)) + ('mu_mean_T', 'mu_current', 'mu_previous')
STATES = tuple(product((0, 1), repeat=2))
ZERO = F(0)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).encode()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
    temporary.replace(path)


def share(n, d):
    assert d or not n
    return F(n, d) if n else ZERO


def dot(left, right):
    return sum((a*b for a, b in zip(left, right) if a and b), ZERO)


def solve_exact(matrix, rhs):
    a = [list(map(F, row))+[F(v)] for row, v in zip(matrix, rhs)]
    for j in range(len(a)):
        p = next(i for i in range(j, len(a)) if a[i][j])
        a[j], a[p] = a[p], a[j]
        scale = a[j][j]
        a[j] = [x/scale for x in a[j]]
        for i in range(len(a)):
            if i != j and a[i][j]:
                scale = a[i][j]
                a[i] = [x-scale*y for x, y in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


@lru_cache(None)
def policy_inverses(theta):
    answer = []
    for policy in product((0, 1), repeat=4):
        matrix = [[F(i == j) for j in range(4)] for i in range(4)]
        for i, (a, t) in enumerate(STATES):
            matrix[i][2*t+policy[i]] -= theta
        columns = [solve_exact(matrix, [F(i == j) for i in range(4)]) for j in range(4)]
        inverse = tuple(tuple(columns[j][i] for j in range(4)) for i in range(4))
        answer.append((policy, inverse))
    assert len(answer) == 16
    return tuple(answer)


def read_input():
    assert digest(POINT) == POINT_SHA
    assert digest(MATRIX) == MATRIX_SHA
    data = json.loads(POINT.read_text())
    matrix = json.loads(gzip.decompress(MATRIX.read_bytes()))
    assert data['original_columns'] == matrix['original_columns'] == 4849
    assert len(data['columns']) == len(matrix['columns']) == 15593
    assert len(matrix['rows']) == data['verified_rows'] == 19621
    assert [{k: v for k, v in col.items() if k != 'weight'} for col in data['columns']] == matrix['columns']
    masses = defaultdict(F)
    hist_columns = []
    for j, col in enumerate(data['columns'][:4849]):
        if col['kind'] == 'hist':
            bits = tuple(map(int, col['actual_bits']))
            d = int(col['d'])
            assert len(bits) == 6 and set(bits) <= {0, 1} and 0 <= d <= 6
            words = tuple(product((0, 1), repeat=3))
            assert sum(col['hist']) == 6
            assert sum(n*w[0] for n, w in zip(col['hist'], words)) == d
            mass = F(col['weight'])
            assert mass >= 0
            masses[bits, d] += mass
            hist_columns.append((j, bits, d, mass))
    positive = {key: mass for key, mass in sorted(masses.items()) if mass}
    u = tuple(sum((mass*share(bits[i], sum(bits)) for j, bits, d, mass in hist_columns), ZERO) for i in range(6))
    assert sum(u, ZERO) == F(data['W'])
    assert data['columns'][0]['kind'] == 'K'
    K = F(data['columns'][0]['weight'])
    return data, hist_columns, positive, u, K


def features(bits, d, source, a, t, c, s):
    p, ell = sum(bits[:source-1]), sum(bits[:5])
    z, denominator = p+t+s+c, p+t+s+1
    terminal = share(c, z)
    ans = (share(t, z), F(s, ell+1), F(c, ell+1), F(s), F(c))
    ans += tuple(F(bit, denominator)-terminal for bit in bits)
    ans += (F(d, 6*denominator)-terminal,
            F(t, denominator)-terminal, F(a, denominator)-terminal)
    assert len(ans) == 14
    return ans


def wallet(source, u, K):
    middle = 5-source
    return (u[source-1], middle*u[5], u[5], middle*K, K)+(ZERO,)*9


def exact_bellman(bits, d, source, params, theta):
    k = 7-source
    p, ell = sum(bits[:source-1]), sum(bits[:5])
    fixed_query = dot(params[5:11], tuple(map(F, bits)))+params[11]*F(d, 6)
    query_mass = sum(params[5:], ZERO)
    alpha = params[3]+params[1]/(ell+1)
    beta = params[4]+params[2]/(ell+1)
    def cost(a, t, c, s):
        numerator = params[0]*t-query_mass*c
        z = p+t+s+c
        return (numerator/z if numerator else ZERO)+alpha*s+beta*c+(fixed_query+params[12]*t+params[13]*a)/(p+t+s+1)
    edges = {(a, t, c): min(cost(a, t, c, s) for s in range(k-1))
             for a, t, c in product((0, 1), repeat=3)}
    candidates = []
    for policy, inverse in policy_inverses(theta):
        costs = tuple(edges[a, t, policy[i]] for i, (a, t) in enumerate(STATES))
        candidates.append(tuple(dot(row, costs) for row in inverse))
    values = tuple(min(candidate[i] for candidate in candidates) for i in range(4))
    assert values in candidates
    slacks = [cost(a, t, c, s)+theta*values[2*t+c]-values[2*a+t]
              for a, t, c in product((0, 1), repeat=3) for s in range(k-1)]
    assert min(slacks) >= 0
    for i, (a, t) in enumerate(STATES):
        assert values[i] == min(edges[a, t, c]+theta*values[2*t+c] for c in (0, 1))
    psi = tuple((1-theta)*v for v in values)
    for t in (0, 1):
        w = psi[2+t]-psi[t]
        assert (1-theta)*params[13]/(p+t+k-1) <= w <= (1-theta)*params[13]/(p+t+1)
    return psi, len(slacks), min(slacks)


def occupation_certificate(keys, masses, source, seed, theta, tables, marginals, external):
    k = 7-source
    actions = tuple(product((0, 1), range(k-1)))
    residual = list(external)
    witnesses = []
    offset = 0
    for key, table in zip(keys, tables):
        bits, d = key
        policies = []
        for state in range(4):
            row = [max(float(x), 0.) for x in marginals[offset:offset+len(actions)]]
            offset += len(actions)
            total = sum(row)
            if total > 1e-13:
                rational = [F(x/total).limit_denominator(10**9) if x/total > 1e-12 else ZERO for x in row]
                norm = sum(rational, ZERO)
                assert norm > 0
                rational = [x/norm for x in rational]
            else:
                rational = [F(j == 0) for j in range(len(actions))]
            assert min(rational) >= 0 and sum(rational, ZERO) == 1
            policies.append(rational)
        transition = [[ZERO for _ in range(4)] for _ in range(4)]
        for state, (a, t) in enumerate(STATES):
            for action, (c, s) in enumerate(actions):
                transition[state][2*t+c] += policies[state][action]
        initial = [ZERO]*4
        initial[bits[seed-1]] = 1-F(d, 6)
        initial[2+bits[seed-1]] = F(d, 6)
        system = [[F(i == j)-theta*transition[j][i] for j in range(4)] for i in range(4)]
        flow = solve_exact(system, [(1-theta)*x for x in initial])
        assert min(flow) >= 0 and sum(flow, ZERO) == 1
        for i in range(4):
            assert flow[i]-theta*sum((flow[j]*transition[j][i] for j in range(4)), ZERO) == (1-theta)*initial[i]
        for j in range(14):
            expected = sum((flow[state]*policies[state][action]*table[state][action][j]
                            for state in range(4) for action in range(len(actions))), ZERO)
            residual[j] -= masses[key]*expected
        witnesses.append({'actual_bits': ''.join(map(str, bits)), 'd': d,
                          'mass': str(masses[key]), 'initial_distribution': list(map(str, initial)),
                          'action_probabilities': [list(map(str, row)) for row in policies],
                          'discounted_state_flow': list(map(str, flow))})
    assert offset == len(marginals)
    active = [j for j in range(14) if not (source == 5 and j in (1, 3))]
    bound, active_bound = min(residual), min(residual[j] for j in active)
    return {'scope': 'Exact lower bound for all 14 globally nonnegative normalized weights at this one fixed source, seed, discount and input point.',
            'meaning': 'Local occupation witnesses are LP dual objects, not common realizable game strategies.',
            'actions_c_s': [list(action) for action in actions],
            'all_parameter_residuals': {name: str(x) for name, x in zip(NAMES, residual)},
            'exact_cone_lower_bound': str(bound), 'exact_cone_lower_bound_float': float(bound),
            'active_parameter_lower_bound': str(active_bound), 'active_parameter_lower_bound_float': float(active_bound),
            'nonseparation_certified': bound >= 0, 'all_flow_equations_exact': True,
            'occupation_witnesses': witnesses}


def discover_case(data, hist_columns, masses, u, K, source, seed, theta, emit_general):
    started = time.monotonic()
    keys = list(masses)
    k = 7-source
    actions = tuple(product((0, 1), range(k-1)))
    dim, nvar = 14, 14+4*len(keys)
    rr, cc, vv = [], [], []
    tables = []
    external = wallet(source, u, K)
    objective = list(map(float, external))+[0.]*(4*len(keys))
    nrows = 0
    for q, (bits, d) in enumerate(keys):
        objective[dim+4*q+bits[seed-1]] -= float((1-theta)*masses[bits, d]*(1-F(d, 6)))
        objective[dim+4*q+2+bits[seed-1]] -= float((1-theta)*masses[bits, d]*F(d, 6))
        table = []
        for state, (a, t) in enumerate(STATES):
            local = []
            for c, s in actions:
                cost = features(bits, d, source, a, t, c, s)
                local.append(cost)
                for j, x in enumerate(cost):
                    if x:
                        rr.append(nrows); cc.append(j); vv.append(-float(x))
                rr.extend((nrows, nrows))
                cc.extend((dim+4*q+state, dim+4*q+2*t+c))
                vv.extend((1., -float(theta)))
                nrows += 1
            table.append(local)
        tables.append(table)
    matrix = coo_matrix((vv, (rr, cc)), shape=(nrows, nvar)).tocsr()
    normalization = coo_matrix(([1.]*dim, ([0]*dim, list(range(dim)))), shape=(1, nvar)).tocsr()
    bounds = [(0, None)]*dim+[(None, None)]*(nvar-dim)
    if k == 2:
        bounds[1] = bounds[3] = (0, 0)
    answer = linprog(objective, A_ub=matrix, b_ub=np.zeros(nrows), A_eq=normalization, b_eq=[1.],
                     bounds=bounds, method='highs',
                     options={'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
    record = {'case_id': f'actual{source}_seedA{seed}_theta{theta.numerator}_{theta.denominator}',
              'source': source, 'seed': seed, 'theta': str(theta), 'k': k,
              'point_sha256': POINT_SHA, 'matrix_sha256': MATRIX_SHA,
              'parameter_names': list(NAMES), 'parameter_count': dim,
              'normalization': 'All globally nonnegative parameters sum to one; inert middle parameters are fixed to zero only at k=2.',
              'visible_positive_types': len(keys), 'lp_variables': nvar, 'lp_inequalities': nrows,
              'success': bool(answer.success)}
    if not answer.success:
        record.update(message=answer.message, seconds=time.monotonic()-started)
        return record
    params = [F(float(x)).limit_denominator(10**7) if x > 1e-12 else ZERO for x in answer.x[:dim]]
    norm = sum(params, ZERO)
    assert norm > 0
    params = tuple(x/norm for x in params)
    assert min(params) >= 0 and sum(params, ZERO) == 1
    cache = {}
    def project(bits, d):
        key = bits, d
        if key not in cache:
            cache[key] = exact_bellman(bits, d, source, params, theta)
        psi = cache[key][0]
        t = bits[seed-1]
        return (1-F(d, 6))*psi[t]+F(d, 6)*psi[2+t]
    exact_slack = dot(external, params)-sum((mass*project(*key) for key, mass in masses.items()), ZERO)
    row = [ZERO]*4849
    row[0] = (k-2)*params[3]+params[4]
    for j, bits, d, mass in hist_columns:
        row[j] = params[0]*share(bits[source-1], sum(bits))+((k-2)*params[1]+params[2])*share(bits[5], sum(bits))-project(bits, d)
    assert sum((v*F(col['weight']) for v, col in zip(row, data['columns'][:4849])), ZERO) == exact_slack
    sparse = [[i, str(v)] for i, v in enumerate(row) if v]
    cert = occupation_certificate(keys, masses, source, seed, theta, tables, -answer.ineqlin.marginals, external)
    assert F(cert['exact_cone_lower_bound']) <= exact_slack
    record.update(float_objective=float(answer.fun), exact_slack=str(exact_slack), exact_slack_float=float(exact_slack),
                  parameters_full=list(map(str, params)), parameters={n: str(v) for n, v in zip(NAMES, params) if v},
                  budget_value=str(dot(external, params)), budget_coordinates=list(map(str, external)),
                  coefficients=sparse, sparse_row_sha256=sha256(canonical(sparse)).hexdigest(),
                  original_column_count=4849, total_column_count=15593, auxiliary_column_count=10744,
                  auxiliary_coefficients='all zero', occupation_certificate=cert)
    if exact_slack < 0 or emit_general == 'all':
        general = []
        for bits in product((0, 1), repeat=6):
            for d in range(7):
                initial = project(bits, d)
                psi, checks, minimum = cache[bits, d]
                t = bits[seed-1]
                coefficient = params[0]*share(bits[source-1], sum(bits))+((k-2)*params[1]+params[2])*share(bits[5], sum(bits))-initial
                general.append({'actual_bits': ''.join(map(str, bits)), 'd': d,
                                'psi_four_states': list(map(str, psi)), 'initial_average': str(initial),
                                'base': str(psi[t]), 'previous_price': str(psi[2+t]-psi[t]),
                                'coefficient': str(coefficient)})
        assert len(general) == 448
        record.update(general_type_count=448, general_types=general,
                      general_types_sha256=sha256(canonical(general)).hexdigest(),
                      full_original_coefficients=list(map(str, row)),
                      full_original_coefficients_sha256=sha256(canonical(list(map(str, row)))).hexdigest())
    record.update(exact_bellman_types=len(cache), stationary_next_bit_policies_per_type=16,
                  exact_bellman_inequalities_checked=sum(value[1] for value in cache.values()),
                  minimum_bellman_slack=str(min(value[2] for value in cache.values())),
                  seconds=time.monotonic()-started)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', default='1,2,3,4,5')
    parser.add_argument('--seeds', default='1,2,3,4,5,6')
    parser.add_argument('--thetas', required=True)
    parser.add_argument('--cases', help='Optional exact list source:seed:theta, overriding the Cartesian product.')
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--emit-general', choices=('negative', 'all'), default='negative')
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    output = (HERE/args.output_dir).resolve()
    assert output.is_relative_to(HERE) and output != HERE
    output.mkdir(parents=True, exist_ok=True)
    if args.cases:
        cases = [(int(source), int(seed), F(theta)) for source, seed, theta in (item.split(':') for item in args.cases.split(','))]
    else:
        cases = list(product(map(int, args.sources.split(',')), map(int, args.seeds.split(',')), map(F, args.thetas.split(','))))
    assert len(set(cases)) == len(cases)
    assert all(1 <= source <= 5 and 1 <= seed <= 6 and 0 <= theta < 1 for source, seed, theta in cases)
    data, hist_columns, masses, u, K = read_input()
    manifest = {'scope': 'Direct six-comparison-label average from the fixed-seed previous-theme price. Necessary LP point only; no SPE or universal half conclusion.',
                'point': str(POINT.relative_to(RUN)), 'point_sha256': POINT_SHA,
                'matrix': str(MATRIX.relative_to(RUN)), 'matrix_sha256': MATRIX_SHA,
                'W': data['W'], 'K': str(K), 'actual_u': list(map(str, u)),
                'rows': 19621, 'columns': 15593, 'original_columns': 4849,
                'generator_sha256': digest(__file__), 'verifier_sha256': digest(HERE/'verify.py'),
                'runtime': {'python': platform.python_version(), 'numpy': np.__version__, 'scipy': scipy.__version__},
                'cases_requested': [[source, seed, str(theta)] for source, seed, theta in cases],
                'parameter_names': list(NAMES), 'emit_general': args.emit_general,
                'result_files': []}
    write_json(output/'manifest.json', manifest)
    started = time.monotonic()
    summaries = []
    for source, seed, theta in cases:
        record = discover_case(data, hist_columns, masses, u, K, source, seed, theta, args.emit_general)
        name = record['case_id']+'.json'
        write_json(output/name, record)
        manifest['result_files'].append({'file': name, 'sha256': digest(output/name)})
        write_json(output/'manifest.json', manifest)
        summary = {key: record[key] for key in ('case_id', 'success', 'exact_slack_float', 'seconds') if key in record}
        if record['success']:
            summary['cone_lower_bound_float'] = record['occupation_certificate']['exact_cone_lower_bound_float']
            summary['nonseparation_certified'] = record['occupation_certificate']['nonseparation_certified']
        summaries.append(summary)
        write_json(output/'summary.json', {'cases': len(summaries), 'negative_cases': sum(x.get('exact_slack_float', 0) < 0 for x in summaries),
                                         'exact_nonseparation_certificates': sum(x.get('nonseparation_certified', False) for x in summaries),
                                         'elapsed_seconds': time.monotonic()-started, 'results': summaries})
        print(json.dumps(summary, ensure_ascii=False), flush=True)
    assert all(x['success'] for x in summaries)
    if args.verify:
        subprocess.run([sys.executable, str(HERE/'verify.py'), '--input-dir', str(output), '--output', str(output/'independent_audit.json')], check=True)
    print(json.dumps({'completed_cases': len(summaries), 'output_dir': str(output), 'seconds': time.monotonic()-started}), flush=True)


if __name__ == '__main__':
    main()
