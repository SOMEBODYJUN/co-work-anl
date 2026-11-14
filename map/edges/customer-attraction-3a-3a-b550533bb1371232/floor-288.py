"""Audit the frozen best row using only exact rational arithmetic."""
import json
import sys
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit('usage: floor-288.py PATH_TO_static_floor_r3_bg0.json')
raw = Path(sys.argv[1]).read_bytes()
assert sha256(raw).hexdigest() == 'a6c41511e961cd70d38945c93499aadb68298950b721f72c325816ad5a5b8d39'
best = json.loads(raw)['best']
assert best['r'] == 3 and best['k'] == 6 and best['prefix'] == [0] * 6
labels = range(best['k'])
types = {
    tuple(label for label in labels if mask & 1 << label): count
    for mask, count in enumerate(best['weights'], 1)
    if count
}
assert len(types) == 22 and sum(types.values()) == 288

def alpha(distribution, group):
    return sum(distribution[label] for label in group)

def payoff(history, query):
    return sum(
        Fraction(count, 1 + sum(label in group for label in history))
        for group, count in types.items() if query in group
    )

def utilities(leaf):
    return tuple(payoff(leaf[:i] + leaf[i+1:], a) for i, a in enumerate(leaf))

p = tuple(Fraction(x, 500) for x in (74, 51, 61, 118, 47, 149))
q = tuple(Fraction(x, 500) for x in (72, 13, 50, 150, 34, 181))
assert sum(p) == sum(q) == 1 and min(p) >= 0 and min(q) >= 0
den = {group: 1 + 2 * alpha(q, group) for group in types}
pure = [sum(count / den[group] for group, count in types.items() if a in group) for a in labels]
value = sum(p[a] * pure[a] for a in labels)
slopes = [
    sum(count * alpha(p, group) / den[group]**2 for group, count in types.items() if a in group)
    for a in labels
]
weighted_slope = sum(q[a] * slopes[a] for a in labels)
tangents = [value + 2 * (weighted_slope - slope) for slope in slopes]
lb, ub = min(tangents), max(pure)
print('a tangent interval (10^6) pure interval (10^6)')
for a in labels:
    print(a, tangents[a] * 10**6 // 1, pure[a] * 10**6 // 1)
print('argmin tangent', tangents.index(lb), 'argmax pure', pure.index(ub))
assert Fraction(221, 3) < Fraction(737, 10) < lb <= ub < Fraction(1844, 25) < Fraction(457, 6)

max_roots, min_followers, passed_last = [], [], []
for bad in best['bads']:
    a = bad['action']
    assert bad['terminal'][a] == 1
    b, c = (label for label in labels if label != a and bad['terminal'][label])
    leaf = a, b, c
    u = utilities(leaf)
    max_roots.append(u[0])
    min_followers.extend(u[1:])
    print('fixed leaf', leaf, tuple(map(str, u)))
    for second, third in ((b, c), (c, b)):
        vector = tuple(payoff((a, second), query) for query in labels)
        opt = max(vector)
        br = tuple(i for i in labels if vector[i] == opt)
        if vector[third] == opt:
            passed_last.append((a, second, third))
        print((a, second, third), 'specified', str(vector[third]), 'BR', br, str(opt),
              'gain', str(opt - vector[third]), 'all', tuple(map(str, vector)))
assert max(max_roots) == Fraction(221, 3) and min(min_followers) == Fraction(457, 6)

assert passed_last == [(1, 5, 3)]

def last_choices(a,b):
    pay = tuple(payoff((a,b), i) for i in labels)
    return tuple(i for i in labels if pay[i] == max(pay))

assert last_choices(1, 5) == (3,) and last_choices(1, 3) == (4,)
assert payoff((1, 3), 5) == Fraction(527, 6)
assert payoff((1, 4), 3) == Fraction(289, 3)
assert payoff((1, 4), 3) - payoff((1, 3), 5) == Fraction(17, 2)
print('root 1 second actual 5', tuple(map(str, utilities((1,5,3)))))
for b in labels:
    print('root 1 alternative second',b,'possible (BR, second utility)',
          [(c,str(payoff((1,c),b))) for c in last_choices(1,b)])

# All subgame outcomes implementable by weak backward induction. At a fixed
# (a,b), arbitrary ties can be picked independently across b. Thus a chosen
# branch (b,c) can be supported exactly when it beats every other b's minimum.
child = {}
for a in labels:
    low_b = [min(payoff((a,c),b) for c in last_choices(a,b)) for b in labels]
    child[a] = [(b,c) for b,c in product(labels, repeat=2) if c in last_choices(a,b) and
                all(payoff((a,c),b) >= low_b[other] for other in labels if other != b)]
    print('root child SPE', a, [(b,c,str(payoff((b,c),a))) for b,c in child[a]])
min_child = {a:min(payoff((b,c),a) for b,c in child[a]) for a in labels}
full = [(a,b,c) for a in labels for b,c in child[a] if
        all(payoff((b,c),a) >= min_child[other] for other in labels if other != a)]
print('full SPE leaves', [(leaf,tuple(map(str,utilities(leaf)))) for leaf in full])

for a in labels:
    rows = [last_choices(a, b) for b in labels]
    assert all(len(row) == 1 for row in rows)
    continuation = tuple(row[0] for row in rows)
    second_scores = tuple(payoff((a, continuation[b]), b) for b in labels)
    opt = max(second_scores)
    second_best = tuple(b for b in labels if second_scores[b] == opt)
    assert len(second_best) == 1
    runner_up = max(second_scores[b] for b in labels if b not in second_best)
    terminal_margins = []
    for b in labels:
        scores = sorted((payoff((a,b),c) for c in labels), reverse=True)
        terminal_margins.append(scores[0] - scores[1])
    print(a, continuation, tuple(map(str,second_scores)), second_best, str(opt-runner_up),
          str(min(terminal_margins)), str(min_child[a]))
assert full == [(5, 3, 0)]
assert utilities(full[0]) == (Fraction(341, 3), Fraction(553, 6), Fraction(493, 6))
assert sum(utilities(full[0])) == 288
