from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
BASE=Path(__file__).resolve().parent
TYPES={3:1,5:2,6:1,7:5,10:2,11:16,12:8,13:6,14:9}
PLAYERS=4

def payoff(path):
 return tuple(sum((F(w,sum(1 for t in path if mask>>t&1)) for mask,w in TYPES.items() if mask>>a&1),F(0)) for a in path)
def welfare(path):return sum(w for mask,w in TYPES.items() if any(mask>>a&1 for a in path))
def choose(h):
 if len(h)==0:return 0
 if len(h)==1:return 0 if h==(3,) else 3
 if len(h)==2:return 0 if h==(3,3) else 3
 assert len(h)==3
 if h.count(3)==3:return 1
 if h.count(3)==2 and 1 in h:return 2
 if h.count(3)==2 and 2 in h:return 1
 return 3
def rollout(h):
 while len(h)<PLAYERS:h=h+(choose(h),)
 return h
margins=[]
for d in range(PLAYERS):
 for h in product(range(4),repeat=d):
  real=rollout(h);u=payoff(real)[d]
  for a in range(4):
   dev=rollout(h+(a,));v=payoff(dev)[d]
   assert u>=v,(h,a,u,v)
   margins.append(u-v)

pne=[]; nonpne={}
for path in product(range(4),repeat=4):
 c=tuple(path.count(a) for a in range(4))
 if c in nonpne or c in [p[0] for p in pne]:continue
 u=payoff(path);bad=None
 for i in range(4):
  for a in range(4):
   dev=path[:i]+(a,)+path[i+1:]
   if payoff(dev)[i]>u[i]:bad=(i,a,str(payoff(dev)[i]-u[i]));break
  if bad:break
 if bad:nonpne[c]=bad
 else:pne.append((c,welfare(path),tuple(map(str,u))))
assert min(v for _,v,_ in pne)==50
root=rollout(())
assert root==(0,3,3,3) and welfare(root)==49
assert sum(TYPES.values())==50
cert=json.load(open(BASE/'pne_bridge_reduced.json'))
assert cert['instance']['players']==PLAYERS
assert cert['certificate']['terminal_counts']==[1,0,0,3]
for row in cert['certificate']['actions']:
 assert choose(tuple(row['history']))==row['action']
print(json.dumps({'types_mask':TYPES,'on_path':root,'utilities':list(map(str,payoff(root))),'welfare':welfare(root),'OPT':50,'SPE_histories':sum(4**d for d in range(4)),'SPE_deviation_checks':len(margins),'min_SPE_margin':str(min(margins)),'PNE_count_vectors':pne,'nonPNE_count_vectors':len(nonpne),'root_action_values':{str(a):str(payoff(rollout((a,)))[0]) for a in range(4)}},indent=2))
