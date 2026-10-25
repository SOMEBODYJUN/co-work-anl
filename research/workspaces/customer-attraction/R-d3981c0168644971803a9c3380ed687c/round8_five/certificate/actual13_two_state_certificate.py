"""Independent exact q/r elimination for the 13-row actual-source cut.

The 3*2*6 core table covers all background/selected-H/optimal counts. Every
one of its four q/r alternatives is checked with Fraction.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
HERE=Path(__file__).resolve().parent


def share(n,d):return F(n,d) if n else F(0)


def core(p,h,d,q,r):
    return (share(-8251*h+983*q+1808*r,p+h+q+r)
            +F(983*q,(p+h+1)*(p+h+2))-F(4703*q,p+3)-F(5446*r,p+3)
            -F(165*d,p+h+q+1)+F(14774*h,p+3)-307*h)


THETA={(p,h,d):max(core(p,h,d,q,r) for q,r in product((0,1),repeat=2))
       for p in range(3) for h in (0,1) for d in range(6)}


def costs(c):
    pairs=[(c['x'],c['y'],1,1,92),(c['y'],c['z'],1,1,66),
           (c['ab'],c['d'],5,5,2),(c['su'],c['x'],5,1,15),
           (c['su'],c['sv'],5,5,7),(c['su'],c['sw'],5,5,17),
           (c['sv'],c['d'],5,5,4)]
    C1=sum(w*(nb*a+na*b-2*a*b) for a,b,na,nb,w in pairs)
    C2=sum(w*2*a*b for a,b,na,nb,w in pairs)
    return C1,C2


def conditioned(c,h):
    p=c['p'];d=c['d'];C1,C2=costs(c)
    return (8251*c['u']+307*c['m']-F(925*c['ae'],p+3)
            -F(C1,p+h+1)-F(C2,p+h+2)+THETA[p,h,d])


def hinge(c):
    p=c['p'];d=c['d'];C1,C2=costs(c)
    return (conditioned(c,0)
            +max(F(0),THETA[p,1,d]-THETA[p,0,d]+F(C1,(p+1)*(p+2))+F(C2,(p+2)*(p+3))))


def certify():
    residuals={}
    for (p,h,d),value in THETA.items():
        for q,r in product((0,1),repeat=2):
            gap=value-core(p,h,d,q,r);assert gap>=0
            residuals[f'{p},{h},{d},{q},{r}']=str(gap)
    import actual13_projection as original
    srcpath=HERE/'actual13_projection.json';src=json.loads(srcpath.read_text());weights=src['nonnegative_integer_row_weights']
    assert sum(weights[n]*na*nb for n,na,nb in [
        ('trueH:tax:X:Y',1,1),('trueH:tax:Y:z4',1,1),('AB:trueH:tax:mY:opt',5,5),
        ('Sbranch:trueH:tax:mU:X',5,1),('Sbranch:trueH:tax:mU:mV',5,5),
        ('Sbranch:trueH:tax:mU:mW',5,5),('Sbranch:trueH:tax:mV:opt',5,5)])==983
    pointpath=HERE/'exact_current_source_own_index_v1.json';point=json.loads(pointpath.read_text());comparisons=0;gap=F(0)
    for a in point['atoms']:
        c=original.context(a)
        for h in (0,1):
            value=conditioned(c,h)
            exact=max(original.conditioned(c,(h,q,r),weights) for q,r in product((0,1),repeat=2))
            assert value==exact;comparisons+=1
        full=max(conditioned(c,h) for h in (0,1))
        assert full==original.coefficient(a,weights)==hinge(c)
        gap+=F(a['exact_mass'])*full
    assert gap==F(src['exact_projection_slack'])<0
    report={'scope':'Exact reduction of the universal actual13 eight-state projection to two selected-H states. No new assumption or half certificate.',
            'theta_table':{f'{p},{h}':[str(THETA[p,h,d]) for d in range(6)] for p in range(3) for h in (0,1)},
            'complete_core_domain':{'p':[0,1,2],'h':[0,1],'d':list(range(6)),'qr':list(product((0,1),repeat=2))},
            'exact_core_residuals':residuals,'core_states_checked':len(residuals),
            'source_conditioned_comparisons':comparisons,'same_exact_projection_slack':str(gap),
            'integer_tax_budget_coefficient':983,
            'universal_algebraic_identity':'G=fixed_common-C1/(p+h+1)-C2/(p+h+2)+core(p,h,d,q,r); raw family costs contain h but neither q nor r.',
            'source_certificate_sha256':hashlib.sha256(srcpath.read_bytes()).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'actual13_two_state_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='exact_core_residuals'},indent=2))


if __name__=='__main__':certify()
