from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess
repo=Path('/workspace/scratch/37f0f9248cfc/boss4-research');stage=repo.parent/'boss4-next-cache/r3-um-following-audit-primary';ev=stage/'archives/unrelated-machines/tools/evidence/um-following-audit-primary'
cap=json.loads((repo.parent/'boss4-r3-next15aa-claim.json').read_text());ids=['d5a14149ab0edb517bc1','8db8d8577400f86d0b4e','e92ad715a0c9aff7de17','122e8b2a473d0aeaf6d8','3cb3475471e5beaf4e40'];assert cap['status']=='pushed' and cap['actor']=='Boss4' and set(ids)<=set(cap['ids'])
inv={e['id']:e for e in map(json.loads,(repo/'cleanup/inventory.jsonl').read_text().splitlines())}
# Frozen inventory data and current related mathematical texts, with outputs kept in their actual named layout.
compnames=['cartesian_menu_recoupling_and_coordinate_consistency.md','dual_rail_threshold_soundness_boundary.md','bounded_collision_label_resource_floor.md','cartesian_menu_reverse_amplification_review.md','dual_rail_threshold_soundness_boundary_review.md','bounded_collision_label_floor_review.md','pairwise_label_resource_floor.json']
items=[(sid,'original') for sid in ids]
for name in compnames:
 es=[e for e in inv.values() if Path(e['path']).name==name]
 assert len(es)==1,(name,es);items.append((es[0]['id'],'comparisons' if name.endswith('.md') else 'historical-runs'))
for sid in ['2fbfc0ca1d7366227c6e','9e050980899db202ae93']:items.append((sid,'historical-runs'))
for e in inv.values():
 if 'evidence/runs/unrelated_machines/cartesian_menu_reverse_v1/' in e['path']:items.append((e['id'],'historical-runs/cartesian_menu_reverse_v1'))
# Indexed cache lookup avoids re-exporting byte-identical existing originals.
allpaths=list((repo.parent/'boss4-next-cache').rglob('*'))+list((repo/'archives').rglob('*'))+list((repo/'tools').rglob('*'));byname={}
for p in allpaths:
 if p.is_file():byname.setdefault(p.name,[]).append(p)
def one(item):
 sid,category=item;e=inv[sid];dest=ev/category/Path(e['path']).name;dest.parent.mkdir(parents=True,exist_ok=True)
 # Some original evidence is stored as <ID>.raw/json; allow exact ID lookup as well.
 cand=byname.get(dest.name,[])+byname.get(sid+'.raw',[])+byname.get(sid+'.json',[])
 match=next((p for p in cand if p!=dest and p.stat().st_size==e['size'] and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']),None)
 if match:data=match.read_bytes();method='verified existing frozen bytes';origin=str(match)
 else:
  p=subprocess.run(['python','work.py','clean','show',sid],cwd=repo,capture_output=True,check=True);data=p.stdout;method='read-only work.py clean show';origin=sid
 assert len(data)==e['size'] and hashlib.sha256(data).hexdigest()==e['sha256'],(sid,len(data));dest.write_bytes(data)
 return {'id':sid,'primary':sid in ids,'path':e['path'],'sha256':e['sha256'],'size':e['size'],'sources':e['sources'],'evidence_path':str(dest.relative_to(stage)),'materialization':method,'local_origin':origin}
# Primary actual source acquisition independent; each target is a distinct file.
with ThreadPoolExecutor(max_workers=3) as pool:records=list(pool.map(one,items))
(ev/'manifest.json').write_text(json.dumps({'claim_status':cap['status'],'actor':cap['actor'],'claim_tip':cap['remote_tip'],'primary_ids':ids,'records':records},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_files':len(records),'primary':len(ids),'claim_tip':cap['remote_tip']},ensure_ascii=False))
