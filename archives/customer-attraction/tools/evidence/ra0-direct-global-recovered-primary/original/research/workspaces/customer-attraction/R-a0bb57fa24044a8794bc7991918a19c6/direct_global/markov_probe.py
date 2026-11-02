"""Exploratory m=3 equality between full-history and count-Markov SPE outcomes.
Finite evidence only. Markov ties are enumerated; second-stage selections remain
independent across distinct one-action count states. No claim from passing tests.
"""
from itertools import combinations_with_replacement, product
from random import Random
from math import prod
import json
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def inc(q,a):
 q=list(q);q[a]+=1;return tuple(q)

def markov3(I,cap=1000000):
 k=I.topic_count;z=(0,)*k;cache={}
 def u(q,a):
  if q not in cache:cache[q]=I.topic_payoffs(q)
  return cache[q][a]
 pairs=[inc(inc(z,a),b) for a,b in combinations_with_replacement(range(k),2)]
 br=[]
 for q in pairs:
  v=[u(inc(q,a),a) for a in range(k)];mx=max(v)
  br.append([a for a in range(k) if v[a]==mx])
 if prod(map(len,br))>cap:return None
 found=set()
 for row in product(*br):
  last=dict(zip(pairs,row));children=[]
  for a in range(k):
   v=[];out=[]
   for b in range(k):
    q=inc(inc(z,a),b);t=inc(q,last[q]);out.append(t);v.append(u(t,b))
   mx=max(v);children.append(set(out[b] for b in range(k) if v[b]==mx))
  floor=max(min(u(t,a) for t in child) for a,child in enumerate(children))
  found.update(t for a,child in enumerate(children) for t in child if u(t,a)>=floor)
 return found

if __name__=='__main__':
 import sys
 R=Random(317);num=int(sys.argv[1]) if len(sys.argv)>1 else 10000;k=int(sys.argv[2]) if len(sys.argv)>2 else 4
 for it in range(num):
  weights=[R.choice([0,0,0,1,1,2,3,4]) for mask in range(1,1<<k)]
  I=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if mask>>a&1),w) for mask,w in enumerate(weights,1) if w),3)
  full=set(ExactSPESolver(I).outcomes());markov=markov3(I)
  if markov is None:continue
  if full!=markov:
   print(json.dumps({'iteration':it,'instance':I.to_dict(),'full_only':sorted(full-markov),'markov_only':sorted(markov-full),'full_welfares':sorted({I.welfare(t) for t in full}),'markov_welfares':sorted({I.welfare(t) for t in markov})}));break
 else:print('no separation',num)
