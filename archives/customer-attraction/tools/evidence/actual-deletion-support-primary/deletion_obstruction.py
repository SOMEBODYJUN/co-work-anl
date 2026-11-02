"""Definition-level audit of a static-dual-support obstruction.

No canonical solver, LP, or compressed input is imported.  Customers are
expanded individually.  The full 43-node ordered strategy is checked.
"""
from fractions import Fraction
from itertools import combinations, product
import json


X, Y = tuple(range(3)), tuple(range(3,6))
customers = [frozenset((x,y)) for x in X for y in Y]
for I in combinations(X,2):
    for J in combinations(Y,2):
        customers += [frozenset(I+J)]*3
assert len(customers)==36


def action(h):
    if not h: return 0
    if len(h)==1: return 3 if h[0] in X else 0
    group=X if h[1] in X else Y
    return next(a for a in group if a not in h)


def finish(h):
    while len(h)<3: h=h+(action(h),)
    return h


def payoff(a,z):
    return sum((Fraction(1,sum(b in T for b in z)) for T in customers if a in T),Fraction())


comparisons=0
for d in range(3):
    for h in product(range(6),repeat=d):
        z=finish(h)
        own=payoff(z[d],z)
        for a in range(6):
            assert own>=payoff(a,finish(h+(a,)))
            comparisons+=1
assert comparisons==258
z=finish(())
u=[payoff(a,z) for a in z]
W=sum(u)
assert z==(0,3,4) and u==[10,12,12] and W==34
backgrounds=[z[:i]+z[i+1:] for i in range(3)]
matrix=[[payoff(a,(a,)+B) for B in backgrounds] for a in range(6)]
assert matrix[5]==[12,12,12]
assert Fraction(12)>W/3
# Thus ANY mixture supported on actual terminal deletions has cap at least12.
# The mixed static security value is only10 (known matching certificate), so
# this failure excludes a restricted dual construction, not W>=3v.

frac_values=[]
for a in range(6):
    frac_values.append(sum((Fraction(3,3+2*sum(b in T for b in z)) for T in customers if a in T),Fraction()))
assert frac_values==[Fraction(43,5),Fraction(373,35),Fraction(373,35),Fraction(65,7),Fraction(65,7),Fraction(397,35)]
assert max(frac_values)-W/3==Fraction(1,105)
print(json.dumps({'status':'exact audit passed','ordered_histories':43,'action_comparisons':comparisons,'path':z,'payoffs':list(map(str,u)),'W':str(W),'deletion_backgrounds':backgrounds,'query_matrix':[[str(t) for t in row] for row in matrix],'fractional_actual_load_values':list(map(str,frac_values))},indent=2))
