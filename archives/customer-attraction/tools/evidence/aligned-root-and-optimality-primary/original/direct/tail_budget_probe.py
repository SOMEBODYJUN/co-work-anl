"""Test parent root-menu tail payment against full-history 5-player SPEs.
This is only an attack on that precise sufficient inequality.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
import json, random
from pathlib import Path

M=5; L=60

def probe(weights,p):
    finals=[]
    for tup in combinations_with_replacement(range(p),M):
        c=tuple(tup.count(j) for j in range(p)); finals.append(c)
    pay=[];welfare=[]
    for c in finals:
        pp=[0]*p;ww=0
        for mask,weight in weights.items():
            q=sum(c[j] for j in range(p) if mask>>j&1)
            if q:
                ww+=weight
                for j in range(p):
                    if mask>>j&1:pp[j]+=weight*(L//q)
        pay.append(pp);welfare.append(ww)
    lookup={c:i for i,c in enumerate(finals)}
    def inc(c,a):return c[:a]+(c[a]+1,)+c[a+1:]
    @lru_cache(None)
    def R(c):
        if sum(c)==M:return frozenset([lookup[c]])
        ch=[R(inc(c,a)) for a in range(p)]
        floor=max(min(pay[f][a] for f in fs) for a,fs in enumerate(ch))
        return frozenset(f for a,fs in enumerate(ch) for f in fs if pay[f][a]>=floor)
    root=(0,)*p;ch=[R(inc(root,a)) for a in range(p)]
    floor=max(min(pay[f][a] for f in fs) for a,fs in enumerate(ch))
    opt=max(welfare)
    # The five topics are an optimal tuple when p=5 and cover the union.
    if p!=5:return None
    for a,fs in enumerate(ch):
        for f in fs:
            u=pay[f][a]
            if u<floor:continue
            branches=[]
            for t,rs in enumerate(ch):
                if t==a:g=f
                else:g=max((k for k in rs if pay[k][t]<=u),key=lambda k:L*welfare[k]-pay[k][t])
                branches.append(g)
            vs=[L*welfare[g]-pay[g][t] for t,g in enumerate(branches)]
            gap=5997*sum(vs)+4985*u-25994*L*welfare[f]
            if gap>0:
                return {'weights':weights,'actual_root':a,'actual_counts':finals[f], 'u1_over_60':u,'W':welfare[f],'O':opt,'branch_counts':[finals[g] for g in branches], 'tail_over_60':vs,'gap_over_60':gap}
    return None

if __name__=='__main__':
    random.seed(938254)
    for trial in range(2000):
        weights={mask:random.randrange(1,9) for mask in range(1,32) if random.random()<.28}
        ans=probe(weights,5)
        if ans:
            ans['trial']=trial
            out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(ans,indent=2));print(json.dumps(ans));break
    else:print('No counterexample in 2000 five-topic inputs; this is not a proof.')
