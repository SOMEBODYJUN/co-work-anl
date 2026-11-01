"""Exact expanded-client audit of the strict unique-SPE selector counterexample.

No canonical game classes, equilibrium solver, certificate verifier, NumPy, or
LP software are imported. Strictness at every node proves uniqueness backwards.
"""
import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', type=Path,
                    default=Path(__file__).with_name('last_average_selection_small_certificate.json'))
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    source = json.loads(args.input.read_text())
    obj = source['instance']
    k, n = len(obj['topics']), obj['players']
    clients = [frozenset(t['topics']) for t in obj['customers']
               for _ in range(t['multiplicity'])]
    policy = {tuple(r['history']): r['action'] for r in source['certificate']['actions']}
    histories = [h for d in range(n) for h in product(range(k), repeat=d)]
    assert len(policy) == len(source['certificate']['actions'])
    assert set(policy) == set(histories)

    def terminal(h):
        while len(h) < n:
            h += (policy[h],)
        return h

    def utilities(a):
        answer = [Fraction() for _ in a]
        for client in clients:
            hit = [i for i, topic in enumerate(a) if topic in client]
            for i in hit:
                answer[i] += Fraction(1, len(hit))
        return tuple(answer)

    def welfare(a):
        return sum(any(topic in client for topic in a) for client in clients)

    rows, margins = [], []
    for h in histories:
        action = policy[h]
        values = [utilities(terminal(h+(a,)))[len(h)] for a in range(k)]
        for a in range(k):
            if a == action:
                assert values[action] == values[a]
            else:
                # Strictness is crucial: it excludes every alternative SPE,
                # inductively from final nodes to the root.
                assert values[action] > values[a], (h, a, values)
                margins.append(values[action]-values[a])
        rows.append({'history': list(h), 'chosen': action,
                     'values': [str(v) for v in values]})

    path = terminal(())
    U, W = utilities(path), welfare(path)
    assert path == (1, 2, 1)
    assert U == (Fraction(11, 2), Fraction(5), Fraction(11, 2))
    assert W == 16
    assert n*U[-1] > W
    opt = max(welfare(a) for a in product(range(k), repeat=n))
    assert opt == 16
    report = {'status': 'passed', 'distinct_unit_clients': len(clients),
              'all_ordered_histories': len(histories),
              'spe_comparisons_including_self': len(histories)*k,
              'strict_nonself_comparisons': len(margins),
              'minimum_strict_margin': str(min(margins)),
              'unique_spe_reason': 'At every history the prescribed action strictly exceeds all alternatives; backward induction gives one complete SPE.',
              'unique_spe_path': path, 'utilities': [str(v) for v in U],
              'welfare': W, 'opt': opt,
              'last_minus_mean': str(U[-1]-Fraction(W,n)),
              'half_coverage_margin': 2*W-opt,
              'refuted': 'Some minimum-welfare SPE has last utility at most W/n.',
              'not_refuted': 'Some minimum-welfare SPE has last utility at most W/(n-1).',
              'all_node_values': rows}
    print(json.dumps({k:v for k,v in report.items() if k != 'all_node_values'}, indent=2))
    if args.output:
        with args.output.open('x') as f:
            json.dump(report, f, indent=2)
            f.write('\n')


if __name__ == '__main__':
    main()
