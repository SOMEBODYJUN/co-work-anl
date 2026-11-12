from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
out=Path(__file__).parent
# Literal Appendix B truncation fails before any implementation issue.
cut=1/(F(11,10)*2);left=sum(v for v in [F(9,20),F(11,20)] if v>=cut)
assert cut==F(5,11) and left==F(11,20)<F(10,11)
# Test exact q-grid/count/residue deletion guarantees on all short integer patterns.
s=F(1,2);q=1+s;k=0
while q**(-k)>s/q:k+=1
assert q**(-k)/(1-q**(-k))<=s
checks=0
for counts in product(range(4),repeat=7):
 vals=[q**(-i) for i in range(len(counts))];rounded=[]
 for d in counts:
  if not d:rounded.append(0);continue
  ell=0
  while q**(ell+1)<=d:ell+=1
  z=q**ell;c=(z.numerator+z.denominator-1)//z.denominator
  assert F(d)/q<=c<=d;rounded.append(c)
 keep=[0]*len(counts)
 for residue in range(k):
  best=0
  for i in range(residue,len(counts),k):
   if rounded[i]>best:keep[i]=rounded[i];best=rounded[i]
 old=sum(c*v for c,v in zip(rounded,vals));new=sum(c*v for c,v in zip(keep,vals));assert new>=old/q
 checks+=1
# Exhaust every arbitrary high-guess acceptance pattern for small integer optima.
# The tested predicate accepts all K<=OPT; high guesses may behave arbitrarily.
searches=0
for U in range(0,10):
 for opt in range(U+1):
  for high in product([False,True],repeat=U-opt):
   acc={K:(True if K<=opt else high[K-opt-1]) for K in range(1,U+1)}
   lo,hi=0,U+1
   while hi-lo>1:
    mid=(lo+hi)//2
    if acc[mid]:lo=mid
    else:hi=mid
    assert hi>opt
   assert lo>=opt;searches+=1
params=[]
for alpha,eta in product([F(2),F(3),F(10)],[F(1,10),F(1)]):
 ss=F(1,2)
 while (1-ss)/(1+ss)**3<=alpha/(alpha+eta):ss/=2
 b=(1-ss)/(1+ss)**3;a0=(alpha/b+alpha+eta)/2
 assert alpha/b<=a0<alpha+eta
 params.append({'alpha':str(alpha),'eta':str(eta),'s':str(ss),'b':str(b),'a0':str(a0)})
report={'scope':'Finite exact arithmetic/contract checks, not all-parameter proof or construction of the assumed UM algorithm.','literal_appendix_counterexample':{'cutoff':str(cut),'remaining':str(left),'claimed_bound':str(F(10,11))},'q_grid_residue_count_patterns':checks,'q':str(q),'kappa':k,'tail_ratio':str(q**(-k)/(1-q**(-k))),'nonmonotone_search_predicates':searches,'fixed_parameter_examples':params}
(out/'rational-contract-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
