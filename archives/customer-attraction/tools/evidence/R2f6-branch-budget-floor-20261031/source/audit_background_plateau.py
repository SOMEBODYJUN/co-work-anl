"""Independent reconstruction of the background-security plateau witness.

No source strategy, source solver, or source audit is imported.  Five distinct
unit customers are explicit.  This verifies a general candidate's finite main
tree; the all-B justification is the exact pair-ranking calculation in the
companion review.
"""
from collections import Counter
from fractions import Fraction as F
from functools import cache
from itertools import product
import json
from pathlib import Path

M = 4
THEMES = ((0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4),
          (0,), (1,), (2,), (3,), (4,))
PAIRS = ((1, 1), (1, 2), (1, 3), (2, 2), (1, 4),
         (2, 3), (2, 4), (3, 3), (3, 4), (4, 4))
RANK = {pair: 10-i for i, pair in enumerate(PAIRS)}
TARGET = (1, 1, 1, 1, 0, 0)

def plus(c, a):
    return c[:a] + (c[a]+1,) + c[a+1:]

def load(z):
    out = [0]*5
    for a in z:
        for x in THEMES[a]:
            out[x] += 1
    return out

def count_load(c):
    return load(tuple(a for a, n in enumerate(c) for _ in range(n)))

def ordinal(a, c):
    ell = count_load(c)
    return RANK[tuple(sorted(ell[x] for x in THEMES[a]))]

@cache
def outcomes(c):
    if sum(c) == M:
        return frozenset((c,))
    child = [outcomes(plus(c, a)) for a in range(6)]
    threshold = max(min(ordinal(a, z) for z in child[a]) for a in range(6))
    return frozenset(z for a in range(6) for z in child[a]
                     if ordinal(a, z) >= threshold)

main_policy = {}
def realize(h, c, target, force=None):
    if len(h) == M:
        assert c == target
        return
    child = [outcomes(plus(c, a)) for a in range(6)]
    threshold = max(min(ordinal(a, z) for z in child[a]) for a in range(6))
    choices = [a for a in range(6) if target in child[a]
               and ordinal(a, target) >= threshold]
    chosen = choices[0] if force is None else force
    assert chosen in choices
    main_policy[h] = chosen
    for a in range(6):
        goal = target if a == chosen else min(child[a], key=lambda z: (ordinal(a,z), z))
        realize(h+(a,), plus(c,a), goal)

zero = (0,)*6
assert TARGET in outcomes(zero)
realize((), zero, TARGET, force=0)

full_policy = {}
@cache
def canonical(h):
    if len(h) == M:
        return h
    children = [canonical(h+(a,)) for a in range(11)]
    def score(z, a):
        ell = load(z)
        return RANK[tuple(sorted(ell[x] for x in THEMES[a]))]
    # Every main payoff strictly exceeds every singleton payoff for B>=3.
    chosen = max(range(6), key=lambda a: (score(children[a],a), -a))
    full_policy[h] = chosen
    return children[chosen]

def graft(h):
    if len(h) == M:
        return
    if all(a < 6 for a in h):
        full_policy[h] = main_policy[h]
        for a in range(11):
            graft(h+(a,))
    else:
        canonical(h)

graft(())
assert len(full_policy) == sum(11**d for d in range(M))

def terminal(h):
    while len(h) < M:
        h += (full_policy[h],)
    return h

def utility(z, i, B):
    ell = load(z)
    return sum((F(1,B+ell[x]) for x in THEMES[z[i]]), F())

def check(B):
    slacks = []
    for d in range(M):
        for h in product(range(11), repeat=d):
            actual = terminal(h)
            for a in range(11):
                slacks.append(utility(actual,d,B)-utility(terminal(h+(a,)),d,B))
    assert min(slacks) >= 0
    value = F(3,2*(B+2)) + F(1,2*(B+3))
    query = [F(1,6)]*6 + [F(0)]*5
    def f(a, bg):
        ell = load(bg)
        return sum((F(1,B+1+ell[x]) for x in THEMES[a]),F())
    lower = min(sum((query[a]*f(a,bg) for a in range(11)),F())
                for bg in product(range(11), repeat=3))
    assert lower == value
    # Competitor mixtures contain the frozen root 0, so certify both upper bounds.
    backgrounds = ((0,4,2), (0,4,5))
    caps = [sum((F(1,2)*f(a,bg) for bg in backgrounds),F())
            for a in range(11)]
    assert max(caps) == value
    z = terminal(())
    u = utility(z,0,B)
    assert Counter(z) == Counter({a:n for a,n in enumerate(TARGET) if n})
    assert value-u == F(1,2*(B+2)*(B+3))
    return dict(B=B,histories=len(full_policy),comparisons=len(slacks),
                minimum_slack=str(min(slacks)),actual=z,
                root_utility=str(u),v4=str(value),v3_after_0=str(value),
                plateau_gap=str(value-u),static_lower=str(lower),
                static_upper_queries=list(map(str,caps)))

if __name__ == '__main__':
    result = dict(status='PASS',scope='Independent finite certificate; all-B proof in companion review.',
                  main_states=outcomes.cache_info().currsize,
                  main_histories=len(main_policy),
                  audits=[check(B) for B in (3,4,10)],
                  full_policy=[dict(history=h,action=a)
                               for h,a in sorted(full_policy.items(),key=lambda z:(len(z[0]),z[0]))])
    dest = Path(__file__).with_name('background_plateau_independent_audit.json')
    dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='full_policy'},ensure_ascii=False,indent=2))
