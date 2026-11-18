"""Four-label, two-mover subgame. Enumerate strict response maps H ⊊ P.
Only to discover witnesses. Printed integers are subsequently checked exactly.
"""
from itertools import product
from fractions import Fraction
from math import lcm
import numpy as np
from scipy.optimize import linprog

labels = 'HPQR'
types = [mask for mask in range(1, 15) if not (mask & 1) or (mask & 2)]
acts = range(4)
def vec(leader, follower):
    return np.array([float(Fraction(1, 1 + ((m >> follower) & 1))) if (m >> leader) & 1 else 0 for m in types])
options = []
for reply in product(range(1,4), repeat=4):
    rows = [vec(reply[a],a)-vec(z,a) for a in acts for z in acts if z!=reply[a]]
    rows += [vec(0,reply[0])-vec(a,reply[a]) for a in (1,2,3)]
    # Inclusion maximality, strict containment, and active pair intersections.
    rows += [np.array([int(m>>a&1 and not(m>>b&1)) for m in types]) for a in (1,2,3) for b in (1,2,3) if a!=b]
    rows += [np.array([int(m>>1&1 and not(m&1)) for m in types])]
    rows += [np.array([int(m>>a&1 and m>>b&1) for m in types]) for a,b in [(1,2),(1,3)]]
    sol = linprog(np.ones(len(types)),A_ub=-np.array(rows), b_ub=-np.ones(len(rows)),bounds=(0,None),method='highs')
    if not sol.success:
        continue
    wr = [Fraction(str(round(x,8))).limit_denominator(100000) for x in sol.x]
    d = lcm(*(x.denominator for x in wr))
    wi = [int(x*d) for x in wr]
    assert min(np.array(rows)@wi) >= 1
    options.append((sum(wi),reply,wi))

if options:
    total,reply,wi = min(options)
    print('eligible strict maps',len(options),'minimum rational-LP witness converted to integers',total)
    print('reply',''.join(labels[a] for a in reply))
    print('types',{' '.join(labels[a] for a in acts if m>>a&1):w for m,w in zip(types,wi) if w})
    print('twice payoff of row when column chosen (HPQR):')
    for a in acts:
        print(labels[a],*[int(2*(vec(a,z)@wi)) for z in acts])
else:
    print('no strict map')
