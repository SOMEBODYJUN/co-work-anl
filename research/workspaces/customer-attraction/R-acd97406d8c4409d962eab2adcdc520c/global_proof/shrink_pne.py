import json,time
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate
from .scan_bridges import check,comps
base='research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/'
obj=json.load(open(base+'bridge_counterexample.json'));inst=Instance.from_dict(obj['instance'])
changed=True
while changed:
 changed=False
 for t in range(inst.topic_count):
  customers=[]
  for z in inst.customers:
   ts=frozenset(x-int(x>t) for x in z.topics if x!=t)
   if ts:customers.append(CustomerType(ts,z.multiplicity))
  trial=Instance(tuple(str(x) for x in range(inst.topic_count-1)),tuple(customers),inst.players)
  r=check(trial)
  if r and r[0]=='PNE':inst=trial;changed=True;print('topic',t,inst.topic_count,flush=True);break
 if changed:continue
 for i,z in enumerate(inst.customers):
  for val in [0]+list(range(1,z.multiplicity)):
   cs=list(inst.customers)
   if val:cs[i]=CustomerType(z.topics,val)
   else:cs.pop(i)
   trial=Instance(inst.topics,tuple(cs),inst.players)
   r=check(trial)
   if r and r[0]=='PNE':inst=trial;changed=True;print('weight',i,val,inst.customer_count,len(inst.customers),flush=True);break
  if changed:break
r=check(inst);kind,c,v,solver=r
cert=solver.certificate(target_counts=c);verify_certificate(inst,cert).assert_valid()
obj={'kind':kind,'instance':inst.to_dict(),'counts':c,'welfare':inst.welfare(c),'comparison':v,'certificate':cert.to_dict()}
open(base+'pne_bridge_reduced.json','w').write(json.dumps(obj,indent=2))
print(json.dumps({k:v for k,v in obj.items() if k!='certificate'},indent=2))
print('path',cert)
