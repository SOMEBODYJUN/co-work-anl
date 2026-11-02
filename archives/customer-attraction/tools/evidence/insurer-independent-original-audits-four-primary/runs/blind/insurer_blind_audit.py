"""Definition-level Fraction audit of the proposed disjoint insurer and product compiler.

No customer_attraction solver is imported. The policy is completed by exact ordered
backward induction with forced spine nodes, then separately replayed at every node.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, math


def insurer_sizes(m,s):return (2*s,(m-1)*s)+((s,)*(m-2))

def disjoint_payoff(sizes,h,i):
 a=h[i];return F(sizes[a],h.count(a))

def forced(m,h,mode):
 if not h:return 0
 # Root Y: pure-Y prefix picks X; after unique X, continue Y.
 if h[0]==1:
  if all(a==1 for a in h):return 0
  if h.count(0)==1 and all(a in (0,1) for a in h):return 1
 # Root X and specified modes; alternative second Y keeps all Y.
 if h[0]==0:
  if mode=='compliant' and h.count(0)==1 and all(a in (0,1) for a in h):return 1
  if mode=='punitive':
   if len(h)==1:return 0
   if h[1]==0 and h.count(0)==2 and all(a in (0,1) for a in h):return 1
   if h[1]==1 and h.count(0)==1 and all(a in (0,1) for a in h):return 1
 return None

def complete(m,s,mode):
 sizes=insurer_sizes(m,s);pol={};z={}
 for d in range(m-1,-1,-1):
  for h in product(range(m),repeat=d):
   cand=[]
   for a in range(m):
    hh=h+(a,);term=hh if d+1==m else z[hh]
    cand.append((disjoint_payoff(sizes,term,d),term))
   mx=max(v for v,t in cand);a=forced(m,h,mode)
   if a is None:a=next(i for i,(v,t) in enumerate(cand) if v==mx)
   assert cand[a][0]==mx,('forced not optimal',m,mode,h,a,cand)
   pol[h]=a;z[h]=cand[a][1]
 return pol,z

def replay(pol,h,m):
 while len(h)<m:h=h+(pol[h],)
 return h

def audit_insurer(m):
 modes={};checks=0
 for mode in ('compliant','punitive'):
  pol,z=complete(m,1,mode);sizes=insurer_sizes(m,1)
  for h,a in pol.items():
   t=replay(pol,h,m);u=disjoint_payoff(sizes,t,len(h))
   for b in range(m):
    dev=replay(pol,h+(b,),m)
    assert u>=disjoint_payoff(sizes,dev,len(h))
    checks+=1
  t=replay(pol,(),m)
  assert t==((0,)+(1,)*(m-1) if mode=='compliant' else (0,0)+(1,)*(m-2))
  assert disjoint_payoff(sizes,t,0)==(2 if mode=='compliant' else 1)
  for b in range(1,m):
   dev=replay(pol,(b,),m)
   assert disjoint_payoff(sizes,dev,0)<=1
  modes[mode]={'path':t,'root_payoff':str(disjoint_payoff(sizes,t,0)),'nodes':len(pol)}
 assert sum(sizes)==2*m-1
 assert sizes[0]+sizes[1]==m+1
 assert 2*(sizes[0]+sizes[1])-sum(sizes)==3
 return {'m':m,'modes':modes,'node_action_checks':checks}

def old_utility(customers,h,i):
 return sum((F(w,sum(a in T for a in h)) for T,w in customers if h[i] in T),F(0))

def old_plan(m,k,customers):
 pol={};z={}
 for d in range(m-1,-1,-1):
  for h in product(range(k),repeat=d):
   vals=[]
   for a in range(k):
    hh=h+(a,);t=hh if d+1==m else z[hh]
    vals.append((old_utility(customers,t,d),t))
   best=max(v for v,t in vals) if d else min(v for v,t in vals)
   a=next(i for i,(v,t) in enumerate(vals) if v==best)
   pol[h]=a;z[h]=vals[a][1]
 delta=max(old_utility(customers,z[(a,)],0) for a in range(k))-old_utility(customers,z[()],0)
 return pol,z,delta

def audit_product(m=4):
 k=3;customers=[((0,),2),((1,),5),((0,1),1),((1,2),4),((2,),1)]
 oldpol,z,delta=old_plan(m,k,customers)
 assert delta>0
 scale=delta.denominator
 customers=[(T,w*scale) for T,w in customers];delta*=scale
 oldpol,z,delta2=old_plan(m,k,customers);assert delta2==delta
 s=int(delta);a0=oldpol[()]
 ipols={mode:complete(m,s,mode)[0] for mode in ('compliant','punitive')}
 acts=tuple(product(range(k),range(m)))
 def act(h):
  oh=tuple(a for a,b in h);ih=tuple(b for a,b in h)
  mode='compliant' if not h or h[0][0]==a0 else 'punitive'
  return (oldpol[oh],ipols[mode][ih])
 def play(h):
  while len(h)<m:h=h+(act(h),)
  return h
 sizes=insurer_sizes(m,s)
 def util(t,i):return old_utility(customers,tuple(a for a,b in t),i)+disjoint_payoff(sizes,tuple(b for a,b in t),i)
 checks=0
 for d in range(m):
  for h in product(acts,repeat=d):
   u=util(play(h),d)
   for a in acts:
    assert u>=util(play(h+(a,)),d),(h,a,u,util(play(h+(a,)),d))
    checks+=1
 actual=play(());oldactual=z[()]
 oldW=sum(w for T,w in customers if any(a in T for a in oldactual))
 oldOPT=max(sum(w for T,w in customers if any(a in T for a in h)) for h in product(range(k),repeat=m))
 newW=oldW+(m+1)*s;newOPT=oldOPT+(2*m-1)*s
 assert newOPT-2*newW==oldOPT-2*oldW-3*delta
 return {'m':m,'old_scale':scale,'delta':str(delta),'actual':actual,'checks':checks,'old_gap':str(oldOPT-2*oldW),'new_gap':str(newOPT-2*newW)}

if __name__=='__main__':
 report={'insurers':[audit_insurer(m) for m in range(2,7)],'product':audit_product()}
 print(json.dumps(report,indent=2))
 Path(__file__).with_name('insurer_blind_audit.json').write_text(json.dumps(report,indent=2)+'\n')
