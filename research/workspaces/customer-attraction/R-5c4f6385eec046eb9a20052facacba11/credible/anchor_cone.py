from anchor_synthesis import *
import numpy as np
from scipy.optimize import linprog
from functools import lru_cache

def policy(ins,s):
 acts={():0};q0=(0,)*6
 for a in range(6):
  qa=ins.counts((a,))
  if a==0:
   acts[(a,)]=4
   for b in range(6):
    if b==4:acts[(a,b)]=5
    else:
     vals=[ins.topic_payoff(t,ins.counts((a,b,t),terminal=True)) for t in range(6)]
     mx=max(vals);br=[t for t in range(6) if vals[t]==mx]
     acts[(a,b)]=min(br,key=lambda t:ins.topic_payoff(b,ins.counts((a,b,t),terminal=True)))
  else:
   desired=min(s.outcomes(qa),key=lambda z:ins.topic_payoff(a,z));floor=s.threshold(qa)
   good=[b for b in range(6) if desired in s.outcomes(ins.counts((a,b))) and ins.topic_payoff(b,desired)>=floor]
   chosen=good[0];acts[(a,)]=chosen
   for b in range(6):
    if b==chosen:
     acts[(a,b)]=next(t for t in range(6) if ins.counts((a,b,t),terminal=True)==desired)
    else:
     ends=s.outcomes(ins.counts((a,b)));z=min(ends,key=lambda z:ins.topic_payoff(b,z));acts[(a,b)]=next(t for t in range(6) if ins.counts((a,b,t),terminal=True)==z)
 return acts

def optimize(acts):
 supports=[15,2]+MASKS
 def terminal(h):
  while len(h)<3:h=h+(acts[h],)
  return h
 def coeff(h,who):
  counts=[h.count(a) for a in range(6)];a=h[who]
  return np.array([float(Fraction(1,sum(counts[b] for b in range(6) if mask>>b&1))) if mask>>a&1 else 0 for mask in supports])
 rows=[]
 for h,a in acts.items():
  base=coeff(terminal(h),len(h))
  for b in range(6):rows.append(coeff(terminal(h+(b,)),len(h))-base)
 result=linprog([0,-1]+[0]*15,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),bounds=[(1,1),(0,3)]+[(0,20)]*15,method='highs')
 return result
if __name__=='__main__':
 rng=random.Random(99446);best=0
 data=json.loads((ROOT/'anchor_best.json').read_text());weights=data['weights']
 for it in range(500):
  if it%10==0:
   weights=[0]*15
   for j in range(12):weights[rng.randrange(15)]+=1
  ins=make(weights,x=3,a=2);s=ExactSPESolver(ins);acts=policy(ins,s);r=optimize(acts)
  if r.success and r.x[1]>best+1e-8:
   best=r.x[1];print(it,'max_a',best,'solution',r.x.tolist(),flush=True)
   (ROOT/'anchor_cone_best.json').write_text(json.dumps({'a':best,'solution':r.x.tolist(),'actions':[[list(h),a] for h,a in acts.items()]},indent=2))
  if r.success:
   scale=60;weights=[int(round(z*scale)) for z in r.x[2:]]
  else:
   j=rng.randrange(15);weights[j]+=rng.choice([1,2])
 print('done',best,flush=True)
