"""Independent standard-library audit of the fixed-policy iid-Nash dual."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def sigma(h):
    if len(h)==0:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    group=range(3) if h[1]<3 else range(3,6)
    return next(a for a in group if a not in h)


def end(h):
    h=tuple(h)
    while len(h)<3:h+=sigma(h),
    return h


def payoff_coefficient(T,a,z):
    if not (T>>a&1):return F(0)
    return F(1,sum(T>>b&1 for b in z))


if __name__=='__main__':
    cert=json.loads((Path(__file__).resolve().parents[2]/'evidence/certificates/customer_attraction/iid_security_conditional_36.json').read_text())
    assert cert['n']==3 and cert['m']==6
    q=list(map(F,cert['q']));assert sum(q)==1 and all(x>=0 for x in q)
    hs=[h for k in range(3) for h in product(range(6),repeat=k)]
    assert len(hs)==43
    z=end(())
    found=[]
    for T in range(1,64):
        t=sum(q[a] for a in range(6) if T>>a&1)
        psi=1-(1-t)**3
        g=F(1) if t==0 else psi/(3*t)
        c=F(any(T>>a&1 for a in z))
        total=F(0)
        for row in cert['sparse_spe']:
            h=tuple(row['history']);a=row['deviation'];lam=F(row['lambda'])
            assert h in hs and a in range(6) and lam>=0
            total+=lam*(payoff_coefficient(T,sigma(h),end(h))-
                        payoff_coefficient(T,a,end(h+(a,))))
        for row in cert['sparse_ne']:
            a=row['action'];lam=F(row['lambda']);assert lam>=0
            total+=lam*(psi-3*g*(T>>a&1))
        r=c-psi-total
        assert r>=0,(T,r)
        assert r==F(cert['residuals'].get(str(T),'0'))
        found.append(r)
    # Original 36 customer weights: 9 cross pairs of mass 1 and 9 four-sets of mass 3.
    weights={}
    for T in range(1,64):
        kx=(T&7).bit_count();ky=(T>>3).bit_count()
        if kx==ky==1:weights[T]=1
        if kx==ky==2:weights[T]=3
    w=sum(weights.values());assert w==36
    W=sum(v for T,v in weights.items() if any(T>>a&1 for a in z))
    Psi=sum(F(v)*(1-(1-F(T.bit_count(),6))**3) for T,v in weights.items())
    assert W==34 and Psi==F(97,3)
    root_u=sum(F(v)*payoff_coefficient(T,z[0],z) for T,v in weights.items())
    assert root_u==10 and root_u<Psi/3
    def phi(profile):
        return sum(F(w)*sum((F(1,k) for k in range(1,sum(T>>a&1 for a in profile)+1)),F(0))
                   for T,w in weights.items())
    def utility(a,profile):
        return sum(F(w)*payoff_coefficient(T,a,profile) for T,w in weights.items())
    slacks=[];deletion_differences=[]
    for i in range(3):
        s=F(0);d=F(0)
        for h in product(range(6),repeat=i):
            prob=F(1,6**i);zh=end(h)
            deleted=zh[:i]+zh[i+1:]
            s+=prob*utility(sigma(h),zh)
            d+=prob*phi(deleted)
            for a in range(6):
                za=end(h+(a,));deleted_a=za[:i]+za[i+1:]
                s-=prob*q[a]*utility(a,za)
                d-=prob*q[a]*phi(deleted_a)
        slacks.append(s);deletion_differences.append(d)
    iid_phi=sum(F(1,6**3)*phi(profile) for profile in product(range(6),repeat=3))
    harmonic_excess=phi(z)-W
    iid_excess=iid_phi-Psi
    residual=sum(deletion_differences)-harmonic_excess+iid_excess
    assert slacks==[F(0),F(1,2),F(31,18)]
    assert sum(slacks)==F(20,9)
    assert residual==F(-5,9)
    assert W-Psi==sum(slacks)+residual
    out={'fraction_dual_valid':True,'customer_columns':63,'spe_rows':len(cert['sparse_spe']),
         'stationarity_rows':len(cert['sparse_ne']),'minimum_residual':str(min(found)),
         'original36':{'W':W,'iid_Nash_expected_coverage':str(Psi),
                       'root_utility':str(root_u),'individual_iid_benchmark_fails':True},
         'iid_prefix_tree_flow':{'level_slacks':list(map(str,slacks)),
                                'sum_slacks':str(sum(slacks)),
                                'deletion_potential_differences':list(map(str,deletion_differences)),
                                'root_harmonic_excess':str(harmonic_excess),
                                'iid_harmonic_excess':str(iid_excess),
                                'residual':str(residual),
                                'compensated_budget':str(W-Psi),
                                'fixed_iid_prefix_multiplier_certificate_fails':True}}
    print(json.dumps(out,indent=2))
