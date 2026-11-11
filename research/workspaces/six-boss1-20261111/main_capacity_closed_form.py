"""Main's independent 128-case proof and point audit of the u2+13K/64 cut."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json
import sys


def phi(p,t,q):
    if p == 0:
        return F(25,64)*t + F(1,16)*q - F(1,20)*t*q
    assert p == 1
    return F(109,320)*t + F(1,32)*q - F(1,48)*t*q


def prove_table():
    table=[]
    for p,t,q in product((0,1),repeat=3):
        costs=[]
        for h in product((0,1),repeat=4):
            s,g=sum(h[:3]),h[3]
            den=p+t+s+g
            cost=(F(t,den)-F(g,16*den) if den else F())
            cost += F(3*s+4*g,64)+F(q,16*(p+t+s+1))
            costs.append(cost)
        assert min(costs)==phi(p,t,q)
        assert all(cost>=phi(p,t,q) for cost in costs)
        table.append({'p':p,'t':t,'q':q,'minimum':str(phi(p,t,q)),
                      'minimizers':sum(cost==phi(p,t,q) for cost in costs)})
    return table


def main():
    out={'domain':'all p,t,q bits and all four actual follower membership bits',
         'literal_cases':128,'table':prove_table(),'left_budget':'u_2+13K/64'}
    point=Path(sys.argv[1]); raw=point.read_bytes(); data=json.loads(raw)
    cols=data['columns'];ys=[F(c['weight']) for c in cols]
    lhs=F(13,64)*ys[0];rhs=F()
    for idx,c in enumerate(cols):
        if c['kind']=='hist':
            a=tuple(map(int,c['actual_bits']))
            if a[1]:lhs+=ys[idx]*F(1,sum(a))
        elif c['kind']=='maximum-root-family-state':
            a=tuple(map(int,cols[c['hist_column']]['actual_bits']))
            rhs+=ys[idx]*phi(a[0],c['hidden'][0],a[5])
    out.update(input=str(point),input_sha256=sha256(raw).hexdigest(),
               target='maximum-root H_0',query='A_6',left=str(lhs),right=str(rhs),
               slack=str(lhs-rhs),slack_float=float(lhs-rhs),negative=lhs<rhs)
    Path(sys.argv[2]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
