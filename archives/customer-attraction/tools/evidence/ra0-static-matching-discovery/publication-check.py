#!/usr/bin/env python3
"""Static publication checks; no source imports, payoffs, SPE or optimizer calls."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,json,hashlib,re

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def walk(o,path=''):
 if isinstance(o,dict):return [z for k,v in o.items() for z in walk(v,path+'/'+k)]
 if isinstance(o,list):return [z for k,v in enumerate(o) for z in walk(v,path+'/'+str(k))]
 return [{'pointer':path,'value':o}]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stage',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();stage=a.stage.resolve();repo=a.repo.resolve();ev=stage/'archives/customer-attraction/tools/evidence/ra0-static-matching-discovery'
 sources=json.loads((ev/'source-manifest.json').read_text())['primary_sources'];assert len(sources)==9 and sum(s['size'] for s in sources)==79419;byid={s['id']:s for s in sources}
 for s in sources:
  p=stage/s['preserved_path'];assert p.stat().st_size==s['size'] and sha(p)==s['sha256']
 reading=json.loads((ev/'lossless-report-reading.json').read_text());values=[];reports={}
 for s in sources:
  if s['path'].endswith('.json'):
   o=json.loads((stage/s['preserved_path']).read_text());reports[s['id']]=o;assert reading['reports'][s['id']]==o;leaves=walk(o,'/'+s['id']);assert len(leaves)==reading['primitive_leaf_counts'][s['id']];values+=leaves
 assert values==reading['all_primitive_leaves'] and len(values)==2399
 f=reports['1a8b3c307ddfe82ddcd7'];i=reports['37a2579b9e06bf2da779'];assert f['candidate']['certificate']==i['certificate']
 acts=i['certificate']['actions'];mapping={tuple(r['history']):r['action'] for r in acts};assert len(acts)==len(mapping)==259
 expected={h for d in range(4) for h in product(range(6),repeat=d)};assert set(mapping)==expected and all(0<=v<6 for v in mapping.values())
 identity=json.loads((ev/'saved-point-identities.json').read_text());oldpath=repo/identity['old_final_repo_path'];assert sha(oldpath)==identity['old_final_sha256'];old=json.loads(oldpath.read_text());assert old['certificate']==i['certificate'];assert old['actual']==i['actual']==[3,3,2,2]
 w={str(sum(1<<t for t in r['topics'])):r['multiplicity'] for r in old['instance']['customers']};assert w==i['weights'] and len(w)==22 and sum(w.values())==52
 assert len(f['candidate']['weights'])==63 and sum(x>0 for x in f['candidate']['weights'])==26
 assert 'query_factor' not in f['parameters'] and 'active_types' not in reports['4ef78b15c34281e6d772'] and 'max_weight' not in reports['4ef78b15c34281e6d772']
 ex=reports['b8c1eabef3727fa39a12'];assert len(ex)==14 and sum(r['checked'] for r in ex)==138
 for r in ex:
  assert set(r)=={'file','m','p','checked','maximum_gap','counts','target','value','W','OPT'}
  assert F(r['value'])-r['W']==F(r['maximum_gap']);assert len(r['counts'])==r['p'] and sum(r['counts'])==r['m'] and len(r['target'])==r['m']
 assert sum(F(r['maximum_gap'])==0 for r in ex)==3
 deps=json.loads((ev/'dependency-reuse-manifest.json').read_text())['canonical_modules'];assert len(deps)==4
 for d in deps:
  p=repo/d['reused_repo_path'];assert p.stat().st_size==d['size'] and sha(p)==d['sha256']
 prior=json.loads((ev/'prior-success-reuse-manifest.json').read_text())['files'];assert len(prior)==5
 for r in prior:
  p=repo/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
 comparisons=json.loads((ev/'comparison-bindings.json').read_text())['files'];assert len(comparisons)==5
 for r in comparisons:
  p=repo/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
 receipts=json.loads((stage/'cleanup/workspaces/Boss2/receipts-ra0-static-matching-nine.json').read_text());assert {r['id'] for r in receipts}==set(byid)
 for r in receipts:
  for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert r[k] is True
  for k in ['read_note','comparison_note','decision_note','disposition','targets']:assert r[k]
  assert all((stage/t).is_file() for t in r['targets'])
 links=0;formal=[];ids=[]
 for p in (stage/'archives/customer-attraction/state').rglob('*.md'):
  text=p.read_text();assert text.startswith('---\n');front=text.split('---',2)[1]
  for k in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+k+':',front,re.M)
  ids.append(re.search(r'^id:\s*"?(.*?)"?$',front,re.M).group(1));formal.append(str(p.relative_to(stage)))
  for commit in re.findall(r'source:([a-f0-9]+):',front):assert len(commit)==40
  for target in re.findall(r'\]\(([^)]+)\)',text):
   if re.match('[a-zA-Z]+:',target) or target.startswith('#'):continue
   q=(p.parent/target.split('#')[0]).resolve()
   if not q.exists():assert (repo/q.relative_to(stage)).exists(),str(q)
   links+=1
 assert len(formal)==len(set(ids))==2
 for target in re.findall(r'\]\(([^)]+)\)',(ev/'README.md').read_text()):assert (ev/target).resolve().exists();links+=1
 out={'status':'passed','scope':'Static source/JSON/action-domain/identity/report-arithmetic/evidence/link/receipt QA. No source import, payoff/IC/matching evaluation, discovery, LP or MILP.','primary_sources':9,'primary_bytes':79419,'native_JSON_documents':6,'all_primitive_leaves':2399,'full_policy_actions_unique':259,'full_policy_action_occurrences':518,'old52_weights_certificate_actual_equal':True,'fixture_rows':14,'fixture_checked_field_sum':138,'canonical_runtime_modules_reused':4,'old_success_paths_bound':5,'formal_comparison_paths_bound':5,'original_or_scientific_entrypoints':0,'complete_primary_receipts':9,'formal_objects':sorted(formal),'relative_links_checked':links}
 a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()
