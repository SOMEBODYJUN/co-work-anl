"""Definition-level Fraction checks of the same-m catalog-padding lemma.
No canonical SPE solver, strategy cone, or floating point library is imported.
The finite run checks the implementation; the all-m proof is in safe_catalog_padding.md.
"""
import itertools,json,random
from fractions import Fraction
from pathlib import Path

def payoff(types,terminal,player):
    a=terminal[player]
    return sum((Fraction(v,sum(bool(mask>>b&1) for b in terminal)) for mask,v in types.items() if mask>>a&1),Fraction())

def backward_policy(k,m,types,allowed=None):
    allowed=tuple(range(k)) if allowed is None else tuple(allowed)
    actions={};terminals={}
    for depth in range(m,-1,-1):
        for h in itertools.product(range(k),repeat=depth):
            if depth==m:terminals[h]=h;continue
            vals={a:payoff(types,terminals[h+(a,)],depth) for a in allowed}
            a=max(allowed,key=lambda a:(vals[a],-a));actions[h]=a;terminals[h]=terminals[h+(a,)]
    return actions,terminals

def verify(k,m,types,actions):
    terminals={};comparisons=0;gap=None
    for depth in range(m,-1,-1):
        for h in itertools.product(range(k),repeat=depth):
            if depth==m:terminals[h]=h;continue
            a=actions[h];z=terminals[h+(a,)];terminals[h]=z
            for b in range(k):
                diff=payoff(types,z,depth)-payoff(types,terminals[h+(b,)],depth)
                assert diff>=0,(h,a,b,diff)
                gap=diff if gap is None else min(gap,diff);comparisons+=1
    return terminals,comparisons,gap

def main():
    rng=random.Random(231029);records=[]
    for m in range(1,5):
        for k in range(1,4):
            for sample in range(3):
                types={mask:rng.randrange(0,5) for mask in range(1,1<<k)}
                requested_k=k
                signatures=[tuple(mask for mask,v in types.items() if v and mask>>a&1) for a in range(k)]
                unique=list(dict.fromkeys(signatures));mapping=[unique.index(x) for x in signatures]
                quotient={}
                for mask,v in types.items():
                    if not v:continue
                    qmask=sum(1<<b for b in set(mapping[a] for a in range(k) if mask>>a&1))
                    quotient[qmask]=quotient.get(qmask,0)+v
                types=quotient;kk=len(unique)
                K=max(sum(v for mask,v in types.items() if mask>>a&1) for a in range(kk))
                old,_=backward_policy(kk,m,types)
                p=m if K else 0 # no duplicate empty themes when the cap is zero
                k=kk
                ext_types={mask:v*m for mask,v in types.items()}
                ext_types.update({1<<(k+j):K for j in range(p)})
                restricted,_=backward_policy(k+p,m,ext_types,range(k))
                actions={h:(old[h] if all(a<k for a in h) else restricted[h]) for h in restricted}
                terminals,comp,gap=verify(k+p,m,ext_types,actions)
                h=();actual=[]
                while len(h)<m:actual.append(actions[h]);h+=(actions[h],)
                assert all(a<k for a in actual)
                for i in range(m):assert payoff(ext_types,actual,i)==m*payoff(types,actual,i)
                def cov(T):return sum(v for mask,v in ext_types.items() if any(mask>>a&1 for a in T))
                exactopt=max(cov(J) for J in itertools.combinations_with_replacement(range(k+p),m))
                convolution=max(max(sum(v*m for mask,v in types.items() if any(mask>>a&1 for a in J)) for J in itertools.combinations_with_replacement(range(k),r))+(m-r)*K for r in range(1,m+1))
                assert exactopt==convolution
                records.append({'players':m,'old_topics':k,'requested_old_topics':requested_k,'sample':sample,'old_max_size':K,'comparisons':comp,'minimum_gap':str(gap),'OPT':exactopt,'convolution':convolution})
                k=requested_k
    report={'scope':'36 finite exact checks of the general construction; not proof by enumeration','cases':records,'comparisons':sum(x['comparisons'] for x in records)}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'cases':len(records),'comparisons':report['comparisons'],'status':'all exact checks passed'}))
if __name__=='__main__':main()
