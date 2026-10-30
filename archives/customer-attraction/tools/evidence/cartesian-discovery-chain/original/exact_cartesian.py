"""Exact recheck of Cartesian SPE welfare nonadditivity candidate."""
from pathlib import Path
import json,itertools as it
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate
OUT=Path(__file__).resolve().parent
rs=[[0,7,3,2,2,4,9],[8,0,1,1,4,8,2]]
sets=[]
for j,r in enumerate(rs):
 ss=[set()for _ in range(3)];x=0
 for mask,mult in enumerate(r,1):
  for t in range(mult):
   for a in range(3):
    if mask>>a&1:ss[a].add((j,x))
   x+=1
 sets.append(ss)
ins=[]
for ss in sets:ins.append(Instance.from_topic_sets(ss,players=3))
ssprod=[ss|tt for ss,tt in it.product(*sets)]
ins.append(Instance.from_topic_sets(ssprod,players=3))
res=[]
for j,I in enumerate(ins):
 sol=ExactSPESolver(I);W=sol.minimum_welfare();cert=sol.worst_certificate();verify_certificate(I,cert).assert_valid()
 rec=dict(index=j,instance=I.to_dict(),W=W,OPT=I.optimal_welfare(),outcomes=[list(x)for x in sol.outcomes()],certificate=cert.to_dict(),verification=str(verify_certificate(I,cert)))
 res.append(rec)
 print(j,W,I.optimal_welfare(),len(sol.outcomes()),flush=True)
assert res[2]['W']<res[0]['W']+res[1]['W']
(OUT/'exact_cartesian_candidate.json').write_text(json.dumps(res,indent=2))
