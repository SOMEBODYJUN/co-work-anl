"""Byte/provenance/report-literal/semantic accounting only; no probe import."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-occupation-reserve-independent-audit-three-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==3 and [x['size'] for x in rows]==[3317,694,7090] and sum(x['size'] for x in rows)==11101
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
 o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
assert rows[2]['exact_prior_normal_show_reused'] and rows[2]['no_new_normal_show_for_this_source']
run=read(E/'prior-normal-reuse/normal-show-run.json');assert run['exit_code']==0 and run['argv'][1:5]==['work.py','clean','show',rows[2]['id']] and run['cwd']==str(R)
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==15 and {x['id'] for x in rows}<=set(claim['ids'])
assert claim['remote_tip']=='6fe5597b6da6cd52cbac68cb8706ff296dc201f0' and claim['local_sync']['status']=='needs-attention'
p=read(E/'claim-sync-preservation.json');assert p['untracked_count']==3 and len(p['tracked'])==2 and all(x['same'] for x in p['tracked']) and p['missing']==p['different']==[] and not p['unmerged'] and p['stash_kept'] and p['stash']=='2a650aa3d6113342e3e833276bab20840a460d82'
cm=read(E/'formal-comparison.json');assert len(cm)==3;cmp_paths={x['path'] for x in cm}
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
rec=read(W/'semantic-receipts.json');assert len(rec)==3 and {x['id'] for x in rec}=={x['id'] for x in rows} and [x['disposition'] for x in rec]==['retained','retained','duplicate']
for x in rec:assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all((S/t).is_file() or (R/t).is_file() or t in cmp_paths for t in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==6
expected=dict(status='PASS',scope='Finite Fraction checks of exact general formulas and integer-load boundary only; not SPE or half evidence',integer_distribution_cases=4095,minimum_I='0',minimum_strengthened_reserve='0',fractional_I_boundary=dict(I='-1/48',G='7/24',D='1/2',V='1/6',n_qKp='7/48',reserve_after_gap='3/16',grouped_tax='1/4',nonzero_load_square='-1/16'),fractional_strengthening_boundary=dict(I='1/80',G='17/180',D='2/25',V='1/90',n_qKp='17/720',reserve_after_gap='-7/3600',grouped_tax='8/225',nonzero_load_square='-3/80'))
assert read(S/rows[1]['stage_path'])==expected
formal=S/'archives/customer-attraction/state/程序/整数占用储备独审的标量回归合同与完整报告--程序.md';t=formal.read_text()
for term in ['函数n不在参数中','4095','无main guard','三种两点概率','七个顶层键','没有实际构造它们','16值','−7/3600','−1/48','None','没有重新执行旧4095项回归','首次primary','同SHA精确复用']:
 assert term in t,term
for doc in [formal,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(doc.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and ((R/q.relative_to(S)).is_file() or str(q.relative_to(S)) in cmp_paths)),(doc,target)
ex=read(E/'execution-boundaries.json')
for k in ['original_entry_runs','original_imports','evaluate_calls','old4095_regression_replays','SPE_or_IC_runs','LP_runs','solver_runs','new_mathematical_program_runs']:assert ex[k]==0
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result=dict(status='pass',scope='frozen bytes/provenance/all original report literal fields/source accounting/scoped declarations/links only; no original evaluate or mathematical program execution',primary_files=3,primary_bytes=11101,new_normal_sources=2,prior_normal_review_reused=True,original_report_top_level_keys=7,boundary_fields=16,formal_comparisons=3,new_formal_objects=1,retained=2,duplicate=1,relations=6,source_state_updates=[],raw_claim_local_sync='needs-attention',preservation='3u2tracked same/no missing-different-unmerged/stash kept',original_entry_runs=0,original_imports=0,evaluate_calls=0,old4095_regression_replays=0,SPE_or_IC_runs=0,LP_runs=0,solver_runs=0,new_mathematical_program_runs=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
