"""Attack exact arbitrary-SPE-child ROW contract. Finite falsification only."""
from functools import lru_cache
from itertools import combinations
from math import lcm
from pathlib import Path
import json,random

def attack(weights,k,r,prefix):
    L=lcm(*range(1,sum(prefix)+r+1))
    rows=[([a for a in range(k) if mask>>a&1],w) for mask,w in weights.items()]
    @lru_cache(None)
    def values(q):
        us=[0]*k;W=0
        for labels,w in rows:
            c=sum(q[a] for a in labels)
            if c:
                W+=w
                for a in labels:us[a]+=w*(L//c)
        return tuple(us),W
    @lru_cache(None)
    def outcomes(q,left):
        if not left:return (q,)
        cs=[]
        for a in range(k):
            child=list(q);child[a]+=1
            cs.append(outcomes(tuple(child),left-1))
        cap=max(min(values(z)[0][a] for z in cs[a]) for a in range(k))
        return tuple(set(z for a in range(k) for z in cs[a] if values(z)[0][a]>=cap))
    children=[]
    for a in range(k):
        q=list(prefix);q[a]+=1
        children.append(outcomes(tuple(q),r-1))
    mins=[min(values(z)[0][a] for z in children[a]) for a in range(k)]
    costs=[0]*(1<<k);unions=[0]*(1<<k)
    for bits in range(1,1<<k):
        low=bits&-bits;a=low.bit_length()-1
        costs[bits]=costs[bits^low]+mins[a]
        unions[bits]=sum(w for mask,w in weights.items() if mask&bits)
    for a0 in range(k):
        for z0 in children[a0]:
            d0,W0=values(z0)[0][a0],values(z0)[1]
            for bits in range(1,1<<k):
                cost=costs[bits]+((d0-mins[a0]) if bits>>a0&1 else 0)
                gap=L*(unions[bits]-W0)-cost
                if gap>0:
                    selected=[(z0 if a==a0 else min(children[a],key=lambda z:values(z)[0][a])) for a in range(k)]
                    return {'weights':weights,'topics':k,'remaining':r,'prefix':prefix,'scale':L,'A0':a0,'subset':[a for a in range(k) if bits>>a&1],'gap_scaled':gap,'children':[{'A':a,'final_counts':z,'d_scaled':values(z)[0][a],'W':values(z)[1]} for a,z in enumerate(selected)]}

def main():
    rng=random.Random(981823)
    for r in range(3,7):
        for k in range(3,8):
            for it in range(500):
                weights={mask:rng.randrange(1,31) for mask in range(1,1<<k) if rng.random()<(0.4 if mask.bit_count()<=2 else 0.03)}
                if not weights:continue
                prefix=[0]*k
                for _ in range(rng.randrange(0,3)):prefix[rng.randrange(k)]+=1
                out=attack(weights,k,r,tuple(prefix))
                if out:
                    out['iteration']=it
                    Path(__file__).with_name('child_menu_general_counterexample.json').write_text(json.dumps(out,indent=2))
                    print(json.dumps(out),flush=True);return
            print('completed',r,k,flush=True)
    print('NO COUNTEREXAMPLE; finite only',flush=True)
if __name__=='__main__':main()
