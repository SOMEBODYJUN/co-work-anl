"""Finite falsification only of arbitrary-child ROW contract; no inference from misses."""
from itertools import product
from math import lcm
import random,json
from pathlib import Path

def test(weights,k,btopics=()):
    masks=list(weights)
    r=3
    L=lcm(*range(1,len(btopics)+r+1))
    def leaf(path):
        prof=btopics+path
        us=[0]*len(prof); W=0
        for mask,w in weights.items():
            chosen=[i for i,a in enumerate(prof) if mask>>a&1]
            if chosen:
                W+=w
                for i in chosen:us[i]+=w*(L//len(chosen))
        return tuple(us[-3:]),W
    choices=[]
    for a in range(k):
        br={}
        for b in range(k):
            vals=[(c,*leaf((a,b,c))) for c in range(k)]
            best=max(x[1][2] for x in vals)
            br[b]=[x for x in vals if x[1][2]==best]
        cap=max(min(x[1][1] for x in br[b]) for b in range(k))
        choices.append([(b,c,u,W) for b in range(k) for c,u,W in br[b] if u[1]>=cap])
    mind=[min(x[2][0] for x in cs) for cs in choices]
    union=[0]*(1<<k)
    cost=[0]*(1<<k)
    for bits in range(1,1<<k):
        low=bits&-bits;a=low.bit_length()-1
        cost[bits]=cost[bits^low]+mind[a]
        union[bits]=sum(w for mask,w in weights.items() if mask&bits)
    for a0 in range(k):
        for b,c,u,W in choices[a0]:
            for bits in range(1,1<<k):
                d=cost[bits]+((u[0]-mind[a0]) if bits>>a0&1 else 0)
                gap=L*(union[bits]-W)-d
                if gap>0:
                    chosen=[]
                    for a in range(k):
                        z=(b,c,u,W) if a==a0 else min(choices[a],key=lambda x:x[2][0])
                        chosen.append({'A':a,'tail':[z[0],z[1]],'u':z[2],'W':z[3]})
                    return {'weights':weights,'topics':k,'prefix':btopics,'scale':L,'A0':a0,'subset':[a for a in range(k) if bits>>a&1],'gap_scaled':gap,'children':chosen}

def main():
    rng=random.Random(819417)
    for k in range(3,9):
        for it in range(3000):
            weights={mask:rng.randrange(0,10) for mask in range(1,1<<k)}
            weights={m:w for m,w in weights.items() if w}
            prefix=tuple(rng.randrange(k) for _ in range(rng.randrange(0,4)))
            out=test(weights,k,prefix)
            if out:
                out['iteration']=it
                p=Path(__file__).with_name('child_menu_contract_counterexample.json')
                p.write_text(json.dumps(out,indent=2))
                print(json.dumps(out));return
        print('completed',k,flush=True)
    print('NO COUNTEREXAMPLE; finite only')
if __name__=='__main__':main()
