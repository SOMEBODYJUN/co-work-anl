"""Finite search on all SPE outcomes; fractional cap values checked rationally."""
from pathlib import Path
from fractions import Fraction as F
import importlib.util
import random,json,time
import numpy as np

ROOT=Path(__file__).resolve().parents[5]
source=ROOT/'research/workspaces/customer-attraction/R-d28e1c3c70cf4adfbb52398ac7cf4c7b/experiments/cex_exact_sweep.py'
spec=importlib.util.spec_from_file_location('prior_exact',source)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)

def run(k,m,trials,seed):
    s=prior.IntegerSetSolver(k,m);rng=random.Random(seed)
    bits=np.array([[(t>>a)&1 for t in s.types] for a in range(k)],dtype=int)
    qmat=np.array(s.terminals,dtype=int)
    loads=qmat@bits
    coeff=bits[None,:,:]/(1+F(m-1,m)*loads[:,None,:])
    coeff=np.asarray(coeff,dtype=float)
    champ=[0]*len(s.types);champ[0]=m
    for a in range(1,min(k,m)):champ[(1<<a)-1]=1
    best=0.;records=[];tested=0;start=time.monotonic()
    for i in range(trials):
        if i==0:w=champ.copy()
        elif i%29==0:w=[rng.randrange(1,21) if rng.random()<.15 else 0 for _ in s.types]
        elif i%17==0:
            w=[0]*len(s.types)
            for a in range(k):w[(1<<a)-1]=rng.randrange(1,m+3)
            for _ in range(k):w[rng.randrange(len(w))]+=rng.randrange(1,m+3)
        else:
            w=champ.copy()
            for _ in range(rng.randrange(1,5)):
                j=rng.randrange(len(w));w[j]=max(0,w[j]+rng.choice((-3,-2,-1,1,2,3)))
        out=s.solve(w);local=0.
        for q in out['root_outcomes']:
            j=s.tindex[q];W=int(s.last_welfare[j]);tested+=1
            if not W:continue
            vals=coeff[j]@w;a=int(np.argmax(vals));ratio=(m-.5)*vals[a]/W
            local=max(local,ratio)
            if ratio>best+1e-10:
                cap=sum((F(v)/(1+F(m-1,m)*sum(q[b] for b in range(k) if t>>b&1)) for t,v in zip(s.types,w) if t>>a&1),F(0))
                exact=F(2*m-1,2)*cap/W
                assert abs(float(exact)-ratio)<1e-10
                best=ratio
                rec={'trial':i,'counts':q,'query':a,'W':W,'cap':str(cap),'ratio':str(exact),'weights':w}
                records.append(rec)
                print(json.dumps({x:v for x,v in rec.items() if x!='weights'}),flush=True)
                if exact>1:
                    return dict(status='candidate needs ordered-strategy certificate',records=records,topics=k,players=m,trials_completed=i+1,seed=seed,tested_outcomes=tested,seconds=time.monotonic()-start)
        if local>=best-1e-10 or rng.random()<.05:champ=w.copy()
    return dict(status='finite search only; no violation',records=records,topics=k,players=m,trials_completed=trials,seed=seed,tested_outcomes=tested,seconds=time.monotonic()-start)

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('--topics',type=int,default=7);a.add_argument('--players',type=int,default=5);a.add_argument('--trials',type=int,default=2000);a.add_argument('--seed',type=int,default=20261021);a.add_argument('--output',type=Path,required=True);x=a.parse_args()
    assert not x.output.exists()
    # Zero, m=1, one-theme and all-tie cases use the same exact backend.
    selftest=prior.self_test()
    r=run(x.topics,x.players,x.trials,x.seed);r['backend_selftest']=selftest
    x.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='records'}),flush=True)
