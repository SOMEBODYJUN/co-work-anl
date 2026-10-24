"""Independent raw-type audit of the fixed-background zero-regret repair witness.

No solver or author search code imported. Enumerates all last-player best replies,
all legal full contingent last-player policies and first-player best replies.
"""
import hashlib
import json
from fractions import Fraction
from itertools import product
from pathlib import Path

source = Path(__file__).resolve().parents[1] / 'new_cross_branch/zero_repair_simplified.json'
raw = source.read_bytes()
d = json.loads(raw)
w = d['weights']
n = 4
canonical = json.loads((source.parent / 'zero_regret_repair_witness.json').read_text())
canonical_weights = [0] * (1 << n)
for customer in canonical['customers']:
    mask = sum(1 << a for a in customer['topics'])
    canonical_weights[mask] += customer['multiplicity']
assert canonical_weights == w
assert canonical['old_background'] == [1,0,0,0]
assert canonical['old_tail_strategy']['last_after_first'] == d['old_policy']

def payoff(topic, leaf):
    return sum((Fraction(mult, sum(bool(mask & (1 << a)) for a in leaf))
                for mask, mult in enumerate(w) if mask & (1 << topic)), Fraction(0))

def welfare(leaf):
    return sum(mult for mask, mult in enumerate(w)
               if any(mask & (1 << a) for a in leaf))

def check(background, policy):
    prefix = [] if background is None else [background]
    br = [tuple(b for b in range(n)
                if payoff(b, prefix + [a,b]) ==
                max(payoff(c, prefix + [a,c]) for c in range(n)))
          for a in range(n)]
    branches = [prefix + [a,policy[a]] for a in range(n)]
    first = [payoff(a, branches[a]) for a in range(n)]
    return br, branches, first

old_policy = tuple(d['old_policy'])
old_br, old_leaves, old_first = check(d['background'],old_policy)
assert all(old_policy[a] in old_br[a] for a in range(n))
assert d['path'] == [2,1] and old_policy[2] == 1
assert old_first[2] == max(old_first)
assert welfare(old_leaves[2]) == 18

new_br, projected, old_deleted_first = check(None,old_policy)
assert old_policy[2] in new_br[2]
assert old_deleted_first[2] == max(old_deleted_first)
assert welfare(projected[2]) == 17

all_spe = []
for last_policy in product(*new_br):
    br, branches, first = check(None,last_policy)
    assert all(last_policy[a] in br[a] for a in range(n))
    for a in range(n):
        if first[a] == max(first):
            all_spe.append((a,last_policy[a],welfare(branches[a]),str(first[a])))
assert new_br == [(2,), (3,), (1,), (1,)]
assert set(all_spe) == {(3,1,16,'9')}

print(json.dumps({
    'source_sha256': hashlib.sha256(raw).hexdigest(),
    'canonical_source_sha256': hashlib.sha256((source.parent / 'zero_regret_repair_witness.json').read_bytes()).hexdigest(),
    'old_background': d['background'],
    'old_best_reply_menus': old_br,
    'old_actual_first_payoff': str(old_first[2]),
    'old_actual_total_welfare_including_background': welfare(old_leaves[2]),
    'deleted_projected_first_payoffs': list(map(str,old_deleted_first)),
    'deleted_projected_actual_node_regret': str(max(old_deleted_first)-old_deleted_first[2]),
    'deleted_projected_welfare': welfare(projected[2]),
    'deleted_exact_best_reply_menus': new_br,
    'deleted_all_pure_spe_outcomes': sorted(set(all_spe)),
}, indent=2))
