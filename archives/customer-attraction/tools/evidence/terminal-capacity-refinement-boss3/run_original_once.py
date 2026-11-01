"""One original --capacity --verify event, in a fresh external directory."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    repo,runtime=map(lambda x:Path(x).resolve(),sys.argv[1:3])
    runtime.mkdir(parents=True,exist_ok=False)
    shared=json.loads((repo/'archives/customer-attraction/tools/evidence/combined-branch-master-program/source-manifest.json').read_text())
    inputs=[]
    for rec in shared['frozen_sources']:
        src=repo/rec['stored_path'];assert src.stat().st_size==rec['size'] and sha(src)==rec['sha256']
        dest=runtime/rec['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
        inputs.append({**rec,'materialization_role':'shared available dependency'})
    related=json.loads((HERE/'related-inputs-manifest.json').read_text())['sources']
    own=json.loads((HERE/'source-manifest.json').read_text())['sources']
    for rec in related+own:
        src=(HERE/'related'/Path(rec['path']).name) if 'retained_related_path' in rec else (HERE/'original'/rec['id']/Path(rec['path']).name)
        dest=runtime/rec['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
        assert sha(dest)==rec['sha256'];inputs.append({**rec,'materialization_role':'prior completed input' if rec in related else 'new two-source batch'})
    (runtime/'work.py').write_text('# Root-location marker only, no executable behavior.\n')
    before={r['path']:sha(runtime/r['path']) for r in inputs}
    script=next(runtime/r['path'] for r in related if r['id']=='b4dd5c92d5e5f049779e')
    argv=[sys.executable,'-B',str(script),'--capacity','--verify']
    start_utc=datetime.now(timezone.utc).isoformat();start=time.monotonic()
    result=subprocess.run(argv,cwd=runtime,input=b'',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    elapsed=time.monotonic()-start
    runs=HERE/'runs';runs.mkdir(exist_ok=True)
    (runs/'original.stdout').write_bytes(result.stdout);(runs/'original.stderr').write_bytes(result.stderr)
    after={r['path']:sha(runtime/r['path']) for r in inputs}
    record=dict(start_utc=start_utc,argv=argv,cwd=str(runtime),elapsed_seconds=elapsed,
        exit_code=result.returncode,stdout_bytes=len(result.stdout),stderr_bytes=len(result.stderr),
        input_manifest_entries=len(inputs),unique_materialized_input_files=len(before),
        materialized_inputs_unchanged=before==after,inputs=inputs,
        capacity_verifier_executions=1,default_verifier_executions=0,LP_or_discovery_executions=0,
        scope='one original 5112-row finite necessary-system verification; available inputs are not an import log')
    (runs/'original-execution.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    assert result.returncode==0 and not result.stderr and before==after
    print(json.dumps({k:v for k,v in record.items() if k!='inputs'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
