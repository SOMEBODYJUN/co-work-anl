"""Validate this package's bytes, structure and recorded version edits; no archived math program runs."""
import hashlib
import json
import re
from pathlib import Path
stage=Path(__file__).resolve().parents[3]
repo=stage.parent.parent/'boss4-research'
ev=stage/'tools/evidence/um-bounded-bundle-cactus-reviews'
ws=stage/'cleanup/workspaces/Boss4/r3-um-bounded-bundle-cactus-reviews'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inv={a['id']:a for a in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())}
src=load(ev/'source-manifest.json');sups=load(ev/'supporting-source-manifest.json')
assert len(src)==len(sups)==5
verified=[]
for a in src+sups:
 p=stage/a['preserved_path']; v=inv[a['id']]
 assert sha(p)==a['sha256']==v['sha256'] and p.stat().st_size==a['size']==v['size']
 assert len(p.read_text().splitlines())==a['lines']
 verified.append({'id':a['id'],'path':a['preserved_path'],'sha256':sha(p),'size':a['size'],'lines':a['lines']})
assert sum(a['size'] for a in src)==53098 and sum(a['lines'] for a in src)==602
assert sum(a['lines'] for a in sups)==834
coverage=load(ev/'source-section-map.json');assert len(coverage['blocks'])==44
for a in src:
 got=[]
 for block in coverage['blocks']:
  if block['source_id']!=a['id']:continue
  lo,hi=block['lines'];assert 1<=lo<=hi<=a['lines'];got.extend(range(lo,hi+1))
  for p in block['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
 assert got==list(range(1,a['lines']+1)),a['id']
receipts=load(ws/'semantic-receipts.json');assert len(receipts)==5 and {a['id'] for a in receipts}=={a['id'] for a in src}
for a in receipts:
 assert a['disposition']=='integrated'
 assert all(a[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert all((stage/p).is_file() for p in a['targets'])
formal=sorted((stage/'archives').rglob('*.md'));assert len(formal)==6
ids=[]
for p in formal:
 t=p.read_text();assert t.startswith('---\n');front=t.split('---\n',2)[1]
 for k in ('id','kind','type_tag','title','status','summary','source_refs'):assert re.search(r'^'+k+':',front,re.M),(p,k)
 ids.append(re.search(r'^id: (.+)$',front,re.M).group(1).strip('"\''))
 body=t.split('---\n',2)[2];assert body.count('$$')%2==0,(p,'unpaired display math')
 assert body.replace('$$','').count('$')%2==0,(p,'unpaired inline math')
assert len(set(ids))==len(ids)
old_ids=set()
for p in (repo/'archives').rglob('*.md'):
 m=re.search(r'^id: (.+)$',p.read_text(),re.M)
 if m:old_ids.add(m.group(1).strip('"\''))
assert not set(ids)&old_ids
links=[]
for p in formal+[ev/'README.md',ws/'README.md',ws/'semantic-review.md']:
 for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',link):continue
  target=link.split('#',1)[0]
  if not target:continue
  rel=(p.parent/target).resolve().relative_to(stage)
  assert (stage/rel).exists() or (repo/rel).exists(),(str(p.relative_to(stage)),link)
  links.append({'from':str(p.relative_to(stage)),'to':str(rel)})
comparison=load(ev/'comparison-manifest.json');assert len(comparison)==8
for a in comparison:
 p=repo/a['path'];assert sha(p)==a['sha256'];assert a['actual_read_scope']=='full' and a['extra_done'] is False and a['modified'] is False
prov=load(ev/'provenance-bindings.json');mentions=prov['historical_hash_mentions'];assert len(mentions)==35
for a in mentions:
 for match in a['inventory_matches']:assert inv[match['id']]['sha256']==a['reported_sha256']
assert sum(bool(a['inventory_matches']) for a in mentions)==24
p=next(a for a in sups if a['path'].endswith('bounded_configuration_cardinality_slot_margin.md'))
old=re.sub(r'### 4\.1\..*?(?=## 5\.)','',(stage/p['preserved_path']).read_text(),flags=re.S).encode()
assert len(old)==8538 and hashlib.sha256(old).hexdigest()==prov['bounded_K5_inverse']['inverse_sha256']=='8f32aa1662305c493a28418f646ac320bb82257833faa320c572b6f88b26a345'
p=next(a for a in sups if a['path'].endswith('bundle_coupling_subdivision_barrier.md'))
pre=((stage/p['preserved_path']).read_text().split('\n共同更强边界现已入库：')[0].rstrip('\n')+'\n').encode()
assert len(pre)==14900 and hashlib.sha256(pre).hexdigest()==prov['bundle_crossref_inverse']['inverse_sha256']=='f923212d74e42ac3b32c09d73e15382dd656e90e10b39ea22bc4fa29559cd894'
relations=load(ws/'relations.json')['relations'];assert len(relations)==12
for a in relations:
 assert all(a.get(k) for k in ('from','to','type','common_premises','evidence','gap'))
 assert (stage/a['from']).is_file() and ((stage/a['to']).is_file() or (repo/a['to']).is_file())
json_paths=sorted(stage.rglob('*.json'))
for p in json_paths:load(p)
collisions=[str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file() and (repo/p.relative_to(stage)).exists()];assert not collisions,collisions
result={'status':'PASS','scope':'byte/structure/version-edit validation only; no archived mathematical program executed','primary_files':5,'primary_bytes':53098,'primary_lines':602,'supporting_full_read_files':5,'supporting_full_read_lines':834,'source_coverage_blocks':44,'formal_files':6,'formal_lines':sum(len(p.read_text().splitlines()) for p in formal),'formal_ids':ids,'semantic_receipts':5,'comparison_full_read_snapshots':8,'comparison_lines':sum(a['lines'] for a in comparison),'local_markdown_links_checked':len(links),'links':links,'historical_sha_mentions':35,'inventory_bound_mentions':24,'superseded_or_scratch_mentions_not_falsely_bound':11,'bounded_K5_inverse_match':True,'bundle_crossref_inverse_match':True,'C2_old_sentence_inverse_not_claimed_newly_executed':True,'relations_with_premises_and_gaps':12,'json_files_parsed_before_validation_and_manifest':len(json_paths),'verified_originals':verified,'new_repo_path_collisions':collisions,'fresh_archived_mathematical_program_runs':0,'external_pdf_new_read':False,'no_worker_git_claim_done_or_graph_mutation':True}
(ev/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'formal_ids','links','verified_originals'}},ensure_ascii=False))
