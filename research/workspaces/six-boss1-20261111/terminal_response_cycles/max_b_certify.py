"""Recover one exact Farkas row and its all-customer-type analytic projection.

No optimizer is called.  Float dual values only nominate the small rational
multiplier vector; every sign, cancellation and point value is then exact.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import gcd, lcm
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
OLD=4849


def add(r,j,v):
    r[j]=r.get(j,Q())+v
    if not r[j]:del r[j]


def serial(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [serial(x) for x in v]
    return v


def sparse(r):return [[j,str(v)] for j,v in sorted(r.items()) if v]


def main():
    data=json.loads((HERE/'max_b_symbolic_lift.json').read_bytes())
    discovered=json.loads((HERE/'max_b_phase_I.json').read_bytes())
    audit=json.loads((HERE/'max_b_independent_preflight.json').read_bytes())
    sh=sha256((HERE/'max_b_symbolic_lift.json').read_bytes()).hexdigest()
    assert audit['status']=='passed' and audit['symbolic_lift_sha256']==sh
    assert discovered['symbolic_lift_sha256']==sh and discovered['linprog_calls']==1
    rows=[{j:Q(v) for j,v in r['row']} for r in data['rows']]
    lam={i:Q(-v).limit_denominator(1000000) for i,v in enumerate(discovered['inequality_marginals']) if v < -1e-8}
    assert len(lam)==10 and min(lam.values())>0 and sum(lam.values())==1
    denominator=lcm(*(v.denominator for v in lam.values()))
    assert denominator==331
    integer={i:v*denominator for i,v in lam.items()}
    combined={}
    for i,v in integer.items():
        for j,c in rows[i].items():add(combined,j,v*c)
    oldrow={j:c for j,c in combined.items() if j<OLD}
    newrow={j:c for j,c in combined.items() if j>=OLD}
    assert len(oldrow)==17 and len(newrow)==5 and max(newrow.values())<0
    assert all(data['new_columns'][j-OLD]['kind']=='common-X-mass' for j in newrow)
    mu={j:-c for j,c in newrow.items()}
    fullcheck=dict(combined)
    for j,c in mu.items():add(fullcheck,j,c)
    assert fullcheck==oldrow
    pp=WORK/'full624_augmented_lp/recovery/augmented_lp_exact.json'
    assert sha256(pp.read_bytes()).hexdigest()==data['point_sha256']
    point=json.loads(pp.read_bytes());values=[Q(c['weight']) for c in point['columns']]
    val=sum((c*values[j] for j,c in oldrow.items()),Q())
    assert val<0

    # Reconstruct the projected row without referring to any selected LP rows.
    # This formula is meaningful on every actual six-bit/C-menu customer type.
    universal={0:Q(3)};hist_table=[]
    for j,c in enumerate(point['columns'][:OLD]):
        if c['kind']!='hist':continue
        bits=tuple(map(int,c['actual_bits']));p=sum(bits[:4]);D=(p+1)*(p+2);total=sum(bits)
        a5,a6=bits[4:]
        dc=db=dbc=0
        for word,n in zip(product((0,1),repeat=3),c['hist']):
            db+=word[1]*n;dc+=word[2]*n;dbc+=word[1]*word[2]*n
        aa=Q(a5,total) if a5 else Q();bb=Q(a6,total) if a6 else Q()
        kappa=Q(36*a6+72*a5+18*dc-(p+2)*(3*p+27),D)
        base=192*aa+72*bb-Q(36*a6,p+1)-Q(8*db+26*dc,p+1)+Q(8*dbc,D)
        coeff=base+max(Q(),kappa)
        add(universal,j,coeff)
        hist_table.append({'hist_column':j,'actual_bits':c['actual_bits'],'P':p,
                           'd_B':db,'d_C':dc,'d_BC':dbc,'kappa':str(kappa),
                           'positive_part':str(max(Q(),kappa)),'row_coefficient':str(coeff)})
    assert universal==oldrow
    simplified={j:c/3 for j,c in oldrow.items()}

    # Universal Boolean remainder check on every feasible pair-menu count.
    checks=0
    for p in range(5):
        D=(p+1)*(p+2)
        for a5,a6,xx in product((0,1),repeat=3):
            total=p+a5+a6
            aa=Q(a5,total) if a5 else Q();bb=Q(a6,total) if a6 else Q()
            for n00 in range(7):
                for n01 in range(7-n00):
                    for n10 in range(7-n00-n01):
                        n11=6-n00-n01-n10
                        B=Q(n10+n11,6);C=Q(n01+n11,6);BC=Q(n11,6)
                        capA=aa-Q(a6,p+1)+Q(a6*xx,D)
                        capC=aa-C/Q(p+1)+C*xx/Q(D)
                        quote=bb-Q(xx,p+1)+Q(a5*xx,D)
                        rc=aa+Q(xx,p+1)-(B+C)/Q(p+1)+BC/Q(D)
                        composed=36*capA+108*capC+72*quote-3*xx+48*rc
                        base=192*aa+72*bb-Q(36*a6,p+1)-(48*B+156*C)/Q(p+1)+48*BC/Q(D)
                        kappa=Q(36*a6+72*a5,D)+108*C/Q(D)-Q(24,p+1)-3
                        assert composed==base+kappa*xx
                        assert max(Q(),kappa)-kappa*xx>=0
                        checks+=1
    assert checks==3360
    cert={'status':'exact-negative-row-certified','scope':'Universal necessary analytic row; its negative evaluation excludes the cb45 16-hist point, not the six-player theorem.',
          'point_sha256':data['point_sha256'],'symbolic_lift_sha256':sh,
          'pair_rows_sha256':data['pair_rows_sha256'],'linprog_calls':1,
          'integer_multiplier_sum':denominator,
          'row_multipliers':[{'row_index':i,'name':data['rows'][i]['name'],'multiplier':str(v)} for i,v in integer.items()],
          'new_nonnegativity_multipliers':[{'column':j,'descriptor':data['new_columns'][j-OLD],'multiplier':str(v)} for j,v in mu.items()],
          'all_new_columns_cancel_after_nonnegativity':True,'all_420_overlap_coefficients_zero':True,
          'all_old_auxiliary_coefficients_zero':True,'sparse_original4849_row':sparse(oldrow),
          'sparse_original4849_row_K_normalized':sparse(simplified),
          'exact_point_value':str(val),'exact_point_value_float':float(val),
          'exact_phase_I_lower_bound':str(-val/denominator),
          'exact_phase_I_lower_bound_float':float(-val/denominator),
          'K_normalized_point_value':str(val/3),'K_normalized_point_value_float':float(val/3),
          'universal_literal_cases':checks,'universal_hist_reconstruction_equals_Farkas':True,
          'hist_table':hist_table}
    (HERE/'max_b_exact_certificate.json').write_text(json.dumps(cert,ensure_ascii=False,indent=2)+'\n')
    summary={k:cert[k] for k in ('status','linprog_calls','exact_point_value','exact_point_value_float','K_normalized_point_value_float','exact_phase_I_lower_bound_float','universal_literal_cases')}
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
