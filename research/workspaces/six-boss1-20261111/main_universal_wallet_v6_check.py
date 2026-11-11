"""Main independently replays v6 and rebuilds all P25 visible coefficients."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent


def main():
    ip = HERE / 'universal_union_wallet_v6/exact_input.json'
    cp = HERE / 'universal_union_wallet_v6/exact_certificate.json'
    assert sha256(ip.read_bytes()).hexdigest() == '49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936'
    assert sha256(cp.read_bytes()).hexdigest() == '98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d'
    inp, cert = json.loads(ip.read_text()), json.loads(cp.read_text())
    old = json.loads((HERE / 'universal_union_wallet_v5/exact_input.json').read_text())
    assert inp['raw_rows'][:546] == old['raw_rows']
    for key in ['atom_columns', 'objective', 'equality', 'K_column', 'nonnegative_columns']:
        assert inp[key] == old[key]
    rows = {r['name']: r for r in inp['raw_rows']}
    assert len(rows) == 867

    # Derive the entire new visible family directly from the proved local minimum.
    checks = 0
    for i in range(1, 6):
        n = 6-i
        cap = F(n+1, 2)
        for T in range(1, 9):
            for Q in range(1, 9):
                row = rows[f'PORTFOLIO25_i{i}_T{T}_Q{Q}']
                assert F(row['rhs']) == 0
                for v in range(256):
                    bits = [(v >> (7-k)) & 1 for k in range(8)]
                    a, x, o = bits[:6], bits[6], bits[7]
                    p, total = sum(a[:i-1]), sum(a)
                    A = cap + F(24, p+n+1)
                    B = F(1, p+1)
                    C = F(n, (p+1)*(p+n+1))
                    labels = a + [x]
                    if T == Q == 8:
                        cost = F(o, 6)*(A+B)
                    elif T == 8:
                        q = labels[Q-1]
                        cost = B*q+F(o, 6)*(A-C*q)
                    elif Q == 8:
                        t = labels[T-1]
                        cost = A*t+F(o, 6)*(B-C*t)
                    else:
                        t, q = labels[T-1], labels[Q-1]
                        cost = A*t+B*q-C*t*q
                    coefficient = (F(25*a[i-1], total) if total else F(0))-cost
                    assert coefficient == F(row['a'].get(str(v), 0)), (i, T, Q, v)
                    checks += 1
                assert F(row['a'].get('256', 0)) == cap
                checks += 1
    root = json.loads((HERE / 'main_root30_capacity_feedback/ROOT30_B2_CAPACITY_FEEDBACK.json').read_text())
    actual = rows[root['name']]
    assert F(actual['rhs']) == 0
    assert all(F(actual['a'].get(str(j), 0)) == F(root['a'].get(str(j), 0)) for j in range(257))

    point = {str(j): F(cert['primal'].get(str(j), 0)) for j in range(257)}
    assert min(point.values()) >= 0
    def dot(a):
        return sum((F(c)*point[j] for j, c in a.items()), F(0))
    assert dot(inp['equality']['a']) == F(inp['equality']['rhs']) == 1
    slacks = {name: dot(row['a'])-F(row['rhs']) for name, row in rows.items()}
    assert all(s >= 0 and s == F(cert['raw_row_slacks'][name]) for name, s in slacks.items())
    objective = dot(inp['objective'])
    assert objective == F(cert['objective'])
    dual = cert['dual']
    weights = {name: F(value) for name, value in dual['row_weights'].items()}
    assert len(weights) == 12 and min(weights.values()) > 0
    nu = F(dual['normalization_multiplier'])
    residuals = []
    for j in range(257):
        key = str(j)
        residual = F(inp['objective'].get(key, 0))-nu*F(inp['equality']['a'].get(key, 0))
        residual -= sum((weight*F(rows[name]['a'].get(key, 0)) for name, weight in weights.items()), F(0))
        assert residual == F(dual['nonnegative_column_residual'].get(key, 0)) >= 0
        assert residual*point[key] == 0
        residuals.append(residual)
    assert nu*F(inp['equality']['rhs'])+sum((weight*F(rows[name]['rhs']) for name, weight in weights.items()), F(0)) == objective
    assert all(slacks[name] == 0 for name in weights)
    out = {
        'status': 'PASS_MAIN_ALL867_ROWS257_COLUMNS_AND_INDEPENDENT_P25_REBUILD',
        'optimizer_calls': 0,
        'input_sha256': sha256(ip.read_bytes()).hexdigest(),
        'certificate_sha256': sha256(cp.read_bytes()).hexdigest(),
        'old546_rows_identical': True, 'source25_coefficients_checked': checks,
        'root_feedback_coefficients_checked': 257, 'raw_rows': 867, 'columns': 257,
        'objective': str(objective), 'objective_decimal': float(objective), 'K': cert['K'],
        'positive_budget_weights': {name: str(value) for name, value in weights.items()},
        'positive_primal_atoms': [j for j in range(256) if point[str(j)] > 0],
        'zero_residual_columns': [j for j, value in enumerate(residuals) if value == 0],
        'released_for_precise_new_obligations': True,
        'not_claimed': ['complete SPE realization', 'half coverage', 'whole optimum-face exclusion']
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
