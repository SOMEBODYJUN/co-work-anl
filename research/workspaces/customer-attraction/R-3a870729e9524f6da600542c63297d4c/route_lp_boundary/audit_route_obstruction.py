#!/usr/bin/env python3
"""Exact audit of frozen Farkas witnesses for five route-conditioned LP gaps.

No LP solver is used.  Every column is rebuilt with Fraction and each frozen
nonnegative y is checked against A^T y >= 0 and y^T target < 0.  This only
separates the stated row family; it is not a game/SPE counterexample.
"""
from fractions import Fraction as Q
from itertools import combinations_with_replacement
import json
from pathlib import Path

N,S=6,7
DATA=Path(__file__).with_name('farkas_witnesses.json')

def floors(n,s):
 A=[Q(n+t,(t+1)*(s*n-(s-2)*t)) for t in range(n-1)]+[Q(1,n+s-1)]
 B=[Q(2,s*n-(s-2)*t) for t in range(n-1)]+[Q(n+1,n*(n+s-1))]
 return [min(A[t:]) for t in range(n)],[min(B[t:]) for t in range(n)]

def rows(inc,true):
 count=true.bit_count(); pay=[Q((true>>t)&1,count) if count else Q(0) for t in range(N)]
 alpha,beta=floors(N,S); bits=inc.bit_count()
 mixed=[pay[t]-(Q(1,N) if bits==S else alpha[t] if bits==1 else beta[t]) for t in range(N)]
 prior=(true&((1<<(N-1))-1)).bit_count()
 last=[pay[-1]-Q((inc>>j)&1,prior+1) for j in range(S)]
 pref=(true&((1<<(N-2))-1)).bit_count(); suff=pay[-2]+pay[-1]
 tax=Q((true>>(N-2))&1,(pref+1)*(pref+2)); pair=[]
 for a,b in combinations_with_replacement(range(S),2):
  c=((inc>>a)&1)+((inc>>b)&1)
  pair.append(suff+tax-(Q(c,pref+c) if c else Q(0)))
 return mixed+last+pair

def columns(route):
 final=route[-1]; out=[]
 for inc in range(1,1<<S):
  req=(inc>>final)&1; elig=sum(1<<t for t,j in enumerate(route) if inc>>j&1); tr=elig
  while True:
   if ((tr>>(N-1))&1)==req:
    target=Q(int(tr!=0))-Q(1,2)+Q(int(inc==(1<<6)),2)
    out.append((inc,tr,target,rows(inc,tr)))
   if tr==0: break
   tr=(tr-1)&elig
 return out

def run():
 d=json.loads(DATA.read_text()); reports=[]
 for item in d['routes']:
  route=tuple(item['route']); cols=columns(route); assert len(cols)==item['column_count']
  y=[Q(0)]*len(cols)
  for s in item['support']:
   i=s['column']; assert cols[i][0]==s['incidence'] and cols[i][1]==s['true_membership']
   y[i]=Q(s['weight_num'],s['weight_den'])
  assert sum(y)==1
  av=[sum(y[i]*cols[i][3][j] for i in range(len(cols))) for j in range(41)]
  obj=sum(y[i]*cols[i][2] for i in range(len(cols)))
  assert min(av)>=0 and obj<0
  reports.append({'route':list(route),'columns':len(cols),'support':sum(v>0 for v in y),'min_row_average':str(min(av)),'target_average':str(obj),'penultimate_label':route[-2],'penultimate_count_first4':sum(x==route[-2] for x in route[:4])})
 print(json.dumps({'status':'passed','scope':d['scope'],'target':d['target'],'reports':reports},indent=2))
if __name__=='__main__': run()
