"""Standard-library exact audit of the tau<=21/5 six-player half certificate.

Does not import a game solver, LP solver, or a discovery program. Every client
appears only through six actual membership bits and its comparison-set bit.
The mathematical validity of the nine global rows is proved in the MD file.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

TAU=F(21,5)
FLOOR=list(map(F,['2784735/10526656','240968825/852659136','65773795/213164784',
                  '820179895/4547515392','14864915/252639744','9728723/24060928']))
H4=F(99135297,120304640)
H5=F(9429757,30076160)
PAIR=F(8821071,12030464)


def share(bit,load):
    return F(bit,load) if bit else F(0)


def main():
    residuals=[];zero=[];by_count={c:[] for c in range(7)}
    for e in product((0,1),repeat=6):
        c=sum(e);u=[share(bit,c) for bit in e]
        b=[sum(e[:i]) for i in range(6)];p=b[4];D=(p+1)*(p+2)
        for o in (0,1):
            floors=[TAU*u[i]-F(o,b[i]+6-i) for i in range(6)]
            h4=u[3]-F(e[5],b[3]+3)
            h5=u[4]-F(e[5],b[4]+2)
            pair=u[4]+u[5]+F(e[4],D)-o*(F(2,TAU*(p+1))-F(1,TAU*TAU*D))
            q=2*int(c>0)-o-sum(x*y for x,y in zip(FLOOR,floors))-H4*h4-H5*h5-PAIR*pair
            assert q>=0,(e,o,q)
            residuals.append(q);by_count[c].append(q)
            if not q:zero.append({'actual_bits':e,'comparison_bit':o})
    report={'scope':'universal local-bit certificate for six players and fractional cover tau<=21/5',
            'tau':str(TAU),'state_count':len(residuals),'minimum_residual':str(min(residuals)),
            'minimum_positive_residual':str(min(q for q in residuals if q)),
            'minimum_by_actual_count':{str(c):str(min(q)) for c,q in by_count.items()},
            'floor_multipliers':list(map(str,FLOOR)),'actual_fourth_to_B':str(H4),
            'actual_fifth_to_B':str(H5),'averaged_strong_PAIR':str(PAIR),
            'zero_states':zero}
    out=Path(__file__).with_name('fractional_cover_pair_half_audit.json')
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='zero_states'},indent=2))


if __name__=='__main__':main()
