"""Test the exact general candidate min_arbitrary_path sum M(h) >= OPT/2.
Finite runs only refute candidates; no positive conclusion is inferred.
"""
import json,random,sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def attack(ins):
    sol=ExactSPESolver(ins)
    @lru_cache(None)
    def go(q):
        if sum(q)==ins.players:return (Fraction(0),())
        nxt=[]
        for a in range(ins.topic_count):
            c=q[:a]+(q[a]+1,)+q[a+1:]
            v,z=go(c);nxt.append((v,(a,)+z))
        v,z=min(nxt)
        return (v+sol.threshold(q),z)
    v,z=go((0,)*ins.topic_count)
    return v,z,sol

def main():
    rng=random.Random(763809)
    best=Fraction(100);report={'candidate':'For every CAG and arbitrary full path z, sum_i M(h_i) >= OPT_m/2','seed':763809,'runs':0,'counterexample':None}
    for run in range(300):
        m=rng.choice([3,4,5,6]);p=rng.choice([3,4,5,6])
        types=tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),rng.randrange(1,9)) for mask in range(1,1<<p) if rng.random()<.18)
        ins=Instance(tuple(map(str,range(p))),types,m)
        v,z,sol=attack(ins);o=ins.optimal_welfare();report['runs']+=1
        ratio=Fraction(2*v,o) if o else Fraction(1)
        if ratio<best:
            best=ratio;print('best',run,m,p,str(ratio),str(v),o,z,flush=True)
        if 2*v<o:
            q=(0,)*p;rows=[]
            for a in z:
                rows.append({'prefix':list(q),'M':str(sol.threshold(q)),'action':a});q=q[:a]+(q[a]+1,)+q[a+1:]
            report['counterexample']={'instance':ins.to_dict(),'path':z,'sum_M':str(v),'OPT':o,'rows':rows}
            break
    report['min_2sumM_over_OPT']=str(best)
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2))
if __name__=='__main__':main()
