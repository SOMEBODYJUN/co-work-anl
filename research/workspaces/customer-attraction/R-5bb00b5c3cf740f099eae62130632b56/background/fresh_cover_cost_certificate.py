from itertools import product
from fractions import Fraction
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).parent
LABELS='ABTSQR'
LAST=[('B','A'),('Q','T'),('R','S')]
NAMES=['root_T_Q','root_S_R']+[f'floor_{a}' for a in LABELS]+['old_cover']+[f'last_{a}_{b}_{c}' for a,b in LAST for c in LABELS if c!=a]
def rows(tau):
    result=[];rhs=[]
    for v in product((0,1),repeat=6):
        bits=dict(zip(LABELS,v))
        for occupied,p in ((False,0),(True,1),(True,2)):
            u=lambda a,b:bits[a]*(p+2-bits[b])
            a,b,t,s=(bits[x] for x in 'ABTS')
            row=[u('A','B')-u('T','Q'),u('A','B')-u('S','R')]
            row += [u('A','B')-bits[x]*(p+1) for x in LABELS]
            row += [tau*u('A','B')-(p+1 if occupied else 0)]
            row +=[u(a,b)-u(c,b) for a,b in LAST for c in LABELS if c!=a]
            target=(p+2)*(a+b)-2*a*b if occupied else 2*(2*(a+b-a*b)-(t+s-t*s))
            if occupied and p==2:
                oldrow=result[-1];oldrhs=rhs[-1]
                row=[y-x for y,x in zip(row,oldrow)];target-=oldrhs
            result.append(row);rhs.append(target)
    return np.array(result),np.array(rhs)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--tau',type=str,default='2');args=ap.parse_args();tau=Fraction(args.tau);A,b=rows(tau)
    res=linprog(np.ones(len(NAMES)),A_ub=np.array(A,dtype=float),b_ub=np.array(b,dtype=float),bounds=(0,None),method='highs')
    if res.success:
        lam=[Fraction(float(x)).limit_denominator(100000) for x in res.x]
        rests=[bb-sum(Fraction(x)*y for x,y in zip(row,lam)) for row,bb in zip(A,b)]
        assert min(rests)>=0
        data=dict(tau=str(tau),success=True,slacks={k:str(v) for k,v in zip(NAMES,lam) if v},minimum=str(min(rests)))
    else:data=dict(tau=str(tau),success=False,message=res.message)
    print(json.dumps(data,indent=2));(HERE/('fresh_cover_cost_'+str(tau).replace('/','_')+'.json')).write_text(json.dumps(data,indent=2)+'\n')
