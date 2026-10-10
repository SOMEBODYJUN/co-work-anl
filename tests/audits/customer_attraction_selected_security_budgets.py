"""Independent ordered-history SPE menu and optimal budget bound audit.

Unlike the generator, every menu element is a FULL ORDERED PROFILE. There
is no count-state compression and no generator/solver import.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

BASE=Path(__file__).resolve().parents[2]/'evidence/certificates/customer_attraction/selected_security_budgets'

def verify(path):
    d=json.loads(Path(path).read_text());g=d['game'];n=g['players'];m=len(g['topics']);p=list(map(F,d['security']['primary']))
    assert sum(p)==1 and min(p)>=0
    def utility(z,i):
        return sum((F(r['multiplicity'],sum(b in r['topics'] for b in z)) for r in g['customers'] if z[i] in r['topics']),F(0))
    def query(a,B):
        return sum((F(r['multiplicity'],1+sum(b in r['topics'] for b in B)) for r in g['customers'] if a in r['topics']),F(0))
    def coverage(z):return sum(r['multiplicity'] for r in g['customers'] if any(a in r['topics'] for a in z))
    def Cbranch(z,i):
        B=z[:i]+z[i+1:]
        return sum(p[a]*query(a,B) for a in range(m))
    @lru_cache(None)
    def feasible(h):
        if len(h)==n:return (h,)
        i=len(h);branches=[feasible(h+(b,)) for b in range(m)]
        threshold=max(min(utility(z,i) for z in branch) for branch in branches)
        return tuple(z for branch in branches for z in branch if utility(z,i)>=threshold)
    profiles=feasible(());best=None;per_profile={}
    for z in profiles:
        Cs=F(0)
        for i,chosen in enumerate(z):
            own=utility(z,i)
            for b in range(m):
                if b==chosen:cvalue=Cbranch(z,i)
                else:
                    alternatives=[off for off in feasible(z[:i]+(b,)) if utility(off,i)<=own]
                    assert alternatives
                    cvalue=max(Cbranch(off,i) for off in alternatives)
                Cs+=p[b]*cvalue
        violation=Cs-coverage(z);per_profile[z]=violation
        if best is None or violation>best:best=violation
    assert len(profiles)==d['possible_ordered_SPE_paths']
    assert best==F(d['GB_violation_sumC_minus_W'])
    # Matching stored strategy is a genuine complete policy attaining the bound.
    raw=d['strategy']['actions'];policy={tuple(r['history']):r['action'] for r in raw}
    histories=[h for depth in range(n) for h in product(range(m),repeat=depth)]
    assert len(raw)==len(policy) and set(policy)==set(histories)
    def terminal(h):
        z=list(h)
        while len(z)<n:z.append(policy[tuple(z)])
        return tuple(z)
    for h in histories:
        value=utility(terminal(h),len(h))
        for a in range(m):assert value>=utility(terminal(h+(a,)),len(h))
    actual=terminal(());Ctotal=F(0)
    for i in range(n):
        for b in range(m):Ctotal+=p[b]*Cbranch(terminal(actual[:i]+(b,)),i)
    assert Ctotal-coverage(actual)==best
    Q=[(tuple(r['rivals']),F(r['probability'])) for r in d['security']['dual']]
    assert sum(q for B,q in Q)==1 and min(q for B,q in Q)>=0
    floor=min(sum(p[a]*query(a,B) for a in range(m)) for B in product(range(m),repeat=n-1))
    cap=max(sum(q*query(a,B) for B,q in Q) for a in range(m));assert floor==cap
    return {'file':Path(path).name,'status':'PASS','complete_ordered_decision_histories':len(histories),
            'ordered_SPE_outcomes':len(profiles),'minimum_GB_budget_over_all_pure_SPE_at_given_optimal_p':str(-best),
            'attaining_strategy_full_comparisons':len(histories)*m,'static_security_value':str(floor)}

if __name__=='__main__':
    cases=[verify(BASE/f'all_SPE_GB_{name}.json') for name in ['original36','individual34','individual360','root_tax_failure','global_decorrelation_failure']]
    print(json.dumps({'status':'PASS','scope':'Five fixed games at one specified exact optimal p each; no universal claim','cases':cases},indent=2))
