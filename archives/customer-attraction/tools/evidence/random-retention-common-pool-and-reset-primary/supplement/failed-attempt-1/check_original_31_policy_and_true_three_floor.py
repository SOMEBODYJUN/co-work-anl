#!/usr/bin/env python3
"""One informed independent definition-level check of the exact 31-client certificate.
No original/canonical math module imports. No parameter/input scan or new strategy search.
The three-player ordered-tree outcome BI is necessary to certify max-min child floors.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import hashlib,json,sys
inp=Path(sys.argv[1]);outdir=Path(sys.argv[2]);assert not outdir.exists();outdir.mkdir(parents=True)
raw=inp.read_bytes();assert len(raw)==10115 and hashlib.sha256(raw).hexdigest()=='2b8fc76f799bee83b5e8588f94f7c8dfa6f91a634ffe624ede820cc909af541c'
data=json.loads(raw);inst=data['instance'];m=inst['players'];p=len(inst['topics']);assert m==p==4
customers=[]
for a in inst['customers']:
 assert isinstance(a['multiplicity'],int) and a['multiplicity']>=0
 customers += [frozenset(a['topics']) for _ in range(a['multiplicity'])]
assert len(customers)==31
policy={tuple(a['history']):a['action'] for a in data['certificate']['actions']};histories=[h for d in range(m) for h in product(range(p),repeat=d)]
assert len(policy)==len(data['certificate']['actions'])==len(histories)==85 and set(policy)==set(histories) and all(0<=a<p for a in policy.values())
def profit(z,i):
 a=z[i];return sum((F(1,sum(t in c for t in z)) for c in customers if a in c),F(0))
def welfare(z):return sum(any(t in c for t in z) for c in customers)
def follow(h):
 h=tuple(h)
 while len(h)<m:h+= (policy[h],)
 return h
actual=follow(());assert actual==tuple(data['path'])==(1,3,0,0)
ic=[]
for h in histories:
 i=len(h);obey=follow(h);u=profit(obey,i)
 for t in range(p):
  dev=follow(h+(t,));d=profit(dev,i);slack=u-d;assert slack>=0
  ic.append({'history':h,'prescribed':policy[h],'forced':t,'prescribed_leaf':obey,'forced_leaf':dev,'prescribed_profit':str(u),'forced_profit':str(d),'slack':str(slack)})
assert len(ic)==340
actualprofits=[profit(actual,i) for i in range(m)];assert actualprofits==[F(28,3),F(8),F(41,6),F(41,6)] and welfare(actual)==31
# A complete three-player outcome BI with ordered histories; no count quotient.
birecords={}
@lru_cache(None)
def true_three(h):
 if len(h)==3:return frozenset([h])
 i=len(h);child={t:true_three(h+(t,)) for t in range(p)}
 ell={t:min(profit(z,i) for z in leaves) for t,leaves in child.items()};mu=max(ell.values())
 feasible=frozenset(z for t,leaves in child.items() for z in leaves if profit(z,i)>=mu)
 assert feasible
 birecords[h]={'history':h,'ell':{str(t):str(v) for t,v in ell.items()},'mu':str(mu),'argmin':{str(t):min(z for z in child[t] if profit(z,i)==ell[t]) for t in range(p)},'children':{str(t):sorted(child[t]) for t in range(p)},'feasible':sorted(feasible)}
 return feasible
rootleaves=true_three(());assert true_three.cache_info().misses==85 and len(birecords)==21
nodes=[(),(3,),(3,0)];table=[birecords[h] for h in nodes];expected=[[F(12),F(10),F(47,6),F(9)],[F(12),F(10),F(47,6),F(5)],[F(15,2),F(10),F(47,6),F(5)]]
for rec,ex in zip(table,expected):assert [F(rec['ell'][str(t)]) for t in range(p)]==ex
zprime=actual[1:];up=[profit(zprime,i) for i in range(3)];floors=[F(birecords[h]['mu']) for h in nodes];diff=[mu-u for mu,u in zip(floors,up)];positive=[max(F(0),v) for v in diff]
assert up==[F(8),F(15,2),F(15,2)] and floors==[F(12),F(12),F(10)] and diff==positive==[F(4),F(9,2),F(5,2)]
assert sum(positive)==11>actualprofits[0] and sum(positive)-actualprofits[0]==F(5,3) and welfare(zprime)==23
exclusive=sum(actual[0] in c and not any(t in c for t in zprime) for c in customers);refund=sum(up)-sum(actualprofits[1:]);assert exclusive==8 and refund==actualprofits[0]-exclusive==F(4,3)
zreset=(3,0,1);ur=[profit(zreset,i) for i in range(3)];resetfloors=[F(birecords[zreset[:i]]['mu']) for i in range(3)];resetdeficits=[max(F(0),a-b) for a,b in zip(resetfloors,ur)]
assert ur==[F(9),F(12),F(10)] and resetfloors==floors and sum(resetdeficits)==3<=actualprofits[0]
assert zprime not in rootleaves and zreset in rootleaves and set(welfare(z) for z in rootleaves)=={31}
optthree=max(welfare(z) for z in product(range(p),repeat=3));assert optthree==31
summary={'status':'pass','implementation_identity':'informed independent definition-level supplement; not original author CLI, not unread-proof blind','input_sha256':hashlib.sha256(raw).hexdigest(),'input_bytes':len(raw),'expanded_unit_customers':len(customers),'original_players':m,'topics':p,'original_complete_strategy_nodes':85,'original_real_IC_comparisons_including_self':len(ic),'minimum_IC_slack':str(min(F(a['slack']) for a in ic)),'original_actual':actual,'original_profits':[str(v) for v in actualprofits],'original_welfare_and_OPT4':31,'true_three_ordered_states':85,'true_three_decision_nodes':len(birecords),'true_three_forced_children':4*len(birecords),'true_three_SPE_terminal_count':len(rootleaves),'true_three_SPE_welfare_set':[31],'true_three_OPT':optthree,'deleted_target':zprime,'deleted_target_is_SPE_outcome':zprime in rootleaves,'target_profits':[str(v) for v in up],'floors':[str(v) for v in floors],'positive_deficits':[str(v) for v in positive],'sum_deficits':str(sum(positive)),'budget':str(actualprofits[0]),'budget_failure':str(sum(positive)-actualprofits[0]),'deleted_exclusive_clients':exclusive,'actual_refund':str(refund),'BR_reset_target':zreset,'BR_reset_profits':[str(v) for v in ur],'BR_reset_sum_deficits':str(sum(resetdeficits)),'original_entry_calls':0,'canonical_imports_or_solver_calls':0,'own_supplement_entry_calls':1,'new_inputs_or_parameter_scans':0}
for name,obj in [('summary.json',summary),('all-original-340-IC.json',ic),('all-true-three-BI.json',[birecords[h] for h in sorted(birecords,key=lambda h:(len(h),h))])]: (outdir/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
