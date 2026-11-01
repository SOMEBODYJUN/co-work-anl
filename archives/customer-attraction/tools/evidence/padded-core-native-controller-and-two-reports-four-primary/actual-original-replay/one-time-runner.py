from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time

c = Path(__file__).resolve().parent
manifest = json.loads((c/'resumed-next-padded_core_native_controller_and_two_reports_four-originals/actual-source-manifest.json').read_text())
rows = {x['id']: x for x in manifest['rows']}
source = Path(rows['aa9e8c07ae71348ecd58']['local_path'])
run = c/'padded-core-native-original-first-run'
assert not run.exists(), 'One-time original replay already exists; inspect actual events, do not rerun.'
run.mkdir()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
events = []
for k, report_id in [(1,'0d656e3e4a6b4fe49d65'), (12,'1fc4c3642371404ecdfb')]:
    case = run/('k'+str(k)); case.mkdir()
    script = case/'audit_padded_core_controller.py'
    shutil.copyfile(source, script)
    expected = Path(rows[report_id]['local_path'])
    assert sha(source) == sha(script) == rows['aa9e8c07ae71348ecd58']['sha256']
    before = {'original_program':sha(source),'isolated_program':sha(script),'original_report':sha(expected)}
    cmd = [sys.executable,'-B',str(script),'--k',str(k)]
    env = dict(os.environ, PYTHONOPTIMIZE='0')
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    clock = time.monotonic()
    result = subprocess.run(cmd, cwd=case, env=env, capture_output=True, timeout=90)
    elapsed = time.monotonic()-clock
    (case/'stdout.txt').write_bytes(result.stdout)
    (case/'stderr.txt').write_bytes(result.stderr)
    output = case/f'padded_core_k{k}_audit.json'
    after = {'original_program':sha(source),'isolated_program':sha(script),'original_report':sha(expected)}
    event = {'event':'first actual execution of this exact original implementation and parameter in this continuation; original stored report replay, not a new independent or all-k proof','k':k,'argv':cmd,'cwd':str(case),'interpreter':sys.version,'assertions_enabled':True,'explicit_child_environment':{'PYTHONOPTIMIZE':'0'},'started_utc':started,'duration_seconds':elapsed,'exit_code':result.returncode,'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr),'before_sha256':before,'after_sha256':after,'source_and_original_report_unchanged':before==after,'output_sha256':sha(output) if output.exists() else None,'output_matches_entire_original_report_bytes':output.exists() and output.read_bytes()==expected.read_bytes(),'stdout_matches_output_bytes':output.exists() and result.stdout==output.read_bytes()}
    (case/'execution-event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
    assert result.returncode==0 and not result.stderr and before==after
    assert event['output_matches_entire_original_report_bytes'] and event['stdout_matches_output_bytes']
    events.append(event)
    print(json.dumps({'k':k,'exit':result.returncode,'seconds':elapsed,'same_entire_bytes':True,'output_sha256':sha(output)}),flush=True)
(run/'execution-events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n')
