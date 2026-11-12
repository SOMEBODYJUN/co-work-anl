"""Main's independent full3056 certificate, complete face, and real C budgets.

No optimizer, producer imports, support truncation, or changes to frozen inputs.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json
import sympy as sp

W = Path(__file__).resolve().parent
P = W / 'visible_maximum_joint_v5_solve'
ATOMS = list(product((0, 1), repeat=9))


def load(p):
    return json.loads(p.read_text())


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def dot(a, x):
    return sum((F(v) * x[int(h)] for h, v in a.items()), F(0))


def true_cost(p, t, o, tail, tau, beta, a):
    load_ = p + t + sum(tail)
    numerator = a*t - tail[3] - sum(tau[j]*tail[j] for j in range(3))
    assert load_ or numerator == 0
    cost = numerator/load_ if load_ else F(0)
    cost += sum(beta[j]*tail[j] for j in range(3)) + tail[3]
    cost += F(o, 6*(p+t+sum(tail[:3])+1))
    cost += sum((tau[j]*F(o, 6*(p+t+sum(tail[:j])+4-j)) for j in range(3)), F(0))
    return cost


def main():
    out = W / 'main_visible_c_v5_certificate_check.json'
    assert not out.exists()
    ip = W / 'visible_maximum_joint_v5/exact_input.json'
    cp = P / 'exact_certificate.json'
    fp = P / 'optimal_face.json'
    assert digest(ip) == '12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac'
    assert digest(cp) == 'c29c711bdbfeac80265c8806b1a76e8e5810277c2a11801335d35cc4f3bdb265'
    assert digest(fp) == '0109e4155fd1db271e1c10634cee6c430b3ff2bcaebf288fe305d90d2d5a5e2d'
    inp, cert, face = load(ip), load(cp), load(fp)
    rows, eqs = inp['raw_rows'], inp['equalities']
    primal = list(map(F, cert['primal']))
    ys = list(map(F, cert['dual']['raw_row_weights']))
    eta = list(map(F, cert['dual']['equality_multipliers']))
    residual = list(map(F, cert['dual']['nonnegative_column_residual']))
    assert len(rows) == len(ys) == 3056
    assert len(primal) == len(residual) == 513 and len(eqs) == len(eta) == 2
    assert min(primal) >= 0 and min(ys) >= 0 and min(residual) >= 0
    pos = [k for k, y in enumerate(ys) if y]
    assert pos == [46, 47, 134, 218, 221, 868, 1803, 2563, 2564, 2606]
    for k, row in enumerate(rows):
        slack = dot(row['a'], primal) - F(row['rhs'])
        assert slack == F(cert['raw_row_slacks'][k]) >= 0
        assert slack * ys[k] == 0
    for eq in eqs:
        assert dot(eq['a'], primal) == F(eq['rhs'])
    for h in range(513):
        r = F(inp['objective'].get(str(h), '0'))
        r -= sum((ys[k]*F(rows[k]['a'].get(str(h), '0')) for k in pos), F(0))
        r -= sum((v*F(eq['a'].get(str(h), '0')) for v, eq in zip(eta, eqs)), F(0))
        assert r == residual[h] and r*primal[h] == 0
    alpha = dot(inp['objective'], primal)
    dual = sum((ys[k]*F(rows[k]['rhs']) for k in pos), F(0))
    dual += sum((v*F(eq['rhs']) for v, eq in zip(eta, eqs)), F(0))
    assert alpha == dual == F(cert['objective'])
    zero = [h for h, r in enumerate(residual) if not r]
    assert zero == face['zero_residual_columns']
    assert zero == [0, 2, 3, 14, 15, 18, 19, 22, 23, 50, 51, 74, 75, 331, 459, 483, 499, 512]
    assert [h for h in range(513) if h not in zero] == face['forced_zero_columns']
    equations = eqs + [rows[k] for k in pos]
    rhs = list(map(F, face['equation_rhs']))
    assert rhs == [F(eq['rhs']) for eq in equations]
    matrix = [[F(eq['a'].get(str(h), '0')) for h in zero] for eq in equations]
    assert sp.Matrix(matrix).rank() == 12
    coords = {r['column']: [F(r['constant'])] + list(map(F, r['parameter_coefficients'])) for r in face['coordinates']}
    assert sorted(coords) == zero and all(len(v) == 7 for v in coords.values())
    for q in range(7):
        for row, b in zip(matrix, rhs):
            assert sum((v*coords[h][q] for v, h in zip(row, zero)), F(0)) == (b if q == 0 else 0)
    assert sp.Matrix([[coords[h][q] for q in range(1, 7)] for h in zero]).rank() == 6
    assert len(face['all_raw_inequality_restrictions']) == 3056
    for row, rec in zip(rows, face['all_raw_inequality_restrictions']):
        want = [sum((F(row['a'].get(str(h), '0'))*coords[h][q] for h in zero), F(0))
                - (F(row['rhs']) if q == 0 else 0) for q in range(7)]
        assert want == [F(rec['constant'])] + list(map(F, rec['parameter_coefficients']))
    assert len(face['all513_nonnegative_coordinate_restrictions']) == 513
    for h, rec in enumerate(face['all513_nonnegative_coordinate_restrictions']):
        assert rec['column'] == h and rec['forced_zero'] == (h not in zero)
        assert [F(rec['constant'])] + list(map(F, rec['parameter_coefficients'])) == coords.get(h, [F(0)]*7)

    # Reconstruct every real source wallet at the four new positive raw rows.
    tauC = (F(0), F(5977, 6912), F(43, 48))
    source_specs = [(1803, tauC, F(61273, 6912), 8, True),
                    (2563, (F(0), F(0), F(8, 9)), F(9), 4, False),
                    (2564, (F(0), F(0), F(8, 9)), F(9), 5, False),
                    (2606, tauC, F(0), 8, False)]
    zeros = {}; states = 0; real_columns = 0; weight_records = []
    for raw, tau, s, target, conly in source_specs:
        beta = tuple(F(1, 12) + tau[j] + sum((tau[l]/(6*(4-l)*(5-l)) for l in range(j+1, 3)), F(0)) for j in range(3))
        a, S = 25 + sum(tau) - s, 1 + sum(beta)
        assert a > 0 and min(beta) > 0 and min(tau) >= 0
        minima = {}
        for p, t, o in product((0, 1), repeat=3):
            vals = {tail: true_cost(p, t, o, tail, tau, beta, a) for tail in product((0, 1), repeat=4)}
            states += len(vals)
            mv = min(vals.values()); minima[p, t, o] = mv
            anchor = t*(S + F(24, p+5) - s/5) + F(o, 6*(p+4*t+1))
            anchor += sum((tau[j]*F(o, 6*(p+(j+1)*t+4-j)) for j in range(3)), F(0))
            assert mv == anchor
            zeros[raw, p, t, o] = {tail for tail, v in vals.items() if v == mv}
        for h in range(513):
            ec = F(eqs[1]['a'].get(str(h), '0'))
            if h == 512:
                val = S
            else:
                bits = ATOMS[h]; load_ = sum(bits[:6])
                u2 = F(bits[1], load_) if load_ else F(0)
                val = a*u2-minima[bits[0], bits[target], bits[7]]
            if conly:
                val += (S-s/5)*ec
            assert val == F(rows[raw]['a'].get(str(h), '0')), (raw, h)
            real_columns += 1
        weight_records.append({'raw': raw, 'tau': list(map(str, tau)), 's': str(s),
                               'a': str(a), 'beta': list(map(str, beta)), 'S': str(S)})
    common = []
    for p, c, o in product((0, 1), repeat=3):
        tails = sorted(zeros[1803, p, c, o] & zeros[2606, p, c, o])
        assert tails
        if c and o:
            assert tails == ([(1, 1, 1, 1)] if not p else [(1, 1, 1, 0)])
            assert zeros[1803, p, c, o] == set(tails)
        common.append({'pco': [p, c, o], 'all_common_weak_tails': list(map(list, tails))})
    assert zeros[1803, 1, 1, 0] & zeros[2606, 1, 1, 0] == {(1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, 0)}

    functionals = {}
    for h in range(513):
        if h == 512:
            K = F(1); u2 = co = oo = om = F(0); N = {j: F(0) for j in range(3, 6)}
        else:
            bits = ATOMS[h]; p, c, o = bits[0], bits[8], bits[7]
            K = F(0); load_ = sum(bits[:6]); u2 = F(bits[1], load_) if load_ else F(0)
            co, oo, om = F(c*(1-o)), F(o*(1-c)), F(o)
            N = {j: F(o, 6*(p+(j-2)*c+7-j)) for j in range(3, 6)}
            assert N[5]-N[4] == F(o*(1-c), 6*(p+2)*(p+3))
        values = {'K': K, 'C_outside_O_mass': co, 'O_outside_C_mass': oo,
                  'u2_minus_K_over5_from_new_C_pair': u2-K/5,
                  **{f'K_over5_minus_N{j}': K/5-N[j] for j in range(3, 6)},
                  'N5_minus_N4': N[5]-N[4], 'N5_minus_N4_minus_OneMinusK_over36': N[5]-N[4]-(om-K)/36}
        for name, value in values.items():
            functionals.setdefault(name, []).append(value)
        ec = F(eqs[1]['a'].get(str(h), '0'))
        assert F(rows[1803]['a'].get(str(h), '0')) - F(rows[2606]['a'].get(str(h), '0')) == F(61273, 6912)*(K/5-u2)+F(1528993, 497664)*ec
    fixed = {}
    for name, cs in functionals.items():
        vals = [sum((cs[h]*coords[h][q] for h in zero), F(0)) for q in range(7)]
        assert all(v == 0 for v in vals[1:]), name
        fixed[name] = str(vals[0])
    for rec in load(P/'true_branch_face_functionals.json')['functionals']:
        name = rec['name']; cs = functionals[name]
        assert all(F(rec['full_coefficients'].get(str(h), '0')) == cs[h] for h in range(513))
        weights = list(map(F, rec['signed_face_equation_weights']))
        extras = {int(h): F(v) for h, v in rec['signed_forced_zero_column_weights'].items()}
        assert all(h not in zero for h in extras)
        for h in range(513):
            assert cs[h] == sum((v*F(row['a'].get(str(h), '0')) for v, row in zip(weights, equations)), F(0))+extras.get(h, F(0))
        assert F(rec['constant']) == sum((v*b for v, b in zip(weights, rhs)), F(0)) == F(fixed[name])
    assert F(fixed['C_outside_O_mass']) == F(fixed['u2_minus_K_over5_from_new_C_pair']) == 0
    assert F(fixed['K_over5_minus_N3']) > 0
    assert F(fixed['K_over5_minus_N4']) < 0 and F(fixed['K_over5_minus_N5']) < 0
    assert F(fixed['O_outside_C_mass']) == 1-F(fixed['K']) > 0
    assert F(fixed['N5_minus_N4_minus_OneMinusK_over36']) == 0
    assert F(fixed['N5_minus_N4']) > 0
    report = {'status': 'PASS_MAIN_FULL3056_RAW513_DUAL_FULL_FACE_AND_FRESH_TRUE_C_BRANCH',
              'optimizer_calls': 0, 'input_sha256': digest(ip), 'certificate_sha256': digest(cp),
              'face_sha256': digest(fp), 'proof_sha256': digest(P/'proof.md'),
              'source_proof_personally_read_complete': True, 'raw_rows': 3056, 'nonnegative_columns': 513,
              'equalities': 2, 'alpha': str(alpha), 'alpha_decimal': float(alpha),
              'positive_raw_dual_indices': pos, 'all_zero_residual_columns': zero,
              'restricted_rank': 12, 'affine_parameter_count': 6,
              'true_wallet_hidden_states': states, 'true_wallet_all_columns': real_columns,
              'current_positive_source_weights': weight_records,
              'all_common_weak_zero_states': common, 'fixed_functionals': fixed,
              'signed_face_identity_columns': 6*513,
              'scope': 'Exact universal necessary-cone welfare bound; entire optimum face cannot be a complete-history pure SPE. No half theorem, no SPE counterexample, no optimizer rerun.'}
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ['current_positive_source_weights', 'all_common_weak_zero_states', 'scope']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
