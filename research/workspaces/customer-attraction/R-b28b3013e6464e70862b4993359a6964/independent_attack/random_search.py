import random,time
from customer_attraction import Instance, ExactSPESolver
from fractions import Fraction
random.seed(20261024)
best=(Fraction(0),None)
start=time.time(); checked=0
for it in range(4000):
    p=random.randint(2,5)
    m=random.randint(2,7)
    n=random.randint(p, min(18, p*4+4))
    cover=[set() for _ in range(p)]
    for x in range(n):
        mask=random.randrange(1,1<<p)
        for j in range(p):
            if mask>>j&1: cover[j].add(x)
    inst=Instance.from_topic_sets(cover,m)
    try:
        s=ExactSPESolver(inst)
        opt=inst.optimal_welfare(); mw=s.minimum_welfare(); rat=Fraction(opt,mw) if mw else Fraction(999)
    except Exception: continue
    checked+=1
    if rat>best[0]:
      best=(rat,(it,p,m,n,opt,mw,inst.to_dict(),sorted(s.worst_outcomes())))
      print('BEST',best[0],best[1][:6],best[1][6],best[1][7],flush=True)
      if rat>2: break
    if time.time()-start>110: break
print('done',checked,'best',best[0],best[1][:6] if best[1] else None,'sec',time.time()-start)
