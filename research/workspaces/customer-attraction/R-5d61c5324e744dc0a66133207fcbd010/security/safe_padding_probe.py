"""Probe the same-player safe-disjoint-padding closure of a full SPE cone."""
import argparse,importlib.util,itertools,json,random,sys
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
p=Path(__file__).with_name('direct_floor_probe.py');s=importlib.util.spec_from_file_location('directfloor',p);d=importlib.util.module_from_spec(s);s.loader.exec_module(d)
OUT=Path(__file__).parent

def run(k,m,cases,seed):
    rng=random.Random(seed);records=[]
    size=[np.array([int(mask>>a&1) for mask in range(1,1<<k)],float) for a in range(k)]
    for case in range(cases):
        w=[rng.randrange(1,7) if rng.random()<.25 else 0 for _ in range((1<<k)-1)]
        if case<3:
            w=[0]*((1<<k)-1)
            for a in range(k):w[((1<<a)|(1<<((a+1)%k)))-1]=1
        acts=d.random_policy(k,m,w,rng);c=d.lib.StrategyCone(k,m,acts)
        a=acts[()];u=d.lib.payoff_row(k,c.root,a);best=(-1,None)
        # Every possible maximal old theme is treated, not just the generating input's max.
        for C in range(k):
            G=np.vstack([-c.matrix]+[size[b]-size[C] for b in range(k)])
            kw=dict(A_ub=G,b_ub=np.zeros(len(G)),A_eq=[np.array(u,float)],b_eq=[1],bounds=(0,None),method='highs')
            for r in range(2,min(m,k)+1):
                for J in itertools.combinations(range(k),r):
                    obj=np.array(d.lib.coverage_row(k,J),float)+(m-r)/m*size[C]
                    res=linprog(-obj,**kw)
                    if not res.success:raise RuntimeError(res.message)
                    if -res.fun>best[0]:best=(-res.fun,{'max_topic':C,'old_slots':r,'portfolio':J})
                    if -res.fun>2*m+1e-7:
                        vals=tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
                        if not c.verify(vals) or d.lib.dot(u,vals)!=1:continue
                        sizes=[sum(v for mask,v in enumerate(vals,1) if mask>>b&1) for b in range(k)]
                        if sizes[C]!=max(sizes):continue
                        value=d.lib.dot(d.lib.coverage_row(k,J),vals)+Fraction(m-r,m)*sizes[C]
                        if value<=2*m:continue
                        cand={'players':m,'topics':k,'max_topic':C,'old_slots':r,'portfolio':J,'value':str(value),'weights':list(map(str,vals)),'actions':[{'history':h,'action':a} for h,a in acts.items()]}
                        (OUT/'safe_padding_candidate.json').write_text(json.dumps(cand,indent=2)+'\n');return records,cand
        rec={'case':case,'k':k,'m':m,'root_action':a,'rows':len(c.rows),'best':best}
        records.append(rec);print(rec,flush=True)
        (OUT/f'safe_padding_probe_n{m}_k{k}_seed{seed}.json').write_text(json.dumps({'scope':'finite float discovery only','records':records},indent=2)+'\n')
    return records,None
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--topics',type=int,default=6);a.add_argument('--players',type=int,default=3);a.add_argument('--cases',type=int,default=8);a.add_argument('--seed',type=int,default=231028);z=a.parse_args();run(z.topics,z.players,z.cases,z.seed)
