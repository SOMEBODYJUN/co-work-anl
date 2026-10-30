"""Replay the same-author separate audit, then check every stored exact record.

The discovery producer is loaded only for its exact rows function.  Its run()
and scipy linprog are not invoked.  Stored active sets and recovery history are
not reconstructed or represented as newly replayed floating searches.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import runpy
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent


def alternate_credit_summary(records):
    """Derive six-point credit metadata from the already checked stored report."""
    old=records[1]
    alternate=records[3]
    other_pair=records[5]
    assert (old['B'],old['C'])==(alternate['B'],alternate['C'])
    assert old['multipliers']!=alternate['multipliers']
    new_e=list(map(F,alternate['residual_spectrum_d0_to_d5']))
    old_e=list(map(F,old['residual_spectrum_d0_to_d5']))
    assert new_e==list(map(F,other_pair['residual_spectrum_d0_to_d5']))
    differences=[]
    alpha=F(297,35060)
    for d in range(6):
        assert new_e[d]==F(max(d-1,0),5)+alpha*max(d-1,0)*(4-d)
        difference=new_e[d]-old_e[d]
        assert difference==F(297,35060)*max(d-1,0)*(20-d)>=0
        differences.append(str(difference))
    B,C=F(alternate['B']),F(alternate['C'])
    coefficients=[35060*(F(4,5)-4*alpha),35060*(F(1,5)+5*alpha),
                  -35060*alpha,35060*C,35060*B]
    assert coefficients==[26860,8497,-297,291470,1781800]
    return {'scope':'metadata and exact six-point algebra derived from the completed all-stored-record check; no repeated coefficient-domain audit',
            'source_record_indices':[3,4],'rho_values':['23/100','6/25'],
            'B':alternate['B'],'C':alternate['C'],
            'alternate_multipliers':alternate['multipliers'],
            'old_O_envelope_spectrum':list(map(str,old_e)),
            'alternate_spectrum':list(map(str,new_e)),
            'nonnegative_credit_improvements':differences,
            'difference_formula':'297 (d-1)_+ (20-d) / 35060',
            'integer_O_D_S2_K_u_coefficients':list(map(str,coefficients))}


def main():
    replay=HERE/'replay'
    replay.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='maxroot-record-replay-') as directory:
        folder=Path(directory)
        audit=folder/'audit_maxroot_envelope.py'
        producer=folder/'maxroot_envelope.py'
        shutil.copyfile(HERE/'source/audit_maxroot_envelope.py',audit)
        shutil.copyfile(HERE/'source/maxroot_envelope.py',producer)
        shutil.copyfile(HERE/'original/maxroot_envelope.json',folder/'maxroot_envelope.json')
        run=subprocess.run([sys.executable,str(audit)],text=True,capture_output=True,check=True)
        assert not run.stderr,run.stderr
        generated=audit.with_suffix('.json').read_bytes()
        original=(HERE/'original/audit_maxroot_envelope.json').read_bytes()
        assert generated==original
        (replay/'audit_maxroot_envelope.json').write_bytes(generated)
        (replay/'audit_maxroot_envelope.stdout.json').write_text(run.stdout)
        namespace=runpy.run_path(str(producer),run_name='exact_rows_only_no_discovery')
        rows=namespace['rows']
        data=json.loads((folder/'maxroot_envelope.json').read_bytes())
        atoms=[(b,d) for b in product((0,1),repeat=5) for d in range(6)]
        assert data['atoms']==[[list(b),d] for b,d in atoms]
        assert data['row_names']==list(rows(*atoms[0]))
        table={(b,d):rows(b,d) for b,d in atoms}
        assert len(data['records'])==11 and len(data['row_names'])==49
        results=[]
        for index,record in enumerate(data['records']):
            rho,beta,B,C=map(F,(record['rho'],record['value'],record['B'],record['C']))
            weights={name:F(value) for name,value in record['multipliers'].items()}
            assert all(value>=0 for value in weights.values())
            assert weights.get('root-IC',F(0))==B and C==B*rho-beta
            residuals={}
            for b,d in atoms:
                c=b[0];V=F(c,sum(b)) if c else F(0)
                supported={name:value for name,value in weights.items() if name!='root-IC'}
                formal=B*V-C*c-int(d>0)-sum(value*table[b,d][name]
                                            for name,value in supported.items())
                discovery=beta*c-int(d>0)-sum(value*(rho*c-V if name=='root-IC' else table[b,d][name])
                                               for name,value in weights.items())
                assert formal==discovery and formal>=0,(index,b,d,formal)
                residuals[b,d]=formal
            assert min(residuals.values())==F(record['minimum_residual'])==0
            spectrum=[min(value for (b,dd),value in residuals.items() if dd==d)
                      for d in range(6)]
            results.append({'record_index':index,'rho':str(rho),'value':str(beta),
                            'B':str(B),'C':str(C),
                            'multipliers':record['multipliers'],
                            'checked_atoms':len(atoms),'minimum_residual':'0',
                            'zero_residuals':sum(value==0 for value in residuals.values()),
                            'residual_spectrum_d0_to_d5':list(map(str,spectrum)),
                            'discovery_to_universal_identity_verified':True})
    groups={}
    for record in results:
        signature=json.dumps([record['B'],record['C'],record['multipliers']],sort_keys=True)
        groups.setdefault(signature,[]).append(record['rho'])
    exact={'scope':'all 11 stored records evaluated from unchanged author rows; no floating discovery, no primal optimality or full candidate-row semantic audit',
           'row_catalogue_count':49,'records':results,
           'distinct_B_C_pairs':len({(r['B'],r['C']) for r in results}),
           'distinct_B_C_multiplier_representations':len(groups),
           'representation_rho_groups':list(groups.values()),
           'total_record_type_pairs':len(results)*len(atoms)}
    (replay/'all_stored_records_exact.json').write_text(json.dumps(exact,indent=2)+'\n')
    (replay/'alternate_representation_credit.json').write_text(
        json.dumps(alternate_credit_summary(results),indent=2)+'\n')
    report={'scope':'same-author separate implementation replay plus complete stored-record exact evaluation; no historical LP/recovery replay',
            'original_audit_report_bytes_equal':True,
            'original_audit_report_sha256':hashlib.sha256(original).hexdigest(),
            'same_author_separate_audit_certificates':len(json.loads(generated)['certificates']),
            'full_record_count':len(results),'types_per_record':192,
            'full_record_type_pairs':len(results)*len(atoms),
            'distinct_B_C_pairs':exact['distinct_B_C_pairs'],
            'distinct_B_C_multiplier_representations':len(groups),
            'floating_discovery_run_invoked':False,
            'original_solve_exact_invoked':False,'stderr_empty':True}
    (replay/'reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
