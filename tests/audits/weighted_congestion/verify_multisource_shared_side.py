from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import hashlib,json,platform,sys
from itertools import product
from random import Random
rng=Random(9137)
counts={'reset':0,'source':0,'games':0,'states':0,'deviations':0,'UF_checks':0}
coverage={k:False for k in ('nonunit_u','zero_side','constant_side','empty_H','empty_L','source_in_H','source_without_light','empty_lights','d2_alpha4')}
def alpha_for(d):
 r=isqrt(d);return Q(1+r+(r*r<d))
def poly(a,x):return sum((c*x**k for k,c in enumerate(a)),Q(0))
def kap(d,t):return min(d*t,t+1)
def rosen(a,x,n):return sum((poly(a,x+r) for r in range(1,n+1)),Q(0))
for d in range(2,31):
 alpha=alpha_for(d)
 assert (alpha-1)**2>=d
 for _ in range(120):
  n=rng.randrange(0,9)
  ts=[Q(rng.randrange(1,21),rng.randrange(1,41)) for _ in range(n)]
  T=sum(ts);a=[Q(rng.randrange(0,4)) for _ in range(d+1)]
  S=sum(kap(d,t)*(poly(a,1+t)-alpha*poly(a,T)) for t in ts)
  M=alpha*poly(a,1+T)-poly(a,1)
  assert S<=(alpha-1)*M,(d,alpha,ts,a,S,M)
  counts['source']+=1
  n=rng.randrange(0,9);T=Q(rng.randrange(1,40),rng.randrange(1,40));w=T*Q(rng.randrange(1,10),10);s=(T-w)*Q(rng.randrange(0,11),10)
  z=rosen(a,s+w,n)-rosen(a,s,n)
  assert z<=kap(d,w)*poly(a,T+n),(d,T,w,s,n,z)
  counts['reset']+=1
# Random actual multi-source games, UF constructed with uniform main monomial
for d in (2,3,4,5,8,9):
 alpha=Q(4) if d==2 else alpha_for(d)
 assert (alpha-1)**2>=d
 for sample in range(13):
  u=(Q(1),Q(2,3),Q(3,2))[sample%3]
  nh=3;nl=0 if sample==12 else 5;orig=[rng.randrange(2) for _ in range(nl)];weights=[Q(rng.randrange(1,6),30) for _ in range(nl)]
  coverage["nonunit_u"]|=u!=1
  coverage["empty_lights"]|=nl==0
  coverage["source_without_light"]|=not any(v==2 for v in orig)
  coverage["d2_alpha4"]|=d==2 and alpha==4
  W=[sum((weights[l] for l in range(nl) if orig[l]==v),Q(0)) for v in range(nh)]
  # shrink light weights so F(1+w)-alpha F(W)>0 at degree d.
  weights=[u*w/(1+max(W))*Q(1,4) for w in weights]
  W=[sum((weights[l] for l in range(nl) if orig[l]==v),Q(0)) for v in range(nh)]
  side=[]
  for j in range(4):
   H={v for v in range(nh) if rng.randrange(2)};L={l for l in range(nl) if rng.randrange(2)}
   a=([Q(0)]*(d+1) if j==0 else [Q(2)]+[Q(0)]*d if j==1 else [Q(0)]*d+[Q(rng.randrange(1,4))]);side.append((H,L,a))
  side.extend([(set(),set(range(nl)),[Q(0)]*d+[Q(1)]),(set(range(nh)),set(),[Q(1)]),(set(range(nh)),set(range(nl)),[Q(0)]*d+[Q(1)])])
  for H,L,a in side:
   coverage["zero_side"]|=all(c==0 for c in a)
   coverage["constant_side"]|=a[0]>0 and all(c==0 for c in a[1:])
   coverage["empty_H"]|=not H;coverage["empty_L"]|=not L
   coverage["source_in_H"]|=any(orig[l] in H for l in L)
  main=[]
  for v in range(nh):
   need=Q(1)
   for l in range(nl):
    if orig[l]!=v:continue
    sideP=sum((alpha*poly(a,sum((weights[k] for k in L),Q(0))+len(H)*u)-poly(a,weights[l]) for H,L,a in side if l in L),Q(0))
    denom=(u+weights[l])**d-alpha*W[v]**d
    assert denom>0
    need=max(need,sideP/denom)
   main.append([Q(0)]*d+[need])
  def energy(h):
   e=Q(0)
   for H,L,a in side:
    for b in (0,1):
     n=sum(h[v]==b for v in H);x=sum((weights[l] for l in L if h[orig[l]]==b),Q(0))
     e+=sum((poly(a,x+r*u) for r in range(1,n+1)),Q(0))
   return e
  def costs(bits):
   hub=bits[:nh];li=bits[nh:];cost=[]
   for v in range(nh):
    x=u+sum((weights[l] for l in range(nl) if orig[l]==v and li[l]==hub[v]),Q(0))
    c=poly(main[v],x)
    for H,L,a in side:
     if v in H:
      x=sum((u for k in H if hub[k]==hub[v]),Q(0))+sum((weights[l] for l in L if 1-li[l]==hub[v]),Q(0))
      c+=poly(a,x)
    cost.append(c)
   for l in range(nl):
    v=orig[l];x=sum((weights[k] for k in range(nl) if orig[k]==v and li[k]==li[l]),Q(0))+(u if hub[v]==li[l] else Q(0))
    c=poly(main[v],x)
    for H,L,a in side:
     if l in L:
      x=sum((u for k in H if hub[k]==1-li[l]),Q(0))+sum((weights[k] for k in L if li[k]==li[l]),Q(0))
      c+=poly(a,x)
    cost.append(c)
   return cost
  for l in range(nl):
   v=orig[l]
   left=poly(main[v],u+weights[l])+sum((poly(a,weights[l]) for H,L,a in side if l in L),Q(0))
   right=alpha*(poly(main[v],W[v])+sum((poly(a,sum((weights[k] for k in L),Q(0))+len(H)*u) for H,L,a in side if l in L),Q(0)))
   assert left>=right;counts["UF_checks"]+=1
  for h in product((0,1),repeat=nh):
   E=energy(h)
   if any(energy(tuple(1-b if k==v else b for k,b in enumerate(h)))<E for v in range(nh)):continue
   bits=h+tuple(1-h[orig[l]] for l in range(nl));old=costs(bits)
   for p in range(nh+nl):
    new=list(bits);new[p]=1-new[p]
    assert old[p]<=alpha*costs(tuple(new))[p],(d,sample,h,p)
    counts["deviations"]+=1
   counts['states']+=1
  counts['games']+=1
assert all(coverage.values()),coverage
result={'status':'passed','scope':'Finite exact implementation checks, not a general proof','counts':counts,'coverage':coverage,'seed':9137,'arithmetic':'fractions.Fraction; no floating threshold checks','python':platform.python_version(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'command':'python3 '+str(Path(__file__).resolve()),'parameters':{'scalar_d':[2,30],'scalar_samples_each_d':120,'game_d':[2,3,4,5,8,9],'games_each_d':13,'hubs':3,'lights':'5, except last sample per d has no lights','alpha':'d=2 games use 4; otherwise 1+ceil(sqrt(d)), certified by integer arithmetic','u':'games cycle 1,2/3,3/2; scalar tests normalized to 1','random_generation':'sources in {0,1}; raw light weights {1,...,5}/30 scaled by u/[4(1+largest raw source total)]; random side sets supplemented by empty/full sets and zero/constant/degree-d costs; main monomial amplitudes chosen as exact max of UF ratios'}}
print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
