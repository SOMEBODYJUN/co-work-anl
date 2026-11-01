from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, time

c = Path(__file__).resolve().parent
m = json.loads((c / 'root-oa-security-common-rows-originals/actual-source-manifest.json').read_text())
src = next(x for x in m['rows'] if x['id'] == '6872af198112d93b8e51')
old = next(x for x in m['rows'] if x['id'] == 'c87d6242f66b0cbb8703')
out = c / 'root-oa-group-common-dual-original-run-001'
assert not out.exists(), 'Do not replay an existing original entry'
out.mkdir()
p = out / 'audit_group_common_dual.py'
shutil.copy2(src['local_path'], p)
assert hashlib.sha256(p.read_bytes()).hexdigest() == src['sha256']
argv = [sys.executable, str(p), '--output']
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.monotonic()
r = subprocess.run(argv, cwd=out, capture_output=True)
elapsed = time.monotonic() - t
(out/'stdout.json').write_bytes(r.stdout)
(out/'stderr.txt').write_bytes(r.stderr)
generated = out/'group_common_dual_exact.json'
record = dict(original_entry_runs=1, original_module_imports=0,
    discoverer_or_canonical_solver_imports=0, LP_MILP_calls=0,
    argv=argv, cwd=str(out), python=sys.version, started_utc=started,
    elapsed_seconds=elapsed, exit_code=r.returncode, stderr_bytes=len(r.stderr),
    source_sha256=src['sha256'], source_after_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
    frozen_report_sha256=old['sha256'])
if generated.exists():
    b=generated.read_bytes()
    record.update(generated_report_bytes=len(b), generated_report_sha256=hashlib.sha256(b).hexdigest(),
        full_generated_report_byte_identical=b==Path(old['local_path']).read_bytes(),
        stdout_byte_identical=r.stdout==Path(old['local_path']).read_bytes())
(out/'execution-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
assert r.returncode == 0 and not r.stderr and record['full_generated_report_byte_identical']
assert record['stdout_byte_identical'] and record['source_after_sha256']==src['sha256']
print(json.dumps(record,ensure_ascii=False))
