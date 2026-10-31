"""Exact exploratory audit, independent of the displayed algebra expansion.

The finite checks do not prove the theorem for arbitrary backgrounds.  The
general proof is in occupied_background_half.md.  The SPE oracle imported
below is the repository's complete outcome-set oracle, not a tie selector.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def lam(r, B):
    return max(Q(d * (r - d), (B + d) * (r - 1))
               for d in range(1, r + 1))


def factor(r, B):
    return Q((r - 2) * (B + 1), r * (B + r)) + Q(2, 1) / (
        r + (r - 1) * lam(r, B))


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def profit(instance, prefix, future):
    ans = Q(0)
    for client in instance.customers:
        b = sum(prefix[a] for a in client.topics)
        d = sum(future[a] for a in client.topics)
        if d:
            ans += client.multiplicity * Q(d, b + d)
    return ans


def run():
    checks = 0
    # Include fractional intermediate loads: this additionally checks the
    # Jensen/minimax variant of the same pointwise inequality.
    for r in range(2, 23):
        for B in range(0, r + 2):
            coefficient = lam(r, B)
            backgrounds = sorted({Q(B), Q(B + 1), Q(B + 7), Q(2 * B + 1, 2)})
            for b in backgrounds:
                for d in range(r + 1):
                    for h2 in range(2 * r - 1):
                        h = Q(h2, 2)
                        target = Q(d, b + d) if d else Q(0)
                        rhs = (d + coefficient * h) / (b + 1 + h)
                        assert target <= rhs, (r, B, b, d, h)
                        checks += 1
    ranges = []
    for r in range(6, 301):
        B = r - 4
        assert lam(r, B) <= Q(r, 3 * (r - 1))
        assert factor(r, B) >= Q(1, 2)
        ranges.append((r, str(factor(r, B))))
    assert lam(5, 2) == Q(3, 8)
    assert factor(5, 2) == Q(257, 455)

    rng = random.Random(202610215)
    spe_games, spe_outcomes = 0, 0
    worst_ratio = None
    cases = []
    for r, B in [(2, 0), (3, 0), (4, 1), (5, 2), (6, 2), (7, 3), (8, 4)]:
        for trial in range(12):
            k = 3
            # B copies of each legal theme form the fixed ordered prefix.
            # Every interest type consequently has at least B incumbents.
            prefix = (B,) * k
            clients = []
            for mask in range(1, 1 << k):
                weight = rng.randrange(0, 8)
                if weight:
                    clients.append(CustomerType(frozenset(
                        a for a in range(k) if mask >> a & 1), weight))
            instance = Instance(tuple(map(str, range(k))), tuple(clients), r + sum(prefix))
            oracle = ExactSPESolver(instance)
            outcomes = oracle.outcomes(prefix)
            optimum = max(profit(instance, prefix, future)
                          for future in compositions(r, k))
            actual = min(profit(instance, prefix, tuple(z[a] - prefix[a] for a in range(k)))
                         for z in outcomes)
            assert actual >= factor(r, B) * optimum
            if r >= 5:
                assert 2 * actual >= optimum
            if optimum:
                ratio = actual / optimum
                if worst_ratio is None or ratio < worst_ratio:
                    worst_ratio = ratio
            spe_games += 1
            spe_outcomes += len(outcomes)
            if trial == 0:
                cases.append({'r': r, 'B': B, 'full_players': instance.players,
                              'F': str(optimum), 'minimum_SPE_P': str(actual),
                              'bound_factor': str(factor(r, B)),
                              'all_SPE_terminal_counts': len(outcomes)})

    return {'status': 'finite exact audit only; general proof is analytic and awaits independent review',
            'per_customer_inequalities_checked': checks,
            'half_range_checked': {'r_min': 6, 'r_max': 300, 'B': 'r-4'},
            'r5_B2_factor': str(factor(5, 2)),
            'complete_outcome_oracle_legal_background_games': spe_games,
            'all_SPE_outcomes_checked': spe_outcomes,
            'minimum_P_over_F_in_games': str(worst_ratio),
            'representative_games': cases}


if __name__ == '__main__':
    result = run()
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if len(sys.argv) > 1:
        with Path(sys.argv[1]).open('x') as stream:
            stream.write(rendered + '\n')
