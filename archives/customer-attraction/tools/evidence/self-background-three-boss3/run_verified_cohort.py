from pathlib import Path
import sys,subprocess,json,time,hashlib,platform,os,shutil
from datetime import datetime,timezone
import numpy,scipy
S=Path(__file__).resolve().parent
R=S.parent/'self_background_explicit21_runtime'
assert not R.exists(), 'fresh runtime required; preserve old events'
manifest=json.loads((S/'runtime-dependency-manifest.json').read_text())
actual=[]
for d in manifest:
 if d['path'].endswith('prefix_coupled_seats_strict.json'):continue
 src=S/'runtime-inputs'/d['path']; assert hashlib.sha256(src.read_bytes()).hexdigest()==d['sha256']
 dst=R/d['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);actual.append({'path':d['path'],'size':dst.stat().st_size,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
source_rel=Path('research/workspaces/customer-attraction/R-5dbadd913a00492e994a6cfca3ec53fc/continuation/self_background_probe.py')
p=R/source_rel;p.parent.mkdir(parents=True);shutil.copy2(S/'original/self_background_probe.py',p)
files=sorted((R/'examples/customer_attraction').glob('*.json'))
assert len(files)==21
assert all(set(('topics','customers','players')).issubset(json.loads(f.read_text())) for f in files)
assert not any(f.name=='prefix_coupled_seats_strict.json' for f in files)
D=S/'replay';D.mkdir()
(D/'actual-runtime-manifest.json').write_text(json.dumps(actual,ensure_ascii=False,indent=2)+'\n')
start=datetime.now(timezone.utc).isoformat();tick=time.monotonic();env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
r=subprocess.run([sys.executable,str(p)],cwd=R,env=env,text=True,capture_output=True)
(D/'stdout.txt').write_text(r.stdout);(D/'stderr.txt').write_text(r.stderr)
output=p.parent/'signed_self_background_probe.json'
if output.exists():(D/'signed_self_background_probe.json').write_bytes(output.read_bytes())
record={'event':'second unmodified original entry; explicit21 original canonical Instance files; copy/hash/schema assertions immediately before subprocess','command':[sys.executable,str(p)],'cwd':str(R),'start_utc':start,'elapsed_seconds':time.monotonic()-tick,'exit_code':r.returncode,'original_entry_calls_this_event':1,'unsigned_entry_calls':0,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'Python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'assertions_enabled':__debug__,'output_file_exists':output.exists(),'stdout_bytes':len(r.stdout.encode()),'stderr_bytes':len(r.stderr.encode()),'actual_runtime_JSON_files':len(files),'canonical_Instances':21,'schema_exclusions':1,'scope':'new explicitly delimited corpus event; no historical execution identity or exact negative primal/dual certificate claimed'}
(D/'execution-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record,ensure_ascii=False,indent=2))
if output.exists():print(output.read_text())
assert r.returncode==0
