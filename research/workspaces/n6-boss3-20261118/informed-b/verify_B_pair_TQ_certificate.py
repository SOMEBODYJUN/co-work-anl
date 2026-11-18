"""Pure-standard-library exact verification of the reciprocal-pair TQ bound.

No solver, floating point, or imported discovery module. Verifies a direct
pointwise inequality for every shared client type, then its scalar K budget.
The proof of validity of the genuine IC/TQ rows is in TQ-cut-validation.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def verify():
    pattern=[(0,1),(1,0),(2,3),(3,2)]
    records=[]
    for block in range(7):
        for bits in product((0,1),repeat=5):
            if block==6 and not any(bits):continue
            e=bits[0];extra=bits[1:];p=e+int(4<=block<6)
            ws=[];last_rows=F();TQ_rows=F()
            for j,(a,y) in enumerate(pattern):
                tj=int(block==j);aa=extra[a];yy=extra[y]
                total=p+tj+aa+yy
                w=F(tj,total) if tj else F()
                u=F(aa,total) if aa else F()
                v=F(yy,total) if yy else F()
                ws.append(w)
                others=(2,3) if j<2 else (0,1)
                for k in others:
                    query=F(int(block==k),p+tj+aa+1)
                    last_rows+=query-v
                T,Q=(2,3) if j<2 else (0,1)
                ft=F(extra[T],p+tj+1)
                uqt=F(extra[Q],p+tj+extra[T]+1)
                TQ_rows+=ft+uqt-u
            residue=(F(7,40)*e+F(3,40)*sum(extra)+sum(ws,F())/4
                     +last_rows/20+TQ_rows/10-F(7,20)*int(block<4))
            assert residue>=0,(block,bits,residue)
            records.append({'block':block,'bits':bits,'residual':str(residue)})
    scalar=4*F(7,20)-F(7,40)-4*F(3,40)-4*F(1,10)
    assert scalar==F(21,40)>F(1,2)
    return {'scope':'Pointwise rational proof for the fixed four-branch reciprocal-pair mode and simultaneous label/anchor renamings only.',
            'client_types':len(records),'minimum_residual':str(min(F(v['residual']) for v in records)),
            'zero_residual_types':sum(F(v['residual'])==0 for v in records),
            'average_forced_payoff_bound_per_K':str(scalar),'residuals':records}

if __name__=='__main__':
    result=verify()
    out=Path(__file__).with_name('shared-B-pair-TQ-exact-replay.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='residuals'},indent=2))
