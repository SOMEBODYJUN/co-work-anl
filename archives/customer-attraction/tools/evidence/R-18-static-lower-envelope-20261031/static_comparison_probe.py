from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from random import Random
from math import lcm
from functools import lru_cache
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver

def comps(n,p):
    if p==1:
        yield (n,)
    else:
        for k in range(n+1):
            for v in comps(n-k,p-1):yield (k,)+v

def analyze(m,p,r):
    scale=lcm(*range(1,m+1))
    types=[(tuple(a for a in range(p) if mask>>a&1),v) for mask,v in enumerate(r,1) if v]
    @lru_cache(None)
    def u(q):
        out=[0]*p
        for bs,v in types:
            c=sum(q[b] for b in bs)
            if c:
                for b in bs:
                    if q[b]:out[b]+=v*(scale//c)
        return tuple(out)
    def welfare(q):return sum(v for bs,v in types if any(q[b] for b in bs))
    @lru_cache(None)
    def spe(q):
        if sum(q)==m:return frozenset([q])
        children=[spe(q[:a]+(q[a]+1,)+q[a+1:]) for a in range(p)]
        floor=max(min(u(t)[a] for t in child) for a,child in enumerate(children))
        return frozenset(t for a,child in enumerate(children) for t in child if u(t)[a]>=floor)
    terminals=list(comps(m,p))
    pne=[]
    for q in terminals:
        good=True
        for a in range(p):
            if not q[a]:continue
            for b in range(p):
                if a==b:continue
                qq=list(q);qq[a]-=1;qq[b]+=1
                if u(tuple(qq))[b]>u(q)[a]:good=False;break
            if not good:break
        if good:pne.append(q)
    sout=spe((0,)*p)
    sq=min(sout,key=welfare);nq=min(pne,key=welfare)
    return {'spe_w':welfare(sq),'pne_w':welfare(nq),'spe_q':sq,'pne_q':nq,'opt':max(map(welfare,terminals)),'types':r,'m':m,'p':p}

def verify(item):
    ins=Instance(tuple(map(str,range(item['p']))),tuple(CustomerType(frozenset(a for a in range(item['p']) if mask>>a&1),v) for mask,v in enumerate(item['types'],1) if v),item['m'])
    oracle=ExactSPESolver(ins)
    assert tuple(item['spe_q']) in oracle.outcomes()
    assert oracle.minimum_welfare()==item['spe_w']
    return oracle.certificate(item['spe_q']).to_dict()

if __name__=='__main__':
    rng=Random(1567683)
    count=0
    for m,p,rounds in [(2,3,3**7),(3,4,20000),(4,4,20000),(5,5,5000)]:
        rows=product(range(3),repeat=7) if (m,p)==(2,3) else ([rng.choice([0,0,0,1,2,3,5,8]) for _ in range(2**p-1)] for __ in range(rounds))
        for r in rows:
            count+=1
            item=analyze(m,p,r)
            if item['spe_w']<item['pne_w']:
                item['checked']=count
                item['certificate']=verify(item)
                dest=Path(__file__).with_name('static_lower_envelope_counterexample.json')
                dest.write_text(json.dumps(item,indent=2))
                print(json.dumps({k:v for k,v in item.items() if k!='certificate'}));sys.exit(0)
        print('completed',m,p,rounds,flush=True)
    print('No counterexample',count)
