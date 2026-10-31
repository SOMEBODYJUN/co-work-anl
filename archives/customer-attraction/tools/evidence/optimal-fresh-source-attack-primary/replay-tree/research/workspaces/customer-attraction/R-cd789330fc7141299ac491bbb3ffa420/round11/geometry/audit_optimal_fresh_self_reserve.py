"""Bounded refutation audit of a precisely stated general sufficient helper.

No new equilibria are synthesized. Existing named root certificates are read;
this script does not independently certify their SPE property. It checks only
their frozen counts against the optimal-tuple self-reserve candidate. Passing
these examples proves no general claim.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).with_suffix('.json')


def solve(instance, counts):
    p = len(instance['topics'])
    m = instance['players']
    if p > 16 or sum(counts) != m:
        return None
    customers = instance['customers']
    g = [Fraction(0) for _ in range(p)]
    welfare = 0
    reserve = Fraction(0)
    for customer in customers:
        liked = customer['topics']
        value = customer.get('multiplicity', 1)
        c = sum(counts[a] for a in liked)
        if c:
            welfare += value
            reserve += Fraction(value, 1 + c)
        for a in liked:
            g[a] += Fraction(value, 1 + c)
    cheapest = min(g)
    opt = -1
    mincost = None
    support_at_min = None
    for k in range(min(m, p) + 1):
        for support in combinations(range(p), k):
            support_set = set(support)
            cover = sum(z.get('multiplicity', 1) for z in customers
                        if support_set.intersection(z['topics']))
            # If k<m and cover=OPT, padding by any legal theme cannot add
            # coverage, or this would contradict maximality of OPT.
            cost = sum((g[a] for a in support), Fraction(0)) + (m-k)*cheapest
            if cover > opt or (cover == opt and cost < mincost):
                opt, mincost, support_at_min = cover, cost, list(support)
    assert mincost is not None
    return {'m': m, 'p': p, 'W': welfare, 'OPT': opt,
            'reserve': str(reserve), 'min_optimal_fresh_sum': str(mincost),
            'self_reserve_margin': str(welfare + reserve - mincost),
            'candidate_holds': mincost <= welfare + reserve,
            'support_at_min': support_at_min}


def main():
    rows = []
    cert_dir = ROOT / 'evidence/certificates/customer_attraction'
    example_dir = ROOT / 'examples/customer_attraction'
    for cert in sorted(cert_dir.glob('*.json')):
        instance_path = example_dir / cert.name
        if not instance_path.exists():
            continue
        try:
            certificate = json.loads(cert.read_text())
            instance = json.loads(instance_path.read_text())
            strategy = certificate.get('strategy', certificate)
            counts = strategy.get('terminal_counts')
            if counts is None:
                continue
            result = solve(instance, counts)
        except (KeyError, TypeError, ValueError):
            continue
        if result is not None:
            rows.append({'source_certificate': str(cert.relative_to(ROOT)),
                         'source_instance': str(instance_path.relative_to(ROOT)),
                         **result})
    report = {'status': 'finite candidate-refutation audit only; no general proof',
              'candidate': 'min_OPT_m tuple sum_j g_actual(T_j) <= W+Rself',
              'certificate_SPE_reverified_here': False, 'rows': rows,
              'counterexamples_found': sum(not r['candidate_holds'] for r in rows)}
    OUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'checked': len(rows),
                      'counterexamples': report['counterexamples_found'],
                      'output': str(OUT)}))


if __name__ == '__main__':
    main()
