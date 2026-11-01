"""Independent definition-level audit of the neighboring potential candidate.

Does not import the discovery script, solver, equilibrium model, or optimizer.
Only the JSON potential table and full ordered-history policy are read.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json


HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'next_independent/candidate_potential_individual.json'


def main():
    data=json.loads(SOURCE.read_text())
    p,n=data['topics'],data['players']
    phi={tuple(row['counts']):F(row['value']) for row in data['potential']}
    actions={tuple(row['history']):row['action'] for row in data['actions']}
    def cnt(h):return tuple(h.count(a) for a in range(p))
    def plus(q,a):return tuple(x+(i==a) for i,x in enumerate(q))
    def minus(q,a):
        assert q[a]>0
        return tuple(x-(i==a) for i,x in enumerate(q))
    def payoff(a,q):
        assert q[a]>0
        return phi[q]-phi[minus(q,a)]
    expected={cnt(h) for k in range(n+1) for h in combinations_with_replacement(range(p),k)}
    assert set(phi)==expected
    assert phi[(0,)*p]==0
    required={h for k in range(n) for h in product(range(p),repeat=k)}
    assert set(actions)==required
    monotonic=[];dr=[];self_congestion=[]
    for q in expected:
        depth=sum(q)
        if depth<n:
            for a in range(p):monotonic.append(phi[plus(q,a)]-phi[q])
        if depth<=n-2:
            for a,b in product(range(p),repeat=2):
                dr.append(phi[plus(q,a)]+phi[plus(q,b)]-phi[q]-phi[plus(plus(q,a),b)])
        if depth:
            for a,b in product(range(p),repeat=2):
                if a!=b and q[a] and q[b]:
                    r=plus(minus(q,b),a)
                    self_congestion.append(payoff(a,q)-payoff(a,r))
    assert min(monotonic)>=0 and min(dr)>=0 and min(self_congestion)>=0
    def terminal(h):
        h=list(h)
        while len(h)<n:h.append(actions[tuple(h)])
        return tuple(h)
    spe=[]
    for h in sorted(required,key=lambda h:(len(h),h)):
        z=terminal(h);own=payoff(actions[h],cnt(z))
        for a in range(p):spe.append(own-payoff(a,cnt(terminal(h+(a,)))))
    assert min(spe)>=0
    actual=terminal(())
    q=cnt(actual)
    utilities=[payoff(a,q) for a in actual]
    welfare=sum(utilities)
    query=list(map(F,data['query']))
    assert sum(query)==1 and min(query)>=0
    static=[]
    for h in combinations_with_replacement(range(p),n-1):
        b=cnt(h)
        static.append((b,sum(query[a]*payoff(a,plus(b,a)) for a in range(p))))
    lower=min(x for b,x in static)
    assert welfare==10458 and lower==3549 and welfare-n*lower==-189
    # A concrete harmonic same-theme ratio excluded by this candidate.
    pure=[payoff(a,tuple(n*(i==a) for i in range(p))) for a in range(p)]
    assert pure==[0]*p
    violations=[]
    for a in range(p):
        if q[a] and q[a]*payoff(a,q)>n*pure[a]:
            violations.append({'topic':a,'terminal_payoff':str(payoff(a,q)),
                               'pure_payoff':str(pure[a]),
                               'harmonic_dilution_slack':str(n*pure[a]-q[a]*payoff(a,q))})
    result={'status':'independent_exact_audit_passed_ABSTRACT_NOT_CAG',
            'potential_domain':'all count vectors with total at most 3',
            'potential_entries':len(phi),'ordered_decision_nodes':len(required),
            'checks':{'monotonicity':len(monotonic),'unit_DR':len(dr),
                      'self_congestion_all_positive_levels':len(self_congestion),
                      'full_history_SPE':len(spe),'unordered_static_backgrounds':len(static)},
            'minimum_slacks':{'monotonicity':str(min(monotonic)),'DR':str(min(dr)),
                              'self_congestion':str(min(self_congestion)),'SPE':str(min(spe))},
            'actual_path':actual,'actual_payoffs':list(map(str,utilities)),
            'welfare':str(welfare),'fixed_query_guarantee':str(lower),
            'welfare_minus_n_guarantee':str(welfare-n*lower),
            'CAG_exclusion_by_sharp_same_theme_dilution':violations,
            'full_domain_extension_not_claimed':True}
    target=HERE/'potential_candidate_independent_audit.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
