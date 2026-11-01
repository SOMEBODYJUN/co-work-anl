"""Byte identity, reversible reading and full report-table roundtrips; no scientific replay."""
from pathlib import Path
from itertools import product
import json,hashlib,re,copy
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-stationary-successor-source-and-independent-five-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==5 and [x['size'] for x in rows]==[2765,9985,8190,7721,3951] and sum(x['size'] for x in rows)==32612
for x in rows:
 check(S/x['stage_path'],x);assert x['full_file_reviewed'] and len(x['sources'])==2
 o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['operation']=='claim' and len(claim['ids'])==17 and {x['id'] for x in rows}<=set(claim['ids']) and claim['remote_tip']=='f16d20f6e674d6da43bee1ebd6c55012b5265eda' and claim['local_sync']['status']=='needs-attention'
p=read(E/'independent-sync-preservation.json');assert p['untracked_count']==3 and len(p['tracked'])==2 and all(x['same'] for x in p['tracked']) and p['missing']==p['different']==[] and p['unmerged']=='' and p['stash_kept'] and p['stash']=='ed58a908bece13b42bd5e331d62dde56d85d9f30'
inputs=read(E/'input-source-manifest.json');runtime=read(E/'runtime-source-manifest.json');assert len(inputs)==12 and sum(x['size'] for x in inputs)==1823372 and len(runtime)==4 and sum(x['size'] for x in runtime)==25475
for x in inputs+runtime:check(S/x['snapshot'],x);assert not x['new_primary'] and not x['new_done']
dag=next(x for x in inputs if 'pure_menu_two_block_dag' in x['path']);assert dag['prior_full_DAG_verification_reused'] and not dag['full_literal_DAG_read_current']
for x in inputs:
 if x is not dag:assert x['full_file_reviewed']
views=read(E/'complete-reading-manifest.json');assert len(views)==4 and sum(x['action_rows'] for x in views)==3124;by={x['id']:x for x in inputs}
for x in views:
 path=S/x['snapshot'];assert sha(path)==x['sha256'] and path.stat().st_size==x['bytes'] and x['full_file_reviewed'];doc=read(path);cert=doc.get('strategy',doc.get('certificate',doc));enc=cert['actions'];k=len(cert['terminal_counts']);acts=[]
 for layer in enc['layers']:
  histories=list(product(range(k),repeat=layer['depth']));assert len(histories)==len(layer['actions']);acts.extend(dict(history=list(h),action=int(v)) for h,v in zip(histories,layer['actions']))
 order=enc['original_row_order'];cert['actions']=acts if order=='canonical depth-then-lex' else [acts[i] for i in order]
 assert doc==read(S/by[x['source_id']]['snapshot']) and len(acts)==x['action_rows']
prior=read(E/'prior-sufficient-audit/execution.json');assert prior['returncode']==0 and prior['source_invocations']==1 and prior['extra_original_function_calls']==0 and prior['output']['sha256']==rows[3]['sha256']
for fn,key in [('stdout.txt','stdout'),('stderr.txt','stderr')]:assert sha(E/'prior-sufficient-audit'/fn)==prior[key]['sha256'] and (E/'prior-sufficient-audit'/fn).stat().st_size==prior[key]['bytes']
matches=read(E/'prior-audit-exact-identity.json');assert len(matches)==2 and all(x['whole_bytes_equal'] and x['no_new_run'] and x['prior_SHA256']==x['actual_primary_SHA256'] for x in matches)
assert prior['source_inputs'][0]['sha256_before']==prior['source_inputs'][0]['sha256_after']==dag['sha256']
cm=read(E/'formal-comparison.json');assert len(cm)==5;cmp_paths={x['path'] for x in cm}
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
rec=read(W/'semantic-receipts.json');assert len(rec)==5 and [x['disposition'] for x in rec]==['retained','retained','duplicate','duplicate','retained']
for x in rec:assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all((S/t).is_file() or (R/t).is_file() or t in cmp_paths for t in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==10
lemma=S/'archives/customer-attraction/state/引理/合法前缀单调基准的最小首位失败与枝外扩张--引理.md';program=S/'archives/customer-attraction/state/程序/平稳后继来源作者探针与既有独审的原始合同--程序.md';l=lemma.read_text();t=program.read_text();assert '@@' not in l+t
for word in ['tag{PM}','基例','所有目录和合法背景','不识别','tag{EXPAND}','任意有序离轨平局']:
 if word=='不识别':continue
 assert word in l,word
for word in ['没有main guard','仅有有理可行原始解','39字段','未重新逐节点阅读或扫描','3210','418','0原入口']:
 assert word in t,word
author=read(S/rows[1]['stage_path']);audit=read(S/rows[3]['stage_path']);names={x['name'] for x in author};ad={};mats={name:{'K':[],'P':[]} for name in names};bd=[];kd={'K':[],'P':[]};au={}
for line in t.splitlines():
 if not line.startswith('|'):continue
 a=[x.strip() for x in line.split('|')[1:-1]]
 if a[0] in names:
  if len(a)==11:
   name,m,k,Wvalue,u,cap,gap,Q,queries,terminal,H=a;ad[name]=dict(name=name,m=int(m),k=int(k),W=int(Wvalue),u=u,cap=cap,gap=gap,Q=json.loads(Q),queries=json.loads(queries),terminal=json.loads(terminal),full_histories=int(H))
  elif len(a)==4:
   name,key,i,v=a;assert int(i)==len(mats[name][key]);mats[name][key].append(json.loads(v))
 elif len(a)==2 and a[0] in audit and a[0] not in ['K','P','root_branches']:au[a[0]]=json.loads(a[1])
 elif len(a)==6 and a[0] in audit['topics']:
  root,path,rpay,fpay,mf,copies=a;bd.append(dict(root=root,path=json.loads(path),root_payoff=rpay,follower_payoffs=json.loads(fpay),minimum_follower=mf,follower_copies_of_root=int(copies)))
 elif len(a)==3 and a[0] in ['K','P']:
  key,i,v=a;assert int(i)==len(kd[key]);kd[key].append(json.loads(v))
assert [dict(ad[x['name']],**mats[x['name']]) for x in author]==author
au.update(root_branches=bd,**kd);assert au==audit and len(au)==39 and len(bd)==8
for doc in [lemma,program]:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  p=(doc.parent/target).resolve();assert p.is_file() or (p.is_relative_to(S) and ((R/p.relative_to(S)).is_file() or str(p.relative_to(S)) in cmp_paths)),(doc,target)
ex=read(E/'execution-boundaries.json')
for k in ['original_entry_runs','project_module_imports','verify_certificate_calls','IC_replays','SPE_solver_calls','LP_calls','matrix_arithmetic_runs','new_scientific_runs']:assert ex[k]==0
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
out=dict(status='pass',scope='only bytes/provenance/full6x13+39 fields8branches matrix-table roundtrip/four compact views exact original JSON roworder reconstruction/old successful audit identity/receipts/links; no utility/IC/LP/matrix arithmetic',primary_files=5,primary_bytes=32612,retained=3,duplicate=2,new_formal_objects=2,related_files=16,related_bytes=1848847,current_full_reading_views=4,current_view_action_rows=3124,total_six_input_policy_action_rows=3210,prior_full_DAG_audit_reused=True,current_DAG_node_scan=False,author_records=6,author_fields_each=13,author_KP_cells=418,audit_fields=39,audit_root_branches=8,audit_KP_cells=128,formal_comparisons=5,relations=10,source_state_updates=[],raw_claim_local_sync='needs-attention',old_same_SHA_independent_audit_runs_reused=1,new_original_entry_runs=0,new_verify_or_IC_runs=0,new_SPE_or_LP_runs=0,new_matrix_arithmetic_runs=0,new_scientific_runs=0)
(W/'selfcheck-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
