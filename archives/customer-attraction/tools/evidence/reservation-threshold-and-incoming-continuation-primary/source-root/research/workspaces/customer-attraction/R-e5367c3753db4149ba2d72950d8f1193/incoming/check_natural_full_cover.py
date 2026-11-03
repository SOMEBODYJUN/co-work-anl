"""Stress one general incoming-payment claim using named existing full SPEs.

Exact tested claim: if OPT covers every customer (hence actual G=0), some
ordered optimal tuple and owner allocation has ordinary natural action-return
cost K <= W.  No policies or games are generated.  For each fixed ordered tuple,
owners are optimized exactly and independently by customer type; this is exact
even if distinct copies of one type may have different owners.

This script does not assert the claim, and a successful finite check is not
evidence for its universal truth.  Every supplied policy is independently checked
at every ordered history before reporting costs.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[5]


def check(name):
    raw = json.loads((ROOT / 'examples/customer_attraction' / (name+'.json')).read_text())
    cert = json.loads((ROOT / 'evidence/certificates/customer_attraction' / (name+'.json')).read_text())
    cert = cert.get('strategy', cert.get('certificate', cert))
    policy = {tuple(r['history']): r['action'] for r in cert['actions']}
    m, k = raw['players'], len(raw['topics'])
    types = [(frozenset(t['topics']), t['multiplicity']) for t in raw['customers']]
    N = sum(w for _, w in types)
    expected = {h for d in range(m) for h in product(range(k), repeat=d)}
    assert len(policy) == len(cert['actions']) and set(policy) == expected

    @lru_cache(None)
    def finish(h):
        return h if len(h) == m else finish(h+(policy[h],))

    @lru_cache(None)
    def payoff(z, a):
        return sum((F(w, sum(b in likes for b in z)) for likes, w in types if a in likes), F())

    checks = 0
    for h, action in policy.items():
        v = payoff(finish(h), action)
        for a in range(k):
            assert v >= payoff(finish(h+(a,)), a), (name, h, action, a)
            checks += 1
    actual = finish(())
    u = tuple(payoff(actual, a) for a in actual)
    W = sum(u, F())
    R = [j for j, (likes, _) in enumerate(types) if not any(a in likes for a in actual)]
    assert W.denominator == 1
    opt = []
    for T in combinations_with_replacement(range(k), m):
        cov = sum(w for likes, w in types if any(a in likes for a in T))
        if cov == N:
            opt.append(T)
    assert opt, 'This test is restricted to the precise full-cover diagnostic.'

    @lru_cache(None)
    def price(j, i, a):
        likes = types[j][0]
        assert a in likes and j in R
        z = finish(actual[:i]+(a,))
        D = payoff(z, a)
        future = [l for l in range(i+1, m) if z[l] in likes]
        c = 1 + len(future)
        assert 0 < D <= u[i]
        return (u[i]/D + sum((price(j, l, z[l]) for l in future), F()))/c

    best = None
    worst = None
    orders = 0
    for multiset in opt:
        for T in sorted(set(permutations(multiset))):
            owners = {j: min((i for i, a in enumerate(T) if a in types[j][0]),
                             key=lambda i: (price(j, i, T[i]), i)) for j in R}
            cost = sum((types[j][1]*price(j, i, T[i]) for j, i in owners.items()), F())
            row = (cost, T, owners)
            if best is None or row[0] < best[0]:
                best = row
            if worst is None or row[0] > worst[0]:
                worst = row
            orders += 1
    b, T, owners = best
    return dict(case=name, exact_claim='existence of ordinary natural K<=W with all optimal orders and all owners; full-cover case',
                status='precise obstruction' if b > W else 'finite diagnostic only; no obstruction',
                players=m, topics=k, customers=N, ordered_histories=len(policy), original_IC_checks=checks,
                actual=actual, payoffs=list(map(str, u)), W=str(W), OPT=N,
                optimal_multisets=len(opt), optimal_orders=orders,
                minimum_natural_cost=str(b), minimum_tax=str(b-(N-W)),
                half_slack=str(2*W-N), cost_minus_W=str(b-W),
                best_order=T, best_owners_by_type=owners,
                worst_order_cost_with_best_owners=str(worst[0]), worst_order=worst[1])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cases', nargs='+')
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    rows = [check(name) for name in args.cases]
    body = json.dumps(rows, indent=2)+'\n'
    if args.out:
        args.out.write_text(body)
    print(body)
