"""Independent exact reconstruction of the five aggregate root-D payment.

Uses only the historical rational source atoms, and does not import the discovery
LP or any SPE solver. The proof is in root_D_payment.md.
"""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[6]
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
T3=list(itertools.product((0,1),repeat=3))
T4=list(itertools.product((0,1),repeat=4))
ALPHA,GAMMA,BETA,DELTA,EPSILON=F(79,100),F(1,20),F(13,100),F(2,125),F(3,200)

def share(n,d):
    if not n:return F(0)
    assert d>0
    return F(n,d)

def features(atom):
    a,b,c,d,e,u,v,w,x,y=map(int,atom['bits'])
    root=share(a,a+b+c+d+e)
    kae=cae=kh=ch=F(0)
    for count,(tt,rr,ss) in zip(atom['AE_hist'],T3):
        kae+=count*share(rr,a+e+tt+rr+ss)
        cae+=count*F(1,a+e+tt+2)
    for count,(tt,hh,ii,jj) in zip(atom['second_hist'],T4):
        kh+=count*share(hh,a+tt+hh+ii+jj)
        ch+=count*F(1,a+tt+3)
    return root,kae,cae,kh,ch,d,e

def projected(z,n,i):
    root,kae,cae,kh,ch,d,e=z
    return ((ALPHA+BETA)*root+3*DELTA*kae+EPSILON*kh
            +share(-ALPHA*d+GAMMA*i,d+n+i)
            -share(GAMMA*e,d+n+1)-DELTA*n*cae
            -(BETA/F(5)+EPSILON*ch)*i)

def original(z,f,g,h,i):
    root,kae,cae,kh,ch,d,e=z
    total=d+f+g+h+i
    slacks=(root-share(d,total),
            share(i,total)-share(e,d+f+g+h+1),
            root-F(i,5),
            3*kae-(f+g+h)*cae,
            kh-i*ch)
    return sum(q*s for q,s in zip((ALPHA,GAMMA,BETA,DELTA,EPSILON),slacks))

def main():
    source=json.loads(SOURCE.read_text())['primal']
    atom_audit=[];gap=F(0);states=0
    assert all(x>=0 for x in (ALPHA,GAMMA,BETA,DELTA,EPSILON))
    for atom in source['atoms']:
        z=features(atom)
        # Exactly reconstruct the literal five nonnegative aggregate rows.
        original_values=[]
        for f,g,h,i in itertools.product((0,1),repeat=4):
            lhs=original(z,f,g,h,i)
            assert lhs==projected(z,f+g+h,i)
            original_values.append(lhs);states+=1
        choices=[(projected(z,n,i),n,i) for n in range(4) for i in range(2)]
        value,n,i=max(choices)
        assert value==max(original_values)
        mass=F(int(atom['mass_numerator']),int(source['denominator']))
        gap+=mass*value
        atom_audit.append({'max':str(value),'n':n,'last':i})
    assert gap<0
    # The identity itself only uses d,e,n,i and five symbolic old features.
    # Check their five affine basis directions for every binary d,e,16 replies.
    algebra_cases=0
    for d,e in itertools.product((0,1),repeat=2):
        for basis in [tuple(F(int(j==k)) for j in range(5)) for k in range(5)]+[(F(0),)*5]:
            z=(*basis,d,e)
            for f,g,h,i in itertools.product((0,1),repeat=4):
                assert original(z,f,g,h,i)==projected(z,f+g+h,i)
                algebra_cases+=1
    out={'status':'Exact nonnegative-slack envelope and historical-point exclusion; no half or SPE counterexample claim',
         'weights':dict(zip(('alpha','gamma','beta','delta','epsilon'),map(str,(ALPHA,GAMMA,BETA,DELTA,EPSILON)))),
         'source_atoms':len(atom_audit),'source_membership_cases':states,'affine_identity_cases':algebra_cases,
         'exact_projected_gap':str(gap),'approx_projected_gap':float(gap),'per_atom':atom_audit}
    (HERE/'audit_root_D_payment.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='per_atom'},indent=2))

if __name__=='__main__':main()
