"""Read-only frozen-source/fixture validation. Never imports/runs primary programs."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import ast,hashlib,json,re
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/capacity-half-slot-and-row-reviews');ws=Path('cleanup/workspaces/Boss4/r3-capacity-half-slot-and-row-reviews')
def read(p):return json.loads((stage/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def c2(n):return n*(n-1)//2
m=read(ev/'manifest.json');by={r['id']:r for r in m['records']}
assert len(m['records'])==18 and sum(r['primary'] for r in m['records'])==4
for r in m['records']:
 p=stage/r['target'];assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
 if p.suffix=='.py':ast.parse(p.read_text())
for p in stage.rglob('*.json'):json.loads(p.read_text())
# Executable primary import chains consist only of the actual listed standard modules.
expected={'698bdcab0669d55a1efa':{'collections','fractions','itertools','json','platform'},'3366609734cf33d87e19':{'fractions','itertools','json'}}
for sid,allowed in expected.items():
 t=ast.parse((stage/by[sid]['target']).read_text());found=set()
 for n in ast.walk(t):
  if isinstance(n,ast.Import):found.update(a.name for a in n.names)
  if isinstance(n,ast.ImportFrom):found.add(n.module)
 assert found==allowed,(sid,found)
# Verify all of the saved original star output's counts by closed-form identities, no build/audit call.
r=read(by['e024705ef6909102d311']['target']);assert r['sha256'][by['698bdcab0669d55a1efa']['path']]==by['698bdcab0669d55a1efa']['sha256']
rows=r['reports']['capacity_pair_reproduced.json']['checks'];assert [x['k'] for x in rows]==list(range(3,13))
for x in rows:
 k=x['k'];M=k*k+3*k-1;N=2*k*k+k;GG=c2(k-1);RR=k*c2(k+1);VR=k*(k+1);VG=k*(k-1);explicit=GG+RR+VR+VG
 assert (x['machines'],x['jobs'],x['supported_configurations'])==(M,N,2*k**3+3*k*k+k)
 assert x['machine_pairs_checked']==c2(M)==x['explicit_compatible_pair_couplings']+x['factorized_product_pairs']
 assert x['explicit_compatible_pair_couplings']==explicit
 assert x['explicit_types']=={'V-G':VG,'V-R':VR,'G-G':GG,'R-R':RR}
 assert x['explicit_joint_entries_checked']==GG*k+RR*2*k+VR*3*k+VG*(2*k-1)
 L=x['supported_configurations'];squares=k*4+(k-1)*k*k+k*(k+1)*4*k*k
 all_cart=(L*L-squares)//2
 assert x['factorized_product_entries_represented']==all_cart-(GG*k*k+RR*4*k*k+VR*4*k+VG*2*k)
 assert x['minimal_overload_star_irreducible'] is True and x['minimum_job_eligibility']==k and F(x['proved_integer_optimum'])==F(2*k-1,k)
# Complete fixed historical parity input/certificate: consume every job, edge, fractional coefficient and sigma entry.
r=read(by['12b601da50cee4eab718']['target']);assert r['source_sha256'][by['3366609734cf33d87e19']['path']]==by['3366609734cf33d87e19']['sha256']
h=r['actual_joint_rounding_certificate'];assert h==read(ev/'fixtures/parity-half-unit-complete-input-and-witness.json')
i=h['input'];assert (len(i['machine_labels']),len(i['job_labels']))==(10,14) and h['machines']==10 and h['jobs']==14
triples=[(0,0,0),(0,1,1),(1,0,1),(1,1,0)];assert not [p for p in combinations(triples,2) if all(len({a[t] for a in p})==2 for t in range(3))]
P=[]
for job,edges in zip(i['job_labels'],i['eligible_times']):
 d={a:F(p) for a,p in edges};assert len(d)==len(edges) and all(0<=a<10 and p in (F(1,2),F(1)) for a,p in d.items());P.append(d)
assert len(P)==14 and sum(map(len,P))==34
X=[]
for j,fr in enumerate(h['fractional_certificate_by_job']):
 d={a:F(w) for a,w in fr};assert len(d)==len(fr) and sum(d.values(),F(0))==1 and all(a in P[j] and w>0 for a,w in d.items());X.append(d)
assert len(X)==14
loads=[sum((P[j].get(a,F(0))*X[j].get(a,F(0)) for j in range(14)),F(0)) for a in range(10)];assert loads==list(map(F,h['fractional_loads']))==[F(1)]*10
mass=[]
for a in range(10):
 times=[P[j][a] for j in range(14) if a in P[j]];gamma=min(times);assert max(times)<=2*gamma
 assert sum((X[j].get(a,F(0)) for j in range(14) if P[j].get(a,F(0))>F(1,2)),F(0))<=1
 assert sum((X[j].get(a,F(0)) for j in range(14) if P[j].get(a,F(0))>F(1,3)),F(0))<=2
 q=sum((d.get(a,F(0)) for d in X),F(0));assert q<=1//gamma;mass.append(q)
assert mass==[F(2),F(2)]+[F(3,2)]*4+[F(1)]*4 and sum(-(-q.numerator//q.denominator) for q in mass)==16
sigma=h['assignment'];assert len(sigma)==14;actual=[F(0)]*10
for j,a in enumerate(sigma):assert a in P[j];actual[a]+=P[j][a]
assert actual==list(map(F,h['st_loads'])) and max(actual)==F(h['OPT'])==F(3,2)
# Final whole/section identities are actual bytes; intermediate whole hashes remain documentary only.
v=read(ev/'version-bindings.json');assert sha(stage/v['half_unit']['old_full_body_evidence'])==r['source_sha256']['research/current/unrelated_machines/joint_slot_prefix_rounding.md']
b=(stage/by['8e7fbfe13b8dcfeb9ec6']['target']).read_bytes();section=b[b.index(b'## 7.'):];assert hashlib.sha256(section).hexdigest()==v['machine_config_review']['section_sha256'];assert (stage/v['machine_config_review']['actual_preserved_frozen_section']).read_bytes()==section
# All review-code identities and finite scope fields remain bound to the actual retained sources.
row=read(by['292abbaeaee297858760']['target']);multi=read(by['99fabfaf306e1766cd1e']['target']);cfg=read(by['fad6c1261ebf89ea2271']['target'])
for sid in ['8b7bf377eea33a7333c6','26338f459180608ece93','698bdcab0669d55a1efa','a1d8cc0d5e532a980090']:assert row['sources'][by[sid]['path']]==by[sid]['sha256']
assert multi['results']['script_sha256']==by['4ac60b67eeb6e0760426']['sha256'] and multi['results']['independent_family_source_sha256']==by['26338f459180608ece93']['sha256']
for sid in ['010e62eecd902e6e97b5','357bed819f77ccb983f1','8b7bf377eea33a7333c6','8e7fbfe13b8dcfeb9ec6']:assert cfg['sources'][by[sid]['path']]==by[sid]['sha256']
assert cfg['reviewed_section_sha256']==hashlib.sha256(section).hexdigest();assert cfg['independent']['scalar']['k_range']==[2,128] and cfg['independent']['scalar']['cases']==127
assert [(x['k'],x['queries']) for x in cfg['independent']['representative']['runs']]==list(zip(range(3,9),[18,27,44,77,142,271]))
assert [x['queries'] for x in cfg['primary']['checks']]==[333,951,2907]
for x in read(ev/'related-formal-material.json'):assert sha(repo/x['path'])==x['sha256']
f=read(ev/'comparison-findings.json');assert f['old_scope_clause'] in (stage/f['snapshot']).read_text() and sha(stage/f['snapshot'])==f['old_sha256']
receipts=read(ws/'semantic-receipts.json');assert len(receipts)==4 and {x['id'] for x in receipts}=={x['id'] for x in m['records'] if x['primary']}
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(x[k] for k in ['read_note','comparison_note','decision_note','disposition','targets'])
 for p in x['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
rt=read(ev/'runtime-dependencies-and-run-binding.json');assert rt['new_original_program_runs']==0 and all(x['historical_exit_code'] is None and not x['new_stdout'] for x in rt['bindings'])
broken=[];docs=list((stage/'archives/unrelated-machines/state').rglob('*.md'))+[stage/ev/'README.md']+list((stage/ws).glob('*.md'))
for p in docs:
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?:|#|source:)',dest):continue
  q=(p.parent/dest.split('#',1)[0]).resolve()
  try:rel=q.relative_to(stage)
  except ValueError:broken.append([str(p.relative_to(stage)),dest]);continue
  if not q.exists() and not (repo/rel).exists():broken.append([str(p.relative_to(stage)),dest])
assert not broken,broken
report={'status':'passed','primary_sources':4,'formal_objects':4,'new_original_program_runs':0,'checks':['18 frozen source/dependency/run files size/SHA exact; source Python AST only','2 primary standard-library import chains exact and adequate same-SHA historical runs reused','all10 historical star output parameter rows verified by size/config/pair/entry closed forms','complete10machine14job34edge half-unit input, fractional coverage/prefix/floor,16slots and actual sigma checked','MP frozen8037section and old8b1whole bytes verified, intermediate whole-body SHA identities documentary only','all related old formal objects unchanged; old scalar/expanded suggestion not applied','4 complete primary receipts with real targets; next5 local unread candidates recorded','all new Markdown links resolve; all JSON parses']}
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
files=sorted({str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}|{str(ws/'copy-files.json')});(stage/ws/'copy-files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
report['file_count']=len(files);report['file_identities_excluding_self']=[{'path':p,'size':(stage/p).stat().st_size,'sha256':sha(stage/p)} for p in files if p!=str(ws/'validation.json')];(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
assert set(files)=={str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}
print(json.dumps({'status':'passed','files':len(files),'bytes':sum((stage/p).stat().st_size for p in files),'new_original_program_runs':0,'formal_objects':4},ensure_ascii=False))
