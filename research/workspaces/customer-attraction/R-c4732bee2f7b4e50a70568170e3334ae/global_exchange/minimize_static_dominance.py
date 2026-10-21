"""Heuristic integer minimization; every accepted candidate is exact verified."""
import importlib,json
from customer_attraction import *
f=importlib.import_module('research.workspaces.customer-attraction.R-c4732bee2f7b4e50a70568170e3334ae.global_exchange.static_dominance_probe')
p='research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/global_exchange/'
r=json.load(open(p+'static_dominance_sparse_result.json')); base=r['instance']; masks=[x['topics'] for x in base['customers']]; weights=[x['multiplicity'] for x in base['customers']]
def check(w,m=5):
 ins=Instance(tuple(base['topics']),tuple(CustomerType(frozenset(mask),z) for mask,z in zip(masks,w) if z),m)
 ss=ExactSPESolver(ins);sp=ss.minimum_welfare();pnes=list(f.pne_counts(ins));pn=min(map(ins.welfare,pnes))
 return (sp<pn),(ins,ss,pnes,sp,pn)
change=True
while change:
 change=False
 for j,z in enumerate(weights):
  for zz in range(z):
   w=weights.copy();w[j]=zz;good,_=check(w)
   if good:weights=w;change=True;print('reduced',weights,flush=True);break
ok,(ins,ss,pnes,sp,pn)=check(weights)
cert=ss.worst_certificate();verify_certificate(ins,cert).assert_valid()
res={'instance':ins.to_dict(),'weights':weights,'worst_spe':sp,'worst_spe_counts':[list(q) for q in ss.worst_outcomes()],'worst_pne':pn,'pne_counts':[list(q) for q in pnes],'spe_count':len(ss.outcomes()),'opt':ins.optimal_welfare()}
json.dump(res,open(p+'static_dominance_minimized.json','w'),indent=2)
json.dump(cert.to_dict(),open(p+'static_dominance_certificate.json','w'),indent=2)
print(json.dumps(res,indent=2),flush=True)
for m in (2,3,4,6):
 ok,(_,_,_,sp,pn)=check(weights,m);print('other_m',m,'spe',sp,'pne',pn,flush=True)
