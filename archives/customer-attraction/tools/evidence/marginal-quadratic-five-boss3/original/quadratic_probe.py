"""Exploratory exact BI + floating static security for symmetric quadratic potentials."""
import argparse,json,random,time
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def evaluate(G,h,m):
 k=len(h)
 @lru_cache(None)
 def pay(s):return tuple(h[a]-sum(G[a][b]*(s[b]-(a==b)) for b in range(k)) for a in range(k))
 @lru_cache(None)
 def solve(q):
  if sum(q)==m:return frozenset([q])
  ch=[];th=[]
  for a in range(k):
   v=list(q);v[a]+=1;c=solve(tuple(v));ch.append(c);th.append(min(pay(s)[a] for s in c))
  floor=max(th)
  return frozenset(s for a,c in enumerate(ch) for s in c if pay(s)[a]>=floor)
 zeros=(0,)*k;outs=solve(zeros)
 worst=min(outs,key=lambda s:sum(s[a]*pay(s)[a] for a in range(k)))
 welfare=sum(worst[a]*pay(worst)[a] for a in range(k))
 # v=max_p h*p -(m-1)*max_b G[p,b]
 A=np.array([[-h[a]+(m-1)*G[a][b] for a in range(k)]+[1.] for b in range(k)])
 res=linprog([0.]*k+[-1.],A_ub=A,b_ub=[0.]*k,A_eq=[[1.]*k+[0.]],b_eq=[1.],bounds=[(0,None)]*k+[(None,None)],method='highs')
 assert res.success
 v=-res.fun
 return {'welfare':welfare,'security':v,'gap':welfare-m*v,'worst_counts':worst,'query':res.x[:k].tolist()}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=1000);ap.add_argument('--topics',type=int,default=5);ap.add_argument('--players',type=int,default=3);ap.add_argument('--seed',type=int,default=19);ap.add_argument('--out',default='quadratic_probe.json');arg=ap.parse_args();rng=random.Random(arg.seed);best=None;start=time.time()
 for t in range(arg.games):
  k=arg.topics;m=arg.players;cap=10
  G=[[0]*k for _ in range(k)]
  for a in range(k):
   G[a][a]=cap
   for b in range(a):G[a][b]=G[b][a]=rng.randrange(cap+1)
  h=[(m-1)*cap+(rng.randrange(15) if t%2 else 0) for a in range(k)]
  ans=evaluate(G,h,m);ans.update(G=G,h=h,trial=t)
  if best is None or ans['gap']<best['gap']-1e-8:best=ans;print(json.dumps(best),flush=True)
  if best['gap']<-1e-7:break
 result={'status':'finite exploratory search only','args':vars(arg),'best':best,'elapsed_seconds':time.time()-start}
 Path(__file__).with_name(arg.out).write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
