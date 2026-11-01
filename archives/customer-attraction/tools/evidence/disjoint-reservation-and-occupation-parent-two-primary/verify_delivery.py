"""Only frozen bytes/provenance/semantic accounting/links; no math execution."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-disjoint-reservation-and-occupation-parent-two-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==2 and [x['size'] for x in rows]==[5653,2999] and sum(x['size'] for x in rows)==8652
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
 o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==16 and {x['id'] for x in rows}<=set(claim['ids'])
assert claim['remote_tip']=='740462be0e8b6f0119cc38ed3fe33f59ff20efdd' and claim['local_sync']['status']=='needs-attention'
p=read(E/'claim-sync-preservation.json');assert p['untracked_count']==3 and len(p['tracked'])==2 and all(x['same'] for x in p['tracked']) and p['missing']==p['different']==[] and not p['unmerged'] and p['stash_kept'] and p['stash']=='45e854251187c97c8238d269d7c6e4f70d19a69c'
related=read(E/'related-source-manifest.json');assert len(related)==3 and sum(x['size'] for x in related)==29490
for x in related:
 checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
 d=E/'related-acquisition'/x['id'];run=read(d/'normal-show-run.json');assert run['exit_code']==0 and run['cwd']==str(R) and run['argv'][1:5]==['work.py','clean','show',x['id']]
 assert read(d/'normal-show.json')['source']['sha256']==x['sha256']
cm=read(E/'formal-comparison.json');assert len(cm)==9
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
rec=read(W/'semantic-receipts.json');assert len(rec)==2 and {x['id'] for x in rec}=={x['id'] for x in rows} and all(x['disposition']=='retained' for x in rec)
for x in rec:assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==10
lift=S/'archives/customer-attraction/state/构造/不交保留主题的增人数全历史嵌入--构造.md';occ=S/'archives/customer-attraction/state/引理/整数后继占用储备的全菜单自税分解--引理.md'
t=lift.read_text()
for term in ['每一个旧决策历史','tag{P}','tag{R}','tag{L}','不可返回保留域','知情内部审查','intended proof','14个终端平局差异','647/8772','全部84整数竞争多重集','η=29/3']:
 assert term in t,term
t=occ.read_text()
for term in ['任意完整形式计划','CURRENT-GAP','CURRENT-IC','−1/48','−7/3600','−163/840','69/80','G(p_0)=59/36','全局最大元p*','右方向导数','WD?当前已否定','4095','不需要后继']:
 assert term in t,term
assert '\\mathfrak d(p^*)' in t and 'p_ε=(1−ε)p*+εq*' in t
for doc in [lift,occ,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(doc.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and (R/q.relative_to(S)).is_file()),(doc,target)
ex=read(E/'execution-boundaries.json')
for k in ['original_entry_runs','original_imports','LP_runs','solver_runs','IC_replays','old_scalar_regressions','new_mathematical_program_runs']:assert ex[k]==0
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result=dict(status='pass',scope='bytes/provenance/full-source semantic accounting/scoped declarations and links only; no mathematical replay or certification by this verifier',primary_MDs=2,primary_bytes=8652,related_MDs=3,related_bytes=29490,formal_comparisons=9,new_formal_objects=2,retained=2,relations=10,source_state_updates=[],raw_claim_local_sync='needs-attention',preservation='3untracked2tracked allsame/stashkept/no missing-different-unmerged',original_entry_runs=0,original_imports=0,LP_runs=0,solver_runs=0,IC_replays=0,old_scalar_regressions=0,new_mathematical_program_runs=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
