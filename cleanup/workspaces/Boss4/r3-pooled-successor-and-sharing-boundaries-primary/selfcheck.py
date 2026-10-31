"""Integrity/format verification only; never imports or executes the original audit."""
from pathlib import Path
import json,hashlib,os,re,ast
here=Path(__file__).resolve().parent;stage=here.parents[3]
repo=stage.parent.parent/'boss4-research'
E=stage/'archives/customer-attraction/tools/evidence/pooled-successor-and-sharing-boundaries-primary'
out=here/'selfcheck.json';checks=[];links=[]
def rd(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(k,v):checks.append({'check':k,'passed':bool(v)})
ss=rd(E/'source-manifest.json')['rows'];rr=rd(here/'semantic-receipts.json')
ck('five actual primary exact',len(ss)==len(rr)==5 and {x['id'] for x in ss}=={x['id'] for x in rr})
ck('40666 original primary bytes',sum(x['size'] for x in ss)==40666)
ck('two integrated three duplicates',sum(x['disposition']=='integrated' for x in rr)==2 and sum(x['disposition']=='duplicate' for x in rr)==3)
contexts=rd(E/'context-manifest.json')['rows'];programs=rd(E/'context-program-manifest.json');cm=rd(E/'comparison-manifest.json')
ck('related counter MD 10247',len(contexts)==1 and contexts[0]['size']==10247)
ck('related normal-show code/report 11285',len(programs)==2 and sum(x['size'] for x in programs)==11285)
ck('eight formal full comparisons',len(cm)==8)
for r in ss+contexts+programs+cm:
 p=stage/r['evidence_path'];b=p.read_bytes()
 ck('size '+str(p.relative_to(stage)),len(b)==r['size'])
 ck('SHA256 '+str(p.relative_to(stage)),sha(b)==r['sha256'])
 if 'blob' in r:ck('blob '+r['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'])
 if p.suffix=='.py':
  ast.parse(b.decode());ck('AST only (not execution) '+r['id'],True)
baselines=rd(E/'duplicate-canonical-baselines.json')
for b in baselines:
 p=repo/b['path']
 ck('published duplicate canonical same-SHA '+b['path'],p.exists() and p.stat().st_size==b['size'] and sha(p.read_bytes())==b['sha256'] and b['same_as_frozen_LV'])
dm=rd(here/'duplicate-map.json')
ck('18 complete duplicate units',len(dm)==3 and sum(len(x['coverage']) for x in dm)==18 and all(x['full_file_reviewed_as_primary'] for x in dm))
for d in dm:
 ck('six coverage units '+d['id'],len(d['coverage'])==6)
 for u in d['coverage']:
  p=stage/u['target']
  if not p.exists():p=repo/u['target']
  ck('duplicate target section '+d['id']+' '+u['source_unit'],p.exists() and u['target_section'] in p.read_text())
targets=rd(here/'target-paths.json');ck('two new objects',len(targets)==2)
for t in targets:
 p=stage/t;b=p.read_bytes();s=b.decode()
 ck('canonical actual bytes no C0 '+t,not any(x<32 and x not in (9,10,13) for x in b))
 ck('canonical whitespace '+t,not any(l.rstrip()!=l for l in s.splitlines()))
 fm=s.split('---',2)[1]
 meta={k.strip():json.loads(v.strip()) for k,v in (l.split(':',1) for l in fm.strip().splitlines())}
 ck('flat MATEK '+t,all(k in meta for k in ['id','kind','type_tag','title','status','summary','source_refs']))
 for _,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',s):
  if target.startswith(('http:','https:','#')):continue
  rel=Path(os.path.normpath(str(p.parent/target.split('#')[0]))).relative_to(stage)
  ok=(stage/rel).exists() or (repo/rel).exists()
  links.append({'source':t,'target':target,'resolved':str(rel),'exists':ok});ck('local link '+t+' '+target,ok)
 for block in re.findall(r'(?:^\|.*\|\n){2,}',s,re.M):
  ck('generated table shape '+t,len({l.count('|') for l in block.strip().splitlines()})==1)
for r in rr:
 z=next(x for x in ss if x['id']==r['id'])
 ck('receipt final enum '+r['id'],r['disposition'] in ['integrated','duplicate'] and r['owner']=='Boss4')
 ck('receipt identity '+r['id'],r['source_path']==z['path'] and r['source_size']==z['size'] and r['source_sha256']==z['sha256'])
 ck('receipt semantic completeness '+r['id'],all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(len(r[k])>35 for k in ['read_note','comparison_note','decision_note']))
 ck('receipt true targets '+r['id'],r['targets'] and all((stage/t).exists() or (repo/t).exists() for t in r['targets']))
cap=rd(here/'claim-evidence.json');a=rd(here/'primary-authorization-check.json');pr=rd(here/'claim-sync-preservation.json')
ck('raw capture whole ten pushed/needs-attention preserved',len(cap['ids'])==10 and cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='needs-attention' and sha((here/'claim-evidence.json').read_bytes())==a['capture_sha256'])
ck('actual five subset only',set(a['actual_subset'])=={x['id'] for x in ss} and set(a['actual_subset'])<=set(cap['ids']))
ck('independent preservation proof kept',not pr['missing'] and not pr['different'] and not pr['unmerged'] and all(x['same'] for x in pr['tracked']) and pr['stash_kept'] and sha((here/'claim-sync-preservation.json').read_bytes())==a['preservation_sha256'])
for o in a['owner_snapshots']:
 b=(stage/o['snapshot_path']).read_bytes();v=json.loads(b)
 ck('actual owner/source snapshot '+o['id'],sha(b)==o['sha256'] and v['owner']=='Boss4' and v['disposition']=='in-progress' and v['source_sha256']==o['source_sha256'])
scope=rd(E/'scope.json')
ck('all math/original entries zero',all(scope[k]==0 for k in ['original_program_entries','independent_math_entries','canonical_entries','source_function_calls','LP_solver_runs','parameter_or_SPE_scans']))
ck('author/counter four missing retained',len(rd(E/'initial-local-program-missing.json')['missing'])==4)
ck('blind original missing two retained',len(rd(E/'initial-blind-kernel-missing.json')['missing'])==2)
code=next(x for x in programs if x['id']=='5f96320a8099835aa1a9');rep=next(x for x in programs if x['id']=='b6a55365186b119a8022')
j=rd(stage/rep['evidence_path']);claim=rd(E/'blind-kernel-input-and-scope.json')
ck('blind frozen fields true scope',j['true_CAG_r3_product']['forced_joint_As']==9 and j['true_CAG_r3_product']['next_joint_IC_checks']==81 and j['true_CAG_r3_product']['last_joint_IC_checks']==729 and j['true_CAG_r3_product']['Psi']=='8/3' and j['true_CAG_r3_product']['D']=='2/3' and claim['true_r3_frozen_fields']['root_IC_checked'] is False)
ck('blind prior fields retained',j['author_code_or_draft_read'] is False and j['statement_contained_extreme_point_and_rounding_hints'] is True)
ck('blind literal input closure no run',claim['data_input_files']==[] and claim['original_entries']==0 and claim['full_code_and_report_read'])
ck('12 relation checks',len(rd(here/'relation-review.json'))==12 and all(x['checked'] for x in rd(here/'relation-review.json')))
ck('68 manual math checks distinct from program',len(re.findall(r'^\d+\. ',(here/'mathematical-self-review.md').read_text(),re.M))==68)
nr=rd(here/'next-candidates.json');ck('next actual 5 26135B',len(nr)==5 and sum(x['size'] for x in nr)==26135)
for r in nr:
 b=Path(r['local_path']).read_bytes();ck('next exact local '+r['id'],len(b)==r['size'] and sha(b)==r['sha256'])
bad=[];decoded=[]
for p in sorted(stage.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes();rel=str(p.relative_to(stage))
 if any(x<32 and x not in (9,10,13) for x in b):bad.append(rel)
 if p.suffix=='.json' and p!=out:json.loads(b);decoded.append(rel)
ck('all actual files C0 clean',not bad)
ck('all JSON decoded',bool(decoded))
ck('no shared progress writes',not any(str(p.relative_to(stage)).startswith('cleanup/progress/') for p in stage.rglob('*') if p.is_file()))
result={'status':'pass' if all(x['passed'] for x in checks) else 'fail','scope':'format/integrity/authorization/schema checks only; no original audit execution, mathematical LP or SPE verification','check_count':len(checks),'checks':checks,'local_link_count':len(links),'local_links':links,'decoded_JSON_files':decoded,'unexpected_C0_files':bad}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
manifest=here/'copy-files.json'
files=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and p!=manifest)
files=sorted(files+[str(manifest.relative_to(stage))]);manifest.write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'check_count':len(checks),'local_link_count':len(links),'file_count':len(files),'total_bytes':sum((stage/p).stat().st_size for p in files),'manifest':str(manifest),'manifest_size':manifest.stat().st_size,'manifest_sha256':sha(manifest.read_bytes())},ensure_ascii=False))
assert all(x['passed'] for x in checks),[x for x in checks if not x['passed']]
