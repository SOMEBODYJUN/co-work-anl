"""Independent mathematical-entry audit of the shared-K 61-row dual.

No discovery/evaluator imports.  Reconstructs COPY-M's complete type residual,
the binary-background dependency from submitted multipliers and raw shares,
and the capacity/complement algebra. Full conditional pricing is a separate
reviewed implementation, whose output hash is recorded by the review.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/model.py').is_file())
ACTOR=HERE.parent
DUAL=ACTOR/'dual/exact_shared_root.json'
BINARY=ROOT/'research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent/binary_tail_exact_1999.json'
CG=ROOT/'research/workspaces/customer-attraction/R-a27734a8bba345cbb5fad186c120d0bf/root_shared_max_copy_cg.json'

def q(n,d):
    return F(n,d) if n else F(0)

def copy_check():
    residuals=[]
    # t,b2,b3,b4,b5,c,q are seven unrestricted binary memberships.
    for t,b2,b3,b4,b5,c,z in product((0,1),repeat=7):
        p=t+b2+b3; load=p+b4+b5; cload=p+b5+c
        r,v4,v5=q(t,load),q(b4,load),q(b5,load)
        L=v4-q(b5,cload)
        ZQ=v5-q(z,p+b4+1)
        ZC=v5-q(c,p+b4+1)
        CQ=q(c,cload)-q(z,p+b5+1)
        # Formal u and K coefficients cancel. Set both to zero to evaluate
        # target minus the explicit nonnegative-slack combination.
        target=-F(16,3)*t-q(z,1+4*t)
        paid=-F(44,3)*r-F(b2+b3,2)-F(11,15)*b4-F(13,15)*b5
        paid+=F(4,15)*L+F(14,15)*ZQ+F(2,15)*ZC+F(1,15)*CQ
        rho=target-paid
        assert rho>=0,(t,b2,b3,b4,b5,c,z,rho)
        residuals.append(rho)
    assert F(1,2)+F(1,2)+F(11,15)+F(13,15)==F(13,5)
    return {'complete_binary_membership_types':len(residuals),'minimum_residual':str(min(residuals)),
            'zero_types':sum(v==0 for v in residuals),'size_cap_coefficient':'13/5'}

def binary_check():
    cert=json.loads(BINARY.read_text());lam={n:F(v) for n,v in cert['multipliers'].items()}
    assert len(lam)==13 and min(lam.values())>=0
    a,b=F(cert['beta0']),F(cert['beta1']);assert (a,b)==(F(1999,1000),F(5,3))
    vals={};checks=0
    for p,bits,comparators in product((0,1),product((0,1),repeat=7),product((0,1),repeat=4)):
        labels=dict(zip('abcdqrs',bits));actual=bits[:4];off=(bits[3],)+bits[4:]
        def util(path,i):return q(path[i],p+sum(path))
        def safe(path,i,label):return util(path,i)-q(labels[label],p+sum(path[:i])+4-i)
        def optrow(path):return 4*util(path,3)-sum((q(t,p+sum(path[:3])+1) for t in comparators),F())
        def pairrow(path):
            pref=p+sum(path[:2]);H=util(path,2)+util(path,3)+q(path[2],(pref+1)*(pref+2))
            return sum((H-q(comparators[i]+comparators[j],pref+comparators[i]+comparators[j])
                        for i,j in combinations(range(4),2)),F())
        rows={}
        for name in lam:
            s=name.split(':')
            if name=='root-copy-d':v=util(actual,0)-util(off,0)
            elif s[-1]=='pair-opt':v=pairrow(actual if s[0]=='actual' else off)
            elif s[-1]=='sum-opt':v=optrow(actual if s[0]=='actual' else off)
            else:v=safe(actual if s[0]=='actual' else off,int(s[1]),s[-1])
            rows[name]=v
        e=sum(comparators);k=sum(actual)
        rho=(a if p==0 else b)*q(k,p+k)-q(e,p+e)-sum((lam[n]*rows[n] for n in lam),F())
        assert rho>=0,(p,bits,comparators,rho)
        key=p,bits,e
        assert key not in vals or vals[key]==rho
        vals[key]=rho;checks+=1
    assert len(vals)==1280 and sum(v==0 for v in vals.values())==19
    return {'raw_comparator_membership_checks':checks,'compressed_types':len(vals),'minimum_residual':str(min(vals.values())),
            'zero_compressed_types':sum(v==0 for v in vals.values()),'nonnegative_multipliers':len(lam)}

def capacity_check():
    integer=[]
    for c in range(1,6):
        gap=F(c)+F(20,c)-9
        assert gap==F((c-4)*(c-5),c)>=0
        integer.append(str(gap))
    compchecks=0
    for t,opt in product((0,1),product((0,1),repeat=5)):
        d=sum(opt)
        avg=sum((q(d-opt[i],t+d-opt[i]) for i in range(5)),F())/5
        assert avg>=F(4,5)*int(d>0)-F(2,5)*t
        compchecks+=1
    a,b=F(1999,1000),F(5,3)
    assert 750*(-4*a+b+F(2,5))==-4447
    assert 750*(20*a-b)==28735
    assert 750*F(4,5)==600
    assert (20*28735,20*600,20*4447)==(574700,12000,88940)
    return {'integer_loads_checked':5,'integer_gaps':integer,'raw_complement_assignments':compchecks,
            'derived_row':'574700 u - 12000 OPT_5 - 88940 K >= 0'}

def active_coefficients_check():
    cert=json.loads(DUAL.read_text());cg=json.loads(CG.read_text())
    weights={n:int(v) for n,v in cert['integer_multipliers'].items()}
    denominator=int(cert['common_denominator']);bn=int(cert['beta_numerator'])
    assert len(weights)==61 and min(weights.values())>0
    assert F(bn,denominator)==F(cert['dual_beta'])
    assert all(F(v,denominator)==F(cert['multipliers'][n]) for n,v in weights.items())
    kcols=dict(zip(cg['row_names'],map(F,cg['K_column'])))
    own={}
    for n in weights:
        own[n]=(F(1) if n.startswith('MAX:fixed:') else F(78) if n.startswith('KRS:fixed:') else F(-88940) if n=='KCAP:4' else F())
        assert own[n]==kcols[n],(n,own[n],kcols[n])
    kres=-sum((weights[n]*own[n] for n in weights),F())
    assert kres==0
    # The COPY row atom coefficient must agree with its 30-scaled theorem.
    checks=0
    for bits in product((0,1),repeat=10):
        load=sum(bits[:5]);u=q(bits[0],load)
        for i,j in ((3,4),(5,3)):
            t,z=bits[i],bits[j]
            direct=30*(F(44,3)*u-F(16,3)*t-z+F(4,5)*t*z)
            assert direct==440*u-160*t-30*z+24*t*z
            checks+=1
    return {'positive_multipliers':len(weights),'exact_beta':str(F(bn,denominator)),
            'K_coefficient_residual':str(kres),'copy_fixed_mask_checks':checks}

def main():
    out={'scope':'Independent mathematical-entry review for full-type shared-K 61-row certificate; not HALF(5)',
         'copy_128':copy_check(),'binary_tail_dependency':binary_check(),
         'capacity':capacity_check(),'certificate_coefficients':active_coefficients_check(),
         'inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (DUAL,BINARY,CG)}}
    HERE.joinpath('audit_shared_root_math.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
