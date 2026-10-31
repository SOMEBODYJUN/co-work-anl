from itertools import product
from functools import lru_cache
from math import lcm
import random,json,argparse,time

def comps(n,p):
 if p==1: yield (n,); return
 for v in range(n+1):
  for z in comps(n-v,p-1):yield (v,)+z

def solve(w,m,p,cap=1000000,table=None):
 D=lcm(*range(1,m+1))
 states=[tuple(comps(t,p)) for t in range(m+1)]
 @lru_cache(None)
 def U(q,a):
  if table is not None: return table[q,a]
  return sum(n*(D//sum(q[b] for b in range(p) if mask>>b&1)) for mask,n in enumerate(w,1) if n and mask>>a&1)
 def add(k,a):return k[:a]+(k[a]+1,)+k[a+1:]
 @lru_cache(None)
 def R(k):
  if sum(k)==m:return frozenset([k])
  vals=[R(add(k,a)) for a in range(p)]
  floor=max(min(U(q,a) for q in vals[a]) for a in range(p))
  return frozenset(q for a in range(p) for q in vals[a] if U(q,a)>=floor)
 full=R((0,)*p)
 assignments=[tuple(states[m])]; peak=1
 for t in range(m-1,-1,-1):
  childids={k:i for i,k in enumerate(states[t+1])}
  new=set()
  for row in assignments:
   choices=[]
   for k in states[t]:
    qs=[row[childids[add(k,a)]] for a in range(p)]
    vals=[U(q,a) for a,q in enumerate(qs)]
    vmax=max(vals)
    choices.append(tuple(set(qs[a] for a in range(p) if vals[a]==vmax)))
   count=1
   for z in choices:count*=len(z)
   if count>cap:return full,None,{'level':t,'estimate':count,'peak':peak}
   new.update(product(*choices))
   if len(new)>cap:return full,None,{'level':t,'estimate':len(new),'peak':peak}
  assignments=new;peak=max(peak,len(new))
 markov={z[0] for z in assignments}
 return full,markov,{'peak':peak}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=4);ap.add_argument('--topics',type=int,default=3);ap.add_argument('--trials',type=int,default=500);args=ap.parse_args()
 rng=random.Random(1001); skipped=0; peaks=0;start=time.time()
 for i in range(args.trials):
  w=tuple(rng.randrange(8) for _ in range(2**args.topics-1));full,markov,info=solve(w,args.players,args.topics);peaks=max(peaks,info['peak'])
  if markov is None:skipped+=1;continue
  if full!=markov:
   print(json.dumps({'weights':w,'only_full':list(full-markov),'full':list(full),'markov':list(markov),'info':info,'trial':i}));break
 else:print(json.dumps({'equal':args.trials-skipped,'skipped':skipped,'peak':peaks,'seconds':time.time()-start}))
