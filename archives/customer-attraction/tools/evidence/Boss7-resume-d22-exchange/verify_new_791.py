"""One new definition-level check of the previously unavailable 791 input only.
No original author entry, solver, NumPy, SciPy, optimization or 24-case execution.
"""
import hashlib,json,sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions must remain enabled')
source=Path(sys.argv[1]);output=Path(sys.argv[2]);raw=source.read_bytes();d=json.loads(raw)
k=len(d['topics']);m=3
assert k==7 and d['customers']==791
counts={int(T):v for T,v in d['integer_types'].items()};assert all(type(v)is int and v>0 for v in counts.values())and all(0<T<(1<<k)for T in counts)
assert sum(counts.values())==791
expected={h for z in range(m)for h in product(range(k),repeat=z)}
policy={tuple(x['history']):x['action']for x in d['actions']};assert len(policy)==len(d['actions'])==len(expected)==57 and set(policy)==expected and all(type(a)is int and 0<=a<k for a in policy.values())
sets=[{T for T in counts if T>>a&1}for a in range(k)];assert len({frozenset(s)for s in sets})==7 and not sets[6]
def finish(h):
 h=tuple(h)
 while len(h)<m:h+=policy[h],
 return h
def u(a,z,extra=0):
 return sum((F(w,extra+sum((T>>b)&1 for b in z))for T,w in counts.items()if T>>a&1),F())
def W(z):return sum(w for T,w in counts.items()if any(T>>b&1 for b in z))
def phi(z):
 return sum((w*sum((F(1,t)for t in range(1,1+sum((T>>b)&1 for b in z))),F())for T,w in counts.items()),F())
slacks=[]
for depth in range(m):
 for h in product(range(k),repeat=depth):
  own=finish(h);own_u=u(own[depth],own)
  for a in range(k):
   alt=finish(h+(a,));margin=own_u-u(a,alt);assert margin>=0
   slacks.append(dict(history=list(h),deviation=a,slack=str(margin)))
assert slacks==d['comparison_slacks'] and len(slacks)==399
root=finish(());root_u=u(root[0],root)
menu=[]
for b in range(k):
 z=finish((b,));menu.append(dict(first_action=b,terminal=list(z),owner_payoff=str(u(b,z)),potential=str(phi(z)),welfare=W(z),query_cap_values=[str(u(a,z,1))for a in range(k)]))
assert menu==d['root_menu']
computed=dict(root=list(root),root_u=str(root_u),root_utilities=[str(u(c,root))for c in root],root_welfare=W(root),query_a=2,column_b=4,cap=str(u(2,finish((4,)),1)),cap_minus_root_u=str(u(2,finish((4,)),1)-root_u),potential_a=str(phi(finish((2,)))),potential_b=str(phi(finish((4,)))),maximum_menu_potential=str(max(phi(finish((b,)))for b in range(k))),comparisons_checked=len(slacks),minimum_slack=str(min(F(x['slack'])for x in slacks)))
for key,v in computed.items():assert d[key]==v,(key,d[key],v)
assert u(5,finish((1,)),1)==196>root_u and phi(finish((5,)))-phi(finish((1,)))==-3
assert u(2,finish((4,)),1)-root_u==F(35,2)
assert max(u(a,root,1)for a in range(k))==F(353,2)<root_u
assert source.read_bytes()==raw
report=dict(status='PASS-new-791-definition-check-only',source_sha256=hashlib.sha256(raw).hexdigest(),customers=791,policy_nodes=57,comparisons_including_self=399,comparisons_nonself=342,minimum_slack='0',integer_types=d['integer_types'],actions=d['actions'],comparison_slacks=slacks,root_menu=menu,computed_native_fields=computed,strict_potential_descent=dict(query=5,column=1,query_price='196',root_u=str(root_u),potential_difference_query_column='-3'),good_actual_column=dict(column=0,query_cap='353/2',root_u=str(root_u),slack=str(root_u-F(353,2))),scope='certifies this input / full ordered policy / all 399 IC / all 49 root query prices and stated potential obstructions; no other policy, optimization, 24 rerun or general half result')
output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({key:report[key]for key in ['status','source_sha256','customers','policy_nodes','comparisons_including_self','comparisons_nonself','minimum_slack']},indent=2))
