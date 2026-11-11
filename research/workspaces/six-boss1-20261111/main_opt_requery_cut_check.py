"""Main literal nine-wallet check and direct actual-history application; no LP."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from itertools import product
import json

HERE = Path(__file__).resolve().parent


def main():
    folder = HERE / 'maximal_root_opt_requery'
    cp = folder / 'exact_certificate.json'
    assert sha256(cp.read_bytes()).hexdigest() == '209959db4dfce6ba4fe796eeb168b8ab71f186f795e0599f9148d08ceaa8b13e'
    cert = json.loads(cp.read_text())
    cut = {}
    tables = []
    positive = zero = 0
    for h, bits in enumerate(product((0, 1), repeat=7)):
        p, y2, y3, y4, y5, z, o = bits
        old_load = p + y2 + y3 + y4 + y5 + z
        b = p + y2
        costs = {}
        for q, s4, s5, s6 in product((0, 1), repeat=4):
            D = 1 + b + q + s4
            new_v5 = F(s5, D + s6)
            new_v6 = F(s6, D + s5)
            value = 126000 * F(q, b + 1 + s4 + s5 + s6)
            value += F(43 * s4 + 31218 * s5 + 34458 * s6, b + y3 + 3)
            value += F(1654 * (s4 + s5 + s6), b + y3 + y4 + y5 + 1)
            value += 5400 * (F(o, 6 * (D + s5)) - new_v6)
            pair_cost = F(o, 3 * D) - F(o, 36 * D * (D + 1))
            pair_wallet = new_v5 + new_v6 + F(s5, D * (D + 1))
            value += 7740 * (pair_cost - pair_wallet)
            costs[(q, s4, s5, s6)] = value
        a0 = min(value for state, value in costs.items() if state[0] == 0)
        a1 = min(value for state, value in costs.items() if state[0] == 1)
        delta, gamma = max(a1 - a0, F(0)), max(a0 - a1, F(0))
        assert delta > 0 and gamma == 0
        m = a0 + delta * F(o, 6) - gamma * o
        assert m == (a0 if o == 0 else min((5 * a0 + a1) / 6, a1))
        for state, value in costs.items():
            residual = value + (gamma - delta) * state[0] - a0
            assert residual >= 0
            positive += residual > 0
            zero += residual == 0
        wallet = F(126000 * y3 + 65719 * y4 + 4962 * z, old_load) if old_load else F(0)
        cut[h] = wallet - m
        assert cut[h] == F(cert['universal_cut']['cut_z'][str(h)])
        tables.append({'h': h, 'bits': list(bits), 'a0': str(a0), 'a1': str(a1),
                       'm': str(m), 'delta': str(delta), 'gamma': str(gamma), 'cut': str(cut[h])})
    assert cert['universal_cut']['cut_K'] in [0, '0']
    assert cert['universal_cut']['cut_u'] in [0, '0']
    evaluations = {}
    for name in ['universal_union_wallet_lp', 'universal_union_wallet_v2', 'universal_union_wallet_v3']:
        p = HERE / name
        data = json.loads((p / 'exact_input.json').read_text())
        exact = json.loads((p / 'exact_certificate.json').read_text())
        value = F(0)
        mapped = {}
        for atom in data['atom_columns']:
            sixbits = atom['a']
            h = 0
            for bit in sixbits + [atom['o']]:
                h = 2 * h + bit
            mapped[str(atom['index'])] = str(cut[h])
            value += cut[h] * F(exact['primal'].get(str(atom['index']), '0'))
        evaluations[name] = {'input_sha256': sha256((p / 'exact_input.json').read_bytes()).hexdigest(),
                             'certificate_sha256': sha256((p / 'exact_certificate.json').read_bytes()).hexdigest(),
                             'cut_value': str(value), 'cut_value_decimal': float(value)}
        if name == 'universal_union_wallet_v3':
            actual_cut = mapped
    out = {
        'status': 'PASS_LITERAL_2048_STATES_128_ENVELOPES_AND_ACTUAL_HISTORY_MAP',
        'optimizer_calls': 0, 'certificate_sha256': sha256(cp.read_bytes()).hexdigest(),
        'old_types': 128, 'joint_states': 2048, 'positive_state_residuals': positive, 'zero_state_residuals': zero,
        'wallet': {'v3': 126000, 'v4': 65719, 'v6': 4962, 'K': 0, 'actual_root_u': 0},
        'all128_delta_strictly_positive': True, 'all128_gamma_zero_derived': True,
        'scope_extension': 'Every ordered two-action history and its prescribed four-player continuation, any six legal query labels and their union; neither maximal C nor K nor actual-root IC is used by the nine positive wallets.',
        'q_interval_preserved': '[o/6,o]', 'cut_all128': {str(h): str(value) for h, value in cut.items()},
        'actual_all256_coefficients': actual_cut, 'actual_K_coefficient': '0',
        'actual_point_evaluations': evaluations, 'local_envelopes': tables,
        'not_claimed': ['complete SPE realization', 'half coverage', 'whole v3 optimal-face exclusion'],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
