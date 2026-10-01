from random import Random
from fractions import Fraction as Q
from itertools import product
import time
from facility_spe.exact.bounded_overlap import local

def geq_q(z): return z>=0 and z*z+z>=1

def gt_q(z): return z>=0 and z*z+z>1

def audit(r,v):
 C=sum(v);x=max(v,default=Q(0));a=1-C;b=r-C
 rec=local(v+[a,b],[set(range(len(v)))|{len(v)},set(range(len(v)))|{len(v)+1}],0,1)
 got=any(geq_q(p['hi']/r) and geq_q(rec['total']-p['lo']) for p in rec['pieces'])
 pred=C-x>=1-r or geq_q((1-x)/r)
 assert got==pred,(r,v,pred,got,rec)
 pure=any(geq_q(p['hi']/r) and geq_q(rec['total']-p['lo']) for p in rec['pieces'] if 0 not in p['states'])
 two=any(geq_q(p['hi']/r) and geq_q(rec['total']-p['lo']) for p in rec['pieces'] if p['states'].count(0)<=2)
 return got,pure,two

def main():
    rng=Random(749361);count=0;purefail=None;twofail=None;start=time.time()
    for i in range(2500):
     n=rng.randrange(1,7);r=Q(rng.randrange(810,1001),1000)
     C=Q(rng.randrange(1,int(float(r)*618)),1000)
     cuts=sorted(rng.sample(range(1,1000),n-1));vv=[Q(y-x,1000)*C for x,y in zip([0]+cuts,cuts+[1000])]
     got,pure,two=audit(r,vv);count+=1
     if got and not pure and purefail is None:purefail=(r,vv);print('PUREFAIL',purefail,flush=True)
     if got and not two and twofail is None:twofail=(r,vv);print('TWOFAIL',twofail,flush=True)
    print('DONE',count,'iff checks',time.time()-start,'purefail',purefail,'twofail',twofail)

if __name__ == "__main__":
    main()
