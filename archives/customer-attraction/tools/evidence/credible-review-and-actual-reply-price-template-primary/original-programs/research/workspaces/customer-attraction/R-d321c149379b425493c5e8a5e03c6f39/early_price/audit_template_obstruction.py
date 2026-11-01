"""Exact identity and three-customer separation audit, independent of LP."""
import itertools,json
from fractions import Fraction as F
from pathlib import Path

def share(p,a,b):return F(a,p+a+b) if a else F()
def rho(p,a,b,d,e,tau,t,s,l):
    P=F(p,p+a+b) if p else F();beta=share(p,b,a);D=(p+1)*(p+2)
    return P+(1-t-l)*beta-min(F(1),d)+d/F(p+1)+(t/tau)*e/F(p+a+1)-(s/tau)*d*e/F(D)-(1-s)*e/F(p+1)+(1-s)*tau*b/F(p+1)-(1-s)*b*d/F(D)+l*a/F(p+2)

def main():
    checks=0
    for p,a,b in itertools.product(range(8),range(2),range(2)):
        for z in [(F(1),),(F(1,3),F(2,3)),(F(1),F(1)),(F(1,2),)*3]:
            tau=sum(z)
            for bits in itertools.product(range(2),repeat=2*len(z)):
                qs=bits[:len(z)];rs=bits[len(z):];d=sum(w*x for w,x in zip(z,qs));e=sum(w*x for w,x in zip(z,rs));h=sum(w*x*y for w,x,y in zip(z,qs,rs));D=(p+1)*(p+2);alpha=share(p,a,b);beta=share(p,b,a)
                U=lambda x,y:F(x,p+1+y)
                S=tau*alpha-sum(w*U(x,y) for w,x,y in zip(z,qs,rs));Z=tau*beta-sum(w*U(y,a) for w,y in zip(z,rs));V=sum(w*v*(U(y,x)-U(yy,x)) for w,x,y in zip(z,qs,rs) for v,yy in zip(z,rs));H=sum(w*(U(y,x)-U(b,x)) for w,x,y in zip(z,qs,rs));L=beta-U(a,1)
                assert S==tau*alpha-d/F(p+1)+h/F(D)
                assert Z==tau*beta-e/F(p+a+1)
                assert V==(d*e-tau*h)/F(D)
                assert H==e/F(p+1)-h/F(D)-tau*b/F(p+1)+b*d/F(D)
                for t,s,l in [(F(),F(),F()),(F(2,3),F(3,5),F(1,7))]:
                    G=S+t/tau*Z+s/tau*V+(1-s)*H+l*L
                    P=F(p,p+a+b) if p else F();target=P+beta-min(F(1),d)+tau*alpha
                    assert target-G==rho(p,a,b,d,e,tau,t,s,l);checks+=1
    # Both sides are affine in all three parameters; these four points prove
    # their coefficient identities exactly, not by sampling a continuous range.
    for t,s,l in [(F(),F(),F()),(F(1),F(),F()),(F(),F(1),F()),(F(),F(),F(1))]:
        R=[rho(*q,F(1),t,s,l) for q in [(0,0,1,F(1),F(1)),(0,1,0,F(1),F(1)),(3,1,1,F(1),F())]]
        assert R==[F(1,2)-l,(t+s+l)/2-1,F(1,4)-(t+s)/5]
        assert R[0]/8+R[1]/4+5*R[2]/8==F(-1,32)
    out={'status':'exact restricted-template obstruction; not an SPE counterexample','identity_instances':checks,'three_residue_affine_coefficient_checks':4,'separation':'rho_I/8+rho_II/4+5*rho_III/8=-1/32'}
    Path(__file__).with_name('template_obstruction_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
