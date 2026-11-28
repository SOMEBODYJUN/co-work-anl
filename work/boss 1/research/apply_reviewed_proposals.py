"""Apply only the independently reviewed bytes, sequentially through work.py."""
from pathlib import Path
import json,hashlib,subprocess
W=Path(__file__).resolve().parents[1]; ROOT=W.parents[1]; R=W/'research'
receipt=R/'tasks/research_independent_review/proposal_receipt.json'
review=json.loads(receipt.read_text()); reviews={x['id']:x for x in review['reviews']}
packfile=R/'audit_proposal_pack.json';pack=json.loads(packfile.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(packfile)==review['pack_sha256']
base=[str(ROOT/'.venv-methods/bin/python'),str(ROOT/'work.py'),'--workspace',str(W)]
logs=[]
for p in pack['proposals']:
 f=R/'proposals'/f'{p["id"]}.json'; x=reviews[p['id']]
 assert x['verdict']=='pass' and x['target']==p['target'] and sha(f)==x['file_sha256']
 for args in [ ['proposal','--file',str(f)], ['proposal-review','--id',p['id'],'--verdict','pass','--reviewer',review['reviewer'],'--note',x['note']+' 独立实读回执：research/tasks/research_independent_review/proposal_receipt.json SHA256 '+sha(receipt)], ['apply','--id',p['id']] ]:
  z=subprocess.run(base+args,cwd=ROOT,capture_output=True,text=True)
  if z.returncode: print(z.stdout,z.stderr); raise SystemExit(z.returncode)
  logs.append({'command':args[:1]+(['--id',p['id']] if args[0]!='proposal' else []),'result':json.loads(z.stdout)})
 print(p['id'],p['target'],'applied',flush=True)
(R/'receipts/proposals_applied.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
z=subprocess.run(base+['graph-status'],cwd=ROOT,capture_output=True,text=True)
if z.returncode: print(z.stdout,z.stderr);raise SystemExit(z.returncode)
g=json.loads(z.stdout);(R/'receipts/graph_status_after_audit.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
s=json.loads((W/'research_state.json').read_text())
(R/'graph_current.json').write_text(json.dumps({'revision':s['revision'],'nodes':list(s['nodes'].values()),'edges':list(s['edges'].values())},ensure_ascii=False,indent=2)+'\n')
print('unresolved',g['unresolved'],g['unresolved_edges'],'revision',s['revision'])
