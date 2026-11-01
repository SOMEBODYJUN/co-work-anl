from pathlib import Path
import json,hashlib,re,argparse
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/37f0f9248cfc/boss4-resume-20261101'));args=ap.parse_args()
B=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent;R=args.repo
E=B/'archives/customer-attraction/subarchives/six-providers/tools/evidence/warm-dag-discovery-primary'
D=json.loads((W/'delivery.json').read_text());M=json.loads((E/'source-manifest.json').read_text())
assert len(M)==11 and len([x for x in M if x['primary']])==3
assert sum(x['size'] for x in M if x['primary'])==12485
for r in M:
 data=(B/r['local_path']).read_bytes();assert len(data)==r['size'] and hashlib.sha256(data).hexdigest()==r['sha256']
receipts=json.loads((W/'semantic-receipts.json').read_text());assert {r['id'] for r in receipts}==set(D['source_ids'])
for rec in receipts:
 assert all(rec[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(rec[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for target in rec['targets']:assert (B/target).exists() or (R/target).exists(),target
owner=json.loads((W/'owner-snapshot.json').read_text())['actual_read']
assert {r['id'] for r in owner}==set(D['source_ids'])
for r in owner:assert r['progress']['owner']=='Boss4' and r['progress']['source_sha256']==r['sha256']
links=[];ids=[]
for fp in D['formal_paths']:
 text=(B/fp).read_text();ids.append(re.search(r'^id: "([^"]+)"',text,re.M)[1])
 for r in M:
  for q in r['sources']:assert 'source:'+q['commit']+':'+q['path'] in text
assert len(ids)==len(set(ids))==2
for p in [B/q for q in D['formal_paths']]+[E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if link.startswith(('http','#')):continue
  q=(p.parent/link.split('#')[0]).resolve();good=q.exists()
  if not good:
   try:good=(R/q.relative_to(B)).exists()
   except ValueError:pass
  assert good,(p.name,link)
  links.append(link)
scope=json.loads((E/'version-and-execution-scope.json').read_text())
assert scope['warm_script_matches'] is False and scope['original_DAG_matches'] is True
assert all(scope[k]==0 for k in ['current_original_cli_runs','current_imports','current_MILP_calls','current_LP_calls','current_oracle_calls','current_policy_replay_implementation_runs','new_math_implementation_runs'])
report=json.loads((B/next(x['local_path'] for x in M if x['id']=='23a9decde7450d02d501')).read_text());assert len(report)==9
# Metadata and certificate shape only; no strategy, payoff, primal or dual evaluation.
assert len(report['exact_candidate']['strategy']['actions'])==3
workspace=json.loads((B/next(x['local_path'] for x in M if x['id']=='29d0b0997f32f56dd8cf')).read_text());assert set(workspace)=={'schema','save','actor','instance'}
res={'status':'PASS','primary_files':3,'primary_bytes':12485,'preserved_sources':11,'preserved_source_bytes':sum(x['size'] for x in M),'receipts':3,'formal_objects':2,'links_checked':len(links),'owner_source_SHA_verified':True,'version_gap_explicit':True,'current_math_runs':0,'scope':'byte SHA/size, owner/receipt targets, source refs, IDs, links, report/metadata shape and explicit version-binding flags only; no original import or mathematical evaluation'}
(W/'self-check-result.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');print(json.dumps(res,ensure_ascii=False))
