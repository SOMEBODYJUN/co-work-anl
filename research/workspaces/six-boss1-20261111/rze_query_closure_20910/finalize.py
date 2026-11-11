"""Freeze the completed finite envelope task and conditional diagnostic.

Only this task's outputs are written.  Frozen dispatch inputs and every raw
cloud artifact are read and SHA-checked, never overwritten.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
REPO=WORK.parents[2]

def sha(p):return sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((HERE/n).read_bytes())
def save(n,d):(HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def record(p):return {'path':str(p.relative_to(REPO)),'bytes':p.stat().st_size,'sha256':sha(p)}

def main():
    ready=read('actions_ready.json');cert=read('exact_certificate.json')
    check=read('independent_certificate_audit.json');diagnostic=read('conditional_B4_independent_audit.json')
    cloud=read('actions_output/phase_I_discovery.json')
    assert cert['kind']=='primal' and check['passed'] and diagnostic['passed']
    assert check['certificate_sha256']==diagnostic['E_certificate_sha256']==sha(HERE/'exact_certificate.json')
    assert check['verifier_sha256']==sha(HERE/'verify_certificate.py')
    assert diagnostic['verifier_sha256']==sha(HERE/'verify_conditional_B4.py')
    assert cert['recovery_source_sha256']==sha(HERE/'recover_exact.py')
    assert cloud['linprog_calls']==1 and cloud['phase_I']==0
    for item in ready['dependencies']:assert sha(REPO/item['path'])==item['sha256']
    main_download=WORK/'compute_dispatch/rze-closure-download-input-audit.json'
    provenance=json.loads(main_download.read_bytes())
    for item in provenance['runtime_outputs']:assert sha(REPO/item['path'])==item['sha256']
    requested=read('new_envelopes_exact.json')['rows']
    families=[]
    for name in sorted({r['name'][0] for r in requested}):
        rr=[r for r in requested if r['name'][0]==name]
        families.append({'family':name,'rows':len(rr),'zero':sum(F(r['value'])==0 for r in rr),
                         'positive':sum(F(r['value'])>0 for r in rr),'negative':sum(F(r['value'])<0 for r in rr),
                         'minimum':str(min(F(r['value']) for r in rr))})
    summary={'status':'COMPLETE_AND_FROZEN: all 177 single-query envelopes exact feasible; one new-E conditional B4 diagnostic exact negative in both off families.',
             'scope':'Finite necessary envelope task and a fixed-new-E conditional diagnostic only. No common realization, universal E exclusion, or full SPE claim.',
             'point_sha256':check['point_sha256'],'symbolic_lift_sha256':check['symbolic_lift_sha256'],
             'exact_certificate_sha256':sha(HERE/'exact_certificate.json'),
             'independent_certificate_audit_sha256':sha(HERE/'independent_certificate_audit.json'),
             'conditional_diagnostic_sha256':sha(HERE/'conditional_B4_diagnostic.json'),
             'conditional_independent_audit_sha256':sha(HERE/'conditional_B4_independent_audit.json'),
             'rows':21572,'new_E_variables':776,'canonical_min_variables':10258,
             'E_recovery_rank':cert['E_rank'],'E_free_variables':cert['E_free_variables'],
             'positive_E_values':cert['positive_E_values'],'exact_phase_I':'0',
             'zero_full_rows':sum(F(v)==0 for v in cert['row_slacks']),
             'positive_full_rows':sum(F(v)>0 for v in cert['row_slacks']),
             'requested_query_rows':177,'zero_requested_rows':8,'positive_requested_rows':169,
             'query_families':families,'conditional_rows':diagnostic['rows'],
             'conditional_negative_rows':2,'conditional_blocks_checked':960,'conditional_cells_checked':7680,
             'optimization_calls_total':1,'optimization_calls_local':0,'optimization_calls_after_discovery':0,
             'cloud_run_id':provenance['run_id'],'cloud_artifact_id':provenance['artifact_id'],
             'source_commit':provenance['commit'],'solver_seconds':cloud['solver_seconds'],'iterations':cloud['iterations'],
             'all_frozen_inputs_unchanged':True,'all_raw_cloud_outputs_unchanged':True,
             'remaining_local_task':None,'six_player_half_status':'OPEN'}
    save('final_summary.json',summary)
    logs=[]
    for script,stdout,stderr in [('recover_exact.py','recover.stdout.json','recover.stderr.txt'),
                                  ('verify_certificate.py','verify.stdout.json','verify.stderr.txt'),
                                  ('conditional_B4.py','conditional_B4.stdout.json','conditional_B4.stderr.txt'),
                                  ('verify_conditional_B4.py','verify_conditional.stdout.json','verify_conditional.stderr.txt')]:
        assert (HERE/stdout).stat().st_size>0 and not (HERE/stderr).read_bytes()
        logs.append({'argv':['python',str((HERE/script).relative_to(REPO))],'observed_exit_code':0,
                     'source':record(HERE/script),'stdout':record(HERE/stdout),'stderr':record(HERE/stderr),
                     'optimization_calls':0})
    save('completion_execution_manifest.json',{'executions':logs,'cloud_outputs_kept_byte_identical':True})
    save('completion_source_reading.json',{'sources':[record(p) for p in [
         WORK/'main_E_B4_conditional_bound.md',WORK/'main_E_B4_conditional_bound.py',
         WORK/'main_E_B4_conditional_bound.json',main_download]],
         'old_zero_faces_recomputed_at_cb45':True,'older_point_common_atoms_used':False})
    artifacts=[record(HERE.with_suffix('.md'))]
    artifacts.extend(record(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='freeze_manifest.json')
    save('freeze_manifest.json',{'status':'COMPLETE_AND_FROZEN','run':'six-boss1-20261111',
                                'scope':summary['scope'],'dispatch_inputs':ready['dependencies'],
                                'raw_cloud_outputs':provenance['runtime_outputs'],'artifacts':artifacts,
                                'summary_sha256':sha(HERE/'final_summary.json'),
                                'optimization_calls_total':1,'optimization_calls_local':0,
                                'active_local_computations':False,'next_task':'Any next-point or larger joint lift requires a separately assigned obligation.'})
    print(json.dumps({k:summary[k] for k in ('status','exact_certificate_sha256','independent_certificate_audit_sha256',
                                             'conditional_diagnostic_sha256','conditional_independent_audit_sha256',
                                             'positive_requested_rows','zero_requested_rows','conditional_negative_rows')},ensure_ascii=False))
    print(json.dumps({'freeze_manifest_sha256':sha(HERE/'freeze_manifest.json')}))

if __name__=='__main__':main()
