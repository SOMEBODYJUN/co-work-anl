"""One new exact polynomial check for a newly found source formula defect.

No game solving, SPE verification, LP, random sampling, or old audit replay.
Coefficient lists are ascending powers of the integer parameter m.
"""
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

def trim(a):
    a=list(a)
    while len(a)>1 and a[-1]==0:a.pop()
    return tuple(a)
def add(a,b):
    return trim(tuple((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                      for i in range(max(len(a),len(b)))))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return trim(out)
def scale(k,a):return trim(tuple(k*x for x in a))

source=Path(sys.argv[1]);raw=source.read_bytes()
expected='fba5271b8795af9f00d489d3158df865d512d2e0c4a9a964a031e3a7b1792f4f'
assert hashlib.sha256(raw).hexdigest()==expected
text=raw.decode()
assert r'2(m-1)(m^2-m-1)' in text
assert r'D_m-2(m-1)(m^2-m-1)=3m^2+m-4' in text

m=(0,1);one=(1,);minusone=(-1,1)
D=(-2,3,-1,2)
oldN=scale(2,mul(minusone,(-1,-1,1)))
newN=scale(2,mul(minusone,(1,-1,1)))
gamma=(-1,2,-3,4)
def weighted_a_cross(N):
    return add(mul(mul(N,m),(-1,2)),mul(sub(D,N),mul(minusone,minusone)))
def weighted_b_cross(N):return add(N,scale(2,mul(m,sub(D,N))))
a_target=mul(mul(gamma,m),minusone);b_target=scale(2,gamma)
assert weighted_a_cross(newN)==a_target
assert weighted_b_cross(newN)==b_target
assert weighted_a_cross(oldN)!=a_target
assert weighted_b_cross(oldN)!=b_target
assert sub(D,newN)==(0,-1,3)  # m(3m-1)>0 for every m>=2
assert sub(scale(2,D),gamma)==(-3,4,1)  # m^2+4m-3>0 for every m>=2
assert sub(sub(D,oldN),(-4,1,3))==(0,2)

n=2;den=2*n**3-n*n+3*n-2
old_weight=F(2*(n-1)*(n*n-n-1),den)
new_weight=F(2*(n-1)*(n*n-n+1),den)
pa,pb,la,lb=F(2*n-1,n-1),F(1,2),F(n-1,n),F(n)
old_pair=(old_weight*pa+(1-old_weight)*la,old_weight*pb+(1-old_weight)*lb)
new_pair=(new_weight*pa+(1-new_weight)*la,new_weight*pb+(1-new_weight)*lb)
target=F(4*n**3-3*n*n+2*n-1,den)
assert old_pair==(F(13,16),F(29,16)) and new_pair==(F(23,16),F(23,16))
assert target==F(23,16)
report={
 'status':'passed-new-correction-algebra-only',
 'source_sha256':expected,'source_bytes':len(raw),
 'coefficient_order':'ascending powers of m',
 'D':D,'old_lambda_numerator':oldN,'corrected_lambda_numerator':newN,
 'gamma_numerator':gamma,
 'corrected_a_cross':weighted_a_cross(newN),'a_target_cross':a_target,
 'corrected_b_cross':weighted_b_cross(newN),'b_target_cross':b_target,
 'original_a_cross_residual':sub(weighted_a_cross(oldN),a_target),
 'original_b_cross_residual':sub(weighted_b_cross(oldN),b_target),
 'corrected_D_minus_numerator':sub(D,newN),
 'two_D_minus_gamma_numerator':sub(scale(2,D),gamma),
 'original_claimed_positivity_identity_residual':sub(sub(D,oldN),(-4,1,3)),
 'm2_sanity':{'old_lambda':str(old_weight),'corrected_lambda':str(new_weight),
              'old_a_b':list(map(str,old_pair)),'corrected_a_b':list(map(str,new_pair)),
              'gamma':str(target)},
 'domain':'polynomial identities exact; denominators and signs for integer m>=2 justified analytically in new body',
 'does_not_check':['any game or SPE history','the old unprovided audit','any original optimizer run','PB background reachability','any half conjecture beyond the stated structural theorem']}
print(json.dumps(report,ensure_ascii=False,indent=2))
