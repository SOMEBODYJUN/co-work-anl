"""Exact, limited attack on the two all-input optimal-prefix bill candidates.

This is not a search for a new positive fixed-player theorem. It only reads old
complete-policy certificates with the simple actions-list schema and checks
the explicit general BILL-LOW/BILL-UP assertions from README.md.
"""
import itertools
import json
import argparse
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]


def attack(instance_path, certificate_path):
    ins = json.loads(instance_path.read_text())
    cert = json.loads(certificate_path.read_text())
    if not isinstance(ins, dict) or not isinstance(cert, dict):
        return None
    if not all(k in ins for k in ('topics', 'players', 'customers')):
        return None
    if not isinstance(cert.get('actions'), list):
        return None
    m, p = ins['players'], len(ins['topics'])
    if p ** m > 150000 or sum(p ** k for k in range(m)) > 50000:
        return None
    acts = {tuple(z['history']): z['action'] for z in cert['actions']}
    expected = set(itertools.chain.from_iterable(itertools.product(range(p), repeat=k) for k in range(m)))
    if set(acts) != expected:
        return None
    types = [(set(z['topics']), z['multiplicity']) for z in ins['customers']]

    def finish(h):
        h = tuple(h)
        while len(h) < m:
            h += (acts[h],)
        return h

    def utilities(z):
        ans = [F(0) for _ in range(m)]
        for B, n in types:
            who = [i for i, a in enumerate(z) if a in B]
            if who:
                for i in who:
                    ans[i] += F(n, len(who))
        return ans

    def coverage(z):
        z = set(z)
        return sum(n for B, n in types if B & z)

    nodes = comparisons = 0
    for h in expected:
        i = len(h)
        old = utilities(finish(h))[i]
        for a in range(p):
            assert old >= utilities(finish(h + (a,)))[i]
            comparisons += 1
        nodes += 1
    rule_matched = None
    if instance_path.name == 'prefix_balance_failure.json':
        priority = [2, 1, 0, 3, 4, 5]
        for h in expected:
            if len(h) == 0:
                prescribed = 1
            elif len(h) == 1:
                prescribed = 1 if h[0] == 2 else 2
            elif len(h) == 2:
                prescribed = 1 if h == (2, 2) else 2
            else:
                prescribed = max(priority, key=lambda a: utilities(h + (a,))[3])
            assert acts[h] == prescribed
        rule_matched = True
    actual = finish(())
    W = coverage(actual)
    opt = max(map(coverage, itertools.combinations_with_replacement(range(p), m)))
    by_multiset = []
    for multiset in itertools.combinations_with_replacement(range(p), m):
        if coverage(multiset) != opt:
            continue
        bills = []
        for pi in set(itertools.permutations(multiset)):
            D = sum((utilities(finish(pi[:k]))[k - 1] for k in range(1, m + 1)), F(0))
            bills.append((D, pi))
        lo, hi = min(bills), max(bills)
        row = {'multiset': multiset, 'min': str(lo[0]), 'min_order': lo[1],
                            'max': str(hi[0]), 'max_order': hi[1],
                            'low_failure': 2 * lo[0] < opt,
                            'fixed_multiset_up_failure': lo[0] > W}
        if instance_path.name == 'prefix_balance_failure.json':
            row['all_orders'] = []
            for D, pi in sorted(bills, key=lambda z: z[1]):
                leaves = [finish(pi[:k]) for k in range(1, m + 1)]
                payoffs = [utilities(leaves[k - 1])[k - 1] for k in range(1, m + 1)]
                row['all_orders'].append({'order': pi, 'D': str(D),
                                           'forced_payoffs': list(map(str, payoffs)),
                                           'forced_rollouts': leaves})
        by_multiset.append(row)
    return {'instance': str(instance_path.relative_to(ROOT)), 'm': m, 'p': p,
            'actual': actual, 'W': W, 'OPT': opt, 'nodes': nodes,
            'comparisons': comparisons, 'compact_source_rule_matched': rule_matched,
            'optimal_multisets': by_multiset}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-only', action='store_true')
    args = parser.parse_args()
    if args.source_only:
        instance = ROOT / 'examples/customer_attraction/prefix_balance_failure.json'
        cert = ROOT / 'evidence/certificates/customer_attraction/prefix_balance_failure.json'
        ans = attack(instance, cert)
        out = Path(__file__).with_name('bill_up_failure.json')
        out.write_text(json.dumps(ans, indent=2) + '\n')
        print(json.dumps(ans, indent=2))
        return
    reports = []
    for cert in sorted((ROOT / 'evidence/certificates/customer_attraction').glob('*.json')):
        instance = ROOT / 'examples/customer_attraction' / cert.name
        if not instance.exists():
            continue
        try:
            ans = attack(instance, cert)
        except (KeyError, TypeError, ValueError):
            continue
        if ans is not None:
            reports.append(ans)
    out = Path(__file__).with_name('forcing_bill_old_certificates.json')
    out.write_text(json.dumps(reports, indent=2) + '\n')
    print(json.dumps(reports, indent=2))


if __name__ == '__main__':
    main()
