"""异权共享侧资源排序势独立精确审计（有限检查，不替代一般证明）。"""
from fractions import Fraction as Q
from itertools import product, combinations
import random, json, hashlib, pathlib, sys, math
SEED=7215309
rng=random.Random(SEED)
counts={"marginals":0,"resets":0,"source_budget":0,"UF_games":0,"states":0,"local_minima":0,"PNE_inequalities":0,"kappa_scale":0}

def G(c,x): return sum((a*x**k for k,a in enumerate(c)),Q())
def kap(d,t): return min(d*t,t+1)
def P(c,weights,selected,x):
 p=Q(); val=Q()
 for i in sorted(selected,key=lambda i:(-weights[i],i)):
  p+=weights[i];val+=G(c,x+p)
 return val

def ceilq(x): return -((-x.numerator)//x.denominator)
def ceilsqrt(x):
 q=math.isqrt(x.numerator//x.denominator)
 return q if q*q>=x else q+1

# Whole finite grid attacks sorted insertion/removal independently of game generation.
for d in (2,3,5):
 for n in range(1,5):
  for trial in range(18):
   weights=[Q(rng.randint(1,15),rng.randint(1,5)) for _ in range(n)]
   c=[Q(rng.randint(0,3),rng.randint(1,4)) for _ in range(d+1)]
   x=Q(rng.randint(0,9),rng.randint(1,6)); A=min(weights)
   for bits in product(range(2),repeat=n):
    S={i for i,b in enumerate(bits) if b}
    for i in set(range(n))-S:
     diff=P(c,weights,S|{i},x)-P(c,weights,S,x)
     cost=G(c,x+sum((weights[j] for j in S),Q())+weights[i])
     assert cost<=diff<=(weights[i]/A)*cost,(weights,S,i,x,c,diff,cost)
     counts['marginals']+=1
    w=Q(rng.randint(1,9),rng.randint(1,6)); extra=Q(rng.randint(0,9),rng.randint(1,6));T=x+w+extra
    M=sum(weights,Q()); diff=P(c,weights,S,x+w)-P(c,weights,S,x)
    assert 0<=diff<=kap(d,w/A)*G(c,T+M),(weights,S,x,w,T,diff,c)
    counts['resets']+=1
   for a in weights:
    for w in (Q(1,100),Q(1,3),Q(2),Q(17,3)):
     assert kap(d,w/A)<=max(Q(1),a/A)*kap(d,w/a)
     counts['kappa_scale']+=1

# Source scalar with arbitrary light partitions, including T around 1.
for d in (2,3,5):
 for trial in range(300):
  n=rng.randint(1,5); ts=[Q(rng.randint(1,20),rng.randint(1,20))*(Q(1,100) if trial%2 else 1) for _ in range(n)]
  t=sum(ts,Q());c=[Q(rng.randint(0,3),rng.randint(1,5)) for _ in range(d+1)]
  K=Q(rng.randint(1,8)); alpha=Q(1+ceilsqrt(K*d))
  lhs=K*sum((kap(d,z)*(G(c,1+z)-alpha*G(c,t)) for z in ts),Q())
  rhs=(alpha-1)*(alpha*G(c,1+t)-G(c,1))
  assert (alpha-1)**2>=K*d and lhs<=rhs
  counts['source_budget']+=1

# Literal strategies and resource reconstruction, independent of the potential evaluator.
def make_game(d,n,trial):
 hub=[Q(rng.randint(1,8),rng.randint(1,3)) for _ in range(n)]
 lights=[]
 for v,a in enumerate(hub):
  for z in range(rng.randint(0,2)):
   lights.append((v,a*Q(rng.randint(1,3),100)))
 if not lights and trial%2: lights.append((n-1,hub[-1]/100))
 W=[sum((w for v,w in lights if v==i),Q()) for i in range(n)]
 sides=[]
 for j in range(rng.randint(0,6)):
  H={i for i in range(n) if rng.randrange(3)}
  L={l for l in range(len(lights)) if rng.randrange(2)}
  c=[Q(rng.randint(0,2),rng.randint(1,3)) for _ in range(d+1)]
  sides.append((H,L,c))
 ratios=[max(hub[i] for i in H)/min(hub[i] for i in H) for H,L,c in sides if H]
 R=max([Q(1)]+ratios)
 K=max([Q(1)]+[hub[lights[l][0]]/min(hub[i] for i in H) for H,L,c in sides if H for l in L])
 alpha=max(ceilq(R),1+ceilsqrt(K*d))
 F=[]
 for v,a in enumerate(hub):
  bound=Q()
  for l,(o,w) in enumerate(lights):
   if o!=v: continue
   p=sum((alpha*G(c,sum((lights[k][1] for k in L),Q())+sum((hub[k] for k in H),Q()))-G(c,w) for H,L,c in sides if l in L),Q())
   denominator=(a+w)**d-alpha*W[v]**d
   assert denominator>0
   bound=max(bound,p/denominator)
  F.append([Q(0)]*d+[Q(max(0,ceilq(bound))+1)])
 # literal resources: each side has two replicas, every main two replicas.
 rc={}; strategies=[]
 for v,c in enumerate(F):
  for b in (0,1): rc[('A',v,b)]=c
 for j,(H,L,c) in enumerate(sides):
  for b in (0,1): rc[('B',j,b)]=c
 for v in range(n): strategies.append([{('A',v,b)}|{('B',j,b) for j,(H,L,c) in enumerate(sides) if v in H} for b in (0,1)])
 for l,(o,w) in enumerate(lights): strategies.append([{('A',o,b)}|{('B',j,1-b) for j,(H,L,c) in enumerate(sides) if l in L} for b in (0,1)])
 weights=hub+[w for o,w in lights]
 def costs(state):
  load={r:Q() for r in rc}
  for i,b in enumerate(state):
   for r in strategies[i][b]: load[r]+=weights[i]
  return [sum((G(rc[r],load[r]) for r in strategies[i][b]),Q()) for i,b in enumerate(state)]
 def potential(h,light_sources=None):
  val=Q()
  for H,L,c in sides:
   for b in (0,1):
    x=sum((lights[l][1] for l in L if (h[lights[l][0]] if light_sources is None else light_sources[l])==b),Q())
    val+=P(c,hub,{i for i in H if h[i]==b},x)
  return val
 for l,(v,w) in enumerate(lights):
  lhs=G(F[v],hub[v]+w)+sum((G(c,w) for H,L,c in sides if l in L),Q())
  rhs=alpha*(G(F[v],W[v])+sum((G(c,sum((lights[k][1] for k in L),Q())+sum((hub[k] for k in H),Q())) for H,L,c in sides if l in L),Q()))
  assert lhs>=rhs
 for h in product(range(2),repeat=n):
  counts['states']+=1
  if any(potential(h)>potential(h[:v]+(1-h[v],)+h[v+1:]) for v in range(n)): continue
  counts['local_minima']+=1
  state=h+tuple(1-h[o] for o,w in lights); old=costs(state)
  for i in range(len(weights)):
   dev=state[:i]+(1-state[i],)+state[i+1:];new=costs(dev)
   assert old[i]<=alpha*new[i],(d,hub,lights,sides,alpha,h,i,old[i],new[i])
   counts['PNE_inequalities']+=1
 counts['UF_games']+=1
 return {'R':str(R),'K':str(K),'alpha':str(alpha),'n':n,'lights':len(lights),'sides':len(sides)}
examples=[]
for d in (2,3,5):
 for n in range(1,5):
  for trial in range(14):
   v=make_game(d,n,trial)
   if len(examples)<4: examples.append(v)
print(json.dumps({'title':'异权共享侧资源排序势独立精确审计','seed':SEED,'python':sys.version.split()[0], 'arithmetic':'fractions.Fraction','counts':counts,'examples':examples,'sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
