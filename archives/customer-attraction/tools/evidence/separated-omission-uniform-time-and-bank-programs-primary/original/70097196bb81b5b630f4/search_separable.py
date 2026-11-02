"""Finite diagnostic of an explicit candidate, not a general theorem."""
from pathlib import Path
import sys,json,random,time
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import CustomerType,Instance,ExactSPESolver,verify_certificate
rng=random.Random(728551)
summary={'candidate':'D<=W when each theme meets at most one omitted component, each component fully available','cases':0,'seed':728551,'found':None}
t0=time.time()
for m,k,tries in [(2,2,2000),(3,3,400),(4,3,30)]:
 q=2*k+m
 for trial in range(tries):
  # Disjoint omitted blocks, each present in two variants. Banks cover C.
  a=[rng.randrange(1,11) for _ in range(k)]
  customers=[CustomerType(frozenset({2*j,2*j+1}),a[j]) for j in range(k)]
  for _ in range(rng.randrange(3,14)):
   cover={t for t in range(2*k) if rng.randrange(2)}
   cover.update(2*k+t for t in range(m) if rng.randrange(2))
   if not any(t>=2*k for t in cover):cover.add(2*k+rng.randrange(m))
   customers.append(CustomerType(frozenset(cover),rng.randrange(1,7)))
  inst=Instance(tuple(map(str,range(q))),tuple(customers),m)
  W=sum(c.multiplicity for c in customers[k:])
  # Every bank theme participates in actual C; selected bank combination must cover it.
  D=sum(a)
  if D<=W:continue
  solver=ExactSPESolver(inst)
  for outcome in solver.outcomes():
   if any(outcome[:2*k]):continue
   w=inst.welfare(outcome)
   if D>w:
    cert=solver.certificate(outcome);verify_certificate(inst,cert).assert_valid()
    summary['found']={'m':m,'k':k,'trial':trial,'D':D,'W':w,'outcome':outcome,'customers':[{'topics':sorted(c.topics),'multiplicity':c.multiplicity} for c in customers],'certificate':cert.to_dict()}
    break
  summary['cases']+=1
  if summary['found']:break
 if summary['found']:break
summary['elapsed_seconds']=time.time()-t0
out=Path(__file__).with_name('separable_search_audit.json');out.write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k!='found'},indent=2));print('FOUND',summary['found'] is not None)
