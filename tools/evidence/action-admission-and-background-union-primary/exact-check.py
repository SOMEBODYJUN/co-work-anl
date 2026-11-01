from fractions import Fraction as F
from itertools import product
import json

def serial(v):
 if isinstance(v,F):return str(v)
 if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
 if isinstance(v,(list,tuple)):return [serial(x) for x in v]
 return v

def greedy(actions,u,e):
 n=len(actions); t=[F(1) if M==0 else F(0) for M,A,D in actions]
 f=[u*A/D if M else F(0) for M,A,D in actions]
 v=[M*D/A if M else F(0) for M,A,D in actions]
 for j in sorted(range(n),key=lambda i:(-v[i],i)):
  if f[j]: t[j]=min(F(1),e/f[j]); e-=t[j]*f[j]
 return t,f,v

def vertex_opt(actions,u,e):
 n=len(actions); f=[u*A/D if M else F(0) for M,A,D in actions]
 best=F(0); count=0
 # Include all feasible box vertices, even when the budget is slack.
 for t in product([F(0),F(1)],repeat=n):
  if sum((t[j]*f[j] for j in range(n)),F(0))<=e:
   best=max(best,sum((t[j]*actions[j][0] for j in range(n)),F(0)));count+=1
 # A clipped-box vertex on the one budget facet has <=1 non-box coordinate.
 for j in range(n):
  if not f[j]:continue
  others=[i for i in range(n) if i!=j]
  for bits in product([F(0),F(1)],repeat=len(others)):
   t=[F(0)]*n
   for i,b in zip(others,bits):t[i]=b
   t[j]=(e-sum((t[i]*f[i] for i in others),F(0)))/f[j]
   if 0<=t[j]<=1:
    best=max(best,sum((t[i]*actions[i][0] for i in range(n)),F(0)));count+=1
 return best,count

def units(types):
 return [frozenset(labels) for labels,n in types for _ in range(n)]
def topic(U,a):return {i for i,x in enumerate(U) if a in x}
def union(U,t):return set().union(*(topic(U,a) for a in t)) if t else set()
def payoff(U,z,i):return sum((F(1,sum(a in x for a in z)) for x in U if z[i] in x),F(0))
def background(U,old,tail):
 b=[sum(a in x for a in old) for x in U];c=[sum(a in x for a in tail) for x in U]
 H={i for i,v in enumerate(b) if v};new={i for i in range(len(U)) if not b[i] and c[i]}
 B=sum((F(b[i],b[i]+c[i]) for i in H),F(0))
 V=sum((F(c[i],b[i]+c[i]) for i in range(len(U)) if c[i]),F(0))
 assert B+V==len(H)+len(new)
 return H,new,B,V

def main():
 cases=[
  (F(4),[(F(3),F(1),F(2)),(F(2),F(1),F(3)),(F(5),F(2),F(4))]),
  (F(3),[(F(2),F(1),F(2)),(F(3),F(3,2),F(2)),(F(1),F(1,2),F(1)),(F(0),F(0),F(0))]),
  (F(1),[(F(2),F(1),F(1)),(F(1),F(1),F(1))]),
  (F(0),[(F(0),F(0),F(0))]),
 ]
 local=[];vertices=0
 for k,(u,actions) in enumerate(cases):
  for M,A,D in actions:
   assert (M==A==0) or (M>0 and A>0 and 0<D<=u)
  total=sum((u*A/D if M else F(0) for M,A,D in actions),F(0))
  budgets=sorted(set([F(0),total,total+1]+[total*F(j,8) for j in range(9)]))
  for e in budgets:
   t,f,v=greedy(actions,u,e);accepted=sum((t[j]*actions[j][0] for j in range(len(t))),F(0))
   best,ct=vertex_opt(actions,u,e);vertices+=ct;assert accepted==best
   used=sum((t[j]*f[j] for j in range(len(t))),F(0));assert used<=e
   if e<total:assert used==e
   lam=[(1-t[j])*actions[j][1]/actions[j][2] if actions[j][0] else F(0) for j in range(len(t))]
   stop=sum(((1-t[j])*actions[j][0] for j in range(len(t))),F(0))
   assert stop==sum((lam[j]*v[j] for j in range(len(t))),F(0))
   rejected=[v[j] for j in range(len(t)) if actions[j][0] and t[j]<1]
   accept=[v[j] for j in range(len(t)) if actions[j][0] and t[j]>0]
   tau=max(rejected) if rejected else (min(accept) if accept else F(0))
   assert all(x<=tau for x in rejected) and all(x>=tau for x in accept)
   assert stop<=tau*sum(lam,F(0))
   if stop:
    L=sum(lam,F(0));assert L>0
    mass=[(1-t[j])*actions[j][0]/stop for j in range(len(t))]
    fin=[l/L for l in lam]
    assert sum(mass,F(0))==sum(fin,F(0))==1
    assert all(mass[j]==lam[j]*v[j]/stop for j in range(len(t)))
   local.append(dict(case=k,budget=e,theta=t,accepted=accepted,vertex_opt=best,stop=stop,tau=tau,vertices=ct))
 U52=units([([j for j in range(6) if mask>>j&1],n) for mask,n in [(1,10),(2,12),(4,5),(8,5),(20,2),(24,2),(36,2),(40,2),(49,6),(50,6)]])
 H,N,B,V=background(U52,(0,1),(0,1)); O=union(U52,(2,3));allpairs=[len(union(U52,t)) for t in product(range(6),repeat=2)]
 actual=(0,1,0,1);pay=[payoff(U52,actual,i) for i in range(4)]
 assert len(U52)==52 and len(H)==34 and len(N)==0 and B==V==17
 assert len(O)==18 and not(H&O) and len(H|O)==52 and B+2*V==51
 assert max(allpairs)==34 and max(allpairs)<=B+2*V
 assert pay==[8,9,8,9] and len(union(U52,actual))==34 and len(union(U52,(0,1,2,3)))==52
 bg52=dict(clients=52,actual=actual,actual_payoffs=pay,H=len(H),new=len(N),B=B,V=V,comparison_TQ=len(O),union_comparison=len(H|O),budget=B+2*V,union_violation=len(H|O)-B-2*V,bare_all_ordered_pairs=36,bare_max=max(allpairs),root_W=34,root_OPT=52,root_half_slack=16,credibility='existing-full-canonical-proof;not-rerun259nodes')
 U61=units([([ord(a)-ord('A') for a in s],n) for s,n in [('A',12),('B',8),('C',4),('D',8),('AE',6),('AF',6),('CE',3),('CF',3),('AEF',6),('BEF',2),('CEF',1),('DEF',2)]])
 Ts=[topic(U61,a) for a in range(4)];private=[len(Ts[j]-set().union(*(Ts[k] for k in range(4) if k!=j))) for j in range(4)]
 p61=[payoff(U61,(0,0,0,5),i) for i in range(4)]
 assert len(union(U61,(0,1,2,3)))==len(U61)==61 and private==[30,10,11,10] and p61==[9,9,9,11]
 assert min(private)-p61[0]==1
 U11=units([([0],2),([1],2),([2],1),([2,3],1),([2,4],1),([0,3,4],3),([1,3,4],1)])
 H11,N11,B11,V11=background(U11,(0,),(0,1));O11=union(U11,(1,2));S11=topic(U11,0)
 q=[]
 for a,other in [(1,2),(2,1)]:
  q.append(len(topic(U11,a)-(H11|S11|topic(U11,other)))-len(S11-(H11|O11)))
 p11=[payoff(U11,(0,0,1),i) for i in range(3)]
 assert q==[3,3] and p11==[F(5,2),F(5,2),3] and min(q)-p11[1]==F(1,2)
 assert B11==F(5,2) and V11==F(11,2) and len(H11|O11)==11<=B11+2*V11
 return dict(status='PASS',arithmetic='standard-library-Fraction;expanded-distinct-unit-customers',new_definition_check_runs=1,original_program_entries=0,old_full_strategy_replays=0,local_cases=len(cases),local_budget_instances=len(local),feasible_vertex_instances=vertices,local_checks=local,background52=bg52,private61=dict(private=private,payoffs=p61,strict_gap=1,credibility='existing-full-canonical-proof;actualpath-arithmetic-only'),local11=dict(q=q,payoffs=p11,B=B11,V=V11,budget=B11+2*V11,union_comparison=11,strict_local_gap=F(1,2),credibility='existing31node-proof;actualpath-arithmetic-only'),scope='abstractlocalrowsnotclaimedSPE;threeexistingcertificatepatharithmeticonly;nogeneralfinite-searchinference')

if __name__=='__main__':
 print(json.dumps(serial(main()),ensure_ascii=False,indent=2))
