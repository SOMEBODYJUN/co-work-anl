"""Artifact integrity only. Does not import or execute a mathematical program."""
from pathlib import Path
import json,hashlib,re,os
here=Path(__file__).resolve().parent;stage=here.parents[3];repo=stage.parent.parent/'boss4-research'
E=stage/'archives/customer-attraction/tools/evidence/priority-coupling-and-child-audit-primary'
out=here/'selfcheck.json';checks=[];links=[]
def rd(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(s,v):checks.append({'check':s,'passed':bool(v)})
ss=rd(E/'source-manifest.json')['rows'];rs=rd(here/'semantic-receipts.json');cm=rd(E/'comparison-manifest.json');ct=rd(E/'context-manifest.json')['rows']
ck('five actual primary23186B',len(ss)==len(rs)==5 and sum(x['size'] for x in ss)==23186)
ck('three old full contexts23309B',len(ct)==3 and sum(x['size'] for x in ct)==23309)
ck('eight current formal full comparisons',len(cm)==8)
for r in ss+cm+ct:
 p=stage/r['evidence_path'];b=p.read_bytes()
 ck('size '+str(p.relative_to(stage)),len(b)==r['size']);ck('SHA256 '+str(p.relative_to(stage)),sha(b)==r['sha256'])
 if 'blob' in r:ck('blob '+r['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'])
targets=rd(here/'target-paths.json');ck('three independent objects',len(targets)==3)
for t in targets:
 p=stage/t;b=p.read_bytes();s=b.decode()
 ck('actual canonical bytes C0 '+t,not any(x<32 and x not in (9,10,13) for x in b))
 ck('generated whitespace '+t,not any(x.rstrip()!=x for x in s.splitlines()))
 front=s.split('---',2)[1];meta={k.strip():json.loads(v.strip()) for k,v in (l.split(':',1) for l in front.strip().splitlines())}
 ck('flat MATEK '+t,all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs']))
 for _,link in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
  if link.startswith(('http:','https:','#')):continue
  rel=Path(os.path.normpath(str(p.parent/link.split('#')[0]))).relative_to(stage)
  ok=(stage/rel).exists() or (repo/rel).exists();links.append({'source':t,'target':link,'resolved':str(rel),'exists':ok});ck('local link '+t+' '+link,ok)
 for block in re.findall(r'(?:^\|.*\|\n){2,}',s,re.M):ck('table shape '+t,len({x.count('|') for x in block.strip().splitlines()})==1)
for r in rs:
 z=next(x for x in ss if x['id']==r['id'])
 ck('receipt final integrated '+r['id'],r['disposition']=='integrated' and r['owner']=='Boss4')
 ck('receipt identity '+r['id'],r['source_size']==z['size'] and r['source_sha256']==z['sha256'] and r['source_path']==z['path'])
 ck('receipt true full primary '+r['id'],all(r[x] is True for x in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(len(r[x])>35 for x in ['read_note','comparison_note','decision_note']))
 ck('receipt targets '+r['id'],bool(r['targets']) and set(r['targets'])<=set(targets))
c=rd(here/'claim-evidence.json');a=rd(here/'primary-authorization-check.json')
ck('whole22 raw actual claim preserved',len(c['ids'])==22 and c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and sha((here/'claim-evidence.json').read_bytes())==a['capture_sha256'])
ck('only own actual subset',set(a['actual_subset'])=={x['id'] for x in ss} and set(a['actual_subset'])<=set(c['ids']))
for x in a['owners']:
 b=(stage/x['path']).read_bytes();o=json.loads(b)
 ck('actual owner/source '+x['id'],sha(b)==x['sha256'] and o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['source_sha256'])
lm=rd(here/'initial-local-source-export-manifest.json');nm=rd(here/'normal-acquisition-manifest-unmodified.json')
ck('initial missing2 separate from later actual2',len(lm['rows'])==3 and len(lm['missing'])==2 and len(nm['rows'])==2 and nm['primary_actual_claim_checked'] is False)
for r in nm['rows']:
 p=here/'actual-source-acquisition'/Path(r['actual_normal_show_capture']).name
 ck('unmodified original normal capture '+r['id'],p.read_bytes()==Path(r['actual_normal_show_capture']).read_bytes())
q=E/'replay/child-support-original-run-1';j=rd(q/'actual-invocation.json');scope=rd(E/'scope.json');ps=rd(E/'program-input-and-call-scope.json')
ck('exactly one original entry and no import',j['original_program_calls_actual']==scope['original_program_entries']==1 and j['imports_of_original_program_before_entry']==scope['original_program_imports_before_entry']==0)
ck('original entry success independently recorded',j['status']=='finished' and j['returncode']==0 and j['elapsed_seconds']>0 and j['source_unchanged'] and j['frozen_report_byte_equal'] and j['frozen_report_semantic_equal'])
code=Path(j['command'][1]);b=code.read_bytes()
ck('unaltered actual executed source code4734',len(b)==j['source_code_size']==4734 and sha(b)==j['source_code_sha256']=='b174188da2d7d72153b0499ed07e44c8852386c801c987c798a3d18cd6555a61')
frozen=next(x for x in ss if x['id']=='4b15bb8e3de0852a0cec');b=(stage/frozen['evidence_path']).read_bytes();actual=Path(j['program_output_path']).read_bytes()
ck('output1029 exact frozen bytes and SHA',len(actual)==1029 and actual==b and sha(actual)==j['output_sha256']==frozen['sha256'])
ck('stdout same1029 and stderr empty', (q/'stdout.txt').read_bytes()==actual and (q/'stderr.txt').read_bytes()==b'' and j['stdout_size']==1029 and j['stderr_size']==0)
b=Path(j['input_replay_path']).read_bytes();ck('complete unaltered binary input372216 SHA',len(b)==j['input_size']==372216 and sha(b)==j['input_sha256']=='bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce')
ck('input original source and mirrored copy same',Path(j['input_source']).read_bytes()==b and '/original-tree/research/workspaces/customer-attraction/' in str(code) and j['relocation'].startswith('new isolated prefix'))
v=json.loads(actual);ck('actual finite972/1275 scope',v['status']=='passed' and v['support_checks']==972 and v['single_customer_cut_chains']==1275 and v['old13']['mM_plus_K_minus_2W']=='37/66')
ck('actual old13 inherited explicitly not fullaudit',v['old13']['all_history_SPE_status']=='inherited from existing source audit; not re-audited here' and ps['old13_read_scope']['all_strategy_nodes_or_IC_rechecked'] is False)
ck('no other math entries',all(scope[k]==0 for k in ['old13_full_automaton_entries','independent_mathematical_entries','canonical_entries','LP_solver_runs','new_parameter_searches_or_SPE_scans','priority_diagnostic_program_entries']))
ck('60 manual checks',len(re.findall(r'^\d+\. ',(here/'mathematical-self-review.md').read_text(),re.M))==scope['manual_math_checks']==60)
ck('15 explained relation checks',len(rd(here/'relation-review.json'))==scope['relations']==15 and all(x['checked'] for x in rd(here/'relation-review.json')))
old=rd(E/'reused-old13-manifest.json');ck('old13 sufficient success reuse only',old['same_SHA_prior_full_success_sufficient'] and old['old13_full_automaton_original_entries_this_batch']==0)
for r in old['rows']:
 b=(stage/r['evidence_path']).read_bytes();ck('old evidence size/SHA '+r['repository_path'],len(b)==r['size'] and sha(b)==r['sha256'] and not r['executed_this_batch'])
full=rd(E/'reused-old13/replay-refined-tax.json');su=rd(E/'reused-old13/replay-summary.json');one=rd(E/'reused-old13/replay-alpha-one.json')
ck('prior full27243/112050 PASS binding',su['status']=='passed' and su['original_source_hashes_verified'] and full['status']=='PASS' and full['automaton_nodes']==27243 and full['decision_comparisons']==112050 and one['source_sha256']==j['input_sha256'])
nxt=rd(here/'next-candidates.json');nmiss=rd(here/'next-programs-local-missing-manifest.json')
ck('next4 programs localmissing honestly',len(nmiss['missing'])==4 and nmiss['rows']==[])
ck('two actual readable oldMD candidates',len(nxt)==2 and sum(x['size'] for x in nxt)==10701)
for x in nxt:
 b=Path(x['local_path']).read_bytes();ck('next exact actual local '+x['id'],len(b)==x['size'] and sha(b)==x['sha256'] and x['progress_snapshot'] is None)
bad=[];decoded=[];binary=[]
for p in sorted(stage.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();rel=str(p.relative_to(stage))
 if p.suffix=='.gz':binary.append({'path':rel,'size':len(b),'sha256':sha(b)});continue
 if any(x<32 and x not in (9,10,13) for x in b):bad.append(rel)
 if p.suffix=='.json' and p!=out:json.loads(b);decoded.append(rel)
ck('actual text bytes all files C0 clean',not bad);ck('binary gzip input retained once and hashed',len(binary)==1 and binary[0]['size']==372216 and binary[0]['sha256']==j['input_sha256']);ck('all JSON decode',bool(decoded))
ck('no shared progress files',not any(str(p.relative_to(stage)).startswith('cleanup/progress/') for p in stage.rglob('*') if p.is_file()))
result={'status':'pass' if all(x['passed'] for x in checks) else 'fail','scope':'artifact/source/authorization/link integrity only, no mathematical program executed by this checker','check_count':len(checks),'checks':checks,'local_link_count':len(links),'local_links':links,'decoded_JSON_files':decoded,'unexpected_C0_files':bad,'binary_files_C0_inapplicable_hash_checked':binary}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
mp=here/'copy-files.json';files=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and p!=mp);files=sorted(files+[str(mp.relative_to(stage))]);mp.write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks),'local_link_count':len(links),'file_count':len(files),'total_bytes':sum((stage/p).stat().st_size for p in files),'manifest':str(mp),'manifest_size':mp.stat().st_size,'manifest_sha256':sha(mp.read_bytes())},ensure_ascii=False))
assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
