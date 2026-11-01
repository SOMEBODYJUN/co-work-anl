"""Artifact integrity only. Does not execute or import original programs."""
from pathlib import Path
import json,hashlib,os,re
here=Path(__file__).resolve().parent;stage=here.parents[3];repo=stage.parent.parent/'boss4-research';E=stage/'archives/customer-attraction/tools/evidence/priority-selection-two-implementations-primary';out=here/'selfcheck.json';checks=[];links=[]
def rd(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(n,v):checks.append({'check':n,'passed':bool(v)})
ss=rd(E/'source-manifest.json')['rows'];rs=rd(here/'semantic-receipts.json');cm=rd(E/'comparison-manifest.json');sc=rd(E/'scope.json')
ck('four primary12301B',len(ss)==len(rs)==4 and sum(r['size'] for r in ss)==12301)
ck('two programs and two frozen reports',len([r for r in ss if r['path'].endswith('.py')])==2 and len([r for r in ss if r['path'].endswith('.json')])==2)
ck('eight full canonical comparisons',len(cm)==sc['full_canonical_comparisons']==8)
for r in ss+cm:
 b=(stage/r['evidence_path']).read_bytes();ck('size '+r['evidence_path'],len(b)==r['size']);ck('SHA256 '+r['evidence_path'],sha(b)==r['sha256'])
 if 'blob' in r:ck('blob '+r['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'])
ts=rd(here/'target-paths.json');ck('one computation object',len(ts)==1)
for t in ts:
 p=stage/t;b=p.read_bytes();s=b.decode();ck('actual canonical bytes C0 '+t,not any(x<32 and x not in (9,10,13) for x in b));ck('generated whitespace '+t,not any(l.rstrip()!=l for l in s.splitlines()))
 f=s.split('---',2)[1];meta={k.strip():json.loads(v.strip()) for k,v in (l.split(':',1) for l in f.strip().splitlines())};ck('flat MATEK '+t,all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs']))
 for _,link in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
  if link.startswith(('http:','https:','#')):continue
  rel=Path(os.path.normpath(str(p.parent/link.split('#')[0]))).relative_to(stage);ok=(stage/rel).exists() or (repo/rel).exists();links.append({'source':t,'target':link,'resolved':str(rel),'exists':ok});ck('local link '+link,ok)
 for block in re.findall(r'(?:^\|.*\|\n){2,}',s,re.M):ck('table shape',len({l.count('|') for l in block.strip().splitlines()})==1)
for r in rs:
 z=next(x for x in ss if x['id']==r['id']);ck('receipt final integrated '+r['id'],r['owner']=='Boss4' and r['disposition']=='integrated');ck('receipt identity '+r['id'],r['source_path']==z['path'] and r['source_size']==z['size'] and r['source_sha256']==z['sha256']);ck('receipt full source coverage '+r['id'],all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(len(r[k])>35 for k in ['read_note','comparison_note','decision_note']));ck('receipt target '+r['id'],r['targets']==ts)
c=rd(here/'claim-evidence.json');a=rd(here/'primary-authorization-check.json');ck('raw19 actual whole claim',len(c['ids'])==19 and c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['ids']==a['raw_complete_ids'] and sha((here/'claim-evidence.json').read_bytes())==a['capture_sha256']);ck('own4 subset only',set(a['actual_subset'])=={r['id'] for r in ss} and set(a['actual_subset'])<=set(c['ids']))
for r in a['owners']:
 b=(stage/r['path']).read_bytes();d=json.loads(b);ck('owner snapshot '+r['id'],sha(b)==r['sha256'] and d['owner']=='Boss4' and d['disposition']=='in-progress' and d['source_sha256']==r['source_sha256'])
nm=rd(here/'normal-acquisition-manifest-unmodified.json');mi=rd(here/'initial-local-missing-manifest-unmodified.json');ck('initial four missing plus later normal four preserved',len(mi['missing'])==4 and mi['rows']==[] and len(nm['rows'])==4 and nm['primary_actual_claim_checked'] is False)
for r in nm['rows']:
 p=here/'actual-source-acquisition'/Path(r['actual_normal_show_capture']).name;ck('normal capture unchanged '+r['id'],p.read_bytes()==Path(r['actual_normal_show_capture']).read_bytes())
ex=rd(E/'actual-execution-summary.json');ck('exactly two successful original entries',ex['total_original_entries']==sc['original_program_entries']==2 and len(ex['programs'])==2 and ex['all_success'] and ex['all_outputs_byte_equal_frozen'])
for j in ex['programs']:
 run=E/'replay'/(j['program']+'-original-entry-1');v=rd(run/'actual-invocation.json');ck('raw invocation unchanged '+j['program'],v==j and v['status']=='finished' and v['returncode']==0 and v['original_program_calls_actual']==1 and v['imports_of_original_before_entry']==0 and v['source_unchanged'] and v['elapsed_seconds']>0)
 code=Path(v['command'][1]);b=code.read_bytes();ck('actual source unaltered '+j['program'],len(b)==v['source_size'] and sha(b)==v['source_sha256'] and '/original-tree/research/workspaces/customer-attraction/' in str(code))
 f=next(r for r in ss if r['id']==v['frozen_report_id']);fb=(stage/f['evidence_path']).read_bytes();ob=Path(v['program_output_path']).read_bytes();ck('new output own frozen bytes '+j['program'],ob==fb and len(ob)==v['output_size']==f['size'] and sha(ob)==v['output_sha256']==f['sha256'] and v['frozen_report_byte_equal'] and v['frozen_report_semantic_equal']);ck('stdout equals JSON stderr zero '+j['program'],(run/'stdout.txt').read_bytes()==ob and (run/'stderr.txt').read_bytes()==b'' and v['stderr_size']==0)
 ck('actual original claim binding '+j['program'],v['claim_capture_sha256']==a['capture_sha256'] and v['claim_status']=='pushed' and v['claim_local_sync']=='synced')
ck('no extra mathematical entries',all(sc[k]==0 for k in ['original_program_imports_before_entries','independent_new_math_entries','canonical_entries','LP_solver_runs','new_parameter_searches','old_child_QA_entries','old13_full_entries']))
ck('internal four literal validations each and same17/21 domain',sc['internal_validation_helpers']=={'author_audit_calls':4,'independent_verify_calls':4} and sc['same_original_IC_domain_per_implementation']==17 and sc['winner_mean_scalar_coordinates_per_implementation']==21)
ck('32 manual checks',len(re.findall(r'^\d+\. ',(here/'mathematical-self-review.md').read_text(),re.M))==sc['manual_math_checks']==32);rr=rd(here/'relation-review.json');ck('eight explained relations',len(rr)==sc['relations']==8 and all(r['checked'] for r in rr))
search=rd(E/'actual-pre-entry-search.json');ck('actual preentry exactSHA search captured',search['performed_before_original_entries'] and search['sufficient_bound_prior_actual_same_SHA_replay_found'] is False and len(search['rows'])==4)
nxt=rd(here/'next-candidates.json');ck('next five actual MD14925B delivery snapshot',len(nxt)==5 and sum(r['size'] for r in nxt)==14925 and all(r['progress_snapshot'] is None for r in nxt))
for r in nxt:
 b=Path(r['local_path']).read_bytes();ck('next local actual SHA '+r['id'],len(b)==r['size'] and sha(b)==r['sha256'])
bad=[];decoded=[]
for p in sorted(stage.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();r=str(p.relative_to(stage))
 if any(x<32 and x not in (9,10,13) for x in b):bad.append(r)
 if p.suffix=='.json' and p!=out:json.loads(b);decoded.append(r)
ck('all actual bytes text C0 clean',not bad);ck('all JSON decoded',bool(decoded));ck('no shared progress mutations in whitelist',not any(str(p.relative_to(stage)).startswith('cleanup/progress/') for p in stage.rglob('*') if p.is_file()))
result={'status':'pass' if all(x['passed'] for x in checks) else 'fail','scope':'source/authorization/format/recorded replay integrity only; no original program executed by checker','check_count':len(checks),'checks':checks,'local_link_count':len(links),'local_links':links,'unexpected_C0_files':bad,'decoded_JSON_files':decoded};out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');mp=here/'copy-files.json';files=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and p!=mp);files=sorted(files+[str(mp.relative_to(stage))]);mp.write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':result['status'],'check_count':len(checks),'local_link_count':len(links),'file_count':len(files),'total_bytes':sum((stage/p).stat().st_size for p in files),'manifest':str(mp),'manifest_size':mp.stat().st_size,'manifest_sha256':sha(mp.read_bytes())},ensure_ascii=False));assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
