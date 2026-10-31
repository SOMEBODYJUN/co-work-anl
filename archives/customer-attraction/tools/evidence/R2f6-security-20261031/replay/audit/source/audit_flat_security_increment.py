"""Exact all-history certificate for a flat-safety local debt counterexample.

The family B>=3 uses the same six-action skeleton, with singleton branches
grafted by ordinary finite backward induction. The saved B=3 child policy has
all 1464 ordered histories and is checked against all eleven actions. This is
a counterexample to a local proof candidate, not to global safety or half.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement as cwr
from pathlib import Path
import json

HERE=Path(__file__).parent
SETS=tuple(frozenset((a,j)) for a in range(2) for j in range(2,5))+tuple(frozenset((x,)) for x in range(5))
PAIRS=((1,1),(1,2),(1,3),(2,2),(1,4),(2,3),(2,4),(3,3),(3,4),(4,4))
RANK={p:len(PAIRS)-j for j,p in enumerate(PAIRS)}
N=4

def add(c,a):return c[:a]+(c[a]+1,)+c[a+1:]
def loads(c):return tuple(sum(c[a] for a,s in enumerate(SETS[:len(c)]) if x in s) for x in range(5))
def code(a,z):
    l=loads(z)
    return tuple(sorted(l[x] for x in SETS[a]))
def utility(B,a,z):
    l=loads(z)
    return sum((F(1,B+l[x]) for x in SETS[a]),F())

def solver(k,score):
    @lru_cache(None)
    def outcomes(c):
        if sum(c)==N:return (c,)
        children=[outcomes(add(c,a)) for a in range(k)]
        threshold=max(min(score(a,z) for z in zs) for a,zs in enumerate(children))
        return tuple(sorted(set(z for a,zs in enumerate(children) for z in zs if score(a,z)>=threshold)))
    def realize(h,c,target,policy,force=None):
        if sum(c)==N:
            assert c==target
            return
        children=[outcomes(add(c,a)) for a in range(k)]
        threshold=max(min(score(a,z) for z in zs) for a,zs in enumerate(children))
        legal=[a for a,zs in enumerate(children) if target in zs and score(a,target)>=threshold]
        assert legal
        a=min(legal) if force is None else force
        assert a in legal
        policy[h]=a
        for b,zs in enumerate(children):
            z=target if b==a else min(zs,key=lambda zz:(score(b,zz),zz))
            realize(h+(b,),add(c,b),z,policy)
    return outcomes,realize

def main():
    out6,realize6=solver(6,lambda a,z:RANK[code(a,z)])
    zero6=(0,)*6
    target=(1,1,1,1,0,0)
    assert target in out6(add(zero6,0)) and target in out6(zero6)
    skeleton={}
    realize6((),zero6,target,skeleton,force=0)
    # Exact full B=3 child; enforce the six-action skeleton until the first
    # singleton, and realize arbitrary full BI outcomes afterwards.
    B=3;k=11
    out11,realize11=solver(k,lambda a,z:utility(B,a,z))
    policy={}
    def graft(h,c):
        if len(h)==N:return
        assert all(a<6 for a in h)
        policy[h]=skeleton[h]
        for a in range(k):
            cc=add(c,a)
            if a<6:graft(h+(a,),cc)
            elif len(h)+1<N:
                z=min(out11(cc))
                realize11(h+(a,),cc,z,policy)
    graft((),(0,)*k)
    histories=[h for d in range(N) for h in product(range(k),repeat=d)]
    assert set(policy)==set(histories)
    @lru_cache(None)
    def leaf(h):return h if len(h)==N else leaf(h+(policy[h],))
    def count(z):return tuple(z.count(a) for a in range(k))
    comparison_count=0;min_slack=None
    for h in histories:
        a=policy[h];z=count(leaf(h));u=utility(B,a,z)
        for b in range(k):
            v=utility(B,b,count(leaf(h+(b,))))
            assert u>=v,(h,b,u,v)
            slack=u-v
            min_slack=slack if min_slack is None else min(min_slack,slack)
            comparison_count+=1
    actual=leaf(());actual_count=count(actual)
    assert actual_count[:6]==target and not any(actual_count[6:])
    V=F(3,2*(B+2))+F(1,2*(B+3))
    primary=[F(1,6)]*6+[F()]*5
    backgrounds=list(cwr(range(k),3))
    def query(a,BG):return sum((F(1,B+1+sum(x in SETS[b] for b in BG)) for x in SETS[a]),F())
    primary_values=[sum((p*query(a,BG) for a,p in enumerate(primary)),F()) for BG in backgrounds]
    assert min(primary_values)==V
    # All these root backgrounds contain the actual first action 0. Deleting
    # 0 therefore simultaneously gives a legal two-slot dual after that action.
    dual=(((0,4,5),F(1,2)),((0,1,5),F(1,4)),((0,4,2),F(1,4)))
    dual_values=[sum((p*query(a,BG) for BG,p in dual),F()) for a in range(k)]
    assert dual_values[:6]==[V]*6 and max(dual_values)==V
    u=utility(B,0,actual_count)
    assert u==F(11,30) and V==F(23,60) and V-u==F(1,60)
    # Rank inequalities: all except 22>14 are componentwise or equal-sum strict
    # reciprocal convexity. The exceptional exact numerator is B-2>0.
    rank_checks=[]
    for bb in (3,4,10):
        vals=[sum((F(1,bb+d) for d in pair),F()) for pair in PAIRS]
        assert all(a>b for a,b in zip(vals,vals[1:]))
        rank_checks.append(dict(B=bb,values=list(map(str,vals))))
    rec=dict(status='exact local counterexample; global safety and half remain open',
        remaining_players=N,background_per_customer=B,original_total_players=5*B+N,
        main_sets=[sorted(s) for s in SETS[:6]],singletons=[sorted(s) for s in SETS[6:]],
        main_after_zero_outcomes=[list(z) for z in out6(add(zero6,0))],
        main_after_zero_payoff_codes=[list(code(0,z)) for z in out6(add(zero6,0))],
        actual=list(actual),root_utility=str(u),root_safety=str(V),child_safety=str(V),
        safety_increment='0',chain_debt=str(u-V),
        static_backgrounds=len(backgrounds),primary=list(map(str,primary)),
        dual=[dict(background=list(BG),probability=str(p)) for BG,p in dual],
        dual_query_values=list(map(str,dual_values)),
        ordered_histories=len(histories),comparisons=comparison_count,min_slack=str(min_slack),
        main_skeleton_histories=len(skeleton),rank_order=[list(p) for p in PAIRS],rank_checks=rank_checks,
        policy=[dict(history=list(h),action=policy[h]) for h in histories])
    (HERE/'flat_security_increment_certificate.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps({k:v for k,v in rec.items() if k not in ('policy','rank_checks','primary','dual')}))

if __name__=='__main__':main()
