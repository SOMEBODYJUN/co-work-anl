"""Independent exact certificate replay and polynomial tail review.

Imports neither the author's audit nor a discovery/model implementation.
The finite columns are reconstructed from genuine incidence and membership.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations_with_replacement
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'general_joint_analytic'

def envelope(n):
    A=[Q(n+t,(t+1)*(7*n-5*t)) for t in range(n-1)]+[Q(1,n+6)]
    B=[Q(2,7*n-5*t) for t in range(n-1)]+[Q(n+1,n*(n+6))]
    return [min(A[t:]) for t in range(n)],[min(B[t:]) for t in range(n)]

def coefficients(n,I,E):
    J=E+((I&1)<<(n-1));z=J.bit_count()
    shares=[Q((J>>t)&1,z) if z else Q() for t in range(n)]
    A,B=envelope(n);m=I.bit_count()
    M=[shares[t]-(Q(1,n) if m==7 else A[t] if m==1 else B[t]) for t in range(n)]
    L=[shares[-1]-Q((I>>j)&1,E.bit_count()+1) for j in range(7)]
    h=(E&((1<<(n-2))-1)).bit_count();d=(E>>(n-2))&1
    T=[]
    for j,k in combinations_with_replacement(range(7),2):
        v=((I>>j)&1)+((I>>k)&1)
        T.append(shares[-2]+shares[-1]+Q(d,(h+1)*(h+2))-(Q(v,h+v) if v else Q()))
    return J,M,L,T

def literal(cert):
    n=cert['n'];lam=[Q(v,cert['denominator']) for v in cert['numerators']]
    assert len(lam)==n+35 and min(lam)>=0
    active=[(q,w) for q,w in enumerate(lam) if w]
    minimum=None;witness=None;count=0
    for I in range(1,128):
      for E in range(1<<(n-1)):
        J,M,L,T=coefficients(n,I,E);rows=M+L+T
        r=Q(bool(J))-Q(1,2)-sum((w*rows[q] for q,w in active),Q())
        assert r>=0,(n,I,J,r)
        if minimum is None or r<minimum:minimum,witness=r,(I,J)
        count+=1
    assert count==cert['columns'] and minimum==Q(cert['minimum_residual'])
    return {'n':n,'columns':count,'minimum':str(minimum),'witness':witness}

a,b,c,e=Q(3,4),Q(2,19),Q(11,133),Q(6,665)
q=6*c+15*e;delta=b+c+5*e
assert q==Q(12,19)==6*b and delta==Q(31,133)

def residual(f,k,p,d,F):
    z=p+d+f
    G=Q(k,p+1) if not f else Q(6-k,p+1)+Q(2*k,p+2)
    K=Q(k*(6-k),p+1)+Q(k*(k-1),p+2)
    return Q(bool(z))-Q(1,2)+a*F+Q(b*k,p+d+1)+c*G+e*K-(Q(a*p+q*d+(q+6*b)*f,z) if z else 0)-Q(q*d,(p+1)*(p+2))

def finite(n):
    A,B=envelope(n);P=sum(A[:-2],Q());V=sum(B[:-2],Q())
    minimum=None;witness=None;count=0
    for f in (0,1):
      for k in range(7):
        if not f+k:continue
        for p in range(n-1):
          for d in (0,1):
            F=Q(n-2,n) if f+k==7 else P if f+k==1 else V
            r=residual(f,k,p,d,F);assert r>=0
            if minimum is None or r<minimum:minimum,witness=r,(f,k,p,d)
            count+=1
    return {'n':n,'columns':count,'minimum':str(minimum),'witness':witness}

def tail():
    # All rational identities below, after multiplying (p+1)(p+2),
    # have degree at most two. Three distinct substitutions prove each
    # coefficient identity, while signs follow from the displayed forms.
    D=Q(1,8) # private floor set to 1/2; omitted common term is -3/(4n).
    private={
        (0,0):lambda p:D+Q(delta,p+1),
        (0,1):lambda p:D+Q(187*p-18,532*(p+1)*(p+2)),
        (1,0):lambda p:D-Q(9,532*(p+1)),
        (1,1):lambda p:D+Q(27*p-9,266*(p+1)*(p+2)),
    }
    checks=0
    for (f,d),fun in private.items():
      for p in (1,2,3) if (f,d)==(0,0) else (0,1,2):
        assert residual(f,1-f,p,d,Q(1,2))==fun(p);checks+=1
    uncovered_private=residual(0,1,0,0,Q(1,2))
    assert uncovered_private==Q(115,1064)
    assert uncovered_private-Q(3,28)==Q(1,1064)
    C1=lambda k:a-2*q+b*k+c*(6-k)+e*k*(6-k)
    C2=lambda k:2*c*k+e*k*(k-1)
    E=lambda k:Q(27,266)+delta*k+(6-k)*(c+e*k)-q
    assert C1(1)==Q(27,532) and C1(6)==Q(9,76)
    assert E(1)==Q(43,266) and E(6)==Q(33,38)
    assert -Q(1,4)+2*(b+c)==Q(67,532)
    for k in range(2,7):
        assert residual(0,k,0,0,Q(1,3))==-Q(1,4)+(b+c)*k+e*Q(k*(11-k),2)
        for p in (1,2,3):
            assert residual(0,k,p,0,Q(1,3))==Q((b+c)*k,p+1)+e*(Q(k*(6-k),p+1)+Q(k*(k-1),p+2))
            checks+=1
    for k in range(1,7):
      assert C1(k)>0 and C2(k)>=0 and E(k)>0
      for p in (0,1,2):
        assert residual(1,k,p,0,Q(1,3))==Q(C1(k),p+1)+Q(C2(k),p+2)
        assert residual(1,k,p,1,Q(1,3))==Q(p*(Q(27,266)+delta*k)+E(k),(p+1)*(p+2))
        checks+=2
    for p in (0,1,2):
        assert residual(0,2,p,1,Q(1,3))-e*Q(2*4,p+1)-e*Q(2,p+2)==Q(263*p+78,532*(p+1)*(p+2))
        checks+=1
    # Private floor quadratic and logarithm lower-bound arithmetic.
    assert Q(3*7*7-18*7-5,4)>0
    assert Q(316,375)>Q(5,6) and 3*(7*13+5)>7*(2*13+15)
    return {'status':'passed','rational_identity_checks':checks,
            'uncovered_shared_lower_bound':'67/532',
            'private_uniform_bound_at_n7':'1/1064',
            'analytic_scope':'all n>=13; finite substitutions check polynomial identities, not a finite n extrapolation',
            'reviewed_sign_mechanism':['positive private endpoint bound', 'nonnegative shared pair terms', 'concave C1 and E with positive endpoints', 'log-integral shared floor >=1/3']}

if __name__=='__main__':
    certs=json.loads((SRC/'n7_n8_exact_duals.json').read_text())
    result={'status':'passed','literal':[literal(x) for x in certs],
            'finite_compressed':[finite(n) for n in range(9,13)],'analytic_tail':tail(),
            'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (SRC/'seven_maxima_seven_plus.md',SRC/'n7_n8_exact_duals.json')}}
    (Path(__file__).with_suffix('.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
