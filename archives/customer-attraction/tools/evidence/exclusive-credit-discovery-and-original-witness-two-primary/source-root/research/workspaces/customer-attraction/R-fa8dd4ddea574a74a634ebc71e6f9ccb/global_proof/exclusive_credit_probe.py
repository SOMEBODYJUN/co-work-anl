"""Exact finite attack on the proposed first-exclusive local credit."""
import sys,random,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType,Instance,ExactSPESolver,verify_certificate
rng=random.Random(111290)
for k in range(2000):
 p=rng.choice([4,5,6]);m=rng.choice([2,3,4])
 weights={s:rng.randint(1,12) for s in rng.sample(range(1,1<<p),rng.randint(3,min(12,(1<<p)-1)))}
 inst=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(i for i in range(p) if s>>i&1),w) for s,w in weights.items()),m)
 sol=ExactSPESolver(inst);floor=sol.threshold((0,)*p)
 for c in sol.outcomes():
  val=[F(0) for _ in range(p)]
  for t in inst.customers:
   load=sum(c[a] for a in t.topics)
   for a in t.topics:val[a]+=F(t.multiplicity,load+1)
  M=max(val)
  for a in range(p):
   cc=tuple(int(a==j) for j in range(p))
   if c not in sol.outcomes(cc) or inst.topic_payoff(a,c)<floor:continue
   credit=sum(F(t.multiplicity,2) for t in inst.customers if a in t.topics and sum(c[i] for i in t.topics)==1)
   gap=inst.topic_payoff(a,c)+credit-M
   if gap<0:
    path=next(path for path in sol.ordered_outcomes(c) if path[0]==a)
    cert=sol.certificate(on_path=path);verify_certificate(inst,cert).assert_valid()
    record={'status':'exact_local_counterexample','seed':111290,'iteration':k,'instance':inst.to_dict(),'actual':path,'counts':c,'root_action':a,'root_payoff':str(inst.topic_payoff(a,c)),'exclusive_credit':str(credit),'entrant_values':list(map(str,val)),'gap':str(gap),'certificate':cert.to_dict()}
    f=Path(__file__).with_name('exclusive_credit_witness.json');f.write_text(json.dumps(record,indent=2));print('FOUND',k,str(gap),f,flush=True);sys.exit()
print('NO COUNTEREXAMPLE',k+1)
