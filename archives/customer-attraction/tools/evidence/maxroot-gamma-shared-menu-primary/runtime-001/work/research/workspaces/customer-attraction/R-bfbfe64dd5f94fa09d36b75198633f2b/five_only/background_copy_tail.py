"""Full-type four-tail discovery retaining a real deviation to legal root Y.

The old root/background Y is a legal common-catalog theme. New path (Y,F,G,H)
uses the same original strategy after the first tail player copies it. No
follower actions are frozen. All numerical outputs require exact recovery.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb
import sys,json,time,numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from legal_background_tail import coefficients as old,Q

def coefficients(p,eta,e):
    names,rows,target,V=old(p,eta[:7],e)
    a,b,c,d,q,r,s,f,g,h=eta
    labels=dict(zip('abcdqrsfgh',eta))
    paths=[('actual',(a,b,c,d),range(4)),('off',(d,q,r,s),range(1,4)),('copyY',(p,f,g,h),range(1,4))]
    for pn,path,indices in paths:
        for i in indices:
            u=Q(path[i],p+sum(path));den=p+sum(path[:i])+4-i
            lab=labels.items() if pn=='copyY' else [(x,labels[x]) for x in 'fgh']
            for name,x in lab:
                names.append(f'{pn}:{i}:K:{name}');rows.append(u-Q(x,den))
            if pn=='copyY':
                names.append(f'{pn}:{i}:background');rows.append(u-Q(p,den))
                names.append(f'{pn}:{i}:sum-opt');rows.append(4*u-Q(e,den))
        pref=p+sum(path[:2]);HH=Q(path[2]+path[3],p+sum(path))+Q(path[2],(pref+1)*(pref+2))
        if pn=='copyY':
            names.append(pn+':pair-opt');rows.append(6*HH-Q(e*(4-e),pref+1)-Q(e*(e-1),pref+2))
            names.append(pn+':pair-opt-background');rows.append(4*HH-Q(e*(1-p)+(4-e)*p,pref+1)-Q(2*e*p,pref+2))
            names.append(pn+':pair-background-background');rows.append(HH-Q(2*p,pref+2))
            for label,x in labels.items():
                names.append(pn+':pair-background-'+label);rows.append(HH-Q(p+x-2*p*x,pref+1)-Q(2*p*x,pref+2))
        # Genuine 3-player suffix, background p+path[0]. Compare all triples
        # of the four opt labels, and triples involving legal Y.
        bg=p+path[0];VV=Q(sum(path[1:]),p+sum(path))
        g3=Q(e*(e-1),bg+e-1)+Q((4-e)*e,bg+e)
        names.append(pn+':three-profit-opt');rows.append(20*VV-3*g3)
        gY=sum((comb(e,t)*comb(4-e,2-t)*Q(p+t,bg+p+t) for t in range(3) if t<=e and 2-t<=4-e),F(0))
        names.append(pn+':three-profit-YTT');rows.append(10*VV-gY)
        gYY=e*Q(2*p+1,bg+2*p+1)+(4-e)*Q(2*p,bg+2*p)
        names.append(pn+':three-profit-YYT');rows.append(20*VV-3*gYY)
        names.append(pn+':three-profit-YYY');rows.append(5*VV-3*Q(3*p,bg+3*p))
    names.append('first-tail-copy-legal-Y');rows.append(Q(a,p+a+b+c+d)-Q(p,2*p+f+g+h))
    return names,rows,target,V

def run(beta0=F(2)):
    t=time.time();A=[];rhs=[];states=[]
    for p,eta,e in product(range(2),product(range(2),repeat=10),range(5)):
        names,rows,target,V=coefficients(p,eta,e)
        A.append([float(v) for v in rows]+[-float(V) if p else 0.]);rhs.append(float((beta0*V if not p else 0)-target));states.append((p,eta,e))
    A=np.asarray(A);rhs=np.asarray(rhs)
    print(json.dumps({'columns':len(states),'rows':len(names),'setup_seconds':time.time()-t}),flush=True)
    out=linprog([0.]*len(names)+[1.],A_ub=A,b_ub=rhs,bounds=(0,None),method='highs')
    report={'scope':'floating all-type coefficient discovery only','beta0':str(beta0),'success':out.success,'message':out.message,'seconds':time.time()-t}
    if out.success:
        report.update(beta1=out.fun,min_residual=float(np.min(rhs-A@out.x)),multipliers={n:float(v) for n,v in zip(names,out.x[:-1]) if v>1e-9})
    target=HERE/'background_copy_tail_discovery.json';target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':run(F(sys.argv[1]) if len(sys.argv)>1 else F(2))
