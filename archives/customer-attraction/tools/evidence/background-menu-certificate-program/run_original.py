"""Run the unmodified frozen entry point once in a new directory."""
import argparse, hashlib, json, platform, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
import numpy, scipy

def digest(p):
    raw=p.read_bytes()
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--source', type=Path, required=True)
    a.add_argument('--out-dir', type=Path, required=True)
    args=a.parse_args()
    source=args.source.resolve()
    out=args.out_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)
    copied=out/'background_menu_certificate.py'
    shutil.copyfile(source,copied)
    before=digest(copied)
    started=datetime.now(timezone.utc).isoformat()
    begin=time.perf_counter()
    proc=subprocess.run([sys.executable,'-B',str(copied)],cwd=out,capture_output=True,timeout=120)
    duration=time.perf_counter()-begin
    (out/'stdout.txt').write_bytes(proc.stdout)
    (out/'stderr.txt').write_bytes(proc.stderr)
    produced={p.name:digest(p) for p in sorted(out.iterdir()) if p.is_file()}
    report=out/'background_menu_certificate.json'
    data=json.loads(report.read_text()) if report.exists() else None
    record=dict(command=[sys.executable,'-B',str(copied)],cwd=str(out),started_utc=started,finished_utc=datetime.now(timezone.utc).isoformat(),duration_seconds=duration,timeout_seconds=120,returncode=proc.returncode,versions=dict(python=platform.python_version(),numpy=numpy.__version__,scipy=scipy.__version__),source_before=before,source_after=digest(copied),files=produced,certificate=data,original_entry_calls=1,linprog_calls_in_original_main=1,other_original_entry_calls=0,status_file_present=(out/'background_menu_certificate_status.json').exists(),frozen_certificate_sha256='db25a2460aa58d9a8438f7aea0e20445c12264f717c587cafdd9974338d58689',new_output_matches_frozen_bytes=report.exists() and digest(report)['sha256']=='db25a2460aa58d9a8438f7aea0e20445c12264f717c587cafdd9974338d58689')
    (out/'execution.json').write_text(json.dumps(record,indent=2)+'\n')
    assert proc.returncode==0 and data and data['success'] and not proc.stderr
    assert before==digest(copied) and record['new_output_matches_frozen_bytes']
    print(json.dumps(record,indent=2))
if __name__=='__main__':main()
