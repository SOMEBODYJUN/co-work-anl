"""One unchanged pure-stdlib independent original entry, exact saved data only.

Refuse an existing execution record. No author60-class, threshold, graph,
optimizer or SPE entry is called. ROOT is the original fixed parents[5].
"""
from datetime import datetime, timezone
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import json
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
MAIN='research/workspaces/customer-attraction/R-d0dc7461ada541a5a2ab9a2b8ad4e623/strategy/independent_zz_bound.py'

def digest(p):return sha256(p.read_bytes()).hexdigest()

def main():
    for name in ['execution.json','stdout.json','stderr.txt']:
        if (HERE/name).exists():raise SystemExit('Existing run output; refusing a repeat execution: '+name)
    inputs=[]
    for x in json.loads((HERE/'source-manifest.json').read_text()):
        p=HERE/'source-root'/x['path'];assert p.stat().st_size==x['size'] and digest(p)==x['sha256'];inputs.append(dict(path=x['path'],size=x['size'],sha256=x['sha256']))
    deps=json.loads((HERE/'runtime-input-manifest.json').read_text())
    for x in deps:
        p=HERE/x['runtime_path'];assert p.stat().st_size==x['size'] and digest(p)==x['sha256']
    command=[sys.executable,'-I','-B',str(HERE/'source-root'/MAIN)]
    start=datetime.now(timezone.utc).isoformat();clock=time.perf_counter()
    p=subprocess.run(command,cwd=HERE/'source-root',capture_output=True)
    elapsed=time.perf_counter()-clock;finish=datetime.now(timezone.utc).isoformat()
    (HERE/'stdout.json').write_bytes(p.stdout);(HERE/'stderr.txt').write_bytes(p.stderr)
    event=dict(scope='one unchanged4433B independent main; only strongest unrestricted fixed-marginal class; no author60-class run or graph/LP/SPE',argv=command,cwd=str(HERE/'source-root'),started_utc=start,finished_utc=finish,elapsed_seconds=elapsed,exit_code=p.returncode,python=sys.version,assertions_enabled=__debug__,original_independent_main_calls=1,original_author_main_calls=0,old_3889_verifier_calls=0,lp_calls=0,spe_solver_calls=0,primary_sources=inputs,runtime_dependencies=deps,stdout_bytes=len(p.stdout),stdout_sha256=digest(HERE/'stdout.json'),stderr_bytes=len(p.stderr),stderr_sha256=digest(HERE/'stderr.txt'))
    (HERE/'execution.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
    if p.returncode:raise SystemExit(p.returncode)
    result=json.loads(p.stdout)
    frozen=json.loads((HERE/'source-root/research/workspaces/customer-attraction/R-d0dc7461ada541a5a2ab9a2b8ad4e623/strategy/zz_bound_exact.json').read_text())
    assert Fraction(result['unrestricted_joint_upper_bound'])==Fraction(frozen['unrestricted_pairwise_upper_bounds']['minimum_upper_bound'])<0
    for x in inputs:assert digest(HERE/'source-root'/x['path'])==x['sha256']
    for x in deps:assert digest(HERE/x['runtime_path'])==x['sha256']
    (HERE/'post-run-binding.json').write_text(json.dumps(dict(status='MATCHES_SAVED_STRONGEST_CLASS_WITH_IDENTICAL_INPUT',source_sha256=result['source_sha256'],result=result,unchanged_original_bytes=True,comparison='one source_family0/query_family1/pattern0102, not other three broad bounds or all60 rows',independent_vs_author_report_equal=True),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(exit_code=p.returncode,elapsed_seconds=elapsed,stdout_bytes=len(p.stdout),stderr_bytes=len(p.stderr),result=result),ensure_ascii=False))
if __name__=='__main__':main()
