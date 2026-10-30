#!/usr/bin/env python3
"""Independent literal two-action resource audit; no compressed costs imported."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

M,N,p=3,4,8
alpha=F(21,20)
weights=(F(1),F(1,4),F(1,16))
tests=((0,1,1,-1),(1,2,1,-1),(2,0,4,-1))
coeffs=(F(311296,9765625),F(4294967296,1171875),F(38386270208,6624208646923275))
P=M*N
# Player j*M+a; resource (test,heavy index,side) encoded as integer.
strategies=[[set(),set()] for _ in range(P)]
resource_coeff=[]
for t,(a,b,K,orientation) in enumerate(tests):
    resource_coeff.extend([coeffs[t]]*(2*N))
    delta=int(a>b)
    for j in range(N):
        h=j*M+a
        pair=2*N*t+2*j
        strategies[h][0].add(pair)
        strategies[h][1].add(pair+1)
        for k in range(K):
            i=(j+delta+k)%N
            u=i*M+b
            zero_side=int(u>h)^int(orientation==-1)
            strategies[u][0].add(pair+zero_side)
            strategies[u][1].add(pair+1-zero_side)
R=len(resource_coeff)
assert all(s[0].isdisjoint(s[1]) for s in strategies)
@lru_cache(None)
def costs(state):
    loads=[F(0)]*R
    for i in range(P):
        for e in strategies[i][state[i]]:
            loads[e]+=weights[i%M]
    resource_cost=[c*x**p for c,x in zip(resource_coeff,loads)]
    return tuple(sum((resource_cost[e] for e in strategies[i][state[i]]),F(0)) for i in range(P))
def flip(state,i):
    s=list(state);s[i]^=1;return tuple(s)
def margin(state,i):
    return costs(state)[i]-alpha*costs(flip(state,i))[i]
def front(phases):
    return tuple(int((phases[a]-j-1)%(2*N)<N) for j in range(N) for a in range(M))
def twist(state):
    s=[None]*P
    for j in range(N):
        for a in range(M):
            s[((j+1)%N)*M+a]=state[j*M+a]^int(j==N-1)
    return tuple(s)
def frac(q):return str(q)
def min_margin(states):
    vals=[(margin(s,i),k,i) for k,s in enumerate(states) for i in range(P)]
    return min(vals)
# Literal 24-step same-order cycle.
s=(0,)*P
cycle=[]
for step in range(2*P):
    i=step%P
    cycle.append({'step':step,'player':(i%M,i//M),'old':frac(costs(s)[i]),'new':frac(costs(flip(s,i))[i]),'margin':frac(margin(s,i))})
    assert margin(s,i)>0,(step,i,margin(s,i))
    s=flip(s,i)
assert s==(0,)*P
# Every phase front is transported exactly and every full state has cost/gain covariance.
for code in range(1<<P):
    s=tuple((code>>i)&1 for i in range(P))
    ts=twist(s)
    for i in range(P):
        ti=(((i//M)+1)%N)*M+i%M
        assert costs(s)[i]==costs(ts)[ti]
        assert margin(s,i)==margin(ts,ti)
for x in range(2*N):
 for y in range(2*N):
  for z in range(2*N):
    phases=(x,y,z)
    s=front(phases)
    assert twist(s)==front(tuple((u+1)%(2*N) for u in phases))
    neighbors={flip(s,i) for i in range(P)}
    true_front_neighbors={front(tuple((u+d)%(2*N) if a==b else u for b,u in enumerate(phases))) for a in range(M) for d in (-1,1)}
    assert neighbors.intersection({front((xx,yy,zz)) for xx in range(2*N) for yy in range(2*N) for zz in range(2*N)})==true_front_neighbors
s=front((0,4,0))
front_moves=[]
for a in range(M):
 for direction in (-1,1):
    x=(0,4,0)[a]
    j=(x-1)%N if direction==-1 else x%N
    i=j*M+a
    front_moves.append({'class':a,'direction':direction,'clone':j,'old':frac(costs(s)[i]),'new':frac(costs(flip(s,i))[i]),'margin':frac(margin(s,i)),'margin_float':float(margin(s,i))})
    assert margin(s,i)<0
all_moves=[]
for i in range(P):
    all_moves.append({'class':i%M,'clone':i//M,'margin':frac(margin(s,i)),'margin_float':float(margin(s,i)),'improves':margin(s,i)>0})
assert any(v['improves'] for v in all_moves)
# Separately reconstruct P,Q only as a consistency check of given normalization.
normalizations=[]
for (a,b,K,_),z in zip(tests,coeffs):
    Pa=weights[a]**p
    Qa=(weights[a]+K*weights[b])**p
    Pb=sum(((weights[a]+r*weights[b])**p for r in range(1,K+1)),F(0))
    Qb=sum(((r*weights[b])**p for r in range(1,K+1)),F(0))
    normalizations.append(frac(z*max(Pa,Qa,Pb,Qb)))
result={'construction':'independent literal resources; no imported compressed cost formula','M':M,'N':N,'p':p,'alpha':frac(alpha),'resources':R,'cycle_steps':len(cycle),'cycle_all_strict':True,'all_4096_states_cost_gain_covariance':True,'all_512_front_phase_transport_and_neighbors':True,'normalized_coefficients':normalizations,'target_phase':[0,4,0],'target_front_moves':front_moves,'target_all_moves':all_moves,'cycle':cycle}
stable=[]
for phases in product(range(8),repeat=3):
 s=front(phases)
 margins=[]
 for a in range(3):
  for d in (-1,1):
   j=(phases[a]-1)%4 if d<0 else phases[a]%4
   margins.append(margin(s,3*j+a))
 if max(margins)<=0:stable.append(phases)
expected=[(t,(4+t)%8,t) for t in range(8)]
assert stable==expected
# Literal clock: transformed side = action xor (0,1,0).
clock_cases=[]
for state in product((0,1),repeat=3):
 sides=tuple(state[i]^(i==1) for i in range(3))
 if len(set(sides))==1:continue
 for mover in range(3):
  nxt=list(state);nxt[mover]^=1
  new_sides=tuple(nxt[i]^(i==1) for i in range(3))
  if len(set(new_sides))==1:continue
  old_load=sum(F(3,7) for side in sides if side==sides[mover])
  new_load=sum(F(3,7) for side in new_sides if side==new_sides[mover])
  assert old_load==new_load==F(6,7)
  clock_cases.append([state,mover,tuple(nxt)])
# Non-ordered raw wrap triple shows why nontrigger endpoint condition matters.
state=(1,0,0);nxt=(1,1,0);triple=(2,0,1)
before=tuple(state[i] for i in triple);after=tuple(nxt[i] for i in triple)
assert before==(0,1,0) and after==(0,1,1)
result['front_stable_states_by_literal_costs']=stable
result['clock_nontrigger_edges_checked']=len(clock_cases)
result['clock_equal_load']='6/7 for w=3/7'
result['scope']='Finite literal example and boundary checks only; not all-front existence or general compiler impossibility.'
print(json.dumps(result,ensure_ascii=False,indent=2))
