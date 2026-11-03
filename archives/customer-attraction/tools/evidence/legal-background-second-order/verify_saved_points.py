"""Audit only two frozen pairwise points, without running discovery or finite-B SPE."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def check(record, uniform):
    K, r = record['K'], record['r']
    masks = record['masks']
    weights = list(map(lambda x: F(str(x)), record['weights']))
    P = [1] * K if uniform else record['P']
    ds = [sum(P[a] for a in range(K) if mask >> a & 1) for mask in masks]
    leading = [sum((w / d for mask, w, d in zip(masks, weights, ds)
                    if mask >> a & 1), F(0)) for a in range(K)]
    C = [[sum((w / (d*d) for mask, w, d in zip(masks, weights, ds)
               if mask >> a & 1 and mask >> b & 1), F(0))
          for b in range(K)] for a in range(K)]
    actions = {tuple(x['history']): x['action'] for x in record['actions']}
    expected = {h for length in range(r) for h in product(range(K), repeat=length)}
    assert set(actions) == expected

    def terminal(h):
        while len(h) < r:
            h += (actions[h],)
        return h

    comparisons = []
    for h, a in actions.items():
        z = terminal(h + (a,))
        cost = sum((C[a][b] for b in z), F(0))
        for b in range(K):
            alternate = terminal(h + (b,))
            comparisons.append(sum((C[b][c] for c in alternate), F(0))-cost)
    z = terminal(())
    assert list(z) == record['z']
    p = [F(1, K)] * K if uniform else list(map(lambda x: F(str(x)), record['query']))
    assert sum(p) == 1
    security_upper = max(sum((p[a]*(C[a][a]+(r-1)*C[a][b])
                              for a in range(K)), F(0)) for b in range(K))
    actual = sum((C[z[0]][b] for b in z), F(0))
    return dict(uniform=uniform, r=r, K=K, histories=len(actions),
                comparisons_including_self=len(comparisons),
                min_cost_difference=str(min(comparisons)),
                leading=list(map(str, leading)),
                actual_root_cost=str(actual), query_upper=str(security_upper),
                excess_over_query_upper=str(actual-security_upper),
                min_weight=str(min(weights)),
                scope='fixed exact rational pairwise points; no discovery LP or finite-B SPE')


if __name__ == '__main__':
    uniform = json.loads((ROOT/'original/d1de014dc093ed268858.json').read_text())
    nonuniform = json.loads((ROOT/'original/075418a816f776aa2bde.json').read_text())
    result = [check(rec, True) for rec in uniform] + [check(nonuniform, False)]
    print(json.dumps(result, ensure_ascii=False, indent=2))
