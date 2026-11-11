"""One full 21-parameter cone, with all 65 atoms and original AB histograms.

The only numerical optimization is the saved fixed-source/discount/initial LP.
Re-running this file replays its saved raw output; it does not optimize again.
All proof-bearing Bellman values and occupation-flow bounds are rational.
"""
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
from scipy.sparse import coo_matrix, save_npz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ZERO = F(0)
THETA = F(1, 2)
STATES = tuple(product((0, 1), repeat=2))
ACTIONS = tuple(product((0, 1), range(4)))
NAMES = ['sigma', 'alpha_m', 'alpha_l', 'beta_m', 'beta_l']
NAMES += ['mu_'+c for c in 'ABCDEUVWXY']
NAMES += ['mu_mean_T', 'mu_Z', 'mu_current', 'mu_previous',
          'lambda_AB_price', 'mu_AB_terminal_mean']


def share(n, d):
    assert d or not n
    return F(n, d) if n else ZERO


def dot(a, b):
    return sum((v*w for v, w in zip(a, b)), ZERO)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solve_exact(matrix, rhs):
    rows = [list(map(F, row))+[F(y)] for row, y in zip(matrix, rhs)]
    for j in range(len(rows)):
        pivot = next(i for i in range(j, len(rows)) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        z = rows[j][j]
        rows[j] = [x/z for x in rows[j]]
        for i in range(len(rows)):
            if i != j and rows[i][j]:
                z = rows[i][j]
                rows[i] = [x-z*y for x, y in zip(rows[i], rows[j])]
    return tuple(row[-1] for row in rows)


@lru_cache(None)
def policy_inverses():
    result = []
    for policy in product((0, 1), repeat=4):
        matrix = [[F(i == j) for j in range(4)] for i in range(4)]
        for i, (a, t) in enumerate(STATES):
            matrix[i][2*t+policy[i]] -= THETA
        columns = [solve_exact(matrix, [F(i == j) for i in range(4)]) for j in range(4)]
        inverse = tuple(tuple(columns[j][i] for j in range(4)) for i in range(4))
        result.append((policy, inverse))
    return tuple(result)


def load_data():
    data = json.loads((HERE/'inputs.json').read_text())
    assert data['parameter_names'] == NAMES
    for relative, expected in data['source_sha256'].items():
        assert digest(ROOT/relative) == expected, relative
    source = json.loads((ROOT/next(iter(data['source_sha256']))).read_text())
    assert data['atoms'] == source['atoms'] and data['capacity_mass'] == source['capacity_mass']
    assert len(data['atoms']) == 65
    atoms = []
    utilities = [ZERO]*5
    Uab = ZERO
    for index, record in enumerate(data['atoms']):
        w = record['witness']
        b, bits, d = w['background'], tuple(map(int, w['bits'])), w['d']
        mass = F(record['mass'])
        assert b in (0, 1) and len(bits) == 10 and set(bits) <= {0, 1}
        assert mass > 0 and 0 <= d <= 5
        hist = w['histograms']['AB']
        assert len(hist) == 8 and all(isinstance(v, int) and v >= 0 for v in hist)
        assert sum(hist) == 5
        triples = tuple(v for v, count in zip(product((0, 1), repeat=3), hist) for _ in range(count))
        assert sum(t for t, x, y in triples) == d
        p = b+bits[0]+bits[1]
        D = sum((share(1, p+t+x+1) for t, x, y in triples), ZERO)
        L = sum((share(y, p+t+x+y) for t, x, y in triples), ZERO)
        ybar = F(sum(y for t, x, y in triples), 5)
        atoms.append({'id': index, 'b': b, 'bits': bits, 'd': d, 'mass': mass,
                      'D': D, 'L': L, 'ybar': ybar})
        Uab += mass*L
        for i in range(5):
            utilities[i] += mass*share(bits[i], b+sum(bits[:5]))
    K = F(data['capacity_mass'])
    budget = [utilities[0], 3*utilities[4], utilities[4], 3*K, K]+[ZERO]*14+[Uab, ZERO]
    return data, atoms, utilities, K, Uab, budget


def features(atom, a, t, c, s):
    b, bits, d = atom['b'], atom['bits'], atom['d']
    ell = b+sum(bits[:4])
    load, den = b+t+s+c, b+t+s+1
    terminal = share(c, load)
    out = [share(t, load), share(s, ell+1), share(c, ell+1), F(s), F(c)]
    out += [share(bit, den)-terminal for bit in bits]
    out += [share(d, 5*den)-terminal, share(b, den)-terminal,
            share(t, den)-terminal, share(a, den)-terminal]
    out += [c*atom['D'], atom['ybar']/den-terminal]
    assert len(out) == 21
    return tuple(out)


def bellman_exact(atom, params):
    edge = {(a, t, c): min(dot(params, features(atom, a, t, c, s)) for s in range(4))
            for a, t, c in product((0, 1), repeat=3)}
    candidates = []
    for policy, inverse in policy_inverses():
        costs = [edge[a, t, policy[state]] for state, (a, t) in enumerate(STATES)]
        candidates.append(tuple(dot(row, costs) for row in inverse))
    V = tuple(min(candidate[state] for candidate in candidates) for state in range(4))
    assert V in candidates
    slacks = [dot(params, features(atom, a, t, c, s))+THETA*V[2*t+c]-V[2*a+t]
              for a, t, c in product((0, 1), repeat=3) for s in range(4)]
    assert min(slacks) >= 0
    psi = tuple((1-THETA)*v for v in V)
    return psi, min(slacks)


def occupation(atoms, tables, duals, budget):
    residual = list(budget)
    witnesses = []
    offset = 0
    for atom, table in zip(atoms, tables):
        probabilities = []
        for state in range(4):
            row = [max(float(v), 0.0) for v in duals[offset:offset+8]]
            offset += 8
            total = sum(row)
            if total > 1e-13:
                row = [F(v/total).limit_denominator(10**9) if v/total > 1e-12 else ZERO for v in row]
                scale = sum(row, ZERO)
                row = [v/scale for v in row]
            else:
                row = [F(i == 0) for i in range(8)]
            assert min(row) >= 0 and sum(row, ZERO) == 1
            probabilities.append(row)
        transition = [[ZERO]*4 for _ in range(4)]
        for state, (a, t) in enumerate(STATES):
            for probability, (c, s) in zip(probabilities[state], ACTIONS):
                transition[state][2*t+c] += probability
        matrix = [[F(i == j)-THETA*transition[j][i] for j in range(4)] for i in range(4)]
        initial = [F(i == 3*atom['b']) for i in range(4)]
        flow = solve_exact(matrix, [(1-THETA)*v for v in initial])
        assert min(flow) >= 0 and sum(flow, ZERO) == 1
        for state in range(4):
            assert flow[state]-THETA*sum(flow[j]*transition[j][state] for j in range(4)) == (1-THETA)*initial[state]
        for j in range(21):
            cost = sum((flow[state]*probabilities[state][action]*table[state][action][j]
                        for state in range(4) for action in range(8)), ZERO)
            residual[j] -= atom['mass']*cost
        witnesses.append({'atom_id': atom['id'], 'mass': str(atom['mass']),
                          'initial': list(map(str, initial)),
                          'action_probabilities': [list(map(str, row)) for row in probabilities],
                          'discounted_state_flow': list(map(str, flow))})
    assert offset == len(duals)
    lower = min(residual)
    return {'parameter_residuals': dict(zip(NAMES, map(str, residual))),
            'parameter_residuals_float': dict(zip(NAMES, map(float, residual))),
            'whole_cone_lower_bound': str(lower), 'lower_bound_float': float(lower),
            'nonseparation_certified': lower >= 0,
            'witnesses': witnesses, 'not_a_common_realizable_SPE_strategy': True}


def main():
    started = time.monotonic()
    data, atoms, utilities, K, Uab, budget = load_data()
    nvar, nrows = 21+4*len(atoms), 32*len(atoms)
    objective = list(map(float, budget))+[0.0]*(nvar-21)
    rr, cc, vv, tables = [], [], [], []
    row_index = 0
    for atom in atoms:
        offset = 21+4*atom['id']
        objective[offset+3*atom['b']] -= float((1-THETA)*atom['mass'])
        table = []
        for state, (a, t) in enumerate(STATES):
            row = []
            for c, s in ACTIONS:
                ft = features(atom, a, t, c, s)
                row.append(ft)
                for j, v in enumerate(ft):
                    if v:
                        rr.append(row_index); cc.append(j); vv.append(-float(v))
                rr += [row_index, row_index]
                cc += [offset+state, offset+2*t+c]
                vv += [1.0, -float(THETA)]
                row_index += 1
            table.append(row)
        tables.append(table)
    assert row_index == nrows
    A = coo_matrix((vv, (rr, cc)), shape=(nrows, nvar)).tocsr()
    normal = coo_matrix(([1.0]*21, ([0]*21, list(range(21)))), shape=(1, nvar)).tocsr()
    lp_spec = {'variables': nvar, 'inequalities': nrows, 'equalities': 1,
               'objective': objective, 'b_ub': [0.0]*nrows, 'b_eq': [1.0],
               'bounds': [[0, None]]*21+[[None, None]]*(nvar-21),
               'method': 'highs-ds',
               'options': {'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9},
               'atom_aggregation': False, 'input_sha256': digest(HERE/'inputs.json')}
    (HERE/'lp_numeric_input.json').write_text(json.dumps(lp_spec, indent=2)+'\n')
    save_npz(HERE/'lp_inequality_matrix.npz', A)
    save_npz(HERE/'lp_normalization_matrix.npz', normal)
    raw_path = HERE/'lp_numeric_output.json'
    if raw_path.exists():
        raw = json.loads(raw_path.read_text())
        assert raw['input_sha256'] == lp_spec['input_sha256']
        assert raw['lp_numeric_input_sha256'] == digest(HERE/'lp_numeric_input.json')
        mode = 'replayed_saved_single_LP'
    else:
        fit = linprog(objective, A_ub=A, b_ub=np.zeros(nrows), A_eq=normal, b_eq=[1.0],
                      bounds=lp_spec['bounds'], method=lp_spec['method'], options=lp_spec['options'])
        assert fit.success, fit.message
        raw = {'input_sha256': lp_spec['input_sha256'],
               'lp_numeric_input_sha256': digest(HERE/'lp_numeric_input.json'),
               'success': bool(fit.success), 'status': int(fit.status), 'message': fit.message,
               'objective': float(fit.fun), 'iterations': int(fit.nit), 'x': fit.x.tolist(),
               'inequality_residuals': fit.ineqlin.residual.tolist(),
               'inequality_marginals': fit.ineqlin.marginals.tolist(),
               'equality_marginals': fit.eqlin.marginals.tolist(),
               'lower_bound_marginals': fit.lower.marginals.tolist(),
               'number_of_optimization_calls': 1}
        raw_path.write_text(json.dumps(raw, indent=2)+'\n')
        mode = 'performed_single_LP'
    assert raw['success'] and raw['number_of_optimization_calls'] == 1
    params = [F(v).limit_denominator(10**7) if v > 1e-12 else ZERO for v in raw['x'][:21]]
    scale = sum(params, ZERO)
    params = [v/scale for v in params]
    atom_table, psi_sum = [], ZERO
    for atom in atoms:
        psi, minimum = bellman_exact(atom, params)
        b, bits = atom['b'], atom['bits']
        coefficient = (params[0]*share(bits[0], b+sum(bits[:5]))
                       +(3*params[1]+params[2])*share(bits[4], b+sum(bits[:5]))
                       +params[19]*atom['L']-psi[3*b])
        psi_sum += atom['mass']*psi[3*b]
        atom_table.append({'atom_id': atom['id'], 'mass': str(atom['mass']),
                           'D_AB': str(atom['D']), 'L_AB': str(atom['L']), 'ybar_AB': str(atom['ybar']),
                           'psi': list(map(str, psi)), 'initial_value': str(psi[3*b]),
                           'customer_coefficient': str(coefficient), 'min_bellman_slack': str(minimum)})
    slack = dot(params, budget)-psi_sum
    capcoef = 3*params[3]+params[4]
    assert sum((F(row['mass'])*F(row['customer_coefficient']) for row in atom_table), ZERO)+K*capcoef == slack
    occ = occupation(atoms, tables, [-v for v in raw['inequality_marginals']], budget)
    assert F(occ['whole_cone_lower_bound']) <= slack
    result = {'schema': 1, 'case': data['case'], 'source': 1, 'theta': '1/2',
              'initial_pair': ['Z', 'Z'], 'remaining': 5, 'middle_count': 3,
              'parameter_names': NAMES, 'parameters': list(map(str, params)),
              'positive_parameters': {n: str(v) for n, v in zip(NAMES, params) if v},
              'normalization': 'All 21 globally nonnegative parameters sum to one.',
              'input_sha256': digest(HERE/'inputs.json'), 'source_sha256': data['source_sha256'],
              'atoms': len(atoms), 'atom_aggregation': False, 'lp_variables': nvar,
              'lp_inequalities': nrows, 'lp_equalities': 1, 'lp_calls': 1,
              'numeric_objective': raw['objective'], 'exact_slack': str(slack),
              'exact_slack_float': float(slack), 'actual_tail_utilities': list(map(str, utilities)),
              'U_AB': str(Uab), 'U_AB_float': float(Uab), 'capacity_mass': str(K),
              'budget_coordinates': list(map(str, budget)), 'capacity_coefficient': str(capcoef),
              'atom_table': atom_table, 'occupation_certificate': occ,
              'negative_row_found': slack < 0, 'not_an_SPE_counterexample': True,
              'execution_mode': mode, 'seconds': time.monotonic()-started}
    (HERE/'single_case_result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('source_sha256', 'atom_table', 'occupation_certificate')}, indent=2))
    print(json.dumps({k: v for k, v in occ.items() if k != 'witnesses'}, indent=2))


if __name__ == '__main__':
    main()
