"""Optimizer-free reconstruction of the strict HI path-price certificate."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
obj = json.loads((HERE/'interval_price_strict_candidate.json').read_text())
ins = obj['instance']
p, m = len(ins['topics']), ins['players']
types = [(frozenset(c['topics']), c['multiplicity']) for c in ins['customers']]
zero = (0,)*p


def add(b, a):
    return b[:a]+(b[a]+1,)+b[a+1:]


@lru_cache(None)
def utility(q):
    out = []
    for a in range(p):
        out.append(sum((F(w, sum(q[j] for j in B))
                        for B, w in types if a in B and q[a]), F()))
    return tuple(out)


def welfare(q):
    return sum(w for B, w in types if any(q[a] for a in B))


floors, allowed = {}, {}
@lru_cache(None)
def HI(b):
    if sum(b) == m:
        return frozenset({b})
    children = [HI(add(b, a)) for a in range(p)]
    L = max(min(utility(q)[a] for q in children[a]) for a in range(p))
    E = [a for a in range(p) if max(utility(q)[a] for q in children[a]) >= L]
    floors[b], allowed[b] = L, E
    return frozenset(q for a in E for q in children[a])


@lru_cache(None)
def SPE(b):
    if sum(b) == m:
        return frozenset({b})
    children = [SPE(add(b, a)) for a in range(p)]
    L = max(min(utility(q)[a] for q in children[a]) for a in range(p))
    return frozenset(q for a in range(p) for q in children[a] if utility(q)[a] >= L)


HI(zero)
paths = []
def walk(b, actions, edges):
    if sum(b) == m:
        paths.append((tuple(actions), b, tuple(edges)))
        return
    for a in allowed[b]:
        walk(add(b, a), actions+[a], edges+[(b, a)])
walk(zero, [], [])

lambdas = {(tuple(x['b']), x['a']): F(x['lambda']) for x in obj['dual_nonzero']}
assert all(x >= 0 for x in lambdas.values())
beta = F(obj['exact_price_value'])
groups = defaultdict(list)
violating_paths = []
for actions, q, edges in paths:
    u = utility(q)
    price = F(welfare(q))+sum((lambdas.get((b, a), F())*(floors[b]-u[a])
                              for b, a in edges), F())
    assert price >= beta
    assert sum(q[a]*u[a] for a in range(p)) == welfare(q)
    groups[q].append((price, actions))
    if welfare(q) == 25:
        violating_paths.append({'actions': actions,
                                'floor_deficits': [{'b': b, 'a': a,
                                                    'L_minus_U': str(floors[b]-u[a]),
                                                    'lambda': str(lambdas.get((b, a), F()))}
                                                   for b, a in edges if floors[b] > u[a]],
                                'priced_value': str(price)})

weights = {tuple(x['actions']): F(x['weight']) for x in obj['primal_nonzero']}
assert sum(weights.values()) == 1 and all(x >= 0 for x in weights.values())
edges = {e for _, _, es in paths for e in es}
for edge in edges:
    margin = sum((weights.get(actions, F())*(utility(q)[edge[1]]-floors[edge[0]])
                  for actions, q, es in paths if edge in es), F())
    assert margin >= 0
assert sum((weights.get(actions, F())*welfare(q) for actions, q, _ in paths), F()) == beta
exact = SPE(zero)
assert min(welfare(q) for q in exact) == beta
assert len(exact) == 1
assert all(any((a in B) != (b in B) for B, w in types)
           for a in range(p) for b in range(a+1, p))
report = {'status': 'all checks exact; no optimizer or canonical equilibrium core imported',
          'path_count': len(paths), 'true_SPE_terminal_counts': sorted(exact),
          'price_bound': str(beta),
          'priced_edges': [{'b': b, 'a': a, 'L': str(floors[b]), 'lambda': str(lam)}
                           for (b, a), lam in sorted(lambdas.items())],
          'HI_terminals': [{'q': q, 'W': welfare(q),
                            'minimum_price': str(min(x[0] for x in group)),
                            'paths': len(group)} for q, group in sorted(groups.items())],
          'low_W_paths': violating_paths}
(HERE/'interval_price_strict_audit.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
