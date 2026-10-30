"""Fraction audit of cycle transport and two prescribed static-kernel failures.

No equilibrium solver or optimizer is imported. Default output is stdout;
--output creates a new report and refuses to replace an existing file.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def cycles_of(response):
    cycles = set()
    for seed in range(len(response)):
        path, seen, a = [], {}, seed
        while a not in seen:
            seen[a] = len(path)
            path.append(a)
            a = response[a]
        cycle = path[seen[a]:]
        start = cycle.index(min(cycle))
        cycles.add(tuple(cycle[start:] + cycle[:start]))
    return sorted(cycles)


def verify(name):
    input_path = ROOT / 'examples/customer_attraction' / (name + '.json')
    cert_path = ROOT / 'evidence/certificates/customer_attraction' / (name + '.json')
    game, cert = json.loads(input_path.read_text()), json.loads(cert_path.read_text())
    n, m = game['players'], len(game['topics'])
    types = [(sum(1 << a for a in row['topics']), row['multiplicity'])
             for row in game['customers']]
    assert all(type(w) is int and w > 0 and 0 < T < 1 << m for T, w in types)
    assert len(set(T for T, w in types)) == len(types)
    policy = {tuple(row['history']): row['action'] for row in cert['strategy']['actions']}
    histories = [h for depth in range(n) for h in product(range(m), repeat=depth)]
    assert len(policy) == len(cert['strategy']['actions']) and set(policy) == set(histories)
    assert all(type(a) is int and 0 <= a < m for a in policy.values())

    @lru_cache(None)
    def finish(h):
        return h if len(h) == n else finish(h + (policy[h],))

    def load(T, z):
        return sum(bool(T & (1 << a)) for a in z)

    def rho(a, z, T):
        return F(1, load(T, z)) if T & (1 << a) else F(0)

    def f(a, B, T):
        return F(1, 1 + load(T, B)) if T & (1 << a) else F(0)

    def utility(z, i):
        return sum((w * rho(z[i], z, T) for T, w in types), F(0))

    def query(a, B):
        return sum((w * f(a, B, T) for T, w in types), F(0))

    def coverage(z):
        return sum(w for T, w in types if load(T, z))

    comparisons, ties = 0, 0
    for h in histories:
        own = utility(finish(h), len(h))
        for a in range(m):
            slack = own - utility(finish(h + (a,)), len(h))
            assert slack >= 0, (name, h, a, slack)
            comparisons += 1
            ties += slack == 0
    z = finish(())
    W, O = coverage(z), max(coverage(y) for y in product(range(m), repeat=n))
    assert tuple(cert['expected']['outcome']) == z and F(cert['expected']['W']) == W
    assert cert['strategy']['terminal_counts'] == [z.count(a) for a in range(m)]
    assert sum(utility(z, i) for i in range(n)) == W

    # All last-pair histories, all reply cycles, all customer types and queries.
    transport_checks = divergence_checks = 0
    for P in product(range(m), repeat=n - 2):
        A, actual = policy[P], finish(P)
        response = [policy[P + (a,)] for a in range(m)]
        for cycle in cycles_of(response):
            assert all(response[a] == cycle[(j + 1) % len(cycle)]
                       for j, a in enumerate(cycle))
            for t in range(m):
                for T in range(1, 1 << m):
                    left = rho(A, actual, T) - sum((f(t, P + (a,), T)
                            for a in cycle), F(0)) / len(cycle)
                    paid = F(0)
                    for a in cycle:
                        off = finish(P + (a,))
                        gamma_parent = rho(A, actual, T) - rho(a, off, T)
                        gamma_last = rho(response[a], off, T) - f(t, P + (a,), T)
                        paid += (gamma_parent + gamma_last) / len(cycle)
                    assert left == paid
                    transport_checks += 1
        pi = [F(a + 1, m * (m + 1) // 2) for a in range(m)]
        pushed = [sum((pi[a] for a in range(m) if response[a] == b), F(0))
                  for b in range(m)]
        for t in range(m):
            for T in range(1, 1 << m):
                left = rho(A, actual, T) - sum((pi[a] * f(t, P + (a,), T)
                        for a in range(m)), F(0))
                paid = F(0)
                for a in range(m):
                    off = finish(P + (a,))
                    paid += pi[a] * (rho(A, actual, T) - rho(a, off, T)
                            + rho(response[a], off, T) - f(t, P + (a,), T))
                residual = sum((pi[a] - pushed[a] for a in range(m)
                               if T & (1 << a)), F(0)) / (1 + load(T, P))
                assert left == paid + residual
                divergence_checks += 1

    kernel = cert['prescribed_static_kernel']
    Q = {tuple(row['rivals']): F(row['probability']) for row in kernel['dual']}
    assert sum(Q.values()) == 1 and all(q >= 0 and len(B) == n - 1 for B, q in Q.items())
    caps = [sum((q * query(a, B) for B, q in Q.items()), F(0)) for a in range(m)]
    coefficient = F(kernel['target_coefficient'])
    result = {'name': name, 'unit_customers': sum(w for T, w in types),
              'ordered_histories': len(histories), 'all_action_comparisons': comparisons,
              'tied_comparisons': ties, 'outcome': z,
              'utilities': [str(utility(z, i)) for i in range(n)], 'W': W, 'OPT': O,
              'transport_coordinate_identities': transport_checks,
              'divergence_coordinate_identities': divergence_checks,
              'prescribed_kernel_query_values': list(map(str, caps)),
              'target_coefficient': str(coefficient),
              'prescribed_cap_gap': str(max(caps) - F(W, coefficient))}
    if name == 'root_stationary_kernel':
        assert (n, m, sum(w for T, w in types), z, W) == (3, 6, 22, (0, 3, 4), 17)
        assert all(any(bool(T & (1 << a)) != bool(T & (1 << b)) for T, w in types)
                   for a in range(m) for b in range(a))
        K = [[F(finish((a,))[1:].count(b), n - 1) for b in range(m)] for a in range(m)]
        assert K == [[F(b in (3, 4), 2) for b in range(m)] for a in range(3)] + [
                    [F(b in (0, 1), 2) for b in range(m)] for a in range(3)]
        pi = list(map(F, kernel['stationary']))
        assert pi == [F(1, 4), F(1, 4), F(0), F(1, 4), F(1, 4), F(0)]
        assert all(sum(pi[a] * K[a][b] for a in range(m)) == pi[b] for b in range(m))
        assert Q == {(0, 1): F(1, 2), (3, 4): F(1, 2)}
        assert caps == list(map(F, kernel['query_values']))
        assert max(caps) - F(W, 3) == F(kernel['cap_gap']) == F(1, 3)
        other = [query(a, (0, 3)) for a in range(m)]
        assert max(other) == 5 < F(W, 3)
        result['all_menu_background_03_cap'] = '5'
    else:
        assert (n, m, sum(w for T, w in types), z, W) == (3, 4, 7, (1, 0, 1), 7)
        q = [F(z.count(a), n) for a in range(m)]
        assert q == list(map(F, kernel['marginal']))
        iid = {B: q[B[0]] * q[B[1]] for B in product(range(m), repeat=n - 1)
               if q[B[0]] * q[B[1]]}
        assert Q == iid
        a = kernel['query']
        assert caps[a] == F(kernel['query_value']) == F(77, 27)
        assert caps[a] - F(W, coefficient) == F(kernel['query_gap']) == F(7, 135)
        p = list(map(F, cert['security']['primary']))
        dual = [(tuple(row['rivals']), F(row['probability'])) for row in cert['security']['dual']]
        assert min(p) >= 0 and sum(p) == 1 and sum(q for B, q in dual) == 1
        floor = min(sum(p[a] * query(a, B) for a in range(m))
                    for B in product(range(m), repeat=n - 1))
        cap = max(sum(q * query(a, B) for B, q in dual) for a in range(m))
        assert floor == cap == F(cert['security']['value']) == 2
        result['true_security_value'] = '2'
    result['sha256'] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in (input_path, cert_path)}
    return result


def run():
    results = [verify(name) for name in ('root_stationary_kernel', 'empirical_iid_kernel')]
    return {'status': 'PASS', 'scope': 'Pointwise transport implementation plus two prescribed kernels; no global bridge counterexample.',
            'results': results, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2) + '\n'
    if args.output:
        with args.output.open('x') as handle:
            handle.write(rendered)
    print(rendered, end='')
