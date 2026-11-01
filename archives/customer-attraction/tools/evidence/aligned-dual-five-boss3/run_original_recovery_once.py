from pathlib import Path
import subprocess,sys,time,json,hashlib,platform
from datetime import datetime,timezone
S=Path(__file__).resolve().parent;R=S.parent/'aligned_dual_runtime';P=R/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible';script=P/'recover_aligned_dual.py'
T=S/'replay';T.mkdir(exist_ok=True);tick=time.monotonic();start=datetime.now(timezone.utc).isoformat();cmd=[sys.executable,'-I','-B',str(script)]
# -I excludes the script directory from sys.path, but original imports siblings.
# Use an explicit isolated bootstrap that adds exactly that frozen sibling path.
bootstrap='import runpy,sys;sys.path.insert(0,sys.argv[1]);runpy.run_path(sys.argv[2],run_name="__main__")'
cmd=[sys.executable,'-I','-B','-c',bootstrap,str(P),str(script)]
r=subprocess.run(cmd,cwd=R,text=True,capture_output=True)
(T/'stdout.txt').write_text(r.stdout);(T/'stderr.txt').write_text(r.stderr)
out=P/'aligned_support_exact_dual.json';old=S/'original/aligned_support_exact_dual.json'
if out.exists():(T/'aligned_support_exact_dual.json').write_bytes(out.read_bytes())
event={'event':'one unmodified original recovery top-level run through isolated runpy bootstrap adding its exact frozen sibling directory; no reoptimization','command':cmd,'cwd':str(R),'start_utc':start,'elapsed_seconds':time.monotonic()-tick,'exit_code':r.returncode,'Python':platform.python_version(),'assertions_enabled':True,'source_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'original_recovery_top_level_runs':1,'original_reopt_import_or_runs':0,'LP_calls':0,'outside_column_evaluations':0,'recovered_file_bytes_equal':out.exists()and out.read_bytes()==old.read_bytes(),'recovered_file_all_fields_equal':out.exists()and json.loads(out.read_text())==json.loads(old.read_text()),'stdout_bytes':len(r.stdout.encode()),'stderr_bytes':len(r.stderr.encode())}
(T/'execution-record.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n');print(json.dumps(event,ensure_ascii=False,indent=2));assert r.returncode==0,(r.stderr);assert event['recovered_file_bytes_equal']
