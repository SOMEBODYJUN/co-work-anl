#!/usr/bin/env python3
"""Fixed inputs from the frozen diagnostics; no random-search CLI invocation."""
from pathlib import Path
from math import comb
import runpy,json,time,gc,hashlib
P=Path(__file__).resolve().parent
solve=runpy.run_path(str(P/'original/cartesian_scout.py'))['solve']
expected=json.loads((P/'original/finite_component_diagnostics.json').read_bytes())
reports=[];events=[];start=time.perf_counter()
for n in range(2,14):
 t0=time.perf_counter();m=n+2;b=3*n;s=2*n;d=3
 weights=((2*b-d,b,b*n),(s,s*(n+1),s))
 report,root=solve(weights,m)
 report['design_target_feasible']=((2,0,n),(1,n,1)) in root
 factors=[solve((w,),m)[0] for w in weights]
 report['component_reports']=factors
 report['component_minimum_sum']=sum(x['W'] for x in factors)
 report['amplification_deficit']=report['component_minimum_sum']-report['W']
 # JSON normalization is necessary only for Python tuple/list representation.
 normalized=json.loads(json.dumps(report))
 assert normalized==expected['reports'][n-2],n
 assert report['states']==sum(comb(t+2,2)**2 for t in range(m+1))
 assert all(x['states']==comb(m+3,3) for x in factors)
 reports.append(report)
 event={'n':n,'m':m,'joint_states':report['states'],'root_outcomes':len(root),'wall_seconds':time.perf_counter()-t0}
 events.append(event);print(json.dumps(event),flush=True)
 del root;gc.collect()
output={'finite_scope_only':True,'reports':reports}
data=(json.dumps(output,indent=2)+'\n').encode()
(P/'replayed_finite_component_diagnostics.json').write_bytes(data)
assert data==(P/'original/finite_component_diagnostics.json').read_bytes()
report={'run_kind':'one deterministic wrapper; 12 joint plus 24 one-component solve calls; random CLI not invoked','wall_seconds':time.perf_counter()-start,'source_calls':36,'cases':12,'byte_exact':True,'sha256':hashlib.sha256(data).hexdigest(),'per_case':events}
(P/'finite-components-event.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='per_case'}),flush=True)
