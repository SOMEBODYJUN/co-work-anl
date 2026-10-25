"""Independent exact audit of existing maximum-root certificates and new payment.

Reconstructs only the nonzero supported rows from original payoff definitions;
does not import the discovery implementation or any SPE solver.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/five_only/maxroot_envelope.json'
def q(n,d):return F(n,d) if n else F(0)

def supported_rows(bits,d):
    c,a2,a3,a4,a5=bits;load=sum(bits)
    u=[q(x,load) for x in bits];p=c+a2+a3
    h=u[3]+u[4]+F(a4,(p+1)*(p+2))
    r={f'size:{i}':F(c-bits[i]) for i in range(1,5)}
    r.update({'IC:2:4':u[2]-F(a5,c+a2+3),
              'opt:4':5*u[4]-F(d,c+a2+a3+a4+1),
              'r2:O':F(5,2)*h+F(p,p+1)-int(d>0),
              'r2:opt':10*h-F(d*(5-d),p+1)-F(d*(d-1),p+2)})
    return u,r

def run():
    src=json.loads(SOURCE.read_text());seen=set();checks=[]
    for rec in src['records']:
        B,C=F(rec['B']),F(rec['C'])
        if (B,C) in seen or B<=0 or C<=0:continue
        seen.add((B,C));ws={n:F(x) for n,x in rec['multipliers'].items() if n!='root-IC'}
        assert min(ws.values())>=0
        assert F(rec['multipliers']['root-IC'])==B
        assert B*F(rec['rho'])-F(rec['value'])==C
        residual=[]
        for bits in product((0,1),repeat=5):
            for d in range(6):
                us,rs=supported_rows(bits,d)
                z=B*us[0]-C*bits[0]-int(d>0)-sum(w*rs[n] for n,w in ws.items())
                assert z>=0,(B,C,bits,d,z)
                residual.append(z)
        checks.append({'B':str(B),'C':str(C),'states':len(residual),'minimum':str(min(residual)),'zeros':sum(z==0 for z in residual)})
    # Genuine positions 2..5 compare C; |C|-|A1| is the sole size row.
    lam=[F(5,4),F(19,9),F(11,3),F(4)]
    payment=[]
    for bits in product((0,1),repeat=6):
        acts=bits[:5];c=bits[5];load=sum(acts);u=[q(a,load) for a in acts]
        ic=[u[i]-F(c,sum(acts[:i])+5-i) for i in range(1,5)]
        target=4*int(load>0)-5*u[0]-4*c+acts[0]
        residual=target-sum(w*row for w,row in zip(lam,ic))
        assert residual>=0,(bits,residual)
        payment.append({'bits':list(bits),'residual':str(residual)})
    out={'status':'passed','scope':__doc__,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'maximum_root_certificates':checks,
         'actual_payment':{'claim':'4W-5r-4|C|+|A1|>=0 for every legal C','maximum_theme_corollary':'4W-5r-3K>=0','states':64,'multipliers':[str(x) for x in lam],'minimum_residual':str(min(F(t['residual']) for t in payment)),'zero_residuals':sum(F(t['residual'])==0 for t in payment),'residual_table':payment}}
    HERE.joinpath('independent_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='actual_payment'},indent=2));print(json.dumps({k:v for k,v in out['actual_payment'].items() if k!='residual_table'},indent=2))
if __name__=='__main__':run()
