"""Independent definition-level audit, no imports from discovery or game code."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
MASSES={1:10,2:13,4:8,8:8,20:5,24:5,36:5,40:5,49:6,50:4,54:1,58:1}
LABELS=('A','B','T','S','E','F')
REPLY=(1,4,4,4,5,4)
CLIENTS=[frozenset(a for a in range(6)if mask>>a&1)for mask,mass in MASSES.items()for _ in range(mass)]
TOPICS=[frozenset(x for x,c in enumerate(CLIENTS)if a in c)for a in range(6)]
assert len(set(TOPICS))==6

def payoff(history,i):
 return sum((F(1,sum(history[j] in clients for j in range(2)))for clients in CLIENTS if history[i]in clients),F(0))
def welfare(history):return len(set().union(*(TOPICS[a]for a in history)))

def main():
 checks=[]
 for a,b in enumerate(REPLY):
  base=payoff((a,b),1)
  for alt in range(6):
   v=payoff((a,alt),1);assert base>=v
   checks.append(dict(history=[a],chosen=b,alternative=alt,payoff=str(base),alternative_payoff=str(v),slack=str(base-v)))
 base=payoff((0,1),0)
 for a,b in enumerate(REPLY):
  v=payoff((a,b),0);assert base>=v
  checks.append(dict(history=[],chosen=0,alternative=a,payoff=str(base),alternative_payoff=str(v),slack=str(base-v)))
 values={tuple(pair):welfare(pair)for pair in product(range(6),repeat=2)}
 opt=max(values.values());supports=sorted({tuple(sorted(pair))for pair,w in values.items()if w==opt})
 C=TOPICS[0]|TOPICS[1];O=TOPICS[2]|TOPICS[3];R=O-C
 assert supports==[(2,3)]
 assert len(C)==35 and opt==38 and len(R)==36
 assert 2*len(C)>=opt and len(R)>len(C)
 result=dict(status='exact independent unit-client replay',customers=len(CLIENTS),distinct_topics=True,histories=7,comparisons=len(checks),strategy={'root':0,'reply':REPLY},actual=[0,1],payoffs=[str(payoff((0,1),i))for i in range(2)],W=len(C),OPT=opt,optimal_supports=supports,optimal_intersection=len(O&C),optimal_uncovered=len(R),half_slack=2*len(C)-opt,uncovered_bridge_violation=len(R)-len(C),coverage_table=[dict(pair=list(pair),coverage=w)for pair,w in values.items()],checks=checks)
 dest=Path(__file__).with_name('uncovered_optimum_audit.json');dest.write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items()if k not in ['coverage_table','checks']}))
if __name__=='__main__':main()
