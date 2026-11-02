"""Structure binding only: no payoff, IC, BI, LP or random generation."""
import argparse
from itertools import combinations_with_replacement
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--evidence-dir', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    sources = [('2257ca523887f632a454', 'cyclic_deletion_k6n5.json'),
               ('356f3beabec287d9eddb', 'cyclic_deletion_k7n4.json'),
               ('be85e59a1d7e43ea8126', 'cyclic_deletion_k8n5.json')]
    records = []
    for source_id, name in sources:
        d = json.loads((args.evidence_dir / 'original' / source_id / name).read_text())
        k, n, best = d['k'], d['n'], d['best']
        expected = {tuple(word.count(a) for a in range(k))
                    for depth in range(n)
                    for word in combinations_with_replacement(range(k), depth)}
        keys = [tuple(r['counts']) for r in best['policy']]
        assert len(keys) == len(set(keys)) and set(keys) == expected
        assert all(set(r) == {'counts', 'action'} and 0 <= r['action'] < k
                   for r in best['policy'])
        policy = {tuple(r['counts']): r['action'] for r in best['policy']}
        history = []
        counts = [0] * k
        for _ in range(n):
            a = policy[tuple(counts)]
            history.append(a)
            counts[a] += 1
        assert counts == best['terminal']
        assert best['weights'][-1] == 1 and all(w == 0 for w in best['weights'][:-1])
        assert d['orbits'][-1] == (1 << k) - 1
        records.append({'source_id': source_id, 'k': k, 'n': n,
                        'records': len(keys), 'complete_count_keys': True,
                        'duplicate_count_keys': 0, 'all_actions_legal': True,
                        'derived_ordered_root_path': history,
                        'declared_terminal_counts': counts,
                        'only_nonzero_weight_full_interest_type': True})
    report = {'identity': 'preserved cyclic policy structure binding only',
              'payoff_or_IC_checks': 0, 'BI_or_optimizer_calls': 0,
              'random_inputs_generated': 0, 'results': records,
              'total_policy_records': sum(r['records'] for r in records)}
    with args.output.open('x') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
