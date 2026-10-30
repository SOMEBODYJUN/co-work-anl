from pathlib import Path
import json,hashlib,shutil
CACHE=Path(__file__).resolve().parents[1];RUN=Path(__file__).resolve().parent;ROOT=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=RUN/'evidence';REPLAY=E/'replay'
primary=json.loads((CACHE/'shared-catalog-side-results-candidate.json').read_text())
related=['facility_spe/__init__.py','facility_spe/local/__init__.py','facility_spe/exact/__init__.py','facility_spe/cli/__init__.py','facility_spe/local/pure.py','facility_spe/local/strong_chord.py','facility_spe/exact/bounded_overlap.py','facility_spe/exact/mitm.py','examples/shared/tiny.json','examples/shared/on_path_chord.json','examples/shared/sharp_lower_rational.json','examples/shared/sparse_four_rational.json','evidence/certificates/shared/tiny_phi.json','evidence/certificates/shared/on_path_chord.json','evidence/certificates/shared/sharp_lower_rational.json']
by={x['path']:x for x in map(json.loads,(ROOT/'cleanup/inventory.jsonl').read_text().splitlines())}
missing=[p for p in related if not (CACHE/p).is_file()]
if missing:raise RuntimeError('Missing canonical dependencies: '+repr(missing))
manifest=[]
for name in [x['path'] for x in primary]+related:
 x=dict(by[name]);data=(CACHE/name).read_bytes();assert len(data)==x['size'] and hashlib.sha256(data).hexdigest()==x['sha256'];out=REPLAY/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
 x['role']='claimed primary' if name in [z['path'] for z in primary] else 'related read/execution dependency; no completion receipt';x['replay_path']='tools/evidence/shared-catalog-side-results/replay/'+name;manifest.append(x)
(E/'replay-manifest.json').write_text(json.dumps({'namespace_stubs_used':False,'source_bytes_modified':False,'files':manifest},ensure_ascii=False,indent=2)+'\n')
print('Prepared',len(primary),'primary and',len(related),'related canonical files; no altered source or stub')
