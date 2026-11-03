"""Static package integrity; does not execute or import the mathematical driver."""
from pathlib import Path
import argparse,json,re,hashlib

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);a=ap.parse_args();h=Path(__file__).resolve().parent;d=h.parents[4]
 src=json.loads((h/'source-manifest.json').read_text());rc=json.loads((h/'receipts.json').read_text());deps=json.loads((h/'reused-dependencies.json').read_text());rel=json.loads((h/'relationship-review.json').read_text());ev=json.loads((h/'execution-event.json').read_text());rr=json.loads((h/'fixed-binding-review.json').read_text())
 assert len(src)==27 and sum(x['size'] for x in src)==134331
 assert len(rc)==27 and {x['id'] for x in src}=={x['id'] for x in rc}
 for x in src:
  p=h/'original'/x['id']/Path(x['path']).name;assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
  assert len(x['sources'])==2 and all(re.fullmatch('[0-9a-f]{40}',s['commit']) for s in x['sources'])
 for x in rc:
  assert x['full_file_reviewed'] and x['related_material_checked'] and x['unique_content_accounted_for'] and x['disposition']=='integrated'
  assert all((d/p).is_file() for p in x['targets'])
 assert len(deps)==33
 for x in deps:
  p=a.repo/x['path'];assert p.is_file() and p.stat().st_size==x['size'] and sha(p)==x['sha256'],x['path']
 assert len(rel)==13
 for x in rel:assert (d/x['from']).is_file() and ((d/x['to']).is_file() or (a.repo/x['to']).is_file())
 fs=sorted((d/'archives/customer-attraction/state').rglob('*.md'));assert len(fs)==7
 ids=[];links=[]
 for p in fs+[h/'README.md']:
  t=p.read_text()
  if p!=h/'README.md':
   ids.append(re.search('^id: (.*)$',t,re.M).group(1));assert t.startswith('---\n') and '\nsource_refs: ' in t
  for v in re.findall(r'\]\(([^)]+)\)',t):
   if '://' in v or v.startswith('#'):continue
   q=(p.parent/v.split('#')[0]).resolve()
   if not q.is_file():assert (a.repo/q.relative_to(d)).is_file(),(p,v)
   links.append({'file':str(p.relative_to(d)),'target':v})
 assert len(set(ids))==7
 assert ev['actual_driver_invocations']==1 and ev['exit_code']==0 and ev['stderr_bytes']==0
 assert ev['input_pre_sha256']==ev['input_post_sha256']
 assert (h/'run.stdout.txt').stat().st_size==ev['stdout_bytes']==8280 and (h/'run.stderr.txt').stat().st_size==0
 for old,v in ev['input_pre_sha256'].items():
  marker='/e7-insurance-bank-and-fixed-projections-primary/'
  if marker in old:p=h/old.split(marker,1)[1]
  else:p=a.repo/old.split('/co-work-anl-boss3/',1)[1]
  assert sha(p)==v,old
 expected={'projection_atom_visits':128,'integer_type_emissions_before_aggregation':640,'projection_last_BR_comparisons_including_self':25,'stored_ell_scalars_algebra_only':100,'original_weight_policy_keys_structurally_bound':647,'forced_branches_evaluated':102,'full_terminal_extra_query_matrix_entries':612,'new_ell_or_SPE_outcome_BI':0,'new_IC':0,'LP':0,'RNG':0,'original_entry_or_import':0}
 assert rr['actual_operations']==expected
 assert [x['positive_types'] for x in rr['projection_checks']]==[60,155]
 assert len(rr['fixed_query_menu_checks'])==5 and all(x['new_IC_or_LP_optimality_checks']==0 for x in rr['fixed_query_menu_checks'])
 fc=json.loads((h/'field-meaning-clarification.json').read_text());assert fc['new_fixed_target_last_node_BR_comparisons_including_self']==25 and fc['new_complete_strategy_or_mature_policy_IC_comparisons']==0
 result={'status':'PASS','scope':'static source/receipt/dependency/link/unique-event/output-shape checks only; zero mathematical reexecution','primary_count':len(src),'primary_bytes':sum(x['size'] for x in src),'receipt_count':len(rc),'formal_count':len(fs),'dependency_count':len(deps),'relation_count':len(rel),'links_checked':len(links),'math_driver_reexecution':0,'unique_math_event':1,'input_pre_post_same':True,'links':links}
 (h/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='links'},ensure_ascii=False))
if __name__=='__main__':main()
