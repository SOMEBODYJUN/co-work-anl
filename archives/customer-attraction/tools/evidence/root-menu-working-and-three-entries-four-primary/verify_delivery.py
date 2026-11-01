"""Verify only frozen bytes, metadata, semantic accounting and links, no math run."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-root-menu-working-and-three-entries-four-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==4 and [x['size'] for x in rows]==[6052,2216,2888,1187] and sum(x['size'] for x in rows)==12343
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'];o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256'];assert len(x['sources'])==2
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==17 and {x['id'] for x in rows}<=set(claim['ids']);assert claim['remote_tip']=='2a6bcdebc542a336ff2fa72006980bc91b08da39' and claim['local_sync']['status']=='needs-attention'
p=read(E/'claim-sync-preservation.json');assert p['untracked_count']==1 and p['tracked']==[] and p['missing']==p['different']==[] and not p['unmerged'] and p['stash_kept'] and p['stash']=='81aa465d9ad1e82e00250635b7a1368c23d14cc1'
related=read(E/'related-math-manifest.json');assert len(related)==3 and sum(x['size'] for x in related)==14633
for x in related:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
cm=read(E/'formal-comparison.json');assert len(cm)==12
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
receipts=read(W/'semantic-receipts.json');assert len(receipts)==4 and {x['id'] for x in receipts}=={x['id'] for x in rows};assert [x['disposition'] for x in receipts]==['retained','duplicate','retained','duplicate']
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
formal=S/'archives/customer-attraction/state/资源/去当前激励的真实孩子菜单合同与全背景入口勘误--资源.md';text=formal.read_text()
for term in ['同一个Z_(A₀)','(I?)','(F?)','(D)','r1','1/3<|T|/2=1/2','18>17','18≤2U34','t≥3/4','弱合同','后读','20736','4c8d0a06','63binary+3重复e5']:assert term in text,term
assert '2W-OPT_m=2(S-D)+t+\\varepsilon' in text
for p in [formal,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(p.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and ((R/q.relative_to(S)).is_file() or str(q.relative_to(S)) in {x['path'] for x in cm})),(p,target)
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result=dict(status='pass',scope='bytes/provenance/complete semantic accounting/corrective-scope declarations/references only',primary_MDs=4,primary_bytes=12343,related_original_math_MDs=3,related_bytes=14633,formal_comparisons=12,receipts_retained=2,receipts_duplicate=2,relations=8,source_state_updates=[],original_entry_runs=0,imports=0,LP_runs=0,solver_runs=0,IC_replays=0,old_parameter_scans=0,new_math_program_runs=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
