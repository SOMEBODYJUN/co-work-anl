"""Universal two-player fresh certificate with the legal background theme.

If the prefix repeats H, a client is fresh iff H is absent. Old clients have
p=L>=1; after denominator (p+1)(p+2) all expressions are affine in L.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).parent
LABELS='ABTSQRHV'
ROOTS=[('T','Q'),('S','R'),('H','V')]
LAST=[('B','A'),('Q','T'),('R','S'),('V','H')]
NAMES=[f'root_{a}_{b}' for a,b in ROOTS]+[f'floor_{a}' for a in LABELS]
NAMES +=[f'last_{chosen}_{prior}_{other}' for chosen,prior in LAST for other in LABELS if other!=chosen]
def vals(bits,p):
    u=lambda a,b: bits[a]*(p+2-bits[b])
    v=[u('A','B')-u(a,b) for a,b in ROOTS]
    v +=[u('A','B')-bits[a]*(p+1) for a in LABELS]
    v +=[u(chosen,prior)-u(other,prior) for chosen,prior in LAST for other in LABELS if other!=chosen]
    return np.array(v,dtype=int)
def target(bits,p):
    a,b,t,s=(bits[x] for x in 'ABTS')
    if not bits['H']:
        assert p==0
        return 2*(2*(a+b-a*b)-(t+s-t*s))
    return (p+2)*(a+b)-2*a*b

def main():
    rows=[];rhs=[];cases=[]
    for bits_tuple in product((0,1),repeat=len(LABELS)):
        bits=dict(zip(LABELS,bits_tuple))
        if bits['H']==0:
            rows.append(vals(bits,0));rhs.append(target(bits,0));cases.append((bits_tuple,'fresh'))
        else:
            v1,v2=vals(bits,1),vals(bits,2)
            rows.extend((v1,v2-v1));rhs.extend((target(bits,1),target(bits,2)-target(bits,1)));cases.extend(((bits_tuple,'p1'),(bits_tuple,'slope')))
    res=linprog(np.ones(len(NAMES)),A_ub=np.array(rows),b_ub=rhs,bounds=(0,None),method='highs')
    if not res.success:
        data=dict(success=False,message=res.message,variables=len(NAMES),rows=len(rows));print(json.dumps(data));(HERE/'background_menu_certificate_status.json').write_text(json.dumps(data,indent=2)+'\n');return
    lam=[Fraction(float(x)).limit_denominator(1000000) for x in res.x]
    rests=[Fraction(b)-sum(Fraction(int(x))*y for x,y in zip(row,lam)) for row,b in zip(rows,rhs)]
    assert min(rests)>=0
    data=dict(success=True,labels=LABELS,slacks={n:str(v) for n,v in zip(NAMES,lam) if v},cases=len(rows),minimum=str(min(rests)))
    (HERE/'background_menu_certificate.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
if __name__=='__main__':main()
