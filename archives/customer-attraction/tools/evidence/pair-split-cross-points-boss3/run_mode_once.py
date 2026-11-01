"""Capture one new frozen-builder event for one mode, outside the clone."""
from pathlib import Path
import sys,json,time,subprocess,platform
HERE=Path(__file__).resolve().parent
def main():
    if len(sys.argv)!=3 or sys.argv[1] not in ('split','cross'):raise SystemExit('usage: run_mode_once.py split|cross /absolute/runtime')
    mode=sys.argv[1];out=HERE/'replay'/mode;out.mkdir(parents=True,exist_ok=True)
    target=out/'execution-record.json'
    if target.exists():raise FileExistsError(target)
    command=[sys.executable,'-B',str(HERE/'verify_pair_mode.py'),mode,sys.argv[2]]
    start=time.time();r=subprocess.run(command,cwd=sys.argv[2],capture_output=True)
    (out/'stdout.txt').write_bytes(r.stdout);(out/'stderr.txt').write_bytes(r.stderr)
    record={'mode':mode,'command':command,'cwd':sys.argv[2],'python':platform.python_version(),'elapsed_seconds':time.time()-start,'exit_code':r.returncode,'original_build_calls':1,'original_CLI_called':False,'optimizer_called':False}
    target.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(record,ensure_ascii=False));print(r.stdout.decode(),end='')
    if r.returncode:print(r.stderr.decode(),file=sys.stderr)
    raise SystemExit(r.returncode)
if __name__=='__main__':main()
