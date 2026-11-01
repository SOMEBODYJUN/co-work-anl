"""True tail-three branch B,Q,R, projected customerwise certificate search.

Each G menu uses six arbitrary comparison themes and true last replies.
Independent reply membership counts are relaxed to [0,6] and projected by
affinity. This is a sufficient-certificate search, not a game search.
"""
from itertools import product
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog

def qf(n,d): return F(n,d) if n else F(0)
def gen(n=6):
    for bits in product(range(2),repeat=n+2):
        act=bits[:n]; q,r=bits[n:]; c,a,b=act[-3:]; k=sum(act[:-3]); p=k+c
        z=sum(act); bz=k+b+q+r
        actual=[qf(t,z) for t in act]
        vq=qf(q,bz);vr=qf(r,bz)
        for d,l1,l2 in product((0,1,n),(0,n),(0,n)):
            names=[]; vals=[]
            def add(name,val): names.append(name); vals.append(val)
            def menu(prefix,x,y,ell,label):
                den=prefix+x+y
                add(label,n*qf(x,den)+qf(y,2*den)-F(d,prefix+1)-F(ell,2*n*(prefix+x+1))+F(d*ell,n*(prefix+1)*(prefix+2)))
            menu(p,a,b,l1,'Gactual')
            menu(k+b,q,r,l2,'Gbranch')
            add('source-IC',actual[-3]-qf(b,bz))
            for i in range(n):
                denom=n-i+sum(act[:i])
                for j,t in enumerate(bits):
                    add(f'floor:{i+1}:{j+1}',actual[i]-F(t,denom))
                add(f'optfloor:{i+1}',n*actual[i]-F(d,denom))
            for lab,pay,denom in [('Q',vq,k+b+2),('R',vr,k+b+q+1)]:
                for j,t in enumerate(bits): add(f'{lab}floor:{j+1}',pay-F(t,denom))
                add(f'{lab}optfloor',n*pay-F(d,denom))
            yield (bits,d,l1,l2),int(z>0),int(d>0),vals,names

def solve(n=6,output=None):
    ss=list(gen(n)); names=ss[0][-1]
    mat=np.array([[float(v) for v in z[3]]+[-z[1]] for z in ss]);rhs=np.array([-z[2] for z in ss])
    obj=np.zeros(len(names)+1);obj[-1]=1
    lp=linprog(obj,A_ub=mat,b_ub=rhs,bounds=(0,None),method='highs')
    out={'n':n,'states':len(ss),'status':lp.message}
    if lp.success:
        out.update(beta=lp.x[-1],coefficients={s:float(v) for s,v in zip(names,lp.x) if v>1e-8})
        if output: np.savez(output,matrix=mat,rhs=rhs,solution=lp.x,dual=lp.ineqlin.marginals)
    return out

if __name__=='__main__':
    print(json.dumps([solve(n) for n in range(3,7)],indent=2))
