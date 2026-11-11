"""One complete 19-parameter previous-theme price cone on the 65-atom point.

Actual tail source 1; k=5; theta=1/2; initial (previous,current)=(Z,Z).
Static queries: ten legal visible labels, the five-comparison mean, and Z.
The true same-source terminal map is not frozen across forced branches.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import sys
import time

sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
POINT = HERE.parent/'free66_lower_certificate.json'
LABELS = 'ABCDEUVWXY'
NAMES = ['sigma', 'alpha_m', 'alpha_l', 'beta_m', 'beta_l']+[f'mu_{c}' for c in LABELS]+['mu_mean_T', 'mu_Z', 'mu_current', 'mu_previous']
STATES = tuple(product((0, 1), repeat=2))
THETA = F(1, 2)
KTAIL = 5
ACTIONS = tuple(product((0, 1), range(4)))
ZERO = F(0)


def q(n, d):
    assert d or not n
    return F(n, d) if n else ZERO


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), ZERO)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solve_exact(matrix, rhs):
    a = [list(map(F, row))+[F(v)] for row, v in zip(matrix, rhs)]
    for j in range(len(a)):
        p = next(i for i in range(j, len(a)) if a[i][j])
        a[j], a[p] = a[p], a[j]
        z = a[j][j]
        a[j] = [v/z for v in a[j]]
        for i in range(len(a)):
            if i != j and a[i][j]:
                z = a[i][j]
                a[i] = [v-z*w for v, w in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


@lru_cache(None)
def inverses():
    out = []
    for policy in product((0, 1), repeat=4):
        matrix = [[F(i == j) for j in range(4)] for i in range(4)]
        for i, (a, t) in enumerate(STATES):
            matrix[i][2*t+policy[i]] -= THETA
        cols = [solve_exact(matrix, [F(i == j) for i in range(4)]) for j in range(4)]
        out.append((policy, tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))))
    return out


def features(key, previous, current, terminal, middle):
    b, bits, d = key
    p, ell = b, b+sum(bits[:4])
    load = p+current+middle+terminal
    den = p+current+middle+1
    ulast = q(terminal, load)
    out = [q(current, load), q(middle, ell+1), q(terminal, ell+1), F(middle), F(terminal)]
    out += [q(bit, den)-ulast for bit in bits]
    out += [q(d, 5*den)-ulast, q(b, den)-ulast,
            q(current, den)-ulast, q(previous, den)-ulast]
    assert len(out) == 19
    return tuple(out)


def exact_bellman(key, params):
    edge = {(a, t, c): min(dot(params, features(key, a, t, c, s)) for s in range(4))
            for a, t, c in product((0, 1), repeat=3)}
    candidates = []
    for policy, inverse in inverses():
        costs = [edge[a, t, policy[i]] for i, (a, t) in enumerate(STATES)]
        candidates.append(tuple(dot(row, costs) for row in inverse))
    V = tuple(min(v[i] for v in candidates) for i in range(4))
    assert V in candidates
    slacks = [dot(params, features(key, a, t, c, s))+THETA*V[2*t+c]-V[2*a+t]
              for a, t, c in product((0, 1), repeat=3) for s in range(4)]
    assert min(slacks) >= 0
    psi = tuple((1-THETA)*v for v in V)
    b = key[0]
    for t in (0, 1):
        price = psi[2+t]-psi[t]
        assert q((1-THETA)*params[-1], b+t+4) <= price <= q((1-THETA)*params[-1], b+t+1)
    return psi, min(slacks)


def read_point():
    inputs = json.loads((HERE/'inputs.json').read_text())
    for name, expected in inputs['source_sha256'].items():
        assert sha(ROOT/name) == expected, name
    data = json.loads(POINT.read_text())
    assert len(data['atoms']) == 65
    masses = defaultdict(F)
    utilities = [ZERO]*5
    for atom in data['atoms']:
        w = atom['witness']
        b, bits, d, mass = w['background'], tuple(map(int, w['bits'])), w['d'], F(atom['mass'])
        assert b in (0, 1) and len(bits) == 10 and set(bits) <= {0, 1} and 0 <= d <= 5 and mass > 0
        masses[b, bits, d] += mass
        for i in range(5):
            utilities[i] += mass*q(bits[i], b+sum(bits[:5]))
    K = F(data['capacity_mass'])
    external = [utilities[0], 3*utilities[4], utilities[4], 3*K, K]+[ZERO]*14
    return inputs, dict(sorted(masses.items())), utilities, K, external


def occupation(keys, masses, tables, marginals, external):
    residual = list(external)
    records = []
    offset = 0
    for key, table in zip(keys, tables):
        policies = []
        for state in range(4):
            row = [max(float(v), 0) for v in marginals[offset:offset+len(ACTIONS)]]
            offset += len(ACTIONS)
            norm = sum(row)
            if norm > 1e-13:
                rational = [F(v/norm).limit_denominator(10**9) if v/norm > 1e-12 else ZERO for v in row]
                total = sum(rational, ZERO)
                rational = [v/total for v in rational]
            else:
                rational = [F(j == 0) for j in range(len(ACTIONS))]
            assert min(rational) >= 0 and sum(rational, ZERO) == 1
            policies.append(rational)
        transition = [[ZERO]*4 for _ in range(4)]
        for i, (a, t) in enumerate(STATES):
            for action, (c, s) in enumerate(ACTIONS):
                transition[i][2*t+c] += policies[i][action]
        initial = [F(i == 3*key[0]) for i in range(4)]
        matrix = [[F(i == j)-THETA*transition[j][i] for j in range(4)] for i in range(4)]
        flow = solve_exact(matrix, [(1-THETA)*v for v in initial])
        assert min(flow) >= 0 and sum(flow, ZERO) == 1
        for i in range(4):
            assert flow[i]-THETA*sum(flow[j]*transition[j][i] for j in range(4)) == (1-THETA)*initial[i]
        for j in range(19):
            expected = sum((flow[i]*policies[i][a]*table[i][a][j] for i in range(4) for a in range(len(ACTIONS))), ZERO)
            residual[j] -= masses[key]*expected
        b, bits, d = key
        records.append({'background': b, 'bits': ''.join(map(str, bits)), 'd': d, 'mass': str(masses[key]),
                        'initial': list(map(str, initial)), 'action_probabilities': [list(map(str, r)) for r in policies],
                        'discounted_state_flow': list(map(str, flow))})
    assert offset == len(marginals)
    lower = min(residual)
    return {'scope': 'Entire normalized 19-parameter cone at actual tail source 1, theta=1/2, initial (Z,Z), fixed 65-atom measure.',
            'all_parameter_residuals': {n: str(v) for n, v in zip(NAMES, residual)},
            'exact_cone_lower_bound': str(lower), 'lower_bound_float': float(lower),
            'nonseparation_certified': lower >= 0, 'occupation_witnesses': records,
            'not_a_common_realizable_strategy': True}


def main():
    started = time.monotonic()
    inputs, masses, utilities, K, external = read_point()
    keys = list(masses)
    dim, nvar = 19, 19+4*len(keys)
    rr, cc, vv, tables = [], [], [], []
    obj = list(map(float, external))+[0.]*(nvar-dim)
    nrows = 0
    for no, key in enumerate(keys):
        obj[dim+4*no+3*key[0]] -= float((1-THETA)*masses[key])
        table = []
        for state, (a, t) in enumerate(STATES):
            local = []
            for c, s in ACTIONS:
                ft = features(key, a, t, c, s)
                local.append(ft)
                for j, v in enumerate(ft):
                    if v:
                        rr.append(nrows); cc.append(j); vv.append(-float(v))
                rr += [nrows, nrows]
                cc += [dim+4*no+state, dim+4*no+2*t+c]
                vv += [1., -float(THETA)]
                nrows += 1
            table.append(local)
        tables.append(table)
    A = coo_matrix((vv, (rr, cc)), shape=(nrows, nvar)).tocsr()
    norm = coo_matrix(([1.]*dim, ([0]*dim, list(range(dim)))), shape=(1, nvar)).tocsr()
    fit = linprog(obj, A_ub=A, b_ub=np.zeros(nrows), A_eq=norm, b_eq=[1],
                  bounds=[(0, None)]*dim+[(None, None)]*(nvar-dim), method='highs-ds',
                  options={'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
    assert fit.success, fit.message
    params = [F(float(v)).limit_denominator(10**7) if v > 1e-12 else ZERO for v in fit.x[:dim]]
    total = sum(params, ZERO)
    params = [v/total for v in params]
    table = []
    psi_sum = ZERO
    for key in keys:
        psi, minimum = exact_bellman(key, params)
        b, bits, d = key
        psi_sum += masses[key]*psi[3*b]
        coefficient = params[0]*q(bits[0], b+sum(bits[:5]))+(3*params[1]+params[2])*q(bits[4], b+sum(bits[:5]))-psi[3*b]
        table.append({'background': b, 'bits': ''.join(map(str, bits)), 'd': d, 'mass': str(masses[key]),
                      'psi': list(map(str, psi)), 'initial_value': str(psi[3*b]),
                      'customer_coefficient': str(coefficient), 'min_bellman_slack': str(minimum)})
    slack = dot(external, params)-psi_sum
    capcoef = 3*params[3]+params[4]
    assert sum(F(r['mass'])*F(r['customer_coefficient']) for r in table)+K*capcoef == slack
    occ = occupation(keys, masses, tables, -fit.ineqlin.marginals, external)
    assert F(occ['exact_cone_lower_bound']) <= slack
    out = {'schema': 1, 'case': 'actual-tail-1_theta-1/2_initial-ZZ', 'source': 1, 'theta': '1/2',
           'remaining': 5, 'middle_count': 3, 'initial_pair': ['Z', 'Z'],
           'source_background': 'b', 'actual_terminal_prefix': 'b+A+B+C+D',
           'parameter_names': NAMES, 'parameters': list(map(str, params)),
           'positive_parameters': {n: str(v) for n, v in zip(NAMES, params) if v},
           'normalization': 'All 19 globally nonnegative parameters sum to one.',
           'point_sha256': sha(POINT), 'source_sha256': inputs['source_sha256'],
           'positive_projected_types': len(keys), 'lp_variables': nvar, 'lp_inequalities': nrows,
           'numeric_objective': float(fit.fun), 'exact_slack': str(slack), 'exact_slack_float': float(slack),
           'actual_tail_utilities': list(map(str, utilities)), 'capacity_mass': str(K),
           'budget_coordinates': list(map(str, external)), 'capacity_coefficient': str(capcoef),
           'type_table': table, 'occupation_certificate': occ,
           'negative_row_found': slack < 0, 'not_an_SPE_counterexample': True,
           'seconds': time.monotonic()-started}
    (HERE/'single_case_result.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('source_sha256', 'type_table', 'occupation_certificate')}, indent=2))
    print(json.dumps({k: v for k, v in occ.items() if k != 'occupation_witnesses'}, indent=2))


if __name__ == '__main__':
    main()
