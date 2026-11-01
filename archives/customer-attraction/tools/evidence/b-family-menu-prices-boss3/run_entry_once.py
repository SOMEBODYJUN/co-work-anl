"""Run one specified original entrypoint in an isolated prepared runtime."""
from pathlib import Path
import sys,json,time,subprocess,platform
HERE=Path(__file__).resolve().parent
def main():
    if len(sys.argv)!=3 or sys.argv[1] not in ('verify','branch-lp'):
        raise SystemExit('usage: run_entry_once.py verify|branch-lp /absolute/prepared-runtime')
    mode=sys.argv[1];runtime=Path(sys.argv[2])
    if not runtime.is_absolute():raise SystemExit('runtime must be absolute')
    if mode=='verify':
        script=runtime/'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/B_menu_prices_master.py'
        command=[sys.executable,'-B',str(script),'--all-families','--verify']
    else:
        command=[sys.executable,'-B',str(HERE/'replay/research_2/branch_family_lp.py')]
    target=HERE/'replay'/(mode+'-execution.json')
    if target.exists():raise FileExistsError(target)
    start=time.time();result=subprocess.run(command,cwd=runtime,capture_output=True)
    (HERE/'replay'/(mode+'-stdout.txt')).write_bytes(result.stdout)
    (HERE/'replay'/(mode+'-stderr.txt')).write_bytes(result.stderr)
    report={'mode':mode,'command':command,'cwd':str(runtime),'python':platform.python_version(),'elapsed_seconds':time.time()-start,'exit_code':result.returncode,'stdout_path':str((HERE/'replay'/(mode+'-stdout.txt')).relative_to(HERE)),'stderr_path':str((HERE/'replay'/(mode+'-stderr.txt')).relative_to(HERE)),'original_entrypoint':True,'optimization_requested':mode=='branch-lp'}
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False));print(result.stdout.decode(),end='')
    if result.returncode:print(result.stderr.decode(),file=sys.stderr)
    raise SystemExit(result.returncode)
if __name__=='__main__':main()
