"""Main's single two-source nested price trial, with exact cone witness.

The inner Bellman parameters and five outer parameters are optimized together.
This imports the frozen inner exact solver, never claims an independent audit,
and records a separate two-level randomized occupation certificate.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import importlib.util
import json
import sys
import time

sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
WS = HERE.parent
SOURCE = WS / 'previous_price_search/discover.py'
spec = importlib.util.spec_from_file_location('frozen_inner_price', SOURCE)
inner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inner)
Z = F(0)
OUTER_NAMES = ('outer_source', 'outer_alpha_m', 'outer_alpha_l', 'outer_beta_m', 'outer_beta_l')


def share(n, d):
    assert d or not n
    return F(n, d) if n else Z


def outer_features(bits, source, y, c, s):
    p, ell = sum(bits[:source-1]), sum(bits[:5])
    return (share(y, p+y+s+c), F(s, ell+1), F(c, ell+1), F(s), F(c))


def rational_distribution(values):
    values = [max(float(x), 0.) for x in values]
    total = sum(values)
    if total <= 1e-13:
        return [F(j == 0) for j in range(len(values))]
    raw = [F(x/total).limit_denominator(10**10) if x/total > 1e-12 else Z for x in values]
    norm = sum(raw, Z)
    assert norm > 0
    return [x/norm for x in raw]


def main():
    started = time.monotonic()
    source, seed, outer_source, theta = 2, 6, 1, F(1, 4)
    data, hist, masses, u, cap = inner.read_input()
    keys = list(masses)
    kin, kout = 7-source, 7-outer_source
    ai = list(product((0, 1), range(kin-1)))
    ao = list(product((0, 1), range(kout-1)))
    names = list(inner.NAMES) + list(OUTER_NAMES)
    wallet = list(inner.wallet(source, u, cap)) + [u[outer_source-1], (kout-2)*u[5], u[5], (kout-2)*cap, cap]
    dim, nvar = 19, 19+6*len(keys)
    rr, cc, vv, descriptors = [], [], [], []
    objectives = list(map(float, wallet)) + [0.]*(nvar-dim)
    tables = []
    def row(coeffs, desc):
        rowid = len(descriptors)
        for j, x in coeffs:
            if x:
                rr.append(rowid); cc.append(j); vv.append(float(x))
        descriptors.append(desc)
        return rowid
    for n, (bits, d) in enumerate(keys):
        vbase, zbase = dim+6*n, dim+6*n+4
        entry = {'inner_rows': [], 'outer_rows': []}
        for state, (a, t) in enumerate(inner.STATES):
            ids = []
            for c, s in ai:
                ft = inner.features(bits, d, source, a, t, c, s)
                ids.append(row([(j, -x) for j, x in enumerate(ft)] + [(vbase+state, F(1)), (vbase+2*t+c, -theta)],
                               ['inner', n, state, c, s]))
            entry['inner_rows'].append(ids)
        for y in (0, 1):
            prob = F(d if y else 6-d, 6)
            objectives[zbase+y] -= float(masses[bits, d]*prob)
            ids = []
            for c, s in ao:
                ft = outer_features(bits, outer_source, y, c, s)
                ids.append(row([(14+j, -x) for j, x in enumerate(ft)] +
                               [(vbase+2*c+bits[seed-1], -(1-theta)), (zbase+y, F(1))],
                               ['outer', n, y, c, s]))
            entry['outer_rows'].append(ids)
        tables.append(entry)
    matrix = coo_matrix((vv, (rr, cc)), shape=(len(descriptors), nvar)).tocsr()
    norm = coo_matrix(([1.]*dim, ([0]*dim, list(range(dim)))), shape=(1, nvar)).tocsr()
    ans = linprog(objectives, A_ub=matrix, b_ub=np.zeros(len(descriptors)), A_eq=norm, b_eq=[1.],
                  bounds=[(0, None)]*dim+[(None, None)]*(nvar-dim), method='highs',
                  options={'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
    assert ans.success, ans.message
    params = [F(float(x)).limit_denominator(10**9) if x > 1e-12 else Z for x in ans.x[:dim]]
    total = sum(params, Z)
    params = [x/total for x in params]
    assert min(params) >= 0 and sum(params, Z) == 1
    cache = {}
    def exact_rhs(bits, d):
        key = bits, d
        if key not in cache:
            psi = inner.exact_bellman(bits, d, source, tuple(params[:14]), theta)[0]
            values = [min(inner.dot(params[14:], outer_features(bits, outer_source, y, c, s)) + psi[2*c+bits[seed-1]]
                          for c, s in ao) for y in (0, 1)]
            cache[key] = (1-F(d, 6))*values[0]+F(d, 6)*values[1]
        return cache[key]
    slack = inner.dot(wallet, params)-sum((mass*exact_rhs(*key) for key, mass in masses.items()), Z)
    # Any rational outer policy, followed by any rational inner policy, gives
    # an exact upper bound for every parameter's nested minimum.
    duals = -ans.ineqlin.marginals
    residuals = list(wallet)
    witnesses = []
    for (bits, d), entry in zip(keys, tables):
        mass = masses[bits, d]
        op = [rational_distribution([duals[r] for r in ids]) for ids in entry['outer_rows']]
        ip = [rational_distribution([duals[r] for r in ids]) for ids in entry['inner_rows']]
        initial = [Z]*4
        for y in (0, 1):
            py = F(d if y else 6-d, 6)
            for prob, (c, s) in zip(op[y], ao):
                initial[2*c+bits[seed-1]] += py*prob
                for j, value in enumerate(outer_features(bits, outer_source, y, c, s)):
                    residuals[14+j] -= mass*py*prob*value
        assert sum(initial, Z) == 1
        transition = [[Z]*4 for _ in range(4)]
        for state, (a, t) in enumerate(inner.STATES):
            for prob, (c, s) in zip(ip[state], ai):
                transition[state][2*t+c] += prob
        system = [[F(i == j)-theta*transition[j][i] for j in range(4)] for i in range(4)]
        flow = inner.solve_exact(system, [(1-theta)*p for p in initial])
        assert min(flow) >= 0 and sum(flow, Z) == 1
        for state, (a, t) in enumerate(inner.STATES):
            assert flow[state]-theta*sum((flow[j]*transition[j][state] for j in range(4)), Z) == (1-theta)*initial[state]
            for prob, (c, s) in zip(ip[state], ai):
                for j, value in enumerate(inner.features(bits, d, source, a, t, c, s)):
                    residuals[j] -= mass*flow[state]*prob*value
        witnesses.append({'actual_bits': ''.join(map(str, bits)), 'd': d, 'mass': str(mass),
                          'outer_action_probabilities': [list(map(str, row)) for row in op],
                          'inner_action_probabilities': [list(map(str, row)) for row in ip],
                          'inner_initial_distribution': list(map(str, initial)),
                          'inner_discounted_flow': list(map(str, flow))})
    lower = min(residuals)
    assert lower <= slack
    coefficients = [Z]*4849
    coefficients[0] = (kin-2)*params[3]+params[4]+(kout-2)*params[17]+params[18]
    for j, bits, d, mass in hist:
        coefficients[j] = params[0]*share(bits[source-1], sum(bits))+params[14]*share(bits[outer_source-1], sum(bits)) \
            + ((kin-2)*params[1]+params[2]+(kout-2)*params[15]+params[16])*share(bits[5], sum(bits))-exact_rhs(bits, d)
    assert sum((coefficient*F(col['weight']) for coefficient, col in zip(coefficients, data['columns'][:4849])), Z) == slack
    out = {'scope': 'One fixed inner source/seed/theta and outer source; the full normalized nonnegative nineteen-parameter cone, not all possible nested pricing and not an SPE.',
           'point_sha256': inner.POINT_SHA, 'matrix_sha256': inner.MATRIX_SHA,
           'inner_source': source, 'seed': seed, 'theta': str(theta), 'outer_source': outer_source,
           'parameter_names': names, 'parameter_count': dim, 'lp_variables': nvar, 'lp_inequalities': len(descriptors),
           'numeric_objective': float(ans.fun), 'exact_slack': str(slack), 'exact_slack_float': float(slack),
           'parameters': {n: str(x) for n, x in zip(names, params) if x}, 'parameters_full': list(map(str, params)),
           'wallet': list(map(str, wallet)), 'coefficients': [[j, str(x)] for j, x in enumerate(coefficients) if x],
           'auxiliary_coefficients': 'all zero', 'normalized_cone_lower_bound': str(lower),
           'normalized_cone_lower_bound_float': float(lower), 'nonseparation_certified': lower >= 0,
           'all_parameter_residuals': {n: str(x) for n, x in zip(names, residuals)},
           'outer_actions_c_s': [list(a) for a in ao], 'inner_actions_c_s': [list(a) for a in ai],
           'occupation_witnesses': witnesses, 'seconds': time.monotonic()-started,
           'sources': [{'path': str(p.relative_to(WS)), 'sha256': sha256(p.read_bytes()).hexdigest()} for p in (SOURCE, Path(__file__))]}
    (HERE / 'one_case_exact.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: out[k] for k in ('lp_variables', 'lp_inequalities', 'numeric_objective', 'exact_slack_float', 'normalized_cone_lower_bound_float', 'nonseparation_certified', 'parameters', 'seconds')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
