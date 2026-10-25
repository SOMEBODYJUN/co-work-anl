"""Independent n5 two-prefix audit from original profit slack expansion."""
from fractions import Fraction as F
from itertools import product,combinations
from math import comb
from pathlib import Path
import json


def share(a,n):return F(a,n) if a else F(0)


def rho3(p,v,q,r,j,l):
    a,b,c=v; k=sum(v)
    aa,bb,cc=[share(z,p+k) for z in v]
    G=(29*aa+36*bb+57*cc-F(6*q+9*r,p+3)
       -F(17*j+2*l,p+a+b+1)-F(12*j,p+a+1)
       +F(4*j*l,(p+a+1)*(p+a+2))
       -14*share(c,p+c+q+r)+3*share(r,p+c+q+r)-F(j,p+c+q+1))
    return F(5,3)*share(k,p+k)-share(j,p+j)-G/30


def main():
    vs=list(product((0,1),repeat=3)); table={}; count=0
    for p,v,j in product(range(3),vs,range(4)):
        vals=[rho3(p,v,q,r,j,l) for q,r,l in product((0,1),(0,1),range(4))]
        assert min(vals)>=0
        table[p,v,j]=min(vals);count+=len(vals)
    def profile(p,v,j):
        return sum(comb(j,d)*comb(5-j,3-d)*(share(d,p+d)+table[p,v,d])
                   for d in range(4) if d<=j and 3-d<=5-j)
    gm={}
    for p in (1,2):
        vals={(v,j):(int(j>0)-profile(p,v,j)/6)*F(p+sum(v),p)
              for v,j in product(vs,range(6))}
        gm[p]=max(vals.values())
        assert gm[p]==(F(401,540) if p==1 else F(59,72))
    identities=0
    for p,v,ts in product(range(3),vs,product((0,1),repeat=5)):
        j=sum(ts); k=sum(v);o=int(j>0)
        expanded=sum(share(sum(ts[i] for i in ix),p+sum(ts[i] for i in ix))
                     +table[p,v,sum(ts[i] for i in ix)] for ix in combinations(range(5),3))
        assert expanded==profile(p,v,j)
        Pold=share(p,p+k); tail=share(k,p+k); w=int(p+k>0)
        D=F(59,72)*Pold-o+expanded/6
        assert D>=0
        assert F(25,9)*tail+o-expanded/6==F(25,9)*w-F(47,24)*Pold-D
        identities+=1
    author=json.loads((Path(__file__).parent.parent/'induction/audit_two_prefix_interface.json').read_text())
    assert all(str(x)==author['r3_minima'][str(p)+':'+''.join(map(str,v))+':'+str(j)]
               for (p,v,j),x in table.items())
    out={'status':'pass','scope':'complete local retained-remainder and subset audit; conditional half only',
         'original_slack_states':count,'minimum_entries':len(table),'indexed_subset_identity_states':identities,
         'gamma_by_p':{str(p):str(z) for p,z in gm.items()},
         'prefix_coefficient':'47/24','simple_half_threshold':'56/141',
         'author_table_agreement':True}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':main()
