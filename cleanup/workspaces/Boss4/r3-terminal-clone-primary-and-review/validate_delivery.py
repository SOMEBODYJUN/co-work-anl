"""Read-only delivery checks; no original program or optimizer reruns."""
from pathlib import Path
import hashlib,json,re
S=Path(__file__).resolve().parents[4];R=S.parent.parent/'boss4-research'
E=S/'archives/customer-attraction/tools/evidence/terminal-clone-primary-and-review'
W=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
errors=[];json_count=code_count=0;links=[]
for p in S.rglob('*'):
 if not p.is_file() or p.name=='copy-files.json':continue
 if '__pycache__' in p.parts:errors.append('unexpected cache '+str(p))
 if p.suffix=='.json':json.loads(p.read_text());json_count+=1
 if p.suffix=='.py':compile(p.read_text(),str(p),'exec');code_count+=1
 if p.suffix=='.md':
  for raw in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   link=raw.split('#',1)[0]
   if not link or '://' in link:continue
   dest=(p.parent/link).resolve()
   try:rel=dest.relative_to(S)
   except ValueError:errors.append('out of stage link '+str(p)+' '+link);continue
   resolved=dest if dest.exists() else R/rel
   ok=resolved.is_file();links.append({'from':str(p.relative_to(S)),'link':link,'resolved':str(resolved),'exists':ok})
   if not ok:errors.append('missing link '+str(p)+' '+link)
pm=json.loads((E/'primary-manifest.json').read_text());ids={r['id'] for r in pm['sources']}
assert len(ids)==5 and pm['primary_bytes']==45504
for r in pm['sources']:
 p=S/r['saved_path'];b=p.read_bytes()
 assert len(b)==r['size'] and sha(p)==r['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
for r in json.loads((E/'runtime-manifest.json').read_text())['sources']:
 p=S/r['saved_path'];assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
cap=json.loads((W/'claim-receipt.json').read_text());ob=json.loads((W/'claim-observation.json').read_text())
assert cap['status']=='pushed' and cap['actor']=='Boss4' and cap['local_sync']['status']=='synced'
assert len(cap['ids'])==24 and ids==set(cap['ids'])&set(ob['expected_worker_ids'])
assert sha(W/'claim-receipt.json')==ob['capture_sha256']
assert sha(W/'intake-source-manifest.json')==ob['intake_manifest_sha256']
assert all(x['record']['owner']=='Boss4' and x['record']['disposition']=='in-progress' for x in ob['local_HEAD_owners'])
receipt=json.loads((W/'semantic-receipts.json').read_text());assert {x['id'] for x in receipt}==ids and len(receipt)==5
for x in receipt:
 assert all(x[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(x[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for t in x['targets']:assert (S/t).is_file() or (R/t).is_file()
orig=json.loads((E/'replay-original-review/execution.json').read_text());dual=json.loads((E/'replay-terminal-duals/execution.json').read_text())
assert orig['returncode']==dual['returncode']==0 and orig['stderr_bytes']==dual['stderr_bytes']==0
assert orig['differing_top_level_keys']==['source'] and orig['all_math_fields_equal']
assert not orig['byte_identical'] and not dual['byte_identical']
assert dual['fixed_cone_LP_calls_completed']==2 and dual['observed_dual_records']==2
assert all(x['records_identical'] and x['differing_top_level_keys']==['source'] for x in dual['comparison'])
assert sha(E/'replay-original-review/terminal_clone_refutation_review.json')==orig['output_sha256']
assert sha(E/'replay-terminal-duals/terminal_exact_audit.json')==dual['output_sha256']
new=json.loads((E/'exact-terminal-duals-review.json').read_text())
assert new['status']=='pass' and new['optimizer_calls']==0 and len(new['records'])==2
assert [x['unique_nonzero_IC_rows'] for x in new['records']]==[48,51]
assert [x['beta'] for x in new['records']]==['7/3','2']
assert [x['distinct_topic_coverages'] for x in new['records']]==[4,2]
assert [x['half_slack'] for x in new['records']]==[7,2]
assert all(len(x['complete_dual_support'])==4 and len(x['all_15_coordinate_residuals'])==15 for x in new['records'])
for r in json.loads((E/'derived-inputs/manifest.json').read_text())['inputs']:
 p=E/'derived-inputs'/Path(r['path']).name;assert sha(p)==r['sha256'] and p.stat().st_size==r['size']
 assert p.read_bytes()==(E/'replay-tree'/r['path']).read_bytes()
out={'status':'pass' if not errors else 'fail','json_files_read':json_count,'python_sources_compiled_without_execution':code_count,
 'primary_files':5,'primary_bytes':45504,'semantic_receipts':5,'integrated':2,'duplicate':3,
 'local_links':links,'errors':errors,'original_programs_or_optimizers_run_by_this_validation':0}
(W/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='local_links'},ensure_ascii=False))
if errors:raise SystemExit(1)
