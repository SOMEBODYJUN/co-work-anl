"""Main's independent analytic rederivation of the shared-max-B cut.

Read only the exact old point and frozen final Farkas row.  Do not import
the lift, its constructor, its auditor, or an optimizer.  Rebuild every
hist coefficient and prove the five-budget expansion in all 3360 Boolean
count cases of a six-player source with a four-action prefix.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
PP=HERE/'full624_augmented_lp/recovery/augmented_lp_exact.json'
CP=HERE/'terminal_response_cycles/max_b_exact_certificate.json'
assert sha256(PP.read_bytes()).hexdigest()=='cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
assert sha256(CP.read_bytes()).hexdigest()=='f6189600d6ccccdbd9fcbc4ae4af9e768c9382af8de1ae41d6e6a7ee7662f664'
point=json.loads(PP.read_bytes());cert=json.loads(CP.read_bytes())

def quote(n,d):
    assert d or n==0
    return F(n,d) if n else F()

def terms(P,a5,a6,dB,dC,dBC):
    D=(P+1)*(P+2);n=P+a5+a6
    u5=quote(a5,n);u6=quote(a6,n)
    kappa=F(12*a6+24*a5+6*dC-(P+2)*(P+9),D)
    bare=64*u5+24*u6-F(12*a6,P+1)-F(16*dB+52*dC,6*(P+1))+F(16*dBC,6*D)
    return bare,kappa,u5,u6

case_count=0
for P,a5,a6,x in product(range(5),(0,1),(0,1),(0,1)):
    D=(P+1)*(P+2)
    for dB,dC in product(range(7),repeat=2):
        for dBC in range(max(0,dB+dC-6),min(dB,dC)+1):
            bare,kappa,u5,u6=terms(P,a5,a6,dB,dC,dBC)
            capA=u5-F(a6,P+1)+F(a6*x,D)
            capC=u5-F(dC,6*(P+1))+F(dC*x,6*D)
            actual6=u6-F(x,P+a5+1)
            capacity=-x  # The separate global +K coefficient is exactly 1.
            pair=u5+F(x,P+1)-F(dB+dC,6*(P+1))+F(dBC,6*D)
            combo=12*capA+36*capC+24*actual6+capacity+16*pair
            assert combo==bare+kappa*x
            assert max(kappa,F())-kappa*x>=0
            case_count+=1
assert case_count==3360

row={0:F(1)};table=[]
for j,c in enumerate(point['columns'][:4849]):
    if c['kind']!='hist':continue
    a=tuple(map(int,c['actual_bits']));P=sum(a[:4])
    dB=sum(n*((w>>1)&1) for w,n in enumerate(c['hist']))
    dC=sum(n*(w&1) for w,n in enumerate(c['hist']))
    dBC=sum(n*int((w&3)==3) for w,n in enumerate(c['hist']))
    bare,kappa,_,_=terms(P,a[4],a[5],dB,dC,dBC)
    coef=bare+max(kappa,F())
    if coef:row[j]=coef
    table.append(dict(column=j,actual_bits=c['actual_bits'],dB=dB,dC=dC,dBC=dBC,
                      kappa=str(kappa),positive_part=str(max(kappa,F())),coefficient=str(coef)))
expected={j:F(v) for j,v in cert['sparse_original4849_row_K_normalized']}
assert row==expected and len(row)==17 and len(table)==16
value=sum((v*F(point['columns'][j]['weight']) for j,v in row.items()),F())
assert value==F(cert['K_normalized_point_value'])<0
assert 3*value==F(cert['exact_point_value'])
report=dict(status='MAIN_INDEPENDENT_ANALYTIC_MAXB_CUT_PASS',
            point_sha256=sha256(PP.read_bytes()).hexdigest(),certificate_sha256=sha256(CP.read_bytes()).hexdigest(),
            source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
            all_Boolean_count_cases=case_count,original_histograms=len(table),
            nonzero_original_coefficients=len(row),zero_auxiliary_columns=20585-4849,
            K_normalization='1',row=[[j,str(v)] for j,v in sorted(row.items())],
            exact_old_point_value=str(value),old_point_value_float=float(value),
            hist_table=table,
            scope='Universal necessary row from a single common max-B label and five exact budgets; negative value excludes only the fixed cb45 necessary-system point.',
            no_optimization=True,no_complete_SPE_claim=True)
(HERE/'main_maxb_cut_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('hist_table','row')},ensure_ascii=False))
