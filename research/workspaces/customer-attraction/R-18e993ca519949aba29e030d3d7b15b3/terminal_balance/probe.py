"""Attack the sufficient bridge (m-1) u_last <= W, using exact SPE paths."""
import json,random,sys,time
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate
rng=random.Random(51021)
start=time.monotonic()
for m,p,trials in [(3,4,200),(4,4,200),(5,4,200),(6,4,100),(5,5,100)]:
 for trial in range(trials):
  types=[]
  for mask in range(1,1<<p):
   weight=rng.randrange(7)
   if weight: types.append(CustomerType(frozenset(a for a in range(p) if mask>>a&1),weight))
  inst=Instance(tuple(map(str,range(p))),tuple(types),m)
  solver=ExactSPESolver(inst)
  for path in solver.ordered_outcomes():
   c=inst.counts(path,terminal=True);w=inst.welfare(c);last=inst.topic_payoffs(c)[path[-1]]
   if (m-1)*last>w:
    cert=solver.certificate(on_path=path);report=verify_certificate(inst,cert);report.assert_valid()
    result={'status':'bridge_refuted','m':m,'p':p,'trial':trial,'seed':51021,'path':path,'welfare':w,'last':str(last),'gap':str((m-1)*last-w),'instance':inst.to_dict(),'certificate':cert.to_dict()}
    out=Path(__file__).with_name('failure.json');out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('certificate','instance')}),flush=True)
    raise SystemExit
 print('completed',m,p,trials,'seconds',time.monotonic()-start,flush=True)
