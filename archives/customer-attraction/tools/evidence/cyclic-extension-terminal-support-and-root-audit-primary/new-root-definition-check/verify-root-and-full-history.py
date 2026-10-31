from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
root=Path('/workspace/scratch/37f0f9248cfc');p=root/'boss4-research/archives/customer-attraction/tools/evidence/R-18-global-proof-incumbent-20261031/original/largest_incumbent_n3p6_best.json';data=p.read_bytes();assert hashlib.sha256(data).hexdigest()=='7dcd445bdfe275e7b0521945ad4242aea3f3401dc0df848fb01c5bcb2fcfcbbd'
x=json.loads(data);m=x['instance']['players'];k=len(x['instance']['topics']);assert (m,k)==(3,6)
clients=[frozenset(c['topics'])for c in x['instance']['customers']for _ in range(c['multiplicity'])];assert len(clients)==963
policy={tuple(r['history']):r['action']for r in x['strategy']['actions']};histories=[h for n in range(m)for h in product(range(k),repeat=n)];assert set(policy)==set(histories) and len(policy)==43

def leaf(h):
 while len(h)<m:h=h+(policy[h],)
 return h

def payoff(a,z):
 return sum((F(1,sum(b in C for b in z))for C in clients if a in C),F(0))

def coverage(z):return sum(any(b in C for b in z)for C in clients)
rows=[];profitable=[]
for h in histories:
 a=policy[h];actual=leaf(h);u=payoff(a,actual);values=[]
 for b in range(k):
  z=leaf(h+(b,));v=payoff(b,z);slack=u-v;values.append(dict(action=b,leaf=z,payoff=str(v),slack=str(slack)))
  if slack<0:profitable.append(dict(history=h,prescribed=a,alternative=b,actual_payoff=str(u),deviation_payoff=str(v),gain=str(-slack),deviation_leaf=z))
 rows.append(dict(history=h,prescribed=a,actual_leaf=actual,actual_payoff=str(u),alternatives=values))
actual=leaf(());outcomes=[(coverage(z),z)for z in product(range(k),repeat=m)];opt=max(w for w,_ in outcomes);w=coverage(actual);profits=[payoff(a,actual)for a in actual]
assert actual==(0,2,3) and profits==[F(375,2),F(579,2),F(273)] and w==750 and opt==963
assert len(profitable)==5 and all(not t['history']for t in profitable)
assert [F(v['payoff'])for v in rows[0]['alternatives']]==[F(375,2),F(303),F(303),F(357),F(190),F(303)]
assert coverage((0,2,3))==750
print(json.dumps(dict(scope='new direct unit-client definition check of disputed existing certificate; no original validator/LP/SPE solver import; no new source done',input_sha256=hashlib.sha256(data).hexdigest(),unit_clients=len(clients),histories=len(histories),comparisons_including_self=len(histories)*k,nonself_comparisons=len(histories)*(k-1),source_verified_flag=x['verified'],is_SPE=False,actual=actual,profits=list(map(str,profits)),W=w,OPT=opt,optimal_ordered_triples=[z for a,z in outcomes if a==opt],source_ratio_is_only_formal_policy_arithmetic=str(F(opt,profits[0])),profitable_deviations=profitable,all_history_rows=rows,all_216_coverage_values=[dict(leaf=z,coverage=a)for a,z in outcomes],source_claim_that_actual_023_covers_all_is_false=True),indent=2)+'\n',end='')
