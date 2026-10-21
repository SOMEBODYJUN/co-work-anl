"""Targeted probe of the new strategy-uniform-Q strengthening.

Generate an actual full-history SPE by backward induction, independently break
all ordered-history ties, and test a Q for its entire CAG customer cone. No
negative result here is a proof of the universal property.
"""
from common_static_dual_probe import matrices,common_q
from itertools import product
from pathlib import Path
import json,sys
import numpy as np

n,k,trials=map(int,sys.argv[1:4]);seed=20261021
rng=np.random.default_rng(seed)
masks=np.arange(1,1<<k);member=((masks[None,:]>>np.arange(k)[:,None])&1).astype(float)
hs=[h for d in range(n) for h in product(range(k),repeat=d)]
out={'scope':'targeted finite floating diagnostic only; does not establish a universal property',
     'n':n,'k':k,'seed':seed,'trials':[]}
for trial in range(trials):
    w=rng.integers(0,11,len(masks)).astype(float);w[rng.random(len(w))<.5]=0
    ends={h:h for h in product(range(k),repeat=n)};policy={}
    for h in reversed(hs):
        values=[]
        for a in range(k):
            z=ends[h+(a,)];load=member[list(z)].sum(axis=0)
            coef=np.divide(member[a],load,out=np.zeros(len(masks)),where=load>0)
            values.append(coef@w)
        vmax=max(values);choices=[a for a,v in enumerate(values) if abs(v-vmax)<1e-10]
        a=int(rng.choice(choices));policy[h]=a;ends[h]=ends[h+(a,)]
    print('constructed',trial,'root',ends[()],flush=True)
    g,st,c,bs,z=matrices(n,k,policy);r,aeq,beq=common_q(g,st,c,n)
    item={'trial':trial,'root':z,'success':r.success,'message':r.message}
    if r.success:item['Q']=[{'background':b,'probability':float(v)} for b,v in zip(bs,r.x[:len(bs)]) if v>1e-8]
    else:
        item['policy']=[{'history':h,'action':policy[h]} for h in hs]
        item['weights']=w.tolist()
    out['trials'].append(item)
    print('commonQ',trial,r.success,flush=True)
    if not r.success:break
Path(__file__).with_name(f'common_q_generated_n{n}_k{k}_diagnostic.json').write_text(json.dumps(out,indent=2)+'\n')
