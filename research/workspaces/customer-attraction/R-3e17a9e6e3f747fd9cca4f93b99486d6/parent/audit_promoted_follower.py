"""Independent Fraction audit of same-source first-follower promotion.

No imports from the author's discovery or coefficient implementation.  This
checks a local identity for the complete six-player coefficient domain, then
separates a frozen necessary-condition point.  That point is not an SPE.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'

def share(bit,load):
    return F(bit,load) if bit else F(0)

def data(a,b,c,d,e):
    p=sum(a[:3]); ell=sum(a[:5]); z=a[5]; full=sum(a)
    q=p+b; den=q+d+e
    r=share(a[3],full); v=share(z,full)
    branch_source=share(b,den)
    tail_d=share(d,den); tail_e=share(e,den)
    queried_c=share(c,q+d+c)
    # Direct two-theme relative harmonic potential, not welfare of incumbents.
    potential=sum(F(1,q+j) for j in range(1,c+z+1))
    tax=F(d,(q+1)*(q+2))
    prices=(F(d,ell+1),F(e,ell+1))
    # Capacity is represented by a formal K column, with per-customer -e.
    raw_without_K=(35*(r-branch_source)+11*(tail_e-queried_c)
                   +3*(tail_d+tail_e+tax-potential)
                   +10*(v-prices[0])+12*(v-prices[1])-3*e)
    H=(share(35*b-3*d-14*e,den)+F(11*c,q+d+1)
       +F(3*(c+z),q+1)-F(3*(d+c*z),(q+1)*(q+2))
       +F(10*d+12*e,ell+1)+3*e)
    assert 35*r+22*v-H==raw_without_K
    return H,r,v

def main():
    count=0
    minima={}
    for a in product(range(2),repeat=6):
        for b,c in product(range(2),repeat=2):
            choices=[]
            for d,e in product(range(2),repeat=2):
                H,_,_=data(a,b,c,d,e);choices.append(H);count+=1
            minima[a,b,c]=min(choices)
    source=json.loads(SOURCE.read_text());K=F(source['columns'][0]['weight'])
    pattern=tuple(product(range(2),repeat=3))
    u4=u6=rhs=F(); mass=F(); terms=0
    for entry in source['columns']:
        if entry['kind']!='hist' or not F(entry['weight']):continue
        weight=F(entry['weight']);a=tuple(map(int,entry['actual_bits']));h=entry['hist']
        assert sum(h)==6
        mass+=weight
        u4+=weight*share(a[3],sum(a));u6+=weight*share(a[5],sum(a))
        for (t,b,c),multiplicity in zip(pattern,h):
            if multiplicity:
                rhs+=weight*multiplicity*minima[a,b,c];terms+=1
    lhs=6*(35*u4+22*u6+3*K)
    gap=lhs-rhs
    assert gap<0
    expected=F('-69927133130576238991444255183583899/1607441918183324070591516176771697440')
    assert gap/74==expected
    out={'status':'EXACT_LOCAL_IDENTITY_AND_SPECIFIED_POINT_SEPARATION',
         'target_status':'OPEN','coefficient_states':count,'projected_states':len(minima),
         'point_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
         'point_file':str(SOURCE.relative_to(ROOT)),'positive_histogram_terms':terms,
         'u4':str(u4),'u6':str(u6),'K':str(K),'lhs':str(lhs),'rhs':str(rhs),
         'slack':str(gap),'normalized_slack':str(gap/74),
         'scope':'Local finite coefficient identity for all six-player membership types, not sampled customers. Frozen 3889-row necessary point separated, not a game or SPE. No half theorem or counterexample.'}
    (HERE/'audit_promoted_follower.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
