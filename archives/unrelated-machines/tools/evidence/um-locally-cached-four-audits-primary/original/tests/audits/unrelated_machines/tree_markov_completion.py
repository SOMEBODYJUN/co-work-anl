#!/usr/bin/env python3
"""Exact five-machine counterexample; no approximation lower bound for all algorithms."""
from fractions import Fraction as F
from itertools import product
import json, hashlib, platform
from pathlib import Path
J=('a','b','d','e','c')
# Machine indices use 1..5. Edge orientation order is explicit.
P={
 'a':{1:F(1),2:F(1,2)},
 'b':{2:F(1,2),3:F(1)},
 'd':{3:F(1),4:F(1,2)},
 'e':{4:F(1,2),5:F(1)},
 'c':{1:F(1),5:F(1)},
}
A={1:('c',),2:('a','b'),3:(),4:('d',),5:('e',)}
B={1:('a',),2:('b',),3:(),4:('d','e'),5:('c',)}
D=((F(1,2),A),(F(1,2),B))
F_EDGES=((1,2),(2,3),(3,4),(4,5))

def load(assignment):
 out={i:F(0) for i in range(1,6)}
 for j,i in assignment.items():
  assert i in P[j]
  out[i]+=P[j][i]
 return out

def from_configs(configs):
 assignment={}
 for i,S in configs.items():
  for j in S:
   assert j not in assignment
   assignment[j]=i
 assert set(assignment)==set(J)
 return assignment

marg={i:{} for i in range(1,6)}
for w,state in D:
 assert max(load(from_configs(state)).values())==1
 for i,S in state.items():marg[i][S]=marg[i].get(S,F(0))+w
pair={}
for u,v in F_EDGES:
 p={}
 for w,state in D:
  key=state[u],state[v];p[key]=p.get(key,F(0))+w
 pair[u,v]=p

# Full assignment oracle independently enumerates every legal schedule.
all_assignments=[]
for choices in product(*(P[j] for j in J)):
 assignment=dict(zip(J,choices));all_assignments.append((max(load(assignment).values()),assignment))
opt=min(v for v,s in all_assignments)
assert len(all_assignments)==32 and opt==1

# Markov gluing of the GIVEN FULL pair marginals along the selected forest.
outputs=[]
for choices in product(*(marg[i] for i in range(1,6))):
 state=dict(zip(range(1,6),choices));w=marg[1][state[1]]
 for u,v in F_EDGES:
  w*=pair[u,v].get((state[u],state[v]),F(0))/marg[u][state[u]]
 if not w:continue
 # Preserve only the four forest jobs, discarding c from the full states.
 partial={}
 for i,S in state.items():
  for j in S:
   if j=='c':continue
   assert j not in partial
   partial[j]=i
 assert set(partial)==set(J)-{'c'}
 tree_load=load(partial)
 completions=[(max(load(partial|{'c':i}).values()),i) for i in P['c']]
 best=min(v for v,i in completions)
 outputs.append(dict(state=state,weight=w,partial=partial,tree_load=tree_load,
                     completion_optimum=best,best_c_machines=[i for v,i in completions if v==best]))
assert len(outputs)==4 and sum(x['weight'] for x in outputs)==1
assert sorted(x['completion_optimum'] for x in outputs)==[F(1),F(1),F(1),F(2)]
# Independently verify every full single-machine marginal survived Markov gluing.
for i in range(1,6):
 actual={}
 for x in outputs:
  S=x['state'][i];actual[S]=actual.get(S,F(0))+x['weight']
 assert actual==marg[i]
for u,v in F_EDGES:
 actual={}
 for x in outputs:
  key=x['state'][u],x['state'][v]
  actual[key]=actual.get(key,F(0))+x['weight']
 assert actual==pair[u,v]
bad=[x for x in outputs if x['completion_optimum']==2]
assert len(bad)==1 and bad[0]['tree_load'][1]==bad[0]['tree_load'][5]==1
assert bad[0]['weight']==F(1,4)

payload={
 'python':platform.python_version(),'arithmetic':'exact Fraction; no numerical tolerance',
 'random_seed':None,
 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'input_processing_times':{j:{str(i):str(p) for i,p in e.items()} for j,e in P.items()},
 'target':'1','exact_OPT':str(opt),'complete_orientations_enumerated':len(all_assignments),
 'global_distribution':[dict(weight=str(w),configs=state) for w,state in D],
 'forest_edges':F_EDGES,
 'pair_marginals':{str(uv):[dict(configs=ss,weight=str(w)) for ss,w in p.items()] for uv,p in pair.items()},
 'markov_outputs':[{**x,'weight':str(x['weight']),'tree_load':{str(i):str(p) for i,p in x['tree_load'].items()},'completion_optimum':str(x['completion_optimum'])} for x in outputs],
 'refuted_contract':'Every positive-probability tree-glued support state, with forest-job assignments frozen, can be completed at makespan strictly below 2T.',
 'limits':'Chosen forest and Markov gluing; does not exclude repair-aware state selection, changing the forest, or moving already assigned jobs.',
}
print(json.dumps(payload,ensure_ascii=False,indent=2))
