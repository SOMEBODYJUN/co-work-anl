"""Verify the supplementary fixed-cone certificates using only the standard library."""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json


SOURCE = Path('archives/customer-attraction/tools/evidence/whole-subtree-nine-endpoints-primary/original')
ENDPOINTS = {
    'clients48': ('m5p7_reentry_incumbent_half.json', 'e6269ea7551820d0d2c6192dd96d60b7bd2ce1f92b6ffd463fd8a13f89da0565'),
    'clients252': ('m5p7_residual.json', '2a154303b023acfdc7b09c8576f63b3acb50abb02bd8e3cca6a793152ad07233'),
}
TOPICS, PLAYERS, SCALE = 7, 5, 60
TYPES = tuple(range(1, 1 << TOPICS))
PORTFOLIOS = tuple(combinations(range(TOPICS), PLAYERS))


def coverage_row(labels):
    union = sum(1 << a for a in labels)
    return tuple(int(bool(mask & union)) for mask in TYPES)


def dot(row, vector):
    return sum(coefficient * value for coefficient, value in zip(row, vector))


def load_endpoint(repo, name):
    filename, expected = ENDPOINTS[name]
    original = (repo / SOURCE / filename).read_bytes()
    assert sha256(original).hexdigest() == expected
    data = json.loads(original)['exact']
    entries = data['strategy']['actions']
    actions = {tuple(entry['history']): entry['action'] for entry in entries}
    expected_histories = {h for n in range(PLAYERS) for h in product(range(TOPICS), repeat=n)}
    assert len(actions) == len(entries) and set(actions) == expected_histories
    assert all(a in range(TOPICS) for a in actions.values())
    clients = tuple(data['integer_clones'])
    assert len(clients) == len(TYPES) and all(type(x) is int and x >= 0 for x in clients)

    @lru_cache(None)
    def terminal(history):
        if len(history) == PLAYERS:
            return history
        return terminal(history + (actions[history],))

    @lru_cache(None)
    def payoff(terminal_path, a):
        return tuple(SCALE // sum(bool(mask & (1 << label)) for label in terminal_path)
                     if mask & (1 << a) else 0 for mask in TYPES)

    rows = {}
    for history, action in actions.items():
        actual = payoff(terminal(history), action)
        for alternate in range(TOPICS):
            if alternate == action:
                continue
            deviation = payoff(terminal(history + (alternate,)), alternate)
            rows[(history, alternate)] = tuple(a - b for a, b in zip(actual, deviation))
    assert len(rows) == 16806
    return {
        'path': terminal(()), 'actions': actions, 'clients': clients,
        'by_deviation': rows, 'rows': sorted({row for row in rows.values() if any(row)}),
    }


def check_primal(rows, vector, w):
    assert len(vector) == len(TYPES) and all(x >= 0 for x in vector)
    assert dot(w, vector) == 1
    assert all(dot(g, vector) >= 0 for g in rows)


def decode_vector(sparse):
    assert len({mask for mask, _ in sparse}) == len(sparse)
    assert all(mask in TYPES and F(value) > 0 for mask, value in sparse)
    values = {mask: F(value) for mask, value in sparse}
    return tuple(values.get(mask, F(0)) for mask in TYPES)


def check_dual(rows, w, c, proof):
    beta = F(proof['beta'])
    weights = {index: F(value) / SCALE for index, value in proof['mu']}
    assert len(weights) == len(proof['mu'])
    assert all(0 <= i < len(rows) and value > 0 for i, value in weights.items())
    for k, (wk, ck) in enumerate(zip(w, c)):
        assert beta * wk - sum(value * rows[i][k] for i, value in weights.items()) >= ck
    return beta


def verify(repo, certificate):
    assert certificate['schema'] == 1
    a = load_endpoint(repo, 'clients48')
    b = load_endpoint(repo, 'clients252')
    assert a['path'] == (0, 1, 0, 1, 0) and b['path'] == (0, 0, 0, 1, 1)
    assert sum(a['actions'][h] != b['actions'][h] for h in a['actions']) == 92
    w = coverage_row((0, 1))
    shared = sorted(set(a['rows']) & set(b['rows']))
    assert (len(a['rows']), len(b['rows']), len(shared)) == (1912, 1867, 1753)
    endpoints = {'clients48': a, 'clients252': b}
    assert (sum(a['clients']), sum(b['clients'])) == (48, 252)
    assert (dot(w, a['clients']), dot(w, b['clients'])) == (30, 160)
    for origin in endpoints.values():
        vector = tuple(F(x, dot(w, origin['clients'])) for x in origin['clients'])
        for policy in endpoints.values():
            check_primal(policy['rows'], vector, w)
    attaining = tuple(F(x, 30) for x in a['clients'])
    assert dot(coverage_row((0, 1, 2, 4, 5)), attaining) == F(8, 5)

    for name, rows in [('clients48', a['rows']), ('clients252', b['rows']), ('shared', shared)]:
        proofs = certificate['suites'][name]
        assert tuple(tuple(proof['J']) for proof in proofs) == PORTFOLIOS
        bounds = []
        for proof in proofs:
            c = coverage_row(proof['J'])
            beta = check_dual(rows, w, c, proof)
            if name != 'shared':
                primal = decode_vector(proof['primal'])
                check_primal(rows, primal, w)
                assert dot(c, primal) == beta
                expected = {(True, True): F(8, 5), (True, False): F(3, 2),
                            (False, True): F(23, 15), (False, False): F(63, 40)}
                assert beta == expected[(0 in proof['J'], 1 in proof['J'])]
            bounds.append(beta)
        assert max(bounds) == F(8, 5)

    for name, proof in certificate['separations'].items():
        opposite = 'clients252' if name == 'clients48' else 'clients48'
        vector = decode_vector(proof['primal'])
        check_primal(endpoints[name]['rows'], vector, w)
        key = (tuple(proof['opposing_history']), proof['opposing_deviation'])
        opposing_row = endpoints[opposite]['by_deviation'][key]
        assert dot(opposing_row, vector) / SCALE == F(proof['opposing_ic']) == -F(1, 45)
    assert set(certificate['separations']) == set(endpoints)
    print('Verified 63 duals, 42 matching primals, two cross-feasible endpoints, and two separating vectors.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repository', type=Path, help='repository root with both frozen endpoints')
    args = parser.parse_args()
    certificate = json.loads(Path(__file__).with_name('certificates.json').read_text())
    verify(args.repository, certificate)
