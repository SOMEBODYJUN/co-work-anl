"""Byte/coverage/link/manifest checks only; does not execute archived mathematics."""
from pathlib import Path
import json,hashlib,re

S=Path(__file__).resolve().parents[3]
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=Path('tools/evidence/um-next-available-reviews')
W=Path('cleanup/workspaces/Boss4/r3-um-next-available-reviews')
def get(rel):return json.loads((S/rel).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=get(E/'source-manifest.json');cov=get(E/'primary-read-coverage.json');layout=get(E/'formal-layout.json')
assert src['claim_pushed']=='a6093a6b20ceb96e5de0c1616d75d54520d5cdaa'
for r in src['sources']:
 p=S/r['preserved_path'];assert sha(p)==r['sha256'] and len(p.read_bytes())==r['size']
 assert len(p.read_bytes().splitlines())==r['lines']
 for a,b in r['actual_read_ranges']:assert 1<=a<=b<=r['lines']
for r in cov:
 n=1
 for b in r['coverage_blocks']:
  assert b['start']==n and b['end']>=n;n=b['end']+1
 assert n==r['lines']+1
assert len(cov)==5 and sum(r['lines'] for r in cov)==417
assert sum(r['size'] for r in src['sources'] if r['role']=='claimed-primary')==51860
assert src['new_archived_math_program_runs']==0 and src['new_external_pdf_reads']==0
receipts=get(W/'semantic-receipts.json');assert {r['id'] for r in receipts}==set(src['primary_ids'])
for r in receipts:
 assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert r['disposition']=='integrated' and all(r[k].strip() for k in ['read_note','comparison_note','decision_note'])
 assert r['targets']==layout['targets'][r['id']]
 assert all((S/p).is_file() for p in r['targets'])
ids=[];links=[]
for rel in layout['formal_files']:
 p=S/rel;assert not (R/rel).exists(),'new path would overwrite '+rel
 text=p.read_text();m=re.search(r'^id: (.+)$',text,re.M);assert m;id=json.loads(m[1]);ids.append(id)
 assert text.startswith('---\n') and all(x in text for x in ['kind: review','type_tag: 审查','source_refs:'])
 for target in re.findall(r'\]\(([^)]+)\)',text):
  if re.match(r'https?://|#',target):continue
  target=target.split('#')[0];q=(p.parent/target).resolve()
  if not q.exists():
   assert q.is_relative_to(S);assert (R/q.relative_to(S)).exists(),(rel,target)
  links.append({'from':rel,'target':target})
 meta=re.search(r'^evidence_manifest: (.+)$',text,re.M);assert meta and (p.parent/meta[1]).resolve().is_file()
assert len(ids)==len(set(ids))==7
for p in (R/'archives').rglob('*.md'):
 text=p.read_text(errors='replace')
 for id in ids:assert not re.search(r'^id: [\"\']?'+re.escape(id)+r'[\"\']?$',text,re.M),(p,id)
v=get(E/'version-and-scope-checks.json')
assert v['old_current_A_through_E_equal'] and v['common_A_E_bytes']==35234
assert all(v[k] for k in ['dual_current_equals_final_review_hash','fixed_sink_current_equals_final_review_hash','arity_current_section7_review_hash_bound'])
assert v['xos_source_table_original_rows']==25 and v['xos_correction_table_rows']==2
assert v['unavailable_field_correction']['field_value'] is True and not v['unavailable_field_correction']['full_program_run_performed']
code=(S/E/'support/1baaf1963c7582471b42.py').read_text()
assert 'values = [None, F(0), F(1, 3), F(1, 2), F(1)]' in code
assert 'for sigma in product(*domains)' in code and '"unavailable": True' in code
assert 24+24**2+24**3==14424
report=get(E/'support/2503c0d7bd0be638eeb2.json')
assert report['triple_full_matrix_oracle']['matrices']==14424
assert report['scope_counterexample']['O4']=='1' and report['scope_counterexample']['ordinary_opt']=='5/4'
assert 'general rational LP backend' in report['not_implemented']
rels=get(W/'relations.json')['relations'];assert len(rels)==13
for r in rels:assert all(r[k] for k in ['from','to','type','common_premises','evidence','gap'])
formal_lines=sum(len((S/p).read_text().splitlines()) for p in layout['formal_files'])
out={'status':'PASS','scope':'source byte hashes, exact stated read coverage, receipts, new IDs, Markdown links and version bindings only; not a mathematical-software run','preserved_originals':len(src['sources']),'primary_sources':5,'primary_bytes':51860,'primary_lines':417,'primary_coverage_blocks':sum(len(r['coverage_blocks']) for r in cov),'support_full_read_files':sum(r['full_file_reviewed'] for r in src['sources'][5:]),'support_selected_read_files':sum(not r['full_file_reviewed'] for r in src['sources'][5:]),'support_actual_read_lines':sum(b-a+1 for r in src['sources'][5:] for a,b in r['actual_read_ranges']),'formal_files':len(ids),'formal_lines':formal_lines,'formal_local_links_checked':len(links),'receipts':len(receipts),'relations':len(rels),'NSW_common_A_E_bytes':35234,'new_archived_math_program_runs':0,'new_external_pdf_reads':0,'unavailable_field_meaning':'includes None endpoints, not missing finite oracle'}
(S/E/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
mp=S/W/'copy-files.json'
if mp.exists():
 m=get(W/'copy-files.json');assert m['ready'] and m['file_count']==len(m['copy_paths'])==len(set(m['copy_paths']))
 assert str(W/'copy-files.json') in m['copy_paths']
 assert {x['path'] for x in m['files']}==set(m['copy_paths'])-{str(W/'copy-files.json')}
 for x in m['files']:
  p=S/x['path'];assert p.exists() and len(p.read_bytes())==x['size'] and sha(p)==x['sha256'],x['path']
 print(json.dumps({'status':'PASS','manifest_files_checked':m['file_count'],'manifest_sha256':sha(mp)},ensure_ascii=False))
else:print(json.dumps(out,ensure_ascii=False))
