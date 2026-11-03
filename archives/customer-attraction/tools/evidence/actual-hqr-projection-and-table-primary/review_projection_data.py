"""Bind frozen reports to exact inputs and the existing, already proved P7 table.

Standard library only. No discovery module import, LP, max8 search, 144-state
coefficient proof replay, or old source-row feasibility reconstruction.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json,sys
HERE=Path(__file__).resolve().parent
REPO=Path(sys.argv[1]).resolve()
BASE=REPO/'archives/customer-attraction/tools/evidence/weighted-source-contracts-resumed-boss3'
SRC=BASE/'original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def leaves(v,path='$'):
 if isinstance(v,dict):
  for k,w in v.items():yield from leaves(w,path+'.'+k)
 elif isinstance(v,list):
  for i,w in enumerate(v):yield from leaves(w,path+f'[{i}]')
 else:yield {'path':path,'type':type(v).__name__,'value':v,**({'float_hex':v.hex()} if isinstance(v,float) else {})}
def dump(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(p.read_text())
manifest=load(HERE/'source-manifest.json')
for m in manifest:assert sha(HERE/'original'/Path(m['path']).name)==m['sha256']
reports={p.name:load(p) for p in (HERE/'original').glob('*.json')}
all_leaves={n:list(leaves(v)) for n,v in reports.items()};dump('all-json-fields-reviewed.json',all_leaves)
tab=reports['trueH_table_certificate.json'];FT=[[F(v) for v in row] for row in tab['F_table']]
parent_path=REPO/'archives/customer-attraction/tools/evidence/five-root-parent-audits-primary/source-root/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/root/audit_trueH_seven_rows.json'
parent=load(parent_path);assert parent['F']==tab['F_table']
assert len(tab['hidden_state_residuals'])==144
assert {f"{r['p']},{r['d']}:{''.join(map(str,r['hidden']))}":r['residue'] for r in parent['residues']}==tab['hidden_state_residuals']
# Compare saved table to the independent mature report; do not recompute G.
for p in range(3):
 for d in range(6):
  zeros=[list(s) for s in product((0,1),repeat=3) if F(tab['hidden_state_residuals'][f'{p},{d}:{"".join(map(str,s))}'])==0]
  assert zeros==tab['maximizing_states'][f'{p},{d}']
assert tab['source_sha256']==sha(HERE/'original/exact_trueH_projection.json')
assert tab['code_sha256']==sha(HERE/'original/trueH_table_certificate.py')

def atom_check(a):
 assert set(a)-{'bits','max_bits','AB_hist','AE_hist','second_hist','menus_lh','exact_mass','H_bit'}==set()
 assert len(a['bits'])==10 and set(a['bits'])<={'0','1'}
 assert len(a['max_bits'])==5 and set(a['max_bits'])<={'0','1'}
 ds=[]
 for k,n in [('AB_hist',8),('AE_hist',8),('second_hist',16)]:
  h=a[k];assert len(h)==n and all(type(v)==int and v>=0 for v in h) and sum(h)==5
  ds.append(sum(h[n//2:]))
 assert len(set(ds))==1
 d=ds[0];assert len(a['menus_lh'])==3
 for l,h in a['menus_lh']:assert 0<=h<=d and 0<=l-h<=5-d
 assert F(a['exact_mass'])>0
 if 'H_bit' in a:assert a['H_bit'] in [0,1]
 return d

def p7(a,j):
 mb=list(map(int,a['max_bits']));p=sum(mb[:2]);d=atom_check(a)
 u=F(mb[2],sum(mb)) if mb[2] else F(0)
 return 17040*u+1085*mb[0]-F(2679*j,p+3)-FT[p][d]
def key(a):return json.dumps({k:v for k,v in a.items() if k not in ('H_bit','exact_mass')},sort_keys=True)
weights_current={'trueH:source-IC':F(426,1289),'trueH:weighted-cap:f1':F(225,1289),'trueH:weighted-cap:f2':F(252,1289),'trueH:R:K:opt':F(15,1289),'trueH:global-size:0':F(217,10312),'trueH:tax:f2:opt':F(9,1289)}
review={};compact=[]
for stem,query in [('payment_v1','z4'),('payment_v2','z4'),('source_last_v1','U'),('fixed_v1',None)]:
 name=f'exact_current_trueH_projection_{stem}.json';r=reports[name]
 sp=SRC/f'exact_current_source_{stem}.json';s=load(sp)
 assert sha(sp)==r['exact_source_sha256']
 assert len(s['atoms'])==r['source_atoms']==s['positive_atoms']
 assert r['new_rows']==747 and r['code_sha256']==sha(HERE/'original/project_current_trueH.py')
 expected=weights_current|({f'trueH:weighted-cap:{query}':F(2679,10312)} if query else {})
 if query:
  assert not r['floating_lift_feasible']
  assert {k:F(v) for k,v in r['exact_nonnegative_row_multipliers'].items()}==expected
  assert len(r['projected_atoms'])==len(s['atoms'])
  total=F(0);rows=[]
  for i,(entry,a) in enumerate(zip(r['projected_atoms'],s['atoms'])):
   assert entry['atom']==a
   j=5*(int(a['max_bits'][4]) if query=='z4' else int(a['bits'][5]))
   value=p7(a,j)/51560;assert value==F(entry['coefficient'])
   assert entry['maximizing_state'] in list(map(list,product((0,1),repeat=3)))
   p=sum(map(int,a['max_bits'][:2]));d=atom_check(a)
   # A stored witness is maximizing by the already proved P7 residual table.
   state=''.join(map(str,entry['maximizing_state']));assert F(tab['hidden_state_residuals'][f'{p},{d}:{state}'])==0
   total+=F(a['exact_mass'])*value
   rows.append({'index':i,'query_membership':j//5,'p':p,'d':d,'exact_mass':a['exact_mass'],'formula_coefficient':str(value),'saved_state':entry['maximizing_state']})
   compact.append(f"{stem}:{i} {a['bits']} {a['max_bits']} AB={a['AB_hist']} AE={a['AE_hist']} S={a['second_hist']} L={a['menus_lh']} mass≈{float(F(a['exact_mass'])):.10g} c={value} arg={state}")
  assert total==F(r['exact_projection_slack'])<0
  assert abs(float(total)-r['negative_slack_float'])<1e-17
  review[name]={'input_file':str(sp.relative_to(REPO)),'input_sha256':sha(sp),'atoms':len(rows),'query':query,'P7_scale':51560,'exact_total':str(total),'rows':rows}
 else:
  assert r['floating_lift_feasible'] and 'projected_atoms' not in r and 'exact_projection_slack' not in r
  for a in s['atoms']:atom_check(a)
  review[name]={'input_file':str(sp.relative_to(REPO)),'input_sha256':sha(sp),'atoms':len(s['atoms']),'saved_float_feasible':True,'exact_lift_masses_present':False}
# Old 64 source rows merge to the 55 report entries, dropping only H_bit.
r=reports['exact_trueH_projection.json'];s=load(SRC/'exact_weighted_source.json');merged={}
for a in s['atoms']:
 atom_check(a);merged[key(a)]=merged.get(key(a),F(0))+F(a['exact_mass'])
assert len(merged)==55==r['source_atoms'] and r['new_states']==8 and r['new_rows']==747
assert r['code_sha256']==sha(SRC/'weighted_true_branch.py')
assert r['source_sha256']==s['source_sha256']
for n,w in r['exact_nonnegative_row_multipliers'].items():assert F(w)>0
old_scale_weights={n:str(F(v)*40844) for n,v in r['exact_nonnegative_row_multipliers'].items()}
assert list(map(int,old_scale_weights.values()))==[17040,9000,10080,600,1085,360,2679]
old_total=F(0);different=[];rows=[]
for i,entry in enumerate(r['projected_atoms']):
 a=entry['atom'];assert F(entry['exact_mass'])==merged[key(a)]
 j=sum(n*t[3] for n,t in zip(a['second_hist'],product((0,1),repeat=4)))
 value=p7(a,j)/40844;assert value==F(entry['coefficient'])
 p=sum(map(int,a['max_bits'][:2]));d=atom_check(a);state=''.join(map(str,entry['maximizing_state']))
 assert F(tab['hidden_state_residuals'][f'{p},{d}:{state}'])==0
 old_total+=F(entry['exact_mass'])*value
 if F(entry['exact_mass'])!=F(a['exact_mass']):different.append(i)
 rows.append({'index':i,'j_mW':j,'outer_mass':entry['exact_mass'],'inner_mass':a['exact_mass'],'coefficient':str(value),'state':state})
 compact.append(f"old55:{i} {a['bits']} {a['max_bits']} H_old={a['H_bit']} AB={a['AB_hist']} AE={a['AE_hist']} S={a['second_hist']} L={a['menus_lh']} mass≈{float(F(entry['exact_mass'])):.10g} c={value} arg={state}")
assert old_total==F(r['exact_projection_slack'])<0
assert 40844*old_total==F(tab['exact_separation_slack_on_frozen_source'])
review['exact_trueH_projection.json']={'source_sha256':r['source_sha256'],'merged_atoms':55,'source_atoms':64,'P7_scale':40844,'integer_weights':old_scale_weights,'exact_total':str(old_total),'outer_inner_mass_differences':different,'rows':rows}
review['table_binding']={'independent_report':str(parent_path.relative_to(REPO)),'sha256':sha(parent_path),'identical_residual_records':144,'recomputed_hidden_scores':0,'table_py_sha256':sha(HERE/'original/trueH_table_certificate.py')}
dump('projection-input-and-P7-binding.json',review)
(HERE/'all-projected-atoms-compact.txt').write_text('\n'.join(compact)+'\n')
dump('validation.json',{'status':'passed','primary_source_count':len(manifest),'json_files':len(reports),'scalar_leaf_count':sum(map(len,all_leaves.values())),'exact_projected_records':206,'current_input_atoms_checked':201,'source_old_atoms_checked':64,'table_records_compared':144,'original_math_entries_run':0,'LP_runs':0,'max8_runs':0,'hidden_144_proof_reruns':0,'old_source_row_reconstructions':0,'checks':['eight frozen hashes','all JSON scalar fields including zero/null/messages and long rational strings','exact current input SHA and complete atom equality','151 new projected coefficients equal the mature P7 repeated-query formula','55 old projected coefficients and merged outer masses equal preserved source data','206 exact mass-weighted coefficients equal four strict negative report totals','stored maximizing states have zero saved mature residual','144 saved residual records equal independent existing report; no coefficient recomputation','fixed50 contains no exact lift certificate']})
print(json.dumps({'status':'passed','source_count':len(manifest),'scalar_leaves':sum(map(len,all_leaves.values())),'projected_records':len(compact),'different_old_masses':different,'separation_totals':{k:v.get('exact_total') for k,v in review.items() if 'exact_total' in v}},ensure_ascii=False,indent=2))
