"""Exact finite cycle certificate for the cyclic-window lift; no LP dependency.
Fixed model: polynomial degree 16, rational resource coefficients, 400 players.
All actual move costs use maintained actual loads, independently of the
compressed class formula. This does not certify nonexistence of equilibria.
"""
from fractions import Fraction as F
from hashlib import sha256
import json

D=16; ALPHA=F(2); M=4; N=100
WEIGHTS=[F(1,10**a) for a in range(M)]
# a, b, K, orientation, coefficient of the max-normalized cost column
TESTS=[(0,1,3,-1,F(33958,10**6)),(0,3,100,1,F(578345,10**6)),(1,2,3,-1,F(100896,10**6)),(2,3,3,-1,F(286801,10**6))]

def main():
 players=[(j,a) for j in range(N) for a in range(M)]
 pos={p:k for k,p in enumerate(players)}
 strategies={p:[set(),set()] for p in players}
 coefficients={};class_old=[F() for _ in range(M)];class_new=[F() for _ in range(M)];test_records=[]
 for ti,(a,b,K,orientation,normalized_coefficient) in enumerate(TESTS):
  wa,wb=WEIGHTS[a],WEIGHTS[b]
  P={a:wa**D,b:sum(((wa+r*wb)**D for r in range(1,K+1)),F())}
  Q={a:(wa+K*wb)**D,b:sum(((r*wb)**D for r in range(1,K+1)),F())}
  if orientation<0:P,Q=Q,P
  scale=max(*P.values(),*Q.values());coefficient=normalized_coefficient/scale
  for c in range(M):class_old[c]+=coefficient*P.get(c,F());class_new[c]+=coefficient*Q.get(c,F())
  for j in range(N):
   for side in (0,1):coefficients[(ti,j,side)]=coefficient
   h=(j,a);strategies[h][0].add((ti,j,0));strategies[h][1].add((ti,j,1))
   delta=int(a>b)
   for k in range(K):
    light=((j+delta+k)%N,b)
    side=0 if pos[light]<pos[h] else 1
    if orientation<0:side=1-side
    strategies[light][0].add((ti,j,side));strategies[light][1].add((ti,j,1-side))
  test_records.append({'heavy_class':a,'light_class':b,'window':K,'orientation':orientation,'resource_coefficient':str(coefficient),'normalized_coefficient':str(normalized_coefficient)})
 assert all(not st[0]&st[1] for st in strategies.values())
 loads={e:F() for e in coefficients}
 for p in players:
  for e in strategies[p][0]:loads[e]+=WEIGHTS[p[1]]
 initial_loads=dict(loads);state={p:0 for p in players};cost_pairs=[]
 for sweep in range(2):
  for p in players:
   w=WEIGHTS[p[1]];old=strategies[p][state[p]];new=strategies[p][1-state[p]]
   old_cost=sum((coefficients[e]*loads[e]**D for e in old),F())
   for e in old:loads[e]-=w
   for e in new:loads[e]+=w
   new_cost=sum((coefficients[e]*loads[e]**D for e in new),F())
   assert old_cost>ALPHA*new_cost,(sweep,p,old_cost,new_cost)
   assert (old_cost,new_cost)==(class_old[p[1]],class_new[p[1]])
   state[p]=1-state[p];cost_pairs.append([sweep,p[0],p[1],str(old_cost),str(new_cost)])
 assert not any(state.values()) and loads==initial_loads
 out={'status':'all exact assertions passed','degree':D,'alpha':str(ALPHA),'players':len(players),'resources':len(coefficients),'moves':len(cost_pairs),'class_weights':[str(x) for x in WEIGHTS],'tests':test_records,'class_margins':[str(x-ALPHA*y) for x,y in zip(class_old,class_new)],'class_cost_ratios':[str(x/y) for x,y in zip(class_old,class_new)],'trajectory_costs_sha256':sha256(json.dumps(cost_pairs,separators=(',',':')).encode()).hexdigest(),'scope':'A literal strict alpha-improvement cycle only; adding legal empty strategies gives an exact all-empty PNE.'}
 print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
