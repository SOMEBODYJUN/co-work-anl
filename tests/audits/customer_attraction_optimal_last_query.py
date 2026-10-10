"""Definition-level exact audit of CA-OPTIMAL-LAST-QUERY-SUM-NO.

No SPE solver, LP oracle, floating arithmetic, or imports from customer_attraction.
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / 'examples/customer_attraction/optimal_last_query_failure.json'
CERT = ROOT / 'evidence/certificates/customer_attraction/optimal_last_query_failure.json'


def audit():
    data = json.loads(INPUT.read_text())
    cert = json.loads(CERT.read_text())
    p, n = len(data['topics']), data['players']
    customers = tuple((frozenset(t['topics']), t['multiplicity']) for t in data['customers'])
    assert (p, n) == (7, 4)
    assert len(customers) == 127
    assert all(isinstance(w, int) and w > 0 for _, w in customers)
    assert sum(w for _, w in customers) == 1651
    policy = {tuple(e['history']): e['action'] for e in cert['strategy']['actions']}
    histories = {h for k in range(n) for h in product(range(p), repeat=k)}
    assert set(policy) == histories
    assert len(policy) == len(cert['strategy']['actions'])
    assert all(a in range(p) for a in policy.values())

    def utility(a, path):
        return sum((F(w, sum(b in B for b in path)) for B, w in customers if a in B), F())

    def welfare(path):
        return sum(w for B, w in customers if any(b in B for b in path))

    def follow(h):
        while len(h) < n:
            h = h + (policy[h],)
        return h

    comparisons, ties, minimum = 0, 0, None
    for h in sorted(histories, key=lambda t: (len(t), t)):
        a = policy[h]
        own = utility(a, follow(h))
        for b in range(p):
            difference = own - utility(b, follow(h + (b,)))
            assert difference >= 0, (h, a, b, difference)
            comparisons += 1
            ties += difference == 0
            minimum = difference if minimum is None else min(minimum, difference)

    actual = follow(())
    payoffs = tuple(utility(a, actual) for a in actual)
    W = welfare(actual)
    terminals = tuple(combinations_with_replacement(range(p), n))
    O = max(welfare(s) for s in terminals)
    optimal = tuple(s for s in terminals if welfare(s) == O)
    background = actual[:-1]
    query = tuple(utility(a, background + (a,)) for a in range(p))
    sums = tuple(sum((query[a] for a in s), F()) for s in optimal)
    assert actual == (4, 6, 0, 2)
    assert payoffs == (F(390), F(389), F(390), F(390))
    assert W == sum(payoffs) == 1559
    assert O == 1562 and optimal == ((1, 2, 3, 5),)
    assert query == (F(884, 3), F(390), F(390), F(390), F(884, 3), F(390), F(884, 3))
    assert sums == (F(1560),) and min(sums) > W

    # Regenerate the unit-customer instance from the four signed potential entries.
    table = [0] * (1 << p)
    for mask, value in cert['construction']['subset_potential'].items():
        table[int(mask)] = value
    assert {i: v for i, v in enumerate(table) if v} == {14: -1, 21: 1, 44: -1, 88: 1}
    coefficients = table.copy()
    for a in range(p):
        for mask in range(1 << p):
            if mask & (1 << a):
                coefficients[mask] -= coefficients[mask ^ (1 << a)]
    signed = [(-1) ** (mask.bit_count() + 1) * mask.bit_count() * coefficients[mask]
              for mask in range(1 << p)]
    for a in range(p):
        for mask in range(1 << p):
            if not mask & (1 << a):
                signed[mask] -= signed[mask | (1 << a)]
    multiplicities = {sum(1 << a for a in B): w for B, w in customers}
    assert cert['construction']['uniform_bias'] == 13
    assert all(multiplicities[B] == signed[B] + 13 for B in range(1, 1 << p))
    assert min(signed[1:]) == -12 and max(signed[1:]) == 8
    harmonic = [sum((F(1, j) for j in range(1, k + 1)), F()) for k in range(p + 1)]
    for mask in range(1 << p):
        assert sum((signed[B] * harmonic[(B & mask).bit_count()]
                    for B in range(1, 1 << p)), F()) == table[mask]

    # A static dual confirms this example does not refute either mixed-security bridge.
    dual_backgrounds = tuple(combinations(range(p), n - 1))
    dual_rows = tuple(sum((utility(a, b + (a,)) for b in dual_backgrounds), F())
                      / len(dual_backgrounds) for a in range(p))
    cap = max(dual_rows)
    assert cap == F(4889, 14) < min(payoffs)
    expected = cert['expected']
    assert expected['actual'] == list(actual)
    assert expected['payoffs'] == list(map(str, payoffs))
    assert expected['welfare'] == W and expected['optimum'] == O
    assert expected['last_prefix'] == list(background)
    assert expected['last_query_values'] == list(map(str, query))
    assert expected['optimal_multisets'] == list(map(list, optimal))
    assert expected['optimal_last_query_sums'] == list(map(str, sums))
    assert expected['minimum_optimal_last_query_sum'] == str(min(sums))
    assert expected['security_dual']['row_values'] == list(map(str, dual_rows))
    assert expected['security_dual']['cap'] == str(cap)

    return {'claim': 'CA-OPTIMAL-LAST-QUERY-SUM-NO',
            'input_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
            'certificate_sha256': hashlib.sha256(CERT.read_bytes()).hexdigest(),
            'unit_customers': sum(w for _, w in customers), 'customer_types': len(customers),
            'players': n, 'topics': p, 'ordered_nodes': len(histories),
            'action_comparisons': comparisons, 'ties': ties, 'minimum_slack': str(minimum),
            'actual': list(actual), 'payoffs': list(map(str, payoffs)),
            'welfare': W, 'optimum': O, 'terminal_multisets_checked': len(terminals),
            'optimal_multisets': list(map(list, optimal)), 'last_prefix': list(background),
            'last_query_values': list(map(str, query)), 'optimal_query_sum': str(min(sums)),
            'failed_bridge_gap': str(min(sums) - W), 'boolean_potential_checks': 1 << p,
            'static_dual_backgrounds': len(dual_backgrounds), 'static_dual_cap': str(cap),
            'actual_minimum_minus_dual_cap': str(min(payoffs) - cap),
            'scope': 'Complete SPE counterexample to the optimal last-query-sum bridge only.'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    result = audit()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as output:
            output.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
