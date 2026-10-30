"""Independent unit-expansion and scalar algebra audit of stationary transport.

Reads canonical games and certificates; imports no generator, first audit,
repository solver or optimizer. Default stdout only; --output is exclusive.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]


def scalar_transport():
    checks = residual_checks = 0
    for m in range(1, 6):
        graphs = [([((a + 1) % m) for a in range(m)], [tuple(range(m))]),
                  ([0] * m, [(0,)]),
                  (list(range(m)), [(a,) for a in range(m)])]
        for background in (0, 1, 3, 10, 1000):
            for response, cycles in graphs:
                mass = [Fraction(m - a, m * (m + 1) // 2) for a in range(m)]
                pushed = [sum((mass[a] for a in range(m) if response[a] == b), Fraction())
                          for b in range(m)]
                singleton_residuals = []
                for mask in range(1, 1 << m):
                    members = set(a for a in range(m) if mask & (1 << a))

                    def U(a, b):
                        return Fraction(int(a in members), background + 1 + int(b in members))

                    actual_action = m - 1
                    actual_payoff = U(actual_action, response[actual_action])
                    for query in range(m):
                        for cycle in cycles:
                            original = actual_payoff - sum((U(query, a) for a in cycle), Fraction()) / len(cycle)
                            paid = sum((actual_payoff - U(a, response[a])
                                      + U(response[a], a) - U(query, a)
                                      for a in cycle), Fraction()) / len(cycle)
                            assert original == paid
                            checks += 1
                        original = actual_payoff - sum((mass[a] * U(query, a)
                                                      for a in range(m)), Fraction())
                        paid = sum((mass[a] * (actual_payoff - U(a, response[a])
                                              + U(response[a], a) - U(query, a))
                                    for a in range(m)), Fraction())
                        residual = sum((mass[a] - pushed[a] for a in members), Fraction()) / (background + 1)
                        assert original - paid == residual
                        residual_checks += 1
                    if len(members) == 1:
                        singleton_residuals.append(residual)
                assert all(value >= 0 for value in singleton_residuals) == (mass == pushed)
    return {'cycle_coordinate_checks': checks, 'divergence_coordinate_checks': residual_checks,
            'background_loads': [0, 1, 3, 10, 1000], 'theme_counts': [1, 2, 3, 4, 5]}


def unit_replay(name):
    game_file = ROOT / 'examples/customer_attraction' / (name + '.json')
    certificate_file = ROOT / 'evidence/certificates/customer_attraction' / (name + '.json')
    game = json.loads(game_file.read_text())
    cert = json.loads(certificate_file.read_text())
    n, m = game['players'], len(game['topics'])
    units = []
    for row in game['customers']:
        likes = frozenset(row['topics'])
        assert type(row['multiplicity']) is int and row['multiplicity'] > 0
        assert likes and len(likes) == len(row['topics']) and min(likes) >= 0 and max(likes) < m
        units.extend([likes] * row['multiplicity'])
    entries = cert['strategy']['actions']
    actions = {tuple(row['history']): row['action'] for row in entries}
    histories = [h for k in range(n) for h in product(range(m), repeat=k)]
    assert len(actions) == len(entries) and set(actions) == set(histories)
    assert all(type(a) is int and 0 <= a < m for a in actions.values())

    def terminal(h):
        z = list(h)
        while len(z) < n:
            z.append(actions[tuple(z)])
        return tuple(z)

    def utility(z):
        result = [Fraction()] * n
        for likes in units:
            positions = [i for i, a in enumerate(z) if a in likes]
            for i in positions:
                result[i] += Fraction(1, len(positions))
        return result

    def static(a, competitors):
        return sum((Fraction(1, 1 + sum(b in likes for b in competitors))
                    for likes in units if a in likes), Fraction())

    def welfare(z):
        return sum(any(a in likes for a in z) for likes in units)

    comparisons = ties = 0
    for h in histories:
        old = utility(terminal(h))[len(h)]
        for a in range(m):
            new = utility(terminal(h + (a,)))[len(h)]
            assert old >= new, (name, h, a, old, new)
            comparisons += 1
            ties += old == new
    z = terminal(())
    W = welfare(z)
    assert tuple(cert['expected']['outcome']) == z and Fraction(cert['expected']['W']) == W
    assert cert['strategy']['terminal_counts'] == [z.count(a) for a in range(m)]
    assert sum(utility(z)) == W
    kernel = cert['prescribed_static_kernel']
    rawQ = kernel['dual']
    Q = {tuple(row['rivals']): Fraction(row['probability']) for row in rawQ}
    assert len(Q) == len(rawQ) and sum(Q.values()) == 1
    assert all(q >= 0 and len(B) == n - 1 and all(0 <= b < m for b in B) for B, q in Q.items())
    caps = [sum((q * static(a, B) for B, q in Q.items()), Fraction()) for a in range(m)]
    coefficient = Fraction(kernel['target_coefficient'])
    menus = {tuple(sorted(off[:i] + off[i + 1:])) for i in range(n)
             for a in range(m) for off in [terminal(z[:i] + (a,))]}
    record = {'name': name, 'unit_customers': len(units), 'decision_histories': len(histories),
              'full_comparisons': comparisons, 'ties': ties, 'outcome': z,
              'utilities': list(map(str, utility(z))), 'W': W,
              'OPT': max(welfare(y) for y in product(range(m), repeat=n)),
              'prescribed_Q_query_values': list(map(str, caps)),
              'target_coefficient': str(coefficient),
              'cap_excess': str(max(caps) - W / coefficient)}
    if name == 'root_stationary_kernel':
        assert len(units) == 22 and z == (0, 3, 4) and utility(z) == [6, 6, 5] and W == 17
        signatures = [frozenset(i for i, likes in enumerate(units) if a in likes) for a in range(m)]
        assert len(set(signatures)) == m
        pi = list(map(Fraction, kernel['stationary']))
        assert sum(pi) == 1 and min(pi) >= 0
        tail = [terminal((a,))[1:] for a in range(m)]
        assert tail[:3] == [(3, 4)] * 3 and tail[3:] == [(0, 1)] * 3
        matrix = [[Fraction(tail[a].count(b), n - 1) for b in range(m)] for a in range(m)]
        assert all(sum(pi[a] * matrix[a][b] for a in range(m)) == pi[b] for b in range(m))
        assert pi == [Fraction(1, 4), Fraction(1, 4), 0, Fraction(1, 4), Fraction(1, 4), 0]
        pushed = {}
        for a in range(m):
            B = tuple(sorted(tail[a]))
            pushed[B] = pushed.get(B, Fraction()) + pi[a]
        assert pushed == Q
        assert caps == [Fraction(23, 4), Fraction(19, 4), 6, Fraction(23, 4), Fraction(19, 4), 6]
        assert max(caps) - Fraction(W, 3) == Fraction(1, 3)
        alternative = (0, 3)
    else:
        assert len(units) == 7 and z == (1, 0, 1) and W == 7
        marginal = list(map(Fraction, kernel['marginal']))
        assert marginal == [Fraction(z.count(a), n) for a in range(m)]
        for B in product(range(m), repeat=n - 1):
            probability = Fraction(1)
            for a in B:
                probability *= marginal[a]
            assert Q.get(B, Fraction()) == probability
        assert caps[2] == Fraction(77, 27) and caps[2] - Fraction(14, 5) == Fraction(7, 135)
        p = list(map(Fraction, cert['security']['primary']))
        raw = cert['security']['dual']
        dual = [(tuple(row['rivals']), Fraction(row['probability'])) for row in raw]
        assert min(p) >= 0 and sum(p) == 1 and all(q >= 0 for B, q in dual) and sum(q for B, q in dual) == 1
        guaranteed = min(sum(p[a] * static(a, B) for a in range(m))
                         for B in product(range(m), repeat=n - 1))
        upper = max(sum(q * static(a, B) for B, q in dual) for a in range(m))
        assert guaranteed == upper == Fraction(cert['security']['value']) == 2
        record['true_security_value'] = '2'
        alternative = (1, 3)
    assert alternative in menus
    alternative_cap = max(static(a, alternative) for a in range(m))
    assert alternative_cap <= Fraction(W, n)
    record['actual_menu_alternative'] = alternative
    record['actual_menu_alternative_cap'] = str(alternative_cap)
    record['sha256'] = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in (game_file, certificate_file)}
    return record


def run():
    return {'status': 'PASS', 'scope': 'Independent exact unit replay and scalar SCT/DIV checks; both failures concern prescribed Q.',
            'algebra': scalar_transport(),
            'games': [unit_replay(name) for name in ('root_stationary_kernel', 'empirical_iid_kernel')],
            'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2) + '\n'
    if args.output:
        with args.output.open('x') as handle:
            handle.write(rendered)
    print(rendered, end='')
