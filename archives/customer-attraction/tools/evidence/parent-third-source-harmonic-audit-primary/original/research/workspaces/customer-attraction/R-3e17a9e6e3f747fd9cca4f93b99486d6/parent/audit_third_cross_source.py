"""Independent audit of source-three first-follower requery with a real 3-tail.

No author modules are imported. It checks all 2048 six-player membership states
and separates the frozen 1269-row necessary-system point, not an SPE.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'astra/promotion_joint_atoms_exact.json'

def sh(n,d):return F(n,d) if n else F()

def evaluate(a,b,c,d,e,f):
    p=sum(a[:2]);ell=sum(a[:5]);z=a[5];s=sum(a);q=p+b;D=q+d+e+f
    u3=sh(a[2],s);u6=sh(z,s)
    source=sh(b,D);ud=sh(d,D);ue=sh(e,D);uf=sh(f,D)
    safe_c=F(c,q+3);final_c=F(c,q+d+e+1)
    # Direct relative harmonic potential for comparing the final two themes.
    bg=q+d
    phi=sum(F(1,bg+j) for j in range(1,c+z+1))
    tax=F(e,(bg+1)*(bg+2))
    pi=F(1,p+4);rho=F(1,ell+1)
    raw_without_K=(44*(u3-source)+(ud-safe_c)+7*(uf-final_c)
                   +2*(ue+uf+tax-phi)+6*(u6-rho*d)+7*(u6-rho*e)
                   +(u3-pi*f)+7*(u6-rho*f)-2*f)
    H=(sh(44*b-d-2*e-9*f,D)+F(c,q+3)+F(7*c,q+d+e+1)
       +F(2*(c+z),q+d+1)-F(2*(e+c*z),(q+d+1)*(q+d+2))
       +6*rho*d+7*rho*e+(pi+7*rho+2)*f)
    assert 45*u3+20*u6-H==raw_without_K
    return H,u3,u6

def main():
    minimum={};checks=0
    for a in product((0,1),repeat=6):
        for b,c in product((0,1),repeat=2):
            vals=[]
            for d,e,f in product((0,1),repeat=3):
                vals.append(evaluate(a,b,c,d,e,f)[0]);checks+=1
            minimum[a,b,c]=min(vals)
    point=json.loads(SOURCE.read_text());K=F(point['K']);masses=[F()]*len(point['histograms'])
    for atom in point['RZ_atoms']:masses[atom['hist_index']]+=F(atom['weight'])
    left=12*K;right=u3=u6=F();pattern=tuple(product((0,1),repeat=3))
    for mass,h in zip(masses,point['histograms']):
        a=tuple(map(int,h['actual_bits']));s=sum(a)
        u3+=mass*sh(a[2],s);u6+=mass*sh(a[5],s)
        for (t,b,c),n in zip(pattern,h['hist']):
            right+=mass*n*minimum[a,b,c]
    left+=6*(45*u3+20*u6)
    slack=left-right
    assert slack==F('-221864648049035706784770943603907738797155442953186912251327/1514504642612697146706405659586806517863314442493087646635684')
    assert slack<0
    report={'status':'EXACT_LOCAL_IDENTITY_AND_1269_POINT_SEPARATION','target_status':'OPEN',
            'raw_coefficient_states':checks,'projected_states':len(minimum),'weights':[44,1,7,2,6,7,1,7,2],
            'point_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'u3':str(u3),'u6':str(u6),'K':str(K),'lhs':str(left),'rhs':str(right),
            'slack':str(slack),'slack_divided_by_77':str(slack/77),
            'scope':'Universal nonnegative decomposition at a source with four remaining players, preserving all three real followers. Six-player finite coefficient audit and strict separation of a specified necessary point, not a half theorem or SPE counterexample.'}
    (HERE/'audit_third_cross_source.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
