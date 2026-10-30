"""Independent definition-level audit; no imports of author code or repository solvers."""
import json,hashlib
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from math import comb
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
import argparse
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input',type=Path,default=ROOT/'examples/customer_attraction/dynamic_iid_local.json')
parser.add_argument('--certificate',type=Path,default=ROOT/'evidence/certificates/customer_attraction/dynamic_iid_local.json')
parser.add_argument('--output',type=Path,help='Create a new report; refuse to overwrite existing files.')
args=parser.parse_args()
source=args.input
input_raw=source.read_bytes();certificate_raw=args.certificate.read_bytes()
game=json.loads(input_raw);data=json.loads(certificate_raw)
n=game['players'];m=len(game['topics'])
assert type(n) is int and len(set(game['topics']))==m
weights={}
for row in game['customers']:
 labels=row['topics'];v=row['multiplicity']
 assert labels and len(set(labels))==len(labels)
 assert all(type(a) is int and 0<=a<m for a in labels)
 assert type(v) is int and v>0
 T=sum(1<<a for a in labels)
 assert T not in weights
 weights[T]=v
policy={}
for row in data['certificate']['actions']:
 h=tuple(row['history']);a=row['action']
 assert len(h)<n and all(type(b) is int and 0<=b<m for b in h)
 assert type(a) is int and 0<=a<m and h not in policy
 policy[h]=a
assert (n,m)==(5,7)
clients=[tuple(a for a in range(m) if T>>a&1) for T,w in weights.items() for _ in range(w)]
assert len(clients)==60
assert len(policy)==sum(m**k for k in range(n))==2801
assert set(policy)==set(h for k in range(n) for h in product(range(m),repeat=k))
assert all(a in range(m) for a in policy.values())
assert all(any((a in interests)!=(b in interests) for interests in clients) for a in range(m) for b in range(a))
# Rebuild ordered terminal utilities by expanding to different unit customers.
terminal_pay={};terminal_W={}
for z in product(range(m),repeat=n):
 vals=[F(0)]*n;covered=0
 for interests in clients:
  indices=[i for i,a in enumerate(z) if a in interests]
  if indices:
   covered+=1
   for i in indices:vals[i]+=F(1,len(indices))
 terminal_pay[z]=tuple(vals);terminal_W[z]=covered
 assert sum(vals)==covered

def replay(prefix):
 history=tuple(prefix)
 while len(history)<n:history+=(policy[history],)
 return history
comparisons=0;zero=0;positive=0;minimum=None
for k in range(n):
 for h in product(range(m),repeat=k):
  z=replay(h);incumbent=terminal_pay[z][k]
  for a in range(m):
   alt=replay(h+(a,));slack=incumbent-terminal_pay[alt][k]
   assert slack>=0,(h,a,z,alt,incumbent,terminal_pay[alt][k])
   comparisons+=1;zero+=slack==0;positive+=slack>0
   minimum=slack if minimum is None else min(minimum,slack)
actual=replay(());actual_u=terminal_pay[actual];W=terminal_W[actual]
assert actual==(6,6,0,3,4);assert actual_u==(F(12),F(12),F(10),F(12),F(12));assert W==58
opt=max(terminal_W.values());opt_profile=min(z for z,cov in terminal_W.items() if cov==opt)
assert opt==60 and terminal_W[(0,1,2,6,6)]==60
# Independent pure-query static expectation by enumerating r-1 iid competitors.
def query_pay(prefix,a,B):
 return sum((F(1,1+sum(b in interests for b in prefix+B)) for interests in clients if a in interests),F(0))
def static_state(prefix,q):
 r=n-len(prefix);support=[a for a in range(m) if q[a]]
 alphas=[]
 for a in range(m):
  value=F(0)
  for B in product(support,repeat=r-1):
   probability=F(1)
   for b in B:probability*=q[b]
   value+=probability*query_pay(prefix,a,B)
  alphas.append(value)
 multiplier=sum(q[a]*alphas[a] for a in range(m))
 assert all(x<=multiplier for x in alphas)
 assert all(alphas[a]==multiplier for a in support)
 # Separately reconstruct every type coefficient via Binomial loads.
 alphas_types=[]
 for a in range(m):
  value=F(0)
  for T,w in weights.items():
   if not T>>a&1:continue
   d=sum(bool(T>>b&1) for b in prefix);t=sum((q[b] for b in range(m) if T>>b&1),F(0))
   value+=w*sum((F(comb(r-1,k))*t**k*(1-t)**(r-1-k)/F(d+1+k) for k in range(r)),F(0))
  alphas_types.append(value)
 assert alphas==alphas_types
 # Z is expected TOTAL PAYOUT TO THE REMAINING PLAYERS, with prefix shares excluded.
 Z=F(0);potential=F(0);rent=F(0);coverage=F(0)
 for A in product(support,repeat=r):
  probability=F(1)
  for a in A:probability*=q[a]
  payout=F(0);phi=F(0);prefix_rent=F(0);complete_coverage=0
  for interests in clients:
   d=sum(a in interests for a in prefix);k=sum(a in interests for a in A)
   if k:payout+=F(k,d+k)
   if d:prefix_rent+=F(d,d+k)
   complete_coverage+=bool(d+k)
   phi+=sum((F(1,j) for j in range(d+1,d+k+1)),F(0))
  Z+=probability*payout;potential+=probability*phi
  rent+=probability*prefix_rent;coverage+=probability*complete_coverage
 assert Z==r*multiplier and Z+rent==coverage
 Ztypes=F(0)
 for T,w in weights.items():
  d=sum(bool(T>>b&1) for b in prefix);t=sum((q[b] for b in range(m) if T>>b&1),F(0))
  Ztypes+=w*sum((F(comb(r,k))*t**k*(1-t)**(r-k)*F(k,d+k) for k in range(1,r+1)),F(0))
 assert Z==Ztypes
 return {'prefix':prefix,'remaining_players':r,'q':list(map(str,q)),'all_query_alpha':list(map(str,alphas)),'KKT_multiplier':str(multiplier),'support_equalities':support,'Z':str(Z),'prefix_rent':str(rent),'complete_expected_coverage':str(coverage),'expected_residual_harmonic_potential':str(potential),'outside_P_alpha':str(alphas[6]),'outside_P_strict_slack':str(multiplier-alphas[6])}
states=[]
for row in data['dynamic_iid_states']:
 state=static_state(tuple(row['history']),list(map(F,row['q'])))
 for key in ('Z','prefix_rent','complete_expected_coverage'):
  assert F(state[key])==F(row[key])
 states.append(state)
assert [x['prefix'] for x in states]==[(6,6),(6,6,0),(6,6,0,3)]
state,child,last=states
assert F(state['Z'])==F(97,3);assert F(child['Z'])==21;assert F(last['Z'])==12
assert F(state['outside_P_alpha'])==F(child['outside_P_alpha'])==8
assert list(actual)==data['root'] and list(map(str,actual_u))==data['root_payoffs']
assert [actual.count(a) for a in range(m)]==data['certificate']['terminal_counts']
change=F(state['Z'])-F(child['Z']);required=F(9,10)*change;deficit=required-actual_u[2]
assert change==F(34,3) and required==F(51,5) and deficit==F(data['weak_local_deficit'])==F(1,5)
debts=[F(state['Z'])-F(child['Z'])-actual_u[2],F(child['Z'])-F(last['Z'])-actual_u[3],F(last['Z'])-actual_u[4]]
assert debts==[F(4,3),F(-3),F(0)] and sum(debts)==F(97,3)-sum(actual_u[2:])
assert data['root_Z_exactly_computed'] is False and F(data['root_Z_upper_bound'])==opt
report={
 'claims':['CA-DYNAMIC-IID-DEBT-INTERFACE','CA-WEAK-LOCAL-IID-DRIFT-NO'],
 'input_sha256':hashlib.sha256(input_raw).hexdigest(),
 'certificate_sha256':hashlib.sha256(certificate_raw).hexdigest(),
 'status':'PASS','players':n,'themes':m,'unit_customers':len(clients),
 'pairwise_distinct_coverages':True,'ordered_histories':len(policy),
 'all_comparisons':comparisons,'strict_comparisons':positive,
 'tie_comparisons':zero,'minimum_SPE_slack':str(minimum),
 'actual':actual,'actual_utilities':list(map(str,actual_u)),'W':W,'OPT_5':opt,
 'all_ordered_terminal_profiles':len(terminal_W),
 'one_OPT_profile':(0,1,2,6,6),'half_coverage_slack':2*W-opt,
 'residual_states':states,'old_tail_debts':list(map(str,debts)),
 'old_tail_total_debt':str(sum(debts)),'local_Z_decrease':str(change),
 'weak_drift_factor':'9/10','required_local_payoff':str(required),
 'actual_local_payoff':str(actual_u[2]),'strict_local_deficit':str(deficit),
 'root_Z_exactly_computed':False,'root_Z_upper_bound':str(opt),
 'global_weak_bridge_slack_lower_bound':str(F(W)-F(9,10)*opt),
 'scope':'Only the original-total-n local actual-prefix drift fails. The example satisfies the global weak iid bridge. No unrestricted global iid, aggregate-security, or half-coverage theorem is proved or refuted.'
}
rendered=json.dumps(report,indent=2)+'\n'
if args.output:
 try:
  with args.output.open('x',encoding='utf-8') as handle:handle.write(rendered)
 except FileExistsError:parser.error(f'Refusing to overwrite existing output: {args.output}')
else:print(rendered,end='')
