#!/usr/bin/env python3
"""Static provenance/receipt/link/schema check only. Never import primary code."""
import argparse,ast,hashlib,json,pathlib,re,sys
p=argparse.ArgumentParser();p.add_argument('--deliverables',type=pathlib.Path,required=True);p.add_argument('--repo',type=pathlib.Path,required=True);a=p.parse_args();root=a.deliverables.resolve();repo=a.repo.resolve();ev=pathlib.Path(__file__).resolve().parent
load=lambda n:json.loads((ev/n).read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(v,n):
 if not v:raise AssertionError(n)
 checks.append(n)
def locate(rel):
 q=root/rel
 return q if q.is_file() else repo/rel
ms=load('source-manifest.json');check(len(ms)==35,'35 primary identities');check(sum(x['size'] for x in ms)==209241,'209241 primary bytes');check(len({x['id'] for x in ms})==35,'no duplicate primary ID')
asts=0
for x in ms:
 q=locate(x['preserved_repo_path']);check(q.is_file() and q.stat().st_size==x['size'] and sha(q)==x['sha256'],'primary bytes '+x['id']);check(len(x['sources'])==2 and all(len(z['commit'])==40 and z['path']==x['path'] for z in x['sources']),'dual precise refs '+x['id'])
 if q.suffix=='.py':ast.parse(q.read_text(),filename=str(q));asts+=1
 if q.suffix=='.json':json.loads(q.read_text())
check(asts==7,'seven primary Python AST parsed, not imported')
rs=load('receipts.json');check({x['id'] for x in rs}=={x['id'] for x in ms} and len(rs)==35,'35 one-to-one receipts')
for r in rs:
 check(all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']),'three real review gates '+r['id']);check(all(r[k] for k in ['read_note','comparison_note','decision_note']),'individual substantive notes '+r['id']);check(r['disposition']=='integrated' and all(locate(t).is_file() for t in r['targets']),'receipt targets '+r['id'])
deps=load('reused-dependencies.json')
for x in deps:
 q=repo/x['path'];check(q.is_file() and q.stat().st_size==x['size'] and sha(q)==x['sha256'],'dependency bytes '+x['path'])
files=sorted((root/'archives/customer-attraction/state').rglob('*.md'));check(len(files)==6,'six formal objects');ids=[];links=0
allowed={f"source:{s['commit']}:{s['path']}" for x in ms for s in x['sources']}
for q in files:
 s=q.read_text();check(s.startswith('---\n'),'frontmatter '+q.name)
 front=s.split('---',2)[1]
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:check(re.search(r'^'+key+r':',front,re.M) is not None,'formal field '+key+' '+q.name)
 ids.append(json.loads(re.search(r'^id: (.+)$',front,re.M).group(1)))
 refs=re.findall(r'^  - (.+)$',front,re.M);check(len(refs)>=2 and all(json.loads(z) in allowed for z in refs),'exact primary source refs '+q.name)
check(len(set(ids))==6,'unique stable object IDs')
for q in files+[ev/'README.md']:
 for target in re.findall(r'\]\(([^)]+)\)',q.read_text()):
  if '://' in target or target.startswith('#'):continue
  dest=(q.parent/target.split('#')[0]).resolve()
  try:rel=dest.relative_to(root)
  except ValueError:raise AssertionError('link outside deliverables namespace '+target)
  check(locate(rel).exists(),'link '+q.name+' '+target);links+=1
proposal=load('current-statement-correction-proposal.json');check(len(proposal['changes'])==12,'12 precise current-statement changes')
for x in proposal['changes']:
 q=repo/x['path'];check(sha(q)==x['base_sha256'] and q.read_text().count(x['before'])==1,'proposal before SHA and unique text '+x['path'])
account=load('execution-accounting.json');check(all(account[k]==0 for k in ['new_mathematical_executions','original_imports','original_main_calls','original_function_calls','new_LP','new_BI','new_random_calls','new_full_IC_comparisons']),'all mathematical call counts zero')
bind=load('mature-execution-identity-binding.json');check(bind['all_12_stored_fields_equal'] and bind['guard_hashes_match_current_originals'] and len(bind['stored_case5_fields_compared'])==12,'mature case5 metadata binding only')
result={'status':'static-integrity-pass-not-game-validation','primary_count':35,'primary_bytes':209241,'new_originals':sum(x['preservation']=='new-byte-preserved-original' for x in ms),'same_SHA_reused_primaries':sum(x['preservation']=='same-SHA-existing-repo-dependency' for x in ms),'formal_count':6,'individual_receipts':35,'primary_AST_parsed_not_executed':asts,'dependency_count':len(deps),'new_formal_and_evidence_README_links':links,'proposal_replacements':12,'checks':len(checks),'new_mathematical_calls':0}
(ev/'self-check-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
