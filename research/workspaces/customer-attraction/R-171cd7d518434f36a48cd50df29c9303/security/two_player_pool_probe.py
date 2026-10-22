"""Exhaust all 3-topic two-player formal policies, local p numerical attack."""
from itertools import product
import json
from pathlib import Path
from pool_probe import build,probe
HERE=Path(__file__).resolve().parent
best=None
for serial,choices in enumerate(product(range(3),repeat=4)):
    actions={():choices[0],**{(a,):choices[a+1] for a in range(3)}}
    G,c,mem,H,full,z=build(actions,2,3)
    rec=probe(G,c,mem,H,2,serial+9171,starts=3)
    rec.update(serial=serial,choices=choices,on_path=z)
    if best is None or rec['ratio']>best['ratio']+1e-9:
        best=rec;print(json.dumps(best),flush=True)
    if rec['ratio']>1+1e-7:break
(HERE/'two_player_pool_report.json').write_text(json.dumps(dict(policies_checked=serial+1,status='finite floating discovery only',best=best),indent=2)+'\n')
