"""Definition-level Fraction audit; does not claim the menu is an SPE."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent

def run(a,b):
    k=8;weights={}
    for i in range(k):weights[sum(1<<((i+j)%k) for j in range(3))]=a
    for i in range(4):weights[(1<<i)|(1<<(i+4))]=b
    assert len(weights)==12 and sum(weights.values())==8*a+4*b
    def pay(label,profile):
        return sum((F(w,sum(mask>>j&1 for j in profile)) for mask,w in weights.items() if mask>>label&1),F(0))
    def query(label,competitors):
        return sum((F(w,1+sum(mask>>j&1 for j in competitors)) for mask,w in weights.items() if mask>>label&1),F(0))
    def welfare(profile):return sum(w for mask,w in weights.items() if any(mask>>j&1 for j in profile))
    theta=F(10*b+23*a,16);d=F(b,2)+2*a;e2=F(b,2)+3*a;e3=b+2*a
    assert d<theta<=e2 and theta<e3
    menus=[]
    for i in range(k):
        z=(i,(i+4)%k,(i+1)%k);u=[pay(j,z) for j in z]
        assert u==[d,e2,e3]
        vals=[query(j,z[:2]) for j in range(k)]
        assert vals[z[-1]]==max(vals)==e3
        assert [j for j in range(k) if vals[j]==max(vals)]==[j for j in range(k) if j not in z[:2]]
        assert vals[i]==vals[(i+4)%k]==F(b,3)+F(3*a,2)
        assert welfare(z)==2*b+7*a
        menus.append(dict(root=i,terminal=z,payoffs=list(map(str,u)),last_query=list(map(str,vals))))
    static=list(combinations_with_replacement(range(k),3))
    means={q:sum((query(j,q) for j in range(k)),F(0))/k for q in static}
    assert len(static)==120 and min(means.values())==theta
    q0=(0,2,5);assert means[q0]==theta
    rotations=[tuple((j+s)%k for j in q0) for s in range(k)]
    assert all(sum((query(j,q) for q in rotations),F(0))/k==theta for j in range(k))
    for q in static:
        pairs=[sum(int(j in [i,i+4]) for j in q) for i in range(4)]
        triples=[sum(int(j in [i,(i+1)%k,(i+2)%k]) for j in q) for i in range(k)]
        assert sum(pairs)==3 and sum(triples)==9
        assert sum((F(1,1+c) for c in pairs),F(0))>=F(5,2)
        assert sum((F(1,1+c) for c in triples),F(0))>=F(23,6)
    pre=(0,2);vals=[query(j,pre) for j in range(k)];best=[j for j in range(k) if vals[j]==max(vals)]
    assert best==[5] and vals[5]==b+3*a
    dev=pay(2,(0,2,5));assert dev==b+F(5*a,2)>e2
    opt=max(welfare(q) for q in static);assert opt==3*b+8*a and welfare(q0)==opt
    assert 2*(2*b+7*a)>opt
    return dict(a=a,b=b,customers=sum(weights.values()),weights=weights,v4=str(theta),u=str(d),tail2=str(e2),tail3=str(e3),second_deviation=str(dev),last_after_deviation=str(vals[5]),OPT3=opt,menu_W=2*b+7*a,static_profiles=len(static),menus=menus,status='Exact menu boundary only; not a full SPE')

if __name__=='__main__':
    out=[run(1,5),run(4,50)]
    path=HERE/'last_br_threshold_menu_audit.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([{key:case[key] for key in ['a','b','customers','u','tail2','tail3','v4','second_deviation','OPT3','menu_W','status']} for case in out],indent=2))
