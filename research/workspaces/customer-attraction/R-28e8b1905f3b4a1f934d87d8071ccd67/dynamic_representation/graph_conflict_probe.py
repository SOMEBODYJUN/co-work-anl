"""Targeted minimal common-continuation conflict for no-repeat marginal games.
All triple potentials =1; pair potential =0 on a path, 1 otherwise.
"""
from itertools import combinations,product
import json

def probe(p):
 vertices=tuple(range(p));pairs=tuple(combinations(vertices,2))
 def v(a,b):return int(abs(a-b)!=1) # F(pair)
 menus=[tuple(x for x in vertices if x not in ab) for ab in pairs]
 target=frozenset(range(0,p,2))
 if len(target)!=3:raise ValueError
 count=0;valid=0;witness=None
 for cs in product(*menus):
  q=dict(zip(pairs,cs));root_options=[]
  for a in vertices:
   branches=[]
   for b in vertices:
    if a==b:continue
    c=q[tuple(sorted((a,b)))];branches.append((1-v(a,c),1-v(b,c),b,c))
   br=max(x[0] for x in branches)
   opts=[x for x in branches if x[0]==br]
   root_options.append(opts)
  floor=max(min(x[1] for x in opts) for opts in root_options)
  for a,opts in enumerate(root_options):
   for sec,root,b,c in opts:
    if frozenset((a,b,c))==target and root>=floor:
     witness={'last':[[list(ab),c]for ab,c in q.items()],'root':a,'second':b,'last_action':c,'root_floor':floor}
     print(json.dumps({'p':p,'target':sorted(target),'checked':count+1,'witness':witness}));return
  count+=1
 print(json.dumps({'p':p,'target':sorted(target),'checked':count,'witness':None}))
if __name__=='__main__':probe(5)
