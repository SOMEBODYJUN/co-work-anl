"""Independent raw-share audit of five_structure maximum-theme cuts.

No import of the structure author's audit or coefficient functions.
The binary-tail multipliers are read as submitted certificate data only.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[5]
CERT = ROOT / 'research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent/binary_tail_exact_1999.json'


def share(bit, load):
    return F(bit,load) if bit else F(0)


def main():
    cert=json.loads(CERT.read_text())
    multipliers={name:F(value) for name,value in cert['multipliers'].items()}
    assert len(multipliers)==13 and all(v>=0 for v in multipliers.values())
    minimum=None
    compressed_zeros=set()
    raw_zeros=0
    for old in (0,1):
        for bits in product((0,1),repeat=7):
            a,b,c,d,q,r,s=bits
            actual=(a,b,c,d)
            off=(d,q,r,s)
            u=[share(x,old+sum(actual)) for x in actual]
            z=[share(x,old+sum(off)) for x in off]
            for comparison in product((0,1),repeat=4):
                e=sum(comparison)
                rows={}
                for name,bit in zip('cdqrs',(c,d,q,r,s)):
                    rows['actual:1:K:'+name]=u[1]-F(bit,old+a+3)
                rows['actual:2:K:d']=u[2]-F(d,old+a+b+2)
                rows['actual:3:sum-opt']=4*u[3]-sum(F(t,old+a+b+c+1) for t in comparison)
                rows['off:1:K:c']=z[1]-F(c,old+d+3)
                rows['off:3:K:b']=z[3]-F(b,old+d+q+r+1)
                rows['off:3:sum-opt']=4*z[3]-sum(F(t,old+d+q+r+1) for t in comparison)
                rows['root-copy-d']=u[0]-z[0]
                for label,path,pay in [('actual',actual,u),('off',off,z)]:
                    bg=old+path[0]+path[1]
                    H=pay[2]+pay[3]+F(path[2],(bg+1)*(bg+2))
                    comparison_sum=F(0)
                    for pair in combinations(range(4),2):
                        count=sum(comparison[j] for j in pair)
                        comparison_sum+=share(count,bg+count)
                    rows[label+':pair-opt']=6*H-comparison_sum
                assert set(rows)==set(multipliers)
                G=sum(multipliers[name]*value for name,value in rows.items())
                target=(F(1999,1000) if old==0 else F(5,3))*sum(u)-share(e,old+e)
                residual=target-G
                assert residual>=0,(old,bits,comparison,residual)
                minimum=residual if minimum is None else min(minimum,residual)
                if residual==0:
                    raw_zeros+=1
                    compressed_zeros.add((old,bits,e))
    assert minimum==0 and len(compressed_zeros)==19

    # Integer load factorization, not a numerical extrapolation in c.
    for k in range(1,5):
        for c in range(1,6):
            difference=F(c)+F(k*(k+1),c)-(2*k+1)
            factor=F((c-k)*(c-k-1),c)
            assert difference==factor>=0

    # Omit each individually indexed comparison topic and compute raw shares.
    for membership in product((0,1),repeat=5):
        e=sum(membership)
        for inside in (0,1):
            total=F(0)
            for omit in range(5):
                count=e-membership[omit]
                total+=share(count,inside+count)
            lower=F(4,5)*bool(e)-F(2,5)*inside*bool(e)
            assert total/5>=lower
            if e:
                expected=(F(4,5) if e==1 else F(1)) if not inside else 1-F(6,5*(e+1))
                assert total/5==expected

    a,b=F(1999,1000),F(5,3)
    expected=[(1200,9097,3497),(1200,3100,15491),(1200,-2897,33482),(600,-4447,28735)]
    for k,(left,ks,us) in enumerate(expected,start=1):
        factor=F(left)/F(4,5)
        Kcoefficient=a*(4-2*k)+b+F(2,5)
        Ucoefficient=a*k*(k+1)-b
        assert Ucoefficient>0
        assert factor*Kcoefficient==ks and factor*Ucoefficient==us
    assert 3000*a==5997 and 3000*(b-a+F(2,5))==203 and 3000*b==5000

    O,u,K=F(83705,36641),F(8897,73282),F(16741,36641)
    assert F(1,5)*K<=u<=K<=1 and O<=5*K
    for left,ks,us in expected:
        assert left*O<=ks*K+us*u
    assert 2400*O<=5997-5000*u+203*K
    alpha,beta,gamma=F(66964000,73245359),F(5000000,73245359),F(641,36641)
    assert alpha>0 and beta>0 and gamma>0 and alpha+beta+gamma==1
    assert alpha*F(25,12)-beta*F(16741,600)==0
    assert -alpha*F(203,2400)+beta*F(2897,1200)-5*gamma==0
    assert alpha*F(5997,2400)==O
    report={'binary_raw_states':4096,'binary_raw_zero_residuals':raw_zeros,
            'binary_compressed_zero_residuals':len(compressed_zeros),'binary_min_residual':str(minimum),
            'capacity_integer_factors':20,'raw_complement_assignments':64,
            'all_four_integer_rows_verified':True,'scalar_dual':list(map(str,(alpha,beta,gamma))),
            'scalar_optimum':str(O),'conclusion':'independent exact audit passed; no half theorem'}
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
