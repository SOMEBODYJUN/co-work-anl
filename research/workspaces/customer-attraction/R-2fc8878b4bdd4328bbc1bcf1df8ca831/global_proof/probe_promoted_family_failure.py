"""Reproduce the three already observed finite oracle checks.
This script is a saved reproduction command, not the general failure proof.
"""
from customer_attraction import ExactSPESolver
from customer_attraction.model import Instance,CustomerType
import json
records=[]
for t,k in ((3,1),(3,2),(4,1)):
 p=k*(t+1)+t-1;m=k+t-1;customers=[]
 for i in range(k):
  customers.append(CustomerType(frozenset(range(i*(t+1),(i+1)*(t+1))),t))
  customers.append(CustomerType(frozenset((i*(t+1),)),t-1))
 for r in range(t-1):
  customers.append(CustomerType(frozenset([i*(t+1)+1+r for i in range(k)]+[k*(t+1)+r]),t-1))
  customers.append(CustomerType(frozenset((k*(t+1)+r,)),1))
 instance=Instance(tuple(map(str,range(p))),tuple(customers),m)
 target=tuple(int(a>=k*(t+1)or a%(t+1)==t)for a in range(p))
 outcomes=ExactSPESolver(instance).outcomes()
 records.append({'t':t,'k':k,'players':m,'topics':p,'target_counts':target,'target_is_SPE_outcome':target in outcomes,'SPE_outcome_count':len(outcomes)})
print(json.dumps(records,indent=2))
