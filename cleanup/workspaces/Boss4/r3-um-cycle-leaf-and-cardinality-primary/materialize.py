from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess
repo=Path('/workspace/scratch/37f0f9248cfc/boss4-research');stage=repo.parent/'boss4-next-cache/r3-um-cycle-leaf-and-cardinality-primary';ev=stage/'archives/unrelated-machines/tools/evidence/um-cycle-leaf-and-cardinality-primary'
cap=json.loads((repo.parent/'boss4-r3-next9ag-claim.json').read_text());ids=['366efae229e35047de7f','14c27eb4d50f284464fa','5b9b83fcae1bb3c91099','4a1b8fc533696fbb6811','b99a62dba759d15bdc1e'];assert cap['status']=='pushed' and cap['actor']=='Boss4' and set(ids)<=set(cap['ids'])
inv={e['id']:e for e in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())};byname={}
for root in [repo.parent/'boss4-next-cache',repo/'archives',repo/'tools']:
 for p in root.rglob('*'):
  if p.is_file():byname.setdefault(p.name,[]).append(p)
def one(sid):
 e=inv[sid];dest=ev/'original'/Path(e['path']).name;dest.parent.mkdir(parents=True,exist_ok=True);candidates=byname.get(dest.name,[])+byname.get(sid+'.raw',[])
 match=next((p for p in candidates if p!=dest and p.stat().st_size==e['size'] and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']),None)
 if match:data=match.read_bytes();how='verified existing frozen cache';origin=str(match)
 else:
  p=subprocess.run(['python','work.py','clean','show',sid],cwd=repo,capture_output=True,check=True);data=p.stdout;how='read-only work.py clean show';origin=sid
 assert len(data)==e['size'] and hashlib.sha256(data).hexdigest()==e['sha256'];dest.write_bytes(data)
 return {'id':sid,'primary':True,'path':e['path'],'sha256':e['sha256'],'size':e['size'],'sources':e['sources'],'evidence_path':str(dest.relative_to(stage)),'materialization':how,'local_origin':origin}
with ThreadPoolExecutor(max_workers=3) as pool:records=list(pool.map(one,ids))
(ev/'manifest.json').write_text(json.dumps({'claim_capture':'/workspace/scratch/37f0f9248cfc/boss4-r3-next9ag-claim.json','claim_status':cap['status'],'actor':cap['actor'],'claim_tip':cap['remote_tip'],'local_sync':cap['local_sync']['status'],'primary_ids':ids,'records':records},ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{'id':r['id'],'size':r['size'],'path':r['path']} for r in records],ensure_ascii=False))
