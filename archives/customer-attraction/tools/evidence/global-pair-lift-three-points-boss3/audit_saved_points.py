#!/usr/bin/env python3
"""One independent Fraction audit of the three saved points; no LP or imports
from either exploration program.  All ordered policy histories are retained.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from collections import Counter
from math import comb, lcm, gcd
import hashlib
import json
import platform
import time

P = Path(__file__).resolve().parent


def subsets(mask):
    e=mask
    while True:
        yield e
        if not e:
            break
        e=(e-1)&mask


def audit(name):
    raw=(P/'original'/name).read_bytes()
    z=json.loads(raw);m=z['m'];p=z['p']
    masks=[s for s in range(1,1<<p) if s.bit_count()<=m]
    t={int(s):F(v) for s,v in z['moments'].items()}
    assert set(t)==set(masks)
    x={int(b):F(v) for b,v in z['lift'].items()}
    assert all(0<b<1<<p and v>0 for b,v in x.items())
    sigma={tuple(map(int,h.split(','))) if h else ():a for h,a in z['policy'].items()}
    histories=[h for depth in range(m) for h in product(range(p),repeat=depth)]
    assert len(sigma)==len(z['policy']) and set(sigma)==set(histories)
    assert all(0<=a<p for a in sigma.values())

    @lru_cache(None)
    def terminal(h):
        return h if len(h)==m else terminal(h+(sigma[h],))

    def counts(h):
        return tuple(h.count(a) for a in range(p))

    @lru_cache(None)
    def payoff(q,a):
        assert q[a]>0
        others=sum(1<<b for b,v in enumerate(q) if v and b!=a)
        answer=F(0)
        for c in subsets(others):
            gamma=sum((F((-1)**(c.bit_count()-e.bit_count()),
                         q[a]+sum(q[b] for b in range(p) if e>>b&1))
                       for e in subsets(c)),F(0))
            answer+=gamma*t[c|(1<<a)]
        return answer

    def cover(s):
        return sum(((-1)**(a.bit_count()+1)*t[a]
                    for a in subsets(s) if a),F(0))

    local=[]
    for a in masks:
        for c in range(1<<p):
            if a&c or (a|c).bit_count()>m:
                continue
            value=sum(((-1)**e.bit_count()*t[a|e] for e in subsets(c)),F(0))
            assert value>=0,(name,'local',a,c,value)
            local.append([a,c,str(value)])

    degree_masks=[s for s in masks if s.bit_count()<=z['degree']]
    recovered={s:sum((v for b,v in x.items() if b&s==s),F(0)) for s in masks}
    assert all(t[s]==recovered[s] for s in degree_masks)
    mismatch=[{'mask':s,'saved':str(t[s]),'provided_lift':str(recovered[s])}
              for s in masks if t[s]!=recovered[s]]

    ic=[];strict=0
    for h in histories:
        a=sigma[h];own=payoff(counts(terminal(h)),a)
        for b in range(p):
            if b==a:
                continue
            alternative=payoff(counts(terminal(h+(b,))),b)
            slack=own-alternative
            assert slack>=0,(name,'IC',h,a,b,slack)
            strict+=int(slack>0)
            ic.append([list(h),a,b,str(own),str(alternative),str(slack)])

    root=terminal(())
    assert list(root)==z['root']
    root_mask=sum(1<<a for a in set(root))
    W=cover(root_mask);assert W==1
    profits=[payoff(counts(root),a) for a in root]
    assert sum(profits)==W
    portfolios=[]
    for J in combinations(range(p),min(m,p)):
        value=cover(sum(1<<a for a in J))
        portfolios.append({'J':list(J),'value':str(value)})
    max_cover=max(F(a['value']) for a in portfolios)
    stored_cover=cover(sum(1<<a for a in z['J']))
    assert stored_cover==max_cover

    family=None;separator=None;integer_instance=None
    if m==3:
        assert not mismatch
        scale=lcm(*(v.denominator for v in x.values()))
        clones={b:int(v*scale) for b,v in x.items()}
        common=gcd(*clones.values())
        clones={b:v//common for b,v in clones.items()}
        factor=F(scale,common)
        def direct(q,a):
            return sum((F(v,sum(q[b] for b in range(p) if mask>>b&1))
                        for mask,v in clones.items() if mask>>a&1),F(0))
        comparisons=0
        for h in histories:
            a=sigma[h];q=counts(terminal(h));own=direct(q,a)
            assert own==factor*payoff(q,a)
            for b in range(p):
                if b==a:
                    continue
                qb=counts(terminal(h+(b,)))
                assert direct(qb,b)==factor*payoff(qb,b)
                assert own>=direct(qb,b)
                comparisons+=1
        integer_instance={'types':{str(b):v for b,v in clones.items()},
                          'customers':sum(clones.values()),'scale_from_saved':str(factor),
                          'full_history_nonself_comparisons':comparisons,
                          'W':str(factor*W),'OPT':str(factor*max_cover),
                          'root_payoffs':[str(factor*v) for v in profits]}
    else:
        center=2
        leaves=[1,3,4,5] if m==4 else [0,1,3,4,5]
        aliases={0,2} if m==4 else {2}
        epsilon=F(1,10) if m==4 else F(1,25)
        for s in masks:
            leaf_count=sum(bool(s>>a&1) for a in leaves)
            has_center=any(s>>a&1 for a in aliases)
            star=F(1) if not leaf_count else (F(1,m-1) if has_center else F(2,m)) if leaf_count==1 else F(0)
            assert t[s]==epsilon+(1-epsilon)*star,(name,'star-mixture',s)
        assert set(sigma.values())<=aliases
        family={'center_aliases':sorted(aliases),'leaves':leaves,'all_interest_mass':str(epsilon),
                'star_coefficient':str(1-epsilon),'all_visible_coordinates_match':True}
        triple=leaves[:3]
        def Q(b):
            alpha=int(bool(b>>center&1));k=sum(bool(b>>a&1) for a in leaves)
            return alpha-alpha*k+comb(k,2)
        triple_mask=sum(1<<a for a in triple)
        values=[Q(b)-int(b&triple_mask==triple_mask) for b in range(1<<p)]
        assert min(values)>=0 and values[0]==0
        q_value=t[1<<center]-sum(t[(1<<center)|(1<<a)] for a in leaves)+sum(t[(1<<a)|(1<<b)] for a,b in combinations(leaves,2))
        assert q_value==0
        residual=q_value-t[triple_mask]
        assert residual<0 and all(Q(b)==0 for b in x)
        separator={'center':center,'leaves':leaves,'triple':triple,'triple_mask':triple_mask,
                   'Q_moment_value':str(q_value),'Q_minus_triple_value':str(residual),
                   'boolean_assignments':1<<p,'minimum_boolean_value':min(values),
                   'empty_type_value':values[0], 'provided_lift_support_on_Q_zero_face':True}

    summary={'file':name,'source_sha256':hashlib.sha256(raw).hexdigest(),'m':m,'p':p,
             'degree':z['degree'],'trial_at_saved_improvement':z['trial'],'seen_at_saved_improvement':z['seen'],
             'visible_moments':len(t),'ordered_histories':len(histories),
             'action_counts':dict(Counter(sigma.values())),'local_cylinders':len(local),
             'minimum_local_slack':str(min(F(r[2]) for r in local)),
             'nonself_IC':len(ic),'strict_nonself_IC':strict,'minimum_IC_slack':str(min(F(r[5]) for r in ic)),
             'lift_support':len(x),'degree_lift_equalities':len(degree_masks),
             'all_moment_mismatches_from_provided_lift':len(mismatch),
             'first_mismatch':mismatch[0] if mismatch else None,
             'root':list(root),'root_payoffs':list(map(str,profits)),'W':str(W),
             'point_max_portfolio_coverage':str(max_cover),'stored_J_attains_point_max':True,
             'historical_float_ratio':z['ratio'],'exact_point_ratio':str(max_cover/W),
             'integer_instance':integer_instance,'star_mixture':family,'nonnegative_extension_separator':separator}
    details={'file':name,'local_rows':[ 'positive_mask','negative_mask','slack' ],'local_checks':local,
             'IC_rows':['history','chosen','alternative','own','deviation','slack'],'IC_checks':ic,
             'provided_lift_mismatches':mismatch,'point_portfolios':portfolios}
    return summary,details


def main():
    start=time.perf_counter()
    summaries=[];details=[]
    for name in ('global2_m3p5.json','global2_m4p6.json','global2_m5p6.json'):
        summary,detail=audit(name);summaries.append(summary);details.append(detail)
    assert sum(x['nonself_IC'] for x in summaries)==9194
    report={'kind':'one independent standard-library Fraction audit of saved points; zero LP/random/source CLI',
            'python':platform.python_version(),'wall_seconds':time.perf_counter()-start,
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'points':summaries,'total_ordered_histories':sum(x['ordered_histories'] for x in summaries),
            'total_nonself_IC':sum(x['nonself_IC'] for x in summaries),
            'total_local_cylinders':sum(x['local_cylinders'] for x in summaries),
            'total_low_degree_lift_equalities':sum(x['degree_lift_equalities'] for x in summaries)}
    (P/'saved-points-exact-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    (P/'saved-points-full-checks.json').write_text(json.dumps(details,separators=(',',':'))+'\n')
    print(json.dumps(report),flush=True)


if __name__=='__main__':
    main()
