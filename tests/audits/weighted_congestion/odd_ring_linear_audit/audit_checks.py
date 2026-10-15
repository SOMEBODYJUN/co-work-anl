"""Finite exact/Decimal evidence for odd-ring audit; not a proof substitute."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
from pathlib import Path

OUT = Path(__file__).with_name('audit_checks.json')

def exact_reset(d, t, alpha):
    z=(1+t)**d
    Q=z-alpha; P=alpha*z-t**d; B=Q/P
    H=(z+t**(d+1))/(1+t*z)
    assert 1 < alpha < H and B>t
    R=5
    while not (t**R < 1/(4*alpha) and (B/t)**R>8*alpha**2):
        R+=4
    x=t**R; n=(1/(2*alpha*x)).numerator//(1/(2*alpha*x)).denominator
    N=1+x-alpha*n*x; M=alpha*(1+n*x)-1
    G=n*N/M*B**R
    assert N>0 and M>0 and P>0 and Q>0 and G>1
    m=(R+1)//2
    xs=[x]+[1/t]*(m-1)
    ns=[n]+[1]*(m-1)
    ks=[1]+[d]*(m-1)
    us=[F(1)]+[t**(2*(m-i)) for i in range(1,m)]
    vs=[t**R]+[t**(2*(m-i)-1) for i in range(1,m)]
    assert all(vs[i]/us[i]==xs[i] and vs[i]/us[(i+1)%m]==t for i in range(m))
    Ns=[(1+xx)**kk-alpha*(nn*xx)**kk for xx,nn,kk in zip(xs,ns,ks)]
    Ms=[alpha*(1+nn*xx)**kk-1 for xx,nn,kk in zip(xs,ns,ks)]
    K=[ns[i]*Ns[i]*Q/(P*Ms[(i+1)%m]) for i in range(m)]
    delta=F(2)
    while delta**(m-1)>=G:
        delta=1+(delta-1)/2
    qs=[F(1)]
    for i in range(m-1): qs.append(K[i]*qs[-1]/delta)
    ps=[(qs[(i+1)%m]*Ms[(i+1)%m]/(ns[i]*Q)+qs[i]*Ns[i]/P)/2 for i in range(m)]
    assert all(qs[i]*Ns[i]>ps[i]*P and ns[i]*ps[i]*Q>qs[(i+1)%m]*Ms[(i+1)%m] for i in range(m))
    with localcontext() as ctx:
        ctx.prec=40
        Gdec=D(G.numerator)/D(G.denominator)
        gd=str(Gdec)
    return dict(d=d,t=str(t),alpha=str(alpha),H=str(H),R=R,m=m,n0=str(n),product_approx=gd,all_exact_inequalities_pass=True,full_state_enumeration=False)

def original_candidate(s):
    ri=2**s; r=F(ri); m=s if s%2 else s+1; L=2*m-1; d=2*s*ri; alpha=r/4
    x=r**(-L); n=(ri**L)//s
    N=(1+x)**s-alpha*(n*x)**s
    M=alpha*(1+n*x)**s-1
    z=(1+1/r)**d; P=alpha*z-r**(-d); Q=z-alpha
    G=n*N/M*(Q/P)**L
    assert N>0 and M>0 and P>0 and Q>0 and G>r/(6*s)>1
    with localcontext() as ctx:
        ctx.prec=40
        gd=D(G.numerator)/D(G.denominator)
        return dict(s=s,r=ri,m=m,d=d,alpha=str(alpha),n0=str(n),product_approx=str(gd),claim_lower=str(r/(6*s)),exact_pass=True)

def decimal_envelope(d):
    with localcontext() as ctx:
        ctx.prec=100
        dd=D(d); L=dd.ln(); t=(L/(dd+1)).exp()-1
        E=1/(t+(1+t)**(-d))
        H=E+t**(d+1)/(1+t*(1+t)**d)
        uniform=dd/(L+2)
        assert H>=E and E>1
        if d>=4: assert E>uniform
        return dict(d=d,t_d=str(t),E_d=str(E),H_at_t_d=str(H),old_uniform=str(uniform),precision=ctx.prec)

if __name__=='__main__':
    data={
      'method':'fractions.Fraction exact parameter/local inequalities; Decimal precision 100 for envelope comparisons',
      'limits':'Exact certificate checks do not enumerate all states. Decimal values are finite numerical evidence; analytic proof is in asymptotic_review.md. mpmath unavailable in both installed interpreters.',
      'original_candidate':[original_candidate(s) for s in [6,7,8]],
      'linear_reset':[exact_reset(*row) for row in [(2,F(1,3),F(113,100)),(3,F(1,3),F(13,10)),(4,F(1,3),F(3,2)),(10,F(1,4),F(5,2))]],
      'envelope':[decimal_envelope(d) for d in [2,3,4,10,100,1000,1000000]],
    }
    OUT.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'output':str(OUT),'original_count':len(data['original_candidate']),'linear_reset':[{k:r[k] for k in ['d','R','m','product_approx']} for r in data['linear_reset']],'envelope_count':len(data['envelope'])},indent=2))
