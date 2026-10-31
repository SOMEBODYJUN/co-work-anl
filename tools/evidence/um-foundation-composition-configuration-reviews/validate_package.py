"""Byte/structure/provenance validation only; never executes archived mathematical programs."""
import hashlib,json,re
from pathlib import Path
stage=Path(__file__).resolve().parents[3]
repo=stage.parent.parent/'boss4-research'
ev=stage/'tools/evidence/um-foundation-composition-configuration-reviews'
ws=stage/'cleanup/workspaces/Boss4/r3-um-foundation-composition-configuration-reviews'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inv={a['id']:a for a in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())}
src=load(ev/'source-manifest.json');sup=load(ev/'supporting-source-manifest.json')
assert len(src)==5 and len(sup)==9
verified=[]
for a in src+sup:
 p=stage/a['preserved_path'];v=inv[a['id']]
 assert sha(p)==a['sha256']==v['sha256'] and p.stat().st_size==a['size']==v['size']
 assert len(p.read_text().splitlines())==a['lines']
 verified.append({'id':a['id'],'path':a['preserved_path'],'sha256':sha(p),'bytes':a['size'],'lines':a['lines']})
assert sum(a['size'] for a in src)==96658 and sum(a['lines'] for a in src)==1292
for a in sup:
 assert a['extra_done'] is False
 assert a['full_file_read_this_batch']==(a['actual_read_ranges']==[[1,a['lines']]])
 for lo,hi in a['actual_read_ranges']:assert 1<=lo<=hi<=a['lines']
assert sum(a['full_file_read_this_batch'] for a in sup)==6
support_read_lines=sum(hi-lo+1 for a in sup for lo,hi in a['actual_read_ranges'])
assert support_read_lines==1567
cov=load(ev/'source-section-map.json');assert len(cov['blocks'])==99
for a in src:
 seen=[]
 for z in cov['blocks']:
  if z['source_id']!=a['id']:continue
  lo,hi=z['lines'];assert 1<=lo<=hi<=a['lines'];seen.extend(range(lo,hi+1))
  assert z['subject'] and z['part_identity']
  for p in z['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
 assert seen==list(range(1,a['lines']+1)),a['id']
receipts=load(ws/'semantic-receipts.json');assert len(receipts)==5 and {a['id'] for a in receipts}=={a['id'] for a in src}
for a in receipts:
 assert a['disposition']=='integrated'
 assert all(a[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all((stage/p).is_file() for p in a['targets'])
formal=sorted((stage/'archives').rglob('*.md'));assert len(formal)==11
assert set(p for a in receipts for p in a['targets'])=={str(p.relative_to(stage)) for p in formal}
ids=[]
for p in formal:
 t=p.read_text();assert t.startswith('---\n');front,body=t.split('---\n',2)[1:]
 for k in ('id','kind','type_tag','title','math_scope','status','summary','source_refs'):assert re.search(r'^'+k+':',front,re.M),(p,k)
 ids.append(re.search(r'^id: (.+)$',front,re.M).group(1).strip('"\''))
 assert body.count('$$')%2==0 and body.replace('$$','').count('$')%2==0,(p,'unpaired math delimiter')
assert len(ids)==len(set(ids))
oldids=set()
for p in (repo/'archives').rglob('*.md'):
 z=re.search(r'^id: (.+)$',p.read_text(),re.M)
 if z:oldids.add(z.group(1).strip('"\''))
assert not set(ids)&oldids
links=[]
for p in formal+[ev/'README.md',ws/'README.md',ws/'semantic-review.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target):continue
  target=target.split('#',1)[0]
  if not target:continue
  rel=(p.parent/target).resolve().relative_to(stage)
  assert (stage/rel).exists() or (repo/rel).exists(),(str(p.relative_to(stage)),target)
  links.append({'from':str(p.relative_to(stage)),'to':str(rel)})
cmp=load(ev/'comparison-manifest.json');assert len(cmp)==13
for a in cmp:
 assert sha(repo/a['path'])==a['sha256'] and a['actual_read_scope']=='full' and a['modified'] is False and a['extra_done'] is False
prov=load(ev/'provenance-bindings.json')
model=next(a for a in sup if a['id']=='d6e0835f7054ca7b4789');elim=next(a for a in sup if a['id']=='8ce8667e13d3c4d60937')
assert hashlib.sha256((stage/model['preserved_path']).read_bytes()[:8620]).hexdigest()==prov['classical_reviewed_prefix']['sha256']=='1974c519f154fc5a69054a27302f93c1a391ff212739cf2cf598fbe0f40befa7'
assert hashlib.sha256((stage/elim['preserved_path']).read_bytes()[:27043]).hexdigest()==prov['elimination_three_claim_prefix']['sha256']=='693ece68235f8ead0523db180849781317bb43101b9bbdef247ecc176aa562d9'
reports=prov['single_cycle_two_report_comparison']['originals'];assert len(reports)==2
x,y=[load(stage/a['preserved_path']) for a in reports];diff=[]
def compare(a,z,path=''):
 if type(a)!=type(z):diff.append(path);return
 if isinstance(a,dict):
  assert set(a)==set(z)
  for k in a:compare(a[k],z[k],path+'.'+k)
 elif isinstance(a,list):
  assert len(a)==len(z)
  for k,(u,v) in enumerate(zip(a,z)):compare(u,v,path+f'[{k}]')
 elif a!=z:diff.append(path)
compare(x,y);assert diff==['.canonical_sha256']
assert [a['exact_matrix_rank_if_run'] for a in x['runs']]==[59,139,None]
assert [a['exact_matrix_rank_if_run'] for a in y['runs']]==[59,139,None]
mentions=prov['historical_hash_mentions'];assert len(mentions)==41
for a in mentions:
 for m in a['inventory_matches']:assert inv[m['id']]['sha256']==a['reported_sha256']
assert sum(bool(a['inventory_matches']) for a in mentions)==13
relations=load(ws/'relations.json')['relations'];assert len(relations)==18
for a in relations:
 assert all(a.get(k) for k in ('from','to','type','common_premises','evidence','gap'))
 assert (stage/a['from']).is_file() and ((stage/a['to']).is_file() or (repo/a['to']).is_file())
non_delivery={ev/'initial-version-checks.json',ev/'reading-progress.json',ev/'working-math-notes.json',ev/'validation.json',ws/'copy-files.json'}
json_paths=sorted(p for p in stage.rglob('*.json') if p not in non_delivery)
for p in json_paths:load(p)
collisions=[str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and (repo/p.relative_to(stage)).exists()];assert not collisions,collisions
out={'status':'PASS','scope':'byte/structure/provenance only; no archived mathematical program executed','primary_files':5,'primary_bytes':96658,'primary_lines':1292,'primary_coverage_blocks':99,'preserved_originals':14,'support_full_read_files':6,'support_selected_read_files':3,'support_actual_read_lines':1567,'formal_files':11,'formal_lines':sum(len(p.read_text().splitlines()) for p in formal),'formal_ids':ids,'semantic_receipts':5,'comparison_full_files':13,'comparison_full_lines':sum(a['lines'] for a in cmp),'local_markdown_links_checked':len(links),'links':links,'classical_prefix8620_matches_old1974':True,'elimination_prefix27043_matches_old693ece':True,'single_cycle_actual_field_diff':diff,'D7_exact_matrix_rank_null_retained':True,'historical_hash_mentions':41,'inventory_bound_mentions':13,'unmatched_superseded_or_scratch_not_falsely_bound':28,'relations_with_premises_and_gaps':18,'json_files_parsed_before_validation_and_manifest':len(json_paths),'new_repo_path_collisions':collisions,'verified_originals':verified,'archived_math_program_new_runs':0,'external_PDF_new_read':False,'no_worker_git_claim_done_or_graph_mutation':True}
(ev/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in {'formal_ids','links','verified_originals'}},ensure_ascii=False))
