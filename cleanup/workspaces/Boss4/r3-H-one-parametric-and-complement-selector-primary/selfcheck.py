"""Artifact checks only; none of the original mathematical scripts is run."""
from pathlib import Path
import json,hashlib,re,os
here=Path(__file__).resolve().parent;stage=here.parents[3];repo=stage.parent.parent/'boss4-research'
E=stage/'archives/customer-attraction/tools/evidence/H-one-parametric-and-complement-selector-primary'
checks=[];links=[];out=here/'selfcheck.json'
def rd(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(s,v):checks.append({'check':s,'passed':bool(v)})
ss=rd(E/'source-manifest.json')['rows'];rs=rd(here/'semantic-receipts.json');cm=rd(E/'comparison-manifest.json')
ck('primary five/26135B',len(ss)==len(rs)==5 and sum(x['size'] for x in ss)==26135)
ck('eight current full comparisons',len(cm)==8)
for r in ss+cm:
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
ck('whole13 actual claim preserved',len(c['ids'])==13 and c['status']=='pushed' and c['actor']=='Boss4' and c['local_sync']['status']=='synced' and sha((here/'claim-evidence.json').read_bytes())==a['capture_sha256'])
ck('actual own subset only',set(a['actual_subset'])=={x['id'] for x in ss} and set(a['actual_subset'])<=set(c['ids']))
for x in a['owners']:
 b=(stage/x['path']).read_bytes();o=json.loads(b)
 ck('actual owner/source '+x['id'],sha(b)==x['sha256'] and o['owner']=='Boss4' and o['disposition']=='in-progress' and o['source_sha256']==x['source_sha256'])
scope=rd(E/'scope.json')
ck('all mathematical entries zero',all(scope[k]==0 for k in ['original_program_entries','independent_math_entries','canonical_entries','source_function_calls','LP_solver_runs','parameter_or_SPE_scans']))
avail=rd(E/'program-availability.json');ck('five local program/report missing preserved',len(avail['missing'])==5 and avail['rows']==[])
ck('55 manual math checks',len(re.findall(r'^\d+\. ',(here/'mathematical-self-review.md').read_text(),re.M))==55)
ck('12 relation checks',len(rd(here/'relation-review.json'))==12 and all(x['checked'] for x in rd(here/'relation-review.json')))
nr=rd(here/'next-candidates.json');ck('actual next five31187B',len(nr)==5 and sum(x['size'] for x in nr)==31187)
for x in nr:
 b=Path(x['local_path']).read_bytes();ck('next exact local '+x['id'],len(b)==x['size'] and sha(b)==x['sha256'])
bad=[];decoded=[]
for p in sorted(stage.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();rel=str(p.relative_to(stage))
 if any(x<32 and x not in (9,10,13) for x in b):bad.append(rel)
 if p.suffix=='.json' and p!=out:json.loads(b);decoded.append(rel)
ck('actual bytes all files C0 clean',not bad);ck('all JSON decoded',bool(decoded))
ck('no shared progress files',not any(str(p.relative_to(stage)).startswith('cleanup/progress/') for p in stage.rglob('*') if p.is_file()))
result={'status':'pass' if all(x['passed'] for x in checks) else 'fail','scope':'source/format/authorization/link integrity only, no original audit or mathematical program execution','check_count':len(checks),'checks':checks,'local_link_count':len(links),'local_links':links,'decoded_JSON_files':decoded,'unexpected_C0_files':bad}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
mp=here/'copy-files.json';files=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and p!=mp);files=sorted(files+[str(mp.relative_to(stage))]);mp.write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks),'local_link_count':len(links),'file_count':len(files),'total_bytes':sum((stage/p).stat().st_size for p in files),'manifest':str(mp),'manifest_size':mp.stat().st_size,'manifest_sha256':sha(mp.read_bytes())},ensure_ascii=False))
assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
