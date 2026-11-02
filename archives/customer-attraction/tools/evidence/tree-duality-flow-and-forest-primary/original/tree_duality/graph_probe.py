from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from pathlib import Path
import json

p=3;n=4
masses={1:2,2:2,4:1}
actions={};terms={}
def count(h):return tuple(h.count(a) for a in range(p))
def form(a,q):
 return tuple(F(1,sum(q[b] for b in range(p) if mask>>b&1)) if mask>>a&1 else F(0) for mask in range(1,1<<p))
def u(a,q):return sum((masses.get(mask,0)*x for mask,x in enumerate(form(a,q),1)),F(0))
for d in range(n,-1,-1):
 for h in product(range(p),repeat=d):
  if d==n:terms[h]=count(h);continue
  vals={a:u(a,terms[h+(a,)]) for a in range(p)}
  best=[a for a in range(p) if vals[a]==max(vals.values())]
  if d==n-1:a=next(a for a in [2,0,1] if a in best)
  elif h==(0,1):a=0
  elif h==(1,0):a=1
  else:a=min(best)
  assert a in best,(h,a,vals)
  actions[h]=a;terms[h]=terms[h+(a,)]
rows={};edges=[];adj=defaultdict(list)
for h,a in actions.items():
 for b in range(p):
  v=(b,terms[h+(b,)]);w=(a,terms[h]);
  row=tuple(x-y for x,y in zip(form(*w),form(*v)))
  rows[h,b]=row
  edges.append((v,w,h,b))
  adj[v].append(w)
  adj[w]
# Tarjan
index=0;stack=[];on=set();idx={};low={};scc=[]
def visit(v):
 global index
 idx[v]=low[v]=index;index+=1;stack.append(v);on.add(v)
 for w in adj[v]:
  if w not in idx:visit(w);low[v]=min(low[v],low[w])
  elif w in on:low[v]=min(low[v],idx[w])
 if low[v]==idx[v]:
  c=[]
  while True:
   w=stack.pop();on.remove(w);c.append(w)
   if w==v:break
  scc.append(c)
for v in list(adj):
 if v not in idx:visit(v)
print('root',terms[()], 'u',[(a,u(a,terms[()])) for a in range(p) if terms[()][a]])
print('row AB->B',rows[(0,1),1])
print('row BA->A',rows[(1,0),0])
assert rows[(0,1),1]==tuple(-x for x in rows[(1,0),0])
# No terminal tie differences between same counts
rmap=defaultdict(set)
for h,a in actions.items():
 if len(h)==n-1:rmap[count(h)].add(a)
assert all(len(v)==1 for v in rmap.values())
print('nontrivial scc',len([c for c in scc if len(c)>1]),[len(c) for c in scc if len(c)>1])
print('nodes',len(adj),'rows',len(edges),'positive-type-slacks',sum(sum(x*masses.get(k,0) for k,x in enumerate(row,1))>0 for row in rows.values()))
result={'topics':p,'players':n,'masses':masses,'actions':[{"h":list(h),"a":a} for h,a in sorted(actions.items())], 'root_counts':terms[()], 'early_reciprocal_row':[str(x) for x in rows[(0,1),1]], 'terminal_reply_set_sizes':sorted(len(v) for v in rmap.values()), 'nontrivial_scc_sizes':sorted(len(c) for c in scc if len(c)>1)}
Path(__file__).with_name('graph_probe.json').write_text(json.dumps(result,indent=2))
