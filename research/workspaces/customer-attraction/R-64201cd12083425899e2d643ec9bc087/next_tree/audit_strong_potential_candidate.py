"""Independent exact audit of the stronger neighboring potential point.

The discovery implementation and optimizer are not imported. This is a finite
potential-domain template obstruction, NOT a customer-attraction game.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent


def main():
    data=json.loads((HERE.parent/'next_independent/candidate_potential_strong_individual.json').read_text())
    p,n=data['topics'],data['players']
    phi={tuple(x['counts']):F(x['value']) for x in data['potential']}
    actions={tuple(x['history']):x['action'] for x in data['actions']}
    def count(h):return tuple(h.count(a) for a in range(p))
    def add(q,a):return tuple(x+(i==a) for i,x in enumerate(q))
    def sub(q,a):return tuple(x-(i==a) for i,x in enumerate(q))
    def u(q,a):
        assert q[a]>0
        return phi[q]-phi[sub(q,a)]
    states={count(h) for k in range(n+1) for h in combinations_with_replacement(range(p),k)}
    assert set(phi)==states and phi[(0,)*p]==0
    histories={h for k in range(n) for h in product(range(p),repeat=k)}
    assert set(actions)==histories
    mono=[];dr=[];selfing=[];sharp=[];harmonic=[]
    for q in states:
        k=sum(q)
        if k<n:
            for a in range(p):mono.append(phi[add(q,a)]-phi[q])
        if k<=n-2:
            for a,b in product(range(p),repeat=2):
                dr.append(phi[add(q,a)]+phi[add(q,b)]-phi[q]-phi[add(add(q,a),b)])
        for a,b in product(range(p),repeat=2):
            if a!=b and q[a] and q[b]:
                r=add(sub(q,b),a)
                selfing.append(u(q,a)-u(r,a))
                sharp.append((q[a]+1)*u(r,a)-q[a]*u(q,a))
    for a in range(p):
        e=tuple(int(b==a) for b in range(p))
        for k in range(1,n+1):
            q=tuple(k*x for x in e)
            harmonic.append(phi[q]-sum(F(1,j) for j in range(1,k+1))*phi[e])
    assert min(mono)>=0 and min(dr)>=0 and min(selfing)>=0 and min(sharp)>=0
    assert all(x==0 for x in harmonic)
    def finish(h):
        while len(h)<n:h=h+(actions[h],)
        return h
    spe=[]
    for h in histories:
        actual=count(finish(h));current=actions[h]
        for a in range(p):spe.append(u(actual,current)-u(count(finish(h+(a,))),a))
    assert min(spe)>=0
    root=count(finish(()));payoffs=[u(root,a) for a in finish(())]
    welfare=sum(payoffs);query=list(map(F,data['query']))
    background_values=[]
    for h in combinations_with_replacement(range(p),n-1):
        q=count(h)
        background_values.append(sum(query[a]*u(add(q,a),a) for a in range(p)))
    lower=min(background_values)
    assert welfare==184878 and lower==61815 and welfare-n*lower==-567
    totals={};mismatches=[]
    for h in combinations_with_replacement(range(p),n):
        q=count(h);support=tuple(a for a in range(p) if q[a])
        total=sum(q[a]*u(q,a) for a in support)
        if support not in totals:totals[support]=(q,total)
        elif totals[support][1]!=total:
            old,v=totals[support]
            mismatches.append({'support':support,'q':old,'r':q,
                               'q_total':str(v),'r_total':str(total),'difference':str(total-v)})
    assert len(mismatches)==9
    # A separate two-support common-customer identity, with C_a inferred from
    # pure n-player payoff, rather than same-support efficiency alone.
    pair_failures=[]
    for a,b in product(range(p),repeat=2):
        if a>=b:continue
        purea=tuple(n*int(c==a) for c in range(p));pureb=tuple(n*int(c==b) for c in range(p))
        qa=tuple(2*int(c==a)+int(c==b) for c in range(p))
        qb=tuple(int(c==a)+2*int(c==b) for c in range(p))
        error=u(qa,a)-u(qb,b)-F(3,2)*(u(purea,a)-u(pureb,b))
        if error:pair_failures.append({'a':a,'b':b,'common_signed_identity_error':str(error)})
    assert pair_failures
    result={'status':'independent_strong_finite_potential_audit_passed_NOT_CAG',
            'domain':'all |q|<=3 only; no global extension asserted',
            'checks':{'potential_entries':len(phi),'ordered_nodes':len(histories),
                      'monotone':len(mono),'DR':len(dr),'self_congestion':len(selfing),
                      'one_step_sharp_dilution':len(sharp),'pure_harmonic':len(harmonic),
                      'full_history_SPE':len(spe),'static_backgrounds':len(background_values)},
            'minimum_slacks':{'monotone':str(min(mono)),'DR':str(min(dr)),
                              'self_congestion':str(min(selfing)),'sharp':str(min(sharp)),
                              'SPE':str(min(spe))},
            'welfare':str(welfare),'query_lower_bound':str(lower),
            'gap':str(welfare-n*lower),'actual_payoffs':list(map(str,payoffs)),
            'same_support_efficiency_mismatches':mismatches,
            'two_support_identity_failures':pair_failures,
            'common_signed_customer_realization_excluded':True}
    (HERE/'strong_potential_independent_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in
                      ['same_support_efficiency_mismatches','two_support_identity_failures']},indent=2))


if __name__=='__main__':main()
