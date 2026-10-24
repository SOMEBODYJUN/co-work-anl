"""One exact diagnostic for the general entrywise symmetric extra-slot budget.

Candidate under test: for every full-history SPE and every pair of legal
queries a,t, sum_i [K_i(t,a)+K_i(a,t)] <= 2 W.  This is stronger than the
known open all-p weak aggregate budget.  No finite pass proves the claim.
"""
import itertools,json,pathlib
from fractions import Fraction as F
ROOT=pathlib.Path(__file__).resolve().parents[5]
OUT=pathlib.Path(__file__).resolve().parent
rows=[]
for ip in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
 cp=ROOT/'evidence/certificates/customer_attraction'/ip.name
 if not cp.exists():continue
 obj=json.loads(ip.read_text());cert=json.loads(cp.read_text())
 strategy=cert.get('strategy',{}) if isinstance(cert,dict) else {}
 if not isinstance(strategy,dict) or not strategy.get('actions'):continue
 acts={tuple(r['history']):r['action'] for r in strategy['actions']}
 m=obj['players'];k=len(obj['topics'])
 if len(acts)!=sum(k**i for i in range(m)):continue
 cs=[(frozenset(c['topics']),c.get('multiplicity',1)) for c in obj['customers']]
 def end(h):
  while len(h)<m:h=h+(acts[h],)
  return h
 def payoff(a,z,extra=0):
  return sum((F(w,extra+sum(t in c for t in z)) for c,w in cs if a in c),F())
 for h in acts:
  assert payoff(acts[h],end(h))>=max(payoff(a,end(h+(a,))) for a in range(k))
 z=end(());W=sum(w for c,w in cs if any(t in c for t in z))
 H=[[F() for a in range(k)] for t in range(k)]
 for i in range(m):
  Z=[end(z[:i]+(a,)) for a in range(k)]
  for t,a in itertools.product(range(k),repeat=2):H[t][a]+=payoff(t,Z[a],1)
 a,t=max(itertools.product(range(k),repeat=2),key=lambda pair:H[pair[0]][pair[1]]+H[pair[1]][pair[0]])
 value=(H[t][a]+H[a][t])/2
 row={'instance':ip.name,'m':m,'W':W,'queries':[a,t],'sym_entry':str(value),'gap':str(value-W),'H':[[str(v) for v in x] for x in H]}
 rows.append(row)
 print(ip.name,'gap',str(value-W),'pair',a,t)
(OUT/'pair_kernel_check.json').write_text(json.dumps({'candidate':'all pairs symmetric extra-slot entries <= W','status':'exact finite diagnostics only','rows':rows},indent=2)+'\n')
