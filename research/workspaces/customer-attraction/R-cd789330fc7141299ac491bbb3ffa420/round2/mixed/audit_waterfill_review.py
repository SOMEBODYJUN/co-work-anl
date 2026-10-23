"""Independent exact review of the waterfill sharpness packet.

Reads only the input/strategy packet and frozen interval data, never the
author audit, builder, canonical model, or SPE solver.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
TAIL=HERE.parent/'tail'
T0=F(28481,2924)
DEFICIT=F(647,8772)


def main():
    instance=json.loads((TAIL/'endogenous_53_instance.json').read_text())
    packet=json.loads((TAIL/'endogenous_53_strategy.json').read_text())
    n=len(instance['topics'])
    assert n==7 and instance['topics']==['X0','X1','X2','Y0','Y1','Y2','P']
    clients=[]
    types=Counter()
    for row in instance['customers']:
        likes=frozenset(row['topics'])
        types[sum(1<<a for a in likes)]+=row['multiplicity']
        clients.extend([likes]*row['multiplicity'])
    expected={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,
              46:3,51:3,53:3,54:3,59:2,64:19}
    assert dict(types)==expected and len(clients)==53
    covers=[frozenset(x for x,t in enumerate(clients) if a in t) for a in range(n)]
    assert len(set(covers))==n
    strategy={tuple(row['history']):row['action'] for row in packet['actions']}
    all_histories={h for depth in range(4) for h in product(range(n),repeat=depth)}
    assert len(packet['actions'])==len(strategy)==len(all_histories)==400
    assert set(strategy)==all_histories
    assert all(a in range(n) for a in strategy.values())

    def follow(h):
        h=tuple(h)
        while len(h)<4:
            h+=(strategy[h],)
        return h

    def pay(z,position,extra_core=0):
        old=sum((F(1,sum(a in likes for a in z))
                 for likes in clients if z[position] in likes),F())
        # Independent direct common-client contribution; all 4 actions cover it.
        common=sum((F(1,sum(a in range(n) for a in z)) for _ in range(extra_core)),F())
        return old+common

    comparisons=0
    minimum=None
    core_translation_checks=0
    for h in sorted(all_histories,key=lambda h:(len(h),h)):
        i=len(h)
        actual=follow(h)
        for a in range(n):
            deviation=follow(h+(a,))
            gap=pay(actual,i)-pay(deviation,i)
            assert gap>=0
            minimum=gap if minimum is None else min(minimum,gap)
            comparisons+=1
            for c in (1,7):
                assert pay(actual,i,c)-pay(deviation,i,c)==gap
                core_translation_checks+=1
    actual=follow(())
    utilities=[pay(actual,i) for i in range(4)]
    assert actual==(6,0,3,4)
    assert utilities==[F(19),F(29,3),F(67,6),F(67,6)]
    assert packet['terminal_counts']==[actual.count(a) for a in range(n)]
    assert [j for j,u in enumerate(utilities[1:]) if u<T0]==[0]
    assert utilities[0]>T0 and T0-utilities[1]==DEFICIT
    load_spectrum=Counter(sum(a in likes for a in actual) for likes in clients if 0 in likes)
    assert dict(load_spectrum)=={2:12,3:11}

    p=tuple(F(a,5848) for a in (570,570,1197,570,570,1197,1174))
    Q=[((0,1,2),370),((0,1,6),3941),((0,2,6),1481),
       ((1,2,6),1481),((3,4,6),4089),((3,5,6),1629),((4,5,6),1629)]
    Q=[(z,F(weight,14620)) for z,weight in Q]
    assert sum(p,F())==1 and sum((q for z,q in Q),F())==1
    assert all(v>=0 for v in p) and all(q>=0 for z,q in Q)

    def insertion(a,z):
        return sum((F(1,1+sum(b in likes for b in z))
                    for likes in clients if a in likes),F())

    static=[(z,sum((p[a]*insertion(a,z) for a in range(n)),F()))
            for z in combinations_with_replacement(range(n),3)]
    assert len(static)==84 and min(v for z,v in static)==T0
    assert all(v>=T0 for z,v in static)
    caps=[sum((q*insertion(a,z) for z,q in Q),F()) for a in range(n)]
    assert caps==[T0]*7

    def equation(rho,c):
        return F(12,1+rho)+F(11,2+rho)+F(c,3+rho)-T0-F(c,4)

    def gamma(rho,c):
        return F(c,3+rho)-F(c,4)

    def bisect(c):
        low,high=F(),F(1)
        assert equation(low,c)>0 and equation(high,c)==-DEFICIT
        for _ in range(96):
            mid=(low+high)/2
            gap=equation(mid,c)
            if gap>0:
                low=mid
            elif gap<0:
                high=mid
            else:
                return mid,mid
        assert equation(low,c)>0 and equation(high,c)<0
        return low,high

    def compact_interval(low,high,scale=10**12):
        lower=(low.numerator*scale)//low.denominator
        upper=(high.numerator*scale+high.denominator-1)//high.denominator
        return [str(F(lower,scale)),str(F(upper,scale))]

    frozen=json.loads((TAIL/'waterfill_exact.json').read_text())
    frozen_checks=[]
    for row in frozen['cases']:
        c=row['common_core']
        low,high=map(F,row['water_weight_interval'])
        assert 0<low<=high<1
        assert equation(low,c)>=0 and equation(high,c)<=0
        lower,upper=gamma(high,c),gamma(low,c)
        assert list(map(F,row['root_gain_interval']))==[lower,upper]
        assert list(map(F,row['root_gain_over_deficit_interval']))==[lower/DEFICIT,upper/DEFICIT]
        assert 0<=lower<=upper<DEFICIT
        frozen_checks.append(c)

    intervals=[]
    for c in (0,1,37,1000,10**6):
        low,high=bisect(c)
        lower,upper=gamma(high,c),gamma(low,c)
        assert 0<=lower<=upper<DEFICIT
        if c:
            assert F(c,c+94)<lower/DEFICIT
            assert upper/DEFICIT<F(c,1)/(F(c)+F(608,9))
        intervals.append(dict(core=c,water_weight_interval=[low,high],
                              gamma_interval=[lower,upper],
                              gamma_over_deficit_interval=[lower/DEFICIT,upper/DEFICIT],
                              compact_ratio_interval=compact_interval(lower/DEFICIT,upper/DEFICIT)))

    report=dict(status='Independent analytic review and definition-level exact checks passed.',
                unit_customers=53,topics=7,players=4,
                ordered_histories=400,spe_comparisons=comparisons,
                minimum_spe_slack=minimum,core_translation_checks=core_translation_checks,
                actual=actual,utilities=utilities,welfare=sum(utilities,F()),
                true_v4=T0,static_backgrounds=84,primal_minimum=min(v for z,v in static),
                dual_caps=caps,low_tail_positions=[1],deficit=DEFICIT,
                X0_original_load_spectrum=dict(load_spectrum),
                frozen_intervals_independently_checked=frozen_checks,
                new_exact_intervals=intervals,
                scope='Sharpness of universal waterfill credit; not sharpness under the extra root<t restriction, not a half counterexample.')
    text=json.dumps(report,default=str,ensure_ascii=False,indent=2)+'\n'
    (HERE/'waterfill_review_audit.json').write_text(text)
    print(json.dumps({k:v for k,v in report.items() if k!='new_exact_intervals'},default=str,ensure_ascii=False,indent=2))
    print(json.dumps([dict(core=r['core'],compact_ratio_interval=r['compact_ratio_interval']) for r in intervals],indent=2))


if __name__=='__main__':
    main()
