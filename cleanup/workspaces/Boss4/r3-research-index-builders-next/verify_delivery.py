#!/usr/bin/env python3
"""New delivery checks only; never executes historical source programs."""
from pathlib import Path
import ast,hashlib,json,re
BASE=Path(__file__).resolve().parents[4]
E=BASE/'tools/evidence/research-index-builders'
REPO=BASE.parent.parent/'boss4-research'
W=Path(__file__).resolve().parent
checks=[]
def check(name,condition,detail=None):
 checks.append({'check':name,'pass':bool(condition),'detail':detail})
 if not condition:raise AssertionError(name)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['source-manifest.json','related-manifest.json','comparison-manifest.json']:
 rows=json.loads((E/name).read_text())
 for r in rows:
  p=BASE/r['saved_path'];size=r.get('size',r.get('bytes'))
  check(name+': '+r['path'],p.is_file() and p.stat().st_size==size and sha(p)==r['sha256'])
for p in [*E.glob('original/**/*.py'),*E.glob('related/**/*.py'),E/'inspect_inputs.py',Path(__file__)]:
 ast.parse(p.read_text());check('AST parse '+str(p.relative_to(BASE)),True)
manifest=json.loads((E/'source-manifest.json').read_text())
check('exact three claimed IDs',{r['id'] for r in manifest}=={'3c77f5d856d06d7dcff2','a8447f8474582ae3d971','2f6fe35ae6ddbac5dbca'})
a=json.loads((E/'input-structural-audit.json').read_text());g=a['graph'];c=a['crosswalk'];x=a['assets'];refs=json.loads((E/'reference-census.json').read_text())
check('true static generated HTML binding',g['static_generated_html_exact_bytes_equal'])
check('true all680 actual table rows binding',c['all680_generated_rows_in_exact_order_equal'] and c['actual_output_rows']==680)
check('true missing title-tail candidate recorded',len(g['ignored_claim_table_rows_after_logic_heading'])==1 and g['ignored_row_ids_in_graph']=={'CA-INCIDENCE-LP-DYNAMIC-BUDGET-v1':False})
review=json.loads((E/'related/research/review_status.json').read_text())
check('title-tail candidate absent review too','CA-INCIDENCE-LP-DYNAMIC-BUDGET-v1' not in {r['id'] for r in review['entries']})
m=json.loads((E/'related/research/path_migration.json').read_text())
check('actual two migration key sets disjoint',not(set(m['moved'])&set(m['retired_code_paths'])))
check('all JSON fields census actual input count',a['all_json_files']==14 and len(json.loads((E/'json-field-census.json').read_text()))==14)
check('complete counted path references',refs['total_references']==15535 and refs['unique_paths']==2754 and not refs['missing_files'])
check('33 true module links all frozen present',x['learning_modules']==33 and len(x['learning_links'])==273 and all(y['frozen_exists'] for y in x['learning_links']))
check('actual five input/cert metadata equal',sum(len(r['input_certificate_bindings']) for r in x['historical_run_manifests'])==5 and all(v['equal'] for r in x['historical_run_manifests'] for v in r['input_certificate_bindings']))
receipts=json.loads((W/'semantic-receipts.json').read_text())
check('three complete receipts',len(receipts)==3 and {r['id'] for r in receipts}=={r['id'] for r in manifest} and all(all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']) and all(r[k] for k in ['read_note','comparison_note','decision_note','disposition','targets']) for r in receipts))
formal=[]
for r in receipts:
 for target in r['targets']:
  p=BASE/target;check('receipt target exists '+target,p.is_file());text=p.read_text();formal.append(p)
  head=text.split('---',2)[1]
  for k in ['id','kind','type_tag','title','status','summary','source_refs']:
   check('frontmatter '+p.name+':'+k,re.search(r'^'+k+r':',head,re.M) is not None)
  check('both exact commits '+p.name,all(commit in head for commit in ['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c']))
  check('no trailing whitespace derived '+p.name,all(line==line.rstrip() for line in text.splitlines()))
  clean=re.sub(r'`[^`]*`','',text)
  for href in re.findall(r'\]\(([^)]+)\)',clean):
   if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',href) or href.startswith('#'):continue
   dest=(p.parent/href.split('#',1)[0]).resolve();rel=dest.relative_to(BASE.resolve())
   check('formal real local link '+p.name+' -> '+href,dest.exists() or (REPO/rel).exists())
for p in BASE.rglob('*.json'):
 json.loads(p.read_text())
check('all delivery JSON parses',True)
out={'scope':'delivery integrity and explicitly bounded new structural evidence only; no old suite, browser, full dependency materialization, current graph acceptance or mathematical proof','passed':len(checks),'checks':checks,'formal_files':len(set(formal)),'formal_bytes':sum(p.stat().st_size for p in set(formal)),'source_files':len(manifest),'source_bytes':sum(r['size'] for r in manifest)}
(W/'self-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},ensure_ascii=False))
