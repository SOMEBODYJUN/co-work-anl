"""Independent structural/lineage and twelve common-pivot-row audit; no optimizer."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json,hashlib,sys,platform
BASE=Path('/workspace/scratch/12f86aef52bc')
NEW=BASE/'boss8-active/sources/4dec003956d30e008996.json'
OLD=BASE/'co-work-anl-boss8/archives/customer-attraction/tools/evidence/added-six-boss3/original/reopt_added_triple.json'
ROW=BASE/'boss8-active/sources/ee9f74e216313dff242c.py'
OUT=Path(__file__).parent
new=json.loads(NEW.read_text());old=json.loads(OLD.read_text())
ns={};exec(compile(ROW.read_text(),str(ROW),'exec'),ns)
labels='ABCDEUVWXY';paths=('ABCDE','AEUVW','ABEXY')
def fp(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def independent_rows(a):
 b=dict(zip(labels,map(int,a['bits'])))
 d=sum(n*ty[0] for n,ty in zip(a['AB_hist'],product((0,1),repeat=3)))
 t=[1]*d+[0]*(5-d)
 menus=[]
 for ell,h in a['menus_lh']:
  menus.append([1]*h+[0]*(d-h)+[1]*(ell-h)+[0]*((5-d)-(ell-h)))
 out={}
 for r,path in enumerate(paths):
  p=sum(b[z] for z in path[:3])
  for s in range(3):
   if r==s:continue
   out[f'common-pivot:{r}:diag-menu:{s}']=sum((F(menus[r][i]-menus[s][i],p+t[i]+1) for i in range(5)),F())
   out[f'common-pivot:{r}:off-menu:{s}']=sum((F(menus[r][i]-menus[s][j],p+t[i]+1) for i in range(5) for j in range(5) if j!=i),F())
 return out
checks={}
checks['expected_field_order']=list(new)==['scope','status','objective','point','names','atoms','dual_lambda','dual_beta']
checks['lengths']=len(new['atoms'])==len(new['point'])==65 and len(new['names'])==len(new['dual_lambda'])==2408
checks['unique_row_names']=len(set(new['names']))==2408
checks['unchanged_atoms']=new['atoms']==old['atoms']
checks['unchanged_first_2396_names']=new['names'][:2396]==old['names']
checks['point_differs']=new['point']!=old['point']
checks['dual_differs']=new['dual_lambda'][:2396]!=old['dual_lambda']
checks['finite_nonnegative_points_and_lambda']=all(isinstance(z,(int,float)) and F(z)>=0 for k in ('point','dual_lambda') for z in new[k])
checks['all_atom_local_domains']=True
for a in new['atoms']:
 assert len(a['bits'])==10 and set(a['bits'])<={'0','1'}
 ds=[]
 for tag,n in [('AB_hist',3),('AE_hist',3),('second_hist',4)]:
  h=a[tag];assert len(h)==2**n and all(type(v)is int and v>=0 for v in h) and sum(h)==5
  ds.append(sum(v*ty[0] for v,ty in zip(h,product((0,1),repeat=n))))
 assert ds[0]==ds[1]==ds[2]
 d=ds[0];assert len(a['menus_lh'])==3
 for ell,h in a['menus_lh']:assert type(ell)is int and type(h)is int and 0<=h<=d and 0<=ell-h<=5-d
assert all(checks.values())
cols=[independent_rows(a) for a in new['atoms']]
checks['independent_index_expansion_all_coefficients_equal']=all(c==ns['rows'](a) for c,a in zip(cols,new['atoms']))
assert checks['independent_index_expansion_all_coefficients_equal']
newnames=new['names'][2396:];assert newnames==list(cols[0])
def summary(x):
 w=[int(any(map(int,a['bits'][:5]))) for a in x['atoms']]
 o=[int(any(a['AB_hist'][4:])) for a in x['atoms']]
 norm=sum((F(p)*v for p,v in zip(x['point'],w)),F())
 obj=sum((F(p)*v for p,v in zip(x['point'],o)),F())
 return {'scope':x['scope'],'status':x['status'],'objective_stored':x['objective'],'dual_beta_stored':x['dual_beta'],'positive_point_indices_gt_1e-10':[i for i,v in enumerate(x['point']) if v>1e-10],'positive_dual_count_gt_1e-10':sum(v>1e-10 for v in x['dual_lambda']),'normalization_exact_binary_float':str(norm),'normalization_error_float':float(norm-1),'objective_exact_binary_float':str(obj),'objective_recomputed_float':float(obj),'objective_minus_stored_exact_binary_float':str(obj-F(x['objective'])),'new_row_residuals':{n:{'exact_binary_float':str(sum((F(p)*c[n] for p,c in zip(x['point'],cols)),F())),'float':float(sum((F(p)*c[n] for p,c in zip(x['point'],cols)),F()))} for n in newnames}}
report={'event_kind':'new-independent-diagnostic-not-historical-optimizer-replay','python':platform.python_version(),'inputs':[fp(NEW),fp(OLD),fp(ROW)],'checks':checks,'old':summary(old),'new':summary(new),'comparison':{'row_count_old':len(old['names']),'row_count_new':len(new['names']),'added_names':newnames,'atom_key_counts':{str(k):v for k,v in Counter(tuple(a.keys()) for a in new['atoms']).items()},'legacy_mass_numerator_indices':[i for i,a in enumerate(new['atoms']) if 'mass_numerator'in a],'point_max_abs_difference':max(abs(a-b) for a,b in zip(old['point'],new['point'])),'objective_old_minus_new':old['objective']-new['objective'],'old_positive_only':sorted(set(i for i,v in enumerate(old['point']) if v>1e-10)-set(i for i,v in enumerate(new['point']) if v>1e-10)),'new_positive_only':sorted(set(i for i,v in enumerate(new['point']) if v>1e-10)-set(i for i,v in enumerate(old['point']) if v>1e-10)),'new_positive_dual_on_added_rows':{n:v for n,v in zip(new['names'],new['dual_lambda']) if n in newnames and v>1e-10},'independent_coefficient_comparisons':65*12},'limits':['Only frozen binary floats are treated as exact Fractions here; tiny negative residuals do not prove exact infeasibility of an underlying intended rational point.','No LP or full 2408-row reconstruction is executed.','No universal LP bound, exact optimum, actual catalog optimum, or complete ordered-history SPE is certified.','mass_numerator is inherited metadata and is not the new point mass.']}
(OUT/'audit_json_and_pivot.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'checks':checks,'comparison':report['comparison'],'new_residuals':report['new']['new_row_residuals'],'old_residuals':report['old']['new_row_residuals']},ensure_ascii=False,indent=2))
