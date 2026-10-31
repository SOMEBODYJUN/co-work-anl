"""Byte and semantic-receipt structure checks; never runs archived mathematics."""
from pathlib import Path
import json,hashlib,re
from fractions import Fraction
S=Path(__file__).resolve().parents[3];R=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=Path('tools/evidence/um-following-review-primary');W=Path('cleanup/workspaces/Boss4/r3-um-following-review-primary')
def get(p):return json.loads((S/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
c=get(E/'actual-claim.json');src=get(E/'source-manifest.json');layout=get(E/'formal-layout.json');cov=get(E/'primary-read-coverage.json');rec=get(W/'semantic-receipts.json')
assert c['status']=='pushed' and c['operation']=='claim' and c['actor']=='Boss4' and len(set(c['ids']))==5
assert c['remote_tip']=='478dbd6c134eb4bcbd7966124f94cab2f0eaefee' and c['local_sync']['status']=='synced'
assert src['primary_ids']==c['ids'] and len(src['sources'])==13
for x in src['sources']:
 p=S/x['preserved_path'];assert sha(p)==x['sha256'] and len(p.read_bytes())==x['size'];assert len(p.read_bytes().splitlines())==x['lines']
 for a,b in x['actual_read_ranges']:assert 1<=a<=b<=x['lines']
assert sum(x['lines'] for x in src['sources'][:5])==243 and sum(x['size'] for x in src['sources'][:5])==28096
assert len(cov)==5
for x in cov:
 k=1
 for b in x['coverage_blocks']:assert b['start']==k and b['end']>=k;k=b['end']+1
 assert k==x['lines']+1
assert {x['id'] for x in rec}==set(c['ids'])
for x in rec:
 assert x['disposition']=='integrated' and x['targets']==layout['targets'][x['id']]
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(x[k].strip() for k in ['read_note','comparison_note','decision_note'])
ids=[];links=[]
for rel in layout['formal_files']:
 p=S/rel;assert not (R/rel).exists(),'new formal must not overwrite shared path '+rel
 text=p.read_text();m=re.search(r'^id: (.+)$',text,re.M);assert m;ids.append(json.loads(m[1]));assert text.startswith('---\n') and 'kind: review' in text
 for link in re.findall(r'\]\(([^)]+)\)',text):
  if re.match(r'https?://|#',link):continue
  q=(p.parent/link.split('#')[0]).resolve()
  if not q.exists():assert q.is_relative_to(S) and (R/q.relative_to(S)).exists(),(rel,link)
  links.append((rel,link))
 meta=re.search(r'^evidence_manifest: (.+)$',text,re.M);assert meta and (p.parent/meta[1]).resolve().is_file()
assert len(ids)==len(set(ids))==6
for p in (R/'archives').rglob('*.md'):
 text=p.read_text(errors='replace')
 for id in ids:assert not re.search(r'^id: [\"\']?'+re.escape(id)+r'[\"\']?$',text,re.M),(id,p)
f=get(E/'errata-freeze-receipt.json');assert len(f['frozen_files'])==11
for x in f['frozen_files']:
 p=S/x['path'];assert len(p.read_bytes())==x['size'] and sha(p)==x['sha256'],'frozen errata changed '+x['path']
err=get(E/'errata/errata-manifest.json');assert len(err['entries'])==3
replacements=0
for x in err['entries']:
 p=S/x['before_snapshot'];q=S/x['proposed_snapshot'];assert sha(p)==x['baseline_sha256'] and sha(q)==x['proposed_sha256']
 text=p.read_text()
 for change in x['exact_replacements']:
  a=change['original_exact_paragraph'];b=change['replacement_exact_paragraph'];assert text.count(a)==1
  assert p.read_text()[:p.read_text().index(a)].count('\n')+1==change['old_start_line']
  text=text.replace(a,b,1);replacements+=1
 assert text==q.read_text()
 patch=(S/x['unified_patch']).read_text();assert patch.startswith('--- a/'+x['target_repo_path']+'\n+++ b/'+x['target_repo_path']+'\n')
 for e in x['evidence']:
  p=S/e['path'];assert sha(p)==e['sha256']
  for a,b in e['accurate_ranges']:assert 1<=a<=b<=len(p.read_text().splitlines())
assert replacements==7
v=get(E/'version-and-scope-checks.json');cfg=(S/E/'support/7d0842cc19e53d2607fe.md').read_bytes();assert hashlib.sha256(cfg[:35022]).hexdigest()==v['config_preserved_338_prefix_sha256'] and len(cfg[:35022].splitlines())==338
x=(S/E/'support/e7736babc411473bec2a.md').read_text();a=x.index('## F2.');b=x.index('## 来源分工',a);f2=x[a:b]
assert hashlib.sha256(f2.encode()).hexdigest()==v['F2_exact_operational_slice']['sha256']=='a6be77b334b34e17ac2e7a8bf9895849f297892a6b875bfc73204d9bac8f779f'
assert v['F2_historical_slice_rule_not_reproduced'] and v['F2_historical_report_slice_sha256']!=v['F2_exact_operational_slice']['sha256']
long=get(E/'support/649e8a41070019034b4e.json');assert sum(z.get('independent_oracle',{}).get('orientations',0) for z in long['primary_audit']['instances'])==541184
w=get(E/'support/5b8edefb22e5a2e189ac.json');assert w['counts']['feasible_cases']==3536 and Fraction(w['boundary_fixtures']['tiny_q']['q']).denominator==2**257+1
assert src['new_archived_math_program_runs']==0 and src['new_external_pdf_reads']==0
rels=get(W/'relations.json')['relations'];assert len(rels)==13
for x in rels:assert all(x[k] for k in ['from','to','type','common_premises','evidence','gap'])
comp=get(E/'comparison-manifest.json')['formal_full_comparisons'];assert len(comp)==10
out={'status':'PASS','scope':'byte identity, primary complete coverage, typed receipts, new IDs/links, version bindings, immutable errata exact replacements and manifest; not archived mathematical software correctness','preserved_inventory_originals':13,'primaries':5,'primary_bytes':28096,'primary_lines':243,'primary_coverage_blocks':sum(len(x['coverage_blocks']) for x in cov),'formal_files':6,'formal_lines':sum(len((S/p).read_text().splitlines()) for p in layout['formal_files']),'formal_local_links':len(links),'receipts':len(rec),'support_full_read_files':7,'support_selected_read_files':1,'support_semantic_read_lines':2373,'support_newly_displayed_lines':1309,'support_prior_actual_read_reused_lines':1064,'formal_full_comparisons':10,'formal_comparison_lines':sum(x['lines'] for x in comp),'frozen_errata_files':11,'errata_targets':3,'exact_replacements':7,'worker_applied_shared_patch':False,'relations':13,'archived_math_new_runs':0,'external_pdf_new_reads':0,'F2_historical_unknown_slice_hash_not_falsely_reproduced':True}
(S/E/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
mp=S/W/'copy-files.json'
if mp.exists():
 m=get(W/'copy-files.json');assert m['ready'] and len(m['copy_paths'])==len(set(m['copy_paths']))==m['file_count'];assert str(W/'copy-files.json') in m['copy_paths']
 assert set(x['path'] for x in m['files'])==set(m['copy_paths'])-{str(W/'copy-files.json')}
 for x in m['files']:
  p=S/x['path'];assert p.is_file() and len(p.read_bytes())==x['size'] and sha(p)==x['sha256'],x['path']
 print(json.dumps({'status':'PASS','manifest_files':m['file_count'],'manifest_sha256':sha(mp)},ensure_ascii=False))
else:print(json.dumps(out,ensure_ascii=False))
