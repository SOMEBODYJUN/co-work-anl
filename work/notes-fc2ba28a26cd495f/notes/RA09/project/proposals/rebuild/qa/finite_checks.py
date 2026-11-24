"""Finite boundary and inverse-image checks; these do not prove the general theorems."""
from itertools import product,combinations
from fractions import Fraction
import json
from pathlib import Path
X=set(range(3));Y=set(range(3))
def power(s):
 a=list(s)
 return [set(c) for n in range(len(a)+1) for c in combinations(a,n)]
count=0
for values in product(Y,repeat=len(X)):
 f=dict(zip(sorted(X),values));pre=lambda b:{x for x in X if f[x] in b}
 for b,c in product(power(Y),repeat=2):
  assert pre(b|c)==pre(b)|pre(c)
  assert pre(b&c)==pre(b)&pre(c)
  assert pre(Y-b)==X-pre(b)
  count+=1
indicator=[]
for A in power(X):
 f=lambda x:1 if x in A else 0
 for a in [Fraction(-1),Fraction(0),Fraction(1,2),Fraction(1),Fraction(2)]:
  actual={x for x in X if f(x)>a}
  expected=X if a<0 else A if a<1 else set()
  assert actual==expected
  indicator.append({'A':sorted(A),'a':str(a),'level':sorted(actual)})
Z=[float('-inf'),-1,0,1,float('inf')]
def sigma_atoms(generators):
 groups={}
 for z in Z:groups.setdefault(tuple(z in g for g in generators),set()).add(z)
 atoms=list(groups.values())
 return atoms,{frozenset().union(*ss) for ss in power(tuple(frozenset(a) for a in atoms))}
finite_intervals=[{z for z in Z if a<=z<b} for a,b in product(range(-2,3),repeat=2) if a<b]
a1,s1=sigma_atoms(finite_intervals)
assert len(s1)==16 and all((float('-inf') in s)==(float('inf') in s) for s in s1)
upper_rays=[{z for z in Z if z>a} for a in [Fraction(-2),Fraction(-1),Fraction(-1,2),Fraction(0),Fraction(1,2),Fraction(1),Fraction(2)]]
a2,s2=sigma_atoms(upper_rays)
assert len(s2)==32
images=[]
for j in range(256):
 x=Fraction(j,256)
 digits=[(2**k*x).__floor__()-2*(2**(k-1)*x).__floor__() for k in range(1,9)]
 assert all(b in [0,1] for b in digits)
 assert sum(Fraction(b,2**k) for k,b in enumerate(digits,1))==x
 images.append(sum(Fraction(2*b,3**k) for k,b in enumerate(digits,1)))
assert len(set(images))==256
result={'purpose':'仅核对有限模型中的逆像恒等式、端点和二进制公式；一般证明见蓝色正文。','inverse_images':{'input':'X=Y={0,1,2};全部27个点映射与64对目标子集','cases':count,'union_intersection_complement':'pass'},'indicator_levels':{'input':'X={0,1,2};全部8个A;阈值-1,0,1/2,1,2','cases':len(indicator),'status':'pass','samples':indicator[:10]},'endpoint_generators':{'input':'{-∞,-1,0,1,+∞};所有选定有限端点半开区间与上射线','finite_interval_sigma_size':len(s1),'finite_interval_endpoints_indistinguishable':True,'upper_ray_sigma_size':len(s2),'status':'pass'},'binary_to_ternary':{'input':'x=j/256, j=0,...,255;floor数位前8项','tested_points':256,'reconstruction':'pass','distinct_images':len(set(images)),'status':'pass'}}
p=Path(__file__).with_name('finite-checks.json');p.write_text(json.dumps(result,ensure_ascii=False,indent=2).rstrip()+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='indicator_levels'},ensure_ascii=False))
