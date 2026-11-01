"""Definition-level exact audit; no import of repository game code or LP solver."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

MASKS = {1:1,3:1,4:1,6:1,9:2,10:2,11:2,13:2,15:2,
         16:2,17:2,19:2,20:2,24:1,25:2,26:1,27:2,30:2}
P = 5
PREFIX = (0,3,4)

def utilities(path, masks=MASKS, p=P):
    answer = []
    for a in path:
        answer.append(sum((F(v, sum(bool(mask>>b&1) for b in path))
                           for mask,v in masks.items() if mask>>a&1), F(0)))
    return tuple(answer)

def welfare(path, masks=MASKS):
    return sum(v for mask,v in masks.items() if any(mask>>a&1 for a in path))

def two_menu(prefix, masks=MASKS, p=P):
    follower=[]; first=[]; BR=[]
    for a in range(p):
        follower.append(tuple(utilities(prefix+(a,b),masks,p)[-1] for b in range(p)))
        first.append(tuple(utilities(prefix+(a,b),masks,p)[-2] for b in range(p)))
        BR.append(tuple(b for b in range(p) if follower[a][b]==max(follower[a])))
    ell=tuple(min(first[a][b] for b in BR[a]) for a in range(p))
    M=max(ell)
    pairs=tuple((a,b) for a in range(p) for b in BR[a] if first[a][b]>=M)
    return follower,first,BR,ell,M,pairs

def fs(x):return str(x)
def ftable(t):return [[fs(x) for x in row] for row in t]

def main():
    follower,first,BR,ell,M,pairs=two_menu(PREFIX)
    assert BR==[(1,),(0,),(0,),(0,4),(1,)]
    assert ell==(F(157,30),F(157,30),F(14,3),F(77,15),F(103,20))
    assert M==F(157,30)
    assert pairs==((0,1),(1,0),(3,4))
    pure_profit={pair:sum(utilities(PREFIX+pair)[-2:]) for pair in pairs}
    assert pure_profit=={(0,1):F(157,15),(1,0):F(157,15),(3,4):F(53,5)}
    # First remaining actor chooses 3; last actor mixes 0 with 7/10 and 4 with 3/10.
    low=PREFIX+(3,0); high=PREFIX+(3,4)
    mixed_u=tuple(F(7,10)*u+F(3,10)*v for u,v in zip(utilities(low),utilities(high)))
    mixed_W=F(7,10)*welfare(low)+F(3,10)*welfare(high)
    assert utilities(low)[-1]==utilities(high)[-1]==F(77,15)
    assert mixed_u[-2]==M
    assert mixed_W==28
    assert mixed_u[:3]==(F(169,30),F(157,30),F(203,30))
    assert sum(mixed_u[-2:])==F(311,30)
    assert min(pure_profit.values())-sum(mixed_u[-2:])==F(1,10)
    # Full mixed continuation is credible: every other first branch uses its sole BR.
    for a in range(P):
        expected=(mixed_u[-2] if a==3 else first[a][BR[a][0]])
        assert expected<=M
    # Two independent payoff identities, including legal degenerate menus.
    for masks,p,prefix in [({},1,()), ({1:3},1,(0,)), ({3:4},2,(0,)),
                            ({1:2,2:1},2,()), (MASKS,P,PREFIX)]:
        follower0,first0,BR0,ell0,M0,pairs0=two_menu(prefix,masks,p)
        assert pairs0
        for a,b in product(range(p),repeat=2):
            path=prefix+(a,b);U=utilities(path,masks,p)
            assert sum(U)==welfare(path,masks)
            assert sum(U[-2:])==F(welfare(path,masks))-sum(U[:-2])
        for a in range(p):
            assert BR0[a] and ell0[a]<=M0
    # Exact profiles: root welfare and prefix incumbent rents.
    result={
        'status':'exact definition-level finite menu counterexample; not Q-CAG-HALF counterexample',
        'customers':sum(MASKS.values()),'prefix':PREFIX,
        'last_player_payoff_table':ftable(follower),
        'first_player_payoff_table':ftable(first),
        'BR':BR,'ell':list(map(fs,ell)),'M':fs(M),'pure_ordered_pairs':pairs,
        'pure_remaining_profits':{str(k):fs(v) for k,v in pure_profit.items()},
        'mixed_last_probabilities':{'0':'7/10','4':'3/10'},
        'mixed_incumbent_payoffs':list(map(fs,mixed_u[:3])),
        'mixed_first_payoff':fs(mixed_u[-2]),'mixed_last_payoff':fs(mixed_u[-1]),
        'mixed_remaining_profit':fs(sum(mixed_u[-2:])),
        'mixed_total_welfare':fs(mixed_W),'strict_profit_gap':'1/10',
        'degenerate_cases':5,
    }
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
