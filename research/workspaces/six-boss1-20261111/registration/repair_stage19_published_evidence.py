"""Publish a text-equivalent draft copy while preserving every pinned old byte.

The map published-input gate correctly rejected an attachment available only
after local gzip restoration.  Give the same prose a normal portable text
entry, change only its owning object's evidence/version, and rebind affected
edges with the repository's own complete validation functions.
"""
from pathlib import Path
from hashlib import sha256
import copy
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
W=HERE.parent
R=W.parents[2]
CID='customer-attraction/six-providers/cross-branch-necessary-system-20261111'
old_path=str((HERE/'stage19-gamma36-addition.md').relative_to(R))
new_path=str((HERE/'stage19-gamma36-addition-published.md').relative_to(R))
target=HERE/'stage19-published-evidence-registry.json'
assert not target.exists() and not (R/new_path).exists()
raw=(R/old_path).read_bytes()
assert raw.endswith(b'\n\n') and not raw.endswith(b'\n\n\n')
portable=raw[:-1]
assert portable.splitlines()==raw.splitlines()[:-1]
(R/new_path).write_bytes(portable)
reg=json.loads((R/'research/registry.json').read_text());before=copy.deepcopy(reg)
objects={o['object_id']:o for o in reg['objects']};obj=objects[CID]
assert obj['version']==14
matches=[x for x in obj['evidence'] if x['path']==old_path];assert len(matches)==1
assert matches[0]['sha256']==sha256(raw).hexdigest()
matches[0].update(path=new_path,sha256=sha256(portable).hexdigest())
obj['sources']=[('material:'+new_path if s=='material:'+old_path else s) for s in obj['sources']]
obj['version']=15
materials=[m for m in reg['materials'] if m['path']==old_path];assert len(materials)==1
assert materials[0]['object_ids']==[CID]
materials[0].update(path=new_path,sha256=sha256(portable).hexdigest())
materials[0]['reason']+=' 同文发布副本仅去除多余EOF空行；原草稿SHA及无损gzip仍保存于Stage19c历史。'
assert [o for o in reg['objects'] if o['object_id']!=CID]==[o for o in before['objects'] if o['object_id']!=CID]
assert reg['edge_files']==before['edge_files']
target.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
record={'status':'TEXT_EQUIVALENT_PUBLISHED_EVIDENCE_REPAIR','reason':'Map plan rejected a required published evidence path absent from the committed tree. Local restoration alone is not the publication contract.',
 'old_ref':{'path':old_path,'sha256':sha256(raw).hexdigest(),'restoration_manifest':str((W/'portable_frozen_text_stage19c_eof/manifest.json').relative_to(R))},
 'new_ref':{'path':new_path,'sha256':sha256(portable).hexdigest()},
 'byte_difference':'Remove exactly one final LF from an unaltered historical draft copy; all prose/math lines equal.',
 'unchanged':['canonical computation body','all numerical certificates','all frozen sources','all other objects'],
 'object_id':CID,'old_version':14,'new_version':15,'prior_published_commit':'dac0622b344556cddfbee2a1e1aabab321b780e2'}
(HERE/'stage19-published-evidence-repair.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
p=subprocess.run(['python','work.py','research','register','--record-file',str(target.relative_to(R))],cwd=R,capture_output=True,text=True)
(HERE/'stage19-published-evidence-register.stdout.json').write_text(p.stdout)
(HERE/'stage19-published-evidence-register.stderr.txt').write_text(p.stderr)
assert p.returncode==0,p.stderr
registered=json.loads((R/'research/registry.json').read_text());assert registered==reg
sys.path.insert(0,str(R/'tools'))
import research_runtime as runtime
objects={o['object_id']:o for o in registered['objects']}
affected=[]
for path in sorted((R/'map/edges/six-boss1-20261111').glob('*.json')):
 edge=json.loads(path.read_text())
 if CID not in edge['source_ids']+edge['target_ids']:continue
 assert not any(r['path']==old_path for r in edge['evidence'])
 edge['review_note']+=' 计算v15仅改同文证据的可发布入口；承重正文和数学范围不变，原空行草稿精确SHA仍保留。'
 edge.update(runtime.edge_bindings(R,edge,objects,verify=True))
 path.write_text(json.dumps(edge,ensure_ascii=False,indent=2)+'\n')
 affected.append(str(path.relative_to(R)))
assert len(affected)==8
checked=runtime.edges(R,{'edge_files':affected},objects,verify=True)
assert len(checked)==8
result={'status':'PASS_REPOSITORY_EDGE_BINDINGS_AND_EDGE_VALIDATION','implementation':'tools.research_runtime.edge_bindings and edges, verify=True (the CLI implementation)',
        'affected_edges':affected,'validated_edges':len(checked),'new_computation_pin':runtime.pin(objects[CID]),
        'registry_sha256':sha256((R/'research/registry.json').read_bytes()).hexdigest(),'all_other_objects_unchanged':True}
(HERE/'stage19-published-evidence-edge-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
p=subprocess.run(['python','work.py','research','show',CID],cwd=R,capture_output=True,text=True)
(HERE/'stage19-show-computation-v15.stdout.json').write_text(p.stdout)
(HERE/'stage19-show-computation-v15.stderr.txt').write_text(p.stderr)
assert p.returncode==0 and json.loads(p.stdout)['registration_pin']==result['new_computation_pin']
print(json.dumps(result,ensure_ascii=False),flush=True)
