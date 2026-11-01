"""Exact finite exploratory attack on the residual cardinality-curve candidate.
No finite success proves a universal claim. Uses integer payoff scaling, not floats.
"""
import argparse,json,math,random,time
from functools import lru_cache
from itertools import combinations
from pathlib import Path

def probe(k,m,w):
 scale=math.lcm(*range(1,m+1)); masks=list(w)
 @lru_cache(None)
 def pay(s):
  u=[0]*k
  for mask in masks:
   load=sum(s[a] for a in range(k) if mask>>a&1)
   if load:
    for a in range(k):
     if s[a] and mask>>a&1:u[a]+=w[mask]*(scale//load)
  return tuple(u)
 @lru_cache(None)
 def solve(q):
  if sum(q)==m:return frozenset([q])
  children=[];floors=[]
  for a in range(k):
   v=list(q);v[a]+=1;child=solve(tuple(v));children.append(child)
   floors.append(min(pay(s)[a] for s in child))
  t=max(floors);threshold[q]=t
  return frozenset(s for a,child in enumerate(children) for s in child if pay(s)[a]>=t)
 threshold={};zeros=(0,)*k;outs=solve(zeros)
 def curve(rootmask,residual):
  arr=[0]*(m+1)
  ww={mask:count for mask,count in w.items() if not residual or not mask&rootmask}
  for r in range(1,m+1):
   arr[r]=max((sum(count for mask,count in ww.items() if mask&sum(1<<a for a in J)) for J in combinations(range(k),min(r,k))),default=0)
  return arr
 for s in sorted(outs):
  smask=sum(1<<a for a in range(k) if s[a]);u=pay(s)
  for residual in (True,):
   f=curve(smask,residual);seen=set();stack=[zeros]
   while stack:
    q=stack.pop()
    if q in seen or sum(q)==m:continue
    seen.add(q);r=m-sum(q)
    for a in range(k):
     if q[a]>=s[a]:continue
     v=list(q);v[a]+=1;v=tuple(v)
     if s in solve(v) and u[a]>=threshold[q]:
      gap=f[r]-f[r-1]
      if u[a]<gap*scale:
       return dict(players=m,topics=k,weights=w,target=s,prefix=q,action=a,residual=residual,curve=f,payoff=f'{u[a]}/{scale}',gap=gap)
      stack.append(v)
 return None

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=1);ap.add_argument('--games',type=int,default=100);ap.add_argument('--topics',type=int,default=6);ap.add_argument('--players',type=int,default=3);ap.add_argument('--out',default='marginal_curve_probe.json');args=ap.parse_args();rng=random.Random(args.seed);start=time.time();viol=[]
 for trial in range(args.games):
  k=args.topics;m=args.players
  # Alternate sparse random systems and a protected incumbent market plus outsiders.
  if trial%2:
   w={1:rng.randrange(1,20)}
   for mask in range(2,1<<k):
    if rng.random()<.15:w[mask]=rng.randrange(1,8)
  else:w={mask:rng.randrange(1,8) for mask in range(1,1<<k) if rng.random()<.2}
  if not w:continue
  v=probe(k,m,w)
  if v:
   v['trial']=trial;viol.append(v);print(json.dumps(v),flush=True)
   if v['residual']:break
  if trial%10==0:print('progress',trial,round(time.time()-start,2),flush=True)
 ans=dict(status='finite exact exploratory probe',args=vars(args),violations=viol,elapsed_seconds=time.time()-start)
 Path(__file__).with_name(args.out).write_text(json.dumps(ans,indent=2)+'\n')
if __name__=='__main__':main()
