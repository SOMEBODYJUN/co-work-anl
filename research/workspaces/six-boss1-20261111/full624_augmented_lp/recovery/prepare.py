"""Bind copied inputs for rational recovery; preserve all frozen source bytes."""
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import json,platform,shutil,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
RUN=ROOT.parent
REPO=ROOT.parents[3]
CLOUD=ROOT/'actions_discovery'
AUDIT=RUN/'compute_dispatch/full624-download-input-audit.json'
def sha(p):return sha256(p.read_bytes()).hexdigest()
audit=json.loads(AUDIT.read_text())
assert audit['status']=='DOWNLOADED-INPUTS-AND-BYTE-COPY-VERIFIED'
assert (audit['run_id'],audit['job_id'],audit['artifact_id'])==(43082081632,130737029504,13883693740)
assert audit['commit']=='1ccc0a5a5aaeb68a7b8b74297f0482ca668ba7b6'
for r in audit['inputs']+audit['outputs']:
    assert sha(REPO/r['path'])==r['sha256'],r['path']
assert len(audit['outputs'])==19
frozen=json.loads((ROOT/'freeze_manifest.json').read_text())
for r in frozen['assets']:
    assert sha(REPO/r['path'])==r['sha256'],r['path']
names=('exact_matrix.json.gz','floating_solver_arrays.npz','epigraph_structure.json',
    'zz_envelope_structure.json','inherited_dual_lower_bound.json','inputs_manifest.json',
    'assembly_verification.json','numerical_result.json','assemble_solve.py','recover.py',
    'verify_certificates.py','actions_stage.py')
copies=[]
for name in names:
    target=HERE/name
    assert not target.exists(),str(target)
    shutil.copyfile(CLOUD/name,target)
    assert sha(target)==sha(CLOUD/name)
    copies.append({'name':name,'sha256':sha(target),'source':str((CLOUD/name).relative_to(REPO))})
receipt={'status':'BOUND_INPUTS_READY_NO_OPTIMIZATION','argv':[sys.executable,*sys.argv],
    'cwd':str(Path.cwd()),'python':platform.python_version(),'utc':datetime.now(timezone.utc).isoformat(),
    'prepare_source_sha256':sha(Path(__file__)),'download_audit_sha256':sha(AUDIT),
    'frozen_local_manifest_sha256':sha(ROOT/'freeze_manifest.json'),
    'old_frozen_assets_preserved':len(frozen['assets']),'cloud_output_files_preserved':19,
    'cloud':{k:audit[k] for k in ('run_id','job_id','artifact_id','commit','artifact_sha256')},
    'copies':copies,'all_cloud_original_output_sha256':audit['outputs'],
    'executed_recovery_sources':[{'path':str((ROOT/name).relative_to(REPO)),'sha256':sha(ROOT/name)}
        for name in ('actions_stage.py','assemble_solve.py','recover.py','verify_certificates.py')],
    'optimizer_calls_this_phase':0}
target=HERE/'recovery_input_manifest.json';assert not target.exists()
target.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
