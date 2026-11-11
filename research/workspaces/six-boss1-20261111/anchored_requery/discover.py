#!/usr/bin/env python3
"""Fixed-history k=2 tail closure, with exact known-entry bookkeeping.

The principal source is h_i=(A1,A2,A3,T_i), whose prescribed payoff is r_i.
Neither its subsequent last replies nor its wallet are replaced by the
actual fifth source.  Hist/group data are literal-orbit averages.  All
artifacts are written only beneath this worker's directory.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
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
POINT = RUN / 'discounted_augmented_lp/augmented_lp_exact.json'
MATRIX = RUN / 'discounted_augmented_lp/exact_matrix.json.gz'
POINT_SHA = 'a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505'
MATRIX_SHA = 'a95bd72e0fdc2b0b93af79b1a0e8b324b6bd1fc8f62abe8a3ce642be4bcc3936'
WORDS = tuple(product((0, 1), repeat=3))
ORBITS = ((0, 0), (1, 0), (1, 1))
STATES = tuple(product((0, 1), repeat=2))
QUERIES = tuple([f'A{i+1}' for i in range(6)] +
                ['Ti', 'Bi', 'Ci', 'Tj', 'Bj', 'Cj', 'R', 'Z',
                 'mean_T', 'mean_B', 'mean_C'])


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def canonical_sha(obj):
    return sha256(json.dumps(obj, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def share(a, b):
    assert b or not a
    return F(a, b) if b else F(0)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def names(memory):
    ans = ('source', 'alpha_last', 'beta_last') + tuple('mu_'+q for q in QUERIES) + ('mu_current',)
    return ans + (('mu_previous',) if memory == 4 else ())


def groups(hist):
    result = {}
    for f, diag in ORBITS:
        for wi, wj in product(WORDS, repeat=2):
            ni, nj = hist[WORDS.index(wi)], hist[WORDS.index(wj)]
            count = (ni if wi == wj else 0) if diag else ni*nj-(ni if wi == wj else 0)
            if count:
                result[f, diag, wi, wj] = count
        assert sum(n for g, n in result.items() if g[:2] == (f, diag)) == (6 if diag else 30)
    return result


def read_input():
    assert digest(POINT) == POINT_SHA
    assert digest(MATRIX) == MATRIX_SHA
    data = json.loads(POINT.read_text())
    assert data['original_columns'] == 4849 and len(data['columns']) == 15593
    cols = data['columns'][:4849]
    hs = {}
    owner = {}
    current = None
    for j, col in enumerate(cols):
        if col['kind'] == 'hist':
            current = j
            hs[j] = {'column': col, 'groups': groups(col['hist']),
                     'states': defaultdict(dict), 'joint_columns': {}}
        elif col['kind'] == 'joint-reply':
            f, diag, wi, wj = col['group']
            g = (f, diag, tuple(wi), tuple(wj))
            state = tuple(col['state'])
            hs[current]['states'][g][state] = F(col['weight'])
            hs[current]['joint_columns'][g, state] = j
            owner[j] = current
    for h in hs.values():
        hm = F(h['column']['weight'])
        for g in h['groups']:
            st = h['states'][g]
            assert set(st) == {(0, 1), (1, 0), (1, 1)}
            st[0, 0] = hm - sum(st.values(), F(0))
            assert min(st.values()) >= 0
    u = [sum((F(h['column']['weight']) *
              share(int(h['column']['actual_bits'][i]), sum(map(int, h['column']['actual_bits'])))
              for h in hs.values()), F(0)) for i in range(6)]
    K = sum((F(c['weight']) for c in cols if c['kind'] == 'K'), F(0))
    return data, cols, hs, owner, u, K


def queries(bits, hist, g, rz):
    means = tuple(F(sum(n*w[a] for n, w in zip(hist, WORDS)), 6) for a in range(3))
    return tuple(map(F, bits+g[2]+g[3]+rz)) + means


def source_cost(bits, hist, source):
    if source == 'actual5':
        return share(bits[4], sum(bits))
    assert source == 'offpath5'
    p3 = sum(bits[:3])
    return sum((F(n, 6)*share(w[1], p3+sum(w)) for w, n in zip(WORDS, hist)), F(0))


def datum(h, g, rz, source):
    col = h['column']
    bits = tuple(map(int, col['actual_bits']))
    wi, wj = g[2:]
    if source == 'actual5':
        p, t0, t1 = sum(bits[:4]), rz[0], rz[1]
    else:
        p = sum(bits[:3]) + wi[0]
        t0, t1 = wj[1+g[0]], rz[0]
    # The preceding label for the known first edge is freely fixed to A6.
    # For its tail the state is exactly (t0,t1), retaining the real entry.
    return p, sum(bits[:5]), bits[5], t0, t1, queries(bits, col['hist'], g, rz)


def feature(p, ell, a, t, c, qs, memory):
    z, denominator = p+t+c, p+t+1
    terminal = share(c, z)
    out = [share(t, z), F(c, ell+1), F(c)]
    out.extend(q/denominator-terminal for q in qs)
    out.append(F(t, denominator)-terminal)
    if memory == 4:
        out.append(F(a, denominator)-terminal)
    return tuple(out)


def solve_fraction(mat, rhs):
    a = [list(map(F, row)) + [F(v)] for row, v in zip(mat, rhs)]
    for j in range(len(a)):
        i = next(i for i in range(j, len(a)) if a[i][j])
        a[j], a[i] = a[i], a[j]
        z = a[j][j]
        a[j] = [x/z for x in a[j]]
        for i in range(len(a)):
            if i != j and a[i][j]:
                z = a[i][j]
                a[i] = [x-z*y for x, y in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


@lru_cache(None)
def inverses(theta):
    answer = []
    for policy in product((0, 1), repeat=4):
        mat = [[F(i == j) for j in range(4)] for i in range(4)]
        for i, (a, t) in enumerate(STATES):
            mat[i][2*t+policy[i]] -= theta
        columns = [solve_fraction(mat, [F(i == j) for i in range(4)]) for j in range(4)]
        answer.append((policy, tuple(tuple(columns[j][i] for j in range(4)) for i in range(4))))
    return tuple(answer)


def bellman(p, ell, qs, params, theta, memory):
    if memory == 2:
        e = {(t, c): dot(feature(p, ell, 0, t, c, qs, memory), params)
             for t, c in product((0, 1), repeat=2)}
        psi = (min(e[0, 0], (1-theta)*e[0, 1]+theta*e[1, 1],
                   (e[0, 1]+theta*e[1, 0])/(1+theta)),
               min(e[1, 1], (1-theta)*e[1, 0]+theta*e[0, 0],
                   (e[1, 0]+theta*e[0, 1])/(1+theta)))
        v = tuple(x/(1-theta) for x in psi)
        for t in (0, 1):
            assert v[t] == min(e[t, c]+theta*v[c] for c in (0, 1))
        return psi
    e = {(a, t, c): dot(feature(p, ell, a, t, c, qs, memory), params)
         for a, t, c in product((0, 1), repeat=3)}
    candidates = []
    for policy, inverse in inverses(theta):
        costs = [e[a, t, policy[i]] for i, (a, t) in enumerate(STATES)]
        candidates.append(tuple(dot(row, costs) for row in inverse))
    v = tuple(min(c[i] for c in candidates) for i in range(4))
    assert v in candidates
    for i, (a, t) in enumerate(STATES):
        assert v[i] == min(e[a, t, c]+theta*v[2*t+c] for c in (0, 1))
    return tuple((1-theta)*x for x in v)


def projected(key, params, theta, memory, mode):
    p, ell, a0, t0, t1, qs = key
    psi = bellman(p, ell, qs, params, theta, memory)
    tail = psi[t1 if memory == 2 else 2*t0+t1]
    if mode == 'tail':
        return tail
    first = dot(feature(p, ell, a0, t0, t1, qs, memory), params)
    if mode == 'first':
        return first
    assert mode == 'anchored'
    return (1-theta)*first+theta*tail


def measure(hs, source, orbit):
    out = defaultdict(F)
    denominator = 6 if orbit[1] else 30
    for h in hs.values():
        for g, n in h['groups'].items():
            if g[:2] == orbit:
                for st, mass in h['states'][g].items():
                    if mass:
                        out[datum(h, g, st, source)] += F(n, denominator)*mass
    return dict(out)


def budget(hs, K, u, source, memory):
    r = sum((F(h['column']['weight']) * source_cost(tuple(map(int, h['column']['actual_bits'])), h['column']['hist'], source)
             for h in hs.values()), F(0))
    return [r, u[5], K] + [F(0)]*(len(names(memory))-3)


def exact_row(cols, hs, source, orbit, params, theta, memory, mode):
    row = [F(0)]*4849
    denominator = 6 if orbit[1] else 30
    cache = {}
    def value(h, g, st):
        key = datum(h, g, st, source)
        if key not in cache:
            cache[key] = projected(key, params, theta, memory, mode)
        return cache[key]
    row[0] = params[2]
    for hi, h in hs.items():
        bits = tuple(map(int, h['column']['actual_bits']))
        row[hi] = params[0]*source_cost(bits, h['column']['hist'], source) + params[1]*share(bits[5], sum(bits))
        for g, n in h['groups'].items():
            if g[:2] != orbit:
                continue
            baseline = value(h, g, (0, 0))
            row[hi] -= F(n, denominator)*baseline
            for st in ((0, 1), (1, 0), (1, 1)):
                row[h['joint_columns'][g, st]] = -F(n, denominator)*(value(h, g, st)-baseline)
    return row, len(cache)


def discover_case(cols, hs, K, u, source, orbit, theta, memory, mode):
    started = time.monotonic()
    param_names = names(memory)
    dimension = len(param_names)
    states = measure(hs, source, orbit)
    keys = list(states)
    nvar = dimension+memory*len(keys)
    rr, cc, vv, rhs = [], [], [], []
    for q, (p, ell, a0, t0, t1, qs) in enumerate(keys):
        left_states = ((0, t) for t in (0, 1)) if memory == 2 else iter(STATES)
        for a, t in left_states:
            for c in (0, 1):
                r = len(rhs)
                for j, val in enumerate(feature(p, ell, a, t, c, qs, memory)):
                    if val:
                        rr.append(r); cc.append(j); vv.append(-float(val))
                current = t if memory == 2 else 2*a+t
                nxt = c if memory == 2 else 2*t+c
                rr.extend((r, r)); cc.extend((dimension+memory*q+current, dimension+memory*q+nxt)); vv.extend((1., -float(theta)))
                rhs.append(0.)
    mat = coo_matrix((vv, (rr, cc)), shape=(len(rhs), nvar)).tocsr()
    external = budget(hs, K, u, source, memory)
    objective = list(map(float, external)) + [0.]*(nvar-dimension)
    for q, key in enumerate(keys):
        p, ell, a0, t0, t1, qs = key
        index = t1 if memory == 2 else 2*t0+t1
        tail_factor = theta if mode == 'anchored' else F(1)
        objective[dimension+memory*q+index] -= float(tail_factor*(1-theta)*states[key])
        if mode == 'anchored':
            for j, x in enumerate(feature(p, ell, a0, t0, t1, qs, memory)):
                objective[j] -= float((1-theta)*states[key]*x)
    eq = np.zeros((1, nvar)); eq[0, :dimension] = 1
    result = linprog(objective, A_ub=mat, b_ub=rhs, A_eq=eq, b_eq=[1.],
                     bounds=[(0, None)]*dimension+[(None, None)]*(nvar-dimension), method='highs')
    record = {'source': source, 'orbit': list(orbit), 'theta': str(theta), 'memory': memory,
              'mode': mode, 'visible_positive_states': len(keys), 'success': result.success}
    if not result.success:
        record['message'] = result.message
        return record
    params = [F(float(x)).limit_denominator(1000000) if x > 1e-10 else F(0) for x in result.x[:dimension]]
    total = sum(params, F(0)); params = [x/total for x in params]
    external_value = dot(external, params)
    slacks = {m: external_value-sum((mass*projected(key, params, theta, memory, m) for key, mass in states.items()), F(0))
              for m in ('first', 'tail', 'anchored')}
    assert slacks['anchored'] == (1-theta)*slacks['first']+theta*slacks['tail']
    record.update(float_objective=float(result.fun), exact_slack=str(slacks[mode]),
                  exact_slack_float=float(slacks[mode]),
                  parameters={name: str(x) for name, x in zip(param_names, params) if x},
                  budget_coefficients={'source_average': str(params[0]), 'actual_u6': str(params[1]), 'K': str(params[2])},
                  budget_value=str(external_value),
                  fixed_parameter_slacks={m: str(v) for m, v in slacks.items()},
                  fixed_parameter_slacks_float={m: float(v) for m, v in slacks.items()})
    if slacks[mode] < 0:
        row, cache_count = exact_row(cols, hs, source, orbit, params, theta, memory, mode)
        actual = sum((v*F(col['weight']) for v, col in zip(row, cols)), F(0))
        assert actual == slacks[mode]
        record.update(original_column_count=4849, auxiliary_column_count=10744,
                      auxiliary_coefficients='all zero', all_projected_states=cache_count,
                      coefficients=[[i, str(v)] for i, v in enumerate(row) if v],
                      full_original_coefficients=list(map(str, row)),
                      row_sha256=canonical_sha(list(map(str, row))))
    record['seconds'] = time.monotonic()-started
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', default='offpath5')
    parser.add_argument('--thetas', default='0,1/2,3/4')
    parser.add_argument('--memory', type=int, choices=(2, 4), default=2)
    parser.add_argument('--mode', choices=('tail', 'anchored'), default='tail')
    parser.add_argument('--output', default='offpath_tail_two_state_19578.json')
    args = parser.parse_args()
    output = (HERE/args.output).resolve()
    assert output.parent == HERE
    data, cols, hs, owner, u, K = read_input()
    records = []
    report = {'scope': 'Finite parameter-cone optimization at sampled discounts for fixed legal histories; not SPE or half.',
              'point': str(POINT.relative_to(RUN)), 'point_sha256': POINT_SHA,
              'matrix_sha256': MATRIX_SHA, 'W': data['W'],
              'source_sha256': digest(__file__), 'parameter_names': names(args.memory),
              'old_column_descriptors_sha256': canonical_sha([{k: v for k, v in c.items() if k != 'weight'} for c in cols]),
              'source_payoffs': {s: str(budget(hs, K, u, s, args.memory)[0]) for s in args.sources.split(',')},
              'actual_u': list(map(str, u)), 'K': str(K), 'results': records}
    for source, orbit, theta in product(args.sources.split(','), ORBITS, map(F, args.thetas.split(','))):
        assert source in ('offpath5', 'actual5') and 0 <= theta < 1
        record = discover_case(cols, hs, K, u, source, orbit, theta, args.memory, args.mode)
        records.append(record)
        report['cases'] = len(records)
        report['negative_cases'] = sum(F(r.get('exact_slack', 0)) < 0 for r in records)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps({k: record[k] for k in ('source', 'orbit', 'theta', 'memory', 'mode', 'exact_slack_float', 'seconds') if k in record}, ensure_ascii=False), flush=True)
    print(json.dumps({'output': str(output), 'sha256': digest(output), 'cases': len(records),
                      'negative_cases': report['negative_cases']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
