#!/usr/bin/env python3
"""Static deliverable/identity checks only; no source import, LP, BI, or samples."""
from pathlib import Path
import ast, hashlib, json, re
P=Path(__file__).resolve().parent
S=P.parents[4]
C=Path('/workspace/scratch/9559bf893d22/co-work-anl-boss3')
sha=lambda data:hashlib.sha256(data).hexdigest()
M=json.loads((P/'source-manifest.json').read_text())
assert len(M)==6 and sum(x['size'] for x in M)==17553
for x in M:
 f=P/'original'/Path(x['path']).name;data=f.read_bytes()
 assert len(data)==x['size'] and sha(data)==x['sha256'],f
 if f.suffix=='.py':ast.parse(data,filename=f.name)
 else:json.loads(data)
R=json.loads((S/'cleanup/workspaces/Boss3/receipts-20261101-anonymous-potential-five.json').read_text())
assert len(R)==6 and {x['id'] for x in R}=={x['id'] for x in M}
for r in R:
 assert all(r[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
 assert r['disposition']=='integrated'
 for target in r['targets']:assert (S/target).is_file(),target
outputs=json.loads((P/'run-output-manifest.json').read_text())['files']
for x in outputs:
 data=(P/x['file']).read_bytes();assert len(data)==x['bytes'] and sha(data)==x['sha256']
event=json.loads((P/'cyclic-replay-event.json').read_text())
assert event['original_main_runs']==1 and event['original_solve_calls']==event['original_LP_calls']==2
assert event['random_samples_generated']==event['additional_graph_solve_calls']==event['potential_84_point_rechecks']==0
assert sha((P/'replay_cyclic_entry.py').read_bytes())==event['checker_sha256']
calls=json.loads((P/'cyclic-two-solve-results.json').read_text())
assert len(calls)==2 and calls[0]['potential'] is False and calls[1]['potential'] is True
assert calls[0]['result']['success'] is False and calls[1]['result']['success'] is True and calls[1]['result']['exact_ok'] is True
assert calls[1]['result']['arc_support']==14 and len(calls[1]['result']['backgrounds'])==5
assert json.loads((P/'cyclic-original-main.stdout').read_text())==json.loads((P/'cyclic-current-report.json').read_text())
assert not (P/'cyclic-original-main.stderr').read_bytes() and not (P/'replay-wrapper.stderr').read_bytes()
layout=json.loads((P/'frozen-output-layout.json').read_text())
for x in layout['files']:
 data=(P/'original'/x['file']).read_bytes();render=json.dumps(json.loads(data),indent=2).encode()
 assert len(data)==x['frozen_bytes']==x['current_source_write_text_bytes']
 assert data==render and not data.endswith(b'\n')
 assert x['frozen_equals_current_serialization'] is True and x['frozen_ends_LF'] is False
pages=sorted((S/'archives/customer-attraction/state').rglob('*.md'))
assert len(pages)==3
links=0
for f in pages:
 s=f.read_text();assert s.startswith('---\n') and '\n---\n' in s
 front=s.split('---',2)[1]
 for key in ('id','kind','type_tag','title','status','summary','source_refs'):assert re.search(r'^'+key+r':',front,re.M),(f,key)
 assert s.count('\\[')==s.count('\\]') and s.count('\\(')==s.count('\\)')
 assert s.count('$')%2==0,f
 for line in s.splitlines():assert line==line.rstrip(),f
 for target in re.findall(r'\]\(([^)]+)\)',s):
  if target.startswith(('http:','https:','#','mailto:')):continue
  actual=(f.parent/target).resolve()
  if not actual.is_file():
   try:other=C/actual.relative_to(S)
   except ValueError:raise AssertionError((f,target))
   assert other.is_file(),(f,target)
  links+=1
for f in P.rglob('*.py'):ast.parse(f.read_text(),filename=str(f))
result={'kind':'static deliverable selfcheck; not a second mathematical execution',
 'passed':True,'source_count':6,'source_bytes':17553,'receipt_count':6,'formal_pages':3,
 'local_links_checked':links,'run_output_hashes_checked':len(outputs),
 'original_main_runs_in_saved_event':1,'original_LP_calls_in_saved_event':2,
 'new_source_imports':0,'new_LP_calls':0,'new_BI_calls':0,'new_random_samples':0,
 'static_checker_sha256':sha(Path(__file__).read_bytes())}
(P/'selfcheck-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
