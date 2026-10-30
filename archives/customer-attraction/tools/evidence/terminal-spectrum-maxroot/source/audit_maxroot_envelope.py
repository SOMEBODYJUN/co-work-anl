"""Standard-library coefficient audit independent of discovery implementation.

Same author, separate implementation; not independent mathematical review.
Every one of 192 atom states is checked using only the supported row formulas.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
HERE=Path(__file__).resolve().parent

def audit():
    source=HERE/'maxroot_envelope.json';data=json.loads(source.read_text());seen=set();results=[]
    for rec in data['records']:
        B,C=F(rec['B']),F(rec['C']);key=(B,C)
        if key in seen or not(B>0 and C>0):continue
        seen.add(key);weights={n:F(v) for n,v in rec['multipliers'].items() if n!='root-IC'}
        assert F(rec['multipliers']['root-IC'])==B
        assert B*F(rec['rho'])-F(rec['value'])==C and min(weights.values())>=0
        residuals=[]
        for bits in product((0,1),repeat=5):
            load=sum(bits);u=[F(bit,load) if bit else F(0) for bit in bits]
            c,a2,a3,a4,a5=bits;pref=c+a2+a3
            H=u[3]+u[4]+F(a4,(pref+1)*(pref+2))
            for d in range(6):
                rs={f'size:{i}':F(c-bits[i]) for i in range(1,5)}
                rs['IC:2:4']=u[2]-F(a5,c+a2+3)
                rs['opt:4']=5*u[4]-F(d,pref+a4+1)
                rs['r2:O']=F(5,2)*H+F(pref,pref+1)-int(d>0)
                rs['r2:opt']=10*H-F(d*(5-d),pref+1)-F(d*(d-1),pref+2)
                residual=B*u[0]-C*c-int(d>0)-sum(w*rs[n] for n,w in weights.items())
                assert residual>=0,(key,bits,d,residual)
                residuals.append(residual)
        results.append({'B':str(B),'C':str(C),'states':len(residuals),'minimum_residual':str(min(residuals)),'zero_residuals':sum(x==0 for x in residuals)})
    result={'status':'passed','scope':__doc__,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'certificates':results}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':audit()
