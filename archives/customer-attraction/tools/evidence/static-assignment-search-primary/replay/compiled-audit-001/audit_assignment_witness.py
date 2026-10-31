"""Definition-level exact replay of the disjoint optimal-assignment witness.

No optimizer, canonical model, SPE solver, or canonical verifier is imported.
The source is the saved small integer F/policy. Every full CAG history is
explicitly filled and every action comparison uses Fraction customer shares.
"""
import json
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product
from math import ceil
from pathlib import Path

ROOT = Path(__file__).parent
source = json.loads((ROOT/'assignment_witness.json').read_text())
P = tuple(range(6))
second = {int(a): b for a, b in source['second'].items()}
last = {tuple(map(int, h.split(','))): a for h, a in source['last'].items()}
actual = tuple(source['actual'])
target = tuple(source['target'])
table = {frozenset(map(int, s.split(','))): value
         for s, value in source['F'].items()}


def subsets(s):
    s = tuple(s)
    return (frozenset(t) for k in range(len(s)+1) for t in combinations(s, k))


def F(s):
    return table.get(frozenset(s), 0)


def fresh_pay(path, position):
    return F(path) - F(path[:position] + path[position+1:])


def fresh_action(h):
    if not h:
        return 0
    if len(h) == 1:
        return second[h[0]]
    return last[h]


def fresh_finish(h):
    while len(h) < 3:
        h = h + (fresh_action(h),)
    return h


fresh_comparisons = 0
for depth in range(3):
    for h in permutations(P, depth):
        path = fresh_finish(h)
        obey = fresh_pay(path, depth)
        for a in P:
            if a not in h:
                dev = fresh_finish(h+(a,))
                assert obey >= fresh_pay(dev, depth), (h, a, path, dev)
                fresh_comparisons += 1
assert fresh_finish(()) == actual
assert tuple(fresh_pay(actual, i) for i in range(3)) == (-1, 0, 0)

# M1 double Mobius formula is implemented directly from its definition.
allsets = tuple(subsets(P))
nonempty = tuple(s for s in allsets if s)
c = {s: sum((-1)**(len(s)-len(t))*F(t) for t in subsets(s)) for s in allsets}
z = {s: (-1)**(len(s)+1)*len(s)*c[s] for s in nonempty}
x = {b: sum((-1)**(len(a)-len(b))*z[a]
            for a in nonempty if b <= a) for b in nonempty}
M = sum(abs(v) for v in x.values())
K_M2 = 4*M+1
K = K_M2
r = {b: v+K for b, v in x.items()}
assert min(r.values()) > 0


def utilities(path, weights=None):
    if weights is None:
        weights = r
    out = [Fraction(0) for _ in path]
    for b, weight in weights.items():
        attracted = [i for i, a in enumerate(path) if a in b]
        if attracted:
            share = Fraction(weight, len(attracted))
            for i in attracted:
                out[i] += share
    return tuple(out)


def welfare(path):
    return sum(weight for b, weight in r.items() if any(a in b for a in path))


policy = {(): 0}
policy.update({(a,): b for a, b in second.items()})
policy.update(last)
for a in P:
    fresh = [b for b in P if b != a]
    # Repeated histories are not part of the auxiliary game. Complete them
    # directly by a final-player best response in the compiled legal game.
    policy[a, a] = max(fresh, key=lambda b: (utilities((a, a, b))[2], -b))


def finish(h):
    while len(h) < 3:
        h = h + (policy[h],)
    return h


# Exact simplification for this single fixed full policy.  Every IC slack is
# affine a+Kb.  Its bias slope b is nonnegative.  Thus positivity and all ICs
# can be checked without further search; M2 was only used to motivate the
# initial extension.  We replay all comparisons again at the resulting K.
K_threshold = Fraction(max(1-v for v in x.values()))
unit_bias = {b: 1 for b in nonempty}
for depth in range(3):
    for h in product(P, repeat=depth):
        path = finish(h)
        for a in P:
            dev = finish(h+(a,))
            intercept = utilities(path, x)[depth]-utilities(dev, x)[depth]
            slope = utilities(path, unit_bias)[depth]-utilities(dev, unit_bias)[depth]
            assert slope >= 0, (h, a, slope)
            if slope:
                K_threshold = max(K_threshold, -intercept/slope)
            else:
                assert intercept >= 0
K = ceil(K_threshold)
r = {b: v+K for b, v in x.items()}
assert min(r.values()) > 0

comparisons = 0
minimum_slack = None
for depth in range(3):
    for h in product(P, repeat=depth):
        path = finish(h)
        obey = utilities(path)[depth]
        for a in P:
            dev = finish(h+(a,))
            slack = obey-utilities(dev)[depth]
            assert slack >= 0, (h, a, path, dev, slack)
            minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
            comparisons += 1
assert finish(()) == actual
payoffs = utilities(actual)
W = welfare(actual)
assert sum(payoffs) == W
base = Fraction(56*K, 3)
assert payoffs == (base-1, base, base)
coverage = {t: welfare(t) for t in combinations_with_replacement(P, 3)}
OPT = max(coverage.values())
optima = [t for t, value in coverage.items() if value == OPT]
assert optima == [target]
matrix = [[utilities(actual[:i]+(a,)+actual[i+1:])[i] for a in target]
          for i in range(3)]
assignment = {','.join(map(str, p)): sum(matrix[i][target.index(a)]
                                       for i, a in enumerate(p))
              for p in permutations(target)}
minimum_assignment = min(assignment.values())
assert minimum_assignment > W
report = {
    'status': 'exact complete-history counterexample to static optimal-tuple assignment bridge only',
    'fresh_histories': 1+6+6*5, 'fresh_comparisons': fresh_comparisons,
    'full_histories': len(policy), 'full_comparisons': comparisons,
    'minimum_SPE_slack': str(minimum_slack),
    'M': M, 'K_M2_sufficient': K_M2, 'K_exact_threshold': str(K_threshold),
    'K': K, 'customer_count': sum(r.values()),
    'min_type_multiplicity': min(r.values()), 'max_type_multiplicity': max(r.values()),
    'actual': actual, 'payoffs': list(map(str, payoffs)), 'W': W,
    'unique_optimal_support': target, 'OPT': OPT,
    'static_signed_matrix': [[str(v-base) for v in row] for row in matrix],
    'assignment_costs': {key: str(value) for key, value in assignment.items()},
    'minimum_assignment': str(minimum_assignment),
    'assignment_minus_W': str(minimum_assignment-W),
    'half_margin': 2*W-OPT,
}
input_data = {'topics': list(map(str, P)), 'players': 3,
              'customers': [{'topics': sorted(b), 'multiplicity': weight}
                            for b, weight in sorted(r.items(), key=lambda pair: (len(pair[0]), sorted(pair[0])))]}
policy_data = {'policy': {','.join(map(str, h)): a for h, a in policy.items()},
               'actual': actual}
(ROOT/'assignment_instance.json').write_text(json.dumps(input_data, indent=2)+'\n')
(ROOT/'assignment_full_policy.json').write_text(json.dumps(policy_data, indent=2)+'\n')
(ROOT/'assignment_exact_audit.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
