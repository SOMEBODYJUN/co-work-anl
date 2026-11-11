"""Main exact replay of all221 rows and all257 columns, no optimization."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent


def main():
    p = HERE / 'universal_union_wallet_v3'
    ip, cp = p / 'exact_input.json', p / 'exact_certificate.json'
    assert sha256(ip.read_bytes()).hexdigest() == 'd5808676b4a59bc9a63deece83e291887ead8847a7177c3afac4221523f30f55'
    assert sha256(cp.read_bytes()).hexdigest() == '1d9a898e3ca429b6af3611f01ada831ad50cf7f0708f14d7c518478573f0a9e3'
    a, c = json.loads(ip.read_text()), json.loads(cp.read_text())
    prior = json.loads((HERE / 'universal_union_wallet_v2/exact_input.json').read_text())
    assert a['raw_rows'][:219] == prior['raw_rows']
    assert a['atom_columns'] == prior['atom_columns'] and len(a['atom_columns']) == 256
    assert a['equality'] == prior['equality'] and a['objective'] == prior['objective']
    rows = {r['name']: r for r in a['raw_rows']}
    assert len(rows) == 221
    for name, A, B, C in [('ROOT_SIZE_FEEDBACK', 67140, 9878, 627),
                          ('ROOT_TRUE_TAIL', 112944305160, 11595684007, 2178783435)]:
        row = rows[name]
        for atom in a['atom_columns']:
            j, bits = atom['index'], atom['a']
            load = sum(bits)
            expected = A * (F(bits[0], load) if load else F(0)) - C * atom['o']
            assert F(row['a'].get(str(j), '0')) == expected
        assert F(row['a'].get('256', '0')) == -B and F(row['rhs']) == 0
    x = {int(j): F(v) for j, v in c['primal'].items()}
    assert all(v >= 0 for v in x.values())
    def dot(v):
        return sum((F(q) * x.get(int(j), F(0)) for j, q in v.items()), F(0))
    eq = a['equality']
    assert dot(eq['a']) == F(eq['rhs']) == 1
    slacks = {k: dot(r['a']) - F(r['rhs']) for k, r in rows.items()}
    assert min(slacks.values()) >= 0
    assert all(slacks[k] == F(v) for k, v in c['raw_row_slacks'].items())
    obj = dot(a['objective'])
    assert obj == F(c['objective']) == F(999866079286562265469481, 2318932167377271341801106)
    d = c['dual']
    lam = {k: F(v) for k, v in d['row_weights'].items()}
    nu = F(d['normalization_multiplier'])
    assert len(lam) == 10 and min(lam.values()) > 0
    residuals = []
    for j in range(257):
        k = str(j)
        r = F(a['objective'].get(k, '0')) - nu * F(eq['a'].get(k, '0'))
        r -= sum((v * F(rows[n]['a'].get(k, '0')) for n, v in lam.items()), F(0))
        assert r >= 0 and r == F(d['nonnegative_column_residual'].get(k, '0'))
        assert r * x.get(j, F(0)) == 0
        residuals.append(r)
    assert nu * F(eq['rhs']) + sum((v * F(rows[k]['rhs']) for k, v in lam.items()), F(0)) == obj
    assert all(slacks[k] == 0 for k in lam)
    assert 'ROOT_TRUE_TAIL' in lam and 'TRUE_X_TAIL_CUT' in lam and 'K_ge_size_6' in lam
    assert slacks['ROOT_SIZE_FEEDBACK'] > 0 and 'ROOT_SIZE_FEEDBACK' not in lam
    out = {
        'status': 'PASS_ALL_221_ROWS_257_COLUMNS_AND_NEW_ROOT_FORMULAS',
        'optimizer_calls': 0, 'scope': 'Main exact matrix replay; real-history source derivations separately reviewed',
        'input_sha256': sha256(ip.read_bytes()).hexdigest(), 'certificate_sha256': sha256(cp.read_bytes()).hexdigest(),
        'old219_rows_identical': True, 'all_original_rows': 221, 'all_nonnegative_columns': 257,
        'positive_primal_atoms': len(x) - 1, 'positive_dual_rows': len(lam),
        'positive_customer_residuals': sum(r > 0 for r in residuals[:256]),
        'zero_residual_columns': [j for j, r in enumerate(residuals) if r == 0], 'K_residual': str(residuals[256]),
        'objective': str(obj), 'objective_decimal': float(obj), 'half_gap': str(F(1, 2) - obj), 'K': c['K'],
        'root_size_slack': str(slacks['ROOT_SIZE_FEEDBACK']),
        'released_for_precise_new_obligations': True,
        'not_claimed': ['complete SPE realization', 'half coverage', 'best-known bound'],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
