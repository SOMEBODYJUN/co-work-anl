"""Immutable frozen data validation, not execution/import of original audit modules."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
from math import comb
import ast,hashlib,json,re
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/um-following-audit-primary');ws=Path('cleanup/workspaces/Boss4/r3-um-following-audit-primary')
def read(p):return json.loads((stage/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(ev/'manifest.json');by={x['id']:x for x in m['records']};get=lambda name:next(x for x in m['records'] if Path(x['path']).name==name)
assert len(m['records'])==32 and len(m['primary_ids'])==5 and sum(x['primary'] for x in m['records'])==5
assert m['claim_tip']=='f8aec6ba937b8d78e8c31f77a54296dc03f2df0f' and m['actor']=='Boss4' and m['claim_status']=='pushed'
for x in m['records']:
 p=stage/x['evidence_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
 if p.suffix=='.py':ast.parse(p.read_text())
for p in stage.rglob('*.json'):json.loads(p.read_text())
# All15 old generated outputs match their real old manifest, rootextra stays separate.
tp=ev/'historical-runs/cartesian_menu_reverse_v1';tm=read(tp/'manifest.json');assert tm['audit_code_sha256']==by['d5a14149ab0edb517bc1']['sha256'] and len(tm['files'])==14
for name,digest in tm['files'].items():assert sha(stage/tp/name)==digest
rv=read(tp/'root_original_matrix_verification.json');assert rv['audit_manifest_sha256']==sha(stage/tp/'manifest.json')
total_jobs=total_intersections=0
for t in range(1,5):
 D=1<<t;P=read(tp/f't{t}_sparse_P.json');S=read(tp/f't{t}_all_original_job_schedule.json');I=read(tp/f't{t}_all_complementary_intersections.json');bits=list(product((0,1),repeat=t));resources=set(product(range(4),repeat=t))
 machines={z['id']:z for z in P['machines']};assert len(machines)==2*D*D and set(machines)==set(range(2*D*D))
 rid={tuple(z['u']):a for a,z in machines.items() if z['kind']=='resource'};mid={(tuple(z['g']),tuple(z['ell'])):a for a,z in machines.items() if z['kind']=='private'};assert set(rid)==resources and set(mid)==set(product(bits,bits))
 jobs={z['id']:z for z in P['jobs']};assert len(jobs)==D**3+D and set(jobs)==set(range(len(jobs)))
 supports={k:set() for k in mid};seen_selector=set();seen_inc=set();finite=0
 for j,z in jobs.items():
  g=tuple(z['g']);assert g in bits;rows={a['machine']:a['time_units'] for a in z['finite']};assert len(rows)==len(z['finite']);finite+=len(rows)
  if z['kind']=='selector':assert g not in seen_selector and rows=={mid[g,l]:D for l in bits};seen_selector.add(g)
  else:
   l=tuple(z['ell']);u=tuple(z['u']);assert (g,l,u) not in seen_inc and u in resources and l in bits;seen_inc.add((g,l,u));assert all(((u[i]%2)+g[i]*(u[i]//2))%2==l[i] for i in range(t));assert rows=={mid[g,l]:1,rid[u]:D};supports[g,l].add(u)
 assert seen_selector==set(bits) and len(seen_inc)==D**3 and finite==2*D**3+D*D
 for (g,l),support in supports.items():
  expected={u for u in resources if all(((u[i]%2)+g[i]*(u[i]//2))%2==l[i] for i in range(t))};assert support==expected and len(support)==D
 assert len(P['states'])==D*D
 for z in P['states']:
  key=(tuple(z['g']),tuple(z['ell']));assert z['private_machine']==mid[key] and len(z['resource_machines'])==D and set(z['resource_machines'])=={rid[u] for u in supports[key]}
 loads=[0]*(2*D*D);intervals=[[] for _ in loads];assigned=set();export_counts=Counter();selected={tuple(z['g']):tuple(z['ell']) for z in S['selected_states']};assert selected=={g:g[1:]+g[:1] for g in bits}
 for z in S['assignment']:
  j=z['job'];assert j not in assigned and j in jobs;assigned.add(j);job=jobs[j];rows={a['machine']:a['time_units'] for a in job['finite']};a=z['machine'];assert a in rows and z['time_units']==rows[a];assert z['start_units']>=0 and z['finish_units']-z['start_units']==rows[a];loads[a]+=rows[a];intervals[a].append((z['start_units'],z['finish_units']))
  g=tuple(job['g'])
  if job['kind']=='selector':assert a==mid[g,selected[g]]
  else:
   l=tuple(job['ell']);u=tuple(job['u']);export=l==selected[g] and any(s//2==0 for s in u);assert a==(rid[u] if export else mid[g,l]);export_counts[g]+=int(export)
 assert assigned==set(jobs) and set(export_counts.values())=={D-1}
 for a,row in enumerate(intervals):
  row.sort();assert all(u[1]<=v[0] for u,v in zip(row,row[1:]));assert sum(y-x for x,y in row)==loads[a]
 assert S['machine_load_units']==[{'machine':a,'load_units':v} for a,v in enumerate(loads)] and max(loads)==S['makespan_units']==D+1
 for key,a in mid.items():assert loads[a]==(D+1 if key[1]==selected[key[0]] else D)
 assert Counter(loads[a] for a in rid.values())==Counter({D:D*(D-1),0:D})
 seenpairs=set();assert len(I['certificates'])==I['ordered_pairs_checked']==D**3 and I['unordered_pairs_represented']==D**3//2
 for z in I['certificates']:
  g=tuple(z['g']);h=tuple(z['complement_g']);l=tuple(z['ell']);r=tuple(z['complement_ell']);key=(g,l,r);assert key not in seenpairs and h==tuple(1-a for a in g);seenpairs.add(key);actual=supports[g,l]&supports[h,r];assert actual=={tuple(z['unique_resource'])} and rid[tuple(z['unique_resource'])]==z['resource_machine']
 assert len(seenpairs)==D**3;total_jobs+=len(jobs);total_intersections+=len(seenpairs)
 if t==1:
  opt=read(tp/'t1_full_original_opt_enumeration.json');assert opt['complete_assignments_enumerated']==1024 and opt['exact_OPT_units']==3 and sum(opt['peak_units_histogram'].values())==1024 and min(map(int,opt['peak_units_histogram']))==3
  L=[0]*(2*D*D)
  for z in opt['one_optimal_original_assignment']:
   row={a['machine']:a['time_units'] for a in jobs[z['job']]['finite']};L[z['machine']]+=row[z['machine']]
  assert max(L)==3
assert (total_jobs,total_intersections)==(4710,4680)
# Complete frozenA3input and two actual witnesses, no constructor import.
c=read(get('dual_rail_fullcube_A3_actual_certificate.json')['evidence_path']);assert c['code_sha256']==by['8db8d8577400f86d0b4e']['sha256'];data=c['instance'];A,d,k=map(data.get,['A','d','k']);assert (A,d,k,data['machines'],len(data['jobs']))==(3,5,16,42,165)
for name in ['certificate','A3_hand_certificate']:
 z=c[name];assert len(z['sigma'])==165;L=[F(0)]*42;intern=[0]*5
 for idx,(job,owner) in enumerate(zip(data['jobs'],z['sigma'])):
  if idx<d:expected={2*idx:F(1),2*idx+1:F(1)};assert job['kind']=='selector' and job['variable']==idx
  else:
   mask,v=divmod(idx-d,d);negative=(mask>>v)&1;expected={2*v+negative:F(1,k),2*d+mask:F(1,A)};assert (job['clause_mask'],job['variable'],job['negative'])==(mask,v,negative)
   if negative and owner==2*v+1:intern[v]+=1
  assert {int(a):F(p) for a,p in job['eligible'].items()}==expected and owner in expected;L[owner]+=expected[owner]
 assert L==list(map(F,z['actual_machine_loads'])) and max(L)==F(z['actual_makespan'])==F(9,8) and intern==z['negative_rail_internal_port_counts']
assert c['A3_hand_certificate']['negative_rail_internal_port_counts']==[2,2,1,1,1]
cube=read(get('dual_rail_threshold_soundness_boundary_audit.json')['evidence_path']);r=cube['root_actual_runs']['boss11_dual_rail_cube_cut_actual.json'];assert r['code_sha256']==by['e92ad715a0c9aff7de17']['sha256'] and r['tested_constructor_sha256']==by['8db8d8577400f86d0b4e']['sha256']
assert r['counts']=={'actual_certificates':10,'all_cut_count':6342,'all_physical_breakpoints':352,'original_jobs_checked':11592,'source_no_assignments_checked':680}
for x in r['records']:
 A=x['A'];d=2*A-1;k=1<<(d-1);assert (x['machines'],x['jobs'],x['k'])==(2*d+(1<<d),d+d*(1<<d),k);assert x['all_cut_count']==(d+1)*((1<<d)-1)
 candidates={1+F(h,k) for h in range(k+1)}|{F(B,A) for B in range(A,d+1)};assert len(candidates)==x['all_physical_breakpoints']
 options=[]
 for B in range(A,d+1):
  R=sum(max(s-B,0)*comb(d,s) for s in range(d+1));rr=(R+d-1)//d;options.append(max(F(B,A),1+F(rr,k)))
 assert min(options)==F(x['exact_optimum'])
# Both bounded code hashes and actual import/data dependencies match old-run fields.
b=read(get('bounded_collision_label_floor_audit.json')['evidence_path']);n=b['normative'];ind=b['independent']
for sid in ['122e8b2a473d0aeaf6d8','3cb3475471e5beaf4e40','1d119c87988eadadc643']:assert b['source_sha256'][by[sid]['path']]==by[sid]['sha256']
assert n['example_sha256']==get('pairwise_label_resource_floor.json')['sha256'];assert n['bridge_sha256']==by['1d119c87988eadadc643']['sha256'];assert n['code_sha256']==by['122e8b2a473d0aeaf6d8']['sha256'] and ind['source_sha256']==by['3cb3475471e5beaf4e40']['sha256']
assert n['exhaustive_families']==sum(sum((r*(1<<(r-1)))**q for q in range(1,4)) for r in range(1,5))==35795 and n['coloring_runs']==3*35795
assert n['independent_optimum_families']==1971 and n['independent_oracle_states']==328231 and n['global_group_degree_menus']==2490 and n['global_group_degree_menu_oracle_states']==35565 and n['menu_actual_schedule_checks']==21
assert ind['counts']['exhaustive_full_menu_dags']==15+15**2==240 and ind['counts']['exhaustive_selected_label_certificates']==32+32**2==1056 and ind['counts']['group_degree_approximation_dags']==64+64**2+500+6==4666
assert ind['counts']['actual_resource_parent_assignments']==421839 and ind['counts']['approximation_resource_parent_assignments']==489061
fixtures=read(ev/'fixtures/four-original-bridge-inputs-and-historical-witnesses.json');assert len(fixtures)==4
for z in fixtures:
 p=z['input'];N=p['n'];jobs=z['original_jobs'];sigma=z['historical_sigma'];assert len(jobs)==len(sigma)<=1+len(p['edges'])+N;L=[F(0)]*N
 for job,a in zip(jobs,sigma):row={v:F(p) for v,p in job['finite']};assert a in row;L[a]+=row[a]
 assert L==list(map(F,z['historical_loads'])) and max(L)==F(z['historical_makespan'])
 tree=z['historical_tree'];out=[[] for _ in range(N)];incoming=Counter()
 for u,v in tree:assert [u,v] in p['edges'];out[u].append(v);incoming[v]+=1
 assert all(v==1 for v in incoming.values()) and not incoming[0];reach={0};todo=[0]
 while todo:
  for v in out[todo.pop()]:assert v not in reach;reach.add(v);todo.append(v)
 score=min([F(1)]+[F(len(out[u]),p['demands'][u]) for u in reach if p['demands'][u]]);assert score==F(z['historical_score']) and max(L)<=2-score
# Source semantic receipts, old unchanged mathematical objects, links and manifests.
for x in read(ev/'related-formal-material.json'):assert sha(repo/x['path'])==x['sha256']
receipts=read(ws/'semantic-receipts.json');assert len(receipts)==5 and {x['id'] for x in receipts}==set(m['primary_ids'])
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(x[k] for k in ['read_note','comparison_note','decision_note','disposition','targets'])
 for p in x['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
runtime=read(ev/'runtime-dependencies-and-run-binding.json');assert runtime['new_original_program_runs']==0 and len(runtime['bindings'])==5 and not any(x['new_stdout'] for x in runtime['bindings'])
broken=[];docs=list((stage/'archives/unrelated-machines/state').rglob('*.md'))+[stage/ev/'README.md']+list((stage/ws).glob('*.md'))
for p in docs:
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?:|#|source:)',dest):continue
  q=(p.parent/dest.split('#',1)[0]).resolve()
  try:rel=q.relative_to(stage)
  except ValueError:broken.append([str(p.relative_to(stage)),dest]);continue
  if not q.exists() and not (repo/rel).exists():broken.append([str(p.relative_to(stage)),dest])
assert not broken,broken
report={'status':'passed','primary_sources':5,'formal_objects':3,'new_original_program_runs':0,'actual_primary_lines_read':1497,'checks':['32 frozen sources/dependencies/data/oldoutputs inventorysize/SHAexact; Python ASTonly','unique next15aa f8aec6 pushed Boss4 claim, actual assigned5 IDs','15 generated tensor outputs match14 manifest members plusmanifest; rootextra separatelybound','all4 tensor matrices4710jobs/finiteedges/actualsigma/intervals and4680complementintersections checked','full frozenA3twoedge P165jobs/42machines and2actualsigma/load witnesses checked','all5 oldcube parameter/count rows and exactformula arithmetic checked; nooriginalconstruct/oracle import','bounded bothsource/bridge/fixtureSHA match sufficientoldrun; 4originalP/sigma/treefixtures checked','oldfinite scopes/scalar arithmetic and different oracles/Delta measured accurately','all oldrelatedformal pages unchanged; 5complete receipts, realtargets, validJSON/Markdownlinks']}
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');files=sorted({str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}|{str(ws/'copy-files.json')});(stage/ws/'copy-files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n');report['file_count']=len(files);report['file_identities_excluding_self']=[{'path':p,'size':(stage/p).stat().st_size,'sha256':sha(stage/p)} for p in files if p!=str(ws/'validation.json')];(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert set(files)=={str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}
print(json.dumps({'status':'passed','files':len(files),'bytes':sum((stage/p).stat().st_size for p in files),'formal_objects':3,'new_original_program_runs':0},ensure_ascii=False))
