"""Main: second capacity feedback and a strict global bound, with no LP."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import lcm, gcd
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent


def read(path, expected=None):
    raw = (WS/path).read_bytes()
    if expected:
        assert sha256(raw).hexdigest() == expected
    return json.loads(raw)


def main():
    parent_path = 'main_root30_capacity_feedback/exact_certificate.json'
    parent = read(parent_path, '0256dd3ba234986c95563694c3ef94102f4783f57702b8a64384d3c0e915bdce')
    rho = {int(j): F(value) for j, value in parent['all129_residuals'].items()}
    delta = min(rho[h] for h in range(128) if h & 1 and not ((h >> 3) & 1))
    assert delta == F(1242901025, 57296293387767) > 0
    a, b = F(parent['new_a'])-delta, F(parent['new_b'])+delta
    weights = {name: F(value) for name, value in parent['new_weights'].items()}
    weights['CAP_B4'] += delta
    piK, piO = F(parent['free_mass_multipliers']['K']), F(parent['free_mass_multipliers']['O'])+delta
    original = read('maximal_root_tail_wallet_v2/exact_input.json', '86a235bf210862ef8f8bbbdea7ac324e71f691a8aa7af455a821e6379cfe117d')
    rows = {row['name']: row for row in original['raw_rows']}
    envelope = read('main_thirty_index_strengthening/requery30_envelopes.json', '14ef732b35d0f859113daf92c8dda1f08330413682b057c69a57543a41a360bc')
    residuals = {}
    for h, bits in enumerate(product((0, 1), repeat=7)):
        p, y2, y3, y4, y5, z, o = bits
        D = 1+p+y2+y3+y4
        values = {name: F(row['a'].get(str(h), 0)) for name, row in rows.items()}
        values['PAIR|Omean|Omean'] -= F(o, 36*D*(D+1))
        values['OPT_SOURCE3_REQUERY_CUT'] = F(envelope[h]['cut'])
        r = -sum((weight*values[name] for name, weight in weights.items()), F(0))-piK*p-piO*o
        assert r == rho[h]+delta*(y4-o) >= 0
        residuals[str(h)] = str(r)
    assert 1-sum((weight*F(rows[name]['a'].get('128', 0)) for name, weight in weights.items()), F(0)) == 0
    assert piK+sum((weight*F(rows[name]['bK']) for name, weight in weights.items()), F(0)) == a
    assert piO+sum((weight*F(rows[name]['bO']) for name, weight in weights.items()), F(0)) == b
    residuals['128'] = '0'
    scale = lcm(a.denominator, b.denominator)
    ints = [scale, int(scale*a), int(scale*b)]
    divisor = gcd(gcd(ints[0], ints[1]), ints[2])
    ints = [v//divisor for v in ints]

    inp = read('universal_union_wallet_v6/exact_input.json', '49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936')
    cert = read('universal_union_wallet_v6/exact_certificate.json', '98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d')
    projected, wk = {}, {}
    for atom in inp['atom_columns']:
        aa, o = atom['a'], atom['o']
        total, j = sum(aa), str(atom['index'])
        projected[j] = str((F(aa[0], total) if total else F(0))-b*o)
        wk[j] = str(int(total > 0))
    projected['256'], wk['256'] = str(-a), '-1'
    newrow = {'name': 'ROOT30_B2_B4_CAPACITY_FEEDBACK', 'family': 'ROOT30_CAPACITY_FEEDBACK',
              'a': projected, 'rhs': '0', 'numerical_divisor': '1'}
    input_rows = {row['name']: row for row in inp['raw_rows']}
    oldroot = 'ROOT30_B2_CAPACITY_FEEDBACK'
    lam = {name: F(value) for name, value in cert['dual']['row_weights'].items()}
    beta = lam[oldroot]*delta
    alpha = F(cert['objective'])
    strict = (alpha+beta)/(1+beta)
    assert strict > alpha
    global_residuals = {}
    for j in range(257):
        key = str(j)
        lhs = (1+beta)*F(inp['objective'].get(key, 0))-(alpha+beta)*F(inp['equality']['a'].get(key, 0))
        payment = beta*F(wk[key])
        for name, weight in lam.items():
            assert F(input_rows[name]['rhs']) == 0
            payment += weight*F(projected[key] if name == oldroot else input_rows[name]['a'].get(key, 0))
        r = lhs-payment
        assert r == F(cert['dual']['nonnegative_column_residual'].get(key, 0)) >= 0
        global_residuals[key] = str(r)
    point = {j: F(value) for j, value in cert['primal'].items()}
    violation = sum((F(value)*point.get(j, F(0)) for j, value in projected.items()), F(0))
    assert violation == -delta*(1-F(cert['K'])) < 0
    # Literal W>=K payment: each actual source can force the same maximum C.
    floor_table = []
    for a_bits in product((0, 1), repeat=6):
        floor_res = sum((F(1, sum(a_bits[:i-1])+7-i) for i in range(1, 7)), F(0))-1
        assert floor_res >= 0
        floor_table.append({'actual_bits': list(a_bits), 'residual_on_C': str(floor_res)})
    out = {
        'status': 'PASS_131_ROOT_COLUMNS_257_GLOBAL_COLUMNS_STRICT_UNIVERSAL_BOUND',
        'optimizer_calls': 0, 'parent_certificate_sha256': sha256((WS/parent_path).read_bytes()).hexdigest(),
        'delta': str(delta), 'delta_attaining_types': [h for h in range(128) if h & 1 and not ((h >> 3) & 1) and rho[h] == delta],
        'new_a': str(a), 'new_b': str(b), 'new_integer_line': dict(zip(['u', 'K', 'O'], map(str, ints))),
        'new_weights': {name: str(value) for name, value in weights.items()},
        'free_mass_multipliers': {'K': str(piK), 'O': str(piO)},
        'all129_root_residuals': residuals,
        'new_root_zero_types': [h for h in range(128) if F(residuals[str(h)]) == 0],
        'new_root_row': newrow, 'v6_point_value': str(violation),
        'beta': str(beta), 'old_alpha6': str(alpha), 'strict_alpha': str(strict),
        'strict_alpha_decimal': float(strict), 'strict_gain': str(strict-alpha),
        'global_positive_row_weights': {name: str(value) for name, value in lam.items()},
        'global_payment_replaces': {oldroot: newrow['name']}, 'additional_W_minus_K_weight': str(beta),
        'all257_global_residuals': global_residuals,
        'W_minus_K_true_SAFE_client_residuals': floor_table,
        'scope': 'New root line holds for any six legal queries; strict global bound takes O=OPT6 and pays W-K from all six actual true source ICs.'
    }
    (HERE/'exact_certificate.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
    (HERE/'ROOT30_B2_B4_CAPACITY_FEEDBACK.json').write_text(json.dumps(newrow, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({key: out[key] for key in ['status', 'delta', 'new_integer_line', 'new_root_zero_types', 'strict_alpha', 'strict_alpha_decimal', 'strict_gain', 'v6_point_value']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
