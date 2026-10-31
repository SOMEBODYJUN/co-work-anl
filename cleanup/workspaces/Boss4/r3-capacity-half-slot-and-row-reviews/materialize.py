from pathlib import Path
import hashlib,json,subprocess
repo=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
cache=repo.parent/'boss4-next-cache'
stage=cache/'r3-capacity-half-slot-and-row-reviews'
ev=stage/'archives/unrelated-machines/tools/evidence/capacity-half-slot-and-row-reviews'
inv={x['id']:x for x in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())}
items=[('698bdcab0669d55a1efa','original'),('3366609734cf33d87e19','original'),('c76da606d8c2e7e8fe35','original'),('1f64a487c666cbeb751d','original'),('8c90fcce237d7988a7a5','comparisons'),('8880cf5284ef95a424b1','comparisons'),('8e7fbfe13b8dcfeb9ec6','comparisons'),('e024705ef6909102d311','historical-runs'),('12b601da50cee4eab718','historical-runs'),('292abbaeaee297858760','historical-runs'),('99fabfaf306e1766cd1e','historical-runs'),('fad6c1261ebf89ea2271','historical-runs'),('26338f459180608ece93','dependencies'),('4ac60b67eeb6e0760426','dependencies'),('010e62eecd902e6e97b5','dependencies'),('357bed819f77ccb983f1','dependencies'),('8b7bf377eea33a7333c6','dependencies'),('a1d8cc0d5e532a980090','dependencies')]
records=[]
for sid,category in items:
 e=inv[sid]; dest=ev/category/Path(e['path']).name; dest.parent.mkdir(parents=True,exist_ok=True)
 candidates=list(cache.rglob(dest.name))+list((repo/'archives/unrelated-machines/tools/evidence').rglob(dest.name))
 match=next((p for p in candidates if p!=dest and p.is_file() and p.stat().st_size==e['size'] and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']),None)
 if match: data=match.read_bytes();how='verified existing frozen cache';origin=str(match)
 else:
  p=subprocess.run(['python','work.py','clean','show',sid],cwd=repo,capture_output=True,check=True)
  data=p.stdout;how='read-only work.py clean show';origin=sid
 assert len(data)==e['size'] and hashlib.sha256(data).hexdigest()==e['sha256'],(sid,len(data))
 dest.write_bytes(data)
 records.append({'id':sid,'primary':category=='original','path':e['path'],'sha256':e['sha256'],'size':e['size'],'sources':e['sources'],'materialization':how,'local_origin':origin,'target':str(dest.relative_to(stage))})
(ev/'manifest.json').write_text(json.dumps({'claim_commit':'4062d709a9b0b600597ed94cf4dbd33dfc647b41','source_freeze':'68fad804ec5946cb296f77dc5b336308a66abf12','records':records},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'materialized':len(records),'primary':sum(r['primary'] for r in records)},ensure_ascii=False))
