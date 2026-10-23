"""Exact finite checks only; general proof is in stationary_defect_sharp.md."""
from fractions import Fraction as F
from math import isqrt
import json


def delta(r,b,I,K):
    return F((r-1)*I-K,(r-1)*(b+I+K)) if I+K else F(0)


def sharp(r,b):
    vals=[(F(a*t*(r-a-t),(r-1)*(a+t)*(b+r-a)*(b+t)),a,t)
          for a in range(1,r) for t in range(1,r-a)]
    return max(vals,default=(F(0),0,0))


def extreme(r,b):
    types=[(I,K,K-(r-1)*I,delta(r,b,I,K))
           for I in (0,1) for K in range(r)]
    vals=[d for I,K,z,d in types if z==0]
    for _,_,z,d in types:
        for _,_,w,e in types:
            if z<0<w:
                vals.append((w*d-z*e)/(w-z))
    return min(vals)


def reduced(r,b):
    ans=F(0)
    for ell in range(1,r-1):
        q=r-ell
        if b==0:
            ts=[1]
        else:
            # Locate floor(tau) exactly from derivative sign:
            # (r+2b)t^2+2b(b+ell)t-q*b(b+ell) <= 0.
            d=b*(b+ell)
            lo,hi=0,q
            while lo+1<hi:
                mid=(lo+hi)//2
                if (r+2*b)*mid*mid+2*d*mid-q*d<=0:
                    lo=mid
                else:
                    hi=mid
            ts=[max(1,min(q-1,z)) for z in (lo,lo+1)]
        for t in ts:
            a=q-t
            ans=max(ans,F(a*t*ell,(r-1)*q*(b+r-a)*(b+t)))
    return ans


def realization(r,b,a,t):
    # Rows are root states; columns are follower labels I0,I1,O0,O1.
    n=[[0]*4 for _ in range(4)]
    s=r-1-a
    for j in range(2):
        n[j][1-j]=s
        n[j][2+j]=a
        n[2+j][j]=t
        n[2+j][2+1-j]=r-1-t
    pi=[F(t,2*(a+t))]*2+[F(a,2*(a+t))]*2
    assert all(sum(row)==r-1 and row[i]==0 for i,row in enumerate(n))
    assert all(sum(pi[i]*n[i][j] for i in range(4))==(r-1)*pi[j] for j in range(4))
    value=sum(pi[i]*delta(r,b,int(i<2),sum(n[i][:2])) for i in range(4))
    assert value==-F(a*t*(r-a-t),(r-1)*(a+t)*(b+r-a)*(b+t))
    ed=sum(pi[i]*F(int(i<2),b+int(i<2)+sum(n[i][:2])) for i in range(4))
    er=sum(pi[i]*F(int(i<2)+sum(n[i][:2]),b+int(i<2)+sum(n[i][:2])) for i in range(4))
    cap=F(r)+F((r-1)**2//4,b+1)
    assert er<=cap*ed
    if t==1 and a*(r-1-a)==(r-1)**2//4:
        assert er==cap*ed
    return value

checks=0
samples=[]
for r in range(2,61):
    for b in (0,1,2,5,17,1000):
        val,a,t=sharp(r,b)
        assert extreme(r,b)==-val
        assert reduced(r,b)==val
        if b==0:
            D=(r+1)**2//4
            assert val==F(1-F(r,D),r-1)
        if val:
            realization(r,b,a,t)
        if r>=3:
            aa=(r-1)//2
            realization(r,b,aa,1)
        checks+=1
        if r in (3,4,5,10,60) and b in (0,1,1000):
            samples.append({'r':r,'b':b,'loss':str(val),'a':a,'t':t})
print(json.dumps({'status':'passed','grid_cases':checks,'samples':samples},ensure_ascii=False,indent=2))
