"""Read-only artifact checks; no mathematical entry/original solver rerun."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,re
S=Path(__file__).resolve().parents[4];R=S.parent.parent/'boss4-research';W=Path(__file__).resolve().parent
E=S/'archives/customer-attraction/tools/evidence/quotient-and-fixed-rank-source-primary'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];links=[];json_count=py_count=0
for p in S.rglob('*'):
 if not p.is_file() or p==S/'copy-files.json':continue
 if '__pycache__' in p.parts:errors.append('unexpected cache '+str(p))
 if p.suffix=='.json':json.loads(p.read_text());json_count+=1
 if p.suffix=='.py':compile(p.read_text(),str(p),'exec');py_count+=1
 if p.suffix=='.md':
  for raw in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   link=raw.split('#',1)[0]
   if not link or '://' in link:continue
   dest=(p.parent/link).resolve()
   try:rel=dest.relative_to(S)
   except ValueError:errors.append('link leaves stage '+str(p)+' '+link);continue
   resolved=dest if dest.is_file() else R/rel;exists=resolved.is_file()
   links.append({'from':str(p.relative_to(S)),'link':link,'resolved':str(resolved),'exists':exists})
   if not exists:errors.append('missing link '+str(p)+' '+link)
pm=json.loads((E/'primary-manifest.json').read_text());ids={r['id'] for r in pm['sources']}
assert len(ids)==5 and pm['primary_bytes']==sum(r['size'] for r in pm['sources'])==20588
for r in pm['sources']:
 p=S/r['saved_path'];b=p.read_bytes();assert len(b)==r['size'] and sha(p)==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
 assert b==Path(r['local_path']).read_bytes()
cap=json.loads((W/'claim-receipt.json').read_text());ob=json.loads((W/'claim-observation.json').read_text())
assert cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced'
assert set(cap['ids'])==ids and len(cap['ids'])==5
assert sha(W/'claim-receipt.json')==ob['capture_sha256']
assert sha(W/'intake-local-export-manifest.json')==ob['intake_manifest_sha256']
assert sha(W/'unprovided-dependency-local-export-manifest.json')==ob['missing_dependency_manifest_sha256']
assert all(x['record']['owner']=='Boss4' and x['record']['disposition']=='in-progress' for x in ob['local_working_tree_owners'])
rec=json.loads((W/'semantic-receipts.json').read_text());assert len(rec)==5 and {x['id'] for x in rec}==ids
assert sum(x['disposition']=='duplicate' for x in rec)==1 and sum(x['disposition']=='integrated' for x in rec)==4
for x in rec:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(x[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for path in x['targets']:assert (S/path).is_file() or (R/path).is_file()
missing=json.loads((W/'unprovided-dependency-local-export-manifest.json').read_text())
assert missing['rows']==[] and {x['id'] for x in missing['missing']}=={'667dc37261628075aedc','778506da517c3527abc4','a32ae5fda0d287849e9a','a0956fc8b5c48d613005'}
check=json.loads((E/'reconstructed-rank-strategy-exact-check.json').read_text())
assert check['status']=='pass' and check['new_definition_entry_runs']==1 and check['original_program_runs']==check['optimizer_calls']==0
assert sum(x['constrained_ordered_nodes'] for x in check['cases'])==3260
assert sum(x['including_self_comparisons'] for x in check['cases'])==42578
assert sum(x['nonself_comparisons'] for x in check['cases'])==39318
assert all(F(x['minimum_slack'])==0 for x in check['cases'])
assert [(x['m'],x['cutoff'],x['constrained_ordered_nodes'],x['including_self_comparisons']) for x in check['cases']]==[(5,0,5,50),(9,1,621,11178),(6,2,2591,31092),(3,3,43,258)]
assert check['parameter_lemma_finite_checks']==7168 and check['last_copy_secondary_checks']==1179
assert len(check['threshold_examples'])==9
assert all(F(x['strict_profit'])>0 and x['rank']==x['cutoff']+1 and x['OPT_minus_2W']>0 for x in check['unconstrained_strict_deviation_witnesses'])
rt=json.loads((W/'runtime-summary.json').read_text());new=rt['new_definition_checker']
assert new['entry_runs']==1 and new['optimizer_calls']==0 and new['exit_code']==0
assert sha(S/new['path'])==new['sha256'] and sha(S/new['result']['path'])==new['result']['sha256']
assert all(x==0 for x in rt['original_program_new_runs'].values())
formal=list((S/'archives/customer-attraction/state').rglob('*.md'));assert len(formal)==3
for p in formal:
 text=p.read_text();assert text.startswith('---\n')
 assert not any(s in text for s in ['346?','TODO','TBD'])
 for key in ['id:','kind:','type_tag:','title:','status:','summary:','source_refs:']:assert key in text
out={'status':'pass' if not errors else 'fail','primary_count':5,'primary_bytes':20588,'semantic_receipts':5,
 'integrated':4,'duplicate':1,'new_formal_pages':3,'json_files_read':json_count,'python_sources_compiled_not_executed':py_count,
 'mathematical_programs_or_optimizers_run_by_validation':0,'local_links':links,'errors':errors}
(W/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='local_links'},ensure_ascii=False))
if errors:raise SystemExit(1)
