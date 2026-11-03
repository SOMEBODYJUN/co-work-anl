import json,hashlib
from pathlib import Path
from coupled_d3 import Universe,D,m
from audit_root_copy_rows import check
cases=[check(ts,Universe,True) for ts in [[set()],[set(),{0},{0,1},{1,2}],[set(range(5)),{5},{6},{7},{8}],[{0,1},{1,2},{0,2,3},{3,4},{0,2,4}]]]
sources=[Path(__file__),Path(__file__).with_name('coupled_d3.py'),Path(m.__file__),Path(m.copies.__file__),Path(m.ap.__file__),Path(m.old.__file__)]
report={'sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'scope':'Selected complete ordered-history SPE replay, no universal pricing certificate.','status':'passed','cases':cases}
Path(__file__).with_name('audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'passed','cases':len(cases),'full_IC':sum(c['full_IC'] for c in cases),'rows':cases[-1]['rows']}))
