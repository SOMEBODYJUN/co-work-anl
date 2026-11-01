"""Stored-field, domain and provenance verification only; no source import/LP."""
from pathlib import Path
import json,hashlib,itertools,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-root-regret-construction-attempt-four-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==4 and sum(x['size'] for x in rows)==15982
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'];o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==19 and {x['id'] for x in rows}<=set(claim['ids']);assert claim['remote_tip']=='131a993158ac3fccb33fdc3253bfa6541b725bff' and claim['local_sync']['status']=='needs-attention'
p=read(E/'claim-sync-preservation.json');assert p['untracked_count']==1 and p['tracked']==[] and p['missing']==p['different']==[] and not p['unmerged'] and p['stash_kept'] and p['stash']=='c94434efbbbdde7d6b0cf440ee010ebc4760be70'
inputs=read(E/'runtime-input-manifest.json');deps=read(E/'runtime-dependency-manifest.json');assert len(inputs)==2 and sum(x['size'] for x in inputs)==1802 and len(deps)==5
for x in inputs+deps:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
models={Path(x['path']).stem:read(S/x['snapshot']) for x in inputs};assert models['individual_security_failure']['players']==3 and models['residual_counterexample']['players']==2
assert [sum(t['multiplicity'] for t in models[n]['customers']) for n in ['individual_security_failure','residual_counterexample']]==[34,14]
report=read(S/rows[3]['stage_path']);assert list(report)==['scope','records'] and report['scope']=='Three selected finite policy cones only; no finite negative result is mathematical support';assert len(report['records'])==13 and report==read(E/'stored-report-literal-transcription.json')
formal=S/'archives/customer-attraction/state/程序/两储备复制的末位账与三份五人根缺陷原诊断--程序.md';text=formal.read_text();groups=[('individual_security_failure',6,0,1554,975),('individual_security_failure',6,2,1554,975),('residual_counterexample',5,0,780,412)];at=0
for name,p,root,nodes,nrows in groups:
 ports=list(itertools.combinations(range(p),5));block=report['records'][at:at+len(ports)];at+=len(ports)
 for z,P in zip(block,ports):
  assert list(z)==['seed','players','topics','root','portfolio','positive_depth_nodes','exact_constraint_rows','floating_gap','status'];assert (z['seed'],z['players'],z['topics'],z['root'],z['portfolio'],z['positive_depth_nodes'],z['exact_constraint_rows'])==(name,5,p,root,list(P),nodes,nrows);assert nodes==sum(p**d for d in range(5))-1;assert type(z['floating_gap']) is float and z['status']=='finite floating diagnostic; no universal conclusion'
  line='|'+'|'.join(str(z[k]) for k in ['seed','players','topics','root'])+'|`'+json.dumps(z['portfolio'],separators=(',',':'))+'`|'+'|'.join(str(z[k]) for k in ['positive_depth_nodes','exact_constraint_rows'])+'|`'+repr(z['floating_gap'])+'`|';assert line in text
assert [max(z['floating_gap'] for z in report['records'][a:b]) for a,b in [(0,6),(6,12),(12,13)]]==[-0.9277414505730438,-0.9521869056184002,-1.0]
assert '-0.9999999999999996' in text
cm=read(E/'formal-comparison.json');assert len(cm)==7
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
receipts=read(W/'semantic-receipts.json');assert len(receipts)==4 and {x['id'] for x in receipts}=={x['id'] for x in rows}
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and x['disposition']=='retained';assert all((S/t).is_file() for t in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
for p in [formal,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(p.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and ((R/q.relative_to(S)).is_file() or str(q.relative_to(S)) in {x['path'] for x in cm})),(p,target)
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result=dict(status='pass',scope='bytes/provenance/all stored report fields/formal tables and domains only',primary_count=4,primary_bytes=15982,models=2,model_bytes=1802,dependency_modules=5,report_records=13,fields_per_record=9,formal_comparisons=7,receipts_retained=4,relations=8,original_entry_runs=0,imports=0,solver_runs=0,LP_runs=0,IC_replays=0,new_generated_policy_tables=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
