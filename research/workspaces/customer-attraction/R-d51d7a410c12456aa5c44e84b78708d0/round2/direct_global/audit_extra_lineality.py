"""Independent definition-level audit of full_tree's finite lineality witness.

Only reads the instance and policy JSON.  Does not import the canonical solver,
author's matrix builder, or author's audit.
"""
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'full_tree'/'extra_lineality_exact.json'
data=json.loads(SOURCE.read_text())
m,p=data['players'],data['topics']
types=list(range(1,1<<p)); mass=data['weights']
histories=[h for d in range(m) for h in product(range(p),repeat=d)]
policy=dict(zip(histories,data['policy'],strict=True))

def terminal(h):
 while len(h)<m:
  h=h+(policy[h],)
 return tuple(h.count(a) for a in range(p))

def payoff(a,q):
 row=[]
 for mask in types:
  load=sum(q[b] for b in range(p) if mask>>b&1)
  row.append(F(1,load) if mask>>a&1 else F(0))
 return tuple(row)

def minus(x,y): return tuple(a-b for a,b in zip(x,y))
def dot(x,y): return sum(a*b for a,b in zip(x,y))
def rank(rows):
 matrix=[list(row) for row in rows]
 if not matrix:return 0
 pivot=0
 for col in range(len(matrix[0])):
  selected=next((j for j in range(pivot,len(matrix)) if matrix[j][col]),None)
  if selected is None:continue
  matrix[pivot],matrix[selected]=matrix[selected],matrix[pivot]
  coefficient=matrix[pivot][col]
  matrix[pivot]=[x/coefficient for x in matrix[pivot]]
  for j in range(pivot+1,len(matrix)):
   coefficient=matrix[j][col]
   if coefficient:matrix[j]=[a-coefficient*b for a,b in zip(matrix[j],matrix[pivot])]
  pivot+=1
  if pivot==len(matrix):break
 return pivot

rows={}; edges=[]; vertices=set(); slacks={}
for h in histories:
 a=policy[h]; q=terminal(h+(a,)); tail=(a,q)
 for b in range(p):
  r=terminal(h+(b,)); head=(b,r)
  row=minus(payoff(a,q),payoff(b,r))
  rows[h,b]=row; slacks[h,b]=dot(row,mass)
  assert slacks[h,b]>=0,(h,b,slacks[h,b])
  edges.append((tail,head,(h,b)));vertices.update((tail,head))

# Definition-level SCCs by intersecting forward and reverse reachability.
adj={v:[] for v in vertices}; rev={v:[] for v in vertices}
for u,v,_ in edges: adj[u].append(v);rev[v].append(u)
def reach(v,graph):
 seen={v};todo=[v]
 while todo:
  a=todo.pop()
  for b in graph[a]:
   if b not in seen:seen.add(b);todo.append(b)
 return seen
sccs=[];pending=set(vertices)
while pending:
 v=min(pending);component=reach(v,adj)&reach(v,rev)
 sccs.append(component);pending-=component
index={v:i for i,cc in enumerate(sccs) for v in cc}
scc_rows=[rows[key] for u,v,key in edges if index[u]==index[v]]
zero_rows=[row for key,row in rows.items() if slacks[key]==0]
r=rows[(0,0),2];s=rows[(1,0),1];t=rows[(0,0,0),1]
assert all(a+F(2,5)*b+F(4,5)*c==0 for a,b,c in zip(r,s,t))
assert rank([r,s,t])==2
assert rank(zero_rows)==2
assert rank(scc_rows)==1

# Since all seven masses are strictly positive, this exact SPE is interior to
# the nonnegative mass orthant. Any lineality vector of the row cone has both
# signs represented by nonnegative combinations. Pairing those combinations
# with mass shows that every used row has slack zero. Thus its dimension is
# at most rank(zero_rows)=2. The positive dependence on r,s,t shows that their
# two-dimensional span is contained in the cone's lineality, giving equality.
report={
 'status':'PASS', 'histories':len(histories),'all_action_rows':len(rows),
 'nonself_rows':sum(b!=policy[h] for h,b in rows),
 'positive_mass':all(x>0 for x in mass),
 'zero_slack_rows':sum(v==0 for v in slacks.values()),
 'zero_slack_row_span_rank':rank(zero_rows),
 'r':[str(x) for x in r],'s':[str(x) for x in s],'t':[str(x) for x in t],
 'positive_relation':'r+(2/5)s+(4/5)t=0',
 'relation_span_rank':rank([r,s,t]),
 'mapped_row_cone_lineality_rank':2,
 'payoff_graph_vertices':len(vertices),'payoff_graph_sccs':len(sccs),
 'nontrivial_sccs':[
  [{'action':v[0],'counts':v[1]} for v in sorted(cc)]
  for cc in sccs if len(cc)>1],
 'scc_image_rank':rank(scc_rows),
 'actual_counts':terminal(()),
 'actual_welfare':sum(w for mask,w in zip(types,mass) if any(terminal(())[a] for a in range(p) if mask>>a&1))
}
(HERE/'extra_lineality_independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
