"""Blind input/certificate C7 review, with no project solver imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'independent_reconstruction'

def main():
    ins=json.loads((SOURCE/'cycle_seven_instance.json').read_text())
    cert=json.loads((SOURCE/'cycle_seven_certificate.json').read_text())
    p=len(ins['topics']); m=ins['players']
    customers=[(frozenset(c['topics']),c['multiplicity']) for c in ins['customers']]
    assert p==7 and m==4 and len(customers)==7
    assert all(w==1 and len(B)==2 for B,w in customers)
    policy={tuple(z['history']):z['action'] for z in cert['actions']}
    histories=[h for d in range(m) for h in product(range(p),repeat=d)]
    assert len(policy)==len(cert['actions'])==len(histories)
    assert set(policy)==set(histories)
    assert all(isinstance(a,int) and 0<=a<p for a in policy.values())
    def outcome(h):
        while len(h)<m: h=h+(policy[h],)
        return h
    def utility(h,a):
        return sum((F(w,sum(t in B for t in h))
                    for B,w in customers if a in B),F(0))
    def welfare(h):
        return sum(w for B,w in customers if any(t in B for t in h))
    slacks=[]
    for h in histories:
        a=policy[h]
        actual=utility(outcome(h),a)
        for b in range(p):
            changed=utility(outcome(h+(b,)),b)
            slacks.append(actual-changed)
    assert min(slacks)>=0
    path=outcome(())
    assert tuple(path.count(a) for a in range(p))==tuple(cert['terminal_counts'])
    payoffs=tuple(utility(path,a) for a in path)
    W=welfare(path)
    OPT=max(welfare(h) for h in product(range(p),repeat=m))
    theta_rows=[]
    for h in product(range(p),repeat=m-1):
        us=[utility(h+(a,),a) for a in range(p)]
        theta_rows.append({'prefix':h,'maximum':max(us),
                           'best_replies':[a for a,u in enumerate(us) if u==max(us)]})
    theta=min(row['maximum'] for row in theta_rows)
    static=[h for h in product(range(p),repeat=m-1)]
    uniform=[sum((utility(h+(a,),a) for a in range(p)),F(0))/p for h in static]
    safety_lower=min(uniform)
    opponents=[tuple((a+j)%p for a in (0,2,4)) for j in range(p)]
    against_Q=[sum((utility(h+(a,),a) for h in opponents),F(0))/p for a in range(p)]
    safety_upper=max(against_Q)
    assert safety_lower==safety_upper
    safety=safety_lower
    report={"source_instance":"independent_reconstruction/cycle_seven_instance.json",
            "source_certificate":"independent_reconstruction/cycle_seven_certificate.json",
            "method":"Definition-level Fraction replay, no solver or proposer-code imports",
            "decision_histories":len(histories),"action_comparisons":len(slacks),
            "minimum_spe_slack":min(slacks),"root_path":path,
            "root_payoffs":payoffs,"W":W,"OPT":OPT,
            "theta":theta,"all_last_prefixes":theta_rows,
            "theta_failures":[i+1 for i,u in enumerate(payoffs) if u<theta],
            "half_coverage":2*W>=OPT,
            "aggregate_theta":W>=m*theta,
            "weak_opt_floor":F(OPT,2*m-1),
            "all_weak_floors_hold":all(u>=F(OPT,2*m-1) for u in payoffs),
            "static_safety":safety,"uniform_query_lower":safety_lower,
            "static_upper_opponents":opponents,"query_values_against_upper_Q":against_Q,
            "aggregate_security":W>=m*safety,
            "first_two_security":payoffs[0]+payoffs[1]>=2*safety,
            "first_two_theta":payoffs[0]+payoffs[1]>=2*theta}
    clean=json.loads(json.dumps(report,default=str))
    (HERE/'cycle_seven_independent_audit.json').write_text(json.dumps(clean,indent=2)+'\n')
    print(json.dumps({k:v for k,v in clean.items() if k!='all_last_prefixes'},indent=2))

if __name__=='__main__': main()
