"""Execute one named local step and retain actual bytes, output, and exit code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    name = sys.argv[1]
    path = HERE/(name+'.py')
    assert path.exists() and '/' not in name
    manifests = HERE/'execution_manifest.json'
    records = json.loads(manifests.read_text()) if manifests.exists() else []
    run = sum(r['step'] == name for r in records)+1
    stem = f'{len(records)+1:02d}-{name}-{run}'
    saved = HERE/'executed_sources'
    saved.mkdir(exist_ok=True)
    snapshot = saved/(name+'-'+sha(path)+'.py')
    snapshot.write_bytes(path.read_bytes())
    argv = [sys.executable, '-B', str(path), *sys.argv[2:]]
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
    start = datetime.now(timezone.utc).isoformat()
    t = time.perf_counter()
    with open(HERE/(stem+'.stdout.txt'), 'w') as stdout, open(HERE/(stem+'.stderr.txt'), 'w') as stderr:
        result = subprocess.run(argv, cwd=REPO, env=env, stdout=stdout, stderr=stderr)
    record = dict(step=name, attempt=run, argv=argv, cwd=str(REPO), start_utc=start,
                  elapsed_seconds=time.perf_counter()-t, returncode=result.returncode,
                  source_sha256=sha(path), source_snapshot=str(snapshot.relative_to(HERE)),
                  stdout=stem+'.stdout.txt', stderr=stem+'.stderr.txt',
                  stdout_sha256=sha(HERE/(stem+'.stdout.txt')), stderr_sha256=sha(HERE/(stem+'.stderr.txt')))
    (HERE/('execution_'+name+'_'+str(run)+'.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
    # A previous independent child may have completed while this one ran.
    records = json.loads(manifests.read_text()) if manifests.exists() else []
    records.append(record)
    manifests.write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(record, ensure_ascii=False))
    print((HERE/(stem+'.stdout.txt')).read_text())
    print((HERE/(stem+'.stderr.txt')).read_text())
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
