#!/usr/bin/env python3
"""Run the frozen complete-policy CLI exactly once, then compare both reports."""
from pathlib import Path
import subprocess,sys,json,time,hashlib
P=Path(__file__).resolve().parent
out=P/'replayed_coupled_cartesian_padding_audit.json'
command=[sys.executable,str(P/'original/verify_coupled_cartesian.py'),'--max-n','9','--output',str(out)]
t0=time.perf_counter()
r=subprocess.run(command,cwd=P,capture_output=True)
elapsed=time.perf_counter()-t0
(P/'complete-policy.stdout').write_bytes(r.stdout)
(P/'complete-policy.stderr').write_bytes(r.stderr)
assert r.returncode==0, (r.returncode,r.stderr.decode())
data=out.read_bytes(); got=json.loads(data)
old=json.loads((P/'original/coupled_cartesian_audit.json').read_bytes())
projected={k:v for k,v in got.items()}
projected['reports']=[{k:v for k,v in x.items() if k not in ('safe_padded_OPT','safe_padded_ratio')} for x in got['reports']]
projdata=(json.dumps(projected,indent=2)+'\n').encode()
(P/'replayed_pre_padding_projection.json').write_bytes(projdata)
assert data==(P/'original/coupled_cartesian_padding_audit.json').read_bytes()
assert projected==old and projdata==(P/'original/coupled_cartesian_audit.json').read_bytes()
report={'run_kind':'one original CLI invocation; projection performs no second audit','command':command,'cwd':str(P),'returncode':r.returncode,'wall_seconds':elapsed,'padding_byte_exact':True,'old_projection_byte_exact':True,'cases':len(got['reports']),'dag_nodes_total':sum(x['dag_nodes'] for x in got['reports']),'global_comparisons_total':sum(x['global_comparisons'] for x in got['reports']),'factor_comparisons_total':sum(x['factor_comparisons'] for x in got['reports']),'output_sha256':hashlib.sha256(data).hexdigest()}
(P/'complete-policy-event.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
