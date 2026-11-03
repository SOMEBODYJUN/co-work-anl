"""Exact actual-third HQR cut with separable conditioned family blocks.

The coefficient is the maximum of eight weighted same-strategy raw-row
coefficients. At fixed HQR bits there are no cross-family products.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
HERE=Path(__file__).resolve().parent
STATES=list(product((0,1),repeat=3));LABELS='ABCDEUVWXY'


def share(n,d):return F(n,d) if n else F(0)
def count(a,tag,pos):
    field={'AB':'AB_hist','AE':'AE_hist','Sbranch':'second_hist'}[tag]
    return sum(n*t[pos] for n,t in zip(a[field],product((0,1),repeat=4 if tag=='Sbranch' else 3)))


def context(a):
    b=dict(zip(LABELS,map(int,a['bits'])));mb=tuple(map(int,a['max_bits']))
    return {'p':b['A']+b['B'],'u':share(b['C'],sum(b[t] for t in 'ABCDE')),
            'm':mb[0],'x':b['X'],'y':b['Y'],'z':mb[4],
            'd':sum(a['AB_hist'][4:]),'ab':count(a,'AB',2),'ae':count(a,'AE',2),
            'su':count(a,'Sbranch',1),'sv':count(a,'Sbranch',2),'sw':count(a,'Sbranch',3)}


def raw_blocks(c,state):
    """Return constant, AB, AE, Sbranch raw-row dictionaries.

    p,u,x,y are from fixed old bits; m,z from the original maximum path.
    d is common optimal multiplicity. Only one family's counts enter each
    family block. The true HQR tax pays every queried pair at this history.
    """
    p,u,m,x,y,z,d=(c[t] for t in ('p','u','m','x','y','z','d'));h,q,r=state;s=p+h+q+r
    Vh,Vq,Vr=(share(v,s) for v in (h,q,r));Htax=Vq+Vr+F(q,(p+h+1)*(p+h+2))
    def tax(a,b,na,nb):
        return na*nb*Htax-F(nb*a+na*b-2*a*b,p+h+1)-F(2*a*b,p+h+2)
    fixed={
        'trueH:source-IC':u-Vh,
        'trueH:weighted-cap:f1':F(h-q,p+3),
        'trueH:weighted-cap:f2':F(h-r,p+3),
        'trueH:R:K:opt':5*Vr-F(d,p+h+q+1),
        'trueH:global-size:0':F(m-h),
        'trueH:tax:X:Y':tax(x,y,1,1),
        'trueH:tax:Y:z4':tax(y,z,1,1),
    }
    ab={'AB:trueH:tax:mY:opt':tax(c['ab'],d,5,5)}
    ae={'AE:trueH:weighted-cap:mY':F(5*h-c['ae'],p+3)}
    sb={'Sbranch:trueH:tax:mU:X':tax(c['su'],x,5,1),
        'Sbranch:trueH:tax:mU:mV':tax(c['su'],c['sv'],5,5),
        'Sbranch:trueH:tax:mU:mW':tax(c['su'],c['sw'],5,5),
        'Sbranch:trueH:tax:mV:opt':tax(c['sv'],d,5,5)}
    return fixed,ab,ae,sb


def conditioned(c,state,weights):
    return sum((weights.get(n,0)*v for block in raw_blocks(c,state) for n,v in block.items()),F(0))


def coefficient(a,weights):
    c=context(a);return max(conditioned(c,s,weights) for s in STATES)


def recover():
    srcpath=HERE/'two_real_branches_exact_current_source_own_index_v1.json';src=json.loads(srcpath.read_text())
    original={n:F(v) for n,v in src['single_history_diagnostics']['actual']['exact_nonnegative_row_multipliers'].items()}
    pointpath=HERE/'exact_current_source_own_index_v1.json';point=json.loads(pointpath.read_text());atoms=point['atoms']
    candidates=[]
    for D in (1000,2000,5000,10000,20000,50000,100000,1000000):
        weights={n:round(v*D) for n,v in original.items() if round(v*D)>0}
        gap=sum((F(a['exact_mass'])*coefficient(a,weights) for a in atoms),F(0))
        candidates.append({'common_denominator':D,'negative_slack':str(gap),'negative_slack_float':float(gap)})
        if gap<0:break
    assert gap<0
    # Independent comparison with all full raw-row values, not just the
    # specialized formulas above, on every 63*8 source/hidden state.
    import two_real_weighted_branches as full
    checks=0
    for a in atoms:
        c=context(a)
        for state in STATES:
            expanded={n:v for block in raw_blocks(c,state) for n,v in block.items()}
            expected=full.rows(a,state,'actual')
            assert all(expanded[n]==expected[n] for n in original)
            checks+=len(original)
    report={'scope':'Universal actual-third selected-H true-QR projection. Exact nonnegative row weights, full eight-state maximum. Not a half certificate or game.',
            'source_exact_point_sha256':hashlib.sha256(pointpath.read_bytes()).hexdigest(),
            'nonnegative_integer_row_weights':weights,'common_denominator_approximation_used_only_for_discovery':D,
            'source_atoms':len(atoms),'full_hidden_states':STATES,'source_raw_coefficient_comparisons':checks,
            'exact_projection_slack':str(gap),'negative_slack_float':float(gap),
            'rounding_trials':candidates,'dependency_contract':{'fixed_old_bits':'ABCDE plus X,Y',
                 'maximum_path_bits':'m=max_bits[0], z=max_bits[4]',
                 'common_optimal_count':'d=sum AB_hist[t=1]',
                 'AB':'count mY, with d only','AE':'count mY only',
                 'Sbranch':'counts mU,mV,mW with products within Sbranch only'},
            'pricing_contract':'For positive new-row multiplier mu, max_types(old_score+mu*max_HQR raw_score)=max_HQR max_types(old_score+mu*raw_score). Condition on HQR; then all three family histograms still separate.',
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'actual13_projection.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report


if __name__=='__main__':recover()
