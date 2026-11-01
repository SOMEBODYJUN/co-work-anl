"""Frozen-byte/provenance/semantic-scope checks only; no mathematical replay."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=S/'cleanup/workspaces/Boss4/r3-security-review-scope-projection-rent-four-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows']
assert len(rows)==4 and [x['size'] for x in rows]==[1511,3692,6834,2439] and sum(x['size'] for x in rows)==14476
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
 o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
 assert (E/'normal-show-captures'/Path(x['actual_normal_show_capture']).name).is_file()
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==20 and {x['id'] for x in rows}<=set(claim['ids'])
assert claim['remote_tip']=='5ccaa56066cb6971948dec93190cbe59ac0d8308' and claim['local_sync']['status']=='needs-attention'
p=read(E/'claim-sync-preservation.json');assert p['untracked_count']==3 and len(p['tracked'])==2 and all(x['same'] for x in p['tracked']) and p['missing']==p['different']==[] and not p['unmerged'] and p['stash_kept'] and p['stash']=='a4de73558ff05ccd6f3b672b58294f72b23af5f3'
related=read(E/'related-original-manifest.json');assert len(related)==2 and sum(x['size'] for x in related)==12559
for x in related:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
cm=read(E/'formal-comparison.json');assert len(cm)==8
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
receipts=read(W/'semantic-receipts.json');assert len(receipts)==4 and {x['id'] for x in receipts}=={x['id'] for x in rows}
assert [x['disposition'] for x in receipts]==['duplicate','retained','retained','retained']
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all((S/t).is_file() or (R/t).is_file() for t in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==10
candidate=S/'archives/customer-attraction/state/候选/最优客户投影安全值与完整查询目录的付款候选--候选.md'
resource=S/'archives/customer-attraction/state/资源/最优外客户投影的真实租金门槛与静态覆盖税诊断--资源.md'
c=candidate.read_text();r=resource.read_text()
for term in ['SEC-OPT?','存在同一个O','所有**最优O','没有给出','(P','(m','Gamma','互斥分支','PTQ只覆盖110','两条动态命题真值分离','五人半覆盖证明']:
 if term in ['(P','(m']:continue
 assert term in c,term
for term in ['3(m−1)g','真正完整的孩子SPE','Cartesian','Q−2','W_{\\rm exact}-I=Q','9q','708669/123025','860}{33','2147}{33','31/33','M_H','最优对偶','M_q\\le v_m','原2439B诊断稿']:
 assert term in r,term
assert 'G是实际覆盖客户的折扣和，而非税τ' in r and '反驳该存在命题' in c
for doc in [candidate,resource,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(doc.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and (R/q.relative_to(S)).is_file()),(doc,target)
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
ex=read(E/'execution-boundaries.json')
for key in ['original_entry_runs','original_imports','LP_runs','solver_runs','IC_replays','old_parameter_scans','new_mathematical_program_runs']:assert ex[key]==0
result=dict(status='pass',scope='bytes/provenance/complete semantic accounting/precise mathematical-boundary declarations/links only; no mathematical certification by this verifier',primary_MDs=4,primary_bytes=14476,related_original_MDs=2,related_bytes=12559,formal_comparisons=8,new_formal_objects=2,retained=3,duplicate=1,relations=10,source_state_updates=[],raw_claim_local_sync='needs-attention',preservation_proof='3 untracked + 2 tracked all same; no missing/different/unmerged; stash kept',original_entry_runs=0,original_imports=0,LP_runs=0,solver_runs=0,IC_replays=0,old_parameter_scans=0,new_mathematical_program_runs=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
