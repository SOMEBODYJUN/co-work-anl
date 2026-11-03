"""Independent exact checks for nonnegative shared-incidence loss.

No imports from the discovery/transport evaluator. Finite checks accompany
but do not replace the arbitrary-q algebra in shared_incidence_loss.md.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations
import json,hashlib
HERE=Path(__file__).resolve().parent;ACTOR=HERE.parent

def top(v,k):return sum(sorted(v,reverse=True)[:k],F(0))

def loss(d,tuples,weights):
    n=len(d);counts=[sum(z[j] for z in tuples) for j in range(len(weights))]
    scores=[sum(w*b for w,b in zip(weights,z)) for z in tuples]
    separate=sum((w*top(d,k) for w,k in zip(weights,counts)),F(0))
    joint=sum((a*b for a,b in zip(sorted(d,reverse=True),sorted(scores,reverse=True))),F(0))
    ds=sorted(d,reverse=True);layers=[]
    for r in range(1,n):
        bracket=sum(w*min(k,r) for w,k in zip(weights,counts))-top(scores,r)
        assert bracket>=0
        layers.append((ds[r-1]-ds[r])*bracket)
    assert separate-joint==sum(layers,F(0))
    return separate-joint

def generic_checks():
    count=0
    for q in range(1,5):
        d=[F(1,j+1) for j in range(q)]
        for tuples in product(tuple(product((0,1),repeat=3)),repeat=q):
            loss(d,tuples,(F(1),F(2),F(3)));count+=1
            transformed=[(z[0],1-z[1],z[2]) for z in tuples]
            loss(d,transformed,(F(3),F(1),F(2)));count+=1
    trapezoids=0
    for q in range(1,11):
        for k,l in product(range(q+1),repeat=2):
            for h in range(max(0,k+l-q),min(k,l)+1):
                u=k+l-h
                for r in range(q+1):
                    delta=min(k,r)+min(l,r)-min(h,r)-min(u,r)
                    assert delta==max(0,min(r-h,k-h,l-h,u-r))
                    trapezoids+=1
    return count,trapezoids

def family(atom,label):
    arity=4 if label=='second' else 3
    return [bits for bits,n in zip(product((0,1),repeat=arity),atom[label+'_hist']) for _ in range(n)]

def atom_check(atom):
    a,b,*_=map(int,atom['bits']);src=family(atom,'AB');tar=family(atom,'second');q=len(src)
    assert q==len(tar)
    own=F(0);D=F(0);singles=[F(0),F(0)];joint=F(0);gap=F(0);brute=F(0)
    K=[sum(z[j] for z in tar) for j in (2,3)]
    for t in (0,1):
        source=[z for z in src if z[0]==t];target=[z for z in tar if z[0]==t]
        d=[F(1,a+b+z[0]+z[1]+1) for z in source]
        own+=sum((F(z[2],a+b+z[0]+z[1]+1) for z in source),F(0));D+=sum(d,F(0))
        k,l=[sum(z[j] for z in target) for j in (2,3)];h=sum(z[2]*z[3] for z in target);u=k+l-h
        s=[z[2]+z[3] for z in target]
        singles[0]+=top(d,k);singles[1]+=top(d,l)
        joint+=sum((x*y for x,y in zip(sorted(d,reverse=True),sorted(s,reverse=True))),F(0))
        gap+=loss(d,[(z[2],z[3]) for z in target],(F(1),F(1)))
        r=sum(z[1]==0 for z in source);p=a+b+t
        assert top(d,k)+top(d,l)-top(d,h)-top(d,u)==F(max(0,min(r-h,k-h,l-h,u-r)),(p+1)*(p+2))
        brute+=max((sum((x*y for x,y in zip(d,perm)),F(0)) for perm in set(permutations(s))),default=F(0))
    base=[(q-1)*own-K[j]*D for j in range(2)]
    assert joint==brute
    values=[singles[j]+base[j] for j in range(2)]
    combined=joint+sum(base,F(0))
    assert sum(values,F(0))-combined==gap
    return values,combined,gap

def exact_point():
    path=ACTOR/'round5_pricing/exact_optimum_primal_terminal_cross.json';doc=json.loads(path.read_text());s=[F(0),F(0)];joint=F(0);gap=F(0)
    for atom in doc['atoms']:
        v,j,g=atom_check(atom);m=F(atom['exact_mass'])
        for n in range(2):s[n]+=m*v[n]
        joint+=m*j;gap+=m*g
    assert min(s)>0 and joint<0 and sum(s,F(0))-joint==gap
    return {'source_path':str(path.relative_to(ACTOR)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'atom_count':len(doc['atoms']),'separate_slacks':list(map(str,s)),'joint_slack':str(joint),'joint_slack_float':float(joint),'shared_incidence_loss':str(gap),'literal_permutation_maximum_checks':len(doc['atoms'])}

if __name__=='__main__':
    g,t=generic_checks();point=exact_point()
    report={'scope':'Exact algebra checks and one necessary-condition-point exclusion; no general welfare bound','generic_weighted_three_menu_loss_checks':g,'two_menu_trapezoid_checks':t,'point':point}
    (HERE/'shared_incidence_loss_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
