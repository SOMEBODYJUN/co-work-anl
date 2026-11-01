"""Independent exact recursions; no canonical solver or HI implementation import."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse,json

def compositions(n,q):
 if q==1:yield(n,);return
 for a in range(n+1):
  for tail in compositions(n-a,q-1):yield(a,)+tail

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args();reports=[]
 for q in range(1,7):
  m=q+1;floors={};allowed={};checked=0
  def add(b,a):return b[:a]+(b[a]+1,)+b[a+1:]
  def u(z,a):return F(1,z[a]) if z[a] else F(0)
  @lru_cache(None)
  def exact(b):
   if sum(b)==m:return frozenset({b})
   children=[exact(add(b,a)) for a in range(q)]
   floor=max(min(u(z,a) for z in child) for a,child in enumerate(children))
   return frozenset(z for a,child in enumerate(children) for z in child if u(z,a)>=floor)
  @lru_cache(None)
  def interval(b):
   if sum(b)==m:return frozenset({b})
   children=[interval(add(b,a)) for a in range(q)]
   floor=max(min(u(z,a) for z in child) for a,child in enumerate(children))
   actions=[a for a,child in enumerate(children) if max(u(z,a) for z in child)>=floor]
   floors[b]=floor;allowed[b]=actions
   return frozenset(z for a in actions for z in children[a])
  @lru_cache(None)
  def cost(b):
   if sum(b)==m:return F(0)
   interval(b);return floors[b]+min(cost(add(b,a)) for a in allowed[b])
  for n in range(m+1):
   for b in compositions(n,q):
    r=m-n;H=interval(b);R=exact(b)
    if not r:expected={b};expected_cost=F(0)
    elif max(b)>=2:
     fresh=[a for a in range(q) if not b[a]];expected=set()
     for chosen in combinations(fresh,r):
      z=list(b)
      for a in chosen:z[a]+=1
      expected.add(tuple(z))
     expected_cost=F(r);assert floors[b]==1
    else:
     expected={tuple(2 if a==d else 1 for a in range(q)) for d in range(q)}
     expected_cost=F(r,2);assert floors[b]==F(1,2)
    assert H==R==expected,(q,b,H,R,expected)
    assert cost(b)==expected_cost,(q,b,cost(b),expected_cost)
    checked+=1
  root=(0,)*q;assert cost(root)==F(m,2)
  reports.append({'q':q,'players':m,'all_prefix_states':checked,'G':str(cost(root)),'SPE_welfare':q,'twice_G_minus_OPT':str(2*cost(root)-q)})
 report={'status':'exact finite replay; arbitrary q conclusion rests on the written induction','checks':reports}
 if args.output:
  if args.output.exists():raise FileExistsError(args.output)
  args.output.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report))

if __name__=='__main__':main()
