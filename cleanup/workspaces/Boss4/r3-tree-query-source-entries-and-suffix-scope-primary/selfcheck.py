"""Artifact checks only. No original code imported or executed."""
from pathlib import Path
import json,hashlib,re,os
here=Path(__file__).resolve().parent;stage=here.parents[3];repo=stage.parent.parent/'boss4-research';E=stage/'archives/customer-attraction/tools/evidence/tree-query-source-entries-and-suffix-scope-primary';out=here/'selfcheck.json';checks=[];links=[]
def rd(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(n,v):checks.append({'check':n,'passed':bool(v)})
ss=rd(E/'source-manifest.json')['rows'];rs=rd(here/'semantic-receipts.json');ct=rd(E/'context-manifest.json');cm=rd(E/'comparison-manifest.json');sc=rd(E/'scope.json')
ck('five MD14925B',len(ss)==len(rs)==5 and sum(r['size'] for r in ss)==14925)
ck('two duplicate three integrated',sum(r['disposition']=='duplicate' for r in rs)==2 and sum(r['disposition']=='integrated' for r in rs)==3)
ck('seven full context20560B',len(ct['rows'])==7 and sum(r['size'] for r in ct['rows'])==20560)
ck('thirteen full canonical comparisons',len(cm)==sc['full_canonical_comparisons']==13)
for r in ss+ct['rows']+cm:
 b=(stage/r['evidence_path']).read_bytes();ck('size '+r['evidence_path'],len(b)==r['size']);ck('SHA256 '+r['evidence_path'],sha(b)==r['sha256'])
 if 'blob' in r:ck('blob '+r['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'])
ts=rd(here/'target-paths.json');ck('three new selfcontained objects',len(ts)==3)
for t in ts:
 p=stage/t;b=p.read_bytes();s=b.decode();ck('actual canonical bytes C0 '+t,not any(x<32 and x not in (9,10,13) for x in b));ck('generated whitespace '+t,not any(l.rstrip()!=l for l in s.splitlines()));f=s.split('---',2)[1];meta={k.strip():json.loads(v.strip()) for k,v in (l.split(':',1) for l in f.strip().splitlines())};ck('flat MATEK '+t,all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs']))
 for _,link in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
  if link.startswith(('http:','https:','#')):continue
  rel=Path(os.path.normpath(str(p.parent/link.split('#')[0]))).relative_to(stage);ok=(stage/rel).exists() or (repo/rel).exists();links.append({'source':t,'target':link,'resolved':str(rel),'exists':ok});ck('local link '+link,ok)
 for block in re.findall(r'(?:^\|.*\|\n){2,}',s,re.M):ck('table shape '+t,len({l.count('|') for l in block.strip().splitlines()})==1)
dm=rd(here/'duplicate-coverage-map.json');b=(repo/dm['target']).read_bytes();ck('published duplicate target exact bytes',len(b)==dm['target_size'] and sha(b)==dm['target_sha256'] and dm['target_previously_published']);ck('two complete duplicate maps eight source units',len(dm['sources'])==2 and sum(len(r['units']) for r in dm['sources'])==8 and all(r['all_unique_mathematical_units_covered'] and all(u['checked'] for u in r['units']) for r in dm['sources']))
for r in rs:
 z=next(x for x in ss if x['id']==r['id']);ck('receipt disposition '+r['id'],r['owner']=='Boss4' and r['disposition'] in ['duplicate','integrated']);ck('receipt identity '+r['id'],r['source_path']==z['path'] and r['source_size']==z['size'] and r['source_sha256']==z['sha256']);ck('receipt true fullprimary '+r['id'],all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(len(r[k])>35 for k in ['read_note','comparison_note','decision_note']));ck('receipt target '+r['id'],bool(r['targets']) and set(r['targets'])<=set(ts+[dm['target']]))
 if r['disposition']=='duplicate':ck('duplicate source bound '+r['id'],any(x['id']==r['id'] and x['source_sha256']==r['source_sha256'] for x in dm['sources']))
c=rd(here/'claim-evidence.json');a=rd(here/'primary-authorization-check.json');ck('raw21 actual whole claim',len(c['ids'])==21 and c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and c['ids']==a['raw_complete_ids'] and sha((here/'claim-evidence.json').read_bytes())==a['capture_sha256']);ck('own5 subset only',set(a['actual_subset'])=={r['id'] for r in ss} and set(a['actual_subset'])<=set(c['ids']))
for r in a['owners']:
 b=(stage/r['path']).read_bytes();o=json.loads(b);ck('actual owner/source '+r['id'],sha(b)==r['sha256'] and o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==r['source_sha256'])
ck('all new mathematical entries zero',all(sc[k]==0 for k in ['original_program_entries','independent_mathematical_entries','source_function_calls','canonical_entries','LP_solver_runs','parameter_or_SPE_scans']))
ck('50 manual mathematical checks',len(re.findall(r'^\d+\. ',(here/'mathematical-self-review.md').read_text(),re.M))==sc['manual_math_checks']==50);rr=rd(here/'relation-review.json');ck('14 explained relations',len(rr)==sc['relations']==14 and all(r['checked'] for r in rr))
old=rd(E/'reused-52-success-manifest.json');ck('old52 sufficient success only reused',old['same_SHA_old_success_sufficient'] and old['new_original_entries']==0)
for r in old['rows']:
 b=(stage/r['evidence_path']).read_bytes();ck('reused old evidence sizeSHA '+r['repository_path'],len(b)==r['size'] and sha(b)==r['sha256'] and not r['executed_this_batch'])
p=old['input_existing_retained_reference'];b=(repo/p['repository_path']).read_bytes();ck('old52 actual retained inputSHA',len(b)==p['size']==32574 and sha(b)==p['sha256']=='9e7cf1437a7b03fe89d843d4ae20efa3c6a4137373098ed1220d4370656a5245')
j=rd(E/'reused-52-success/replay/execution.json');d=rd(E/'reused-52-success/replay/origin_retraction_exact_audit.json');case=next(x for x in d['audits'] if x['name']=='unchanged_52_unit_complete_SPE_max_future');ck('prior real successful original record',j['exit_code']==0 and j['generated_bytes_equal_frozen'] and j['source_sha256']=='23fa930019f22e9e12fd99859e37a250485d7ae740e9946b409527c80ccf2c79' and j['generated_sha256']==sha((E/'reused-52-success/replay/origin_retraction_exact_audit.json').read_bytes())=='6488b65a790c2af4bab4f0019a10f6cd4f784d6318fd12517232ba6cfd077cd9');ck('old52 full1554 source input explicit binding',d['status']=='passed' and d['active_fixture_sha256']==p['sha256'] and case['complete_history_IC_checks']==1554 and case['B']==[3,3,2,2] and case['OPT']==52)
mi=rd(here/'historical-peer-replay-local-manifest-unmodified.json');ck('two historical peer files remain missing',len(mi['missing'])==2 and {r['id'] for r in mi['missing']}=={'435fed7a1c1ca486a2aa','e41bc66ebc6b6a23a828'})
nx=rd(here/'next-candidates.json');ck('next five actual local14852B delivery snapshots',len(nx)==5 and sum(r['size'] for r in nx)==14852 and all(r['progress_snapshot'] is None for r in nx))
for r in nx:
 b=Path(r['local_path']).read_bytes();ck('next actual sizeSHA '+r['id'],len(b)==r['size'] and sha(b)==r['sha256'])
bad=[];decoded=[]
for p in sorted(stage.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();r=str(p.relative_to(stage))
 if any(x<32 and x not in (9,10,13) for x in b):bad.append(r)
 if p.suffix=='.json' and p!=out:json.loads(b);decoded.append(r)
ck('all text actual byte C0 clean',not bad);ck('all JSON decoded',bool(decoded));ck('no shared progress file mutation in whitelist',not any(str(p.relative_to(stage)).startswith('cleanup/progress/') for p in stage.rglob('*') if p.is_file()))
result={'status':'pass' if all(x['passed'] for x in checks) else 'fail','scope':'artifact/source/authorization/link and prior-success metadata integrity only; no original mathematical program executed by checker','check_count':len(checks),'checks':checks,'local_link_count':len(links),'local_links':links,'unexpected_C0_files':bad,'decoded_JSON_files':decoded};out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');mp=here/'copy-files.json';files=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and p!=mp);files=sorted(files+[str(mp.relative_to(stage))]);mp.write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':result['status'],'check_count':len(checks),'local_link_count':len(links),'file_count':len(files),'total_bytes':sum((stage/p).stat().st_size for p in files),'manifest':str(mp),'manifest_size':mp.stat().st_size,'manifest_sha256':sha(mp.read_bytes())},ensure_ascii=False));assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
