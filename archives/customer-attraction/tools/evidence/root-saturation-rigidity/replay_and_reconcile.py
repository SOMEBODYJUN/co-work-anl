"""Unchanged original audit replay plus exact reconstruction of review identities.

The submitted 557-row point is input data for fixed-theme cut evaluation only.
No feasibility/optimality audit of that entire relaxation is performed here.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def share(numerator, denominator):
    return F(numerator, denominator) if numerator else F(0)


def rho(t, q, a, b, c):
    load = t+a+b+c
    return (-F(113,21)*t-F(q,1+4*t)+F(311,21)*share(t,load)
            +F(a,2)+F(31,42)*b+F(37,42)*c
            -F(5,21)*(share(b,load)-F(c,t+a+2))
            -share(c,load)+F(q,t+a+b+1))


def closed_minimum(t, a, b, c):
    if t == 0:
        return {(0,0):F(a*(a-1),2*(a+1)),
                (0,1):F(a*(21*a+37),42*(a+2)),
                (1,0):F(a*(21*a*a+52*a+41),42*(a+1)*(a+2)),
                (1,1):F(a,2)+F(13,21)}[b,c]
    return {(0,0):F(21*(2-a)**2+121*(2-a)+70,42*(a+1)),
            (0,1):F((2-a)*(313+21*a*(2-a)),42*(a+2)*(a+3)),
            (1,0):F((2-a)*(111-21*a),42*(a+2)),
            (1,1):F((2-a)*(53-21*a),42*(a+3))}[b,c]


def audit_review_contracts():
    # Expand the summed contract identity customer by customer.  Root u and
    # common bound K cancel symbolically; only the displayed local part remains.
    raw_checks = 0
    for t,q,a2,a3,b,c in product((0,1),repeat=6):
        a = a2+a3
        load = t+a+b+c
        weighted_contract_local = (
            -F(311,21)*share(t,load)-F(a,2)-F(31,42)*b-F(37,42)*c
            +F(5,21)*(share(b,load)-F(c,t+a+2))
            +share(c,load)-F(q,t+a+b+1))
        local_target = -F(113,21)*t-F(q,1+4*t)
        assert local_target == weighted_contract_local+rho(t,q,a,b,c)
        assert rho(t,q,a,b,c) >= 0
        raw_checks += 1
    table = []
    for t,a,b,c in product((0,1),range(3),(0,1),(0,1)):
        q_worst = 1-t
        exact = rho(t,q_worst,a,b,c)
        assert exact == closed_minimum(t,a,b,c)
        assert exact == min(rho(t,q,a,b,c) for q in (0,1))
        table.append({'t':t,'a':a,'b':b,'c':c,'q_worst':q_worst,
                      'rho':str(exact),'1260rho':str(1260*exact)})
    assert F(1,2)+F(1,2)+F(31,42)+F(37,42)==F(55,21)
    terminal_factors = []
    for n,z in product(range(4),(0,1)):
        c=1+n+z
        expense=F(3-n,2)+(1-z)*(1-F(1,c))
        residual=15*(F(1,c)-F(1,5))-expense
        factored=(F((n-3)*(n-7),2*(n+1)) if z==0
                  else F((3-n)*(4-n),2*(n+2)))
        assert residual==factored>=0
        terminal_factors.append({'n':n,'z':z,'residual':str(residual)})
    return {'scope':'supplementary reconstruction from the claimed review contracts; no discovery LP, no SPE enumeration',
            'raw_identity_and_nonnegativity_states':raw_checks,
            'compressed_states_including_q':48,
            'closed_form_worst_q_states':len(table),
            'closed_form_table':table,
            'original_terminal_expense_factor_states':terminal_factors,
            'common_size_coefficient_sum':'55/21',
            'general_coverage_coefficient_at_m5':'267/10',
            'strengthened_coverage_coefficient_at_m5':'2741/105'}


def main():
    replay=HERE/'replay'
    replay.mkdir(exist_ok=True)
    input_path=HERE/'inputs/exact_primal_overlap1.json'
    input_hash=hashlib.sha256(input_path.read_bytes()).hexdigest()
    assert input_hash=='11a26c56faca5a3331a4f2ab002455aa6ca115f999ddde2eced6f1edd39c0825'
    with tempfile.TemporaryDirectory(prefix='root-rigidity-replay-') as directory:
        root=Path(directory)
        # Original code uses this file's existence only to locate its root.
        (root/'AGENTS.md').write_text('Replay fixture root marker.\n')
        script=root/'source/audit_root_rigidity.py'
        script.parent.mkdir()
        shutil.copyfile(HERE/'source/audit_root_rigidity.py',script)
        fixture_input=root/'inputs/exact_primal_overlap1.json'
        fixture_input.parent.mkdir()
        shutil.copyfile(input_path,fixture_input)
        run=subprocess.run([sys.executable,str(script),str(fixture_input)],
                           cwd=root,text=True,capture_output=True,check=True)
        assert not run.stderr,run.stderr
        (replay/'audit_root_rigidity.stdout.txt').write_text(run.stdout)
        generated=script.with_suffix('.json').read_bytes()
        (replay/'audit_root_rigidity.json').write_bytes(generated)
    original=json.loads((HERE/'original/audit_root_rigidity.json').read_bytes())
    actual=json.loads(generated)
    assert len(original['points'])==len(actual['points'])==1
    source_change={'original':original['points'][0]['source'],
                   'replay':actual['points'][0]['source']}
    comparable=json.loads(generated)
    comparable['points'][0]['source']=original['points'][0]['source']
    assert comparable==original
    supplement=audit_review_contracts()
    (replay/'review_contract_reconstruction.json').write_text(json.dumps(supplement,indent=2)+'\n')
    report={'scope':'unchanged original implementation replay; input source-path difference separated from exact mathematical fields',
            'original_script_unchanged':True,'stderr_empty':True,
            'all_mathematical_fields_equal':True,'byte_equality_claimed':False,
            'environment_only_field_difference':{'points[0].source':source_change},
            'input_sha256':input_hash,
            'input_scope':'60 atoms used for fixed-theme cuts only; no validation of all 557 rows or relaxation optimum',
            'local_algebra_cases':actual['local_algebra_audit']['cases'],
            'fixed_pairs':actual['points'][0]['fixed_pairs_checked'],
            'negative_rows':actual['points'][0]['negative_rows'],
            'review_raw_identity_states':supplement['raw_identity_and_nonnegativity_states'],
            'review_closed_form_states':supplement['closed_form_worst_q_states']}
    (replay/'reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
