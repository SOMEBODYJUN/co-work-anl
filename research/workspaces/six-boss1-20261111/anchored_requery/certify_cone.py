#!/usr/bin/env python3
"""Independent exact lower certificates for the sampled entire weight cones.

This does not import the discovery program.  It enumerates all literal six
indices, reconstructs source r_i directly, and obtains a rational stochastic
local policy.  Discounted occupation flows prove a lower bound valid for
every normalized nonnegative portfolio weight, not merely the returned one.
These local policies are LP dual witnesses and are not game strategies.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
POINT = RUN/'discounted_augmented_lp/augmented_lp_exact.json'
EXPECTED = 'a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505'
WORDS = tuple(product((0, 1), repeat=3))
ZERO = Q(0)


def frac(n, d):
    assert d or n == 0
    return Q(n, d) if d else ZERO


def solve(mat, rhs):
    m = [list(row)+[v] for row, v in zip(mat, rhs)]
    for j in range(len(m)):
        pivot = next(i for i in range(j, len(m)) if m[i][j])
        m[j], m[pivot] = m[pivot], m[j]
        z = m[j][j]
        m[j] = [v/z for v in m[j]]
        for i in range(len(m)):
            if i != j and m[i][j]:
                z = m[i][j]
                m[i] = [a-z*b for a, b in zip(m[i], m[j])]
    return tuple(row[-1] for row in m)


def read_data():
    assert sha256(POINT.read_bytes()).hexdigest() == EXPECTED
    data = json.loads(POINT.read_text())
    hs = {}
    current = None
    for i, col in enumerate(data['columns'][:4849]):
        if col['kind'] == 'hist':
            current = i
            hs[i] = {'bits': tuple(map(int, col['actual_bits'])), 'mass': Q(col['weight']),
                     'words': tuple(w for w, n in zip(WORDS, col['hist']) for _ in range(n)),
                     'joint': defaultdict(dict)}
            assert len(hs[i]['words']) == 6
        elif col['kind'] == 'joint-reply':
            f, diag, wi, wj = col['group']
            hs[current]['joint'][f, diag, tuple(wi), tuple(wj)][tuple(col['state'])] = Q(col['weight'])
    for h in hs.values():
        for states in h['joint'].values():
            assert set(states) == {(0, 1), (1, 0), (1, 1)}
            states[0, 0] = h['mass']-sum(states.values(), ZERO)
            assert min(states.values()) >= 0
    return data, hs


def layout(hs, data, source, orbit, parameter_names):
    f, diag = orbit
    edges = [(i, j) for i in range(6) for j in range(6) if (i == j) == bool(diag)]
    assert len(edges) == (6 if diag else 30)
    assert all(sum(i == a for i, j in edges) == (1 if diag else 5) for a in range(6))
    masses = defaultdict(Q)
    source_total = ZERO
    u6 = ZERO
    for h in hs.values():
        bits = h['bits']; words = h['words']; mass = h['mass']
        u6 += mass*frac(bits[5], sum(bits))
        if source == 'actual5':
            source_total += mass*frac(bits[4], sum(bits))
        else:
            source_total += mass*sum((frac(w[1], sum(bits[:3])+sum(w)) for w in words), ZERO)/6
        for i, j in edges:
            wi, wj = words[i], words[j]
            st = h['joint'][f, diag, wi, wj]
            for (r, z), joint_mass in st.items():
                if not joint_mass:
                    continue
                queries = dict(zip([f'A{k+1}' for k in range(6)], map(Q, bits)))
                queries.update(dict(zip(('Ti', 'Bi', 'Ci'), map(Q, wi))))
                queries.update(dict(zip(('Tj', 'Bj', 'Cj'), map(Q, wj))))
                queries.update(R=Q(r), Z=Q(z))
                for k, label in enumerate(('mean_T', 'mean_B', 'mean_C')):
                    queries[label] = Q(sum(w[k] for w in words), 6)
                if source == 'actual5':
                    p, t0, t1 = sum(bits[:4]), r, z
                else:
                    p, t0, t1 = sum(bits[:3])+wi[0], wj[1+f], r
                key = (p, sum(bits[:5]), bits[5], t0, t1, tuple(sorted(queries.items())))
                masses[key] += joint_mass/len(edges)
    K = sum((Q(c['weight']) for c in data['columns'][:4849] if c['kind'] == 'K'), ZERO)
    external = {'source': source_total, 'alpha_last': u6, 'beta_last': K}
    return dict(masses), tuple(external.get(name, ZERO) for name in parameter_names)


def features(key, a, t, c, parameter_names):
    p, ell, a0, t0, t1, named = key
    queries = dict(named)
    terminal = frac(c, p+t+c)
    result = {'source': frac(t, p+t+c), 'alpha_last': Q(c, ell+1), 'beta_last': Q(c),
              'mu_current': Q(t, p+t+1)-terminal,
              'mu_previous': Q(a, p+t+1)-terminal}
    for label, member in queries.items():
        result['mu_'+label] = member/(p+t+1)-terminal
    return tuple(result[name] for name in parameter_names)


def certify(hs, data, entry, parameter_names):
    source, orbit, theta, memory = entry['source'], tuple(entry['orbit']), Q(entry['theta']), entry['memory']
    assert entry['mode'] == 'tail'
    masses, external = layout(hs, data, source, orbit, parameter_names)
    keys = sorted(masses)
    dim = len(parameter_names)
    state_list = [(0, t) for t in (0, 1)] if memory == 2 else list(product((0, 1), repeat=2))
    states = len(state_list)
    rows, columns, vals, rhs = [], [], [], []
    feature_tables = []
    objective = list(map(float, external))+[0.]*(len(keys)*states)
    for q, key in enumerate(keys):
        table = []
        start = key[4] if memory == 2 else 2*key[3]+key[4]
        objective[dim+q*states+start] -= float((1-theta)*masses[key])
        for s, (a, t) in enumerate(state_list):
            state_features = []
            for c in (0, 1):
                cost = features(key, a, t, c, parameter_names)
                state_features.append(cost)
                r = len(rhs)
                for j, x in enumerate(cost):
                    if x:
                        rows.append(r); columns.append(j); vals.append(-float(x))
                nxt = c if memory == 2 else 2*t+c
                rows.extend((r, r)); columns.extend((dim+q*states+s, dim+q*states+nxt)); vals.extend((1., -float(theta)))
                rhs.append(0.)
            table.append(state_features)
        feature_tables.append(table)
    nvar = len(objective)
    matrix = coo_matrix((vals, (rows, columns)), shape=(len(rhs), nvar)).tocsr()
    eq = np.zeros((1, nvar)); eq[0, :dim] = 1.
    solution = linprog(objective, A_ub=matrix, b_ub=rhs, A_eq=eq, b_eq=[1.],
                       bounds=[(0, None)]*dim+[(None, None)]*(nvar-dim), method='highs')
    assert solution.success
    marginals = -solution.ineqlin.marginals
    residual = list(external)
    first_residual = list(external)
    witnesses = []
    for q, key in enumerate(keys):
        table = feature_tables[q]
        probability_one = []
        for s in range(states):
            left, right = marginals[(q*states+s)*2:(q*states+s)*2+2]
            total = left+right
            p = Q(float(right/total)).limit_denominator(10**7) if total > 1e-14 else ZERO
            assert 0 <= p <= 1
            probability_one.append(p)
        transition = [[ZERO]*states for _ in range(states)]
        for s, (a, t) in enumerate(state_list):
            for c in (0, 1):
                nxt = c if memory == 2 else 2*t+c
                transition[s][nxt] += probability_one[s] if c else 1-probability_one[s]
        start = key[4] if memory == 2 else 2*key[3]+key[4]
        system = [[Q(s == j)-theta*transition[j][s] for j in range(states)] for s in range(states)]
        flow = solve(system, [(1-theta)*Q(s == start) for s in range(states)])
        assert min(flow) >= 0 and sum(flow, ZERO) == 1
        for s in range(states):
            assert flow[s]-theta*sum((flow[j]*transition[j][s] for j in range(states)), ZERO) == (1-theta)*Q(s == start)
        for j in range(dim):
            cost = sum((flow[s]*((1-probability_one[s])*table[s][0][j]+probability_one[s]*table[s][1][j]) for s in range(states)), ZERO)
            residual[j] -= masses[key]*cost
        first_features = features(key, key[2], key[3], key[4], parameter_names)
        for j in range(dim):
            first_residual[j] -= masses[key]*first_features[j]
        witnesses.append({'visible': [key[0], key[1], key[2], key[3], key[4], [[k, str(v)] for k, v in key[5]]],
                          'mass': str(masses[key]), 'probability_next_one': list(map(str, probability_one)),
                          'discounted_state_flow': list(map(str, flow))})
    bound = min(residual)
    first_bound = min(first_residual)
    assert bound > 0, (source, orbit, theta, memory, float(bound))
    assert first_bound >= 0, (source, orbit, theta, memory, float(first_bound))
    # Uniform normalization is the same for every customer and history.
    # All residual coordinates are exact; hence every nonnegative portfolio
    # with sum(weights)=1 has slack at least bound.
    return {'source': source, 'orbit': list(orbit), 'theta': str(theta), 'memory': memory,
            'scope': 'Entire normalized nonnegative parameter cone at this fixed discount and fixed input point.',
            'parameter_names': parameter_names, 'visible_positive_states': len(keys),
            'float_optimum': float(solution.fun),
            'exact_cone_lower_bound': str(bound), 'exact_cone_lower_bound_float': float(bound),
            'all_parameter_residuals': {n: str(x) for n, x in zip(parameter_names, residual)},
            'first_edge_min_parameter_residual': str(first_bound),
            'first_edge_parameter_residuals': {n: str(x) for n, x in zip(parameter_names, first_residual)},
            'anchored_cone_lower_bound': str((1-theta)*first_bound+theta*bound),
            'occupation_witnesses': witnesses, 'all_flow_equations_exact': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='+')
    parser.add_argument('--output', default='sampled_cones_exact_certificate_19578.json')
    args = parser.parse_args()
    output = (HERE/args.output).resolve()
    assert output.parent == HERE
    data, hs = read_data()
    result = {'point_sha256': EXPECTED, 'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'claim': 'Exact rational stochastic occupation witnesses certify the whole nonnegative weight cone at each listed discount; these are LP dual witnesses, not game policies.',
              'inputs': [], 'cases': []}
    for filename in args.inputs:
        path = (HERE/filename).resolve()
        assert path.parent == HERE
        pack = json.loads(path.read_text())
        assert pack['point_sha256'] == EXPECTED
        result['inputs'].append({'path': filename, 'sha256': sha256(path.read_bytes()).hexdigest()})
        for entry in pack['results']:
            start = time.monotonic()
            cert = certify(hs, data, entry, pack['parameter_names'])
            result['cases'].append(cert)
            print(json.dumps({k: cert[k] for k in ('source', 'orbit', 'theta', 'memory', 'exact_cone_lower_bound_float')})+f' seconds={time.monotonic()-start:.3f}', flush=True)
            output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'cases': len(result['cases']), 'output': str(output),
                      'sha256': sha256(output.read_bytes()).hexdigest()}), flush=True)


if __name__ == '__main__':
    main()
