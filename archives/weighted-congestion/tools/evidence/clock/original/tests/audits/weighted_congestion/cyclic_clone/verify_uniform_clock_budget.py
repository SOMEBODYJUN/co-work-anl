"""Exact arithmetic audit of the uniform anchored-clock degree barrier.

Standard library only. The general theorem is analytic; abstract parameter
samples below assert necessary input conditions only, not existence of games.
The separate quadratic triad is evaluated from literal resource user sets.
Run from any directory; stdout JSON, optional --output creates a new file.
"""
from fractions import Fraction as F
from itertools import product, combinations
from hashlib import sha256
from pathlib import Path
import argparse
import json
import platform

LOG_TERMS = 64

def logarithm(x):
    """Rigorous rational lower/upper interval for ln(x), x>0."""
    assert x > 0
    if x < 1:
        lo, hi = logarithm(1/x)
        return -hi, -lo
    k = 0
    while x >= 2:
        x /= 2
        k += 1
    def reduced(v):
        z = (v-1)/(v+1)
        value = sum((2*z**(2*j+1)/F(2*j+1) for j in range(LOG_TERMS)), F())
        error = 2*z**(2*LOG_TERMS+1)/((2*LOG_TERMS+1)*(1-z*z))
        return value, value+error
    l2, u2 = reduced(F(2))
    lo, hi = reduced(x)
    return k*l2+lo, k*u2+hi

def parameters(weights, anchor):
    others = [i for i in range(len(weights)) if i != anchor]
    triples = [(anchor,i,j) for i,j in combinations(others,2)]
    delta = max(1-min(weights[i] for i in t)/sum((weights[i] for i in t),F()) for t in triples)
    ratio = max(weights)/min(weights)
    assert 0 < delta < 1
    assert delta >= (ratio+1)/(ratio+2)
    return delta, ratio, len(triples)

def degree(delta, epsilon):
    assert 0 < delta < 1 and 0 < epsilon < 1
    lo, hi = 0, 1
    while delta**hi > epsilon:
        lo, hi = hi, 2*hi
    while hi-lo > 1:
        mid = (lo+hi)//2
        if delta**mid <= epsilon:
            hi = mid
        else:
            lo = mid
    assert delta**hi <= epsilon < delta**(hi-1)
    return hi

def check(weights, anchor, alpha, eta_over_B):
    delta, ratio, L = parameters(weights,anchor)
    assert 1 <= alpha < ratio and 0 < eta_over_B <= 1
    A = 4*alpha**2*L/eta_over_B
    D = degree(delta, 1/A)
    _, logA_hi = logarithm(A)
    assert D > (ratio+1)*logA_hi
    t_lo, t_hi = logarithm(2*alpha)
    assert D > 2*(alpha+1)*t_hi
    assert 2*(alpha+1)*t_lo > alpha+1
    trials = []
    for p in sorted({0,1,D//2,D,2*D}):
        q = max(p,D)
        lo, hi = logarithm(F(q))
        assert q > (alpha+1)*hi
        assert alpha*hi/q < alpha/(alpha+1) < 1
        trials.append((q,alpha*lo/q,alpha*hi/q))
    return D, trials

def costs(profile, weights, resources):
    out = [F() for _ in weights]
    for users_at, power, coefficient in resources:
        users = [i for i,a in enumerate(users_at) if a is not None and profile[i] == a]
        load = sum((weights[i] for i in users),F())
        for i in users:
            out[i] += coefficient*load**power
    return out

def real_triad():
    weights = [F(16),F(2),F(5)]
    initial = [0,1,0]
    alpha = F(21,20)
    raw = [((0,1,1),2,F(13)),((1,1,2),1,F(59)),((1,2,1),2,F(2))]
    resources = []
    for mask,power,coefficient in raw:
        for side in [0,1]:
            literal = [None if m == 0 else (m-1)^side^initial[i] for i,m in enumerate(mask)]
            resources.append((literal,power,coefficient))
    states = list(product([0,1],repeat=3))
    table = {s:costs(s,weights,resources) for s in states}
    B = max(x for row in table.values() for x in row)
    s = (0,0,0)
    margins = []
    for step in range(6):
        i = step%3
        t = list(s); t[i] ^= 1; t = tuple(t)
        margins.append(table[s][i]-alpha*table[t][i])
        s = t
    assert s == (0,0,0)
    eta = min(margins)
    assert 0 < eta <= B
    delta,R,L = parameters(weights,0)
    D,trials = check(weights,0,alpha,eta/B)
    assert D == 62
    return {'weights':list(map(str,weights)), 'alpha':str(alpha), 'B':str(B),
            'eta':str(eta),'delta':str(delta),'R':str(R),'L':L,'D':D,
            'cycle_margins':list(map(str,margins)),
            'normalized_ratio_interval':[str(trials[0][1]),str(trials[0][2])],
            'profiles_evaluated':len(states),
            'scope':'Actual strict double-sweep base game; budget and degree checked, not a new target-scale nonexistence family.'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    args = parser.parse_args()
    # Verify interval inversion and exact known logarithmic identities.
    for x in [F(1,1000),F(1,2),F(1),F(2),F(3),F(8),F(12345)]:
        lo,hi = logarithm(x)
        invlo,invhi = logarithm(1/x)
        assert lo <= hi and invlo == -hi and invhi == -lo
        if x == 1: assert lo == hi == 0
    weights_list = [tuple(map(F,v)) for v in product([1,2,4],repeat=3)]
    weights_list += [tuple(map(F,v)) for v in [(1,1,1,8),(1,8,8,8),(1,2,4,8),(8,4,2,1),
                     (1,1,3,3,9),(9,3,3,1,1),(1,2,3,4,5,6),(1,1,1,1,1,1,1,16)]]
    alphas = [F(1),F(21,20),F(5,4),F(3,2),F(2),F(3)]
    margins = [F(1),F(1,7),F(1,1000)]
    cases = qchecks = anchors = 0
    maximum_D = 0
    digest = sha256()
    for weights in weights_list:
        for anchor in range(len(weights)):
            anchors += 1
            delta,R,L = parameters(weights,anchor)
            for alpha in alphas:
                if alpha >= R: continue
                for eta_over_B in margins:
                    D,trials = check(weights,anchor,alpha,eta_over_B)
                    maximum_D = max(maximum_D,D)
                    cases += 1
                    qchecks += len(trials)
                    digest.update(str((weights,anchor,alpha,eta_over_B,D,trials)).encode())
    out = {'status':'all exact assertions passed','python':platform.python_version(),
           'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
           'arithmetic':'Fraction, exact powers and rational logarithm intervals',
           'log_terms':LOG_TERMS,
           'log_error_bound':'2*z^(2N+1)/((2N+1)*(1-z^2)); dyadic range reduction, |z|<=1/3',
           'seed':'not applicable; deterministic enumeration',
           'parameter_weights':[list(map(str,w)) for w in weights_list],
           'parameter_alphas':list(map(str,alphas)),
           'parameter_eta_over_B':list(map(str,margins)),
           'anchor_configurations':anchors,'parameter_cases':cases,'q_checks':qchecks,
           'maximum_D':maximum_D,'checked_rows_sha256':digest.hexdigest(),
           'actual_triad':real_triad(),
           'scope':'Finite necessary-parameter audit plus one literal base game. General real-input barrier follows from the manuscript, not enumeration.'}
    payload = json.dumps(out,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        with open(args.output,'x') as f: f.write(payload)
    else: print(payload,end='')

if __name__ == '__main__': main()
