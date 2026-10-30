"""Unchanged original COPY audit replay and exact report reconciliation.

Supplementary checks use the submitted complete residual table, not a discovery
solver.  This is not a new independent implementation of the raw contracts.
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


def main():
    replay=HERE/'replay'
    replay.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='copy-rigidity-replay-') as directory:
        script=Path(directory)/'audit_copy_reply_rigidity.py'
        shutil.copyfile(HERE/'source/audit_copy_reply_rigidity.py',script)
        run=subprocess.run([sys.executable,str(script)],text=True,capture_output=True,check=True)
        assert not run.stderr,run.stderr
        generated=script.with_suffix('.json').read_bytes()
    original=(HERE/'original/audit_copy_reply_rigidity.json').read_bytes()
    assert generated==original
    out=json.loads(generated)
    assert len(out['all_128_residuals'])==128
    values={tuple(row['bits']):F(row['rho']) for row in out['all_128_residuals']}
    assert len(values)==128 and min(values.values())==0
    table={(row['T'],row['B2_plus_B3'],row['copy_reply_C']):
           row['scaled_rho_B4B5_00_01_10_11']
           for row in out['compressed_complete_nonnegative_table']}
    assert len(table)==12 and out['table_scale']==900
    compressed_checks=0
    for t,a,d,b,c in product((0,1),range(3),(0,1),(0,1),(0,1)):
        orders=[(x,y) for x,y in product((0,1),repeat=2) if x+y==a]
        pairs=[]
        for a2,a3 in orders:
            by_q=[values[t,q,a2,a3,b,c,d] for q in (0,1)]
            coefficient=-F(1,1+4*t)+F(14,15*(t+a+b+1))+F(1,15*(t+a+c+1))
            assert by_q[1]-by_q[0]==coefficient
            assert (coefficient<=0 if t==0 else coefficient>=0)
            assert by_q[1-t]==min(by_q)
            assert 900*by_q[1-t]==table[t,a,d][2*b+c]
            pairs.append(by_q)
        assert all(pair==pairs[0] for pair in pairs)
        compressed_checks+=1
    weights={key:F(value) for key,value in out['dual'].items()}
    assert len(weights)==9 and all(value>=0 for value in weights.values())
    assert sum(weights['K_B'+str(j)] for j in range(2,6))==F(13,5)
    assert 5*F(44,3)==F(220,3)
    assert 5*F(13,5)==13
    assert 5*F(16,3)-F(4,5)==F(388,15)
    assert 15*F(220,3)==1100 and 15*(13-F(388,15))==-193
    difference={'u':str(F(44,3)-F(311,21)),
                'K':str(F(13,5)-F(55,21)),
                'T_size':str(-F(16,3)+F(113,21))}
    assert difference=={'u':'-1/7','K':'-2/105','T_size':'1/21'}
    (replay/'audit_copy_reply_rigidity.json').write_bytes(generated)
    (replay/'audit_copy_reply_rigidity.stdout.json').write_text(run.stdout)
    assert json.loads(run.stdout)=={k:v for k,v in out.items() if k!='all_128_residuals'}
    report={'scope':'unchanged original implementation replay plus report-level worst-q, compression and coefficient checks; not a new independent raw-contract audit',
            'original_report_bytes_equal':True,
            'original_report_sha256':hashlib.sha256(original).hexdigest(),
            'stderr_empty':True,'raw_membership_count':len(values),
            'raw_zero_residuals':sum(value==0 for value in values.values()),
            'compressed_memberships_including_q':96,
            'worst_q_compressed_values_checked':compressed_checks,
            'table_scale':out['table_scale'],
            'nonnegative_contract_count':len(weights),
            'size_cap_weight_sum':'13/5',
            'new_minus_113_21_coefficients':difference,
            'coverage_coefficients':{'u':'220/3','K':'13','T_size':'-388/15'},
            'maximum_theme_integer_row':'15 OPT_5 + 193 K <= 1100 u'}
    (replay/'reconciliation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
