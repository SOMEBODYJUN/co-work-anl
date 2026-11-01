from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,time
B=Path('/workspace/scratch/37f0f9248cfc');C=B/'boss4-next-cache'
root=C/'weak-stationary-four-current-run-001'
assert not root.exists(), 'Exactly one new fixed-input audit allowed; do not repeat'
base=root/'source-root/research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/global_proof'
base.mkdir(parents=True)
original=C/'resumed-next-weak_stationary_kernel_originals_four-originals'
code=original/'c1a5585cd22ded3d8a9e/weak_stationary_kernel_audit.py'
data=original/'fabeca223266f5117a5e/weak_stationary_kernel_candidate.json'
reference=original/'1f411b70b11c0c0d7470/weak_stationary_kernel_audit.json'
shutil.copyfile(code,base/code.name);shutil.copyfile(data,base/data.name)
def record(p):
 b=p.read_bytes();return {'path':str(p),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
before=[record(p)for p in [code,data,base/code.name,base/data.name]]
env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
argv=[sys.executable,'-B',str(base/code.name)]
started=time.monotonic();result=subprocess.run(argv,cwd=root/'source-root',env=env,capture_output=True);elapsed=time.monotonic()-started
(root/'stdout.txt').write_bytes(result.stdout);(root/'stderr.txt').write_bytes(result.stderr)
after=[record(p)for p in [code,data,base/code.name,base/data.name]]
output=base/'weak_stationary_kernel_audit.json'
event={'identity':'one informed reproduction of original independent stdlib audit on the new25-unit-client/4-player fixed candidate','math_entry_number':1,'original_code_unmodified':True,'argv':argv,'cwd':str(root/'source-root'),'python_version':sys.version,'flags':{'B':True,'O':False,'PYTHONOPTIMIZE':'unset for child','wrapper_optimize':sys.flags.optimize},'exit_code':result.returncode,'elapsed_seconds':elapsed,'stdout':record(root/'stdout.txt'),'stderr':record(root/'stderr.txt'),'before':before,'after':after,'all_four_input_copies_unchanged':before==after,'reference_historical_JSON':record(reference),'output':record(output) if output.exists()else None,'output_byte_identical_to_historical_JSON':output.exists() and output.read_bytes()==reference.read_bytes(),'output_all_JSON_fields_equal_to_historical':output.exists() and json.loads(output.read_text())==json.loads(reference.read_text()),'no_probe_LP_DP_solver_or_old13_22_replay':True,'review_identity':'known input and source read before run; not a blind or external review'}
(root/'execution-event.json').write_text(json.dumps(event,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'exit':result.returncode,'elapsed':elapsed,'stdout_bytes':len(result.stdout),'stderr_bytes':len(result.stderr),'output':event['output'],'byte_identical':event['output_byte_identical_to_historical_JSON'],'all_fields_equal':event['output_all_JSON_fields_equal_to_historical'],'inputs_unchanged':before==after},ensure_ascii=False,indent=2))
