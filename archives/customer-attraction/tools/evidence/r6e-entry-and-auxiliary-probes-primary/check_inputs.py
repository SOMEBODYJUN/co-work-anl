"""Definition-level seed and harmonic-PNE checks; no solver imports."""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json,hashlib
BASE=Path(__file__).resolve().parent
SOURCES=json.loads((BASE/'source-manifest.json').read_text())
def primary(sid):
 x=next(x for x in SOURCES if x['id']==sid)
 p=BASE/'original'/x['path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
 return json.loads(p.read_text())
seed=primary('11b20b3cd0f9f814da06')
inst=seed['instance']; p=len(inst['topics']); m=inst['players']
units=[frozenset(t['topics']) for t in inst['customers'] for _ in range(t['multiplicity'])]
actions={tuple(h):a for h,a in seed['actions']}
required={h for d in range(m) for h in product(range(p),repeat=d)}
assert len(actions)==len(seed['actions']) and set(actions)==required
assert all(a in range(p) for a in actions.values())
def leaf(h):
 while len(h)<m:h=h+(actions[h],)
 return h
def pay(z,i):
 return sum((F(1,sum(a in c for a in z)) for c in units if z[i] in c),F(0))
def welfare(z):return sum(any(a in c for a in z) for c in units)
rows=[]
for h in sorted(required,key=lambda h:(len(h),h)):
 if not h:continue
 z=leaf(h); u=pay(z,len(h))
 for a in range(p):
  alt=leaf(h+(a,)); slack=u-pay(alt,len(h));assert slack>=0
  rows.append({'history':h,'action':a,'actual_leaf':z,'deviation_leaf':alt,'slack':str(slack)})
z=leaf(());root=[pay(leaf((a,)),0) for a in range(p)];u=pay(z,0)
opt=max(welfare(x) for x in combinations_with_replacement(range(p),m))
assert list(z)==seed['actual'] and [str(v) for v in root]==seed['root_deviation_payoffs']
assert str(u)==seed['actual_root_payoff'] and str(max(root)-u)==seed['root_regret']
assert welfare(z)==seed['W'] and opt==seed['OPT_m']
assert len(required)-1==seed['positive_depth_decision_histories']
out={'seed':{'customers':len(units),'decision_nodes':len(required),'positive_depth_nodes':len(required)-1,'positive_depth_comparisons_including_self':len(rows),'actual':z,'actual_payoffs':[str(pay(z,i)) for i in range(m)],'root_deviation_payoffs':[str(v) for v in root],'root_regret':str(max(root)-u),'W':welfare(z),'OPT':opt,'repair_margin':str(F(opt-2*welfare(z))-3*(max(root)-u)),'all_positive_depth_IC':rows}}
# Independently calculate the specific known-input harmonic implication in the README.
cert=json.loads((BASE/'runtime/evidence/certificates/customer_attraction/worst_pne_welfare_failure.json').read_text())
# The canonical instance and certificate are separate frozen inputs.
i=json.loads((BASE/'runtime/examples/customer_attraction/worst_pne_welfare_failure.json').read_text()); pu=len(i['topics']); mu=i['players']
cs=[(frozenset(t['topics']),t.get('multiplicity',1)) for t in i['customers']]
def util(z,j):return sum((F(n,sum(a in c for a in z)) for c,n in cs if z[j] in c),F(0))
def phi(z):return sum((n*sum((F(1,k) for k in range(1,sum(a in c for a in z)+1)),F(0)) for c,n in cs),F(0))
pnes=[]
for z in combinations_with_replacement(range(pu),mu):
 if all(util(z,j)>=util(z[:j]+(a,)+z[j+1:],j) for j in range(mu) for a in range(pu)):
  pnes.append({'counts':[z.count(a) for a in range(pu)],'phi':str(phi(z))})
assert len(pnes)==2 and {x['phi'] for x in pnes}=={'45/2'}
assert phi((0,3,3))==F(133,6)
out['known_input_harmonic_implication']={'actual':[0,3,3],'actual_phi':str(phi((0,3,3))),'all_static_pne_count_vectors':pnes,'strict_potential_gap':str(F(45,2)-F(133,6)),'scope':'specific known 16-customer input; no new half counterexample'}
(BASE/'input-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:({j:v for j,v in x.items() if j!='all_positive_depth_IC'} if isinstance(x,dict) else x) for k,x in out.items()},ensure_ascii=False))
