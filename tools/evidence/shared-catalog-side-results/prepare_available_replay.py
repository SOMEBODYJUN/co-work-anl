from pathlib import Path
import json,hashlib
CACHE=Path(__file__).resolve().parents[1];RUN=Path(__file__).resolve().parent;ROOT=Path('/workspace/scratch/37f0f9248cfc/boss4-research');E=RUN/'evidence';OUT=E/'replay'
primary=json.loads((CACHE/'shared-catalog-side-results-candidate.json').read_text());by={x['path']:x for x in map(json.loads,(ROOT/'cleanup/inventory.jsonl').read_text().splitlines())}
related=['facility_spe/exact/bounded_overlap.py','facility_spe/exact/mitm.py','facility_spe/exact/__init__.py','facility_spe/__init__.py','facility_spe/local/__init__.py','facility_spe/cli/__init__.py'];manifest=[]
for name in [x['path'] for x in primary]+related:
 x=dict(by[name]);src=CACHE/name;recovered=False
 if not src.is_file():src=CACHE/'facility_spe/exact/__init__.py';recovered=True
 data=src.read_bytes();assert len(data)==x['size'] and hashlib.sha256(data).hexdigest()==x['sha256']
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);x.update(replay_path='tools/evidence/shared-catalog-side-results/replay/'+name,read_fully=True,role='claimed primary' if name in [y['path'] for y in primary] else 'related dependency, no completion receipt',canonical_recovery_from=str(src) if recovered else None);manifest.append(x)
(E/'replay-manifest.json').write_text(json.dumps({'scope':'Minimum canonical tree for offdiagonal solver and independent CLI probes; original full suites remain blocked by missing local/fixture dependencies','namespace_stubs_used':False,'source_bytes_modified':False,'files':manifest},ensure_ascii=False,indent=2)+'\n')
print('Preserved',len(manifest),'canonical files, including three init routes recovered by identical source SHA, no stub')
