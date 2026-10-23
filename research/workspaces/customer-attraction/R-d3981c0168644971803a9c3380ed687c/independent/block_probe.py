"""Attack universal two-step safety-debt closure; discovery uses floating LP."""
from fractions import Fraction as F
from pathlib import Path
import json, random
from background_probe import security
from customer_attraction import Instance, CustomerType, ExactSPESolver

def add(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
def run():
 rng=random.Random(9328971);tested=0;best=(0,None)
 for k,r,prefnum,iters in [(5,4,0,200),(6,4,0,200),(6,5,0,100),(5,4,1,200),(6,5,1,100)]:
  for it in range(iters):
   cs=[]
   for mask in range(1,1<<k):
    w=rng.randrange(0,9) if rng.random()<.5 else 0
    if w:cs.append(CustomerType(frozenset(j for j in range(k) if mask>>j&1),w))
   inst=Instance(tuple(map(str,range(k))),tuple(cs),r+prefnum)
   pref=[0]*k
   for j in range(prefnum):pref[rng.randrange(k)]+=1
   pref=tuple(pref);sol=ExactSPESolver(inst);th0=sol.threshold(pref)
   v0,*_=security(inst,pref)
   for a in range(k):
    p1=add(pref,a);th1=sol.threshold(p1)
    for b in range(k):
     p2=add(p1,b);v2,*_=security(inst,p2)
     for q in sol.outcomes(p2):
      U=inst.topic_payoffs(q)
      if U[a]<th0 or U[b]<th1:continue
      gap=float(U[a]+U[b])+(r-2)*v2-r*v0
      if gap < best[0]-1e-7:
       best=(gap,(k,r,prefnum,it,a,b));print('best',tested,best,flush=True)
      if gap < -1e-7:
       data={'instance':inst.to_dict(),'prefix_counts':pref,'first_two':[a,b],'terminal':q,'u_first_two':[str(U[a]),str(U[b])],'V0_float':v0,'V2_float':v2,'gap_float':gap}
       Path(__file__).with_name('block_candidate_failure.json').write_text(json.dumps(data,indent=2));print('FOUND',data,flush=True);return
   tested+=1
  print('batch',k,r,prefnum,'tested',tested,'best',best,flush=True)
 print('DONE',tested,best)
if __name__=='__main__':run()
