"""Main checks the root270 certificate and pays a new full-type global bound."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent


def load(name, expected):
    path = WS/name
    assert sha256(path.read_bytes()).hexdigest() == expected
    return json.loads(path.read_text())


def main():
    inp = load('maximal_root_tail_wallet_v3/exact_input.json', '01c57b65a82b682d222cb449407416c4db0de60961c90d6eaafd35d15b1f79d0')
    cert = load('maximal_root_tail_wallet_v3/exact_certificate.json', 'b7d27bcddc6da34bed635bf7c36a607ffea130b56bcb0f62803b94b3c20dc925')
    rows = {row['name']: row for row in inp['raw_rows']}
    assert len(rows) == 270
    K, O = F(inp['fixed_K']), F(inp['fixed_O'])
    point = {str(j): F(cert['primal'].get(str(j), 0)) for j in range(129)}
    assert min(point.values()) >= 0
    def dot(a):
        return sum((F(value)*point[j] for j, value in a.items()), F(0))
    for eq in inp['equalities']:
        assert dot(eq['a']) == F(eq['rhs'])
    for name, row in rows.items():
        assert F(row['rhs']) == F(row['bK'])*K+F(row['bO'])*O
        slack = dot(row['a'])-F(row['rhs'])
        assert slack == F(cert['raw_unscaled_row_slacks'][name]) >= 0
    dual = cert['dual']
    weights = {name: F(value) for name, value in dual['original_unscaled_row_weights'].items()}
    assert len(weights) == 10 and min(weights.values()) > 0
    assert weights.get('BRANCH_UNION_OPT', F(0)) == 0
    piK, piO = F(dual['equality_C_size']), F(dual['equality_OPT_union'])
    eqK, eqO = inp['equalities']
    for j in range(129):
        key = str(j)
        residual = F(inp['objective'].get(key, 0))-piK*F(eqK['a'].get(key, 0))-piO*F(eqO['a'].get(key, 0))
        residual -= sum((weight*F(rows[name]['a'].get(key, 0)) for name, weight in weights.items()), F(0))
        assert residual == F(dual['column_residuals'].get(key, 0)) >= 0
        assert residual*point[key] == 0
    assert all(F(cert['raw_unscaled_row_slacks'][name]) == 0 for name in weights)
    a = piK+sum((weight*F(rows[name]['bK']) for name, weight in weights.items()), F(0))
    b = piO+sum((weight*F(rows[name]['bO']) for name, weight in weights.items()), F(0))
    assert a == F(cert['universal_root_line']['a']) and b == F(cert['universal_root_line']['b'])
    assert a*K+b*O == dot(inp['objective']) == F(cert['objective'])

    # Rebuild the newly positive P25 row directly from the true source formula.
    p25 = rows['PORTFOLIO25_i4|T=B6|Q=Omean']
    for h in range(128):
        bits = [(h >> (6-k)) & 1 for k in range(7)]
        ell, o = bits[:6], bits[6]
        total, p, t = sum(ell), sum(ell[:3]), ell[5]
        coefficient = (F(25*ell[3], total) if total else F(0))-(F(3, 2)+F(24, p+3))*t-F(o, 6*(p+1+2*t))
        assert coefficient == F(p25['a'].get(str(h), 0))
    assert F(p25['bK']) == -F(3, 2) and F(p25['bO']) == 0

    glob = load('universal_union_wallet_v6/exact_input.json', '49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936')
    gc = load('universal_union_wallet_v6/exact_certificate.json', '98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d')
    oldroot = load('main_root30_capacity_feedback/exact_certificate.json', '0256dd3ba234986c95563694c3ef94102f4783f57702b8a64384d3c0e915bdce')
    da, db = a-F(oldroot['new_a']), b-F(oldroot['new_b'])
    assert da > 0 and db < 0
    epsilon = da/6+db
    assert epsilon > 0
    gw = {name: F(value) for name, value in gc['dual']['row_weights'].items()}
    rootname = 'ROOT30_B2_CAPACITY_FEEDBACK'
    rootweight = gw[rootname]
    alpha = F(gc['objective'])+rootweight*epsilon
    newcoef, kfloor = {}, {}
    for atom in glob['atom_columns']:
        aa, o, key = atom['a'], atom['o'], str(atom['index'])
        total = sum(aa)
        newcoef[key] = str((F(aa[0], total) if total else F(0))-b*o)
        kfloor[key] = str(-F(o, 6))
    newcoef['256'], kfloor['256'] = str(-a), '1'
    newrow = {'name': 'ROOT270_TRUE_BRANCH_P25', 'family': 'TRUE_MAXIMUM_ROOT270',
              'a': newcoef, 'rhs': '0', 'numerical_divisor': '1'}
    global_rows = {row['name']: row for row in glob['raw_rows']}
    gres = {}
    for j in range(257):
        key = str(j)
        lhs = F(glob['objective'].get(key, 0))-alpha*F(glob['equality']['a'].get(key, 0))
        payment = rootweight*da*F(kfloor[key])
        for name, weight in gw.items():
            assert F(global_rows[name]['rhs']) == 0
            payment += weight*F(newcoef[key] if name == rootname else global_rows[name]['a'].get(key, 0))
        residual = lhs-payment
        assert residual == F(gc['dual']['nonnegative_column_residual'].get(key, 0)) >= 0
        gres[key] = str(residual)
    out = {
        'status': 'PASS_MAIN_ROOT270_ALL_ROWS129_COLUMNS131_PARAMETERS_AND_STRICT_GLOBAL257_IDENTITY',
        'optimizer_calls': 0, 'root_input_sha256': cert['input_sha256'],
        'root_certificate_sha256': 'b7d27bcddc6da34bed635bf7c36a607ffea130b56bcb0f62803b94b3c20dc925',
        'root_raw_rows_checked': 270, 'root_columns_checked': 129, 'independent_parameter_columns_checked': 2,
        'new_positive_P25_customer_coefficients_rebuilt': 128,
        'root_a': str(a), 'root_b': str(b), 'root_objective': cert['objective'],
        'branch_union_OPT_weight': '0', 'root_line_allows_any_six_legal_query_union': True,
        'delta_a': str(da), 'delta_b': str(db), 'epsilon_on_K_at_least_O_over_6': str(epsilon),
        'old_alpha6': gc['objective'], 'new_alpha': str(alpha), 'new_alpha_decimal': float(alpha),
        'new_gain': str(alpha-F(gc['objective'])), 'new_gain_decimal': float(alpha-F(gc['objective'])),
        'new_root_row': newrow, 'additional_K_minus_O_over6_row': kfloor,
        'additional_K_minus_O_over6_weight': str(rootweight*da),
        'all257_global_residuals': gres,
        'global_row_weights': {name: str(weight) for name, weight in gw.items()},
        'global_row_replacement': {rootname: newrow['name']},
        'not_claimed': ['new global LP optimum', 'SPE realization', 'half coverage']
    }
    (HERE/'exact_certificate.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    (HERE/'ROOT270_TRUE_BRANCH_P25.json').write_text(json.dumps(newrow, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({key: out[key] for key in ['status', 'delta_a', 'delta_b', 'epsilon_on_K_at_least_O_over_6', 'new_alpha', 'new_alpha_decimal', 'new_gain_decimal']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
