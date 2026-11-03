"""Read every field of the five primary JSON files and bind saved coordinates.
No LP, full pricing, old 437/557 audit, or repeated seven-row audit is executed.
"""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import product
from fractions import Fraction as F
import json,hashlib
B=Path(__file__).resolve().parent
PFX='research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/branch_geometry/'
P=B/'original'/PFX
old=json.loads((B/'dependencies/evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
peer=json.loads((B/'dependencies/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/exact_optimum_primal_overlap1.json').read_text())
report={'scope':'all frozen JSON field consumption and coordinate/version binding; no new mathematical optimization audit','files':{}}
def walk(x,c):
 c[type(x).__name__]+=1
 if isinstance(x,dict):
  for k,v in x.items():c['keys']+=1;walk(v,c)
 elif isinstance(x,list):
  for v in x:walk(v,c)
for p in sorted(P.glob('*.json')):
 c=Counter();walk(json.loads(p.read_text()),c);report['files'][p.name]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'field_counts':dict(c)}
def key(a):return (a['bits'],tuple(a['AB_hist']),tuple(a['AE_hist']),tuple(a['second_hist']),tuple(map(tuple,a['menus_lh'])),tuple(a['D2_bits']))
def verify_atom(a):
 assert set(a)=={'bits','AB_hist','AE_hist','second_hist','menus_lh','D2_bits'}
 assert len(a['bits'])==10 and set(a['bits'])<={'0','1'}
 js=[]
 for n,dim in [('AB_hist',3),('AE_hist',3),('second_hist',4)]:
  h=a[n];assert len(h)==1<<dim and sum(h)==5 and all(type(v) is int and v>=0 for v in h)
  js.append(sum(cnt*t[0] for cnt,t in zip(h,product((0,1),repeat=dim))))
 assert len(set(js))==1;j=js[0]
 assert len(a['menus_lh'])==3 and all(len(x)==2 and all(type(v) is int for v in x) and 0<=x[1]<=j and 0<=x[0]-x[1]<=5-j for x in a['menus_lh'])
 assert len(a['D2_bits'])==3 and all(type(v) is int and v in (0,1) for v in a['D2_bits'])
 return j
cg={}
for n,rows in [('cg_second_D.json',564),('cg_second_D_full.json',908)]:
 d=json.loads((P/n).read_text());assert len(d['row_names'])==len(set(d['row_names']))==rows
 assert len(d['atoms'])==len(d['primal_float']) and len(set(map(key,d['atoms'])))==len(d['atoms'])
 js=[verify_atom(a) for a in d['atoms']]
 vals=d['primal_float'];assert all(type(v) in (int,float) and v>=0 for v in vals)
 assert all(k in d['row_names'] and v>=0 for k,v in d['dual_multipliers_float'].items())
 positive=[];zero=[]
 for i,(a,v,j) in enumerate(zip(d['atoms'],vals,js)):
  if v>0:positive.append({'index':i,'mass_float':v,'mass_hex':v.hex(),'actual_covered':int(any(map(int,a['bits'][:5]))),'query_multiplicity':j,'D2_bits':a['D2_bits']})
  else:zero.append(i)
 hist=d['history'];initial=hist[0]['columns']-hist[0]['new_columns']
 for i,h in enumerate(hist):
  assert set(h)=={'iteration','columns','beta','pricing_minimum_scaled','new_columns','contexts','seconds'} and h['iteration']==i
  assert h['columns']==(initial if i==0 else hist[i-1]['columns'])+h['new_columns']
 assert hist[-1]['columns']==len(vals) and hist[-1]['new_columns']==0
 newprefix='D2full:' if rows==908 else 'D2:'
 cg[n]={'scope':d['scope'],'rows':rows,'atoms':len(vals),'initial_columns':initial,'positive_coordinates':positive,'zero_coordinate_indices':zero,'d_distribution_all_atoms':dict(Counter(js)),'d_distribution_positive_atoms':dict(Counter(x['query_multiplicity'] for x in positive)),'positive_uncovered_actual_atoms':sum(x['actual_covered']==0 for x in positive),'mass_sum':sum(vals),'W_from_saved_float':sum(v*int(any(map(int,a['bits'][:5]))) for a,v in zip(d['atoms'],vals)),'O_from_saved_float':sum(v*int(j>0) for v,j in zip(vals,js)),'beta':d['dual_beta_float'],'all_sparse_dual_entries':[{'name':k,'value':v,'hex':v.hex()} for k,v in d['dual_multipliers_float'].items()],'new_row_positive_duals':{k:v for k,v in d['dual_multipliers_float'].items() if k.startswith(newprefix)},'full_iteration_records':hist,'all_row_names':d['row_names'],'true_SPE_or_exact_bound_claim':False}
report['column_generation']=cg
basic=json.loads((P/'cg_second_D.json').read_text());full=json.loads((P/'cg_second_D_full.json').read_text())
report['frozen_prefix_bindings']={'first557_names_identical':basic['row_names'][:557]==full['row_names'][:557],'first437_names_equal_old_frozen_primal':basic['row_names'][:437]==old['rows'],'all1002_basic_atoms_equal_full_prefix':basic['atoms']==full['atoms'][:len(basic['atoms'])]}
assert all(report['frozen_prefix_bindings'].values())
# Exactly bind the old 64 + optional exact 67 seed union and the two anchors.
seed=[];seen=set()
for source in [old['atoms'],peer['atoms']]:
 for a in source:
  z={k:a[k] for k in ['bits','AB_hist','AE_hist','second_hist','menus_lh']}
  for bits in product((0,1),repeat=3):
   v=dict(z,D2_bits=list(bits));k=key(v)
   if k not in seen:seen.add(k);seed.append(v)
union_before_anchors=len(seed)
for j in (0,5):
 h3=[0]*8;h3[3 if j==0 else 7]=5;h4=[0]*16;h4[7 if j==0 else 15]=5
 v={'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'menus_lh':[[5,j]]*3,'D2_bits':[1,1,1]}
 if key(v) not in seen:seen.add(key(v));seed.append(v)
report['seed_binding']={'old_atoms':len(old['atoms']),'optional_exact_atoms':len(peer['atoms']),'extended_union_before_anchors':union_before_anchors,'extended_union_with_anchors':len(seed),'seed_all_values_and_order_match':seed==basic['atoms']}
assert report['seed_binding']['seed_all_values_and_order_match']
third=json.loads((P/'third_D_completion.json').read_text());two=json.loads((P/'two_D_completion.json').read_text())
byatom=defaultdict(float)
for x in third['nonzero_splits']:
 assert set(x)=={'atom','P','Q','ell','h','mass'} and 0<=x['atom']<64 and x['P'] in (0,1) and x['Q'] in (0,1) and x['mass']>0
 at=old['atoms'][x['atom']];j=sum(c*t[0] for c,t in zip(at['AB_hist'],product((0,1),repeat=3)))
 assert (x['ell'],x['h']) in {(0,0),(j,j),(5-j,0),(5,j)}
 byatom[x['atom']]+=x['mass']
report['third_completion']={'all_split_fields_consumed':len(third['nonzero_splits']),'atoms_with_split':len(byatom),'maximum_mass_bookkeeping_error':max(abs(byatom[i]-float(F(int(a['mass_numerator']),int(old['denominator'])))) for i,a in enumerate(old['atoms'])),'all_active_rows':third['active_rows'],'row_count':third['row_count'],'split_variable_count_excludes_epsilon':third['variable_count'],'minimum_maximum_violation_float':third['maximum_violation'],'status':third['status'],'scope':third['scope'],'exact_feasibility_or_SPE_claim':False}
report['two_completion_all_saved_fields']=two
report['separate_D7_reused']={'primary_py_sha256':hashlib.sha256((P/'separate_second_D.py').read_bytes()).hexdigest(),'primary_json_sha256':hashlib.sha256((P/'separate_second_D.json').read_bytes()).hexdigest(),'prior_full_review':'../../direct-coverage-source-resumed-boss3/README.md','fresh_D7_or_peer_runtime':False}
report['new_row_families_908']=dict(Counter('fixed-triple' if n.startswith('D2full:D2:threeprofit:fixed:') else ':'.join(n.split(':')[1:3]) for n in full['row_names'][557:]))
(B/'saved-field-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'frozen_prefix_bindings':report['frozen_prefix_bindings'],'seed_binding':report['seed_binding'],'third_completion':report['third_completion'],'two_completion':two,'column_generation':{n:{k:v for k,v in z.items() if k in ['rows','atoms','initial_columns','d_distribution_all_atoms','d_distribution_positive_atoms','positive_uncovered_actual_atoms','W_from_saved_float','O_from_saved_float','beta','new_row_positive_duals']} for n,z in cg.items()},'new_row_families_908':report['new_row_families_908']},ensure_ascii=False,indent=2))
