"""Exact definition-level replay of the strict true-tail-menu family.
No repository model or solver imports. Integers are separate unit clients.
The arbitrary-m statement is proved in strict_tail_menu_gap.md.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement,product
from functools import lru_cache
from math import lcm
from pathlib import Path
import json


def family(k):
    C=k*(k+1);h=k+2;P=k+3;t=2*h+1;n=k+1
    # B=0, X leaves=1..h, Y leaves=h+1..2h.
    X=frozenset([0]+list(range(1,h+1)));Y=frozenset([0]+list(range(h+1,t)))
    clients=[X for _ in range(C)]+[Y for _ in range(C)]
    clients += [frozenset([a]) for a in range(1,t) for _ in range(P)]
    return C,h,P,t,n,clients


def audit(k,run_bi=False):
    C,h,P,t,n,clients=family(k);v=F(2*k+3);delta=F(k+1,4*(k+2))
    def f(a,B):
        return sum((F(1,1+sum(b in x for b in B)) for x in clients if a in x),F())
    def g(B):
        return sum((f(a,B) for a in range(1,t)),F())/(2*h)
    # Static backgrounds: exact compressed formula, with selected unit checks.
    def fast_g(B):
        counts=[B.count(a) for a in range(t)]
        u=sum(counts[1:h+1]);w=sum(counts[h+1:])
        return C*F(1,2)*(F(1,k-w+1)+F(1,k-u+1)) + F(P,2*h)*sum((F(1,counts[a]+1) for a in range(1,t)),F())
    assert g((0,)*k)==v
    assert all(f(a,(0,)*k)<=v for a in range(t))
    backgrounds=0;lowest=None;lowest_non_B=None;minimizers=[]
    for B in combinations_with_replacement(range(t),k):
        z=fast_g(B);backgrounds+=1
        assert z>=v
        if lowest is None or z<lowest:lowest=z;minimizers=[B]
        elif z==lowest:minimizers.append(B)
        if B!=(0,)*k:
            lowest_non_B=z if lowest_non_B is None else min(lowest_non_B,z)
            assert z>=v+delta
    assert minimizers==[(0,)*k]
    assert lowest_non_B==v+delta
    assert g((0,)*(k-1)+(1,))==v+delta
    # The pure blocker cap plus uniform primal is an exact matching saddle.
    # A true root branch cannot have all-B tail: each of all possible roots fails last BR.
    last_gaps=[]
    for a in range(t):
        z=(a,)+(0,)*k
        alt=1 if a==0 or a>h else h+1
        old=sum((F(1,sum(b in x for b in z)) for x in clients if 0 in x),F())
        changed=z[:-1]+(alt,)
        new=sum((F(1,sum(b in x for b in changed)) for x in clients if alt in x),F())
        assert new-old==3
        last_gaps.append(new-old)
    out={'k_competitors':k,'players':n,'topics':t,'unit_clients':len(clients),'v':str(v),'delta':str(delta),'static_backgrounds':backgrounds,'unique_worst_background':[0]*k,'min_nonworst_value':str(lowest_non_B),'allB_tail_last_improvement':str(min(last_gaps)),'floor':str(F(P)+F(C,n)),'OPT':3*n*n}
    assert F(P)+F(C,n)==v
    if run_bi:
        scale=lcm(*range(1,n+1));actions={};compares=0;mingap=None;minfloor=None
        @lru_cache(None)
        def utilities(z):
            loads=[sum(a in x for a in z) for x in clients]
            return tuple(sum(scale//d for x,d in zip(clients,loads) if a in x and d) for a in range(t))
        @lru_cache(None)
        def solve(hh):
            if len(hh)==n:return hh
            ends=[solve(hh+(a,)) for a in range(t)]
            vals=[utilities(z)[a] for a,z in enumerate(ends)]
            action=max(range(t),key=lambda a:(vals[a],a));actions[hh]=action
            return ends[action]
        actual=solve(())
        for depth in range(n):
            for hh in product(range(t),repeat=depth):
                a=actions[hh];own=F(utilities(solve(hh))[a],scale)
                minfloor=own if minfloor is None else min(minfloor,own)
                assert own>=v
                for b in range(t):
                    gap=own-F(utilities(solve(hh+(b,)))[b],scale)
                    assert gap>=0
                    mingap=gap if mingap is None else min(mingap,gap);compares+=1
        tailvalues=[g(solve((a,))[1:]) for a in range(t)]
        assert min(tailvalues)>=v+delta
        W=len([x for x in clients if any(a in x for a in actual)])
        opt=max(len([x for x in clients if any(a in x for a in z)]) for z in combinations_with_replacement(range(t),n))
        assert opt==3*n*n
        out['full_SPE_replay']={'histories':len(actions),'comparisons':compares,'minimum_deviation_gap':str(mingap),'minimum_player_payoff_over_all_histories':str(minfloor),'actual':actual,'actual_W':W,'min_root_tail_query':str(min(tailvalues)),'OPT_enumerated':opt}
    return out

if __name__=='__main__':
    report={'scope':'arbitrary-m proof is in the companion note; static exact replay k=1..5 and complete ordered SPE replay k=1..3 only','cases':[audit(k,k<=3) for k in range(1,6)]}
    dest=Path(__file__).with_name('strict_tail_menu_audit.json');dest.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
