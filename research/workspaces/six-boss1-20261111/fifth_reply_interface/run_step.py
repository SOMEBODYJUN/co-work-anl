"""Capture actual command, source, stdout/stderr and exit without touching Git."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    name = sys.argv[1]
    script = HERE/(name+'.py')
    assert script.is_file() and name != 'run_step'
    out = HERE/(name+'.stdout.txt');err = HERE/(name+'.stderr.txt')
    assert not out.exists() and not err.exists(), 'Do not overwrite an actual execution.'
    snap = HERE/'executed_sources';snap.mkdir(exist_ok=True)
    srcsha = sha(script)
    (snap/(name+'-'+srcsha+'.py')).write_bytes(script.read_bytes())
    command = [sys.executable,'-u',str(script)]
    start = time.time()
    with out.open('wb') as of,err.open('wb') as ef:
        result = subprocess.run(command,cwd=HERE,stdout=of,stderr=ef)
    manifest_path = HERE/'execution_manifest.json'
    old = json.loads(manifest_path.read_bytes()) if manifest_path.exists() else []
    record = {'command':command,'cwd':str(HERE),'source_sha256':srcsha,'exit_code':result.returncode,
              'elapsed_seconds':time.time()-start,'stdout':out.name,'stdout_sha256':sha(out),
              'stderr':err.name,'stderr_sha256':sha(err)}
    old.append(record)
    manifest_path.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
    print(out.read_text(),end='')
    if err.stat().st_size:
        print(err.read_text(),file=sys.stderr,end='')
    print(json.dumps(record,ensure_ascii=False))
    raise SystemExit(result.returncode)


if __name__=='__main__':
    main()
