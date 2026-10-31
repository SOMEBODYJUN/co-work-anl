"""Validate frozen rows and explicit immutable fixtures; no original program import/execution."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
from math import comb
import ast,hashlib,json,re
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/um-cycle-leaf-and-cardinality-primary');ws=Path('cleanup/workspaces/Boss4/r3-um-cycle-leaf-and-cardinality-primary')
def read(p):return json.loads((stage/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(ev/'manifest.json');by={x['id']:x for x in m['records']};get=lambda name:next(x for x in m['records'] if Path(x['path']).name==name)
assert len(m['records'])==18 and len(m['primary_ids'])==5 and sum(x['primary'] for x in m['records'])==5
assert m['claim_status']=='pushed' and m['actor']=='Boss4' and m['local_sync']=='synced' and m['claim_tip']=='f6e45a9fec80c36de9276aa1d2e1da06e99f3163'
for x in m['records']:
 p=stage/x['evidence_path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
 if p.suffix=='.py':ast.parse(p.read_text())
for p in stage.rglob('*.json'):json.loads(p.read_text())
# Actual primary import graph is standard-library-only, including leafwriters.
for sid in m['primary_ids']:
 tree=ast.parse((stage/by[sid]['evidence_path']).read_text());mods=set()
 for node in ast.walk(tree):
  if isinstance(node,ast.Import):mods.update(z.name for z in node.names)
  if isinstance(node,ast.ImportFrom):mods.add(node.module)
 assert mods<={'fractions','itertools','math','json','collections','hashlib','platform','pathlib','heapq'}
# C2 old exact fields plus a separate direct negative-square certificate, not Bareiss rerun.
c2=read(get('c2_unit_multislice_gap_audit.json')['evidence_path']);assert c2['files_sha256'][by['366efae229e35047de7f']['path']]==by['366efae229e35047de7f']['sha256']
assert [(x['m'],x['dim'],x['psd'],x['integer_scale']) for x in c2['independent']]==[(2,19,False,16),(3,67,True,243),(4,181,True,6144)]
assert c2['independent'][0]['rank']==4 and c2['independent'][0]['tail_nonzero']==[11,15]
for x in c2['independent'][1:]:
 a=x['m'];n=a+1;assert x['dim']==1+n*a+comb(n,2)*a*a and x['rank']==1+a*(a-1)+a*a*(a-1)*(a-2)//2 and len(x['pivot_signs'])==x['rank'] and x['tail_nonzero'] is None
neg=read(ev/'fixtures/m2-three-monomial-negative-square.json')
def moment_literals(lits):
 d={}
 for j,a in lits:
  if j in d and d[j]!=a:return F(0)
  d[j]=a
 ans=F(1)
 for a in range(2):
  for h in range(sum(z==a for z in d.values())):ans*=F(3,2)-h
 for h in range(len(d)):ans/=3-h
 return ans
monos=neg['zero_based_job_machine_literals'];G=[[moment_literals(a+b) for b in monos] for a in monos];assert G==[list(map(F,row)) for row in neg['gram']];co=neg['coefficients'];assert sum(co[i]*co[j]*G[i][j] for i in range(3) for j in range(3))==F(neg['expected_square'])==F(-1,8)
# Cardinality original code binding and complete finite target table, not closure calls.
card=read(get('bundle_subdivision_audit.json')['evidence_path']);r=card['reports']['cardinality_final.json'];assert card['sha256'][by['14c27eb4d50f284464fa']['path']]==r['source_sha256']==by['14c27eb4d50f284464fa']['sha256']
e=r['exhaustive'];assert e['matrices']==sum(sum((4**a-1)**n for n in range(mx+1)) for a,mx in [(1,3),(2,3),(3,2)])==7689 and e['matrix_targets']==7*7689==53823
assert (e['feasible_schedules_checked'],e['deletions'],e['accepted_infeasible'],e['monotonic_target_checks'])==(115799,7232,0,53823)
assert len(r['two_tree_family'])==22
for x in r['two_tree_family']:
 k=x['k'];theta=2-F(1,k);assert F(x['known_opt'])==theta
 if x['subdivided']:assert x['accepted'] and x['rounds']==x['deletions']==0
 else:assert x['accepted']==(F(x['target'])>=theta)
 if 'binary_search_lower_bound' in x:assert F(x['binary_search_lower_bound'])==(1 if x['subdivided'] else theta)
 assert ('independent_opt' in x)==(k in (2,3))
assert [F(x['lower_bound']) for x in r['boundaries'][:3]]==[0,0,F(43,77)]
assert F(r['boundaries'][3]['lower_bound'])==F(1,10**50+151)+F(3,10**47+53)
# Closedcycle full endpoint descriptions and explicit paths only, no full enumeration/Dijkstra rerun.
cy=read(get('optimal_hull_closed_cycle_audit.json')['evidence_path']);assert cy['sha256'][by['5b9b83fcae1bb3c91099']['path']]==by['5b9b83fcae1bb3c91099']['sha256']
cc=read(ev/'fixtures/three-closed-cycle-original-inputs-and-paths.json');assert len(cc)==3
for z in cc:
 k,d=z['k'],z['d'];scale=z['time_denominator'];P=z['jobs_two_finite_endpoints_in_integer_units'];N=len(P);M=z['machines'];h=z['historical_result'];assert N==(k+1)*d+2*k and M==(k+1)*d+k and scale==4*k*k and h in cy['independent_minimax_path']
 assert all(len(row)==2 and row[0][0]!=row[1][0] and all(0<=a<M and p>0 for a,p in row) for row in P)
 def value(mask):
  L=[0]*M
  for idx,row in enumerate(P):a,p=row[(mask>>idx)&1];L[a]+=p
  return max(L)
 B=value(z['bad_mask']);path=z['explicit_path_masks'];assert path[0]==z['bad_mask'] and all((a^b).bit_count()==1 for a,b in zip(path,path[1:])) and len(path)-1==(k-1)*(d+1)
 assert F(B,scale)==F(h['B'])==2-F(3,k)+F(3,2*k*k) and max(map(value,path))==B+4 and value(path[-1])==scale
 assert h['all_states']==1<<N and F(h['escape_minimum_peak'])==F(B+4,scale) and F(h['peak_increase'])==F(1,k*k)
assert sum(x['all_states'] for x in cy['independent_minimax_path'])==25600 and sum(x['settled_minimax_states'] for x in cy['independent_minimax_path'])==57
# Leaf all input coordinates and complete old q/flow/matching tables.
points=read(ev/'fixtures/three-hardcoded-leaf-input-points.json');mc=read(get('conditional_leaf_consistent_marginals_independent.json')['evidence_path']);weak=read(get('conditional_leaf_hall_path_projection_independent.json')['evidence_path']);replay=read(get('conditional_leaf_hall_root_replay_scope.json')['evidence_path'])
for sid in ['4a1b8fc533696fbb6811','b99a62dba759d15bdc1e']:
 a=next(x for x in replay['audits'] if x['code']==by[sid]['path']);assert a['code_sha256']==by[sid]['sha256'];f=next(x for x in m['records'] if x['path']==a['frozen_output']);assert f['sha256']==a['output_sha256']
def point_parts(p):
 core={c:{s:{u:F(v) for u,v in row.items()} for s,row in states.items()} for c,states in p['core'].items()};lam={(c,s):F(v) for c,s,v in p['lambda']};z={(c,s,u):F(v) for c,s,u,v in p['z']};groups=list(core);blocks={}
 for c,states in core.items():
  assert sum(lam[c,s] for s in states)==1
  for s,row in states.items():assert sum(row.values())==1 and all(v>=0 for v in row.values()) and all(0<=z.get((c,s,u),F(0))<=lam[c,s] for u in row) and sum(v*z.get((c,s,u),F(0)) for u,v in row.items())>=F(p['epsilon'])*lam[c,s]
 for u in p['old_resources']:
  neighbors=[c for c in groups if any(row.get(u,F(0))>0 for row in core[c].values())];beta=[sum(z.get((c,s,u),F(0)) for s in core[c]) for c in neighbors];assert sum(beta)<=1;pi=list(beta)
  if pi:pi[-1]+=1-sum(pi)
  blocks[u]=(neighbors,beta,pi)
 return core,lam,z,blocks
flow_entries=matching_pieces=0
for p,out in zip(points,mc['fixtures']):
 assert p['tag']==out['tag'];core,lam,z,blocks=point_parts(p);allports=[];leafends={};qexpected={};glob={};cond={};beta_count=0
 for u,(neighbors,beta,pi) in blocks.items():
  d=len(neighbors);ports=[f'{u}:port:{a}' for a in range(d)];allports+=ports or [f'{u}:unused']
  for i in range(d-1):
   ell=f'{u}:leaf:{i}';leafends[ell]=[ports[i],ports[i+1]];glob[ell,ports[i]]=sum(pi[i+1:]);glob[ell,ports[i+1]]=sum(pi[:i+1])
  if not d:continue
  for c,states in core.items():
   own=neighbors.index(c) if c in neighbors else None;b=beta[own] if own is not None else F(0)
   for s in states:
    theta=z.get((c,s,u),F(0));assert own is not None or theta==0
    if b==1:qq=[lam[c,s] if j==own else F(0) for j in range(d)];beta_count+=1
    else:qq=[(theta if j==own else F(0))+(lam[c,s]-theta)*(pi[j]-(b if j==own else 0))/(1-b) for j in range(d)]
    assert all(x>=0 for x in qq) and sum(qq)==lam[c,s]
    for j,v in enumerate(qq):qexpected[c,s,u,j]=v
    for i in range(d-1):
     ell=f'{u}:leaf:{i}';cond[c,s,ell,ports[i]]=sum(qq[i+1:]);cond[c,s,ell,ports[i+1]]=sum(qq[:i+1])
 qactual={(c,s,u,j):F(v) for c,s,u,j,v in out['hole_tables']};gactual={(e,a):F(v) for e,a,v in out['global_leaf_flow']};cactual={(c,s,e,a):F(v) for c,s,e,a,v in out['conditional_leaf_flow']}
 assert len(qactual)==len(out['hole_tables']) and len(gactual)==len(out['global_leaf_flow']) and len(cactual)==len(out['conditional_leaf_flow']);assert (qactual,gactual,cactual)==(qexpected,glob,cond)
 states=sum(map(len,core.values()));leaves=len(leafends);positiveports=sum(len(x[0]) for x in blocks.values());assert out['states']==states and out['resources']==len(allports) and out['leaves']==leaves
 assert (out['MC_rows_checked'],out['conditional_rows_checked'],out['conditional_columns_checked'],out['beta_one_state_cases'])==(len(core)*2*leaves,states*leaves,states*positiveports,beta_count)
 for e,ends in leafends.items():assert sum(glob[e,a] for a in ends)==1
 for c,ss in core.items():
  for e,ends in leafends.items():
   for a in ends:assert sum(cond[c,s,e,a] for s in ss)==glob[e,a]
 for u,(neighbors,beta,pi) in blocks.items():
  for i,cowner in enumerate(neighbors):
   a=f'{u}:port:{i}';assert beta[i]+sum(v for (e,b),v in glob.items() if b==a)<=1
   for c,ss in core.items():
    for s in ss:assert (z.get((c,s,u),F(0)) if c==cowner else F(0))+sum(v for (cc,st,e,b),v in cond.items() if cc==c and st==s and b==a)<=lam[c,s]
 mixture=out['conditional_matching_mixtures'];assert set(mixture)=={f'{c}|{s}' for c,ss in core.items() for s in ss}
 for c,ss in core.items():
  for s in ss:
   pieces=mixture[f'{c}|{s}'];reconstructed=defaultdict(F);assert sum((F(x['weight']) for x in pieces),F(0))==lam[c,s]
   for piece in pieces:
    w=F(piece['weight']);mat=piece['matching'];assert w>0 and set(mat)==set(leafends) and len(set(mat.values()))==leaves
    for e,a in mat.items():assert a in leafends[e];reconstructed[e,a]+=w
   for e,ends in leafends.items():
    for a in ends:assert reconstructed[e,a]==cond[c,s,e,a]
 assert sum(map(len,mixture.values()))==out['integral_matching_pieces'] and max(map(len,mixture.values()),default=0)==out['max_pieces_per_state'];matching_pieces+=out['integral_matching_pieces'];flow_entries+=len(qactual)+len(gactual)+len(cactual)
assert matching_pieces==182 and flow_entries==5324
# Rebuild exact expected ordinary matrices from mathematical input labels, then consume every old job/assignment/load.
for point,matkey,sigkey,loadkey,target in [(points[0],'matrix','assignment','all_machine_loads',F(3,2)),(points[1],'toy_matrix','toy_assignment','toy_all_machine_loads',F(2))]:
 core,lam,z,blocks=point_parts(point);lifted={c:{} for c in core};resources=[];leafends={};glob={};conditional={};liftz={}
 for u,(neighbors,beta,pi) in blocks.items():
  ports=[f'port:{u}:{i}' for i in range(len(neighbors))] or [f'unused:{u}'];resources+=ports
  for c,ss in core.items():
   for s,row in ss.items():
    if u in row:
     pos=neighbors.index(c) if c in neighbors else 0;lifted[c].setdefault(s,{})[ports[pos]]=row[u]
     if row[u]>0:liftz[c,s,ports[pos]]=z[c,s,u]
  for i in range(len(neighbors)-1):
   e=f'leaf:{u}:{i}';leafends[e]=[ports[i],ports[i+1]];lifted[e]={'left':{ports[i]:F(1)},'right':{ports[i+1]:F(1)}};glob[e,ports[i]]=1-sum(beta[:i+1]);glob[e,ports[i+1]]=sum(beta[:i+1])
   for c,ss in core.items():
    omit=neighbors.index(c) if c in neighbors else 0
    for s in ss:conditional[c,s,e,ports[i] if i<omit else ports[i+1]]=lam[c,s]
 expected={};machine_set={f'res:{u}' for u in resources}
 for g,ss in lifted.items():
  expected[f'selector:{g}']={f'root:{g}:{s}':F(1) for s in ss}
  for s,row in ss.items():
   root=f'root:{g}:{s}';machine_set.add(root)
   for u,p in row.items():expected[f'inc:{g}:{s}:{u}']={root:p,f'res:{u}':F(1)}
 actual={j:{a:F(p) for a,p in row.items()} for j,row in weak[matkey].items()};assert actual==expected;sig=weak[sigkey];L={a:F(0) for a in machine_set};assert set(sig)==set(expected)
 for j,a in sig.items():assert a in expected[j];L[a]+=expected[j][a]
 assert L=={a:F(v) for a,v in weak[loadkey].items()} and max(L.values())==target
 if point['tag']=='family_t2':
  assert (len(lifted),len(resources),sum(map(len,lifted.values())),len(machine_set),len(expected),sum(map(len,expected.values())))==(57,64,116,180,201,404)
  assert {(c,s):F(v) for c,s,v in weak['lambda']}==lam and {(c,s,u):F(v) for c,s,u,v in weak['z']}==liftz
  assert {(e,a):F(v) for e,a,v in weak['global_leaf_flow']}==glob and {(c,s,e,a):F(v) for c,s,e,a,v in weak['conditional_leaf_flows']}==conditional
 else:assert len(expected)==18 and len(machine_set)==12 and sum(p==0 for row in actual.values() for p in row.values())==4
# Complete receipts, unchanged old pages and exact suggestions.
for x in read(ev/'related-formal-material.json'):assert sha(repo/x['path'])==x['sha256']
for x in read(ev/'comparison-findings.json')['findings']:assert x['exact_old_clause'] in (stage/x['snapshot']).read_text() and sha(stage/x['snapshot'])==x['old_sha256'] and x['applied'] is False
receipts=read(ws/'semantic-receipts.json');assert len(receipts)==5 and {x['id'] for x in receipts}==set(m['primary_ids'])
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(x[k] for k in ['read_note','comparison_note','decision_note','disposition','targets'])
 for p in x['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
rt=read(ev/'runtime-dependencies-and-run-binding.json');assert rt['new_original_program_runs']==0 and all(x['historical_exit_code'] is None and x['new_stdout'] is False for x in rt['bindings'])
broken=[];docs=list((stage/'archives/unrelated-machines/state').rglob('*.md'))+[stage/ev/'README.md']+list((stage/ws).glob('*.md'))
for p in docs:
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?:|#|source:)',dest):continue
  q=(p.parent/dest.split('#',1)[0]).resolve()
  try:rel=q.relative_to(stage)
  except ValueError:broken.append([str(p.relative_to(stage)),dest]);continue
  if not q.exists() and not (repo/rel).exists():broken.append([str(p.relative_to(stage)),dest])
assert not broken,broken
report={'status':'passed','primary_sources':5,'formal_objects':4,'new_original_program_runs':0,'actual_primary_lines_read':765,'checks':['18 inventory frozen originals/comparisons/runs exactsizes/SHA; allsourcePythonASTonly','next9ag actualpushed/Boss4/assigned5/synced claim exacttipf6e45','C2 exactfinite output identity; m2 direct three-monomial negative square -1/8, noBareiss rerun','cardinality all22familytargets/oldcounts/scaledboundaries checked; noclosure calls','3closedcycle alltwoendpoints and explicit path maxima checked; noDijkstra orfullenumeration rerun','all3MC inputpoints, exact2304+18+24hole table entries/global+conditional flows/182fullmatchingpieces read and checked','v2 complete201+18job matrices/finiteedges/actualsigma/allloads and allfamilyflow entries checked','beta1counter6 and m2rank4 diagnostic fields clarified innewresource; oldpages/snapshots unchanged','5complete receipts and realtargets; allJSON parses and newMarkdown links resolve']}
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');files=sorted({str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}|{str(ws/'copy-files.json')});(stage/ws/'copy-files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n');report['file_count']=len(files);report['file_identities_excluding_self']=[{'path':p,'size':(stage/p).stat().st_size,'sha256':sha(stage/p)} for p in files if p!=str(ws/'validation.json')];(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert set(files)=={str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}
print(json.dumps({'status':'passed','files':len(files),'bytes':sum((stage/p).stat().st_size for p in files),'formal_objects':4,'new_original_program_runs':0},ensure_ascii=False))
