"""Artifact integrity only. No original/mathematical program or SPE search is run."""
from pathlib import Path
import json, hashlib, re, os

here=Path(__file__).resolve().parent
stage=here.parents[3]
repo=stage.parent.parent/'boss4-research'
E=stage/'archives/customer-attraction/tools/evidence/insurance-source-and-H-product-primary'
out=here/'selfcheck.json'
checks=[]
def check(label,value):
 checks.append({'check':label,'passed':bool(value)})
def sha(b):return hashlib.sha256(b).hexdigest()
def rd(p):return json.loads(p.read_text())

sources=rd(E/'source-manifest.json')['rows']
contexts=rd(E/'context-manifest.json')['rows']
comp=rd(E/'comparison-manifest.json')
receipts=rd(here/'semantic-receipts.json')
check('five complete primary IDs',len(sources)==len(receipts)==5 and {r['id'] for r in sources}=={r['id'] for r in receipts})
check('primary bytes 23140',sum(x['size'] for x in sources)==23140)
check('context three 20452B',len(contexts)==3 and sum(x['size'] for x in contexts)==20452)
check('eight formal comparisons',len(comp)==8)
for r in sources+contexts+comp:
 p=stage/r['evidence_path']; b=p.read_bytes()
 check('size '+str(p.relative_to(stage)),len(b)==r['size'])
 check('SHA256 '+str(p.relative_to(stage)),sha(b)==r['sha256'])
 if 'blob' in r:
  check('Git blob '+r['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'])
targets=rd(here/'target-paths.json')
check('three independent objects',len(targets)==3)
links=[]
for t in targets:
 p=stage/t; b=p.read_bytes();s=b.decode()
 check('actual canonical bytes C0 '+t,not [(i,x) for i,x in enumerate(b) if x<32 and x not in (9,10,13)])
 front=s.split('---',2)[1]
 meta={k.strip():json.loads(v.strip()) for k,v in (l.split(':',1) for l in front.strip().splitlines())}
 check('flat MATEK '+t,all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs']) and isinstance(meta['source_refs'],list))
 check('canonical whitespace '+t,not any(l.rstrip()!=l for l in s.splitlines()))
 for label,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
  if target.startswith(('http:','https:','#')):continue
  dest=Path(os.path.normpath(str(p.parent/target.split('#')[0])))
  rel=dest.relative_to(stage)
  ok=dest.exists() or (repo/rel).exists()
  links.append({'source':t,'target':target,'resolved_path':str(rel),'exists_in_stage_or_repo':ok})
  check('link '+t+' -> '+target,ok)
 for block in re.findall(r'(?:^\|.*\|\n){2,}',s,re.M):
  bars=[l.count('|') for l in block.strip().splitlines()]
  check('generated table shape '+t,len(set(bars))==1)
for r in receipts:
 src=next(x for x in sources if x['id']==r['id'])
 check('receipt final integrated '+r['id'],r['disposition']=='integrated' and r['owner']=='Boss4')
 check('receipt source identity '+r['id'],r['source_size']==src['size'] and r['source_sha256']==src['sha256'] and r['source_path']==src['path'])
 check('receipt full semantic read '+r['id'],all(r[x] is True for x in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(len(r[x])>35 for x in ['read_note','comparison_note','decision_note']))
 check('receipt valid targets '+r['id'],bool(r['targets']) and set(r['targets'])<=set(targets))
cap=rd(here/'claim-evidence.json');auth=rd(here/'primary-authorization-check.json')
check('raw full capture preserved',len(cap['ids'])==36 and cap['status']=='pushed' and cap['actor']=='Boss4' and cap['operation']=='claim' and cap['local_sync']['status']=='synced' and sha((here/'claim-evidence.json').read_bytes())==auth['capture_sha256'])
check('actual subset only',set(r['id'] for r in sources)<=set(cap['ids']) and set(auth['intersection'])==set(r['id'] for r in sources))
for s in auth['owner_checks']:
 b=(stage/s['snapshot_path']).read_bytes();v=json.loads(b)
 check('actual owner snapshot '+s['id'],sha(b)==s['snapshot_sha256'] and v['owner']=='Boss4' and v['disposition']=='in-progress' and v['source_sha256']==s['source_sha256'])
scope=rd(E/'scope.json')
check('all math/original entries zero',all(scope[k]==0 for k in ['original_program_entries','independent_math_entries','canonical_program_entries','source_function_calls','LP_solver_runs','SPE_or_parameter_scans']))
check('context missing 2 truthful',len(rd(E/'context-program-availability.json')['missing'])==2)
nr=rd(here/'next-candidates.json')
check('actual local next five',len(nr)==5 and sum(r['size'] for r in nr)==40666)
for r in nr:
 p=Path(r['local_path']);b=p.read_bytes()
 check('next source exact '+r['id'],len(b)==r['size'] and sha(b)==r['sha256'])
check('twelve mathematical relations',len(rd(here/'relation-review.json'))==12 and all(x['checked'] for x in rd(here/'relation-review.json')))
check('71 manual mathematical checks',len(re.findall(r'^\d+\. ',(here/'mathematical-self-review.md').read_text(),re.M))==71)
all_json=[];bad_c0=[]
for p in sorted(stage.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(stage);b=p.read_bytes()
 if p.suffix=='.json' and p!=out:
  json.loads(b);all_json.append(str(rel))
 if any(x<32 and x not in (9,10,13) for x in b):bad_c0.append(str(rel))
check('actual bytes all files no unexpected C0',not bad_c0)
check('all JSON decoded',bool(all_json))
check('no shared progress writes in whitelist',not any(str(p.relative_to(stage)).startswith('cleanup/progress/') for p in stage.rglob('*') if p.is_file()))
out.write_text(json.dumps({'status':'pass' if all(c['passed'] for c in checks) else 'fail','scope':'format/source integrity/authorization/link checks only, no math program or original audit execution','checks':checks,'check_count':len(checks),'local_links':links,'local_link_count':len(links),'decoded_json_files':all_json,'unexpected_C0_files':bad_c0},ensure_ascii=False,indent=2)+'\n')
manifest=here/'copy-files.json'
files=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and p!=manifest)
files=sorted(files+[str(manifest.relative_to(stage))])
manifest.write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
summary={'status':rd(out)['status'],'check_count':len(checks),'local_link_count':len(links),'file_count':len(files),'total_bytes':sum((stage/f).stat().st_size for f in files),'manifest':str(manifest),'manifest_size':manifest.stat().st_size,'manifest_sha256':sha(manifest.read_bytes())}
print(json.dumps(summary,ensure_ascii=False))
assert all(c['passed'] for c in checks),[c for c in checks if not c['passed']]
