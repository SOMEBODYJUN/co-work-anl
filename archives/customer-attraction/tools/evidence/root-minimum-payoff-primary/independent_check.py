"""Set-valued exact backward induction plus explicit full-history strategy."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

def audit(rows, n, k, target=None):
    def payoff(z, i):
        return sum((F(w, sum(a in T for a in z)) for T,w in rows if z[i] in T), F())
    def welfare(z):
        return sum(w for T,w in rows if set(z).intersection(T))
    @lru_cache(None)
    def outcomes(h):
        if len(h) == n:
            return (h,)
        d = len(h)
        children = [outcomes(h+(a,)) for a in range(k)]
        floor = max(min(payoff(z,d) for z in child) for child in children)
        return tuple(z for child in children for z in child if payoff(z,d) >= floor)
    root = outcomes(())
    target = tuple(target) if target is not None else root[0]
    assert target in root
    policy = {}
    def construct(h, chosen_leaf):
        assert chosen_leaf in outcomes(h)
        if len(h) == n:
            return
        d = len(h);chosen_action=chosen_leaf[d]
        policy[h] = chosen_action
        for a in range(k):
            branch=h+(a,)
            leaf=(chosen_leaf if a==chosen_action else
                  min(outcomes(branch), key=lambda z:(payoff(z,d),z)))
            assert payoff(chosen_leaf,d) >= payoff(leaf,d)
            construct(branch,leaf)
    construct((), target)
    def finish(h):
        while len(h)<n:h += (policy[h],)
        return h
    assert finish(()) == target
    gaps=[]
    for d in range(n):
        for h in product(range(k),repeat=d):
            assert h in policy
            for a in range(k):
                gaps.append(payoff(finish(h),d)-payoff(finish(h+(a,)),d))
    assert min(gaps) >= 0
    optimum=max(welfare(z) for z in product(range(k),repeat=n))
    return {'all_SPE_terminal_paths':[list(z) for z in root],
            'all_root_payoffs':list(map(str,[payoff(z,0) for z in root])),
            'minimum_root_payoff':str(min(payoff(z,0) for z in root)),
            'selected_path':list(target),'selected_payoffs':list(map(str,[payoff(target,i) for i in range(n)])),
            'W':welfare(target),'OPT':optimum,'ordered_decision_histories':len(policy),
            'IC_comparisons_with_self':len(gaps),'minimum_IC_gap':str(min(gaps)),
            'full_policy':[{'history':list(h),'action':a} for h,a in sorted(policy.items(),key=lambda x:(len(x[0]),x[0]))]}

base=Path(__file__).parent
frozen=json.loads((base/'scan.json').read_text())
finding=frozen['findings'][0]
instance=finding['instance']
rows=[(frozenset(c['topics']),c['multiplicity']) for c in instance['customers']]
result=audit(rows,instance['players'],len(instance['topics']),finding['path'])
assert sum(w for _,w in rows)==14
assert result['all_SPE_terminal_paths']==[[1,3,0,0],[3,1,0,0]]
assert result['selected_payoffs']==finding['payoffs']
assert result['minimum_root_payoff']==finding['rootmin']=='13/4'
assert len(result['all_SPE_terminal_paths'])==finding['root_paths']==2
assert result['W']==12 and result['OPT']==14 and result['ordered_decision_histories']==85
assert result['IC_comparisons_with_self']==340
assert F(result['W'])-4*F(result['minimum_root_payoff'])==-1
assert 2*result['W']>=result['OPT']
boundaries={}
for name,rs,n,k in [('zero_customers',[],3,2),('all_interest',[(frozenset(range(2)),1)],3,2),
                     ('single_label',[(frozenset((0,)),2)],4,1),
                     ('doubled_original',[(T,2*w) for T,w in rows],4,4)]:
    b=audit(rs,n,k)
    boundaries[name]={q:b[q] for q in ('minimum_root_payoff','W','OPT','ordered_decision_histories','IC_comparisons_with_self','minimum_IC_gap')}
assert boundaries['doubled_original']['minimum_root_payoff']=='13/2'
assert boundaries['doubled_original']['W']==24 and boundaries['doubled_original']['OPT']==28
result['root_payment_gap']='-1'
result['boundary_cases']=boundaries
result['status']='exact all-outcomes and explicit-strategy audit passed'
print(json.dumps(result,indent=2))
