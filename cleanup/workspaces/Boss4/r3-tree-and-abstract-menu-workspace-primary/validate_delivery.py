"""Artifact checks only; no discovery/original/new mathematical entry reruns."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re
S=Path(__file__).resolve().parents[4];R=S.parent.parent/'boss4-research'
W=Path(__file__).resolve().parent;E=S/'archives/customer-attraction/tools/evidence/tree-and-abstract-menu-workspace-primary'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];links=[];json_count=py_count=0
for p in S.rglob('*'):
 if not p.is_file() or p==S/'copy-files.json':continue
 if '__pycache__' in p.parts:errors.append('unexpected bytecode '+str(p))
 if p.suffix=='.json':json.loads(p.read_text());json_count+=1
 if p.suffix=='.py':compile(p.read_text(),str(p),'exec');py_count+=1
 if p.suffix=='.md':
  for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   link=link.split('#',1)[0]
   if not link or '://' in link:continue
   target=(p.parent/link).resolve()
   try:rel=target.relative_to(S)
   except ValueError:errors.append('outside stage '+str(p)+' '+link);continue
   resolved=target if target.is_file() else R/rel;exists=resolved.is_file()
   links.append({'from':str(p.relative_to(S)),'link':link,'resolved':str(resolved),'exists':exists})
   if not exists:errors.append('missing link '+str(p)+' '+link)
pm=json.loads((E/'primary-manifest.json').read_text());ids={r['id'] for r in pm['sources']}
assert len(ids)==4 and pm['primary_bytes']==sum(r['size'] for r in pm['sources'])==14698
for r in pm['sources']:
 p=S/r['saved_path'];b=p.read_bytes();assert len(b)==r['size'] and sha(p)==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
 assert b==Path(r['local_path']).read_bytes()
cap=json.loads((W/'claim-receipt.json').read_text());ob=json.loads((W/'claim-observation.json').read_text())
assert cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced'
assert len(cap['ids'])==13 and set(cap['ids'])&ids==ids and set(ob['claimed_primary_ids'])==ids
assert sha(W/'claim-receipt.json')==ob['capture_sha256']
assert sha(W/'intake-source-manifest.json')==ob['intake_manifest_sha256']
assert len(ob['local_working_tree_owners'])==4
assert all(x['record']['owner']=='Boss4' and x['record']['disposition']=='in-progress' for x in ob['local_working_tree_owners'])
receipts=json.loads((W/'semantic-receipts.json').read_text());assert len(receipts)==4 and {x['id'] for x in receipts}==ids
for x in receipts:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert x['disposition']=='integrated' and all(x[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for path in x['targets']:assert (S/path).is_file()
check=json.loads((E/'textual-abstract-example-exact-check.json').read_text())
assert check['status']=='pass' and check['new_entry_runs']==1 and check['optimizer_calls']==check['original_program_runs']==0
assert check['node_count']==13 and check['including_self_comparisons']==39 and check['nonself_comparisons']==26
assert len(check['all_27_profiles'])==27 and len(check['all_node_comparisons'])==13
assert len(check['query_matrix'])==3 and all(len(row)==6 for row in check['query_matrix'])
assert check['root_path']==[1,2,2] and check['root_utilities']==['0','1','1']
assert F(check['exact_union_cap'])==F(3,4) and F(check['W_over_m'])==F(2,3)
assert F(check['A_violation'])==F(1,12) and F(check['B_violation'])==F(3,4)
assert [x['exact_value'] for x in check['per_menu_certificates']]==['3/4','1','1']
assert check['CAG_instance_claimed']==check['half_counterexample_claimed']==False
runtime=json.loads((W/'runtime-summary.json').read_text());assert runtime['new_entry_runs']==1 and runtime['original_program_runs']==0 and runtime['optimizer_calls']==0
assert sha(S/runtime['output']['path'])==runtime['output']['sha256']
assert sha(S/runtime['new_definition_entry'])==runtime['new_entry_source']['sha256']
formal=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(formal)==4
for p in formal:
 t=p.read_text();assert t.startswith('---\n')
 for field in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert field in t
result={'status':'pass' if not errors else 'fail','primary_count':4,'primary_bytes':14698,'semantic_receipts':4,
 'formal_pages':4,'json_files_read':json_count,'python_sources_compiled_not_executed':py_count,
 'mathematical_programs_or_optimizers_run_by_validation':0,'local_links':links,'errors':errors}
(W/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='local_links'},ensure_ascii=False))
if errors:raise SystemExit(1)
