#!/usr/bin/env python3
"""Check the new balanced price coordinates and the fixed-price embedding."""
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import random

import balanced_price_projection as new
import derived_price_projection as old

HERE=Path(__file__).resolve().parent


def independent_values(qs,beta,theta):
    p=sum(map(int,qs[:4]));ell=sum(map(int,qs[:5]))
    a=sum(beta[2:],F(0));q=sum((w*x for w,x in zip(beta[2:-1],qs)),F(0));m=beta[-1]
    b=beta[0]/(ell+1)+beta[1]
    edges={}
    for t,c in itertools.product((0,1),repeat=2):
        numerator=a*(t-c)
        edges[t,c]=(numerator/(p+t+c) if numerator else F(0))+b*c+(q+m*t)/(p+t+1)
    candidates=[]
    for f0,f1 in itertools.product((0,1),repeat=2):
        aa=1-theta*(f0==0);bb=-theta*(f0==1)
        cc=-theta*(f1==0);dd=1-theta*(f1==1)
        determinant=aa*dd-bb*cc
        e0,e1=edges[0,f0],edges[1,f1]
        candidates.append(((1-theta)*(e0*dd-bb*e1)/determinant,
                           (1-theta)*(aa*e1-e0*cc)/determinant))
    return tuple(min(row[i] for row in candidates) for i in (0,1))


def main():
    rng=random.Random(20261111);checks=0
    for actual in itertools.product((0,1),repeat=6):
        for trial in range(5):
            qs=tuple(map(F,actual))+tuple(F(rng.randrange(5),4) for _ in range(11))
            beta=tuple(F(rng.randrange(9),7) for _ in range(20))
            for theta in map(F,('0','1/2','3/4','9/10')):
                (s,w),=new.price_values(qs,theta,[beta])
                assert (s,s+w)==independent_values(qs,beta,theta)
                assert w>0
                checks+=1
    report=json.loads((HERE/'new5752_derived_price_sources1to3.json').read_text())
    r=next(r for r in report['results'] if r['source']==3 and r['member']==1 and r['orbit']==[0,0])
    data,cols,hs,K,u=old.data_api.read_input(report['input'])
    assert hashlib.sha256(Path(report['input']).read_bytes()).hexdigest()==report['input_sha256']
    alpha=[F(r['alpha'].get(n,'0')) for n in old.old.NAMES]
    gamma=[F(r['gamma'].get(n,'0')) for n in old.LABELS]
    orb=tuple(r['orbit']);prices=[]
    for g in gamma:
        beta={n:F(0) for n in new.PRICE_NAMES}
        beta.update(alpha_last=3*g/8,beta_last=g/64,mu_A6=g/4,mu_Ci=g/8,
                    mu_Cj=(0 if orb[1] else g/8),mu_other_C=(5 if orb[1] else 4)*g/8)
        prices.append([beta[n] for n in new.PRICE_NAMES])
    row_old,count_old=old.exact_row(cols,hs,2,1,orb,alpha,gamma)
    row_new,count_new=new.exact_row(cols,hs,2,1,orb,F(3,4),alpha,prices)
    assert row_old==row_new
    assert old.budgets(4,alpha,gamma)==new.budgets(4,alpha,prices)
    dot=sum((v*F(c['weight']) for v,c in zip(row_new,cols)),F(0))
    assert dot==F(r['exact_slack'])
    out={'scope':'coordinate and fixed-price embedding audit; not a new SPE theorem',
         'policy_formula_cases':checks,'input':report['input'],'input_sha256':report['input_sha256'],
         'embedded_case':{'source':3,'member':1,'orbit':[0,0],'theta':'3/4'},
         'full_columns_equal':len(cols),'projected_contexts':[count_old,count_new],
         'budget_equal':list(map(str,new.budgets(4,alpha,prices))),
         'exact_slack':str(dot),'exact_slack_float':float(dot)}
    (HERE/'balanced_price_embedding_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out)


if __name__=='__main__':main()
