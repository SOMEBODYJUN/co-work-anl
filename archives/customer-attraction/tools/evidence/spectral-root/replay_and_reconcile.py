"""Unchanged original seven-certificate spectral audit and aggregation checks.

The supplemental moment, COPY and LAST-SOURCE calculations are kept separate
from the original 7*192 coefficient reconstruction; no strategy search is run.
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

HERE=Path(__file__).resolve().parent
SPECS={
    'old':(F(1,5),F(0),5,(4,1,0,71,400)),
    'O-envelope':(F(113,1753),F(0),3506,(3280,226,0,29147,178180)),
    'pair-envelope':(F(1,5),F(297,35060),35060,(26860,8497,-297,97020,1004000)),
    'pair-envelope-2':(F(1,5),F(1013,119440),119440,(91500,28953,-1013,323195,3391425)),
    'third-source-A':(F(3,59),F(0),118,(112,6,0,1009,6140)),
    'third-source-B':(F(3,59),F(0),59,(56,3,0,187,1800)),
    'third-source-C':(F(3,59),F(0),236,(224,12,0,613,6660))}


def supplement(records):
    projections=[]
    for record in records:
        name=record['name']
        slope,alpha,scale,expected=SPECS[name]
        values=list(map(F,record['e_d']))
        for d in range(6):
            assert values[d]==slope*max(0,d-1)+alpha*max(0,d-1)*(4-d)
            assert max(0,d-1)==d-int(d>0)
            assert max(0,d-1)*(4-d)==5*d-d*d-4*int(d>0)
        coefficients=(scale*(1-slope-4*alpha),scale*(slope+5*alpha),
                      -scale*alpha,scale*F(record['C']),scale*F(record['B']))
        assert coefficients==expected
        projections.append({'name':name,'scale':scale,
                            'integer_O_D_S2_K_u_coefficients':list(map(str,coefficients))})
    copy_values=[]
    for d in range(6):
        membership=[int(i<d) for i in range(5)]
        total=sum((F(membership[j],1+4*membership[i])
                   for i,j in product(range(5),repeat=2)),F(0))
        assert total==5*d-F(4,5)*d*d
        copy_values.append(str(total))
    assert 25*F(44,3)*15==5500
    assert 25*F(13,5)*15==975
    assert (5*F(16,3)+5)*15==475
    assert F(4,5)*15==12
    last_values=[]
    for a,t,q in product(range(5),(0,1),(0,1)):
        residual=F(a,2)-4*t+F(10*t,a+1)-q*(1-F(4*t,5))+F(q,a+1)
        assert residual>=0
        if t==1 and q==0:
            assert residual==F((4-a)*(3-a),2*(a+1))
        if t==0:
            assert residual==F(a,2)-F(q*a,a+1)
        last_values.append({'a':a,'maximum_membership':t,'query_membership':q,
                            'residual':str(residual)})
    last_aggregation=[]
    for t,d in product((0,1),range(6)):
        residual=5*d*(1-F(4*t,5))-(4*int(d>0)+d-4*t)
        assert residual>=0
        last_aggregation.append({'maximum_membership':t,'optimal_multiplicity':d,
                                 'residual':str(residual)})
    assert 118*2+992==1228
    assert F(1009)*F(992,1009)==992
    return {'scope':'supplemental exact aggregation/factor checks, distinct from the original seven 192-state audits',
            'moment_projections':projections,
            'COPY_optimal_ordered_pair_sums_d0_to_d5':copy_values,
            'COPY_moment_row':'5500 u + 975 K - 475 D + 12 S2 >= 0',
            'LAST_SOURCE_local_states':last_values,
            'LAST_SOURCE_optimal_aggregation_states':last_aggregation,
            'conditional_half_threshold':'K >= (992/1009) W',
            'conditional_half_arithmetic_verified':True}


def main():
    replay=HERE/'replay'
    replay.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='spectral-root-replay-') as directory:
        script=Path(directory)/'audit_spectral_root.py'
        shutil.copyfile(HERE/'source/audit_spectral_root.py',script)
        run=subprocess.run([sys.executable,str(script)],text=True,capture_output=True,check=True)
        assert not run.stderr,run.stderr
        generated=script.with_suffix('.json').read_bytes()
    original=(HERE/'original/audit_spectral_root.json').read_bytes()
    assert generated==original
    out=json.loads(generated)
    assert len(out['records'])==7
    assert all(record['checked_types']==192 for record in out['records'])
    assert json.loads(run.stdout)==out
    (replay/'audit_spectral_root.json').write_bytes(generated)
    (replay/'audit_spectral_root.stdout.json').write_text(run.stdout)
    extra=supplement(out['records'])
    (replay/'aggregation_checks.json').write_text(json.dumps(extra,indent=2)+'\n')
    report={'scope':'unchanged original implementation replay; supplemental aggregation checks separately recorded; no new independent raw-row audit',
            'original_report_bytes_equal':True,
            'original_report_sha256':hashlib.sha256(original).hexdigest(),
            'stderr_empty':True,'certificate_records':7,'types_per_certificate':192,
            'total_certificate_type_pairs':1344,
            'record_summaries':[{'name':r['name'],
                                 'minimum_enhanced_residual':r['minimum_enhanced_residual'],
                                 'enhanced_zero_types':r['enhanced_zero_types']}
                                for r in out['records']],
            'supplemental_LAST_SOURCE_local_types':20,
            'supplemental_LAST_SOURCE_aggregation_types':12}
    (replay/'reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
