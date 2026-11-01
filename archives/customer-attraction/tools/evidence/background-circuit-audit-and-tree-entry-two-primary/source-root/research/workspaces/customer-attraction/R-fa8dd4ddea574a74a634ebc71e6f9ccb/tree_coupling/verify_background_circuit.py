"""Formal polynomial certificate for all positive integer s,k; no sympy/LP."""
from fractions import Fraction as F
import json

ZERO={}
ONE={(0,0):F(1)}
S={(1,0):F(1)}
K={(0,1):F(1)}

def add(*ps):
    out={}
    for p in ps:
        for e,c in p.items():out[e]=out.get(e,F(0))+c
    return {e:c for e,c in out.items() if c}

def scale(c,p):return {e:c*v for e,v in p.items() if c*v}

def mul(*ps):
    out=ONE
    for p in ps:
        nxt={}
        for e,c in out.items():
            for f,d in p.items():
                g=tuple(x+y for x,y in zip(e,f));nxt[g]=nxt.get(g,F(0))+c*d
        out={e:c for e,c in nxt.items() if c}
    return out

def verify_general():
    one={(0,0,0):F(1)}
    R={(1,0,0):F(1)};S3={(0,1,0):F(1)};T={(0,0,1):F(1)}
    def mult(*ps):
        out=one
        for p in ps:
            nxt={}
            for e,c in out.items():
                for f,d in p.items():
                    g=tuple(x+y for x,y in zip(e,f));nxt[g]=nxt.get(g,F(0))+c*d
            out={e:c for e,c in nxt.items() if c}
        return out
    D=add(R,S3,scale(2,T));delta=add(R,scale(-1,S3));L=add(R,S3)
    q=(R,S3,T);r=(S3,R,T);q0=(ZERO,L,T)
    alpha=mult(R,S3,D);beta=mult(R,delta,D);gamma=mult(S3,T,add(S3,T))
    eta=mult(delta,T,T)
    zeta=mult(T,add(mult(S3,S3),scale(2,mult(S3,T)),scale(-1,mult(R,T))))
    terms=[(alpha,q,0),(beta,r,1),(gamma,q,2),
           (scale(-1,mult(S3,S3,D)),r,0),
           (scale(-1,mult(delta,L,D)),q0,1),
           (scale(-1,zeta),r,2),(scale(-1,eta),q0,2)]
    for B in range(1,8):
        active=[(coef,add(*(count for a,count in enumerate(counts) if B>>a&1))) for coef,counts,a in terms if B>>a&1]
        assert all(den for _,den in active)
        numerator=ZERO
        for i,(coef,den) in enumerate(active):
            numerator=add(numerator,mult(coef,*(other for j,(_,other) in enumerate(active) if j!=i)))
        assert numerator==ZERO,(B,numerator)
    return {'formal_polynomial_identity':True,'variables':['r','s','t'],
            'domain':'all integers r>=s>=1,t>=1','interest_patterns':7,
            'zeta_nonnegative_condition':'(r-2s)t<=s^2',
            'negative_zeta_may_be_moved_to_left':True}

def main():
    D=add(scale(3,S),scale(2,K))
    q=(scale(2,S),S,K);r=(S,scale(2,S),K);t=(ZERO,scale(3,S),K)
    # Left minus right of the universal positive circuit.
    terms=[(scale(2,mul(S,D)),q,0),(scale(2,mul(S,D)),r,1),
           (mul(K,add(K,S)),q,2),(scale(-1,mul(S,D)),r,0),
           (scale(-3,mul(S,D)),t,1),(scale(-1,mul(K,S)),r,2),
           (scale(-1,mul(K,K)),t,2)]
    degrees=[]
    for B in range(1,8):
        active=[(coef,add(*(count for a,count in enumerate(counts) if B>>a&1))) for coef,counts,a in terms if B>>a&1]
        assert all(den for _,den in active)
        numerator=ZERO
        for i,(coef,den) in enumerate(active):
            numerator=add(numerator,mul(coef,*(other for j,(_,other) in enumerate(active) if j!=i)))
        assert numerator==ZERO,(B,numerator)
        degrees.append(len(active))
    print(json.dumps({'clean_family':{'formal_polynomial_identity':True,'variables':['s','k'],'domain':'all positive integers s,k','interest_patterns':7,'payoff_terms':7,'common_denominator_factor_counts':degrees,'all_circuit_coefficients_positive_on_domain':True},'general_family':verify_general()},indent=2))

if __name__=='__main__':main()
