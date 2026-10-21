"""Exact coefficient proof audit for a three-remaining truncated price budget.
No equilibrium oracle and no numerical LP are used. Integer background is
unbounded: denominators divide L=(p+1)(p+2)(p+3), so the numerator has degree
at most three. Nonnegative Newton coefficients prove every integer p>=1.
"""
from fractions import Fraction as F
from itertools import product
from math import comb,lcm
from pathlib import Path
import json
CERTS=[(F(3,2),F(43,46),[F(0),F(0),F(20,23),F(0),F(6,23),F(21,23),F(0)]),
       (F(2),F(262,411),list(map(F,['8/411','32/411','91/137','61/822','122/411','532/411','16/411']))) ]

def remainder(bits,d,ell,p,t,kappa,lam):
    a,b,c,q,r=bits;s=a+b+c
    alpha,beta,gamma=[F(v,p+s) if v else F() for v in (a,b,c)]
    def u(v,*other):return F(v,p+v+sum(other)) if v else F()
    D=(p+1+a)*(p+2+a)
    # KQ,KR,P,Z,S+(1/t)V,F,J; these are the directly expanded
    # genuine rows. The weighted joint membership h has canceled.
    rows=[3*alpha-F(3*q,p+3),3*alpha-F(3*r,p+3),
          t*gamma-F(d,p+1+a+b),t*gamma-F(ell,p+1+a+b),
          t*beta-F(d,p+1+a)+F(d*ell,t*D),
          alpha-u(c,q,r),t*u(r,c,q)-F(d,p+1+c+q)]
    G=sum((x*y for x,y in zip(lam,rows)),F())
    target=t*alpha+int(p+s>0)-min(F(1),d)-kappa*alpha
    return target-G

reports=[]
for t,kappa,lam in CERTS:
    table=[];raw=[]
    for bits in product(range(2),repeat=5):
        entries=[]
        for d,ell in [(0,0),(1,0),(1,t),(t,0),(t,t)]:
            # Full parameter corner proof: rho is bilinear on each of
            # [0,1]x[0,t] and [1,t]x[0,t]. d=0 has nonnegative ell
            # coefficient, so its minimum is attained at ell=0.
            p0=remainder(bits,d,ell,0,t,kappa,lam)
            values=[remainder(bits,d,ell,p,t,kappa,lam)*(p+1)*(p+2)*(p+3)
                    for p in range(1,5)]
            coeff=[]
            while values:
                coeff.append(values[0]);values=[v-u for u,v in zip(values,values[1:])]
            assert p0>=0 and min(coeff)>=0,(t,bits,d,ell,p0,coeff)
            # Additional implementation checks only; the all-p proof is
            # the denominator/degree argument plus positive Newton basis.
            for p in [5,17,1000]:
                actual=remainder(bits,d,ell,p,t,kappa,lam)*(p+1)*(p+2)*(p+3)
                assert actual==sum((x*comb(p-1,k) for k,x in enumerate(coeff)),F())
            entries.append([p0]+coeff)
            raw.append({'bits':bits,'d':str(d),'ell':str(ell),'p0':str(p0),'newton':list(map(str,coeff))})
        table.append({'bits':''.join(map(str,bits)),'minima':[min(v[j] for v in entries) for j in range(5)]})
    scale=lcm(*(x.denominator for row in table for x in row['minima']))
    for row in table:row['scaled_minima']=[int(scale*x) for x in row.pop('minima')]
    reports.append({'mass':str(t),'kappa':str(kappa),'lambda':list(map(str,lam)),
                    'corner_cases':160,'minimum_scale':scale,'minimum_table':table,'all_corners':raw})
report={'scope':'unbounded integer background; 32 Boolean types and a bilinear corner proof, not finite SPE sampling',
        'status':'all exact coefficients nonnegative','uniform_truncated_price_coefficient':'113/822','certificates':reports}
out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(report,indent=2)+'\n')
for rec in reports:
    print('mass',rec['mass'],'kappa',rec['kappa'],'scale',rec['minimum_scale'])
    print('abcqr | p=0 rho | N(1) | DeltaN(1) | Delta^2N(1) | Delta^3N(1)')
    for row in rec['minimum_table']:print(row['bits'],*row['scaled_minima'])
print(report['status'])
