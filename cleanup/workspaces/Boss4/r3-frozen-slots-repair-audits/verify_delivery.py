"""Validate immutable sources and stored records; do not import or run original audit entrypoints."""
from pathlib import Path
from fractions import Fraction as F
import ast,hashlib,json,re
stage=Path(__file__).resolve().parents[4];repo=stage.parent.parent/'boss4-research';ev=Path('archives/unrelated-machines/tools/evidence/frozen-slots-repair-audits');ws=Path('cleanup/workspaces/Boss4/r3-frozen-slots-repair-audits')
def read(p):return json.loads((stage/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(ev/'manifest.json');entries=m['originals']+m['comparisons'];by={r['id']:r for r in entries}
for r in entries+m['verified_historical_derivations']:
 p=stage/r['evidence_path'];assert p.stat().st_size==r['size'] and sha(p)==r['sha256']
 if p.suffix=='.py':ast.parse(p.read_text())
for p in stage.rglob('*.json'):json.loads(p.read_text())
for r in read(ev/'related-formal-material.json'):
 assert sha(repo/r['path'])==r['sha256']
 if r.get('snapshot'):assert sha(stage/r['snapshot'])==r['sha256']
cur=(stage/by['7ff5e8374a6b9826845c']['evidence_path']).read_bytes();pref=cur.split(b'## 6.',1)[0].rstrip(b'\r\n')+b'\n';assert hashlib.sha256(pref).hexdigest()=='8d9be0a73c77fe457e9af4771e02c6c9d386a9260807baf119d4517b5de2470f';assert pref==(stage/m['verified_historical_derivations'][0]['evidence_path']).read_bytes();frag=cur[cur.index(b'## 4a.'):cur.index(b'## 5.')];assert hashlib.sha256(frag).hexdigest()=='718e3aa75a9b06e649c94244c30b7d2296a3a26a268c96fff75f2b3f20e5243c'
slot=read(by['505de99a49cb4f03d070']['evidence_path']);dest=read(by['b18c04f90e7988a75faf']['evidence_path'])
for sid in ['89aef31093a6ecb486eb','0bb03434cec456fccb4d','e57947bc795251d373c3','2862a57bfd5e5369bc2e']:
 r=by[sid];assert slot['source_hashes'][r['path']]==r['sha256']
for sid in ['24d4cbde4355ee2d7185','134caca8f172fdf8cb34']:
 r=by[sid];assert dest['source_sha256'][r['path']]==r['sha256']
assert slot['main_audit']['code_sha256']==by['89aef31093a6ecb486eb']['sha256'];assert slot['main_audit']['baseline_sha256']==by['e57947bc795251d373c3']['sha256'];assert slot['main_audit']['parameters']=={'machines_inclusive':[1,40],'all_assignment_and_matching_enumeration':[1,2,3],'tie_samples_each_m_2_3':6}
assert len(slot['main_audit']['records'])==40
for r in slot['main_audit']['records']:
 k=r['machines'];assert r['jobs']==k*k and F(r['rounded_makespan'])==F(2*k,k+1) and r['changed_jobs']==k-1
assert slot['independent_slot_audit']['route_A']['bijections_examined']==24 and len(slot['independent_slot_audit']['route_A']['perfect_matchings'])==4
assert slot['independent_slot_audit']['route_B']['cardinality_balanced']==1680 and slot['independent_slot_audit']['route_B']['slot_expandable']==216
seq=dest['independent']['sequential_batch_real_load_checks'];assert len(seq)==39;total=0
for r in seq:
 k=r['m'];assert len(r['batches'])==k-1 and F(r['makespans_including_initial'][0])==F(2*k,k+1)
 for z in r['batches']:
  t=z['t'];v=list(map(F,z['actual_loads']));assert len(v)==k and sum(v)==k;assert max(v)==F(z['makespan'])==F(2*k-t,k+1);assert z['hamming_so_far']==t*k-t*(t+1)//2;total+=1
assert total==780
assert dest['source_sha256']['research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md']==m['verified_historical_derivations'][0]['sha256']
# Independently check the retained 3-machine actual input/certificate, not any original main.
i=read(by['ad3aa0a720cfb4d680e4']['evidence_path']);c=read(by['becfdadfd52de5447a65']['evidence_path']);P=[[F(x) for x in row] for row in i['P']];assert len(P)==3 and all(len(row)==9 for row in P)
def loads(s):
 a=[F(0)]*3
 for j,k in enumerate(s):a[k]+=P[k][j]
 return a
assert all(loads(s)==[F(1)]*3 for s in c['optimal_components']);assert loads(c['canonical_covering_assignment'])==list(map(F,c['cover_loads']));assert loads(c['cross_slot_optimal_repair'])==[F(1)]*3;assert [j for j,(a,b) in enumerate(zip(c['canonical_covering_assignment'],c['cross_slot_optimal_repair'])) if a!=b]==c['changed_jobs']==[3,6]
find=read(ev/'comparison-findings.json')
for x in find['findings']:assert x['exact_old_text'] in (stage/x['existing_page']['snapshot']).read_text()
face=read(by['d23070a66f58856ab6b5']['evidence_path'])
for r in face['count_matrix_and_actual_slot_run']['rank_checks']:
 k=r['m'];assert F(r['fractional_loads'][-1])==k-1+F(1,k)
receipts=read(ws/'semantic-receipts.json');assert len(receipts)==5 and {x['id'] for x in receipts}=={x['id'] for x in m['originals']}
for r in receipts:
 assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']);assert all(r[k] for k in ['read_note','comparison_note','decision_note','targets'])
 for p in r['targets']:assert (stage/p).is_file() or (repo/p).is_file(),p
assert read(ev/'run-binding.json')['new_original_program_runs']==0
broken=[];docs=list((stage/'archives/unrelated-machines/state').rglob('*.md'))+[stage/ev/'README.md']+list((stage/ws).glob('*.md'))
for p in docs:
 for d in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if re.match(r'(?:https?:|#|source:)',d):continue
  q=(p.parent/d.split('#',1)[0]).resolve()
  try:rel=q.relative_to(stage)
  except ValueError:broken.append([str(p.relative_to(stage)),d]);continue
  if not q.exists() and not (repo/rel).exists():broken.append([str(p.relative_to(stage)),d])
assert not broken,broken
report={'status':'passed','primary_sources':5,'new_formal_objects':4,'new_original_program_runs':0,'stored_sequential_batches_checked':780,'checks':['13 immutable inventory source sizes and hashes verified; original Python AST only, no import/execution','exact8d9 historical prefix and unchanged718e section recovered and SHA verified','old slot and repair executable source/baseline hashes match originals','all40 slot records, independent finite counts and780 stored actual batch vectors checked','3-machine actual P/components/cover/repair certificate checked','positive final fractional-load formula matches all stored rank records','5 receipts complete with real target paths','all new Markdown links resolve against stage plus repo','5 existing formal comparison objects and2 old-page snapshots unchanged; errata suggestions unapplied']}
(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
files=sorted({str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()}|{str(ws/'copy-files.json')});(stage/ws/'copy-files.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n');report['file_count']=len(files);report['file_identities_excluding_self']=[{'path':p,'size':(stage/p).stat().st_size,'sha256':sha(stage/p)} for p in files if p!=str(ws/'validation.json')];(stage/ws/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');assert set(files)=={str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file()};print(json.dumps({'status':'passed','files':len(files),'bytes':sum((stage/p).stat().st_size for p in files),'new_original_program_runs':0,'formal_objects':4},ensure_ascii=False))
