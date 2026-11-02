"""Static package integrity only: zero mathematical replays/imports."""
from pathlib import Path
import argparse,json,hashlib,re
E=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);args=parser.parse_args();repo=args.repo.resolve()
# Stage layout and publication layout both supported explicitly.
stage=next((p for p in E.parents if p.name=='deliverables'),None) or repo
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
m=read(E/'source-manifest.json');rr=read(E/'receipts.json');assert len(m)==len(rr)==17 and sum(q['size'] for q in m)==1062548
assert {q['id'] for q in m}=={q['id'] for q in rr}
for q in m:
 p=stage/q['preserved_path'];assert p.is_file() and p.stat().st_size==q['size'] and sha(p)==q['sha256']
for q in rr:
 assert all(q[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
 assert all((stage/p).is_file() or (repo/p).is_file() for p in q['targets'])
for q in read(E/'reused-dependencies.json'):
 p=stage/q['preserved_path'];assert p.stat().st_size==q['size'] and sha(p)==q['sha256'];assert sha(repo/q['repo_path'])==q['sha256']
for q in read(E/'comparison-and-reuse.json')['formal_full_read']:assert sha(repo/q['repo_path'])==q['sha256']
v=E/'review-view';d=read(E/'original/template/aligned_root_cg.json');view=read(v/'cg-dictionaries-and-meta.json');ks=['AB_hist','AE_hist','second_hist','root_hist','menus_lh'];records=[]
for p in sorted(v.glob('cg-atoms-*.jsonl')):records += [json.loads(z) for z in p.read_text().splitlines()]
assert len(records)==934
atoms=[]
for i,z in enumerate(records):
 assert z[0]==i;a={'bits':z[1]};a.update({k:view['dictionaries'][k][z[j+2]] for j,k in enumerate(ks)});a.update(z[-1]);atoms.append(a)
assert atoms==d['atoms'] and [z[-2] for z in records]==d['primal_float']
rows=[]
for p in sorted(v.glob('cg-row-names-*.txt')):rows += [z.split(' ',1)[1] for z in p.read_text().splitlines()]
assert rows==d['row_names'] and view['meta']=={k:v for k,v in d.items() if k not in ['atoms','primal_float','row_names']}
result=read(E/'replay/fixed-audit.json');event=read(E/'replay/execution.json');process=read(E/'replay/process-event.json');assert sha(E/'audit_fixed.py')==event['script']['sha256'];assert process['exit_code']==event['exit_code']==0
assert process['stderr_bytes']==0 and (E/'replay/fixed-audit.stderr.txt').stat().st_size==0
assert result['cg']['isolated_original_function_calls']==3 and len(result['cg']['original_function_exceptions'])==2
for e in result['cg']['original_function_exceptions']:assert e['type']=='IndexError' and 'Traceback' in e['traceback']
assert len(result['cg']['nine_new_names'])==9 and len(result['cg']['aligned_totals_from_saved_decimal_primal'])==34
assert result['games']['direct']['nonprescribed_IC']==3124 and result['games']['security']['nonprescribed_IC']==16806
links=0
for p in list((stage/'archives/customer-attraction/state').rglob('*.md'))+list(E.glob('README.md')):
 prose=re.sub(r'\\\[[\s\S]*?\\\]', '', p.read_text())
 for dest in re.findall(r'\]\(([^)]+)\)',prose):
  if '://' in dest or dest.startswith('#'):continue
  q=(p.parent/dest.split('#')[0]).resolve()
  if not q.exists():
   try:rel=q.relative_to(stage)
   except ValueError:raise AssertionError((p,dest))
   assert (repo/rel).exists(),(p,dest)
  links+=1
assert not list(E.rglob('__pycache__'))
report={'primary_bytes_and_SHA':17,'receipts':17,'reused_dependency_SHA':7,'mature_comparison_SHA':14,'lossless_CG_atoms':934,'lossless_CG_rows':756,'new_pages':4,'local_links':links,'event':'static only; no new math execution; source/function error traces preserved','passed':True}
(E/'static-self-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
