from pathlib import Path
import json,re,hashlib,argparse
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/37f0f9248cfc/boss4-research'));ap.add_argument('--peer-stage',type=Path);args=ap.parse_args()
B=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent;R=args.repo
E=B/'archives/customer-attraction/subarchives/six-providers/tools/evidence/lattice-independent-review-primary'
M=json.loads((E/'source-manifest.json').read_text());D=json.loads((W/'delivery.json').read_text())
for m in M:
 data=(B/m['local_path']).read_bytes();assert len(data)==m['size'] and hashlib.sha256(data).hexdigest()==m['sha256']
assert len([x for x in M if x['role']=='primary'])==3
assert sum(x['size'] for x in M if x['role']=='primary')==8026
receipts=json.loads((W/'semantic-receipts.json').read_text());assert {x['id'] for x in receipts}==set(D['source_ids'])
for q in receipts:
 assert all(q[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all(q[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for p in q['targets']:assert (B/p).exists() or (R/p).exists(),p
ids=[]
for p in D['formal_paths']:
 text=(B/p).read_text();ids.append(re.search(r'^id: "([^"]+)"',text,re.M)[1])
 for m in M:
  for s in m['sources']:assert 'source:'+s['commit']+':'+s['path'] in text
assert len(set(ids))==3
links=[];pending=[]
for p in [B/q for q in D['formal_paths']]+[E/'README.md']:
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if link.startswith(('http','#')):continue
  q=(p.parent/link.split('#')[0]).resolve();good=q.exists()
  try:rel=q.relative_to(B)
  except ValueError:rel=None
  if not good and rel is not None:good=(R/rel).exists() or (args.peer_stage is not None and (args.peer_stage/rel).exists())
  if not good:
   if str(rel)==D['pending_cross_group_file']:pending.append(str(rel))
   else:raise AssertionError((p.name,link))
  links.append({'source':str(p.relative_to(B)),'link':link,'exists':bool(good)})
# Check only lossless data transcription, not the mathematical values or complete strategy.
audit=json.loads((E/'related/lattice_circulation_audit.json').read_text())
construct=(B/D['formal_paths'][1]).read_text()
for n in range(0,len(audit['all_exact_slacks']),3):
 xs=audit['all_exact_slacks'][n:n+3];h=''.join('ABC'[a] for a in xs[0]['history']) or '∅'
 row='| '+h+' | '+' | '.join(x['slack'] for x in xs)+' |'
 assert row in construct
scope=json.loads((E/'execution-scope.json').read_text())
assert all(scope[k]==0 for k in ['current_original_cli_runs','current_original_imports','current_new_math_implementations','current_IC_or_payoff_replays','current_LP_or_SPE_searches'])
res={'status':'PASS' if not pending else 'PASS-own-files;pending-peer-link','primary_files':3,'primary_bytes':8026,'total_evidence_sources':6,'total_evidence_source_bytes':27875,'receipts':3,'formal_objects':3,'links_checked':len(links),'pending_peer_links':pending,'current_math_runs':0,'current_check_scope':'source size/SHA, receipt targets, source refs, stable IDs, links and lossless frozen slack text transfer only; no strategy or payoff computation'}
(W/'self-check-result.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');(W/'link-check.json').write_text(json.dumps(links,ensure_ascii=False,indent=2)+'\n');print(json.dumps(res,ensure_ascii=False))
