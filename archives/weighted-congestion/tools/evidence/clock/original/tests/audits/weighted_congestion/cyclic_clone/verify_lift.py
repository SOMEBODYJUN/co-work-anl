"""Literal Fraction audit of cyclic equal-weight clones and complementary pairs.
No repository files or external services are read or changed.
"""
from fractions import Fraction as F
from collections import Counter
import itertools,json

def audit(weights,N,a,b,K,d,orientation=1):
 assert 0<=a<len(weights) and 0<=b<len(weights) and a!=b
 assert 1<=K<=N and orientation in (-1,1)
 players=[(j,c) for j in range(N) for c in range(len(weights))]
 pos={p:i for i,p in enumerate(players)}
 initial={p:set() for p in players}; users={}
 delta=int(a>b)
 for j in range(N):
  heavy=(j,a); lights=[((j+delta+k)%N,b) for k in range(K)]
  for side in (0,1):users[(j,side)]=set()
  initial[heavy].add((j,0));users[(j,0)].add(heavy)
  for light in lights:
   side=0 if pos[light]<pos[heavy] else 1
   if orientation==-1:side=1-side
   initial[light].add((j,side));users[(j,side)].add(light)
 strategies={p:[set(initial[p]),{(j,1-side) for j,side in initial[p]}] for p in players}
 assert all(not s[0]&s[1] for s in strategies.values())
 state={p:0 for p in players}; first={};second={};load_pairs={p:[] for p in players}
 def resource_load(e):
  return sum((weights[p[1]] for p in players if e in strategies[p][state[p]]),F())
 for sweep in range(2):
  for p in players:
   old=strategies[p][state[p]];new=strategies[p][1-state[p]]
   old_loads=sorted(resource_load(e) for e in old)
   oldcost=sum((x**d for x in old_loads),F())
   state[p]=1-state[p]
   new_loads=sorted(resource_load(e) for e in new)
   newcost=sum((x**d for x in new_loads),F())
   (first if sweep==0 else second)[p]=(oldcost,newcost)
   if sweep==0:load_pairs[p]=(old_loads,new_loads)
 assert first==second
 assert not any(state.values())
 wh,wl=weights[a],weights[b]
 heavy_expected=(wh**d,(wh+K*wl)**d)
 light_expected=(sum(((wh+r*wl)**d for r in range(1,K+1)),F()),sum(((r*wl)**d for r in range(1,K+1)),F()))
 if orientation==-1:heavy_expected=heavy_expected[::-1];light_expected=light_expected[::-1]
 for p in players:
  wanted=heavy_expected if p[1]==a else light_expected if p[1]==b else (F(),F())
  assert first[p]==wanted,(weights,N,a,b,K,d,orientation,p,first[p],wanted,load_pairs[p])
  if p[1]==b:
   wanted_loads=(sorted(wh+r*wl for r in range(1,K+1)),sorted(r*wl for r in range(1,K+1)))
   if orientation==-1:wanted_loads=wanted_loads[::-1]
   assert load_pairs[p]==wanted_loads
 return {'N':N,'classes':len(weights),'a':a,'b':b,'K':K,'degree':d,'orientation':orientation,'heavy':[str(x) for x in heavy_expected],'light':[str(x) for x in light_expected]}

if __name__=='__main__':
 cases=[]
 for N in range(1,7):
  for K in range(1,N+1):
   for a,b in itertools.permutations(range(3),2):
    for d in [0,1,2,5]:
     for orientation in [-1,1]:
      cases.append(audit([F(1),F(1,3),F(2,17)],N,a,b,K,d,orientation))
 print(json.dumps({'status':'all exact assertions passed','cases':len(cases),'selected':cases[-4:]},ensure_ascii=False,indent=2))
