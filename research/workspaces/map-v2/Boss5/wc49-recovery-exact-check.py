"""Local exact checks for wc49 recovery; no imports from archived audit programs."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

OUT = Path(__file__).with_name('wc49-recovery-exact-check.json')
w = [F(16), F(2), F(5)]
specs = [((0, 1, 1), F(13), 2), ((1, 1, 2), F(59), 1),
         ((1, 2, 1), F(2), 2)]

def costs(s):
    answer = [F(0)] * 3
    for mask, coefficient, degree in specs:
        for side in (1, 2):
            users = [i for i in range(3) if mask[i] and
                     (mask[i] if s[i] == 0 else 3-mask[i]) == side]
            value = coefficient * sum((w[i] for i in users), F(0)) ** degree
            for i in users:
                answer[i] += value
    return answer

def flip(s, i):
    t = list(s)
    t[i] = 1-t[i]
    return tuple(t)

states = list(product((0, 1), repeat=3))
table = {s: costs(s) for s in states}
q = {s: max([F(1)] + [table[s][i]/table[flip(s, i)][i]
                      for i in range(3)]) for s in states}
assert min(q.values()) == F(286, 267)
assert [s for s in states if q[s] == min(q.values())] == [(0, 1, 0), (1, 0, 1)]
alpha = F(21, 20)
cycle = [(0, 1, 0)]
cycle_margins = []
for i in [0, 1, 2, 0, 1, 2]:
    s = cycle[-1]
    t = flip(s, i)
    cycle_margins.append(table[s][i] - alpha*table[t][i])
    cycle.append(t)
assert cycle[-1] == cycle[0]
assert cycle_margins[:3] == [F(791, 20), F(677, 20), F(201, 5)]
assert cycle_margins[3:] == cycle_margins[:3]
B = max(v for row in table.values() for v in row)
eta = min(cycle_margins)
delta = F(21, 23)
budget = eta/(4*alpha**2*B)
assert B == 2002 and budget == F(3385, 882882)
assert delta**62 <= budget < delta**61
M = 2*alpha*B
clock = lambda x: M*(F(x, 23)**62)
g = [clock(21)-alpha*clock(18), clock(18)-alpha*clock(7),
     clock(7)-alpha*clock(21)]
gain = clock(23)-clock(18)+alpha*(clock(7)-clock(2))
assert all(a+b > 0 for a, b in zip(cycle_margins[:3], g))
assert g[1]+gain > alpha*B

n, light = 3, F(1, 5)
P, Q = lambda x: x, lambda x: x*x/2
h = lambda m: P(1+m*light)+(n-m)*Q(1+light)+m*Q(F(1))
A = lambda m: P(1+m*light)+Q(light)
D = lambda m: P((n-m+1)*light)+Q(1+light)
orbit = []
for m in range(n+1):
    ratios = [F(1), h(m)/h(n-m)]
    if m:
        ratios.append(A(m)/D(m))
    if m < n:
        ratios.append(D(m+1)/A(m+1))
    orbit.append(max(ratios))
assert orbit == [F(66, 61), F(157, 156), F(71, 56), F(81, 46)]
assert min(h(0)/h(n), A(1)/D(1)) == F(61, 66)

potential = [[F(0), F(296, 33), F(1354, 33)],
             [F(1), F(629, 33), F(2279, 33)],
             [F(5), F(37), F(109)]]
ratios = []
for k, l in product(range(3), repeat=2):
    if k < 2:
        ratios.append((potential[k+1][l]-potential[k][l])/F((k+1+2*l)**2))
    if l < 2:
        ratios.append((potential[k][l+1]-potential[k][l])/F(2*(k+2*(l+1))**2))
assert len(ratios) == 12 and min(ratios) >= 1 and max(ratios) == F(37, 33)

report = {
    'method': 'Exact Fraction reconstruction, no archived audit imports or executions',
    'triad': {'states': 8, 'deviations': 24, 'best_factor': str(min(q.values())),
              'endpoint_states': ['010', '101'], 'B': str(B), 'eta': str(eta),
              'cycle_margins': [str(x) for x in cycle_margins],
              'uniform_budget': str(budget), 'budget_min_degree': 62,
              'directed_clock_legal_constraints': True,
              'directed_clock_illegal_constraint': True},
    'orbit': {'q_values': [str(x) for x in orbit], 'best_factor': str(min(orbit)),
              'coarse_two_attack': str(min(h(0)/h(n), A(1)/D(1)))},
    '37_33_template': {'insertion_edges': len(ratios),
                       'minimum_ratio': str(min(ratios)),
                       'maximum_ratio': str(max(ratios)),
                       'scope': 'Only the stated at-most-two-per-type, h=w template'},
    'status': 'all exact assertions passed'
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(report, ensure_ascii=False))
