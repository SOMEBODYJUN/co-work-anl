"""Freeze the bounded local attempt and exact Actions input handoff."""
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
import ast,json,platform,sys

HERE=Path(__file__).resolve().parent
RUN=HERE.parent
REPO=HERE.parents[3]
def sha(p):return sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(name,data):
    p=HERE/name;assert not p.exists(),str(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
for f in HERE.glob('*.py'):ast.parse(f.read_text(),filename=str(f))
assembly=read(HERE/'assembly_verification.json')
verification=read(HERE/'structure_and_lower_verification.json')
numerical=read(HERE/'numerical_result.json')
inputs=read(HERE/'inputs_manifest.json')
for rel,expected in inputs['sha256'].items():assert sha(RUN/rel)==expected,rel
assert assembly['status']==verification['status']=='PASS'
assert numerical['optimizer_calls']==1 and not numerical['success'] and numerical['W_float'] is None
assert not (HERE/'floating_solver_arrays.npz').exists()
assert not (HERE/'augmented_lp_exact.json').exists()
assert not (HERE/'exact_dual_certificate.json').exists()
assert not (HERE/'certificate_verification.json').exists()
receipts={}
for name,code in [('assemble',0),('solve',1),('verify_structure',0),('actions_dry_run',0)]:
    r=read(HERE/('execution_'+name+'.json'))
    assert r['exit_code']==code
    assert sha(HERE/r['source_snapshot'])==r['source_sha256']
    assert sha(HERE/(name+'_stdout.txt'))==r['stdout_sha256']
    assert sha(HERE/(name+'_stderr.txt'))==r['stderr_sha256']
    receipts[name]=r
own_inputs=('exact_matrix.json.gz','floating_problem.npz','epigraph_structure.json','zz_envelope_structure.json',
    'inherited_dual_lower_bound.json','inputs_manifest.json','assembly_verification.json',
    'assemble_solve.py','recover.py','verify_certificates.py','actions_stage.py','actions_pipeline.py')
command=['python3','-B',str((HERE/'actions_pipeline.py').relative_to(REPO)),
    '--execute','--method','highs-ds','--time-limit','1800','--output','actions_run']
request={'status':'PREPARED_NOT_DISPATCHED','run':'six-boss1-20261111','owner':'Boss1',
    'argv':command,'cwd':'repository root','environment':{'python':'3.12','numpy':'2.3.5','scipy':'1.17.0'},
    'local_solver_version':'HiGHS1.8.0 git222cce7; any Actions version must be logged and all final certificates remain rational',
    'requires_github_actions_environment':True,'optimizer_calls_planned':1,'solver_time_limit_seconds':1800,
    'method':'highs-ds','rows':20910,'columns':20585,'nonzeros':3208797,
    'input_files':[{'path':str((HERE/name).relative_to(REPO)),'sha256':sha(HERE/name)} for name in own_inputs],
    'immutable_repository_dependencies':[{'path':str((RUN/rel).relative_to(REPO)),'sha256':digest} for rel,digest in inputs['sha256'].items()],
    'output_directory':str((HERE/'actions_run').relative_to(REPO)),
    'retain_outputs_on_failure':True,'automatic_numeric_reruns':0,
    'exact_postprocessing':['same-old-W primal recovery when numerically compatible','unfixed-W primal recovery only if the same-W active-face recovery fails',
        'old exact dual zero-extension if sameW','new exact dual only if W rises','independent full20910-row20585-column rational verification'],
    'outcome_required':'A full rational primal/dual equality certificate before claiming same optimum or increased optimum.',
    'dispatch_performed_by_this_agent':False}
write('actions_request.json',request)
manifest={'status':'FROZEN_ACTIONS_READY_OPTIMUM_UNRESOLVED','frozen_utc':datetime.now(timezone.utc).isoformat(),
    'argv':[sys.executable,*sys.argv],'cwd':str(Path.cwd()),'python':platform.python_version(),
    'scope':'Only complete actual4/R/family0-off on original16hist; no fixed point RHS; general six-player half remains OPEN.',
    'result':{'matrix_and_symbolic_append':'INDEPENDENT_EXACT_PASS','inherited_lower_bound':'INDEPENDENT_EXACT_PASS',
        'W_lower_bound':verification['lower_bound'],'local_solver_calls':1,'local_solver_result':'TIME_LIMIT_NO_PRIMAL_ARRAY',
        'exact_primal_recovery_attempts':0,'exact_dual_recovery_attempts':0,
        'new_optimum_comparison':'UNRESOLVED','actions_request':'PREPARED_NOT_DISPATCHED','general_six_half':'OPEN'},
    'actual_stage_receipts':receipts,
    'pending':['Main dispatches the prepared full-matrix Actions job','Successful numerical candidate','Exact rational primal and required dual','Independent full row/column optimum verification'],
    'assets':[]}
excluded={'freeze_manifest.json','execution_freeze.json','freeze_stdout.txt','freeze_stderr.txt'}
for p in sorted(HERE.rglob('*')):
    if p.is_file() and p.name not in excluded:
        manifest['assets'].append({'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size})
note=RUN/'full624_augmented_lp.md'
manifest['assets'].append({'path':str(note.relative_to(REPO)),'sha256':sha(note),'bytes':note.stat().st_size})
write('freeze_manifest.json',manifest)
print(json.dumps({'status':manifest['status'],'assets':len(manifest['assets']),
    'matrix_sha256':assembly['matrix_sha256'],'verification_sha256':sha(HERE/'structure_and_lower_verification.json'),
    'actions_request_sha256':sha(HERE/'actions_request.json'),'freeze_manifest_sha256':sha(HERE/'freeze_manifest.json'),
    'no_optimum_claim':True},ensure_ascii=False,indent=2))
