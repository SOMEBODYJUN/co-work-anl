"""Exact audit of cyclic-clone class-front boundary tables.
Internal scratch: no repo or external writes. Fractions only, no LP.
"""
from fractions import Fraction as F
from itertools import permutations,product
import json,hashlib,platform
from pathlib import Path


def bit(N,phase,j):
 phase%=2*N
 return int(j<phase) if phase<N else int(j>=phase-N)


def sigs(m,N,a,b,K,o):
 ans=[];delta=int(a>b)
 for j in range(N):
  h=j*m+a;sig={h:0}
  for k in range(K):
   u=((j+delta+k)%N)*m+b
   side=int(u>h)
   if o<0:side=1-side
   sig[u]=side
  ans.append(sig)
 return ans


def literal(weights,N,p,test,phases,player):
 m=len(weights);a,b,K,o=test;old=new=F()
 st=[bit(N,phases[c],j) for j in range(N) for c in range(m)]
 for sg in sigs(m,N,*test):
  if player not in sg:continue
  ss=sg[player]^st[player];ls=[F(),F()]
  for u,side in sg.items():ls[side^st[u]]+=weights[u%m]
  old+=ls[ss]**p
  new+=(ls[1-ss]+weights[player%m])**p
 return old,new


def endpoint(weights,N,p,test,c,r):
 a,b,K,o=test;wa,wb=weights[a],weights[b];delta=int(a>b)
 if c==a:
  n0=0
  for k in range(K):
   v=(delta+k)%N;side=int((v,b)>(0,a))
   if o<0:side=1-side
   n0+=int((side^bit(N,r,v))==0)
  return (wa+n0*wb)**p,(wa+(K-n0)*wb)**p
 if c==b:
  old=new=F()
  for k in range(K):
   h=(-delta-k)%N;side=int((0,b)>(h,a))
   if o<0:side=1-side
   e=int(bit(N,r,h)==side)
   old+=((K-k)*wb+wa*e)**p
   new+=((k+1)*wb+wa*(1-e))**p
  return old,new
 return F(),F()


def cycle_costs(weights,p,test):
 a,b,K,o=test;m=len(weights);wa,wb=weights[a],weights[b]
 P=[F() for _ in weights];Q=P.copy()
 P[a]=wa**p;Q[a]=(wa+K*wb)**p
 P[b]=sum(((wa+r*wb)**p for r in range(1,K+1)),F())
 Q[b]=sum(((r*wb)**p for r in range(1,K+1)),F())
 return (P,Q) if o>0 else (Q,P)


def audit_formulas():
 count=0
 # All ordered class roles, every window, both orientations, all relative phases;
 # also translated endpoints and reversed endpoint using r+1 old/new swap.
 for N in range(1,7):
  w=[F(1),F(2,5),F(1,7)];m=len(w)
  for a,b in permutations(range(m),2):
   for K in range(1,N+1):
    for o in [1,-1]:
     test=(a,b,K,o)
     for p in [0,1,2,5]:
      for c in [a,b]:
       other=b if c==a else a
       for r in range(2*N):
        fwd=endpoint(w,N,p,test,c,r)
        phases=[0]*m;phases[other]=r
        assert literal(w,N,p,test,phases,c)==fwd
        count+=1
        for x in [0,1,N,2*N-1]:
         phases=[0]*m;phases[c]=x;phases[other]=(x+r)%(2*N)
         assert literal(w,N,p,test,phases,(x%N)*m+c)==fwd
         back=endpoint(w,N,p,test,c,r+1)[::-1]
         assert literal(w,N,p,test,phases,((x-1)%N)*m+c)==back
         count+=2
 return count


def exact_example():
 w=[F(1),F(1,4),F(1,16)];N=4;p=8;alpha=F(21,20);m=3
 tests=[(0,1,1,-1),(1,2,1,-1),(2,0,4,-1)]
 z=[F(19,100),F(1,3),F(143,300)]
 scales=[];coeff=[];gamma=[F() for _ in w]
 for t,v in zip(tests,z):
  P,Q=cycle_costs(w,p,t);scale=max(P+Q);scales.append(scale);coeff.append(v/scale)
  for c in range(m):gamma[c]+=v/scale*(P[c]-alpha*Q[c])
 assert min(gamma)>F(3,40)
 # Verify all 2mN literal sweep edges, not only compressed class formulas.
 phases=[0]*m
 sweep=[]
 for _ in range(2):
  for j in range(N):
   for c in range(m):
    old=new=F()
    for t,co in zip(tests,coeff):
     u,v=literal(w,N,p,t,phases,j*m+c);old+=co*u;new+=co*v
    assert old-alpha*new==gamma[c]
    sweep.append(old-alpha*new);phases[c]=(phases[c]+1)%(2*N)
 assert phases==[0]*m
 # Freeze a stable vertex of the compressed class-front graph.
 ph=(0,N,0);allmargins=[];front=[]
 for j in range(N):
  for c in range(m):
   old=new=F()
   for t,co in zip(tests,coeff):
    u,v=literal(w,N,p,t,ph,j*m+c);old+=co*u;new+=co*v
   allmargins.append(old-alpha*new)
 for c in range(m):
  front.append([allmargins[(ph[c]%N)*m+c],allmargins[((ph[c]-1)%N)*m+c]])
 assert max(x for row in front for x in row)<-F(9,50)
 assert min(allmargins[3],allmargins[6])>F(1,5)
 # Exhaust all front vertices through endpoint formula; witness itself remains literal.
 stable=[];worst=None
 for phase in product(range(2*N),repeat=m):
  mg=[]
  for c in range(m):
   fo=fn=bo=bn=F()
   for t,co in zip(tests,coeff):
    if c not in t[:2]:continue
    other=t[1] if c==t[0] else t[0];r=phase[other]-phase[c]
    u,v=endpoint(w,N,p,t,c,r);fo+=co*u;fn+=co*v
    u,v=endpoint(w,N,p,t,c,r+1);bo+=co*v;bn+=co*u
   mg.extend([fo-alpha*fn,bo-alpha*bn])
  mx=max(mg)
  if mx<=0:stable.append(phase)
  if worst is None or mx<worst[0]:worst=(mx,phase)
 return {'weights':list(map(str,w)),'clones_per_class':N,'degree':p,'alpha':str(alpha),'tests':[list(t) for t in tests],'max_normalized_coefficients':list(map(str,z)),'resource_coefficients':list(map(str,coeff)),'class_cycle_margins':list(map(str,gamma)),'literal_sweep_edges':len(sweep),'frozen_front_phase':ph,'frozen_front_margins':[[str(v) for v in row] for row in front],'frozen_all_player_margins':list(map(str,allmargins)),'front_state_count':(2*N)**m,'front_stable_count':len(stable),'front_stable_phases':stable,'minimum_over_front_states_of_max_endpoint_margin':str(worst[0]),'minimizing_phase':worst[1],'scope':'Exact counterexample only to the claim that every product-of-class-front state of every strict cyclic-clone base has an improving class-front endpoint. It is not an alpha-PNE: interior clones improve. It does not prove impossibility of all within-class clocks.'}

if __name__=='__main__':
 out={'status':'all exact assertions passed','formula_audit_checks':audit_formulas(),'example':exact_example(),'python':platform.python_version(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 print(json.dumps(out,ensure_ascii=False,indent=2))
