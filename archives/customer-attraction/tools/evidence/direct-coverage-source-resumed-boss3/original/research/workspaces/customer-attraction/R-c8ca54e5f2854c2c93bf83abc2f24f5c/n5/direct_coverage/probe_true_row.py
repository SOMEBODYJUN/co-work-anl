import random, itertools, json, sys, time
from functools import lru_cache
from pathlib import Path
BASE=Path(__file__).resolve().parent

def probe(weights,k=7):
 n=5; L=60
 @lru_cache(None)
 def payoff(q):
  u=[0]*k
  for mask,w in weights.items():
   c=sum(q[a] for a in range(k) if mask>>a&1)
   if c:
    for a in range(k):
     if mask>>a&1: u[a]+=w*(L//c)
  return tuple(u)
 def inc(q,a): return q[:a]+(q[a]+1,)+q[a+1:]
 floor={}; minima={}
 @lru_cache(None)
 def R(q):
  if sum(q)==n:return frozenset([q])
  ch=[R(inc(q,a)) for a in range(k)]
  mn=tuple(min(payoff(z)[a] for z in ch[a]) for a in range(k))
  f=max(mn);floor[q]=f;minima[q]=mn
  return frozenset(z for a in range(k) for z in ch[a] if payoff(z)[a]>=f)
 root=(0,)*k; outs=R(root)
 def W(q):return sum(w for mask,w in weights.items() if any(q[a] and mask>>a&1 for a in range(k)))
 opts=[];O=-1
 for op in itertools.combinations(range(k),5):
  mask=sum(1<<a for a in op); val=sum(w for m,w in weights.items() if m&mask)
  if val>O:O=val;opts=[op]
  elif val==O:opts.append(op)
 best=None
 for z in sorted(outs,key=W)[:30]:
  gap=(O-W(z))*L
  if gap<=0:continue
  states={root:()}
  for depth in range(3):
   nxt={}
   for q,h in states.items():
    for a in range(k):
     c=inc(q,a)
     if z in R(c) and payoff(z)[a]>=floor[q]:
      if depth==2:
       for op in opts:
        row=sum(minima[q][t] for t in op)+(payoff(z)[a]-minima[q][a])*(a in op)
        score=row-gap
        if best is None or score<best[0]:best=(score,{"weights":weights,"opt":op,"OPT":O,"W":W(z),"prefix":h,"actual_action":a,"terminal_counts":z,"root_payoffs60":payoff(z),"row60":row,"gap60":gap,"minima60":minima[q]})
      else:nxt[c]=h+(a,)
   states=nxt
 return best

if __name__=='__main__':
 rng=random.Random(510251); best=None; start=time.time()
 for j in range(int(sys.argv[1]) if len(sys.argv)>1 else 200):
  k=7
  weights={mask:rng.randrange(1,18) for mask in range(1,1<<k) if rng.random()<.16}
  b=probe(weights,k)
  if b and (best is None or b[0]<best[0]):
   best=b; print(j,b[0],b[1],flush=True)
   (BASE/'true_row_probe_best.json').write_text(json.dumps({"iteration":j,"score60":b[0],"data":b[1]},indent=2))
  if b and b[0]<0:break
 print('seconds',time.time()-start,flush=True)
