"""Parent reconstruction from literal terminal shares; no discovery imports.

These are complete customer-state checks of explicit certificate identities,
not finite-game evidence for HALF(5). Mathematical node legality is recorded
in the accompanying review. No random seed or floating-point arithmetic.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]


def utility(leaf, player):
    load = sum(leaf)
    return F(leaf[player], load) if leaf[player] else F(0)


def replacement(leaf, player, action):
    modified = list(leaf)
    modified[player] = action
    return utility(modified, player)


def safe_query(prefix, remaining, action):
    # All remaining copies of the query attain its worst possible load.
    return utility(list(prefix) + [action] * remaining, len(prefix))


def third_floor():
    alpha, cap, size = F(11033, 763), F(2085, 763), F(4139, 763)
    weights = (F(1, 2), F(1093, 1526), F(77, 109), F(618, 763),
               F(165, 763), F(673, 763), F(135, 763), F(180, 763), F(90, 763))
    assert sum(weights[:4]) == cap
    residuals = []
    for t, a, b, c, d, q, e in product((0, 1), repeat=7):
        original = (t, a, b, c, d)
        copied = (t, a, b, d, e)
        r = utility(original, 0)
        rows = (
            -F(a), -F(b), -F(c), -F(d),
            utility(original, 2) - safe_query((t, a), 3, d),
            utility(original, 4) - replacement(original, 4, q),
            utility(original, 4) - replacement(original, 4, e),
            utility(original, 3) - utility(copied, 3),
            utility(copied, 4) - replacement(copied, 4, q),
        )
        target_query = F(q, 1 + 4*t)
        residual = alpha*r - size*t - target_query - sum(w*v for w, v in zip(weights, rows))
        assert residual >= 0
        residuals.append(residual)
    assert alpha/5 + cap - size == F(1, 5)
    return {'states': len(residuals), 'minimum': str(min(residuals)),
            'zeros': sum(v == 0 for v in residuals),
            'alpha': str(alpha), 'cap': str(cap), 'size': str(size)}


def direct_root_cuts():
    path = BASE/'realizability/root_max_direct_certificates.json'
    certificates = json.loads(path.read_text())
    reports = []
    for cert in certificates:
        weights = {k: F(v) for k, v in cert['weights'].items()}
        alpha, cap, size = (F(cert[k]) for k in ('alpha', 'beta', 'lambda'))
        assert min(weights.values()) >= 0
        assert weights['root'] == alpha
        assert sum(weights.get('cap'+str(i), F(0)) for i in range(1, 5)) - size == cap
        residuals = []
        for bits in product((0, 1), repeat=5):
            t, a, b, c, d = bits
            r = utility(bits, 0)
            for count in range(6):
                # All optimal labels enter these rows only through count.
                # Expanding each labelled pair gives these exact two sums.
                prefix = t+a+b
                pair_sum = F(count*(5-count), prefix+1) + F(count*(count-1), prefix+2)
                tax = F(c, (prefix+1)*(prefix+2))
                rows = {
                    'root': -r,
                    **{'cap'+str(i): -F(bits[i]) for i in range(1, 5)},
                    'OPT2': 5*utility(bits, 2) - F(count, t+a+3),
                    'OPT4': 5*utility(bits, 4) - F(count, t+a+b+c+1),
                    'K2_4': utility(bits, 2) - safe_query((t, a), 3, d),
                    'K3_4': utility(bits, 3) - safe_query((t, a, b), 2, d),
                    'PAIRopt': 10*(utility(bits, 3)+utility(bits, 4)+tax)-pair_sum,
                }
                residual = -F(count > 0)-size*t-sum(w*rows[k] for k, w in weights.items())
                assert residual >= 0, (cert, bits, count, residual)
                residuals.append(residual)
        reports.append({'states': len(residuals), 'minimum': str(min(residuals)),
                        'zeros': sum(v == 0 for v in residuals),
                        'alpha': str(alpha), 'cap': str(cap), 'size': str(size)})
    return reports, hashlib.sha256(path.read_bytes()).hexdigest()


def four_tail_max_cut():
    path = BASE/'background/local_max_tail_certificate.json'
    cert = json.loads(path.read_text())
    weights = {k: F(v) for k, v in cert['multipliers'].items()}
    alpha, cap, gamma = (F(cert[k]) for k in ('rounded_A', 'rounded_B', 'gamma_T'))
    assert min(weights.values()) >= 0
    assert weights['root'] == alpha
    assert gamma + sum((5 if k == 'size:opt' else 1)*v for k, v in weights.items() if k.startswith('size:')) == cap
    residuals = []
    for bits in product((0, 1), repeat=8):
        t, a, b, c, d, q, r, s = bits
        actual, copied = (t, a, b, c, d), (t, d, q, r, s)
        for count in range(6):
            rows = {'F': utility(actual, 1)-utility(copied, 1),
                    'root': -utility(actual, 0), 'size:opt': -F(count)}
            rows.update({'size:'+str(i): -F(v) for i, v in enumerate(bits)})
            for tag, leaf, start in (('act', actual, 1), ('off', copied, 2)):
                for seat in range(start, 5):
                    for h, v in enumerate(bits):
                        rows[f'{tag}:K{seat-1}:{h}'] = utility(leaf, seat)-safe_query(leaf[:seat], 5-seat, v)
                    rows[f'{tag}:K{seat-1}:opt'] = 5*utility(leaf, seat)-F(count, sum(leaf[:seat])+5-seat)
                prefix = sum(leaf[:3])
                H = utility(leaf, 3)+utility(leaf, 4)+F(leaf[3], (prefix+1)*(prefix+2))
                rows[f'{tag}:P'] = 10*H-F(count*(5-count), prefix+1)-F(count*(count-1), prefix+2)
            residual = gamma*t-F(count > 0)-sum(v*rows[k] for k, v in weights.items())
            assert residual >= 0, (bits, count, residual)
            residuals.append(residual)
    rootfloor, nonnegative_cap = F(cert['root_floor_multiplier']), F(cert['K_nonnegative_multiplier'])
    assert rootfloor >= 0 and nonnegative_cap >= 0
    assert alpha+rootfloor == 50
    assert cap-rootfloor/5+nonnegative_cap == -8
    return {'states': len(residuals), 'minimum': str(min(residuals)),
            'zeros': sum(v == 0 for v in residuals), 'alpha': str(alpha),
            'cap': str(cap), 'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    direct, digest = direct_root_cuts()
    report = {'scope': 'Independent parent customer-identity reconstruction; HALF(5) remains OPEN',
              'arithmetic': 'fractions.Fraction; complete local state enumeration',
              'third_floor': third_floor(), 'direct_root_cuts': direct,
              'four_tail_max_cut': four_tail_max_cut(),
              'direct_certificate_sha256': digest,
              'external_review': False, 'novelty_certified': False}
    output = Path(__file__).with_suffix('.json')
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
