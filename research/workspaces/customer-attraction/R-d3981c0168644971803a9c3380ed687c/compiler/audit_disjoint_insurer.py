"""Unit-customer exact set-valued BI audit, with arbitrary internal subthemes.

No repository imports. Outcome caching keeps all outcomes and makes no shared
tie selection across ordered histories. This is a finite check of the proof.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations,product
from pathlib import Path
import json,random

HERE=Path(__file__).resolve().parent

def check(sets,m):
    sets=tuple(dict.fromkeys(map(frozenset,sets)));p=len(sets)
    units=frozenset().union(*sets);core=frozenset.intersection(*sets)
    petals=tuple(T-core for T in sets)
    maximal=tuple(a for a,T in enumerate(petals) if not any(T<U for U in petals))
    assert all(not(petals[a]&petals[b]) for a,b in combinations(maximal,2))
    @lru_cache(None)
    def U(z,a):
        return sum((F(1,sum(z[j] for j,S in enumerate(sets) if x in S)) for x in sets[a]),F(0))
    def W(z):return len(frozenset().union(*(sets[a] for a in range(p) if z[a])))
    def inc(k,a):return tuple(n+int(j==a) for j,n in enumerate(k))
    @lru_cache(None)
    def solve(k):
        if sum(k)==m:return frozenset((k,))
        children=[solve(inc(k,a)) for a in range(p)]
        floor=max(min(U(z,a) for z in child) for a,child in enumerate(children))
        result=frozenset(z for a,child in enumerate(children) for z in child if U(z,a)>=floor)
        assert result
        # Every surviving action is maximal at every legal history.
        assert all(a in maximal for a,child in enumerate(children)
                   if any(U(z,a)>=floor for z in child)),(sets,m,k)
        return result
    opt=max(len(frozenset().union(*(sets[a] for a in J)))
            for r in range(1,min(m,p)+1) for J in combinations(range(p),r))
    roots=0;pairs=0;maxscaled=F(0);minslack=None
    for a in range(p):
        prefix=inc((0,)*p,a);outcomes=solve(prefix);roots+=1
        vals=[U(z,a) for z in outcomes];spread=max(vals)-min(vals)
        assert (m+1)*spread<=len(units)
        maxscaled=max(maxscaled,F((m+1)*spread,len(units)))
        for z in outcomes:
            q=tuple(n-int(j==a) for j,n in enumerate(z))
            assert all(not n or j in maximal for j,n in enumerate(q))
            # Each genuine suffix outcome is a static PNE under the actual root.
            for j,n in enumerate(q):
                if not n:continue
                for b in maximal:
                    zz=tuple(v-int(t==j)+int(t==b) for t,v in enumerate(z))
                    assert U(z,j)>=U(zz,b),(sets,m,a,z,j,b)
            # The same proof also guarantees nonnegative root-relaxed dilution.
            assert 2*W(z)-opt>=len(core)
            for zz in outcomes:
                gap=U(z,a)-U(zz,a)
                if gap<=0:continue
                slack=2*W(z)-opt-len(core)-3*gap
                assert slack>=0,(sets,m,a,z,zz,gap,slack)
                minslack=slack if minslack is None else min(minslack,slack)
                pairs+=1
    return dict(m=m,p=p,units=len(units),core=len(core),root_cases=roots,
                positive_spread_pairs=pairs,count_states=solve.cache_info().currsize,
                max_scaled_customer_spread=str(maxscaled),minimum_three_slack=None if minslack is None else str(minslack))

def main():
    rng=random.Random(231043);cases=[]
    # Genuine internal root topics, including an empty root, shared core, and
    # overlapping internal subthemes contained inside disjoint maximal blocks.
    for m in range(2,7):
        for x,y in product(range(1,5),repeat=2):
            B=frozenset(range(x));D=frozenset(range(x,x+y))
            for a in range(x+1):
                K=frozenset(range(100,100+(m%2)))
                sets=[B,D,frozenset(range(a))]
                if x>=3:sets.append(frozenset((0,x-1)))
                if y>=2:sets.append(frozenset((x,)))
                cases.append(check([T|K for T in sets],m))
    # Add structured three-plus-flower cases; this is one proof audit batch,
    # not a general discovery scan.
    for m in range(2,7):
        for _ in range(12):
            blocks=[];offset=0
            for _ in range(rng.randrange(3,5)):
                w=rng.randrange(1,5);blocks.append(frozenset(range(offset,offset+w)));offset+=w
            sets=list(blocks)
            for B in blocks:
                T=frozenset(x for x in B if rng.randrange(2))
                if T not in sets:sets.append(T)
            cases.append(check(sets,m))
    report=dict(scope='Finite exact audit; every fixed-root suffix outcome, all suffix PNE deviations, and every positive same-root payoff pair. Universal quantifiers rest on the analytic proof.',
                seed=231043,cases=len(cases),root_cases=sum(c['root_cases'] for c in cases),
                positive_spread_pairs=sum(c['positive_spread_pairs'] for c in cases),
                count_states=sum(c['count_states'] for c in cases),
                all_passed=True,records=cases)
    (HERE/'disjoint_insurer_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
if __name__=='__main__':main()
