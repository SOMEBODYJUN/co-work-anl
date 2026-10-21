import gzip,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from probe_bridges import probe,lib,ROOT
cases=json.load(gzip.open(ROOT/'evidence/certificates/customer_attraction/new_policy_security_cones.json.gz','rt'))['cases']
for d in cases:
 print('START',d['name'],d['players'],d['topics'],flush=True)
 acts={tuple(x['history']):x['action'] for x in d['policy']}
 probe(lib.StrategyCone(d['topics'],d['players'],acts),d['name'])
