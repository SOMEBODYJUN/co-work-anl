#!/usr/bin/env python3
"""有限域真实最优源与固定阶投影向量贪心的精确核验。"""
import itertools,json,math,hashlib,platform
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import numpy as np


def is_prime(q):
 return isinstance(q,int) and not isinstance(q,bool) and q>=2 and all(q%d for d in range(2,math.isqrt(q)+1))


def source(q,r):
 assert is_prime(q) and isinstance(r,int) and r>=1
 d=2*r+1
 coeff=np.array(list(itertools.product(range(q),repeat=d)),dtype=np.int64)
 raw=np.empty((len(coeff),q),dtype=np.int64)
 for t in range(q):
  v=np.ones(len(coeff),dtype=np.int64)
  for h in range(d-1,-1,-1):v=(v*t+coeff[:,h])%q
  raw[:,t]=v
 owners=np.where(raw<2,0,raw-1)
 cap=2*d
 for i in range(q-1):assert int(np.max(np.sum(owners==i,axis=1)))<=cap
 return raw,owners


def check_independence(raw,owners,hmax,all_subsets):
 count=0;q=raw.shape[1];worlds=len(raw)
 for h in range(1,min(hmax,q)+1):
  subsets=list(itertools.combinations(range(q),h)) if all_subsets else [tuple(range(h)),tuple(range(q-h,q))]
  for jobs in dict.fromkeys(subsets):
   code=sum(raw[:,j]*(q**s) for s,j in enumerate(jobs))
   values=np.bincount(code,minlength=q**h)
   assert np.all(values==worlds//(q**h))
   merged=Counter(tuple(int(owners[z,j]) for j in jobs) for z in range(worlds))
   for targets in itertools.product(range(q-1),repeat=h):
    want=F(math.prod(2 if i==0 else 1 for i in targets),q**h)
    assert F(merged[targets],worlds)==want
   count+=1
 return count


def exact_higher_projection():
 # Actual degree5 polynomial source q3; validates truncation algebra r2,
 # without claiming a bad ratio when q<=B. Finite test uses every source atom.
 q,r=3,2;raw,own=source(q,r);worlds=len(own);p=F(2,3)
 subsets=[()] + [(j,) for j in range(q)] + list(itertools.combinations(range(q),2))
 columns=[[math.prod((F(int(own[z,j]==0))-p for j in S),start=F(1)) for z in range(worlds)] for S in subsets]
 G=[[sum(a*b for a,b in zip(x,y))/worlds for y in columns] for x in columns]
 assert all(G[a][b]==(F(2,9)**len(subsets[a]) if a==b else 0) for a in range(len(G)) for b in range(len(G)))
 coeff=[F(1)]+[F() for _ in subsets[1:]];trace=[]
 for step,j in enumerate(range(q)):
  psi=[sum(c*v[z] for c,v in zip(coeff,columns)) for z in range(worlds)]
  choices=[]
  for i in range(q-1):
   rhs=[sum(v[z]*psi[z] for z in range(worlds) if own[z,j]==i)/worlds for v in columns]
   c=[rhs[a]/G[a][a] for a in range(len(subsets))]
   norm=sum(G[a][a]*c[a]*c[a] for a in range(len(c)))
   choices.append((norm,c))
  assert choices[0][0]>choices[1][0]
  lower=sum(G[a][a]*coeff[a]*coeff[a] for a,S in enumerate(subsets) if len(S)<r)
  top=sum(G[a][a]*coeff[a]*coeff[a] for a,S in enumerate(subsets) if len(S)==r)
  for i,(score,c) in enumerate(choices):
   pi=p if i==0 else 1-p
   assert score==pi*lower+pi*pi*top
  trace.append([str(c[0]) for c in choices]);coeff=choices[0][1]
 return dict(q=q,r=r,source_atoms=worlds,basis_dimension=len(subsets),actual_gram_and_projection=True,scores=trace)


def recurrence_audit():
 checks=0
 for r in range(1,5):
  B=4*r+2
  for q in [p for p in range(B+1,80) if is_prime(p)]:
   p=F(2,q)
   for s in range(q):
    parts=[F(math.comb(s,k))*p**(2*s-k)*(1-p)**k for k in range(min(r,s)+1)]
    lo=sum(parts[:r]);hi=parts[r] if r<=s else F()
    a=p*lo+p*p*hi;b=F(1,q)*lo+F(1,q*q)*hi
    assert a>b>=0
    checks+=1
 return checks


def main():
 cases=[]
 for q in [3,5,7,13]:
  raw,owners=source(q,1)
  caps=[int(np.max(np.sum(owners==i,axis=1))) for i in range(q-1)]
  h=check_independence(raw,owners,3,True)
  cases.append(dict(q=q,r=1,source_atoms=len(raw),distinct_job_sets_checked=h,source_capacity_max=max(caps),anchor_load=6,optimum='6',greedy_makespan=str(max(q,6)),ratio=str(F(max(q,6),6))))
 # Full 161051 coefficient atoms, not random sampling; selected five-point
 # independence checks supplement the universal Vandermonde proof only.
 raw,owners=source(11,2)
 high=dict(q=11,r=2,source_atoms=len(raw),source_max=int(max(np.max(np.sum(owners==i,axis=1)) for i in range(10))),anchor_load=10,selected_job_sets_checked=check_independence(raw,owners,5,False))
 return dict(title='固定阶压缩乘法向量贪心的多项式真实源精确核验',source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),python=platform.python_version(),numpy=np.__version__,arithmetic='integer field operations; exact fractions; deterministic full source enumeration, no seed or floating tolerance',r1_cases=cases,r2_full_source=high,r2_actual_projection=exact_higher_projection(),score_recurrence_checks=recurrence_audit(),limitations=['finite computations are not universal proof','r1 triple independence checked for all job subsets only in listed q','r2 q11 tests selected job subsets, all source capacities; r2 q3 checks actual compressed effects','no hierarchy integrality gap or general scheduling impossibility'])

def export_certificate(directory):
 q,r=13,1;raw,owners=source(q,r);B=6
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
 matrix=[[1]*q+[None] for _ in range(q-1)]+[[None]*q+[B]]
 data=dict(title='q13真实最优矩向量贪心反例',q=q,r=r,m=q,n=q+1,processing_times=matrix,infinity_marker=None)
 cert=dict(title='q13全部系数标签最优调度源',q=q,r=r,degree=3,coefficient_order='a0,a1,a2 lexicographic; f(t)=t^3+a2*t^2+a1*t+a0 mod13',weight_each='1/2197',optimum='6',forced_anchor_job=13,forced_anchor_machine=12,source_schedules=[list(map(int,row))+[12] for row in owners],greedy_schedule=[0]*13+[12],greedy_makespan='13',ratio='13/6',generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 for name,value in [('polynomial_vector_greedy_q13_input.json',data),('polynomial_vector_greedy_q13_certificate.json',cert)]:
  with (directory/name).open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--export-directory',type=Path)
 args=parser.parse_args()
 if args.export_directory:export_certificate(args.export_directory)
 print(json.dumps(main(),ensure_ascii=False,indent=2))
