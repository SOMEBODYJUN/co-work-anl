"""Exact exclusion of the entire v2 optimum face; no optimization call."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
import sympy as sp

HERE = Path(__file__).resolve().parent


def main():
    base = HERE / 'universal_union_wallet_v2'
    ip, cp = base / 'exact_input.json', base / 'exact_certificate.json'
    assert sha256(ip.read_bytes()).hexdigest() == 'bb7c66e141b9ab6080c5fbafe6c00f966a95247269ff54d2ae3abae7809f35f2'
    assert sha256(cp.read_bytes()).hexdigest() == '12d4f059b7be021c8b3c89ed6adf3bde208750da6ce0eee79c383a813d50b36b'
    data, cert = json.loads(ip.read_text()), json.loads(cp.read_text())
    rows = {r['name']: r for r in data['raw_rows']}
    lam = {k: F(v) for k, v in cert['dual']['row_weights'].items()}
    assert len(lam) == 10 and min(lam.values()) > 0
    names = list(lam)
    h = {j: F(cert['dual']['nonnegative_column_residual'].get(str(j), '0')) for j in range(257)}
    zeros = [j for j in range(257) if h[j] == 0]
    assert zeros == [0, 1, 3, 7, 9, 11, 21, 25, 37, 165, 229, 241, 256]
    selected = [data['equality']] + [rows[k] for k in names]
    matrix = sp.Matrix([[sp.Rational(r['a'].get(str(j), '0')) for j in zeros] for r in selected])
    rank = matrix.rank()
    assert rank == 11
    objective = {int(k): F(v) for k, v in data['objective'].items()}
    union = {int(k): F(v) for k, v in data['equality']['a'].items()}

    def identity(target):
        solution, parameters = matrix.T.gauss_jordan_solve(sp.Matrix([sp.Rational(target.get(j, 0)) for j in zeros]))
        assert parameters.rows == 0
        coefficients = [F(str(v)) for v in solution]
        remainder = {
            j: target.get(j, F(0)) - sum((coefficients[k] * F(r['a'].get(str(j), '0')) for k, r in enumerate(selected)), F(0))
            for j in range(257)
        }
        assert all(remainder[j] == 0 for j in zeros)
        assert all(h[j] > 0 for j, v in remainder.items() if v)
        return coefficients, remainder

    kcoef, krem = identity({256: F(1)})
    assert kcoef[0] == F(cert['K'])
    J = {}
    for atom in data['atom_columns']:
        j, bits = atom['index'], atom['a']
        c = sum(bits)
        J[j] = 67140 * (F(bits[0], c) if c else F(0)) - 627 * atom['o']
    J[256] = F(-9878)
    jcoef, jrem = identity(J)
    ell = jcoef[0]
    assert ell == F(-2694628988940630887460, 52739368771603064323)
    ar = dict(zip(names, jcoef[1:]))
    ratios = [(lam[k] / v, 'row:' + k) for k, v in ar.items() if v > 0]
    ratios += [(h[j] / v, 'column:' + str(j)) for j, v in jrem.items() if v > 0]
    gamma = min(v for v, _ in ratios)
    assert gamma > 0
    alpha = F(cert['objective'])
    bound = alpha - gamma * ell
    newlam = {k: lam[k] - gamma * ar[k] for k in names}
    newh = {j: h[j] - gamma * jrem[j] for j in range(257)}
    assert min(newlam.values()) >= 0 and min(newh.values()) >= 0
    for j in range(257):
        rhs = gamma * J.get(j, F(0)) + sum((v * F(rows[k]['a'].get(str(j), '0')) for k, v in newlam.items()), F(0)) + newh[j]
        assert rhs == objective.get(j, F(0)) - bound * union.get(j, F(0))

    def pack(coef, rem):
        return {'normalization_coefficient': str(coef[0]),
                'row_coefficients': {k: str(v) for k, v in zip(names, coef[1:])},
                'forced_zero_column_coefficients': {str(j): str(v) for j, v in rem.items() if v}}

    result = {
        'status': 'PASS_ENTIRE_V2_OPTIMUM_FACE_EXCLUDED', 'optimizer_calls': 0,
        'input_sha256': sha256(ip.read_bytes()).hexdigest(),
        'certificate_sha256': sha256(cp.read_bytes()).hexdigest(),
        'scope': 'Original full256-type 219-row necessary system, every normalized optimum',
        'positive_dual_row_names': names, 'zero_residual_columns': zeros,
        'restricted_rank': rank, 'restricted_affine_dimension': len(zeros) - rank,
        'K_identity': pack(kcoef, krem), 'ROOT_SIZE_identity': pack(jcoef, jrem),
        'ROOT_SIZE_coefficients': {str(j): str(v) for j, v in J.items() if v},
        'K_constant_on_entire_optimum_face': str(kcoef[0]),
        'ROOT_SIZE_constant_on_entire_optimum_face': str(ell),
        'constructive_strict_bound': {
            'old_bound': str(alpha), 'gamma': str(gamma), 'bound': str(bound),
            'bound_decimal': float(bound), 'improvement': str(bound - alpha),
            'binding_ratios': [label for value, label in ratios if value == gamma],
            'old_row_weights': {k: str(v) for k, v in newlam.items() if v},
            'new_root_size_weight': str(gamma),
            'nonnegative_column_residual': {str(j): str(v) for j, v in newh.items() if v},
            'matching_primal_claimed': False, 'best_known_bound_claimed': False,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
