"""Artifact integrity only. Does not import or execute original probes."""
from pathlib import Path
import json,hashlib,os,re
here=Path(__file__).resolve().parent;stage=here.parents[3];repo=stage.parent.parent/'boss4-research';E=stage/'archives/customer-attraction/tools/evidence/latest-net-and-owner-suffix-audit-primary';out=here/'selfcheck.json';checks=[];links=[]
def rd(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(n,v):checks.append({'check':n,'passed':bool(v)})
ss=rd(E/'source-manifest.json')['rows'];rs=rd(here/'semantic-receipts.json');ct=rd(E/'context-manifest.json')['rows'];cm=rd(E/'comparison-manifest.json');sc=rd(E/'scope.json')
ck('five primary14852B',len(ss)==len(rs)==5 and sum(r['size'] for r in ss)==14852);ck('two duplicate two integrated one retained',sum(r['disposition']=='duplicate' for r in rs)==2 and sum(r['disposition']=='integrated' for r in rs)==2 and sum(r['disposition']=='retained' for r in rs)==1);ck('two complete context31127B',len(ct)==2 and sum(r['size'] for r in ct)==31127);ck('eight canonical full comparisons',len(cm)==sc['canonical_comparisons']==8)
for r in ss+ct+cm:
 b=(stage/r['evidence_path']).read_bytes();ck('size '+r['evidence_path'],len(b)==r['size']);ck('SHA256 '+r['evidence_path'],sha(b)==r['sha256'])
 if 'blob' in r:ck('blob '+r['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'])
ts=rd(here/'target-paths.json');ck('one selfcontained computation',len(ts)==1)
for t in ts:
 p=stage/t;b=p.read_bytes();s=b.decode();ck('actual canonical byte C0 '+t,not any(x<32 and x not in (9,10,13) for x in b));ck('generated whitespace '+t,not any(l.rstrip()!=l for l in s.splitlines()));f=s.split('---',2)[1];meta={k.strip():json.loads(v.strip()) for k,v in (l.split(':',1) for l in f.strip().splitlines())};ck('flat MATEK '+t,all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs']))
 for _,link in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
  if link.startswith(('http:','https:','#')):continue
  rel=Path(os.path.normpath(str(p.parent/link.split('#')[0]))).relative_to(stage);ok=(stage/rel).exists() or (repo/rel).exists();links.append({'source':t,'target':link,'resolved':str(rel),'exists':ok});ck('local link '+link,ok)
 for block in re.findall(r'(?:^\|.*\|\n){2,}',s,re.M):ck('table shape',len({l.count('|') for l in block.strip().splitlines()})==1)
dm=rd(here/'duplicate-coverage-map.json');ck('eight complete duplicate units',len(dm)==2 and sum(len(r['units']) for r in dm)==8 and all(r['all_unique_content_accounted_for'] and all(u['checked'] for u in r['units']) for r in dm));existing=[]
for r in dm:
 b=(repo/r['target']).read_bytes();ck('published duplicate target bytes '+r['id'],len(b)==r['target_size'] and sha(b)==r['target_sha256']);existing.append(r['target'])
for r in rs:
 z=next(x for x in ss if x['id']==r['id']);ck('receipt valid final disposition '+r['id'],r['owner']=='Boss4' and r['disposition'] in ['duplicate','integrated','retained']);ck('receipt source identity '+r['id'],r['source_path']==z['path'] and r['source_size']==z['size'] and r['source_sha256']==z['sha256']);ck('receipt full primary '+r['id'],all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(len(r[k])>35 for k in ['read_note','comparison_note','decision_note']));ck('receipt targets '+r['id'],bool(r['targets']) and set(r['targets'])<=set(ts+existing))
c=rd(here/'claim-evidence.json');a=rd(here/'primary-authorization-check.json');ck('raw13 actual complete claim',len(c['ids'])==13 and c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['ids']==a['raw_complete_ids'] and sha((here/'claim-evidence.json').read_bytes())==a['capture_sha256']);ck('only own5 actual subset',set(a['actual_subset'])=={r['id'] for r in ss} and set(a['actual_subset'])<=set(c['ids']))
for r in a['owners']:
 b=(stage/r['path']).read_bytes();o=json.loads(b);ck('actual owner source '+r['id'],sha(b)==r['sha256'] and o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==r['source_sha256'])
run=E/'replay/latest-NET-original-entry-1';j=rd(run/'actual-invocation.json');ck('exact actual journal copied summary',j==rd(E/'actual-execution-summary.json'));ck('one original entry successful unchanged',j['status']=='finished' and j['returncode']==0 and j['original_program_calls_actual']==sc['original_program_entries']==1 and j['imports_of_original_before_entry']==sc['original_imports_before_entry']==0 and j['source_unchanged'] and j['elapsed_seconds']>0)
code=Path(j['command'][1]);b=code.read_bytes();ck('original executed source3922 exactSHA',len(b)==j['source_size']==3922 and sha(b)==j['source_sha256']=='612764ff50a6da93bd99d2e4f39944ac51c3760e4511b3c7b423a83f6006b0d0');ck('default original entry no args',len(j['command'])==2 and '/original-tree/research/workspaces/customer-attraction/' in str(code));ck('stdoutonly no false original generated file',j['program_writes_report_file'] is False and not code.with_suffix('.json').exists() and 'wrapper' in j['wrapper_capture_role'])
f=next(r for r in ss if r['id']=='c99a51344533415215c9');fb=(stage/f['evidence_path']).read_bytes();so=(run/'stdout.txt').read_bytes();co=Path(j['wrapper_capture_path']).read_bytes();ck('stdout3034 exact frozen bytes and wrappercopy',len(so)==j['stdout_size']==3034 and so==fb==co and sha(so)==j['stdout_sha256']==f['sha256'] and j['frozen_report_byte_equal'] and j['frozen_report_semantic_equal']);ck('stderr empty',j['stderr_size']==0 and (run/'stderr.txt').read_bytes()==b'');ck('claim bound to actual run',j['claim_capture_sha256']==a['capture_sha256'] and j['claim_status']=='pushed' and j['claim_local_sync']=='synced')
d=json.loads(so);ck('one entry internal8 run and3460 pairs',j['original_run_function_calls_from_completed_loop']==sc['internal_original_run_m_calls']==8 and j['actual_run_m_values']==list(range(2,10)) and sum(v['tested_initial_target_pairs'] for v in d['results'])==j['tested_initial_target_pairs_total']==sc['tested_initial_target_pairs']==3460);ck('actual structural13over12 scope',d['results'][-1]['not_an_SPE_counterexample'] is True and d['results'][-1]['witness']['density']==j['witness_density']=='13/12' and d['results'][-1]['tested_initial_target_pairs']==1922)
ck('no other original or optimization entries',all(sc[k]==0 for k in ['related_suffix_LP_entries','LP_solver_runs','new_parameter_search_beyond_original_default','old52_entries','oldchild_entries','old13_entries']))
search=rd(E/'actual-pre-entry-search.json');ck('actual preentry fullSHA search captured',search['performed_before_original_entry'] and search['sufficient_bound_prior_actual_same_SHA_replay_found'] is False and len(search['rows'])==2)
ck('35 mathematical selfreviews',len(re.findall(r'^\d+\. ',(here/'mathematical-self-review.md').read_text(),re.M))==sc['manual_math_checks']==35);rr=rd(here/'relation-review.json');ck('ten explained relations',len(rr)==sc['relations']==10 and all(r['checked'] for r in rr))
nx=rd(here/'next-candidates.json');ck('next actual5 local11561B deliverysnapshot',len(nx)==5 and sum(r['size'] for r in nx)==11561 and all(r['progress_snapshot'] is None for r in nx))
for r in nx:
 b=Path(r['local_path']).read_bytes();ck('next actual local bytes '+r['id'],len(b)==r['size'] and sha(b)==r['sha256'])
bad=[];decoded=[]
for p in sorted(stage.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();r=str(p.relative_to(stage))
 if any(x<32 and x not in (9,10,13) for x in b):bad.append(r)
 if p.suffix=='.json' and p!=out:json.loads(b);decoded.append(r)
ck('all actual text bytes C0 clean',not bad);ck('all JSON decoded',bool(decoded));ck('no shared progress mutation in whitelist',not any(str(p.relative_to(stage)).startswith('cleanup/progress/') for p in stage.rglob('*') if p.is_file()))
result={'status':'pass' if all(x['passed'] for x in checks) else 'fail','scope':'artifact/source/authorization/recorded execution integrity only; no original probe or numerical LP executed by checker','check_count':len(checks),'checks':checks,'local_link_count':len(links),'local_links':links,'unexpected_C0_files':bad,'decoded_JSON_files':decoded};out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');mp=here/'copy-files.json';files=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and p!=mp);files=sorted(files+[str(mp.relative_to(stage))]);mp.write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':result['status'],'check_count':len(checks),'local_link_count':len(links),'file_count':len(files),'total_bytes':sum((stage/p).stat().st_size for p in files),'manifest':str(mp),'manifest_size':mp.stat().st_size,'manifest_sha256':sha(mp.read_bytes())},ensure_ascii=False));assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
