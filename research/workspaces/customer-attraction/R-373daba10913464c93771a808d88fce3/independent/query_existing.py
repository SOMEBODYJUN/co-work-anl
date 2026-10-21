import sys,json,itertools
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate

def compositions(n,k):
 if k==1:
  yield (n,); return
 for z in range(n+1):
  for v in compositions(n-z,k-1):yield (z,)+v

def check(inst, cert):
 actions=cert.actions
 def path(h):
  while len(h)<inst.players:h=h+(actions[h],)
  return h
 actual=path(())
 W=inst.welfare(inst.counts(actual))
 V=[Fraction(0)]*inst.topic_count
 for i in range(inst.players):
  for j in range(inst.topic_count):
   out=path(actual[:i]+(j,));q=inst.counts(out); V[j]+=inst.topic_payoff(j,q)
 best=None
 for q in compositions(inst.players,inst.topic_count):
  O=inst.welfare(q);query=sum(n*v for n,v in zip(q,V))
  gap=inst.players*O-(inst.players-1)*W-query
  if best is None or gap>best[0]:best=(gap,q,O,query)
 return actual,W,V,best

for p in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
 c=ROOT/'evidence/certificates/customer_attraction'/p.name
 if not c.exists():continue
 data=json.loads(c.read_text());data=data.get('strategy',data)
 if 'actions' not in data or 'terminal_counts' not in data:continue
 try:
  inst=Instance.from_dict(json.loads(p.read_text()));cert=StrategyCertificate.from_dict(data)
  actual,W,V,best=check(inst,cert)
  print(p.stem,'m',inst.players,'W',W,'gap',str(best[0]),'q',best[1],flush=True)
 except Exception as e:print(p.name,type(e).__name__,str(e),flush=True)
