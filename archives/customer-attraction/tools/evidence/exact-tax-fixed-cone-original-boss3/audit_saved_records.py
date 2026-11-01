"""Read every saved field and verify the saved full policy over unit customers.

Standard library only. This is a new audit of frozen data, not a rerun of the
historical 53-cone LP search and not a certificate of any LP upper bound.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json


def audit():
    base = Path(__file__).resolve().parent
    manifest = json.loads((base / 'source-manifest.json').read_text())
    for item in manifest:
        data = (base / item['local_path']).read_bytes()
        assert len(data) == item['size']
        assert hashlib.sha256(data).hexdigest() == item['sha256']
    report = json.loads((base / 'original/results.json').read_text())
    assert set(report) == {'status', 'records'}
    assert report['status'] == 'finite fixed-cone attack only'
    records = report['records']
    queries = []
    records_by_m = Counter()
    queries_by_m = Counter()
    gaps = Counter()
    detailed = []
    sources = set()
    for index, record in enumerate(records, 1):
        assert set(record) == {'source', 'm', 'p', 'root', 'scores'}
        m, p, root = record['m'], record['p'], record['root']
        assert 1 <= m <= 5 and 1 <= p <= 7
        assert sum(p ** depth for depth in range(m)) <= 3000
        assert len(root) == p and all(type(x) is int and x >= 0 for x in root)
        assert sum(root) == m
        assert record['source'] not in sources
        sources.add(record['source'])
        assert [s['query'] for s in record['scores']] == list(range(p))
        records_by_m[m] += 1
        exact_gaps = []
        for score in record['scores']:
            assert set(score) == {'query', 'gap', 'floating_gap', 'exact_primal'}
            assert score['exact_primal'] is True
            gap = F(score['gap'])
            assert gap <= 0
            # The floating optimum remains a floating historical observation.
            assert abs(float(gap) - score['floating_gap']) < 1e-10
            gaps[str(gap)] += 1
            queries_by_m[m] += 1
            exact_gaps.append(str(gap))
            queries.append((gap, record['source'], score['query']))
        detailed.append({'record': index, 'source': record['source'], 'm': m,
                         'p': p, 'root': root, 'reported_exact_primal_gaps': exact_gaps})

    best = json.loads((base / 'original/best.json').read_text())
    assert set(best) == {'source', 'm', 'p', 'query', 'gap', 'root', 'integer_clones', 'actions'}
    m, p = best['m'], best['p']
    assert (m, p) == (5, 7)
    clones = best['integer_clones']
    assert len(clones) == 2 ** p - 1
    assert all(type(n) is int and n >= 0 for n in clones)
    assert [(mask, n) for mask, n in enumerate(clones, 1) if n] == [(127, 1)]
    actions = {}
    histogram = Counter()
    for item in best['actions']:
        assert set(item) == {'history', 'action'}
        h, a = tuple(item['history']), item['action']
        assert h not in actions
        assert all(type(b) is int and 0 <= b < p for b in h)
        assert type(a) is int and 0 <= a < p
        actions[h] = a
        histogram[len(h), a] += 1
    required = {h for depth in range(m) for h in product(range(p), repeat=depth)}
    assert set(actions) == required

    @lru_cache(None)
    def leaf(h):
        return h if len(h) == m else leaf(h + (actions[h],))

    customers = [tuple(a for a in range(p) if mask & (1 << a))
                 for mask, count in enumerate(clones, 1) for _ in range(count)]

    def payoff(terminal, selected):
        return sum((F(1, sum(a in interested for a in terminal))
                    for interested in customers if selected in interested), F(0))

    checked = 0
    minimum = None
    for h in sorted(required, key=lambda h: (len(h), h)):
        actual = payoff(leaf(h), actions[h])
        for a in range(p):
            difference = actual - payoff(leaf(h + (a,)), a)
            assert difference >= 0
            minimum = difference if minimum is None else min(minimum, difference)
            checked += 1
    terminal = leaf(())
    root = [terminal.count(a) for a in range(p)]
    assert root == best['root']
    loads = [sum(a in interested for a in terminal) for interested in customers]
    welfare = sum(c > 0 for c in loads)
    alpha = F(m - 1, m)
    g = [sum((F(1) / (1 + alpha * c) for interested, c in zip(customers, loads)
              if a in interested), F(0)) for a in range(p)]
    G = sum((F(1) / (1 + alpha * c) for c in loads if c), F(0))
    gap = m * g[best['query']] - welfare - G
    assert welfare == 1 and gap == F(best['gap']) == -F(1, 5)
    largest = max(gap for gap, _, _ in queries)
    assert largest == F(best['gap'])
    matching = [r for r in records if r['source'] == best['source']]
    assert len(matching) == 1 and matching[0]['root'] == root
    assert matching[0]['scores'][best['query']]['gap'] == best['gap']
    return {
        'scope': 'new exact saved-data audit; no historical LP rerun or upper-bound claim',
        'source_hashes_checked': len(manifest),
        'records': len(records), 'queries': len(queries),
        'records_by_m': dict(sorted(records_by_m.items())),
        'queries_by_m': dict(sorted(queries_by_m.items())),
        'reported_gap_histogram': dict(sorted(gaps.items())),
        'record_details': detailed,
        'saved_best': {
            'source': best['source'], 'players': m, 'labels': p,
            'nonzero_customer_types': [[127, 1]], 'unit_customers': len(customers),
            'ordered_decision_histories': len(actions),
            'history_action_histogram': [list(k) + [v] for k, v in sorted(histogram.items())],
            'all_action_comparisons_including_self': checked,
            'nonself_comparisons': len(actions) * (p - 1),
            'minimum_deviation_slack': str(minimum),
            'root_path': terminal, 'root_counts': root,
            'actual_player_payoffs': [str(payoff(terminal, a)) for a in terminal],
            'welfare': welfare, 'g': [str(v) for v in g], 'G': str(G),
            'query': best['query'], 'gap': str(gap),
            'all_labels_have_identical_coverage': True,
        },
        'historical_other_query_vectors_saved': False,
        'historical_exact_dual_certificates_saved': False,
        'universal_tax_bridge_verified': False,
        'six_player_half_verified': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = audit()
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        with args.out.open('x') as output:
            output.write(text)
        print(json.dumps({k: v for k, v in result.items() if k != 'record_details'}, ensure_ascii=False))
    else:
        print(text, end='')
