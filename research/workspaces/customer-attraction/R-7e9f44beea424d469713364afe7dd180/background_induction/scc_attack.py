"""Independently reconstruct payoff graph and seek mapped cone lineality beyond SCCs."""
from itertools import product
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import json,numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).parent

def tarjan(n,edges):
 adj=[[]for _ in range(n)]
 for a,b in edges:adj[a].append(b)
 stack=[];on=set();idx={};lo={};out=[]
 def visit(a):
  idx[a]=lo[a]=len(idx);stack.append(a);on.add(a)
  for b in adj[a]:
   if b not in idx:visit(b);lo[a]=min(lo[a],lo[b])
   elif b in on:lo[a]=min(lo[a],idx[b])
  if lo[a]==idx[a]:
   comp=[]
   while True:
    b=stack.pop();on.remove(b);comp.append(b)
    if b==a:break
   out.append(comp)
 for a in range(n):
  if a not in idx:visit(a)
 return out

def graph(q,m,policy):
 masks=list(range(1,1<<q));verts=[];vid={};edges=[];names=[]
 def terminal(h):
  while len(h)<m:h=h+(policy[h],)
  return tuple(h.count(a)for a in range(q))
 def vertex(c,a):
  key=(c,a)
  if key not in vid:vid[key]=len(verts);verts.append(key)
  return vid[key]
 for h,a in policy.items():
  s=vertex(terminal(h),a)
  for b in range(q):
   t=vertex(terminal(h+(b,)),b)
   if s!=t:edges.append((s,t));names.append((h,b))
 F=[]
 for c,a in verts:
  F.append([Fraction(1,sum(c[b]for b in range(q)if mask>>b&1)) if mask>>a&1 else Fraction(0)for mask in masks])
 G=[[x-y for x,y in zip(F[s],F[t])]for s,t in edges]
 return verts,edges,names,F,G

if __name__=='__main__':
 q,m=2,3;hist=[h for depth in range(m)for h in product(range(q),repeat=depth)]
 for trial,actions in enumerate(product(range(q),repeat=len(hist))):
  pol=dict(zip(hist,actions));v,e,n,F,G=graph(q,m,pol);scc=tarjan(len(v),e);sc={a:i for i,comp in enumerate(scc)for a in comp}
  arr=np.array(G,dtype=float);inside=[j for j,(a,b)in enumerate(e)if sc[a]==sc[b]]
  rankin=np.linalg.matrix_rank(arr[inside]) if inside else 0
  reversible=[];witness={}
  for j,row in enumerate(arr):
   res=linprog(np.ones(len(e)),A_eq=arr.T,b_eq=-row,bounds=(0,None),method='highs')
   if res.success:reversible.append(j);witness[j]=res.x
  rankall=np.linalg.matrix_rank(arr[reversible])if reversible else 0
  if rankall>rankin:
   obj={'q':q,'m':m,'trial':trial,'policy':[{'h':h,'a':a}for h,a in pol.items()],'vertices':v,'edges':e,'edge_names':n,'F':[[str(x)for x in row]for row in F],'G':[[str(x)for x in row]for row in G],'SCCs':scc,'inside_edges':inside,'reversible_edges':reversible,'SCC_image_rank':int(rankin),'image_lineality_rank':int(rankall)}
   for j in reversible:
    if np.linalg.matrix_rank(np.vstack([arr[inside],arr[j]]))>rankin:
     fr=[Fraction(float(z)).limit_denominator(10000)for z in witness[j]]
     assert all(sum(fr[k]*G[k][i]for k in range(len(e)))==-G[j][i]for i in range(len(G[0])))
     obj['additional_reversible_edge']=j;obj['reverse_multipliers']=[str(x)for x in fr];break
   (ROOT/'mapped_extra_lineality.json').write_text(json.dumps(obj,indent=2));print(json.dumps(obj,indent=2));break
 else:print('none')
