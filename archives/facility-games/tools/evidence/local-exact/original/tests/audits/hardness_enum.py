from itertools import product,combinations_with_replacement
from fractions import Fraction as F

def extreme(ws,d=0):
    out=[]
    for ss in product((-1,0,1),repeat=len(ws)):
        k=ss.count(0); D=d+sum(w*s for w,s in zip(ws,ss))
        lo=max([-w for w,s in zip(ws,ss) if s<=0],default=-10**6)
        hi=min([w for w,s in zip(ws,ss) if s>=0],default=10**6)
        if k==1:
            if D: continue
            x=F(lo)
        else:x=F(D,1-k)
        if lo<=x<=hi:out.append((x,ss))
    v=min(v for v,ss in out)
    return v,[ss for x,ss in out if x==v]
if __name__=='__main__':
    for n in range(3,7):
        for ws in combinations_with_replacement(range(1,8),n):
            for d in range(-3,4):
                v,ss=extreme(ws,d)
                if all(s.count(0)>=2 and -1 in s for s in ss):
                    print('Essential B with mixers',ws,d,v,ss);raise SystemExit
