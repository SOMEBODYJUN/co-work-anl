#!/usr/bin/env python3
"""Static package/source/result/receipt/link checks only; no imports or solve."""
from pathlib import Path
import ast,hashlib,json,re
P=Path(__file__).resolve().parent;S=P.parents[4];B=Path('/workspace/scratch/9559bf893d22');C=B/'co-work-anl-boss3'
sha=lambda b:hashlib.sha256(b).hexdigest()
M=json.loads((P/'source-manifest.json').read_text());assert len(M)==6 and sum(x['size'] for x in M)==55369
for x in M:
 f=P/'original'/Path(x['path']).name;data=f.read_bytes();assert len(data)==x['size'] and sha(data)==x['sha256']
 if f.suffix=='.py':ast.parse(data,filename=f.name)
 else:json.loads(data)
for x in json.loads((P/'related-dependencies.json').read_text()):
 data=(P/'related'/x['file']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
for x in json.loads((P/'run-output-manifest.json').read_text())['files']:
 data=(P/x['file']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
R=json.loads((S/'cleanup/workspaces/Boss3/receipts-20261101-root-coupling-six.json').read_text());assert len(R)==6 and {r['id'] for r in R}=={x['id'] for x in M}
for r in R:
 assert all(r[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for')) and r['disposition']=='integrated'
 for path in r['targets']:assert (S/path).is_file(),path
old=json.loads((P/'two-original-top-level-events.json').read_text());new=json.loads((P/'definition-audit-event.json').read_text())
assert old['original_top_level_runs']==2 and old['original_LP_calls']==0 and len(old['runs'])==2
assert sha((P/'replay_two_top_levels.py').read_bytes())==old['wrapper_sha256']
assert new['new_definition_audit_runs']==1 and new['LP_calls']==0 and new['original_top_level_runs']==0
assert sha((P/'audit_fixed92_from_definition.py').read_bytes())==new['checker_sha256']
for run in old['runs']:
 assert run['returncode']==0 and run['byte_equal_frozen'] is True
 assert not (P/run['stderr_file']).read_bytes()
 actual=(P/run['output']).read_bytes();frozen=(P/'original'/run['output'].removeprefix('current-')).read_bytes();assert actual==frozen
 assert len(actual)==run['output_bytes'] and sha(actual)==run['output_sha256']
audit=json.loads((P/'fixed92-definition-audit.json').read_text());assert audit['complete_supported_histograms']==96 and audit['all_96_saved_columns_exhaustive_and_unique'] is True
assert audit['literal_fixed_index_vs_original_offrow_coefficients']==1536 and audit['all_coefficients_equal'] is True
assert audit['zero_column_slacks']==72 and audit['strict_column_slacks']==24 and audit['nu_nonzero_count']==30
pages=sorted((S/'archives/customer-attraction/state').rglob('*.md'));assert len(pages)==2
links=0
for f in pages:
 text=f.read_text();assert text.startswith('---\n') and '\n---\n' in text
 front=text.split('---',2)[1]
 for key in ('id','kind','type_tag','title','status','summary','source_refs'):assert re.search('^'+key+':',front,re.M)
 assert text.count('\\[')==text.count('\\]') and text.count('\\(')==text.count('\\)') and text.count('$')%2==0
 assert all(line==line.rstrip() for line in text.splitlines()),f
 for target in re.findall(r'\]\(([^)]+)\)',text):
  if target.startswith(('http:','https:','#','mailto:')):continue
  actual=(f.parent/target).resolve()
  if not actual.is_file():
   rel=actual.relative_to(S);assert any((base/rel).is_file() for base in (C,B/'boss3_root_menu_delivery')), (f,target)
  links+=1
 # Bind all copied exact certificate multiplier entries and exact budget to calculation prose.
 if f.name.startswith('九十二细胞'):
  for r in audit['nu_nonzero']:
   row='|'+str(r['cell_index_zero_based'])+'|'+str(r['atom'])+'|'+str(r['t'])+'|('+','.join(map(str,r['replies']))+')|'+r['nu'].replace('-','−')+'|'
   assert row in text,row
  numerator,denominator=audit['impossibility_budget'].split('/');assert numerator in text and denominator in text
for f in P.rglob('*.py'):ast.parse(f.read_text(),filename=str(f))
result={'kind':'static deliverable check; not a second mathematical audit','passed':True,'primary_sources':6,'primary_bytes':55369,'receipts':6,'formal_pages':2,'local_links_checked':links,'original_top_level_events_preserved':2,'new_definition_event_preserved':1,'new_original_imports':0,'new_LP_calls':0,'new_BI_calls':0,'new_random_samples':0,'checker_sha256':sha(Path(__file__).read_bytes())}
(P/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
