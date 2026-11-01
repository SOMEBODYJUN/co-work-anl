"""Capture the single enhanced original-builder event outside the clone."""
from pathlib import Path
import sys,json,time,subprocess,platform
HERE=Path(__file__).resolve().parent
def main():
    if len(sys.argv)!=2:raise SystemExit('usage: run_once.py /absolute/prepared-runtime')
    target=HERE/'replay/execution-record.json'
    if target.exists():raise FileExistsError(target)
    command=[sys.executable,'-B',str(HERE/'verify_both_points.py'),sys.argv[1]]
    start=time.time();r=subprocess.run(command,capture_output=True,cwd=sys.argv[1])
    (HERE/'replay/stdout.txt').write_bytes(r.stdout);(HERE/'replay/stderr.txt').write_bytes(r.stderr)
    report={'command':command,'cwd':sys.argv[1],'elapsed_seconds':time.time()-start,'python':platform.python_version(),'exit_code':r.returncode,'original_build_calls':1,'original_CLI_called':False,'optimizer_called':False,'stdout':'replay/stdout.txt','stderr':'replay/stderr.txt'}
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False));print(r.stdout.decode(),end='')
    if r.returncode:print(r.stderr.decode(),file=sys.stderr)
    raise SystemExit(r.returncode)
if __name__=='__main__':main()
