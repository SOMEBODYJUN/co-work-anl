"""Exact local audit of payoff comparison graph identities.
No SPE-solving code or existing cone construction is imported.
The universal claims are proved in payoff_comparison_graph.md; these finite
checks detect implementation/index errors, not a universal half-coverage proof.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
from collections import deque
from math import comb
import random,json


def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def scale(x,t):return tuple(a*t for a in x)

def row(p,v):
 a,q=v
 return tuple(Fraction(1,sum(q[b] for b in range(p)if mask>>b&1)) if mask>>a&1 else Fraction() for mask in range(1,1<<p))

def check(p,m,actions):
 histories=[h for d in range(m)for h in product(range(p),repeat=d)]
 assert set(actions)==set(histories)
 terminal={}
 for d in range(m,-1,-1):
  for h in product(range(p),repeat=d):
   terminal[h]=tuple(h.count(a)for a in range(p))if d==m else terminal[h+(actions[h],)]
 edges=[];vertices=set()
 for h in histories:
  s=actions[h];target=(s,terminal[h]);vertices.add(target)
  for a in range(p):
   source=(a,terminal[h+(a,)]);vertices.add(source)
   edges.append((source,target,sub(row(p,target),row(p,source))))
 vertices=sorted(vertices);adj={v:[]for v in vertices}
 for j,(s,t,r)in enumerate(edges):adj[s].append((t,j))
 def path(s,t):
  queue=deque([s]);prev={s:None}
  while queue:
   v=queue.popleft()
   if v==t:break
   for w,j in adj[v]:
    if w not in prev:prev[w]=(v,j);queue.append(w)
  if t not in prev:return None
  result=[];v=t
  while prev[v]is not None:v,j=prev[v];result.append(j)
  return result[::-1]
 reach={v:{w for w in vertices if path(v,w)is not None}for v in vertices}
 components=[];unseen=set(vertices)
 while unseen:
  v=min(unseen);C={w for w in unseen if w in reach[v]and v in reach[w]};components.append(C);unseen-=C
 cid={v:i for i,C in enumerate(components)for v in C};reps=[min(C)for C in components]
 zero=(Fraction(),)*((1<<p)-1);checks=0
 for C in components:
  for u,v in product(C,repeat=2):
   terms=path(u,v);assert terms is not None
   value=zero
   for j in terms:value=add(value,edges[j][2])
   assert value==sub(row(p,v),row(p,u));checks+=1
 for s,t,r in edges:
  Cs,Ct=cid[s],cid[t];rs,rt=reps[Cs],reps[Ct]
  internal=add(sub(row(p,t),row(p,rt)),sub(row(p,rs),row(p,s)))
  quotient=sub(row(p,rt),row(p,rs))
  assert r==add(internal,quotient);checks+=1
  if Cs!=Ct:
   walk=path(rs,s)+[next(j for j,e in enumerate(edges)if e[0]==s and e[1]==t)]+path(t,rt)
   value=zero
   for j in walk:value=add(value,edges[j][2])
   assert value==quotient;checks+=1
 # F injection and top-lattice discrete potential identity.
 seen={}
 def harmonic(k):return sum((Fraction(1,j)for j in range(1,k+1)),Fraction())
 for v in vertices:
  f=row(p,v);assert f not in seen or seen[f]==v;seen[f]=v
  a,q=v;qprev=list(q);qprev[a]-=1
  delta=tuple(harmonic(sum(q[b]for b in range(p)if mask>>b&1))-harmonic(sum(qprev[b]for b in range(p)if mask>>b&1))for mask in range(1,1<<p))
  assert f==delta;checks+=1
 assert len(vertices)<=p*comb(m+p-2,p-1)
 q=terminal[()]
 welfare=tuple(Fraction(any(q[a] and mask>>a&1 for a in range(p)))for mask in range(1,1<<p))
 paid=zero
 for a in range(p):
  if q[a]:paid=add(paid,scale(row(p,(a,q)),q[a]))
 assert paid==welfare;checks+=1
 return {'topics':p,'players':m,'vertices':len(vertices),'edges':len(edges),'scc_sizes':sorted(map(len,components),reverse=True),'checks':checks}

def main():
 rng=random.Random(830217);cases=[]
 for p,m in [(1,1),(1,4),(2,2),(2,3),(2,4),(3,2),(3,3),(3,4)]:
  for sample in range(8):
   actions={h:rng.randrange(p)for d in range(m)for h in product(range(p),repeat=d)}
   cases.append(check(p,m,actions))
 result={'scope':'finite exact implementation audit of general proved graph identities; no universal welfare claim','cases':len(cases),'checks':sum(x['checks']for x in cases),'max_vertices':max(x['vertices']for x in cases),'nontrivial_scc_cases':sum(any(s>1 for s in x['scc_sizes'])for x in cases),'details':cases}
 print(json.dumps(result,indent=2))

if __name__=='__main__':main()
