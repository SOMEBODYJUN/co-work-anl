"""Bounded discovery attack on an auxiliary pairwise leader-security lemma.

For each generated complete BI policy, optimize the entire symmetric matrix
cone G_aa=1, 0<=G_ab<=1, retaining all true continuation inequalities.
One fixed query p gives a legal upper bound H<=max_b (Gp)_b on overlap
security. A positive leadercost-(n-1)H would refute the auxiliary lemma.
Nothing here is an original CAG counterexample or a proof.
"""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import linprog


def build_policy(G, n):
    k = len(G)
    actions = {}
    @lru_cache(None)
    def finish(h):
        if sum(h) == n:
            return h
        choices = []
        for a in range(k):
            ha = list(h); ha[a] += 1
            c = finish(tuple(ha))
            cost = sum(c[b]*G[a,b] for b in range(k))-G[a,a]
            choices.append((cost, a, c))
        _, a, c = min(choices)
        actions[h] = a
        return c
    z = finish((0,)*k)
    return z, actions, finish


def attack(G, n, p):
    k = len(G)
    edges = list(combinations(range(k), 2))
    index = {e:j for j,e in enumerate(edges)}
    d = len(edges)
    z, actions, finish = build_policy(G, n)
    def row(a, c):
        r = np.zeros(d+1)
        for b in range(k):
            if b != a:
                r[index[tuple(sorted((a,b)))]] += c[b]
        return r, c[a]-1
    rows, rhs = [], []
    for h, a in actions.items():
        here, ch = row(a, finish(h))
        for b in range(k):
            hb = list(h); hb[b] += 1
            alt, ca = row(b, finish(tuple(hb)))
            rows.append(here-alt); rhs.append(ca-ch)
    for b in range(k):
        r = np.zeros(d+1); r[-1] = -1
        for a in range(k):
            if a != b:
                r[index[tuple(sorted((a,b)))]] += p[a]
        rows.append(r); rhs.append(-p[b])
    root = actions[(0,)*k]
    obj, const = row(root, z)
    obj[-1] = -(n-1)
    res = linprog(-obj, A_ub=rows, b_ub=rhs,
                  bounds=[(0,1)]*d+[(0,1)], method='highs')
    if not res.success:
        raise RuntimeError(res.message)
    H = np.eye(k)
    for (a,b), x in zip(edges, res.x[:-1]): H[a,b]=H[b,a]=x
    return dict(gap=-res.fun+const, n=n, p=p.tolist(), matrix=H.tolist(),
                security_overlap_upper=res.x[-1], root=root, terminal=list(z),
                policy=[dict(history=list(h),action=a) for h,a in actions.items()],
                matrix_rows=len(rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=100)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    rng = np.random.default_rng(701)
    best = None
    summary = []
    for n in range(3,7):
        local = None
        for t in range(args.trials):
            k=6
            G=rng.integers(0,10,size=(k,k))
            G=np.tril(G,-1)+np.tril(G,-1).T+10*np.eye(k,dtype=np.int64)
            p=np.ones(k)/k if t%2==0 else rng.dirichlet(np.ones(k))
            rec=attack(G,n,p)
            rec['trial']=t
            if local is None or rec['gap']>local['gap']:local=rec
            if rec['gap']>1e-7:
                best=rec;break
        summary.append(dict(n=n,trials=t+1,maximum_gap=local['gap']))
        if best:break
    report=dict(scope='finite floating discovery only; auxiliary pairwise game',
                summary=summary,positive_candidate=best)
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
