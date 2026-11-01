"""One authorized 160-corner check of the repaired scalar root compression.

No original audit, SPE solver, IC loop, or LP is imported or run.
The printed 17d coefficient and repaired 65d coefficient are both retained.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
C=HERE.parents[1]
MP=C/'resumed-next-three_terminal_transfer_three-originals/actual-source-manifest.json'

def compressed(a,b,c,d,q1,q0,d_coefficient):
    k=1+a+b
    D=(1+a)*(2+a)
    counts={(1,1):q1,(1,0):d-q1,(0,1):q0,(0,0):3-d-q0}
    J=sum((F(n,1+t+v) for (t,v),n in counts.items()),F(0))
    r_coeff={}
    for t,v in product((0,1),repeat=2):
        r_coeff[t,v]=-F(t,(1+v)*(2+v))-F(1,8*(1+t+v))+F(1,4*(1+a))-F(d,12*D)
    value=(F(7,3)*int(a+b+c>0)-3*int(d>0)+F(d,1+a)
           +F(3*c,4)*(F(3,1+a)-F(d,D))
           +(F(d_coefficient*d,48)+F(7*(q1+q0),48)-F(9*c,2))/k
           +d-F(q1,2)+F(c,8)*J
           +3*(F(1,k)-F(1,1+a))
           +sum((counts[t,v]*min(F(0),r_coeff[t,v])for t,v in counts),F(0)))
    return value,counts,J,r_coeff

def main():
    report_path=HERE/'corrected-root-compression-report.json'
    if report_path.exists():
        raise RuntimeError('The one-shot report already exists; do not rerun.')
    manifest=json.loads(MP.read_text())
    primary=manifest['rows']
    frozen_path=next(Path(x['local_path'])for x in primary if x['id']=='7fde0e258a567562a399')
    frozen=json.loads(frozen_path.read_text())
    rows=[]
    tables={}
    old_tables={}
    argmins={}
    for a,b,c in product((0,1),repeat=3):
        abc=''.join(map(str,(a,b,c)))
        for d in range(4):
            key=abc+':'+str(d)
            candidates=[]
            old_candidates=[]
            for q1 in range(d+1):
                for q0 in range(4-d):
                    fixed,counts,J,coefs=compressed(a,b,c,d,q1,q0,65)
                    printed,_,_,_=compressed(a,b,c,d,q1,q0,17)
                    assert fixed-printed==F(d,1+a+b)
                    rows.append(dict(abc=abc,d=d,q1=q1,q0=q0,
                                     class_counts={str(k):v for k,v in counts.items()},
                                     J=str(J),r_coefficients={str(k):str(v)for k,v in coefs.items()},
                                     printed_17d_minimum=str(printed),corrected_65d_minimum=str(fixed)))
                    candidates.append((fixed,q1,q0))
                    old_candidates.append(printed)
            value=min(x[0]for x in candidates)
            tables[key]=str(value)
            old_tables[key]=str(min(old_candidates))
            argmins[key]=[[q1,q0]for v,q1,q0 in candidates if v==value]
    assert len(rows)==160 and len(tables)==32
    counter=next(x for x in rows if(x['abc'],x['d'],x['q1'],x['q0'])==('000',1,1,0))
    assert counter['printed_17d_minimum']=='-1' and counter['corrected_65d_minimum']=='0'
    matches={name:tables==entry['root_compressed_minima']for name,entry in frozen.items()}
    report=dict(scope='one independent 160-corner Fraction check of repaired Eq(5); not original 32768x2 audit, SPE, IC, or LP',
                python=sys.version,process_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                frozen_sources=[dict(id=x['id'],size=x['size'],sha256=x['sha256'],blob=x['blob'])for x in primary],
                frozen_report_sha256=hashlib.sha256(frozen_path.read_bytes()).hexdigest(),
                printed_root_d_coefficient='17/48',corrected_root_d_coefficient='65/48',missing_term='d/(1+a+b)',
                corner_count=len(rows),table_groups=len(tables),all_actual_corner_inputs_and_outputs=rows,
                corrected_32_table=tables,printed_17d_32_table=old_tables,all_corrected_argmins=argmins,
                explicit_printed_formula_counterexample=counter,
                all_corrected_minima_nonnegative=all(F(v)>=0 for v in tables.values()),
                matches_both_frozen_benchmark_root_tables=matches,
                targeted_compressed_check_runs=1,new_original_audit_runs=0,new_SPE_or_IC_or_LP_runs=0)
    with report_path.open('x')as handle:
        handle.write(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    assert report['all_corrected_minima_nonnegative'] and all(matches.values())
    print(json.dumps({k:v for k,v in report.items()if k not in ['all_actual_corner_inputs_and_outputs','all_corrected_argmins','frozen_sources']},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
