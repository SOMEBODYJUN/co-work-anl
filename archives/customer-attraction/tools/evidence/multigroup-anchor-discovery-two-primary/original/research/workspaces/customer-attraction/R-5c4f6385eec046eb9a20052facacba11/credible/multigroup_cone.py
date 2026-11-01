from anchor_synthesis import *
import numpy as np
from scipy.optimize import linprog
import argparse

def fixed_policy(ins,s,path):
 acts={};target=ins.counts(path,terminal=True)
 def extend(h,desired,forced):
  if len(h)==ins.players:return
  q=ins.counts(h)
  if forced:a=path[len(h)]
  else:
   floor=s.threshold(q)
   a=next(a for a in range(ins.topic_count) if desired in s.outcomes(ins.counts(h+(a,))) and ins.topic_payoff(a,desired)>=floor)
  acts[h]=a
  for b in range(ins.topic_count):
   child=h+(b,)
   if b==a:d=desired;f=forced
   else:
    d=min(s.outcomes(ins.counts(child)),key=lambda z:ins.topic_payoff(b,z));f=False
   extend(child,d,f)
 extend((),target,True)
 return acts

def optimize(acts,k):
 nt=4*k+2;m=k+2
 supports=[]
 supports.append([frozenset(range(4*i,4*i+4)) for i in range(k)])
 supports.append([frozenset({4*i+1}) for i in range(k)])
 for mask in MASKS:
  topics=set()
  for b in range(2):
   if mask>>(2+b)&1:topics.update(4*i+2+b for i in range(k))
  for d in range(2):
   if mask>>(4+d)&1:topics.add(4*k+d)
  supports.append([frozenset(topics)])
 terminals={}
 def terminal(h):
  orig=h
  if h in terminals:return terminals[h]
  while len(h)<m:h=h+(acts[h],)
  terminals[orig]=h;return h
 coeffs={}
 def coeff(h,who):
  a=h[who];q=tuple(h.count(t) for t in range(nt));key=(q,a)
  if key not in coeffs:
   coeffs[key]=np.array([sum(1/sum(q[b] for b in sup) for sup in group if a in sup) for group in supports])
  return coeffs[key]
 rows=[]
 for h,a in acts.items():
  base=coeff(terminal(h),len(h))
  for b in range(nt):rows.append(coeff(terminal(h+(b,)),len(h))-base)
 result=linprog([0,-1]+[0]*15,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),bounds=[(1,1),(0,3)]+[(0,20)]*15,method='highs')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--k',type=int,default=2);p.add_argument('--tries',type=int,default=60);args=p.parse_args();k=args.k
 weights=[0,0,0,3,0,0,6,2,4,4,0,0,0,0,0];x=6;a=4;best=0;rng=random.Random(92738)
 for it in range(args.tries):
  if it%10==0 and it:
   weights=[0]*15
   for j in range(rng.randrange(8,18)):weights[rng.randrange(15)]+=1
   x=3;a=2
  ins=make(weights,k=k,x=x,a=a);s=ExactSPESolver(ins);path=tuple(4*i for i in range(k))+(4*k,4*k+1);acts=fixed_policy(ins,s,path);r=optimize(acts,k)
  if r.success:
   if r.x[1]>best+1e-8:
    best=r.x[1];print(it,'k',k,'max_a',best,'solution',r.x.tolist(),flush=True)
    (ROOT/f'anchor_{k}group_cone_best.json').write_text(json.dumps({'k':k,'a':best,'solution':r.x.tolist(),'actions':[[list(h),a] for h,a in acts.items()]},indent=2))
   x=120;a=round(r.x[1]*x);weights=[round(z*x) for z in r.x[2:]]
  else:
   print(it,'infeasible',flush=True);weights[rng.randrange(15)]+=1
 print('done',k,best,flush=True)
