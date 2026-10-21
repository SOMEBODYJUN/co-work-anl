"""Explore valid conditional Gram cuts on one fixed three-player strategy cone.

Finite LP proposal only. Every added row is a true nonnegative-customer square.
A relaxed vector is never called a CAG instance or SPE.
"""
from fractions import Fraction as F
from itertools import product, combinations
from functools import lru_cache
from pathlib import Path
from math import gcd
from functools import reduce
import numpy as np
from scipy.optimize import linprog
import json

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
P=6;N=3
MASKS=[s for s in range(1,1<<P) if s.bit_count()<=N]
MI={s:i for i,s in enumerate(MASKS)}
Z=(F(0),)*len(MASKS)
def unit(s): return tuple(F(i==MI[s]) for i in range(len(MASKS))) if s else Z
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def mul(c,a):return tuple(c*x for x in a)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def subs(s):
 t=s
 while True:
  yield t
  if t==0:return
  t=(t-1)&s
@lru_cache(None)
def joint(s):
 assert s and s.bit_count()<=N
 return tuple(sum(((-1)**(t.bit_count()+1)*unit(t)[j] for t in subs(s) if t),F(0)) for j in range(len(MASKS)))

@lru_cache(None)
def payoff(q,a):
 # Recover in coverage basis from Boolean evaluation by exact elimination.
 supp=sum(1<<b for b in range(P) if q[b]); masks=[s for s in subs(supp) if s]
 rows=[]
 for typ in masks:
  val=F(1,sum(q[b] for b in range(P) if typ>>b&1)) if typ>>a&1 else F(0)
  rows.append([F(bool(s&typ)) for s in masks]+[val])
 for col in range(len(masks)):
  pivot=next(i for i in range(col,len(rows)) if rows[i][col])
  rows[col],rows[pivot]=rows[pivot],rows[col]
  v=rows[col][col];rows[col]=[x/v for x in rows[col]]
  for i in range(len(rows)):
   if i!=col and rows[i][col]:
    v=rows[i][col];rows[i]=[x-v*y for x,y in zip(rows[i],rows[col])]
 out=list(Z)
 for i,s in enumerate(masks):out[MI[s]]=rows[i][-1]
 return tuple(out)

def action(h):
 if not h:return 0
 if len(h)==1:return 3 if h[0]<3 else 0
 group=range(3) if h[1]<3 else range(3,6)
 return next(a for a in group if a not in h)
def term(h):
 while len(h)<N:h=h+(action(h),)
 return tuple(h.count(a) for a in range(P))

def gram_row(condition,sign,z):
 ix=[a for a in range(P) if a!=condition] if condition is not None else list(range(P))
 out=Z
 for i,a in enumerate(ix):
  for j,b in enumerate(ix):
   ab=(1<<a)|(1<<b)
   row=joint(ab)
   if condition is not None:
    abc=ab|(1<<condition)
    row=joint(abc) if sign==1 else sub(row,joint(abc))
   out=add(out,mul(F(z[i]*z[j]),row))
 return out

def build():
 rows=[];names=[]
 for k in range(N):
  for h in product(range(P),repeat=k):
   for b in range(P):
    rows.append(sub(payoff(term(h),action(h)),payoff(term(h+(b,)),b)))
    names.append(f'Gamma:{h}:{b}')
 for u in MASKS:
  for a in subs(u):
   if not a:continue
   s=u&~a
   row=Z
   for r in subs(a):row=add(row,mul(F((-1)**(r.bit_count()+1)),unit(s|r)))
   rows.append(row);names.append(f'alternation:{s}:{a}')
 # Reproduce every sharp same-topic inequality, even though monotone submodularity implies them.
 qs=[q for q in product(range(N+1),repeat=P) if sum(q)==N]
 for a in range(P):
  for q in qs:
   if not q[a]:continue
   for r in qs:
    if not r[a] or q==r:continue
    k=max(F(sum(r[b] for b in range(P) if typ>>b&1),sum(q[b] for b in range(P) if typ>>b&1)) for typ in range(1,1<<P) if typ>>a&1)
    rows.append(sub(mul(k,payoff(r,a)),payoff(q,a)));names.append(f'dilution:{a}:{q}:{r}')
 return rows,names

def main():
 rows,names=build();root=unit((1<<0)|(1<<3)|(1<<4));obj=unit((1<<1)|(1<<2)|(1<<4))
 cuts=[];history=[]
 for it in range(61):
  rr=linprog(-np.array(obj,float),A_ub=-np.array(rows,float),b_ub=np.zeros(len(rows)),A_eq=[np.array(root,float)],b_eq=[1.],bounds=(0,None),method='highs')
  assert rr.success,rr.message
  best=[]
  for cond in [None]+list(range(P)):
   for sign in ([1] if cond is None else [1,-1]):
    ix=list(range(P)) if cond is None else [a for a in range(P) if a!=cond]
    mat=np.array([[dot(joint((1<<a)|(1<<b)),rr.x) if cond is None else dot(joint((1<<a)|(1<<b)|(1<<cond)) if sign==1 else sub(joint((1<<a)|(1<<b)),joint((1<<a)|(1<<b)|(1<<cond))),rr.x) for b in ix] for a in ix],float)
    ev,ve=np.linalg.eigh(mat)
    if ev[0]<-1e-8:
     z=np.rint(64*ve[:,0]).astype(int).tolist();g=reduce(gcd,[abs(v) for v in z]);z=[v//g for v in z]
     row=gram_row(cond,sign,z)
     val=float(dot(row,rr.x))
     if val<-1e-8:best.append((ev[0],cond,sign,z,row,val))
  history.append({'iteration':it,'objective':float(-rr.fun),'negative_kernels':len(best),'worst_eigenvalue':min((b[0] for b in best),default=0)})
  print(json.dumps(history[-1]),flush=True)
  if not best:break
  # add all currently separated conditional kernels; finite many valid rows.
  for eig,cond,sign,z,row,val in best:
   name=f'Gram:{cond}:{sign}:{z}'
   if name in names:continue
   rows.append(row);names.append(name);cuts.append({'condition':cond,'sign':sign,'z':z})
 out={'scope':'one fixed n=3,p=6 source strategy and comparison support {1,2,4}; numerical cut-generation only',
      'history':history,'cuts':cuts,'objective':float(-rr.fun),'point':rr.x.tolist(),'names':names,
      'dual_lambda':(-rr.ineqlin.marginals).tolist(),'dual_beta':float(-rr.eqlin.marginals[0])}
 (HERE/'gram_probe.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
