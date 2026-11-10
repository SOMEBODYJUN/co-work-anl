"""Exact independent check of the fixed saved assignment witness and its two interfaces."""
from fractions import Fraction as Q
from itertools import product, permutations, combinations_with_replacement
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'archives/customer-attraction/tools/evidence/dynamic-exchange/original'
instance = json.loads((BASE / 'assignment_instance.json').read_text())
saved = json.loads((BASE / 'assignment_full_policy.json').read_text())
policy = {tuple(map(int, k.split(','))) if k else (): v for k, v in saved['policy'].items()}
types = [(set(c['topics']), c['multiplicity']) for c in instance['customers']]
p, m = len(instance['topics']), instance['players']

def finish(h):
    h = tuple(h)
    while len(h) < m:
        h += (policy[h],)
    return h

def utility(z, i):
    return sum((Q(weight, sum(a in interests for a in z))
                for interests, weight in types if z[i] in interests), Q())

def welfare(z):
    return sum(weight for interests, weight in types if any(a in interests for a in z))

histories = [h for k in range(m) for h in product(range(p), repeat=k)]
assert set(policy) == set(histories)
slacks = []
for h in histories:
    i = len(h)
    current = utility(finish(h), i)
    for a in range(p):
        slacks.append(current - utility(finish(h + (a,)), i))
assert min(slacks) == 0 and all(s >= 0 for s in slacks)
actual = finish(())
assert list(actual) == saved['actual'] == [0, 3, 4]
W = welfare(actual)
supports = {z: welfare(z) for z in combinations_with_replacement(range(p), m)}
opt = max(supports.values())
optima = [z for z, val in supports.items() if val == opt]
assert W == 1735 and opt == 1740 and optima == [(1, 2, 5)]
J = optima[0]
frozen = [[utility(actual[:i] + (a,) + actual[i+1:], i) for a in J] for i in range(m)]
true = [[utility(finish(actual[:i] + (a,)), i) for a in J] for i in range(m)]
frozen_costs = {','.join(map(str, perm)): sum(frozen[i][J.index(a)] for i, a in enumerate(perm))
                for perm in permutations(J)}
true_costs = {','.join(map(str, perm)): sum(true[i][J.index(a)] for i, a in enumerate(perm))
             for perm in permutations(J)}
assert sorted(frozen_costs.values()) == [1736]*4 + [1737]*2
assert set(true_costs.values()) == {Q(1734)}
assert len(histories) == 43 and len(slacks) == 258
report = {
    'scope': 'Fixed saved 1953-customer witness only; all 43 histories, all 258 real IC comparisons, all 56 optimal multisets, six frozen and six true-prefix assignments. No LP or general compiler completeness claim.',
    'input_sha256': {name: hashlib.sha256((BASE/name).read_bytes()).hexdigest()
                     for name in ['assignment_instance.json', 'assignment_full_policy.json']},
    'histories': len(histories), 'ic_comparisons': len(slacks), 'minimum_slack': str(min(slacks)),
    'customer_count': sum(weight for _, weight in types), 'type_count': len(types),
    'actual': actual, 'utilities': [str(utility(actual, i)) for i in range(m)],
    'W': W, 'OPT': opt, 'optimal_multisets': optima, 'multiset_count': len(supports),
    'frozen_matrix': [[str(x) for x in row] for row in frozen],
    'true_prefix_matrix': [[str(x) for x in row] for row in true],
    'frozen_assignments': {k: str(v) for k, v in frozen_costs.items()},
    'true_prefix_assignments': {k: str(v) for k, v in true_costs.items()},
    'normalized_W': '1', 'normalized_strict_frozen_margin': str(Q(1, W)),
    'true_net_gap': opt-W, 'half_margin': 2*W-opt,
}
out = Path(__file__).with_name('assignment-exact.json')
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ['histories', 'ic_comparisons', 'W', 'OPT', 'true_net_gap', 'half_margin']}))
