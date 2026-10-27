"""Definition-level exact tests; no imports from the repository solver."""
import json,random
from fractions import Fraction as F
from itertools import product,combinations
from duplicate_action_quotient import cover_classes,quotient_policy,quotient_weights,project_history

def histories(k,m):
    return [h for t in range(m) for h in product(range(k),repeat=t)]

def continuation(policy,h,m):
    while len(h)<m:h=h+(policy[h],)
    return h

def pay(profile,weights):
    ans=[F(0) for _ in profile]
    for b,v in weights.items():
        if not v:continue
        users=[j for j,a in enumerate(profile) if b&(1<<a)]
        if users:
            for j in users:ans[j]+=F(v,len(users))
    return tuple(ans)

def is_spe(policy,weights,k,m):
    checked=0
    for h in histories(k,m):
        src=pay(continuation(policy,h,m),weights)[len(h)]
        for a in range(k):
            checked+=1
            if src<pay(continuation(policy,h+(a,),m),weights)[len(h)]:return False,checked
    return True,checked

def opt(weights,k,m):
    best=0
    for n in range(1,min(k,m)+1):
        for acts in combinations(range(k),n):
            mask=sum(1<<a for a in acts)
            best=max(best,sum(v for b,v in weights.items() if b&mask))
    return best

def audit(policy,weights,k,m):
    projection,groups=cover_classes(weights,k)
    quotient,lifts=quotient_policy(policy,m,projection)
    qweights=quotient_weights(weights,projection);qk=len(groups)
    valid,checked=is_spe(quotient,qweights,qk,m);assert valid
    assert cover_classes(qweights,qk)[0]==tuple(range(qk))
    for H,h in lifts.items():
        assert project_history(h,projection)==H
        assert continuation(quotient,H,m)==project_history(continuation(policy,h,m),projection)
    assert pay(continuation(policy,(),m),weights)==pay(continuation(quotient,(),m),qweights)
    assert opt(weights,k,m)==opt(qweights,qk,m)
    return checked

def backward_policy(weights,k,m,rng):
    policy={}; terminal={h:h for h in product(range(k),repeat=m)}
    for t in range(m-1,-1,-1):
        for h in product(range(k),repeat=t):
            values=[pay(terminal[h+(a,)],weights)[t] for a in range(k)]
            choices=[a for a,v in enumerate(values) if v==max(values)]
            a=rng.choice(choices);policy[h]=a;terminal[h]=terminal[h+(a,)]
    return policy

def main():
    exhaustive_games=0;exhaustive_policies=0;exhaustive_spe=0;compiled_IC=0
    hs=histories(3,2)
    for a,b,c in product(range(4),repeat=3):
        weights={3:a,4:b,7:c};exhaustive_games+=1
        for vals in product(range(3),repeat=len(hs)):
            policy=dict(zip(hs,vals));exhaustive_policies+=1
            valid,_=is_spe(policy,weights,3,2)
            if valid:
                exhaustive_spe+=1;compiled_IC+=audit(policy,weights,3,2)
    rng=random.Random(566240);random_games=200;history_dependent_tie_cases=0
    for _ in range(random_games):
        # Original bit positions 0 and 1 are identical; quotient has <=3 topics.
        weights={}
        for b in range(1,8):
            label_b=(3 if b&1 else 0)|(4 if b&2 else 0)|(8 if b&4 else 0)
            weights[label_b]=rng.randrange(6)
        policy=backward_policy(weights,4,3,rng)
        valid,_=is_spe(policy,weights,4,3);assert valid
        compiled_IC+=audit(policy,weights,4,3)
        # Record actual dependence on duplicate-label signals, rather than only count selectors.
        if any(policy[(0,a)]!=policy[(1,a)] for a in range(4)):history_dependent_tie_cases+=1
    # Full six-player scale regression, with one duplicate private label.
    weights={1:6,2:1,4:1,8:1,16:1,96:1}
    policy={h:0 for h in histories(7,6)}
    valid,original_six_IC=is_spe(policy,weights,7,6);assert valid
    compiled_six_IC=audit(policy,weights,7,6)
    compiled_IC+=compiled_six_IC
    print(json.dumps({'exhaustive_games':exhaustive_games,'exhaustive_full_policies':exhaustive_policies,
                      'exhaustive_full_SPE':exhaustive_spe,'random_three_player_games':random_games,
                      'duplicate_signal_dependent_cases':history_dependent_tie_cases,
                      'six_player_original_IC_comparisons':original_six_IC,
                      'six_player_quotient_IC_comparisons':compiled_six_IC,
                      'compiled_exact_IC_comparisons':compiled_IC,'all_checks_passed':True},indent=2))

if __name__=='__main__':main()
