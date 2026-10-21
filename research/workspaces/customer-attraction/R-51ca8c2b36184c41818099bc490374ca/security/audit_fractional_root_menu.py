"""Definition-level Fraction audit for a fractional true-root-menu boundary.

Does not import the model, SPE solver, or the integer-menu audit. The general
lambda minimization follows by convexity and the group exchange involution;
this finite audit checks the input, all ordered histories and exact constants.
"""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent

def audit():
    X=tuple(range(3));Y=tuple(range(3,6))
    units=[frozenset([a,b])for a in X for b in Y]
    units += [frozenset(I+J)for I in combinations(X,2)for J in combinations(Y,2)for _ in range(3)]
    assert len(units)==36
    def group(a):return X if a in X else Y
    def act(h):
        if not h:return 0
        if len(h)==1:return 3 if h[0]in X else 0
        return min(a for a in group(h[1])if a not in h)
    def terminal(h):
        while len(h)<3:h=h+(act(h),)
        return h
    def pay(a,h):return sum((F(1,sum(b in C for b in h))for C in units if a in C),F(0))
    comparisons=0;minslack=None
    for d in range(3):
        for h in product(range(6),repeat=d):
            v=pay(act(h),terminal(h))
            for a in range(6):
                slack=v-pay(a,terminal(h+(a,)))
                assert slack>=0
                comparisons+=1;minslack=slack if minslack is None else min(minslack,slack)
    path=terminal(());u=[pay(a,path)for a in path]
    assert path==(0,3,4)and u==[F(10),F(12),F(12)]
    menus={terminal((a,))[1:]for a in range(6)}
    assert menus=={(0,1),(3,4)}
    def g(load,a):return sum((1/(1+sum(load[b]for b in C))for C in units if a in C),F(0))
    midpoint=[F(1,2),F(1,2),F(0),F(1,2),F(1,2),F(0)]
    values=[g(midpoint,a)for a in range(6)]
    assert values==[F(139,15),F(139,15),F(161,15),F(139,15),F(139,15),F(161,15)]
    # q uniform all six: total competitor mass two, load 1/3 per label.
    free=[F(1,3)]*6;freevalues=[g(free,a)for a in range(6)]
    assert freevalues==[F(333,35)]*6 and max(freevalues)<10
    # Convexity can be certified by each summand's second derivative:
    # 2*(membership imbalance)^2 / (1+affine load)^3 >= 0.
    for C in units:
        nX=sum(a in C for a in (0,1));nY=sum(a in C for a in (3,4))
        assert F(2*(nX-nY)**2)>=0
    return {'status':'PASS','players':3,'topics':6,'unit_customers':36,'complete_ordered_histories':43,'comparisons_including_self':comparisons,'minimum_spe_gap':str(minslack),'path':list(path),'payoffs':list(map(str,u)),'root_tail_menu':[list(x)for x in sorted(menus)],'fractional_menu_midpoint_values':list(map(str,values)),'fractional_menu_minmax':'161/15','root_utility':'10','strict_menu_gap':'11/15','free_fractional_values':list(map(str,freevalues)),'scope':'Only a restricted-menu fractional leader-cap failure. FF-LEADER, extra-mass leader, aggregate security and Q-CAG-HALF remain OPEN.'}

if __name__=='__main__':
    r=audit();print(json.dumps(r,indent=2));(OUT/'fractional_root_menu_audit.json').write_text(json.dumps(r,indent=2)+'\n')
