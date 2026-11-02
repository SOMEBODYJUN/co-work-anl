"""One isolated exact original entry, with immutable start guard and report binding."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys,time
BASE=Path(__file__).resolve().parent
label=sys.argv[1]
assert label in ('fresh','root')
name={'fresh':'audit_random_retention_blind','root':'audit_erasure_kernels'}[label]
D=BASE/'runs'/label
start=D/'started.json';event=D/'event.json'
if start.exists() or event.exists():raise RuntimeError('Already started: do not silently rerun')
entry=D/(name+'.py');expected=D/'frozen-report.json';generated=D/(name+'.json')
assert entry.exists() and expected.exists() and not generated.exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
command=[sys.executable,'-B',str(entry)]
start.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'entry_sha256':sha(entry),'expected_report_sha256':sha(expected),'identity':'informed replay of exact original entry after primary and related mathematical reading'},indent=2)+'\n')
t=time.monotonic();p=subprocess.run(command,cwd=D,text=False,capture_output=True,check=False)
(D/'stdout.txt').write_bytes(p.stdout);(D/'stderr.txt').write_bytes(p.stderr)
e={'exit_code':p.returncode,'wall_seconds':time.monotonic()-t,'entry_sha256':sha(entry),'expected_report_sha256':sha(expected),'generated_report_exists':generated.exists(),'original_entry_invocations':1,'source_function_or_game_or_solver_invocations_outside_original_entry':0,'scope':'Original fixed deterministic arithmetic loops only; no changed parameters, discovery, random scan, SPE/BI/LP or new blind/independent implementation claim'}
if generated.exists():e.update(generated_report_sha256=sha(generated),report_byte_identical=generated.read_bytes()==expected.read_bytes(),stdout_json_equals_report=json.loads(p.stdout)==json.loads(generated.read_bytes()))
e['all_pass']=p.returncode==0 and e.get('report_byte_identical',False) and e.get('stdout_json_equals_report',False) and not p.stderr
assert not event.exists();event.write_text(json.dumps(e,indent=2)+'\n')
print(json.dumps(e,indent=2));assert e['all_pass']
