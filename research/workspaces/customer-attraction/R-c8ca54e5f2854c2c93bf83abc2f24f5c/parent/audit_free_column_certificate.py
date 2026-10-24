"""Independent exact reconstruction of the one-policy free-column evidence.
No all-game or all-policy assertion is tested by a single finite certificate.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,StrategyCertificate,verify_certificate
raw=json.loads((ROOT/'examples/customer_attraction/aggregate_theta_failure.json').read_text())
inst=Instance.from_dict(raw.get('instance',raw))
src=ROOT/'evidence/certificates/customer_attraction/aggregate_theta_failure.json'
obj=json.loads(src.read_text()); cert=StrategyCertificate.from_dict(obj['strategy'])
verify_certificate(inst,cert).assert_valid()
pol=cert.actions; m,k=inst.players,inst.topic_count
clients=[z.topics for z in inst.customers for _ in range(z.multiplicity)]
def finish(g):
 g=tuple(g)
 while len(g)<m:g+=(pol[g],)
 return g
def upay(z,i):
 return sum((F(1,sum(a in x for a in z)) for x in clients if z[i] in x),F())
z=finish(())
checks=0
for d in range(m):
 for h in product(range(k),repeat=d):
  for a in range(k):
   assert upay(finish(h),d)>=upay(finish(h+(a,)),d); checks+=1
M=[]
for i in range(m):
 cols=[]
 for a in range(k):
  w=finish(z[:i]+(a,)); v=w[:i]+w[i+1:]
  cols.append([upay((t,)+v,0) for t in range(k)])
 M.append(cols)
p=[F(0),F(2,5),F(2,5),F(0),F(0),F(1,5)]
qs=[[F(2,5),F(0),F(0),F(3,5),F(0),F(0)],
 [F(1,5),F(4,5),F(0),F(0),F(0),F(0)],
 [F(1),F(0),F(0),F(0),F(0),F(0)]]
assert sum(p)==1 and all(sum(q)==1 for q in qs)
primal=sum(min(sum(p[t]*M[i][a][t] for t in range(k)) for a in range(k)) for i in range(m))
dual=max(sum(qs[i][a]*M[i][a][t] for i in range(m) for a in range(k)) for t in range(k))
assert primal==dual==F(164,5)
pbad=[F(0),F(0),F(1,2),F(0),F(0),F(1,2)]
mins=[min(sum(pbad[t]*M[i][a][t] for t in range(k)) for a in range(k)) for i in range(m)]
assert mins==[F(11),F(19,2),F(12)]
W=sum(upay(z,i) for i in range(m)); assert W==34
assert W-sum(mins)==F(3,2) and W-primal==F(6,5)
# Reconstruct arbitrary anonymous potential coefficient vectors from raw policy.
states=list(combinations_with_replacement(range(k),m))+list(combinations_with_replacement(range(k),m-1))
idx={a:i for i,a in enumerate(states)}; dim=len(states)+m

def phirow(w,i):
 r=[F(0)]*dim
 r[idx[tuple(sorted(w))]]+=1
 r[idx[tuple(sorted(w[:i]+w[i+1:]))]]-=1
 return r

def diff(a,b):return [x-y for x,y in zip(a,b)]
report=json.loads((Path(__file__).parents[1]/'aggregate_security/potential_menu_dual.json').read_text())
assert report['actual_path']==list(z)
acc=[F(0)]*dim
for term in report['terms']:
 coef=F(term['coefficient']); assert coef>=0
 if term['kind']=='IC':
  h=tuple(term['history']); a=term['action']; i=len(h)
  row=diff(phirow(finish(h),i),phirow(finish(h+(a,)),i))
 else:
  i=term['position']; a=term['column']; w=finish(z[:i]+(a,)); v=w[:i]+w[i+1:]
  row=[sum(pbad[t]*phirow((t,)+v,0)[j] for t in range(k)) for j in range(dim)]
  row[len(states)+i]-=1
 acc=[x+coef*y for x,y in zip(acc,row)]
target=[sum(phirow(z,i)[j] for i in range(m)) for j in range(dim)]
for i in range(m):target[len(states)+i]-=1
assert acc==target
out={'scope':'One old policy and its exact cone/certificate only; general aggregate free-column bridge remains OPEN.',
 'source':str(src.relative_to(ROOT)),'full_history_IC_checks':checks,'unit_clients':len(clients),'W':str(W),
 'corrected_old_bad_query_position_minima':list(map(str,mins)),
 'all_query_game_primal':str(primal),'all_query_game_dual':str(dual),'reverse_gap':str(W-primal),
 'anonymous_potential_identity_coordinates':dim,'nonnegative_identity_terms':len(report['terms']),
 'zero_coefficient_remainder':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

# Check the parent's general potential balance, including genuine boundaries.
def potential_balance(unit_clients,policy,n,labels,query,columns):
 def end(g):
  g=tuple(g)
  while len(g)<n:g+=(policy[g],)
  return g
 def phi(leaf):
  return sum((sum((F(1,t) for t in range(1,1+sum(a in x for a in leaf))),F())
              for x in unit_clients),F())
 def util(leaf,i):return phi(leaf)-phi(leaf[:i]+leaf[i+1:])
 actual=end(()); total=sum(util(actual,i) for i in range(n))
 theta=F(); gamma=F(); cross=F()
 for i in range(n):
  assert sum(columns[i])==1
  for a in range(labels):
   branch=end(actual[:i]+(a,)); competitors=branch[:i]+branch[i+1:]
   g=sum(query[t]*(phi(competitors+(t,))-phi(competitors)) for t in range(labels))
   theta+=columns[i][a]*g
   gap=util(actual,i)-util(branch,i); assert gap>=0
   gamma+=columns[i][a]*gap
   cross+=columns[i][a]*(phi(branch)-sum(query[t]*phi(competitors+(t,)) for t in range(labels)))
 assert total-theta==gamma+cross
 return {'lhs':str(total-theta),'IC_slack':str(gamma),'cross_potential':str(cross)}
identities={'old_game':potential_balance(clients,pol,m,k,p,qs)}
for case,n,cust in [('zero_clients',3,[]),('empty_theme',3,[frozenset({0})]*3),
                    ('one_player',1,[frozenset({0}),frozenset({0,1})])]:
 policy={h:0 for d in range(n) for h in product(range(2),repeat=d)}
 identities[case]=potential_balance(cust,policy,n,2,[F(1,2)]*2,[[F(1,2)]*2 for _ in range(n)])
out['general_potential_balance_checks']=identities
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'potential_balance':identities},indent=2))
