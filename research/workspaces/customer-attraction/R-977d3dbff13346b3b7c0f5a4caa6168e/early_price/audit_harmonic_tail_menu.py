"""Definition-level Fraction audit; finite checks do not prove the general claims."""

from fractions import Fraction as F
from itertools import product
from math import ceil
from pathlib import Path
import json
import random


def potential(p, a, k):
    return sum((F(1, p + a + j) for j in range(1, k + 1)), F(0))


def payoff(p, t, k):
    return F(t, p + 1 + k)


def positive(x):
    return max(F(0), x)


def main():
    parameters = 0
    etas = [F(0), F(1, 9), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(1), F(2)]
    for p, a, r, eta in product(range(9), range(2), range(1, 13), etas):
        vals = [F(1, p + 1 + k) + eta * potential(p, a, k) for k in range(r)]
        star = r - 1 if eta == 0 else min(r - 1, max(0, ceil(1 / eta - p - 2 + a)))
        assert vals[star] == min(vals)
        if eta == F(1, 2) and r >= 2:
            target = F(1, p + 1) if p else (F(3, 4) if a else F(1))
            assert min(vals) == target
        for k in range(r):
            kappa = F(1, p + 1) - F(1, p + 1 + k)
            assert potential(p, a, k) == potential(p, 0, k) - a * kappa
        parameters += 1

    rng = random.Random(977713)
    z_list = [(F(1), F(0), F(0)), (F(1, 2),) * 3, (F(1),) * 3]
    identities = 0
    for _ in range(2500):
        p, a, r = rng.randrange(8), rng.randrange(2), rng.randrange(1, 10)
        actual_k = rng.randrange(r)
        members = tuple(rng.randrange(2) for _ in range(3))
        tails = tuple(rng.randrange(r) for _ in range(3))
        z = z_list[rng.randrange(len(z_list))]
        tau = sum(z)
        pi = tuple(v / tau for v in z)
        eta, q = etas[rng.randrange(len(etas))], F(rng.randrange(5), 4)
        u, psi = payoff(p, a, actual_k), potential(p, a, actual_k)
        diagonal_u = sum((pi[i] * payoff(p, members[i], tails[i]) for i in range(3)), F(0))
        independent_u = sum((pi[i] * pi[j] * payoff(p, members[i], tails[j])
                             for i in range(3) for j in range(3)), F(0))
        diagonal_v = sum((pi[i] * potential(p, members[i], tails[i]) for i in range(3)), F(0))
        independent_v = sum((pi[i] * pi[j] * potential(p, members[i], tails[j])
                             for i in range(3) for j in range(3)), F(0))
        cyclic = diagonal_v - independent_v
        assert diagonal_u - independent_u == cyclic
        actual_comparison = psi - sum((pi[i] * potential(p, a, tails[i]) for i in range(3)), F(0))
        slack = tau * (u - diagonal_u)
        g = slack + tau * cyclic + eta * actual_comparison
        d = sum(z[i] * members[i] for i in range(3))
        coverage = q * min(F(1), d)
        mean_reciprocal = sum((pi[i] * F(1, p + 1 + tails[i]) for i in range(3)), F(0))
        assert slack + tau * cyclic == tau * u - d * mean_reciprocal
        assert coverage - d * mean_reciprocal <= positive(q - mean_reciprocal)
        assert coverage - tau * u == coverage - d * mean_reciprocal - slack - tau * cyclic
        residual = sum((pi[i] * (coverage - F(d, p + 1 + tails[i])
                                - eta * potential(p, a, tails[i])) for i in range(3)), F(0))
        assert coverage - tau * u == eta * psi + residual - g
        threshold = min(F(1, p + 1 + k) + eta * potential(p, a, k) for k in range(r))
        assert residual <= positive(q - threshold)
        identities += 1

    root = Path(__file__).resolve().parents[5]
    source = root / 'history/source/notes/customer_attraction/uploaded_2026-10-10/auxiliary_counterexample.json'
    certificate = json.loads(source.read_text())
    weights = {int(mask): value for mask, value in certificate['weights'].items()}
    policy = {tuple(item['history']): item['action'] for item in certificate['policy']}

    def continuation(t):
        history = (t,)
        while len(history) < certificate['n']:
            history += (policy[history],)
        return history[1:]

    tails = {t: continuation(t) for t in (4, 9, 8)}

    def v(t, tail):
        return sum((weight * potential(0, (mask >> t) & 1,
                                       sum((mask >> j) & 1 for j in tail))
                    for mask, weight in weights.items()), F(0))

    def u(t, tail):
        return sum((weight * payoff(0, (mask >> t) & 1,
                                    sum((mask >> j) & 1 for j in tail))
                    for mask, weight in weights.items()), F(0))

    cyclic = sum((v(t, tails[t]) - sum((v(t, tails[j]) for j in (4, 9)), F(0)) / 2
                  for t in (4, 9)), F(0)) / 2
    psi = v(8, tails[8])
    actual_comparison = psi - sum((v(8, tails[t]) for t in (4, 9)), F(0)) / 2
    slack = 2 * u(8, tails[8]) - sum((u(t, tails[t]) for t in (4, 9)), F(0))
    combined = 2 * cyclic + actual_comparison / 2
    assert cyclic == F(-11, 4)
    assert actual_comparison == 3
    assert psi == F(70761167, 3)
    assert slack == 3 and combined == -4 and slack + combined == -1

    return {
        'status': 'all exact finite algebra checks passed; not a general proof',
        'parameter_cases': parameters,
        'general_identity_cases': identities,
        'existing_complete_SPE_source': str(source.relative_to(root)),
        'source_SPE_status': 'uses existing complete certificate, whose SPE audit is in continuation_security_barriers.md; this script recomputes new menu values only',
        'source_menu': {str(t): list(tails[t]) for t in tails},
        'source_values': {k: str(v) for k, v in {
            'R_pi': cyclic, 'Z_pi': actual_comparison, 'Psi': psi,
            'tau': F(2), 'eta': F(1, 2), 'S_z': slack,
            'tau_R_plus_eta_Z': combined, 'G': slack + combined,
        }.items()},
    }


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
