"""Byte/provenance/semantic-boundary checks only; never executes the probe."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-static-random-tax-one-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==1 and rows[0]['id']=='47fd67417431fb978fd9' and rows[0]['size']==1372
x=rows[0];checked(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==10 and x['id'] in claim['ids']
assert claim['remote_tip']=='ef51c6ee061e95d7f7f8d1dfa268ef2dac938873' and claim['local_sync']['status']=='synced'
related=read(E/'related-source-manifest.json');assert len(related)==1 and related[0]['id']=='17182ac367b77ce669e6' and related[0]['size']==1887
x=related[0];checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
o=read(E/'related-owner-at-read'/(x['id']+'.json'));assert o['owner']=='Boss7' and o['source_sha256']==x['sha256']
run=read(E/'related-acquisition/normal-show-run.json');assert run['exit_code']==0 and run['argv'][1:5]==['work.py','clean','show','17182ac367b77ce669e6'] and run['cwd']==str(R)
assert read(E/'related-acquisition/normal-show.json')['source']['sha256']==x['sha256']
cm=read(E/'formal-comparison.json');assert len(cm)==4
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
rec=read(W/'semantic-receipts.json');assert len(rec)==1 and rec[0]['id']==rows[0]['id'] and rec[0]['disposition']=='retained'
assert all(rec[0][k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all((S/t).is_file() or (R/t).is_file() for t in rec[0]['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==6
p=S/'archives/customer-attraction/state/程序/四人六主题终局税随机策略锥的原始探针合同--程序.md';txt=p.read_text()
for term in ['actual manifest恰1row','Σ_M w_M=1','1554','最多100轮','无权','没有要求min(vals)≥0','没有实际输出报告','无main','没有main guard','没有α=3/4缩放','原随机样本','不是W=1','1500','Boss7']:
 if term in ['Σ_M w_M=1','无权','无main']:continue
 assert term in txt,term
assert '\\sum_Mw_M=1' in txt and 'f<−10⁻⁸' in txt and 'TAX?' in txt
for doc in [p,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(doc.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and (R/q.relative_to(S)).is_file()),(doc,target)
ex=read(E/'execution-boundaries.json')
for k in ['original_entry_runs','original_imports','LP_runs','solver_runs','IC_replays','random_scans','new_mathematical_program_runs']:assert ex[k]==0
assert not ex['actual_report_supplied'] and not ex['actual_candidate_supplied'] and ex['Boss7_primary_or_done']==[]
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result=dict(status='pass',scope='frozen bytes/provenance/one-primary semantic accounting/scoped declarations/links only; no SPE or LP certification by this verifier',primary_files=1,primary_bytes=1372,related_files=1,related_bytes=1887,formal_comparisons=4,new_formal_objects=1,retained=1,relations=6,source_state_updates=[],raw_claim_local_sync='synced',original_entry_runs=0,original_imports=0,LP_runs=0,solver_runs=0,IC_replays=0,random_scans=0,new_mathematical_program_runs=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
