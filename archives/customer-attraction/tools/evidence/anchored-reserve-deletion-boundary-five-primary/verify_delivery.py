"""Bytes/provenance/full saved-field and policy-table roundtrips only; no original math run."""
from pathlib import Path
import json,hashlib,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-anchored-reserve-deletion-boundary-five-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==5 and [x['size'] for x in rows]==[4434,22223,3997,5412,6304] and sum(x['size'] for x in rows)==42370
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
 p=read(E/'local-progress-at-read'/(x['id']+'.json'));assert p['owner']=='Boss4' and p['disposition']=='in-progress' and p['source_sha256']==x['sha256']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim' and len(claim['ids'])==7 and {x['id'] for x in rows}<=set(claim['ids']) and claim['remote_tip']=='b0151bf906c8a16bc4170b0b9ed2529faa0cdde1' and claim['local_sync']['status']=='needs-attention'
proof=read(E/'independent-sync-preservation.json');assert proof['untracked_count']==3 and len(proof['tracked'])==2 and all(x['same'] for x in proof['tracked']) and proof['missing']==proof['different']==[] and proof['unmerged']=='' and proof['stash_kept'] and proof['stash']=='5e85942e1fc57db44e4ade1a6ac2e431df01541a'
models=read(E/'models-source-manifest.json');runtime=read(E/'runtime-source-manifest.json');assert len(models)==19 and sum(x['size'] for x in models)==30190 and len(runtime)==4 and sum(x['size'] for x in runtime)==25475
for x in models+runtime:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and not x['new_primary'] and not x['new_done']
report=read(S/rows[1]['stage_path']);exact=read(S/rows[3]['stage_path']);assert len(report['summaries'])==19 and report['strict_failures']==[] and len(exact)==26
assert {Path(x['path']).name for x in models}=={x['name'] for x in report['summaries']}
field=read(E/'stored-field-check/stored-matrix-field-check.json');run=read(E/'stored-field-check/field-check-run.json');assert field['status']=='pass' and run['exit_code']==0 and read(E/'stored-field-check/field-check.stdout')==field and run['script_sha256']==sha(E/'stored-field-check/check_anchored_stored_matrices.py')
assert field['primary_sha256_before']==field['primary_sha256_after']=={x['id']:x['sha256'] for x in rows}
assert field['summary_records']==19 and field['reported_cases']==716 and field['unreported_cases']==697 and field['saved_worst_rows_only'] and field['matrix_columns']==44 and field['query_coordinates']==244 and field['all19_saved_bounds_match'] and field['exact_policy_actions']==43
cm=read(E/'formal-comparison.json');assert len(cm)==8;cmp_paths={x['path'] for x in cm}
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
rec=read(W/'semantic-receipts.json');assert len(rec)==5 and {x['id'] for x in rec}=={x['id'] for x in rows}
for x in rec:assert x['disposition']=='retained' and all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all((S/p).is_file() or (R/p).is_file() or p in cmp_paths for p in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==12
lemma=S/'archives/customer-attraction/state/引理/合法前缀共同背景的锚定计数与同叶祖先储备--引理.md';obstruction=S/'archives/customer-attraction/state/障碍/空根后实际删除混合的锚定预算严格失败--障碍.md';program=S/'archives/customer-attraction/state/程序/实际删除锚定预算的双原程序与完整有限记录--程序.md'
l=lemma.read_text();o=obstruction.read_text();t=program.read_text();assert '@@' not in l+o+t
for term in ['tag{ANCHOR}','AD-RESERVE','r=1','平均边际','52客户','同一Q']:
 assert term in l,term
for term in ['20>18','根规定empty不满足根IC','每份混合','未声称','252项','6³=216']:
 assert term in o,term
for term in ['另697','strict_failures仅在gap_lower>0','OPT_k始终写null','精确重新归一化','26顶层字段','0.03963380500499625']:
 assert term in t,term
def ts(s):assert s.startswith('(') and s.endswith(')');return s[1:-1].split(',') if s[1:-1] else []
def ti(s):return list(map(int,ts(s)))
names={x['name'] for x in report['summaries']};decoded={};prices={name:[] for name in names}
for line in t.splitlines():
 if not line.startswith('|'):continue
 a=[x.strip() for x in line.split('|')[1:-1]]
 if a[0] not in names:continue
 name=a[0]
 if len(a)==11:
  _,cases,b,z,C,Wvalue,opt,low,up,glo,gup=a;decoded[name]=dict(name=name,cases=int(cases),worst=dict(prefix=ti(b),terminal=ti(z),coefficient=int(C),W=int(Wvalue),OPT_k=json.loads(opt),lower=low,upper=up,gap_lower=glo,gap_upper=gup))
 elif len(a)==6:
  _,deleted,lam,A,B,rho=a;decoded[name]['worst'].update(deleted=ti(deleted),**{'lambda':ts(lam)},ancestor_reserves=ts(A),actual_ancestor_profit=B,dual_rho=ts(rho))
 elif len(a)==3:prices[name].append((int(a[1]),ts(a[2])))
for name,s in decoded.items():
 assert [a for a,col in prices[name]]==s['worst']['deleted'];s['worst']['query_prices']=[col for a,col in prices[name]]
assert [decoded[x['name']] for x in report['summaries']]==report['summaries']
decoded_exact={};exactkeys=set(exact)
for line in t.splitlines():
 if not line.startswith('|'):continue
 a=[x.strip() for x in line.split('|')[1:-1]]
 if len(a)==2 and a[0] in exactkeys and a[0] not in ['policy','types']:decoded_exact[a[0]]=json.loads(a[1])
labels=exact['topics'];policy=[];types=[];mode=None
for line in o.splitlines():
 if not line.startswith('|'):continue
 a=[x.strip() for x in line.split('|')[1:-1]]
 if a[0]=='兴趣集合':mode='types';continue
 if a[0]=='节点':mode='first';continue
 if a[0]=='已选第一主题；末位历史首项':mode='last';continue
 if a[0].startswith('---'):continue
 if mode=='types' and len(a)==2 and a[0] in ['B','T','AD','AE','BDE','TDE']:types.append(dict(likes=list(a[0]),count=int(a[1])))
 if mode=='first' and len(a)==2 and a[0] in labels+['∅']:policy.append(dict(history=[] if a[0]=='∅' else [a[0]],action=a[1]))
 if mode=='last' and len(a)==7 and a[0] in labels:
  policy.extend(dict(history=[a[0],b],action=v) for b,v in zip(labels,a[1:]))
decoded_exact['policy']=policy;decoded_exact['types']=types;assert decoded_exact==exact
for doc in [lemma,obstruction,program]:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  p=(doc.parent/target).resolve();assert p.is_file() or (p.is_relative_to(S) and ((R/p.relative_to(S)).is_file() or str(p.relative_to(S)) in cmp_paths)),(doc,target)
ex=read(E/'execution-boundaries.json');assert ex['new_stored_matrix_arithmetic_runs']==1
for k in ['original_entry_runs','project_module_imports','SPE_outcomes_replays','IC_replays','game_query_matrix_evaluations','LP_calls','OPT_enumerations']:assert ex[k]==0
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
out=dict(status='pass',scope='bytes/provenance/19 savedworst15keys and44pricecols244coordinates/full26exactfields43policy6types table roundtrip/receipts/links only; storedmatrixrun1 logs reused; no original query/IC/LP',primary_files=5,primary_bytes=42370,retained=5,duplicate=0,new_formal_objects=3,related_models=19,model_bytes=30190,runtime_files=4,runtime_bytes=25475,formal_comparisons=8,relations=12,source_state_updates=[],raw_claim_local_sync='needs-attention',preservation='3untracked+2tracked same/no missing different unmerged/stash kept',reported_cases=716,explicit_worst_rows=19,unreported_cases=697,matrix_columns=44,query_coordinates=244,exact_report_fields=26,exact_policy_actions=43,positive_depth_nodes=42,original_report_positive_depth_comparisons=252,new_stored_matrix_arithmetic_runs=1,original_entry_runs=0,project_module_imports=0,IC_replays=0,game_query_matrix_evaluations=0,SPE_or_LP_or_OPT_replays=0)
(W/'selfcheck-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
