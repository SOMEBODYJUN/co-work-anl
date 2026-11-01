"""Definition-level independent audit of r4_security's exact pooled-load witness.

Does not import the discovery program, its output, or the old strategy file.
All customers are expanded as separate unit clients.
"""
from fractions import Fraction as F
from itertools import product
import json

COUNTS = {2:82,8:46,9:72,13:6,14:21,16:46,17:12,18:12,19:36,
          21:24,22:9,24:36,32:9,33:10,35:12,36:82,43:27,
          45:21,46:6,51:9,53:57}
CLIENTS = [mask for mask, number in COUNTS.items() for _ in range(number)]
M, K = 3, 6
P = (F(0), F(0), F(1,2), F(0), F(0), F(1,2))

def action(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3,6)
    return next(a for a in group if a not in h)

def finish(h):
    while len(h) < M:
        h += (action(h),)
    return h

def payoff(z, i):
    return sum((F(1, sum((mask >> a) & 1 for a in z))
                for mask in CLIENTS if (mask >> z[i]) & 1), F(0))

def coverage(z):
    return sum(any((mask >> a) & 1 for a in z) for mask in CLIENTS)

def audit():
    gaps = []
    for depth in range(M):
        for h in product(range(K), repeat=depth):
            base = payoff(finish(h), depth)
            for a in range(K):
                gaps.append(base - payoff(finish(h + (a,)), depth))
    assert min(gaps) >= 0
    z = finish(())
    u = tuple(payoff(z, i) for i in range(M))
    w = coverage(z)
    pooled = F(0)
    row_sum = F(0)
    qbar = [F(0) for _ in range(K)]
    for i in range(M):
        for a, pa in enumerate(P):
            y = finish(z[:i] + (a,))
            for j in range(M):
                if j != i:
                    qbar[y[j]] += pa / (M * (M-1))
    for mask in CLIENTS:
        px = sum(P[a] for a in range(K) if (mask >> a) & 1)
        mus = []
        for i in range(M):
            value = F(0)
            for a, pa in enumerate(P):
                y = finish(z[:i] + (a,))
                value += pa * sum((mask >> y[j]) & 1 for j in range(M) if j != i)
            mus.append(value)
        pooled += px / (1 + sum(mus) / M)
        row_sum += sum(px / (1 + mu) for mu in mus)
    background = (0, 2)
    static_values = tuple(sum((F(1, 1 + sum((mask >> b) & 1 for b in background))
                                for mask in CLIENTS if (mask >> a) & 1), F(0))
                          for a in range(K))
    assert len(CLIENTS) == 635
    assert z == (0,3,4) and u == (154,154,154) and w == 462
    assert M*pooled-w == F(40617,340340)
    assert tuple(qbar) == (F(5,12), F(1,6), F(0), F(1,3), F(1,12), F(0))
    assert static_values == (125,154,95,154,154,108)
    return {"unit_clients":len(CLIENTS), "decision_nodes":43, "ic_comparisons":len(gaps),
            "minimum_ic_gap":min(gaps), "actual_path":z, "utilities":u,
            "welfare":w, "optimal_coverage":max(coverage(t) for t in product(range(K), repeat=M)),
            "pooled_competitor_marginal":qbar, "m_times_pooled_query":M*pooled,
            "pooled_minus_welfare":M*pooled-w, "sum_individual_fractional_queries":row_sum,
            "static_background":background, "static_pure_query_values":static_values,
            "static_security_upper_bound":max(static_values),
            "scope":"Only all-p pooled Jensen payment is false; optimal-query payment and HALF remain open."}

if __name__ == "__main__":
    print(json.dumps(audit(), default=str, indent=2))
