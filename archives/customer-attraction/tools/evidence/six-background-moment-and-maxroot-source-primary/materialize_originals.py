#!/usr/bin/env python3
"""Copy declared original bytes into a NEW directory; executes no research code.

This prepares the 39-source relative tree and the two declared parent files.
The fixed_graph/LP old587 dependency closure is intentionally NOT supplied.
"""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
assert not a.out.exists(), 'Use a new directory; never overwrite a prior runtime'
here=Path(__file__).resolve().parent
m=json.loads((here/'source-manifest.json').read_text());deps=json.loads((here/'dependency-manifest.json').read_text())
records=[]
for x in m:
 rel=Path(x['path']).relative_to('research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba')
 records.append((x['preserved_at'],rel,x['sha256']))
for x in deps:
 if x['role'].startswith('prior A3'):
  records.append((x['path'],Path('parent')/Path(x['path']).name,x['sha256']))
# Read and verify every source before creating or writing the new directory.
prepared=[]
for src,rel,sha in records:
 raw=(a.repo/src).read_bytes();assert hashlib.sha256(raw).hexdigest()==sha,(src,sha);prepared.append((rel,raw))
a.out.mkdir(parents=True)
for rel,raw in prepared:
 target=a.out/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
print(json.dumps({'copied_original_files':len(prepared),'research_code_executed':0,'out':str(a.out.resolve()),'missing_fixed_graph_old587_closure':True}))
