"""Only checks whether ADM is refuted by natural modifications of the old 71-client seed."""
from pathlib import Path
import sys,json,random
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P))
from probe_adm import Instance,CustomerType,check
cs=[([0],9),([1],9),([2],13),([3],8),([0,4],1),([1,4],4),([3,4],5),([0,5],1),([1,5],4),([3,5],5),([0,4,5],5),([2,4,5],5),([1,2,4,5],1),([1,3,4,5],1)]
rng=random.Random(63531);records=[];checked=0
for k in range(180):
    m=rng.choice([3,4,5]);q=6
    # Multiplicity mutations leave every customer unit-valued and every topic common.
    types=[CustomerType(frozenset(t),max(1,round(w*rng.choice([.5,.7,1,1,1.3,1.7,2])))) for t,w in cs]
    if k%2:
        q=7
        # A shared supporting topic whose incidence is explicit and finite.
        chosen=[i for i in range(len(types)) if rng.random()<.5]
        types=[CustomerType(ty.topics|({6} if i in chosen else set()),ty.multiplicity) for i,ty in enumerate(types)]
        private=rng.randrange(0,14)
        if private:types.append(CustomerType(frozenset({6}),private))
    ins=Instance(tuple(map(str,range(q))),tuple(types),m)
    best,n=check(ins,f'old71-mutation-{k}',rng,10);checked+=n
    if best:records.append(best)
    if k%20==0:print(k,checked, max((x['gap'] for x in records),default=None),flush=True)
    if best and best['gap']>1e-7:break
out=dict(scope=__doc__,checked=checked,records=sorted(records,key=lambda x:x['gap'],reverse=True)[:10]);(P/'seed_family_discovery.json').write_text(json.dumps(out,indent=2)+'\n')
print('BEST',out['records'][0] if out['records'] else None)
