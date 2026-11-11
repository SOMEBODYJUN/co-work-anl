"""Write provenance and the exact Actions handoff.  No optimization."""
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
REPO=WORK.parents[2]

def sha(p):return sha256(p.read_bytes()).hexdigest()
def save(n,d):(HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def record(p):return {'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size}

def main():
    sources=[WORK/'z_successor_20910.md',WORK/'z_successor_20910/derivation.md',
             WORK/'z_successor_20910/symbolic_lift.json',WORK/'z_successor_20910/exact_certificate.json',
             WORK/'z_successor_20910/literal_audit.py',WORK/'z_successor_20910/build.py',
             WORK/'full624_augmented_lp/recovery/augmented_lp_exact.json',
             WORK/'common_network_19662.md',WORK/'main_z_successor_contract.md',
             REPO/'AGENTS.md',
             REPO/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
             REPO/'archives/customer-attraction/subarchives/six-providers/问题--问题.md',
             REPO/'archives/customer-attraction/state/方法/同源末主题重查询与共享变量消元--方法.md',
             REPO/'archives/customer-attraction/state/引理/共享真实末回复的组合查询投影与同源重配权--引理.md']
    save('source_reading.json',{'sources':[record(p) for p in sources],
                              'older_network_used_only_as_formula_method':True,
                              'old_common_atoms_read_or_migrated':False})
    deps=[HERE/'actions_phase1.py',HERE/'symbolic_lift.json.gz',HERE/'preflight_literal_audit.json',
          WORK/'full624_augmented_lp/recovery/augmented_lp_exact.json']
    audit=json.loads((HERE/'preflight_literal_audit.json').read_bytes())
    assert audit['passed'] and audit['all_rows_checked']==21572
    save('actions_ready.json',{
        'status':'READY for exactly one Actions phase I; no optimizer called locally',
        'run':'six-boss1-20261111','scope':'Complete free-E single-query envelope lift',
        'dependencies':[record(p) for p in deps],
        'argv':['python',str((HERE/'actions_phase1.py').relative_to(REPO)),'--seconds','1800'],
        'requirements':['numpy','scipy'],'solver':'highs-ds','linprog_calls_authorized':1,
        'solver_time_limit_seconds':1800,'recommended_workflow_timeout_minutes':40,
        'phase_I_shape':[21572,11035],'new_E_columns':776,'min_auxiliaries':10258,
        'output_path':str((HERE/'actions_output').relative_to(REPO)),
        'retained_outputs':['started.json','prepared_input.json','phase_I_matrix.npz','phase_I_vectors.npz',
                            'phase_I_input_order.json.gz','executed_actions_phase1.py','phase_I_discovery.json',
                            'phase_I_solution.npz'],
        'failure_policy':'Retain failure/timeout and input order; no automatic repeat or second optimization.',
        'after_discovery':'Exact primal recovery with canonical min, or exact Farkas eliminating all 11034 new columns; independent literal audit required.',
        'local_optimization_calls':0})
    save('failure_log.json',{'failures':[{
        'step':'First build_envelopes.py parse, before any matrix or optimizer',
        'exception':'KeyError: ((0, 0, (0, 0, 1), (0, 0, 1)), E)',
        'cause':'joint-reply.hist_column_old is the pre-expansion legacy hist index, not the current 4849-column index.',
        'repair':'Associate each joint-reply with its enclosing current hist block, as in both frozen independent parser and source builder.',
        'consequence':'No mathematical inference or optimization used the failed parse; all final symbolic rows independently reconstructed.',
        'preserved_source':'failures/build_legacy_hist.py'}]})
    failed=HERE/'failures';failed.mkdir(exist_ok=True)
    source=(HERE/'build_envelopes.py').read_text()
    source=source.replace("if c['kind']=='hist': h=j;hist[j]=c","if c['kind']=='hist': hist[j]=c")
    source=source.replace("            # hist_column_old is a legacy index; the surrounding hist block\n            # determines the present 4849-column coordinate.\n            old[h].setdefault(group(c['group']),{})[tuple(c['state'])]=j",
                          "            old[c['hist_column_old']].setdefault(group(c['group']),{})[tuple(c['state'])]=j")
    (failed/'build_legacy_hist.py').write_text(source)
    save('checkpoint_manifest.json',{'inputs':[record(p) for p in sources],
                                    'artifacts':[record(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='checkpoint_manifest.json'],
                                    'status':'ready for single Actions discovery','optimization_calls':0})
    print(json.dumps({'ready_sha256':sha(HERE/'actions_ready.json'),
                      'audit_sha256':sha(HERE/'preflight_literal_audit.json'),
                      'source_sha256':sha(HERE/'actions_phase1.py')}))

if __name__=='__main__':main()
