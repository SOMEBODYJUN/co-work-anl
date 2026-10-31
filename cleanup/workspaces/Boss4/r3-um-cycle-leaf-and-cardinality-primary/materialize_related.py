from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess
repo=Path('/workspace/scratch/37f0f9248cfc/boss4-research');stage=repo.parent/'boss4-next-cache/r3-um-cycle-leaf-and-cardinality-primary';ev=Path('archives/unrelated-machines/tools/evidence/um-cycle-leaf-and-cardinality-primary');inv={e['id']:e for e in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())}
items=[('528f36466ffc7a22d79e','historical-runs'),('36d3133766908eeb048b','historical-runs'),('409bcd01bd377010b36d','historical-runs'),('e7c981ac171cf2eb2260','historical-runs'),('a36b4eba229032d2fb63','historical-runs'),('86039e74710aa9d97bf7','historical-runs'),('662f60ef16911ee431c3','comparisons'),('1a2d2e45fa8015a84abd','comparisons'),('6a74907a52db2f958ba5','comparisons'),('288001c1e251d3af65d7','comparisons'),('e3bf2fef1967903a2e65','comparisons'),('c36affbedf5dbbdc82cf','comparisons'),('2c9423076f733f78f201','comparisons')]
byname={}
for root in [repo.parent/'boss4-next-cache',repo/'archives',repo/'tools']:
 for p in root.rglob('*'):
  if p.is_file():byname.setdefault(p.name,[]).append(p)
def one(item):
 sid,cat=item;e=inv[sid];dest=stage/ev/cat/Path(e['path']).name;dest.parent.mkdir(parents=True,exist_ok=True);candidates=byname.get(dest.name,[])+byname.get(sid+'.raw',[])+byname.get(sid+'.md',[])
 match=next((p for p in candidates if p!=dest and p.stat().st_size==e['size'] and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']),None)
 if match:data=match.read_bytes();how='verified existing frozen bytes';origin=str(match)
 else:
  p=subprocess.run(['python','work.py','clean','show',sid],cwd=repo,capture_output=True,check=True);data=p.stdout;how='read-only work.py clean show';origin=sid
 assert len(data)==e['size'] and hashlib.sha256(data).hexdigest()==e['sha256'];dest.write_bytes(data)
 return {'id':sid,'primary':False,'path':e['path'],'sha256':e['sha256'],'size':e['size'],'sources':e['sources'],'evidence_path':str(dest.relative_to(stage)),'materialization':how,'local_origin':origin}
with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(one,items))
p=stage/ev/'manifest.json';m=json.loads(p.read_text());m['records']+=rows;p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print({'related_originals':len(rows)})
