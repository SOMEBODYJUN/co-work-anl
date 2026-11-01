"""Preserve one default original invocation in a fresh isolated directory."""
import argparse,hashlib,json,platform,shutil,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
import numpy,scipy
SOURCE_SHA='7e64a94c046218e553d6a30a9367bb109dfa3cfc208122e528fc6693321f30d2'
FROZEN_SHA='390eed8d1f1755881dc5afff4d20e3c275ec9313950897450a44c72e5766755b'
def fingerprint(p):
    raw=p.read_bytes()
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--out-dir',type=Path,required=True)
    args=ap.parse_args();source=args.source.resolve();out=args.out_dir.resolve()
    assert fingerprint(source)['sha256']==SOURCE_SHA
    out.mkdir(parents=True,exist_ok=False)
    script=out/'fresh_cover_cost_certificate.py';shutil.copyfile(source,script)
    before=fingerprint(script);start=datetime.now(timezone.utc).isoformat();clock=time.perf_counter()
    command=[sys.executable,'-B',str(script)]
    proc=subprocess.run(command,cwd=out,capture_output=True,timeout=120)
    elapsed=time.perf_counter()-clock
    (out/'stdout.txt').write_bytes(proc.stdout);(out/'stderr.txt').write_bytes(proc.stderr)
    report=out/'fresh_cover_cost_2.json'
    data=json.loads(report.read_bytes()) if report.exists() else None
    files={p.name:fingerprint(p) for p in sorted(out.iterdir()) if p.is_file()}
    record={'command':command,'cwd':str(out),'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'duration_seconds':elapsed,'timeout_seconds':120,'returncode':proc.returncode,'versions':{'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__},'source_before':before,'source_after':fingerprint(script),'files':files,'report':data,'original_script_invocations':1,'original_linprog_calls':1,'tau':'2 (source CLI default; no argument supplied)','source_matrix_shape':[192,24],'original_success_branch_executed':False,'other_parameter_original_runs':0,'frozen_report_sha256':FROZEN_SHA,'new_report_equals_frozen_bytes':report.exists() and fingerprint(report)['sha256']==FROZEN_SHA}
    (out/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
    assert proc.returncode==0 and not proc.stderr and before==fingerprint(script)
    assert data=={'tau':'2','success':False,'message':'The problem is infeasible. (HiGHS Status 8: model_status is Infeasible; primal_status is None)'}
    assert record['new_report_equals_frozen_bytes'] and proc.stdout==report.read_bytes()
    print(json.dumps(record,indent=2))
if __name__=='__main__':main()
