"""Independent exact checks of insertion paths and finite copy bounds.
No game equilibrium-existence claim is tested.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial
import importlib.util
import argparse
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--repo',type=Path,default=Path.cwd())
args=parser.parse_args()
ROOT=args.repo.resolve()
spec=importlib.util.spec_from_file_location('candidate',ROOT/'tests/audits/weighted_congestion/marginal_potentials/verify_multipliers.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
checks=0
# Direct (non-Faulhaber) sums versus the compressed recurrence, including K=1.
for d,den,k,s in product(range(2,7),[2,3,7],[1,2,4,8],[Q(1,3),Q(1),Q(9)]):
 eps=Q(1,den);t=k*eps
 a=(1+t)**d+s*eps*sum((j*eps)**d for j in range(1,k+1))
 b=1+s*eps*sum((1+j*eps)**d for j in range(1,k+1))
 assert a/b==mod.finite_ratio(d,eps,t,s)
 assert (a/b) > mod.finite_ratio(d,eps,t,s+1)
 checks+=1
# Explicit finite bundle counts: endpoints, extreme ratios, nonintegral products,
# alpha=1, and R very close to alpha. Strictness survives floor integer hits.
for alpha,gap,eta,ratio_position in product([Q(1),Q(6,5),Q(10)], [Q(1,1000),Q(1,2)], [Q(1),Q(1,3),Q(1,100)], [Q(0),Q(1,3),Q(1)]):
 R=alpha+gap
 lower=1/(gap*eta)
 L=lower.numerator//lower.denominator+1
 M=L+(alpha*L/eta).__floor__()+1
 z=eta+ratio_position*(1/eta-eta)
 m=(alpha*L*z).__floor__()+1
 assert m>=1 and L>=1 and m+L<=M
 assert alpha*z < Q(m,L) < R*z
 checks+=1
# The averaging identity is an exact combinatorial fact, checked without
# assuming anonymous F_e. Three resources, two players, arbitrary set values.
from itertools import permutations
n=2;M=3
F=[[Q((e+2)*(u+3)**2+e*u,7) for u in range(1<<n)] for e in range(M)]
perms=list(permutations(range(M)))
for contexts in product(range(1<<n), repeat=M):
 avg=sum(sum(F[perm[e]][contexts[e]] for e in range(M)) for perm in perms)/factorial(M)
 H=[sum(F[e][u] for e in range(M))/M for u in range(1<<n)]
 assert avg==sum(H[u] for u in contexts)
 checks+=1
print(f'PASS {checks} independent exact finite checks: insertion ratios, finite copies, resource averaging.')
