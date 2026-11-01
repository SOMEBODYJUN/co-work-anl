from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def rows(tau, pbg=0):
    out=[]; rhs=[]; states=[]
    for a,b,c,q,r in product(range(2), repeat=5):
        den=pbg+a+b+c
        al,be,ga=(F(v,den) if v else F() for v in (a,b,c))
        def u(v,*o): return F(v, pbg+sum(o)+v) if v else F()
        D=(pbg+1+a)*(pbg+2+a)
        for d,l in [(0,0),(1,0),(1,tau),(tau,0),(tau,tau)]:
            row=[3*al-F(3*q,pbg+3), 3*al-F(3*r,pbg+3),
                 tau*ga-F(d,pbg+1+a+b), tau*ga-F(l,pbg+1+a+b),
                 tau*be-F(d,pbg+1+a)+F(d*l,tau*D),
                 al-u(c,q,r), tau*u(r,c,q)-F(d,pbg+1+c+q)]
            target=(tau+1)*al+be+ga-min(F(1),F(d))/(pbg+1)
            out.append(row); rhs.append(target); states.append((a,b,c,q,r,d,l))
    return out,rhs,states

lams={
  'discounted': list(map(F,['7/36','1/3','5/9','5/72','5/18','1/3','1/6'])),
  'W': list(map(F,['134/2421','536/2421','14231/21789','2573/43578','5146/21789','2144/2421','268/2421']))
}
report={}
for name, lam in lams.items():
    sl=[]; negative=[]; count=0
    for p in range(101):
        A,b,states=rows(F(2),p)
        for row,tar,state in zip(A,b,states):
            a,bt,c,q,r,d,l=state
            if name=='W':
                tar=F(2*a,p+a+bt+c) if a else F()
                tar += int(p+a+bt+c>0)-min(F(1),d)
            slack=tar-sum(x*y for x,y in zip(row,lam))
            sl.append(slack); count += 1
            if slack < 0: negative.append({'pbg':p,'state':state,'slack':str(slack)})
    report[name]={'constraints':count,'min_slack':str(min(sl)),'max_slack':str(max(sl)),
                  'negative_count':len(negative),'first_negative':negative[:3],
                  'lambda':[str(x) for x in lam]}
print(json.dumps(report,indent=2,ensure_ascii=False))
Path(__file__).with_name('exact_mass_dual_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
