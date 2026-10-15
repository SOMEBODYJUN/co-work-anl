"""Literal Fraction replay of the anchored polynomial compiler on the repository
integer quadratic triad. Action zero is relabeled from original profile 010.
Standard library only; no LP, float, randomness, network, or evidence mutation.
"""
from fractions import Fraction as F
from itertools import product,combinations
from hashlib import sha256
import json

WEIGHTS=[F(16),F(2),F(5)]
ALPHA=F(21,20)
INITIAL=(0,1,0)
PAIRS=[((0,1,1),2,F(13)),((1,1,2),1,F(59)),((1,2,1),2,F(2))]

def costs(s,resources):
 result=[F() for _ in WEIGHTS]
 for degree,coefficient,actions in resources:
  users=[i for i,a in enumerate(actions) if a==s[i]]
  load=sum((WEIGHTS[i] for i in users),F())
  fee=coefficient*load**degree
  for i in users:result[i]+=fee
 return result

def flip(s,i):
 t=list(s);t[i]=1-t[i];return tuple(t)

def valid(s):return sum(s[i]!=s[i+1] for i in range(len(s)-1))<=1

def essential_audit():
 results=[]
 for n in range(3,10):
  triples=[(0,i,j) for i,j in combinations(range(1,n),2)]
  count=0
  for s in product((0,1),repeat=n):
   full=lambda t,ss:ss[t[0]]==ss[t[2]]!=ss[t[1]]
   if valid(s):assert not any(full(t,s) for t in triples);continue
   i=next(i for i in range(1,n) if s[i]!=s[0]);after=flip(s,i)
   incident=[t for t in triples if i in t]
   assert any(full(t,s) for t in incident)
   assert not any(full(t,after) for t in incident)
   count+=1
  results.append({'players':n,'states':2**n,'illegal_states_checked':count})
 return results

def main():
 n=len(WEIGHTS);base=[]
 for mask,degree,coefficient in PAIRS:
  for side in (0,1):
   actions=tuple(-1 if m==0 else (m-1)^side^INITIAL[i] for i,m in enumerate(mask))
   base.append((degree,coefficient,actions))
 cycle=[(0,0,0)]
 for step in range(2*n):cycle.append(flip(cycle[-1],step%n))
 states=list(product((0,1),repeat=n));B=max(c for s in states for c in costs(s,base))
 margins=[costs(s,base)[step%n]-ALPHA*costs(cycle[step+1],base)[step%n] for step,s in enumerate(cycle[:-1])]
 ratios=[costs(s,base)[step%n]/costs(cycle[step+1],base)[step%n] for step,s in enumerate(cycle[:-1])]
 eta=min(margins);assert eta>0 and eta<=B
 triples=[(0,i,j) for i,j in combinations(range(1,n),2)];L=len(triples)
 total={t:sum((WEIGHTS[i] for i in t),F()) for t in triples}
 delta=max(1-min(WEIGHTS[i] for i in t)/total[t] for t in triples)
 M=2*ALPHA*B;epsilon=eta/(4*ALPHA**2*B*L);D=1
 while delta**D>epsilon:D+=1
 assert delta**D<=epsilon and delta**(D-1)>epsilon
 clock=[]
 for triple in triples:
  for side in (0,1):
   actions=[-1]*n
   for i,target in zip(triple,(0,1,0)):actions[i]=side^target
   clock.append((D,M/total[triple]**D,tuple(actions)))
 combined=base+clock;records=[]
 for step,s in enumerate(cycle[:-1]):
  i=step%n;t=cycle[step+1]
  assert costs(t,clock)[i]<=L*M*delta**D
  assert costs(s,combined)[i]-ALPHA*costs(t,combined)[i]>=eta/2
 for s in states:
  if valid(s):i=cycle[:-1].index(s)%n
  else:
   i=next(i for i in range(1,n) if s[i]!=s[0]);t=flip(s,i)
   assert costs(s,clock)[i]>=M
   assert costs(t,clock)[i]<=L*M*delta**D
   assert ALPHA*costs(t,combined)[i]<=3*M/4
  t=flip(s,i);old=costs(s,combined)[i];new=costs(t,combined)[i]
  assert old>ALPHA*new
  records.append([list(s),i,str(old),str(new)])
 out={'status':'all exact Fraction assertions passed','fixture':'Repository integer quadratic triad; initial original profile 010 relabeled to 000','weights':[str(w) for w in WEIGHTS],'alpha':str(ALPHA),'base_resource_pairs':[{'mask':m,'degree':d,'coefficient':str(c)} for m,d,c in PAIRS],'original_cycle':[''.join(str(a^b) for a,b in zip(s,INITIAL)) for s in cycle],'cycle_ratios':[str(r) for r in ratios],'cycle_margins':[str(x) for x in margins],'B':str(B),'eta':str(eta),'delta':str(delta),'M':str(M),'epsilon':str(epsilon),'clock_degree':D,'final_degree':max(2,D),'base_resources':len(base),'clock_resources':len(clock),'all_profiles_checked':len(states),'all_cycle_moves_checked':2*n,'illegal_profiles_checked':sum(not valid(s) for s in states),'literal_witness_costs_sha256':sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest(),'essential_clock_full_state_audit':essential_audit(),'scope':'Exact finite compiler replay only. Degree depends on the input instance; does not settle WC-TARGET.'}
 print(json.dumps(out,indent=2))

if __name__=='__main__':main()
