"""Identity, immutable fixture and old-record validation. Does not import/run primary audits."""
from pathlib import Path
from fractions import Fraction as F
import ast,hashlib,json,re
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/compact-count-and-configuration-audits');ws=Path('cleanup/workspaces/Boss4/r3-compact-count-and-configuration-audits')
def read(p):return json.loads((stage/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(ev/'manifest.json');entries=m['originals']+m['comparisons'];by={x['id']:x for x in entries}
for r in entries:
 p=stage/r['evidence_path'];assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
 if p.suffix=='.py':ast.parse(p.read_text())
for p in stage.rglob('*.json'):json.loads(p.read_text())
for r in read(ev/'related-formal-material.json'):
 assert sha(repo/r['path'])==r['sha256']
 if r.get('snapshot'):assert sha(stage/r['snapshot'])==r['sha256']
row=read(by['292abbaeaee297858760']['evidence_path']);multi=read(by['99fabfaf306e1766cd1e']['evidence_path']);cfg=read(by['fad6c1261ebf89ea2271']['evidence_path'])
for sid in ['8b7bf377eea33a7333c6','26338f459180608ece93','698bdcab0669d55a1efa','a1d8cc0d5e532a980090']:assert row['sources'][by[sid]['path']]==by[sid]['sha256']
assert row['independent']['script_sha256']==by['26338f459180608ece93']['sha256']
for r in row['main_family']['checks']:
 k=r['k'];assert (r['machines'],r['jobs'])==(2*k**3+6*k*k-2*k+1,4*k**3+2*k*k);assert r['actual_global_forced_edge_optimizer_queries']==(168 if k==2 else 0);assert r['all_machine_pairs']==r['machines']*(r['machines']-1)//2==r['explicit_pairs']+r['factorized_disjoint_support_pairs']
assert len(row['independent']['exact_finite_OPT'])==7
assert multi['results']['script_sha256']==by['4ac60b67eeb6e0760426']['sha256'] and multi['results']['independent_family_source_sha256']==by['26338f459180608ece93']['sha256']
r=multi['results']['exhaustive_k2'];assert (r['all_center_subsets_checked'],r['all_eligible_v_and_all_configurations_checked'],r['job_assignments_checked'],r['z_configurations_per_U'])==(163,50319,2012760,137)
r=multi['results']['structured_boundary'][0];assert (r['structured_configuration_queries'],r['job_assignments_checked'])==(30,3780)
assert [r['exact_necessary_matching_rank'] for r in multi['results']['sharp_necessary_certificates']]==[7,17]
for sid in ['010e62eecd902e6e97b5','357bed819f77ccb983f1','8b7bf377eea33a7333c6','8e7fbfe13b8dcfeb9ec6']:assert cfg['sources'][by[sid]['path']]==by[sid]['sha256']
assert [r['queries'] for r in cfg['primary']['checks']]==[333,951,2907];assert [r['actual_configuration_entries_checked'] for r in cfg['primary']['checks']]==[18450,158727,1060865];assert [r['full_all_machine_configurations'] for r in cfg['primary']['checks']]==[True,False,False]
assert cfg['primary']['invalid_configurations_rejected']==3
assert cfg['independent']['scalar']['k_range']==[2,128] and cfg['independent']['scalar']['cases']==127 and not cfg['independent']['scalar']['full_instance_enumeration'];assert cfg['independent']['exhaustive']['total_configurations']==333
assert [r['k'] for r in cfg['independent']['representative']['runs']]==list(range(3,9));assert [r['queries'] for r in cfg['independent']['representative']['runs']]==[18,27,44,77,142,271]
b=(stage/by['8e7fbfe13b8dcfeb9ec6']['evidence_path']).read_bytes();section=b[b.index(b'## 7.'):];assert hashlib.sha256(section).hexdigest()==cfg['reviewed_section_sha256']=='8037f85bb3b67b6a9f57553d36367388ec4d0e2597a5b348ee5f5828eaf0c2dc'
# Read and validate every element of the immutable actual dense input/certificate.
ip=stage/by['bf52a0bfec064f91dce5']['evidence_path'];i=json.loads(ip.read_text());c=read(by['a1094622581e9201dddf']['evidence_path']);P=[[None if x is None else F(x) for x in row] for row in i['processing_times']];assert (len(P),len(i['jobs']))==(37,40) and all(len(row)==40 for row in P);assert sum(x is not None for row in P for x in row)==168;assert c['input_sha256']==sha(ip)
cover=[F(0)]*40;ct=0
for a,row in enumerate(c['configurations']):
 assert sum(F(z['weight']) for z in row)==1
 for z in row:
  w=F(z['weight']);assert w>=0 and len(z['jobs'])==len(set(z['jobs']));assert all(P[a][j] is not None for j in z['jobs']);assert sum((P[a][j] for j in z['jobs']),F(0))<=1
  for j in z['jobs']:cover[j]+=w
  ct+=1
assert ct==145 and cover==[F(1)]*40
loads=[F(0)]*37;assert len(c['attaining_assignment'])==40
for j,a in enumerate(c['attaining_assignment']):assert P[a][j] is not None;loads[a]+=P[a][j]
assert loads==list(map(F,c['attaining_loads'])) and max(loads)==F(3,2)
f=read(ev/'comparison-findings.json')['finding'];assert f['exact_old_clause'] in (stage/f['existing_formal']['snapshot']).read_text()
receipts=read(ws/'semantic-receipts.json');assert len(receipts)==5 and {x['id'] for x in receipts}=={x['id'] for x in m['originals']}
for r in receipts:
 assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(r[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for p in r['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
r=read(ev/'runtime-dependencies-and-run-binding.json');assert r['new_original_program_runs']==0 and len(r['bindings'])==5 and all(x['historical_exit_code'] is None and not x['new_stdout'] for x in r['bindings'])
broken=[];docs=list((stage/'archives/unrelated-machines/state').rglob('*.md'))+[stage/ev/'README.md']+list((stage/ws).glob('*.md'))
for p in docs:
 for d in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?:|#|source:)',d):continue
  q=(p.parent/d.split('#',1)[0]).resolve()
  try:rel=q.relative_to(stage)
  except ValueError:broken.append([str(p.relative_to(stage)),d]);continue
  if not q.exists() and not (repo/rel).exists():broken.append([str(p.relative_to(stage)),d])
assert not broken,broken
report={'status':'passed','primary_sources':5,'new_formal_objects':3,'new_original_program_runs':0,'checks':['15 immutable inventory originals/comparisons/dependencies/fixtures match sizes and SHA','all JSON parses; all primary and dependency Python AST parses only','5 original program hashes and actual runtime import-chain hashes match old records where recorded','actual compact k2 matrix37x40/168 edges, all145 configuration entries/40job coverage and attaining sigma peak3/2 checked','old finite scopes/counts and sharp necessary Hall ranks checked; no original mains run','current MP section8037 matches frozen full-section identity','scalar127 parameters separated from expanded k2 and k3..8 representative certificate scopes','5 receipts complete and targets real','all new Markdown links resolve; old4 formal pages unchanged and scope suggestion unapplied']}
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');files=sorted({str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}|{str(ws/'copy-files.json')});(stage/ws/'copy-files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n');report['file_count']=len(files);report['file_identities_excluding_self']=[{'path':p,'size':(stage/p).stat().st_size,'sha256':sha(stage/p)} for p in files if p!=str(ws/'validation.json')];(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert set(files)=={str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()};print(json.dumps({'status':'passed','files':len(files),'bytes':sum((stage/p).stat().st_size for p in files),'new_original_program_runs':0,'formal_objects':3},ensure_ascii=False))
