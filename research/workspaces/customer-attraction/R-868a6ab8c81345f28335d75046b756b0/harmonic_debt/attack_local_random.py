"""Counterexample attack for e_T(q)-d_i(T) <= player i self insertion credit.
Exact integer types; exact Fraction backward induction and exact residual checks.
This is a strictly stronger local candidate than the requested global H4.
"""
from fractions import Fraction as F
from itertools import product
import random,json
random.seed(260624)
K=4;m=4
B=[tuple((mask>>a)&1 for a in range(K)) for mask in range(1,1<<K)]
for trial in range(2000):
 weights=[random.randint(0,20) for _ in B]
 acts={}; cache={}
 def payoff(h,a):
  return sum((F(w*mem[a],sum(mem[x] for x in h)) for w,mem in zip(weights,B) if mem[a]),F())
 def walk(h):
  if len(h)==m:return h
  leaves=[walk(h+(a,)) for a in range(K)]
  values=[payoff(leaf,a) for a,leaf in enumerate(leaves)]
  mx=max(values); choices=[a for a,v in enumerate(values) if v==mx];a=random.choice(choices)
  acts[h]=a
  return leaves[a]
 q=walk(())
 def leaf(h):
  while len(h)<m:h=h+(acts[h],)
  return h
 loads=[sum(mem[x] for x in q) for mem in B]
 for i,a in product(range(m),range(K)):
  e=sum((F(w*mem[a],c+1) for w,mem,c in zip(weights,B,loads)),F())
  g=sum((F(w*mem[q[i]],c*(c+1)) for w,mem,c in zip(weights,B,loads) if c),F())
  d=payoff(leaf(q[:i]+(a,)),a)
  if e-d>g:
   print(json.dumps({'trial':trial,'m':m,'K':K,'weights':weights,'q':q,'i':i,'T':a,'e':str(e),'d':str(d),'g':str(g),'gap':str(e-d-g),'actions':[{'history':h,'action':v} for h,v in acts.items()]}))
   raise SystemExit
print('No counterexample found; this is not evidence of a general theorem.')
