"""Delivery integrity only; no original, solver, or mathematical program call."""
from pathlib import Path
import json,hashlib,re,os
here=Path(__file__).resolve().parent;stage=here.parents[3];repo=stage.parent.parent/'boss4-research';E=stage/'archives/customer-attraction/tools/evidence/query-cover-and-tree-tax-review-primary';out=here/'selfcheck.json';checks=[];links=[]
def rd(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(n,v):checks.append({'check':n,'passed':bool(v)})
ss=rd(E/'source-manifest.json')['rows'];rs=rd(here/'semantic-receipts.json');ct=rd(E/'context-manifest.json')['rows'];cm=rd(E/'comparison-manifest.json');sc=rd(E/'scope.json')
ck('five full MD27525B',len(ss)==len(rs)==5 and sum(r['size'] for r in ss)==27525 and all(r['path'].endswith('.md') for r in ss))
ck('three full context prose plus three structured frozen reports',len(ct)==6 and len([r for r in ct if r['full_file_reviewed']])==3 and len([r for r in ct if not r['full_file_reviewed']])==3)
ck('thirteen full current canonical comparisons',len(cm)==sc['formal_full_comparisons']==13)
for r in ss+ct+cm:
 b=(stage/r['evidence_path']).read_bytes();ck('size '+r['evidence_path'],len(b)==r['size']);ck('SHA256 '+r['evidence_path'],sha(b)==r['sha256'])
 if 'blob' in r:ck('blob '+r['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'])
ts=rd(here/'target-paths.json');ck('three selfcontained objects',len(ts)==3)
for t in ts:
 p=stage/t;b=p.read_bytes();s=b.decode();ck('actual canonical bytes C0 '+t,not any(x<32 and x not in (9,10,13) for x in b));ck('generated whitespace '+t,not any(l.rstrip()!=l for l in s.splitlines()))
 f=s.split('---',2)[1];meta={k.strip():json.loads(v.strip()) for k,v in (l.split(':',1) for l in f.strip().splitlines())};ck('flat MATEK '+t,all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs']))
 for _,link in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
  if link.startswith(('http:','https:','#')):continue
  rel=Path(os.path.normpath(str(p.parent/link.split('#')[0]))).relative_to(stage);ok=(stage/rel).exists() or (repo/rel).exists();links.append({'source':t,'target':link,'resolved':str(rel),'exists':ok});ck('local link '+t+' '+link,ok)
 for block in re.findall(r'(?:^\|.*\|\n){2,}',s,re.M):ck('table shape '+t,len({l.count('|') for l in block.strip().splitlines()})==1)
for r in rs:
 z=next(x for x in ss if x['id']==r['id']);ck('final integrated receipt '+r['id'],r['owner']=='Boss4' and r['disposition']=='integrated');ck('receipt identity '+r['id'],r['source_path']==z['path'] and r['source_size']==z['size'] and r['source_sha256']==z['sha256']);ck('receipt true complete read and disposition '+r['id'],all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(len(r[k])>35 for k in ['read_note','comparison_note','decision_note']));ck('receipt target exists '+r['id'],bool(r['targets']) and set(r['targets'])<=set(ts))
c=rd(here/'claim-evidence.json');a=rd(here/'primary-authorization-check.json');ck('raw actual whole capture preserved',c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and sha((here/'claim-evidence.json').read_bytes())==a['capture_sha256'] and c['ids']==a['raw_complete_ids']);ck('only exact own5 actual subset',set(a['actual_subset'])=={r['id'] for r in ss} and set(a['actual_subset'])<=set(c['ids']))
for r in a['owners']:
 b=(stage/r['path']).read_bytes();o=json.loads(b);ck('actual owner/source '+r['id'],sha(b)==r['sha256'] and o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==r['source_sha256'])
ck('all mathematical entries zero',all(sc[k]==0 for k in ['original_program_entries','independent_mathematical_entries','source_function_calls','canonical_entries','LP_solver_runs','parameter_or_SPE_scans']))
ck('manual proof selfreview complete',sc['manual_math_checks']>=60 and len(re.findall(r'^\d+\. ',(here/'mathematical-self-review.md').read_text(),re.M))==sc['manual_math_checks'])
rr=rd(here/'relation-review.json');ck('15 explained relations',len(rr)==sc['relations']==15 and all(x['checked'] for x in rr))
vs=rd(E/'historical-QA-three-version-fields.json');ck('historical version metadata not worker runs',vs['reading_only'] and vs['no_new_certificate_or_run'] and len(vs['rows'])==3 and all(not v['executed_this_batch'] for v in vs['rows']))
ver={v['source_id']:v for v in vs['rows']};v1=ver['e68b561050c225e9b1c2'];v2=ver['5ba4bca1ecdf84ba14d2'];v3=ver['a05630b313dbe7acd001'];ck('three distinct implementation identities',len({v['implementation_sha256_as_reported'] for v in ver.values()})==3)
for v in ver.values():
 ck('four historical fixtures '+v['source_id'],len(v['fixtures'])==4 and [x['full_IC_including_self'] for x in v['fixtures']]==[1554,258,1,6])
 for f in v['fixtures']:ck('raw historical status '+v['source_id']+' '+f['fixture'],f['status']=='passed')
for v,n,tot,sink in [(v2,7,40,33),(v3,9,44,35)]:
 f=v['fixtures'][0];m=f['merge_statistics'];ck('52 exact interlayer counts '+v['source_id'],m['nonactual_interlayer_unit_edges']==n and m['nonactual_interlayer_context_edges']==1 and f['nonzero_edge_count']==tot and f['nonzero_sink_edge_count']==sink)
 for f in v['fixtures']:
  m=f['merge_statistics'];ck('all four merger fields zero '+v['source_id']+' '+f['fixture'],all(m[k]==0 for k in ['nonactual_natural_merge_contexts','nonactual_init_and_natural_merge_contexts','nonactual_unit_client_merge_coordinates','nonactual_multiple_origin_contexts']))
ck('v1 no interlayer observed',v1['fixtures'][0]['nonzero_edge_count']==0 and v1['fixtures'][1]['nonzero_edge_count']==v1['fixtures'][1]['nonzero_sink_edge_count']==12)
nxt=rd(here/'next-candidates.json');ck('next actual four12301B',len(nxt)==4 and sum(x['size'] for x in nxt)==12301)
for x in nxt:
 b=Path(x['local_path']).read_bytes();ck('next local delivery snapshot '+x['id'],len(b)==x['size'] and sha(b)==x['sha256'] and x['progress_snapshot'] is None)
ck('next programs preclaim no execution',rd(here/'next-program-input-closure-preparation.json')['new_original_entries']==0 and rd(here/'next-program-input-closure-preparation.json')['actual_claim_checked'] is False)
# These are byte/metadata checks, not rerunning any finite mathematical assertion.
bad=[];decoded=[]
for p in sorted(stage.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();r=str(p.relative_to(stage))
 if any(x<32 and x not in (9,10,13) for x in b):bad.append(r)
 if p.suffix=='.json' and p!=out:json.loads(b);decoded.append(r)
ck('all text actual bytes C0 clean',not bad);ck('all JSON decoded',bool(decoded));ck('no shared progress file mutation in whitelist',not any(str(p.relative_to(stage)).startswith('cleanup/progress/') for p in stage.rglob('*') if p.is_file()))
result={'status':'pass' if all(x['passed'] for x in checks) else 'fail','scope':'artifact integrity, source identities and historical metadata only; no original mathematical program execution','check_count':len(checks),'checks':checks,'local_link_count':len(links),'local_links':links,'unexpected_C0_files':bad,'decoded_JSON_files':decoded};out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
mp=here/'copy-files.json';files=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and p!=mp);files=sorted(files+[str(mp.relative_to(stage))]);mp.write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks),'local_link_count':len(links),'file_count':len(files),'total_bytes':sum((stage/p).stat().st_size for p in files),'manifest':str(mp),'manifest_size':mp.stat().st_size,'manifest_sha256':sha(mp.read_bytes())},ensure_ascii=False));assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
