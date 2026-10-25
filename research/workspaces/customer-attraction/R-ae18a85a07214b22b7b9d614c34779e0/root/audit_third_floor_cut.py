"""Exact all-membership identity for the third-floor root rigidity cut."""
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ALPHA=F(11033,763)
BETA=F(2085,763)
GAMMA=-F(4139,763)
WEIGHTS={'size:A':F(1,2),'size:B':F(1093,1526),
         'size:C':F(77,109),'size:D':F(618,763),
         'third:D':F(165,763),'last:Q':F(673,763),
         'last:E':F(135,763),'penultimate:D':F(180,763),
         'copy-last:Q':F(90,763)}

def share(x,d): return F(x,d) if x else F()
def residual(bits):
    t,a,b,c,d,q,e=bits
    load=t+a+b+c+d;copy=t+a+b+d+e;prefix=t+a+b
    r=share(t,load);v3=share(b,load);v4=share(c,load);v5=share(d,load)
    rows={'size:A':-F(a),'size:B':-F(b),'size:C':-F(c),'size:D':-F(d),
          'third:D':v3-F(d,t+a+3),
          'last:Q':v5-F(q,prefix+c+1),
          'last:E':v5-F(e,prefix+c+1),
          'penultimate:D':v4-share(d,copy),
          'copy-last:Q':share(e,copy)-F(q,prefix+d+1)}
    return GAMMA*t-F(q,1+4*t)+ALPHA*r-sum(WEIGHTS[k]*v for k,v in rows.items())

def run():
    records=[]
    assert sum(v for n,v in WEIGHTS.items() if n.startswith('size:'))==BETA
    assert ALPHA/5+BETA+GAMMA==F(1,5)
    for bits in product((0,1),repeat=7):
        rho=residual(bits)
        assert rho>=0,(bits,rho)
        records.append({'bits':list(bits),'residual':str(rho)})
    out={'scope':'Exact 128-membership nonnegative identity; not a half proof',
         'alpha':str(ALPHA),'beta':str(BETA),'gamma':str(GAMMA),
         'weights':{k:str(v)for k,v in WEIGHTS.items()},
         'memberships':records,'zero_count':sum(F(r['residual'])==0 for r in records)}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items()if k!='memberships'}))
    print('max-source aggregate: 3815 OPT + 48298 K <= 275825 u')

if __name__=='__main__':run()
