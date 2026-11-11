"""One Actions discovery for the exact full624 augmented system.

Rational recovery consumes the returned arrays in a separate observed step.
No automatic optimizer retry and no claim based on the numerical objective.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json, os, shutil, subprocess, sys, time

WS=Path(__file__).resolve().parent.parent
REPO=WS.parents[2]
HERE=WS/'full624_augmented_lp'
OUT=HERE/'actions_discovery'
assert os.environ.get('GITHUB_ACTIONS')=='true'
assert not OUT.exists()
request=json.loads((HERE/'actions_request.json').read_bytes())
for item in request['input_files']+request['immutable_repository_dependencies']:
    assert sha256((REPO/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
OUT.mkdir()
names=('exact_matrix.json.gz','floating_problem.npz','epigraph_structure.json','zz_envelope_structure.json',
       'inherited_dual_lower_bound.json','inputs_manifest.json','assembly_verification.json',
       'assemble_solve.py','recover.py','verify_certificates.py','actions_stage.py','actions_pipeline.py')
for name in names:shutil.copyfile(HERE/name,OUT/name)
cmd=[sys.executable,'-B',str(HERE/'actions_stage.py'),'solve',str(OUT),'highs-ds','1800']
record=dict(argv=cmd,started_utc=datetime.now(timezone.utc).isoformat(),optimizer_calls=1,
            output_directory=str(OUT.relative_to(REPO)),exact_recovery='not run; consume returned arrays after download',
            input_sha256={n:sha256((OUT/n).read_bytes()).hexdigest() for n in names})
(OUT/'discovery_request.json').write_text(json.dumps(record,indent=2)+'\n')
start=time.monotonic()
with (OUT/'solver_stdout.txt').open('w') as a,(OUT/'solver_stderr.txt').open('w') as b:
    result=subprocess.run(cmd,cwd=REPO,stdout=a,stderr=b,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
record.update(exit_code=result.returncode,elapsed_seconds=time.monotonic()-start,
              completed_utc=datetime.now(timezone.utc).isoformat(),exact_optimum_claimed=False)
(OUT/'discovery_execution.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='input_sha256'},indent=2),flush=True)
sys.exit(result.returncode)
