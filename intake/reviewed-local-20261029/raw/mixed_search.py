import random,time,sys,json
from fractions import Fraction
from itertools import combinations
from tests.audits.customer_attraction_search import exact_outcomes,instance_record
rng=random.Random(20261027); k=7;m=6
masks=[1<<j for j in range(k)] + [ (1<<i)|(1<<j) for i,j in combinations(range(k),2)]
n=(1<<k)-1; best=(Fraction(1),None,None); start=time.time();checked=0
for restart in range(1000):
  w=[0]*n; mode=restart%6
  for mask in masks:
    if mode==0: val=rng.randrange(0,6)
    elif mode==1: val=rng.choice([0,0,1,2,3,5,8])
    elif mode==2: val=rng.randrange(0,15) if mask.bit_count()==1 else rng.randrange(0,4)
    elif mode==3: val=rng.randrange(0,4) if mask.bit_count()==1 else rng.randrange(0,12)
    elif mode==4: val=rng.randrange(0,31) if rng.random()<.4 else 0
    else: val=1 if rng.random()<.5 else 0
    w[mask-1]=val
  if not any(w):continue
  for it in range(8):
    d=exact_outcomes(k,m,tuple(w));checked+=1
    rat=Fraction(d['worst'],d['optimum']) if d['optimum'] else Fraction(1)
    if rat<best[0]:
      best=(rat,tuple(w),d);print('BEST',rat,d['worst'],d['optimum'],'out',len(d['outcome_ids']),flush=True)
    if 2*d['worst']<d['optimum']:
      print('VIOLATION',json.dumps(instance_record(k,m,tuple(w),d),indent=2));sys.exit()
    nw=list(w)
    for _ in range(1 if rng.random()<.8 else 2):
      mask=rng.choice(masks); idx=mask-1; nw[idx]=max(0,nw[idx]+rng.choice([-3,-2,-1,1,2,3]))
    nd=exact_outcomes(k,m,tuple(nw)); nr=Fraction(nd['worst'],nd['optimum']) if nd['optimum'] else Fraction(1)
    if nr<=rat or rng.random()<.03:w=nw
  if time.time()-start>25: break
print('DONE',checked,'elapsed',time.time()-start,'best',best[0],best[2]['worst'],best[2]['optimum'],'out',len(best[2]['outcome_ids']))
print(json.dumps(instance_record(k,m,best[1],best[2]),indent=2))
