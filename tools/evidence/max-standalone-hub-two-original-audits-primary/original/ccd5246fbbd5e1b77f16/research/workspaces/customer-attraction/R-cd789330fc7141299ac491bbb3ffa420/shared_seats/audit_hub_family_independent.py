"""Independent unit-customer replay; no author/solver imports."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json
from pathlib import Path


def audit(k):
    M = comb(k, k//2)
    private = M//2-1
    # Unit identities are distinct integers, even for identical preferences.
    topics = [set() for _ in range(k+1)]
    unit = 0
    for subset in combinations(range(k), k//2):
        topics[0].add(unit)
        for a in subset:
            topics[a+1].add(unit)
        unit += 1
    for a in range(1,k+1):
        for _ in range(private):
            topics[a].add(unit)
            unit += 1
    assert unit == M+k*private
    assert len(topics[0]) == M
    assert all(len(topics[a]) == M-1 for a in range(1,k+1))
    assert len({frozenset(a) for a in topics}) == k+1
    inter = comb(k-2,k//2-2)
    assert all(len(topics[a]&topics[b]) == inter for a in range(1,k+1) for b in range(1,k+1) if a!=b)

    # last[a][b] is second player's payoff after first a and second b.
    last = [[F(len(topics[b]-topics[a]))+F(len(topics[a]&topics[b]),2)
             for b in range(k+1)] for a in range(k+1)]
    selector = [1]+[a%k+1 for a in range(1,k+1)]
    for a in range(k+1):
        best = max(last[a])
        br = {b for b in range(k+1) if last[a][b] == best}
        expected = set(range(1,k+1)) if a == 0 else set(range(1,k+1))-{a}
        assert br == expected
        assert selector[a] in br
    root = [last[selector[a]][a] for a in range(k+1)]
    v = F(M-1)-F(inter,2)
    assert root[0] == F(3*M,4)
    assert all(t == v for t in root[1:])
    assert root[1] == max(root) and root[1] > root[0]
    welfare = len(topics[1]|topics[selector[1]])
    optimum = max(len(a|b) for a in topics for b in topics)
    assert welfare == optimum == 2*M-2-inter

    # Direct unit-customer averaging over every ordered iid rival pair.
    iid = []
    for query in range(k+1):
        numerator = 0
        for a,b in product(range(1,k+1),repeat=2):
            for x in topics[query]:
                numerator += 6//(1+int(x in topics[a])+int(x in topics[b]))
        iid.append(F(numerator,6*k*k))
    def g(z):
        return 1-z+z*z/3
    lam = F(M,2)*g(F(1,2))+private*g(F(1,k))
    assert iid[0] == M*g(F(1,2)) == F(7*M,12)
    assert all(value == lam for value in iid[1:])
    assert iid[0] < lam
    assert lam > root[0]
    assert v > lam
    # q has no hub mass. Averaging its true two-player root deviations gives v.
    average_real_root = sum(root[1:],F(0))/k
    assert average_real_root == v > lam
    delta_numerator = M*(k*k-12*k+4)-8*(3*k*k-3*k+1)
    assert lam-F(3*M,4) == F(delta_numerator,24*k*k) > 0
    return {'k':k,'topics':k+1,'unit_customers':unit,'M':M,'private_each':private,
            'intersection':inter,'histories':k+2,
            'all_comparisons_including_own':(k+1)**2+(k+1),
            'hub_real_root':str(root[0]),'peripheral_real_root':str(v),
            'hub_static_iid_query':str(iid[0]),'lambda3':str(lam),
            'lambda3_minus_hub_real_root':str(lam-root[0]),
            'q_average_real_root':str(average_real_root),
            'W':welfare,'OPT2':optimum}

results = [audit(12),audit(14)]
# Finite regression only; all-even-k reasoning is in the review.
for k in range(12,102,2):
    M=comb(k,k//2)
    assert M>=6*k*k
    assert M*(k*k-12*k+4)-8*(3*k*k-3*k+1)>0
out={'status':'pass','source':'independent unit construction and exact Fraction replay',
     'expanded_instances':results,'finite_scalar_regression':'even k=12,...,100'}
path=Path(__file__).with_name('hub_family_independent_audit.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
