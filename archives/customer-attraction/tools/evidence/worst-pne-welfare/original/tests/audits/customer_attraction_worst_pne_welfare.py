"""Independent client-expanded audit of the boss's 16-client bridge example.

Uses neither customer_attraction nor its count-cache or verifier. Every payoff
is recomputed by iterating the sixteen distinct unit clients. This script is a
finite certificate check, not an argument about general half coverage.
"""
from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    repo = Path(__file__).resolve().parents[2]
    parser.add_argument('--instance', type=Path,
                        default=repo / 'examples/customer_attraction/worst_pne_welfare_failure.json')
    parser.add_argument('--certificate', type=Path,
                        default=repo / 'evidence/certificates/customer_attraction/worst_pne_welfare_failure.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    obj = json.loads(args.instance.read_text())
    data = {'instance': obj, 'certificate': json.loads(args.certificate.read_text())}
    k, n = len(obj['topics']), obj['players']
    clients = [frozenset(t['topics']) for t in obj['customers']
               for _ in range(t['multiplicity'])]
    policy = {tuple(r['history']): r['action']
              for r in data['certificate']['actions']}
    histories = [h for d in range(n) for h in product(range(k), repeat=d)]
    assert set(policy) == set(histories)

    def terminal(h):
        while len(h) < n:
            h = h + (policy[h],)
        return h

    def payoffs(a):
        pay = [Fraction() for _ in a]
        for client in clients:
            hit = [i for i, topic in enumerate(a) if topic in client]
            for i in hit:
                pay[i] += Fraction(1, len(hit))
        return tuple(pay)

    def welfare(a):
        return sum(any(topic in client for topic in a) for client in clients)

    comparisons = []
    for h in histories:
        chosen = terminal(h)
        actual = payoffs(chosen)[len(h)]
        for action in range(k):
            branch = terminal(h + (action,))
            deviation = payoffs(branch)[len(h)]
            assert actual >= deviation, (h, action, actual, deviation)
            comparisons.append({'history': list(h), 'action': action,
                                'actual': str(actual), 'deviation': str(deviation)})

    all_static = []
    pne = []
    for a in combinations_with_replacement(range(k), n):
        counts = tuple(a.count(topic) for topic in range(k))
        utilities = payoffs(a)
        profitable = []
        for i in range(n):
            for topic in range(k):
                b = a[:i] + (topic,) + a[i+1:]
                gain = payoffs(b)[i] - utilities[i]
                if gain > 0:
                    profitable.append((i, topic, str(gain)))
        record = {'counts': counts, 'welfare': welfare(a),
                  'pne': not profitable, 'profitable_deviations': profitable}
        all_static.append(record)
        if not profitable:
            pne.append(record)

    path = terminal(())
    assert path == (0, 3, 3)
    assert welfare(path) == 15
    assert len(all_static) == 20
    assert {tuple(r['counts']) for r in pne} == {(0, 1, 1, 1), (0, 1, 0, 2)}
    assert {r['welfare'] for r in pne} == {16}
    opt = max(r['welfare'] for r in all_static)
    assert opt == 16
    report = {
        'status': 'passed', 'distinct_unit_clients': len(clients),
        'complete_histories': len(histories), 'spe_comparisons_including_self': len(comparisons),
        'terminal_path': path, 'terminal_payoffs': [str(x) for x in payoffs(path)],
        'terminal_welfare': welfare(path), 'static_count_vectors': len(all_static),
        'static_pne': pne, 'opt': opt,
        'conclusion': 'SPE welfare 15 is below every static PNE welfare 16; half coverage holds.',
        'scope': 'This finite certificate refutes only SPE-to-worst-PNE welfare domination.',
        'spe_comparisons': comparisons, 'static_profiles': all_static,
    }
    if args.output:
        with args.output.open('x') as target:
            target.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in report if k not in ('spe_comparisons', 'static_profiles')}, indent=2))


if __name__ == '__main__':
    main()
