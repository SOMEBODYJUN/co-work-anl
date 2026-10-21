"""Exact finite SPE exploration for global submodular Shapley potentials.
Welfare C(S) is rank over GF(2) of the union of topic vector bundles. This is
monotone submodular, with global DR+self-congestion Shapley potential; it need
not be a nonnegative coverage function. Static safety LP is only a proposal;
negative candidates are rationally verified from every background.
"""
import argparse,json,math,random,time
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def rank(vs):
 piv={}
 for v in vs:
  while v:
   b=v.bit_length()-1
   if b in piv:v^=piv[b]
   else:piv[b]=v;break
 return len(piv)
def sample(rng,k,d):
 return [sorted(set(rng.randrange(1,1<<d) for _ in range(rng.randrange(1,5)))) for a in range(k)]
def coverage(bundles):
 k=len(bundles);return [rank([v for a in range(k) if S>>a&1 for v in bundles[a]]) for S in range(1<<k)]
def signed_weights(C,k):
 full=(1<<k)-1;w={}
 for B in range(1,1<<k):
  z=0;D=B
  while True:
   z+=(-1 if (B.bit_count()-D.bit_count())%2 else 1)*(C[full]-C[full^D])
   if not D:break
   D=(D-1)&B
  if z:w[B]=z
 return w
class Solver:
 def __init__(self,C,k,m):self.C=C;self.k=k;self.m=m;self.scale=math.lcm(*range(1,m+1));self.w=signed_weights(C,k);self.th={}
 @lru_cache(None)
 def pay(self,q):
  u=[0]*self.k
  for B,w in self.w.items():
   load=sum(q[a] for a in range(self.k) if B>>a&1)
   if load:
    for a in range(self.k):
     if q[a] and B>>a&1:u[a]+=w*(self.scale//load)
  return tuple(u)
 @lru_cache(None)
 def solve(self,q):
  if sum(q)==self.m:return frozenset([q])
  ch=[];mins=[]
  for a in range(self.k):
   v=list(q);v[a]+=1;c=self.solve(tuple(v));ch.append(c);mins.append(min(self.pay(s)[a] for s in c))
  t=max(mins);self.th[q]=t
  return frozenset(s for a,c in enumerate(ch) for s in c if self.pay(s)[a]>=t)
 def certificate(self,target):
  acts={};m=self.m;k=self.k
  def expand(h,q,s):
   if len(h)==m:return
   admiss=[]
   for a in range(k):
    z=list(q);z[a]+=1
    if s in self.solve(tuple(z)) and self.pay(s)[a]>=self.th[q]:admiss.append(a)
   a=admiss[0];acts[h]=a
   for b in range(k):
    z=list(q);z[b]+=1;z=tuple(z)
    child=s if b==a else min(self.solve(z),key=lambda t:(self.pay(t)[b],t))
    expand(h+(b,),z,child)
  expand((),(0,)*k,target)
  return [{'history':h,'action':a} for h,a in sorted(acts.items(),key=lambda z:(len(z[0]),z[0]))]
 def evaluate(self):
  k=self.k;m=self.m;zeros=(0,)*k;out=self.solve(zeros)
  target=min(out,key=lambda q:(self.C[sum(1<<a for a in range(k) if q[a])],q));W=self.C[sum(1<<a for a in range(k) if target[a])]
  backgrounds=[q for q in self.th if sum(q)==m-1]
  A=[];AA=[]
  for b in backgrounds:
   row=[]
   for a in range(k):
    q=list(b);q[a]+=1;row.append(F(self.pay(tuple(q))[a],self.scale))
   AA.append(row);A.append([-float(v) for v in row]+[1.])
  lp=linprog([0.]*k+[-1.],A_ub=A,b_ub=[0.]*len(A),A_eq=[[1.]*k+[0.]],b_eq=[1.],bounds=[(0,None)]*k+[(None,None)],method='highs');assert lp.success
  v=-lp.fun;ans={'welfare':W,'security_float':v,'gap_float':W-m*v,'target':target,'query_float':lp.x[:k].tolist()}
  if W-m*v<-1e-8:
   pp=[F(float(p)).limit_denominator(10**6) for p in lp.x[:k]];pp=[p/sum(pp) for p in pp];guarantee=min(sum(p*z for p,z in zip(pp,row)) for row in AA)
   if W<m*guarantee:ans.update(query=[str(p) for p in pp],exact_safety_lower_bound=str(guarantee),exact_gap=str(W-m*guarantee),actions=self.certificate(target),coverage=C,signed_weights=self.w)
  return ans

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=37);ap.add_argument('--topics',type=int,default=6);ap.add_argument('--players',type=int,default=3);ap.add_argument('--dimension',type=int,default=6);ap.add_argument('--games',type=int,default=1000);ap.add_argument('--out',default='matroid_bundle_probe.json');a=ap.parse_args();rng=random.Random(a.seed);best=None;start=time.time();seen=set()
 for trial in range(a.games):
  bundles=sample(rng,a.topics,a.dimension);global C;C=coverage(bundles)
  if tuple(C) in seen:continue
  seen.add(tuple(C));s=Solver(C,a.topics,a.players);ans=s.evaluate();ans.update(bundles=bundles,trial=trial)
  if best is None or ans['gap_float']<best['gap_float']-1e-8:best=ans;print(json.dumps({k:v for k,v in best.items() if k not in ['actions','coverage','signed_weights']}),flush=True)
  if 'exact_gap' in ans:break
 result={'status':'finite exact BI exploration, LP safety proposals; exact candidate if explicitly marked','args':vars(a),'best':best,'distinct_functions':len(seen),'elapsed_seconds':time.time()-start}
 Path(__file__).with_name(a.out).write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
