"""Validate immutable sources, stored primary outputs and links. No original audit import/main execution."""
from pathlib import Path
from fractions import Fraction as F
import ast,hashlib,json,re
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/unrestricted-minwork-row-audits');ws=Path('cleanup/workspaces/Boss4/r3-unrestricted-minwork-row-audits')
def read(p):return json.loads((stage/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(ev/'manifest.json');entries=m['originals']+m['comparisons'];by={r['id']:r for r in entries}
for r in entries+m['verified_historical_derivations']:
 p=stage/r['evidence_path'];assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
 if p.suffix=='.py':ast.parse(p.read_text())
for p in stage.rglob('*.json'):json.loads(p.read_text())
for r in read(ev/'related-formal-material.json'):assert sha(repo/r['path'])==r['sha256']
slot=read(by['505de99a49cb4f03d070']['evidence_path']);face=read(by['d23070a66f58856ab6b5']['evidence_path']);joint=read(by['12b601da50cee4eab718']['evidence_path']);row=read(by['292abbaeaee297858760']['evidence_path'])
assert slot['source_hashes'][by['2862a57bfd5e5369bc2e']['path']]==by['2862a57bfd5e5369bc2e']['sha256']
assert [r['all_slot_to_optimal_pairs_examined'] for r in slot['independent_repair_audit']['records']]==[1,8,45360]
main=face['count_matrix_and_actual_slot_run'];ind=face['independent_labeled_assignment_and_rank_run'];assert main['source_sha256']==by['253f8556a8d8ecbf1dc1']['sha256'];assert ind['sha256']==by['db91cfabf530b5eb601f']['sha256']
assert [r['count_matrix_and_big_position_states'] for r in main['complete_oracles']]==[8,648,640000];assert [r['number_of_labeled_assignments_covered'] for r in main['complete_oracles']]==[8,2187,67108864]
assert [r['assignments'] for r in ind['exhaustive']]==[8,2187];assert len(ind['identities'])==101 and [r['m'] for r in ind['identities'][-2:]]==[10**6,10**50+7]
for r in main['rank_checks']:
 k=r['m'];assert r['active_support_rank']==k*k and F(r['fractional_loads'][-1])==k-1+F(1,k)
for r in main['slot_and_optimal_schedule_checks']:
 k=r['m'];assert r['slots']==k*k and r['slot_edges']==k*(2*k-1) and F(r['slot_matching_makespan'])==2*k-1
assert joint['source_sha256'][by['ad8fccbcbe249fd31a48']['path']]==by['ad8fccbcbe249fd31a48']['sha256'];assert joint['local_prefix_audit']['counts']=={'tested_pairs':83810,'feasible_pairs':39673,'positive_support_pairs':38279};assert joint['local_prefix_audit']['seed']==271828
b=(stage/by['8880cf5284ef95a424b1']['evidence_path']).read_bytes();prefix=b.split(b'## 7.',1)[0].rstrip(b'\r\n')+b'\n';expected='8b1abf7a149759cb2f9c7424c380181442990e0f7ee913273a1c1091526f3e00';assert hashlib.sha256(prefix).hexdigest()==expected==joint['source_sha256'][by['8880cf5284ef95a424b1']['path']];assert prefix==(stage/m['verified_historical_derivations'][0]['evidence_path']).read_bytes()
a=row['main_filter'];assert a['source_sha256']==by['a1d8cc0d5e532a980090']['sha256']==row['sources'][by['a1d8cc0d5e532a980090']['path']];assert (a['legal_matrices'],a['full_assignment_oracle_queries'],a['target_feasible_assignments_preserved'],a['edge_cases'],a['invalid_cases'])==(7344,34344,26624,5,8)
receipts=read(ws/'semantic-receipts.json');assert len(receipts)==5 and {r['id'] for r in receipts}=={r['id'] for r in m['originals']}
for r in receipts:
 assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(r[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for p in r['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
binding=read(ev/'run-binding.json');assert binding['new_original_program_runs']==0 and len(binding['bindings'])==5 and all(r['old_numeric_exit_code'] is None and not r['new_stdout_produced'] for r in binding['bindings'])
broken=[];docs=list((stage/'archives/unrelated-machines/state').rglob('*.md'))+[stage/ev/'README.md']+list((stage/ws).glob('*.md'))
for p in docs:
 for d in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?:|#|source:)',d):continue
  q=(p.parent/d.split('#',1)[0]).resolve()
  try:rel=q.relative_to(stage)
  except ValueError:broken.append([str(p.relative_to(stage)),d]);continue
  if not q.exists() and not (repo/rel).exists():broken.append([str(p.relative_to(stage)),d])
assert not broken,broken
report={'status':'passed','primary_sources':5,'new_formal_objects':4,'new_original_program_runs':0,'checks':['15 inventory original/comparison sources and verified historical prefix size/SHA checked','all JSON parses; all primary Python AST parses only, including unsafe-to-import top-level row-spread','all 5 program hashes match actual old aggregate output or source-hash binding','unrestricted full pair counts and minwork count-vs-label/scaled/rank/slot/101 formula domains checked from stored data','row-spread83810/39673/38279 and exact old canonical8b1a prefix match','row-count7344/34344/26624/5/8 and source identity match','5 full receipts with actual targets','new Markdown links resolve','5 existing formal comparison objects unchanged; no Git/claim/done/spawn']}
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');files=sorted({str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}|{str(ws/'copy-files.json')});(stage/ws/'copy-files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n');report['file_count']=len(files);report['file_identities_excluding_self']=[{'path':p,'size':(stage/p).stat().st_size,'sha256':sha(stage/p)} for p in files if p!=str(ws/'validation.json')];(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert set(files)=={str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()};print(json.dumps({'status':'passed','files':len(files),'bytes':sum((stage/p).stat().st_size for p in files),'new_original_program_runs':0,'new_formal_objects':4},ensure_ascii=False))
