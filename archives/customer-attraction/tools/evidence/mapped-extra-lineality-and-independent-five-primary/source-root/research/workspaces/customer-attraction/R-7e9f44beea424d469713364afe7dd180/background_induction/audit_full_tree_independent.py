#!/usr/bin/env python3
"""Independent exact review of the full-tree payoff-graph example and warning.
Does not import the author's script, canonical solver, LP, or graph libraries.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json

def rank(rows):
 a=[list(map(F,row))for row in rows];r=0
 for j in range(len(a[0])if a else 0):
  k=next((i for i in range(r,len(a))if a[i][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
  for i in range(len(a)):
   if i!=r:
    v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  r+=1
 return r

def check(q,m,policy,weights):
 masks=list(range(1,1<<q));customers=[mask for mask,w in weights.items()for _ in range(w)]
 def leaf(h):
  while len(h)<m:h=h+(policy[h],)
  return h
 def vertex(h,a):
  t=leaf(h+(a,));return(tuple(t.count(b)for b in range(q)),a)
 def vec(v):
  c,a=v;return tuple(F(1,sum(c[b]for b in range(q)if mask>>b&1))if mask>>a&1 else F(0)for mask in masks)
 def payoff(h,a):
  return sum((F(1,sum(int(bool(mask>>b&1))for b in h))for mask in customers if mask>>a&1),F(0))
 rows={};end={};graph={}
 for dep in range(m):
  for h in product(range(q),repeat=dep):
   chosen=policy[h];on=leaf(h)
   for a in range(q):
    off=leaf(h+(a,));source=vertex(h,a);target=vertex(h,chosen)
    row=tuple(x-y for x,y in zip(vec(target),vec(source)))
    exact=payoff(on,chosen)-payoff(off,a)
    assert exact==sum(row[mask-1]*w for mask,w in weights.items()) and exact>=0
    rows[h,a]=row;end[h,a]=(source,target)
    graph.setdefault(source,set()).add(target);graph.setdefault(target,set())
 def reach(v):
  out={v};todo=[v]
  while todo:
   for w in graph[todo.pop()]:
    if w not in out:out.add(w);todo.append(w)
  return out
 reachs={v:reach(v)for v in graph};remain=set(graph);scc=[]
 while remain:
  v=min(remain);s={w for w in remain if w in reachs[v]and v in reachs[w]};scc.append(s);remain-=s
 H=[]
 for s in scc:
  rep=min(s)
  H.extend(tuple(x-y for x,y in zip(vec(v),vec(rep)))for v in s)
 tt=[]
 for h in product(range(q),repeat=m-1):
  for g in product(range(q),repeat=m-1):
   if sorted(h)==sorted(g)and policy[h]!=policy[g]:tt.append(rows[h,policy[g]])
 return rows,end,rank(H),rank(tt),leaf(()),len(graph),len(scc)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
 q,m=3,3;policy={():2,(0,):1,(1,):1,(2,):1}
 table=((1,1,1),(1,0,0),(1,1,1));policy.update({(a,b):table[a][b]for a,b in product(range(q),repeat=2)})
 rows,ends,hr,tr,leaf,nv,ns=check(q,m,policy,{1:3,2:5,3:3,4:3,5:1,6:3})
 assert (hr,tr,leaf)==(3,1,(2,1,1)) and len(rows)==39
 for cycle in [[((),0),((1,1),2)],[((1,),0),((),1),((1,1),2)]]:
  assert all(sum(rows[key][j]for key in cycle)==0 for j in range(7))
  assert all(ends[cycle[k]][1]==ends[cycle[(k+1)%len(cycle)]][0]for k in range(len(cycle)))
 # Additional mapped lineality beyond SCC image, a legal degenerate SPE.
 pol={():0,(0,):0,(1,):0,(0,0):0,(0,1):0,(1,0):1,(1,1):0}
 rr,ee,h2,t2,ll,n2,s2=check(2,3,pol,{3:1})
 g0=rr[(),1];g5=rr[(1,0),0];g6=rr[(1,1),1]
 assert g0==(F(1,3),F(-1,2),0)and g5==(F(-1,2),F(1,2),0)and g6==(1,F(-1,3),0)
 assert all(-g0[j]==F(7,6)*g5[j]+F(1,4)*g6[j]for j in range(3))
 assert all(-g6[j]==4*g0[j]+F(14,3)*g5[j]for j in range(3))
 assert h2==1 and rank([g5,g6])==2
 out={'status':'independent_exact_audit_passed','theorem_review':'Equations (4),(5),(6),(7) correct as fixed-strategy identities; general half OPEN','example':{'comparisons':len(rows),'vertices':nv,'SCCs':ns,'terminal_tie_rank':tr,'all_depth_SCC_image_rank':hr,'root':leaf},'mapped_warning':{'players':3,'topics':2,'SCC_image_rank':h2,'row_cone_lineality_rank':2,'identity':'-g0=(7/6)g5+(1/4)g6','g0':list(map(str,g0)),'g5':list(map(str,g5)),'g6':list(map(str,g6))}}
 text=json.dumps(out,indent=2)
 if args.output:
  with args.output.open('x')as f:f.write(text+'\n')
 print(text)
if __name__=='__main__':main()
