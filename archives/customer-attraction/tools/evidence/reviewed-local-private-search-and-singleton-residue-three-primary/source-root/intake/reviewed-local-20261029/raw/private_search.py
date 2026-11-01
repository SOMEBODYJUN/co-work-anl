import random,time,sys,json
from fractions import Fraction
from tests.audits.customer_attraction_search import exact_outcomes,instance_record
rng=random.Random(20261027); k=7;m=6
best=(Fraction(1),None,None); start=time.time();checked=0
for restart in range(2000):
  w=[0]*((1<<k)-1); mode=restart%5
  for j in range(k):
    if mode==0:w[(1<<j)-1]=rng.randrange(1,31)
    elif mode==1:w[(1<<j)-1]=rng.choice([0,1,2,3,5,8,13,21,34])
    elif mode==2:w[(1<<j)-1]=rng.randrange(1,101) if rng.random()<.8 else 0
    elif mode==3:w[(1<<j)-1]=rng.randrange(1,11)
    else:w[(1<<j)-1]=rng.randrange(1,6) if rng.random()<.5 else 0
  if not any(w):continue
  for it in range(10):
    d=exact_outcomes(k,m,tuple(w)); checked+=1
    rat=Fraction(d['worst'],d['optimum']) if d['optimum'] else Fraction(1)
    if rat<best[0]: best=(rat,tuple(w),d); print('BEST',rat,d['worst'],d['optimum'],'out',len(d['outcome_ids']),'sing',[w[(1<<j)-1] for j in range(k)],flush=True)
    if 2*d['worst']<d['optimum']:
      print('VIOLATION',json.dumps(instance_record(k,m,tuple(w),d),indent=2));sys.exit()
    nw=list(w)
    for _ in range(1 if rng.random()<.8 else 2):
      j=rng.randrange(k); idx=(1<<j)-1; nw[idx]=max(0,nw[idx]+rng.choice([-3,-2,-1,1,2,3]))
    nd=exact_outcomes(k,m,tuple(nw)); nr=Fraction(nd['worst'],nd['optimum']) if nd['optimum'] else Fraction(1)
    if nr<=rat or rng.random()<.03:w=nw
  if time.time()-start>100: break
print('DONE',checked,'elapsed',time.time()-start,'best',best[0],best[2]['worst'],best[2]['optimum'],[best[1][(1<<j)-1] for j in range(k)], 'out',len(best[2]['outcome_ids']))
print(json.dumps(instance_record(k,m,best[1],best[2]),indent=2))
