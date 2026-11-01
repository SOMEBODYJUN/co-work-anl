"""Execute one original early-reply verification, retaining all actual output."""
from pathlib import Path
import sys,json,time,subprocess,platform
HERE=Path(__file__).resolve().parent
def main():
    if len(sys.argv)!=3 or sys.argv[1] not in ('base','floors'):
        raise SystemExit('usage: run_original_once.py base|floors /absolute/prepared-runtime')
    mode=sys.argv[1];runtime=Path(sys.argv[2]);assert runtime.is_absolute()
    target=HERE/'replay'/(mode+'-execution.json')
    if target.exists():raise FileExistsError(target)
    script=runtime/'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/early_reply_prices.py'
    command=[sys.executable,'-B',str(script)]+(['--floors'] if mode=='floors' else [])+['--verify']
    start=time.time();r=subprocess.run(command,cwd=runtime,capture_output=True)
    (HERE/'replay'/(mode+'-stdout.txt')).write_bytes(r.stdout)
    (HERE/'replay'/(mode+'-stderr.txt')).write_bytes(r.stderr)
    report={'mode':mode,'command':command,'cwd':str(runtime),'python':platform.python_version(),'exit_code':r.returncode,'elapsed_seconds':time.time()-start,'original_entrypoint':True,'optimization_requested':False,'stdout_path':'replay/'+mode+'-stdout.txt','stderr_path':'replay/'+mode+'-stderr.txt'}
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False));print(r.stdout.decode(),end='')
    if r.returncode:print(r.stderr.decode(),file=sys.stderr)
    raise SystemExit(r.returncode)
if __name__=='__main__':main()
