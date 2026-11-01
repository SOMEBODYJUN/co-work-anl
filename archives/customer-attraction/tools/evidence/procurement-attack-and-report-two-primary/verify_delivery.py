"""Only verify source bytes, complete stored records, domains and references."""
from pathlib import Path
import json,hashlib,itertools,re
E=Path(__file__).resolve().parent;S=E.parents[4];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');W=S/'cleanup/workspaces/Boss4/r3-procurement-attack-and-report-two-primary'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checked(p,x):
 b=p.read_bytes();assert len(b)==x['size'] and sha(p)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob']
rows=read(E/'actual-source-manifest.json')['rows'];assert len(rows)==2 and sum(x['size'] for x in rows)==22526
for x in rows:
 checked(S/x['stage_path'],x);assert x['full_file_reviewed'];o=read(E/'local-progress-at-read'/(x['id']+'.json'));assert o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['sha256']
claim=read(E/'authoritative-full-claim.json');assert claim['status']=='pushed' and claim['operation']=='claim' and claim['actor']=='Boss4' and len(claim['ids'])==6 and {x['id'] for x in rows}<=set(claim['ids']);assert claim['remote_tip']=='8bef0c7380a0a24f3e50275f6a3b2b33094e3a99' and claim['local_sync']['status']=='needs-attention'
p=read(E/'claim-sync-preservation.json');assert p['untracked_count']==1 and p['tracked']==[] and p['missing']==p['different']==[] and not p['unmerged'] and p['stash_kept'] and p['stash']=='204edfe87f6fe9f566302983298b1fa2bcb27e2d'
models=read(E/'runtime-input-manifest.json');deps=read(E/'runtime-dependency-manifest.json');assert len(models)==1 and models[0]['size']==1465 and len(deps)==6
for x in models+deps:checked(S/x['snapshot'],x);assert x['full_file_reviewed'] and x['new_primary'] is False and x['new_done'] is False
helper=next(x for x in deps if x['id']=='23fa081f6234d227b052');assert helper['size']==6375 and helper['sha256']=='82560b788e8f462e809cbc7944f6d0875b16dab7c6e8b49331a2ee7c248635e9'
inst=read(S/models[0]['snapshot']);assert inst['players']==3 and len(inst['topics'])==6 and len(inst['customers'])==13 and sum(z['multiplicity'] for z in inst['customers'])==34
report=read(S/rows[1]['stage_path']);assert report==read(E/'stored-report-literal-transcription.json');assert list(report)==['scope','seed','players','topics','actual_root','actual_counts','positive_depth_rows','best_floating_gap','records'];assert report['players']==5 and report['topics']==6 and report['actual_root']==0 and report['seed']=='individual_security_failure' and report['actual_counts']==[1,0,1,1,1,1] and report['positive_depth_rows']==969 and report['best_floating_gap']==-0.2
formal=S/'archives/customer-attraction/state/程序/真实根菜单全分数采购的原六十六项锥探针--程序.md';text=formal.read_text();rs=report['records'];assert len(rs)==66
starts=[['1' if a in P else '0' for a in range(6)] for size in range(1,7) for P in itertools.combinations(range(6),size)];assert [x['z'] for x in rs[:63]]==starts and [x['z'] for x in rs[63:]]==[['0','0','0','0','0','1']]*3
for i,x in enumerate(rs):
 assert list(x)==['turn','z','status','floating_gap'] and x['turn']==i and len(x['z'])==6 and all(a in ['0','1'] for a in x['z']);assert type(x['floating_gap']) is float and x['status']=='Optimization terminated successfully. (HiGHS Status 7: Optimal)'
 assert '|'+str(i)+'|`'+''.join(x['z'])+'`|`'+repr(x['floating_gap'])+'`|' in text
assert max(x['floating_gap'] for x in rs)==report['best_floating_gap'];assert [x['turn'] for x in rs if x['floating_gap']==-0.2]==[0,1,2,3,4,5,63,64,65];assert rs[62]['floating_gap']==-0.9999999999999978 and '-0.9999999999999978' in text
reading=(E/'report-full-reading.txt').read_text().splitlines();assert json.loads(reading[0])=={k:v for k,v in report.items() if k!='records'} and [json.loads(z) for z in reading[1:]]==rs
cm=read(E/'formal-comparison.json');assert len(cm)==7
for x in cm:assert (S/x['snapshot']).stat().st_size==x['bytes'] and sha(S/x['snapshot'])==x['sha256'] and x['full_file_reviewed']
receipts=read(W/'semantic-receipts.json');assert len(receipts)==2 and {x['id'] for x in receipts}=={x['id'] for x in rows}
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and x['disposition']=='retained';assert all((S/p).is_file() for p in x['targets'])
assert read(W/'source-state-updates.json')==[] and len(read(W/'relation-evidence.json'))==8
for p in [formal,E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  target=link.split('#')[0]
  if not target or '://' in target:continue
  q=(p.parent/target).resolve();assert q.is_file() or (q.is_relative_to(S) and ((R/q.relative_to(S)).is_file() or str(q.relative_to(S)) in {x['path'] for x in cm})),(p,target)
for x in read(W/'content-manifest.json'):assert (S/x['path']).stat().st_size==x['bytes'] and sha(S/x['path'])==x['sha256']
assert read(W/'copy-files.json')==sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
result=dict(status='pass',scope='bytes/provenance/all original records/tables/domains only',primary_count=2,primary_bytes=22526,runtime_models=1,model_bytes=1465,runtime_modules=6,report_root_fields=9,report_records=66,record_fields=4,binary_starts=63,appended_starts=3,inferred_LP_calls=69,formal_comparisons=7,receipts_retained=2,relations=8,original_entry_runs=0,imports=0,solver_runs=0,LP_runs=0,IC_replays=0,primal_dual_replays=0)
(W/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
