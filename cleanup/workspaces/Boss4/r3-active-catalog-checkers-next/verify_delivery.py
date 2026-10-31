#!/usr/bin/env python3
"""New bounded delivery integrity check; no historical code execution."""
from pathlib import Path
import ast,hashlib,json,re
S=Path(__file__).resolve().parents[4]
E=S/'tools/evidence/active-catalog-checkers'
W=Path(__file__).resolve().parent
R=S.parent.parent/'boss4-research'
PRIOR=S.parent/'r3-research-index-builders'
checks=[]
def check(name,condition,detail=None):
 checks.append({'check':name,'pass':bool(condition),'detail':detail})
 if not condition:raise AssertionError(name)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['source-manifest.json','related-manifest.json','comparison-manifest.json']:
 for row in json.loads((E/name).read_text()):
  p=S/row['saved_path'];check(name+': '+row['path']+':'+row.get('id','snapshot'),p.is_file() and p.stat().st_size==row['size'] and sha(p)==row['sha256'])
source=json.loads((E/'source-manifest.json').read_text())
check('four exact source IDs',{r['id'] for r in source}=={'c4ec30b839b1b52dc78e','2c67c456c9bdaf886f35','c1652066ec8f7c06a897','aba0feb89c0a654eab75'})
check('source bytes',sum(r['size'] for r in source)==27065)
for p in [*E.rglob('*.py'),Path(__file__)]:
 ast.parse(p.read_text());check('AST parses '+str(p.relative_to(S)),True)
for p in E.rglob('*.json'):json.loads(p.read_text())
check('all evidence JSON parses',True)
a=json.loads((E/'contract-structural-audit.json').read_text());c=a['catalog'];active=a['active'];wc=a['wc'];extra=json.loads((E/'additional-inspection.json').read_text())
check('2099 catalog real data rows equal',c['generated_catalog_data_rows']==2099 and c['generated_catalog_all_data_rows_exact_order_equal'])
check('501 WC real data rows equal',c['generated_WC_data_rows']==501 and c['generated_WC_all_data_rows_exact_order_equal'])
check('actual catalog structural exceptions empty',all(not c[k] for k in ['canonical_bad','human_label_and_purpose_bad','unknown_topics_or_roles','unnamed_related_paths']))
check('two frozen required810 metadata sets cover',len(c['required_frozen_metadata'])==2 and all(v['required']==810 and not v['missing_catalog'] and not v['catalog_absent_frozen_paths'] and not v['renamed_old_still_present'] for v in c['required_frozen_metadata'].values()))
check('source/classification170 keys equal',wc['source_files_count']==170 and wc['classification_count']==170 and wc['equal_keysets'])
check('164 retained,6 explicit retire',sum(r['path'] is not None for r in wc['rows'])==164 and sum(bool(r.get('explicit_retirement')) for r in wc['rows'])==6)
check('97 sourcehash metadata matches both commits',sum(isinstance(r.get('frozen_hash_matches_some_recorded_source'),dict) for r in wc['rows'])==97 and all(all(r['frozen_hash_matches_some_recorded_source'].values()) for r in wc['rows'] if isinstance(r.get('frozen_hash_matches_some_recorded_source'),dict)))
check('actual28 archived byte hashes',len(active['actual_retired_byte_checks'])==28 and all(r['equal'] for r in active['actual_retired_byte_checks']))
check('four routing constant versions',len(active['constants'])==4 and all(r['values']['DEFAULT_SAVE']=='customer-attraction' for r in active['constants']))
check('34 input versions and595 lexical links',len(active['actual_entry_input_checks'])==34 and sum(len(r['links']) for r in active['lexical_link_metadata_checks'])==595)
check('all active local frozen presence',all(all(l['frozen_presence'].values()) for r in active['lexical_link_metadata_checks'] for l in r['links']))
check('scope substring limitation recorded',active['substring_accepts_six_specific_target'] is True)
check('77 map files metadata coverage',extra['mathematical_map_files_including_entry']==77 and not extra['missing_linked_mathematical_files'])
check('actual current JSON66 leaves',json.loads((E/'json-field-census.json').read_text())['aba0feb89c0a654eab75']['ordered_scalar_count']==66)
receipts=json.loads((W/'semantic-receipts.json').read_text());check('four complete receipts',len(receipts)==4 and {r['id'] for r in receipts}=={r['id'] for r in source} and all(all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(r[k] for k in ['read_note','comparison_note','decision_note','disposition','targets']) for r in receipts))
formal={t for r in receipts for t in r['targets']}
for target in sorted(formal):
 p=S/target;t=p.read_text();check('formal exists '+target,p.is_file());head=t.split('---',2)[1]
 for key in ['id','kind','type_tag','title','status','summary','source_refs']:check('frontmatter '+p.name+':'+key,re.search('^'+key+':',head,re.M) is not None)
 check('two full commits '+p.name,all(c in head for c in ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']))
 check('no trailing whitespace derived '+p.name,all(l==l.rstrip() for l in t.splitlines()))
 clean=re.sub(r'`[^`]*`','',t)
 for href in re.findall(r'\]\(([^)]+)\)',clean):
  if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',href) or href.startswith('#'):continue
  dest=(p.parent/href.split('#',1)[0]).resolve();rel=dest.relative_to(S.resolve());which='current batch' if dest.exists() else 'result repo' if (R/rel).exists() else 'prior exact delivered batch' if (PRIOR/rel).exists() else 'missing'
  check('local link '+p.name+' -> '+href,which!='missing',which)
out={'scope':'new delivery/metadata and explicitly limited evidence only; no historical-suite execution, full old-tree materialization, mathematical truth or visual PASS','passed':len(checks),'checks':checks,'formal_pages':len(formal),'formal_bytes':sum((S/p).stat().st_size for p in formal),'source_files':4,'source_bytes':27065,'related_versions':80}
(W/'self-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='checks'},ensure_ascii=False))
