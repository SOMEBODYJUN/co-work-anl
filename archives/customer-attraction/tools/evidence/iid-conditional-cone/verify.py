"""Exact definition-level check of frozen and reconstructed iid certificates.

Uses the standard library only; imports neither discovery nor original audits.
Known policy and known certificates are inputs, so this is not a blind review.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

F = Fraction
ROOT = Path(__file__).resolve().parent
HISTORIES = [h for k in range(3) for h in product(range(6), repeat=k)]


def terminal(prefix):
    actions = list(prefix)
    while len(actions) < 3:
        if not actions:
            action = 0
        elif len(actions) == 1:
            action = 3 * (actions[0] < 3)
        else:
            start = 3 * (actions[1] >= 3)
            action = min(set(range(start, start + 3)) - set(actions))
        actions.append(action)
    return tuple(actions)


def share(mask, actions, position):
    if not (mask & (1 << actions[position])):
        return F(0)
    return F(1, sum(bool(mask & (1 << a)) for a in actions))


def gamma(mask, history, action):
    return share(mask, terminal(history), len(history)) - share(
        mask, terminal(history + (action,)), len(history))


def static_rows(mask):
    t = F(mask.bit_count(), 6)
    psi = 1 - (1 - t) ** 3
    g = 1 - t + t * t / 3
    return psi, tuple(psi - 3 * g * bool(mask & (1 << a)) for a in range(6))


def certificate_report(path):
    cert = json.loads(path.read_text())
    assert (cert['n'], cert['m']) == (3, 6)
    assert list(map(F, cert['q'])) == [F(1, 6)] * 6
    spe = {}
    for row in cert['sparse_spe']:
        history, action = tuple(row['history']), row['deviation']
        assert history in HISTORIES and action in range(6)
        assert (history, action) not in spe
        spe[history, action] = F(row['lambda'])
    ne = {}
    for row in cert['sparse_ne']:
        action = row['action']
        assert action in range(6) and action not in ne
        ne[action] = F(row['lambda'])
    assert all(x >= 0 for x in [*spe.values(), *ne.values()])
    assert set(map(int, cert['residuals'])).issubset(range(1, 64))
    residuals = []
    for mask in range(1, 64):
        psi, rows = static_rows(mask)
        c = F(any(mask & (1 << a) for a in terminal(())))
        residual = c - psi - sum(
            multiplier * gamma(mask, history, action)
            for (history, action), multiplier in spe.items()
        ) - sum(multiplier * rows[a] for a, multiplier in ne.items())
        assert residual >= 0
        assert residual == F(cert['residuals'].get(str(mask), 0))
        residuals.append(residual)
    # The all-one customer is a zero objective witness, so 0 is also optimal.
    core = 63
    assert all(gamma(core, h, a) == 0 for h in HISTORIES for a in range(6))
    assert static_rows(core) == (F(1), (F(0),) * 6)
    return {
        'columns_verified': len(residuals),
        'all_spe_rows_available': len(HISTORIES) * 6,
        'positive_spe_multipliers': sum(x > 0 for x in spe.values()),
        'positive_ne_multipliers': sum(x > 0 for x in ne.values()),
        'positive_residuals': sum(x > 0 for x in residuals),
        'zero_residuals': sum(x == 0 for x in residuals),
        'minimum_residual': str(min(residuals)),
        'minimum_nonzero_multiplier': str(min([*spe.values(), *ne.values()])),
        'normalized_objective_optimum_exact': '0',
    }


def original36_report():
    weights = {}
    for mask in range(1, 64):
        x, y = (mask & 7).bit_count(), (mask >> 3).bit_count()
        if (x, y) == (1, 1):
            weights[mask] = 1
        elif (x, y) == (2, 2):
            weights[mask] = 3
    assert sum(weights.values()) == 36
    dot = lambda coeff: sum(F(w) * coeff(mask) for mask, w in weights.items())
    payoff = lambda z, i: dot(lambda mask: share(mask, z, i))
    coverage = lambda z: sum(w for mask, w in weights.items() if any(mask & (1 << a) for a in z))
    harmonic = lambda z: dot(lambda mask: sum(
        (F(1, j) for j in range(1, sum(bool(mask & (1 << a)) for a in z) + 1)), F(0)))
    spe_slacks = [dot(lambda mask: gamma(mask, h, a)) for h in HISTORIES for a in range(6)]
    assert min(spe_slacks) == 0
    ne_values = [dot(lambda mask: static_rows(mask)[1][a]) for a in range(6)]
    assert ne_values == [0] * 6
    root = terminal(())
    utilities = [payoff(root, i) for i in range(3)]
    assert utilities == [10, 12, 12]
    psi = dot(lambda mask: static_rows(mask)[0])
    W = coverage(root)
    assert (W, psi) == (34, F(97, 3))
    optimum = max(coverage(z) for z in product(range(6), repeat=3))
    assert optimum == 36
    G, D = [], []
    for i in range(3):
        expected_slack, deletion = F(0), F(0)
        for h in product(range(6), repeat=i):
            z = terminal(h)
            for a in range(6):
                za = terminal(h + (a,))
                probability = F(1, 6 ** (i + 1))
                expected_slack += probability * (payoff(z, i) - payoff(za, i))
                deletion += probability * (
                    harmonic(z[:i] + z[i + 1:]) - harmonic(za[:i] + za[i + 1:]))
        G.append(expected_slack)
        D.append(deletion)
    iid_phi = sum(harmonic(z) for z in product(range(6), repeat=3)) / 6 ** 3
    root_excess, iid_excess = harmonic(root) - W, iid_phi - psi
    remainder = sum(D) - root_excess + iid_excess
    assert G == [0, F(1, 2), F(31, 18)] and D == [0, -1, 0]
    assert remainder == F(-5, 9) and W - psi == sum(G) + remainder
    return {
        'ordered_histories': len(HISTORIES),
        'spe_comparisons': len(spe_slacks),
        'strict_spe_comparisons': sum(x > 0 for x in spe_slacks),
        'tied_spe_comparisons': sum(x == 0 for x in spe_slacks),
        'minimum_spe_slack': str(min(spe_slacks)),
        'all_six_ne_rows': list(map(str, ne_values)),
        'root_terminal': root, 'root_utilities': list(map(str, utilities)),
        'W': W, 'OPT3': optimum, 'Z3': str(psi),
        'individual_iid_gap': str(utilities[0] - psi / 3),
        'level_slacks': list(map(str, G)), 'same_slot_deletion_differences': list(map(str, D)),
        'root_harmonic_excess': str(root_excess), 'iid_harmonic_excess': str(iid_excess),
        'unit_flow_remainder': str(remainder), 'W_minus_Z3': str(W - psi),
    }


def main():
    frozen_path = ROOT / 'original/evidence/certificates/customer_attraction/iid_security_conditional_36.json'
    generated_path = ROOT / 'replay/36_uniform_iid_ne_dual.json'
    result = {'frozen_certificate': certificate_report(frozen_path), 'original36': original36_report()}
    if generated_path.exists():
        result['reconstructed_generator_certificate'] = certificate_report(generated_path)
        result['reconstructed_generator_json_equals_frozen'] = json.loads(generated_path.read_text()) == json.loads(frozen_path.read_text())
    frozen_run = json.loads((ROOT / 'original/evidence/runs/2026-10-10/customer_attraction_iid_conditional_cone.json').read_text())
    audit_path = ROOT / 'replay/original-audit.json'
    result['original_audit_matches_frozen_run'] = json.loads(audit_path.read_text()) == frozen_run
    assert result['original_audit_matches_frozen_run']
    (ROOT / 'replay/definition-check.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
