"""Finite exploratory LP attack on graph-incidence aggregate last-slot floor.
No universality claim. Full ordered-history certificates retained by canonical solver.
"""
from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate
from fractions import Fraction
from itertools import combinations, product
from scipy.optimize import linprog
import random,sys,json

def comps(k,n):
 if k==1: yield(n,);return
 for x in range(n+1):
  for rest in comps(k-1,n-x):yield(x,)+rest

def run(p=5,n=3,trials=100,seed=1):
 rng=random.Random(seed)
 types=[(a,) for a in range(p)]+list(combinations(range(p),2))
 prefixes=list(comps(p,n-1))
 lastrows=[]
 for c in prefixes:
  lastrows.append([[Fraction(int(a in B),1+sum(c[b] for b in B)) for B in types] for a in range(p)])
 def terminal(history,actions):
  while len(history)<n: history=history+(actions[history],)
  return history
 def row_u(hist,a):
  return [Fraction(int(a in B),sum(b in B for b in hist)) if a in B else Fraction(0) for B in types]
 for it in range(trials):
  weights=[rng.randrange(1,41) for B in types]
  inst=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(B),w) for B,w in zip(types,weights)),n)
  sol=ExactSPESolver(inst)
  cert=sol.certificate(rng.choice(tuple(sol.worst_outcomes())),action_selector=lambda h,opts:rng.choice(opts),continuation_selector=lambda h,opts:rng.choice(opts))
  act=cert.actions
  rows=[]
  for d in range(n):
   for h in product(range(p),repeat=d):
    ah=act[h]
    actual=row_u(terminal(h,act),ah)
    for a in range(p):
     if a!=ah:
      dev=row_u(terminal(h+(a,),act),a)
      rows.append([float(y-x) for x,y in zip(actual,dev)]+[0.])
  for c,lrows in zip(prefixes,lastrows):
   best=max(lrows,key=lambda row:sum(w*x for w,x in zip(weights,row)))
   rows.append([-float(x) for x in best]+[1.])
  path=terminal((),act)
  W=[int(any(a in B for a in path)) for B in types]
  result=linprog(W+[-float(n)],A_ub=rows,b_ub=[0.]*len(rows),A_eq=[[1.]*len(types)+[0.]],b_eq=[1.],bounds=[(0,None)]*(len(types)+1),method='highs')
  if not result.success:raise AssertionError(result.message)
  if result.fun< -1e-7:
   ws=[Fraction(float(x)).limit_denominator(1000000) for x in result.x[:-1]]
   vals=[sum(a*w for a,w in zip(row_u(terminal(h,act),act[h]),ws))-sum(a*w for a,w in zip(row_u(terminal(h+(a,),act),a),ws)) for d in range(n) for h in product(range(p),repeat=d) for a in range(p)]
   th=min(max(sum(x*w for x,w in zip(row,ws)) for row in lrows) for lrows in lastrows)
   welfare=sum(w*z for w,z in zip(ws,W))
   print('FOUND',p,n,it,'gap',n*th-welfare,'minslack',min(vals),flush=True)
   print([(B,str(w)) for B,w in zip(types,ws) if w]); print('path',path,'theta',th,'welfare',welfare)
   out={'p':p,'n':n,'types':[(B,str(w)) for B,w in zip(types,ws)],'actions':[(h,a) for h,a in act.items()],'gap':str(n*th-welfare),'min_slack':str(min(vals))}
   print(json.dumps(out));return out
  if it%25==0:print('progress',p,n,it,'bestgap',-result.fun,flush=True)
 print('no positive LP gap',p,n,trials,flush=True)
if __name__=='__main__':run(*map(int,sys.argv[1:]))
