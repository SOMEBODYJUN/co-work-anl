"""Independent Fraction replay of the 86-unit five-player security failure.

No optimizer, equilibrium solver, generator, or other verifier is imported.
All ordered histories are retained; counts cache only numerical payoffs.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[2]


def replay(input_path, certificate_path):
    game = json.loads(input_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    n, m = game['players'], len(game['topics'])
    assert (n, m) == (5, 10)
    types, seen = [], set()
    for raw in game['customers']:
        likes, count = frozenset(raw['topics']), raw['multiplicity']
        assert likes and len(likes) == len(raw['topics']) and likes not in seen
        assert all(type(a) is int and 0 <= a < m for a in likes)
        assert type(count) is int and count > 0
        seen.add(likes); types.append((likes, count))
    assert sum(count for likes, count in types) == 86
    histories = tuple(h for d in range(n) for h in product(range(m), repeat=d))
    raw = certificate['strategy']['actions']
    policy = {tuple(row['history']): row['action'] for row in raw}
    assert len(raw) == len(policy) and set(policy) == set(histories)
    assert all(type(a) is int and 0 <= a < m for a in policy.values())

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == n else terminal(h + (policy[h],))

    @lru_cache(None)
    def counts(z):
        return tuple(z.count(a) for a in range(m))

    @lru_cache(None)
    def payoff(a, q):
        return sum((F(count, sum(q[b] for b in likes))
                    for likes, count in types if a in likes), F(0))

    def welfare(z):
        return sum(count for likes, count in types if any(a in likes for a in z))

    strict = tied = 0
    for h in histories:
        own = payoff(policy[h], counts(terminal(h)))
        for a in range(m):
            slack = own - payoff(a, counts(terminal(h + (a,))))
            assert slack >= 0, (h, a, str(slack))
            if a != policy[h]:
                strict += slack > 0; tied += slack == 0
    z = terminal(())
    utility = tuple(payoff(a, counts(z)) for a in z)
    W = welfare(z)
    OPT = max(welfare(profile) for profile in combinations_with_replacement(range(m), n))
    assert certificate['strategy']['terminal_counts'] == list(counts(z))
    assert sum(utility) == W
    signatures = [frozenset(i for i, (likes, count) in enumerate(types) if a in likes)
                  for a in range(m)]
    maximal = [S for S in signatures if not any(S < T for T in signatures)]
    assert len(set(signatures)) == len(set(maximal)) == 10
    security = certificate['security']
    p = tuple(map(F, security['primary']))
    Q = [(tuple(row['rivals']), F(row['probability'])) for row in security['dual']]
    assert len(p) == m and min(p) >= 0 and sum(p) == 1
    assert Q and min(q for B, q in Q) >= 0 and sum(q for B, q in Q) == 1
    assert all(len(B) == n - 1 and all(type(a) is int and 0 <= a < m for a in B)
               for B, q in Q)

    @lru_cache(None)
    def query(a, q):
        return sum((F(count, 1 + sum(q[b] for b in likes))
                    for likes, count in types if a in likes), F(0))

    lower = min(sum((p[a] * query(a, counts(B)) for a in range(m)), F(0))
                for B in product(range(m), repeat=n - 1))
    dual_queries = tuple(sum((q * query(a, counts(B)) for B, q in Q), F(0))
                         for a in range(m))
    assert lower == max(dual_queries) == F(security['value'])
    assert all(x == lower for x in dual_queries)
    assert (z, utility, W, OPT, lower) == (
        (4, 5, 6, 7, 8), (F(81, 5),) + (F(86, 5),) * 4, 85, 86, F(2262, 139))
    assert lower - utility[0] == F(51, 695) > 0
    assert W - n * lower == F(505, 139) > 0
    assert 2 * W - OPT == 84 > 0
    result = {
        'status': 'PASS', 'unit_customers': 86, 'customer_types': len(types),
        'players': n, 'topics': m, 'distinct_maximal_coverages': 10,
        'ordered_histories': len(histories), 'all_action_comparisons': m * len(histories),
        'nontrivial_deviations': strict + tied, 'strict_deviations': strict,
        'tied_deviations': tied, 'root': list(z), 'utilities': list(map(str, utility)),
        'W': W, 'OPT': OPT, 'security_value': str(lower),
        'first_player_security_deficit': str(lower - utility[0]),
        'W_minus_nv': str(W - n * lower), 'half_coverage_margin': 2 * W - OPT,
        'ordered_static_backgrounds': m ** (n - 1),
        'dual_query_values': list(map(str, dual_queries)),
        'scope': 'One complete five-player SPE; individual security fails, aggregate security and half coverage hold.',
        'sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in (input_path, certificate_path, Path(__file__))}
    }
    for key, expected in certificate.get('expected', {}).items():
        assert result[key] == expected, (key, result[key], expected)
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path,
                    default=ROOT / 'examples/customer_attraction/five_individual_security.json')
    ap.add_argument('--certificate', type=Path,
                    default=ROOT / 'evidence/certificates/customer_attraction/five_individual_security.json')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    raw = json.dumps(replay(args.input, args.certificate), indent=2) + '\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(raw)
    print(raw, end='')
