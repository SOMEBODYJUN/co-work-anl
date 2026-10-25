"""Exact five-provider maximum-root envelopes, with reviewed true-H projection.

All branch rows concern genuine optimized followers of one forced maximum root.
No off-path payoff is charged to actual welfare. A finite coefficient certificate
is valid for arbitrary finite unit-customer games and ordered-history pure SPE.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ATOMS=list(product(list(product((0,1),repeat=5)),range(6)))
FT=((F(0),F(960),F(1220),F(1480),F(1740),F(2000)),
    (F(0),F(1665,4),F(2745,4),F(3785,4),F(4825,4),F(5865,4)),
    (F(0),F(320),F(524),F(728),F(932),F(1136)))
def q(a,b): return F(a,b) if a else F(0)

def rows(b,d,extra=True):
    v=[q(z,sum(b)) for z in b];c=b[0];out={}
    for j in range(1,5):out[f'size:{j}']=F(c-b[j])
    out['size:opt']=F(5*c-d)
    for i in range(1,5):
        p=sum(b[:i]);k=5-i
        for j in range(5):out[f'IC:{i}:{j}']=v[i]-q(b[j],p+k)
        out[f'opt:{i}']=5*v[i]-q(d,p+k)
    p=sum(b[:3]);H=v[3]+v[4]+q(b[3],(p+1)*(p+2))
    out['r2:O']=F(5,2)*H+q(p,p+1)-int(d>0)
    out['r2:opt']=10*H-q(d*(5-d),p+1)-q(d*(d-1),p+2)
    for j,k in combinations_with_replacement(range(5),2):
        x,y=b[j],b[k]
        out[f'r2:pair:{j}:{k}']=H-q(x+y-2*x*y,p+1)-q(2*x*y,p+2)
    if extra:
        p=c+b[1]
        for j in range(5):
            out[f'trueH:repeat:{j}']=17040*v[2]+1085*c-q(13395*b[j],p+3)-FT[p][d]
        out['trueH:opt']=17040*v[2]+1085*c-q(2679*d,p+3)-FT[p][d]
    return out

def exact_solve(A,y,guess):
    m=[list(a)+[b] for a,b in zip(A,y)];n=len(guess);piv=[];r=0
    for j in range(n):
        hit=next((i for i in range(r,len(m)) if m[i][j]),None)
        if hit is None:continue
        m[r],m[hit]=m[hit],m[r];z=m[r][j];m[r]=[a/z for a in m[r]]
        for i in range(len(m)):
            if i!=r and m[i][j]:
                z=m[i][j];m[i]=[a-z*b for a,b in zip(m[i],m[r])]
        piv.append(j);r+=1
    if any(not any(a[:n]) and a[n] for a in m):raise ValueError('inconsistent equations')
    out=[F(float(a)).limit_denominator(10**9) for a in guess]
    free=[j for j in range(n) if j not in piv]
    for i,j in enumerate(piv):out[j]=m[i][n]-sum(m[i][k]*out[k] for k in free)
    return out

def certify_trueH():
    weights=(17040,9000,10080,600,1085,360,2679)
    residuals=[]
    for p in range(3):
        for d in range(6):
            vals=[]
            for h,z,r in product((0,1),repeat=3):
                s=p+h+z+r;vh,vz,vr=(q(a,s) for a in (h,z,r))
                H=vz+vr+q(z,(p+h+1)*(p+h+2))
                rs=(-vh,q(h-z,p+3),q(h-r,p+3),5*vr-q(d,p+h+z+1),
                    -F(h),5*H-q(5*r+d-2*r*d,p+h+1)-q(2*r*d,p+h+2),q(5*h,p+3))
                val=sum((w*a for w,a in zip(weights,rs)),F())
                vals.append(val);residuals.append(-FT[p][d]-val)
            assert max(vals)==-FT[p][d]
    assert len(residuals)==144 and min(residuals)>=0
    return {'states':len(residuals),'minimum_residual':str(min(residuals))}

def recover(rho,extra=True):
    cols=[rows(*a,extra=extra) for a in ATOMS];names=list(cols[0])
    K=[F(b[0]) for b,d in ATOMS];V=[q(b[0],sum(b)) for b,d in ATOMS];O=[F(d>0) for b,d in ATOMS]
    R0=[rho*k-v for k,v in zip(K,V)];names=['root-IC']+names
    R=[R0]+[[c[n] for c in cols] for n in names[1:]]
    mat=np.array(R,float)
    lp=linprog(-np.array(O,float),A_ub=-mat,b_ub=np.zeros(len(R)),A_eq=[list(map(float,K))],b_eq=[1],bounds=(0,None),method='highs')
    assert lp.success,lp.message
    lam=-lp.ineqlin.marginals;ids=[i for i,z in enumerate(lam) if z>1e-8]
    rem=-lp.fun*np.array(K,float)-np.array(O,float)-lam@mat
    tight=[j for j,z in enumerate(rem) if abs(z)<1e-7]
    A=[[K[j]]+[-R[i][j] for i in ids] for j in tight]
    ans=exact_solve(A,[O[j] for j in tight],[-lp.fun]+[lam[i] for i in ids])
    beta,*ls=ans;assert min(ls)>=0
    rr=[beta*K[j]-O[j]-sum(z*R[i][j] for z,i in zip(ls,ids)) for j in range(len(ATOMS))]
    assert min(rr)>=0
    B=next((z for z,i in zip(ls,ids) if i==0),F());C=B*rho-beta
    # The rho-free identity is checked afresh, rather than assumed from recovery.
    ww={names[i]:z for z,i in zip(ls,ids) if i}
    rr2=[B*V[j]-C*K[j]-O[j]-sum(z*cols[j][n] for n,z in ww.items()) for j in range(len(ATOMS))]
    assert rr2==rr
    return {'rho':str(rho),'value':str(beta),'B':str(B),'C':str(C),
            'multipliers':{n:str(z) for n,z in ww.items()},'states':len(rr),
            'minimum_residual':str(min(rr)),'zero_residuals':sum(z==0 for z in rr)}

def run():
    hidden=certify_trueH();unique={}
    for i in range(200,281):
        rho=F(i,1000);rec=recover(rho);unique[(rec['B'],rec['C'])]=rec
    old=HERE.parent/'five_only'/'maxroot_envelope.json'
    old_records=json.loads(old.read_text())['records']
    improved=[]
    for key,rec in unique.items():
        B,C=map(F,key);rho=F(rec['rho']);value=B*rho-C
        oldvalue=min(F(o['B'])*rho-F(o['C']) for o in old_records)
        if value<oldvalue:
            rec['strict_improvement_at_rho']=str(rho);rec['old_value_at_rho']=str(oldvalue);improved.append(rec)
    out={'scope':__doc__,'hidden_trueH_audit':hidden,'old_source':str(old),'sampled_exact_lines':list(unique.values()),'strictly_improved_lines':improved,
         'sampling_note':'Only discovery rho=0.200,...,0.280 was sampled. The listed lines are globally valid exact inequalities, not a claim to enumerate the entire parametric frontier.'}
    HERE.joinpath('envelope.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()
