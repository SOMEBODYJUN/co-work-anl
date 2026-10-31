"""One original __main__ entry via runpy, plus passive return-frame input observation."""
from pathlib import Path
import contextlib, hashlib, json, os, platform, runpy, shutil, sys, time, traceback
E=Path(__file__).resolve().parent
primary=json.loads((E/'source-manifest.json').read_text())
deps=json.loads((E/'dependency-manifest.json').read_text())
source=next(r for r in primary if r['path'].endswith('audit_incoming_slack_transport.py'))
replay=E/'replay';replay.mkdir(exist_ok=False)
root=replay/'source-root';root.mkdir()
for group,rows in [('original',[source]),('dependencies',deps)]:
 for row in rows:
    target=root/row['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(E/group/row['path'],target)
program=root/source['path']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
observed=[]
def profile(frame,event,arg):
 if event=='return' and frame.f_code.co_filename==str(program) and frame.f_code.co_name=='run':
    v=frame.f_locals
    observed.append({'case':v['name'],'actual':list(v['Z']),'optimum':list(v['optimum']),'covered_count':len(v['C']),'optimal_count':len(v['O']),'missing_count':len(v['R']),'unit_customers':len(v['likes']),'players':v['m'],'topics':v['q'],'loaded_policy_keys':len(v['policy']),'original_return':arg,'observation_scope':'passive original run return locals; no additional finish/pay/IC or search call'})
old_argv=sys.argv[:];old_cwd=Path.cwd();code=0;start=time.time()
try:
 sys.argv=[str(program),'--output','incoming_slack_exact_v2.json'];os.chdir(root)
 with (replay/'original.stdout.txt').open('w') as out,(replay/'original.stderr.txt').open('w') as err:
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        try:
            sys.setprofile(profile)
            runpy.run_path(str(program),run_name='__main__')
        except BaseException:
            code=1;traceback.print_exc()
        finally:sys.setprofile(None)
finally:
 sys.argv=old_argv;os.chdir(old_cwd)
new=program.with_name('incoming_slack_exact_v2.json')
frozen=E/'original'/next(r['path']for r in primary if r['path'].endswith('incoming_slack_exact_v2.json'))
state={'execution_count':1,'original_program_calls':1,'method':'runpy.run_path(original-byte copied source, run_name=__main__); passive sys.setprofile only observes run return locals','argv':[str(program),'--output','incoming_slack_exact_v2.json'],'cwd':str(root),'python':sys.version,'python_executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'exit_code':code,'duration_seconds':time.time()-start,'program_sha256':sha(program),'program_bytes':program.stat().st_size,'dependencies':[{'path':r['path'],'sha256':sha(root/r['path']),'bytes':(root/r['path']).stat().st_size}for r in deps],'local_imports':[],'path_difference':'byte-identical original relative path mirrored beneath independent external source-root; not original frozen filesystem root','output_created':new.exists(),'exclusive_output':'--output sibling path validated by original code; open x','stdout_bytes':(replay/'original.stdout.txt').stat().st_size,'stdout_sha256':sha(replay/'original.stdout.txt'),'stderr_bytes':(replay/'original.stderr.txt').stat().st_size,'stderr_sha256':sha(replay/'original.stderr.txt')}
if new.exists():state.update({'new_report_bytes':new.stat().st_size,'new_report_sha256':sha(new),'equals_frozen_v2_bytes':new.read_bytes()==frozen.read_bytes(),'stdout_equals_report_bytes':(replay/'original.stdout.txt').read_bytes()==new.read_bytes()})
(replay/'execution-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
(replay/'runtime-case-state.json').write_text(json.dumps(observed,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'execution':state,'cases':observed},ensure_ascii=False))
assert code==0,'Original failure preserved; no automatic retry'
