import random,time,sys,json
from fractions import Fraction
from tests.audits.customer_attraction_search import exact_outcomes,instance_record
rng=random.Random(20261027); k=5;m=6;n=(1<<k)-1
best=(Fraction(1),None,None); start=time.time(); checked=0
for restart in range(500):
    mode=restart%6
    if mode==0:w=tuple(rng.randrange(2) for _ in range(n))
    elif mode==1:w=tuple(1 if rng.random()<.25 else 0 for _ in range(n))
    elif mode==2:w=tuple(rng.randrange(1,5) if ((mask.bit_count() in (1,2)) and rng.random()<.5) else 0 for mask in range(1,1<<k))
    elif mode==3:w=tuple(rng.randrange(1,5) if ((mask.bit_count() in (1,4)) and rng.random()<.7) else 0 for mask in range(1,1<<k))
    elif mode==4:w=tuple(rng.randrange(1,8) if rng.random()<.12 else 0 for _ in range(n))
    else:w=tuple(1 if rng.random()<.5 else 0 for _ in range(n))
    if not any(w):continue
    for it in range(80):
      d=exact_outcomes(k,m,w); checked+=1
      rat=Fraction(d['worst'],d['optimum']) if d['optimum'] else Fraction(1)
      if rat<best[0]:best=(rat,w,d);print('BEST',rat,'W/O',d['worst'],d['optimum'],'outcomes',len(d['outcome_ids']),'w',w,flush=True)
      if 2*d['worst']<d['optimum']:
       print('VIOLATION',json.dumps(instance_record(k,m,w,d),indent=2));sys.exit()
      nw=list(w)
      for _ in range(1 if rng.random()<.8 else 2):
       j=rng.randrange(n); nw[j]=0 if nw[j] else 1
      nw=tuple(nw); nd=exact_outcomes(k,m,nw); nrat=Fraction(nd['worst'],nd['optimum']) if nd['optimum'] else Fraction(1)
      if nrat<=rat or rng.random()<.03:w=nw
    if time.time()-start>100:break
print('DONE',checked,'elapsed',time.time()-start,'best',best[0],best[2]['worst'],best[2]['optimum'],best[1], 'outcomes',len(best[2]['outcome_ids']))
print(json.dumps(instance_record(k,m,best[1],best[2]),indent=2))
