"""Definition-level, unit-customer and full ordered-tree check.

Does not import the repository model, solver, certificate code, or the probe.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

p = Path(__file__).with_name('true_reset_floor_counterexample.json')
data = json.loads(p.read_text())
inst = data['instance']
k, m = len(inst['topics']), inst['players']
clients = [frozenset(t['topics']) for t in inst['customers']
           for _ in range(t['multiplicity'])]

def payoff(z, i):
    return sum((F(1, sum(a in c for a in z)) for c in clients
                if z[i] in c), F(0))

def welfare(z):
    return sum(any(a in c for a in z) for c in clients)

actions = {tuple(item['history']): item['action']
           for item in data['certificate']['actions']}
expected = {h for length in range(m)
            for h in product(range(k), repeat=length)}
assert set(actions) == expected

def follow(h):
    while len(h) < m:
        h += (actions[h],)
    return h

actual = follow(())
assert actual == tuple(data['path'])
comparisons = 0
for h in sorted(expected, key=lambda h: (len(h), h)):
    z = follow(h)
    i = len(h)
    for a in range(k):
        assert payoff(z, i) >= payoff(follow(h+(a,)), i), (h, a)
        comparisons += 1

# Full ordered-history outcome recursion in the true (m-1)-player game.
# No ancestor caps; each forced child independently ranges over all SPEs.
n = m-1
@lru_cache(None)
def outcomes(h):
    if len(h) == n:
        return frozenset((h,))
    children = [outcomes(h+(a,)) for a in range(k)]
    mu = max(min(payoff(z, len(h)) for z in child)
             for child in children)
    return frozenset(z for child in children for z in child
                     if payoff(z, len(h)) >= mu)

def floor(h):
    return max(min(payoff(z, len(h)) for z in outcomes(h+(a,)))
               for a in range(k))

target = actual[1:]
floors = tuple(floor(target[:i]) for i in range(n))
profits = tuple(payoff(target, i) for i in range(n))
deficits = tuple(max(F(0), a-b) for a,b in zip(floors, profits))
deleted = payoff(actual, 0)
assert list(map(str, floors)) == data['floors']
assert list(map(str, profits)) == data['new_profits']
assert list(map(str, deficits)) == data['deficits']
assert str(deleted) == data['deleted']
assert sum(deficits) > deleted

result = dict(status='PASS', unit_clients=len(clients),
    original_path=actual, original_welfare=welfare(actual),
    original_payoffs=list(map(str, (payoff(actual,i) for i in range(m)))),
    original_ordered_histories=len(expected), original_IC_comparisons=comparisons,
    deleted_target=target, deleted_target_welfare=welfare(target),
    floors=list(map(str, floors)), profits=list(map(str, profits)),
    positive_floor_deficits=list(map(str, deficits)),
    deficit_sum=str(sum(deficits)), deleted_original_payoff=str(deleted),
    true_smaller_SPE_welfares=sorted({welfare(z) for z in outcomes(())}),
    smaller_full_ordered_states=outcomes.cache_info().currsize)
print(json.dumps(result, indent=2))
