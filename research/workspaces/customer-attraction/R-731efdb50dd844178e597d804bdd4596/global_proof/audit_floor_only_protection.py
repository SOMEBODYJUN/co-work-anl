from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path

customers=[]
for copy in range(3):
 X=tuple(copy*6+a for a in range(3));Y=tuple(copy*6+a for a in range(3,6))
 for a in X:
  for b in Y:customers.append(frozenset((a,b)))
 for I in combinations(X,2):
  for J in combinations(Y,2):customers.extend([frozenset(I+J)]*3)
def utility(path,i):return sum((Fraction(1,sum(a in B for a in path)) for B in customers if path[i] in B),Fraction())
def welfare(path):return sum(any(a in B for a in path) for B in customers)
sizes=[welfare((a,)) for a in range(18)]
assert sizes==[21]*18
opt=max(welfare(J) for J in combinations(range(18),3));assert opt==63
threshold=Fraction(opt,6);rows=[]
for a in range(18):
 copy,local=divmod(a,6);other=range(copy*6+(3 if local<3 else 0),copy*6+(6 if local<3 else 3))
 b,c=tuple(other)[:2];path=(a,b,c);pay=tuple(utility(path,i) for i in range(3));assert pay==(10,12,12)
 assert pay[0]<threshold<min(pay[1:])
 outside=((copy+1)%3)*6;dev=utility((a,b,outside),2);assert dev==21>pay[2]
 rows.append({'root':a,'path':path,'payoffs':list(map(str,pay)),'last_deviation':outside,'deviation_payoff':str(dev)})
out={'status':'exact_instance_audit_passed','scope':'noncredible floor-only protection obstruction; no SPE claimed','players':3,'topics':18,'unit_customers':len(customers),'OPT':opt,'threshold':str(threshold),'root_actions_checked':len(rows),'witnesses':rows}
path=Path(__file__).with_name('floor_only_protection_audit.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='witnesses'},ensure_ascii=False,indent=2))
