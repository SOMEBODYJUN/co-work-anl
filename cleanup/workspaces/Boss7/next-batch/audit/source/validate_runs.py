#!/usr/bin/env python3
from __future__ import annotations
import json, math, hashlib
from pathlib import Path
root=Path(__file__).parent
checks=[]
for name, expected_factor, expected_trace in [('factor25',2.5,278),('factor3',3.0,190)]:
    path=root/(name+'.json')
    data=json.loads(path.read_text())
    checks.append({'name':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':path.stat().st_size})
    assert data['status']=='floating discovery; no universal assertion'
    assert data['factor']==expected_factor
    assert data['full_histories']==43 and data['true_rows']==215
    assert len(data['root_backgrounds'])==2 and len(data['trace'])==expected_trace
    best=data['best']
    assert abs(best['factor'] if 'factor' in best else expected_factor)==expected_factor
    assert len(best['p'])==6 and abs(sum(best['p'])-1)<1e-10 and min(best['p'])>=-1e-10
    assert all(float(v)>=-1e-10 for v in best['weights'].values())
    assert abs(expected_factor*best['cap']-best['W']-best['gap'])<1e-9
    checks[-1].update(best={k:best[k] for k in ('start','iteration','W','cap','gap','p')},trace_len=len(data['trace']))
# Independent source replay of the existing discovery program; first line is exact best row.
replay=(root/'probe_replay.stdout').read_text().splitlines()
assert replay and json.loads(replay[0])['gap']==0.06250000000000011
out={'status':'finite-float-structure-validated','checks':checks,'probe_source_sha256':hashlib.sha256((root/'probe_root_cap.py').read_bytes()).hexdigest(),'probe_replay_lines':len(replay),'probe_best':json.loads(replay[0])}
(root/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
