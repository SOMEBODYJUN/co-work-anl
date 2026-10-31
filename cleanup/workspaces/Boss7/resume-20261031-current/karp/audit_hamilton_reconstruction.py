"""Exhaustive tiny graphs for the reconstructed Karp node-cover Hamilton gadget."""
from itertools import combinations
from functools import lru_cache
from pathlib import Path
import json,hashlib

def has_cover(n,edges,budget):
 return any(all(u in chosen or v in chosen for u,v in edges) for size in range(budget+1) for chosen in combinations(range(n),size))
def graph(edges,budget):
 vertices=[('a',f) for f in range(budget)]
 for i,(u,v) in enumerate(edges):vertices.extend((u,i,b) for u in (u,v) for b in (0,1))
 idx={x:i for i,x in enumerate(vertices)};adj=[set() for _ in vertices]
 def arc(x,y):adj[idx[x]].add(idx[y])
 for i,(u,v) in enumerate(edges):
  for w in (u,v):arc((w,i,0),(w,i,1))
  for b in (0,1):arc((u,i,b),(v,i,b));arc((v,i,b),(u,i,b))
 for u in sorted({w for e in edges for w in e}):
  incidence=[i for i,e in enumerate(edges) if u in e]
  for i,j in zip(incidence,incidence[1:]):arc((u,i,1),(u,j,0))
  for f in range(budget):arc(('a',f),(u,incidence[0],0));arc((u,incidence[-1],1),('a',f))
 return vertices,adj

def ham(adj):
 n=len(adj);full=(1<<n)-1
 @lru_cache(None)
 def dfs(u,mask):
  if mask==full:return 0 in adj[u]
  return any(dfs(v,mask|(1<<v)) for v in adj[u] if not mask>>v&1)
 return dfs(0,1)
checks=[]
for n in (2,3):
 all_edges=list(combinations(range(n),2))
 for mask in range(1,1<<len(all_edges)):
  edges=[e for i,e in enumerate(all_edges) if mask>>i&1]
  active=sorted({v for e in edges for v in e});ren={v:i for i,v in enumerate(active)}
  normalized=[(ren[u],ren[v]) for u,v in edges]
  for budget in range(1,len(active)+1):
   vertices,adj=graph(normalized,budget)
   lhs=has_cover(len(active),normalized,budget);rhs=ham(adj)
   assert lhs==rhs,(n,edges,budget,lhs,rhs)
   checks.append({'original_n':n,'edges':edges,'budget':budget,'output_vertices':len(vertices),'cover':lhs,'hamilton':rhs})
base=Path(__file__).resolve().parent
result={'scope':'All nonempty simple graphs on labelled n=2,3 vertices and every effective positive budget after removing isolated vertices. Finite verification only; general proof in literature object.','case_count':len(checks),'max_output_vertices':max(x['output_vertices'] for x in checks),'checks':checks,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(base/'hamilton-reconstruction-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('scope','case_count','max_output_vertices')},ensure_ascii=False))
