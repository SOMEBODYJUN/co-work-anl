"""Exact finite audit; this is evidence, not a proof of the candidate theorem."""
from fractions import Fraction as F
from itertools import product, combinations
import json

E = tuple(range(4))
all_bases = tuple(frozenset(b) for b in combinations(E, 2))
B1 = tuple(b for b in all_bases if b != frozenset((0, 1)))
B2 = tuple(b for b in all_bases if b != frozenset((0, 2)))
q1 = {frozenset((0, 2)): F(1,10), frozenset((0, 3)): F(1,10),
      frozenset((1, 2)): F(1,5), frozenset((1, 3)): F(7,20),
      frozenset((2, 3)): F(1,4)}
q2 = {frozenset((0, 1)): F(1,10), frozenset((0, 3)): F(1,10),
      frozenset((1, 2)): F(1,5), frozenset((1, 3)): F(1,4),
      frozenset((2, 3)): F(7,20)}
p = tuple(F(x,20) for x in (4,11,11,14))
spaces, qs = (B1,B2,B1), (q1,q2,q1)
n = len(spaces)
for q in qs:
    assert sum(q.values()) == 1 and all(v > 0 for v in q.values())
    assert tuple(sum(v for b,v in q.items() if e in b) for e in E) == p

def delay(e,k):
    return (e+1)*k*k + e*k

def distribution(core,q,eps):
    return {b: eps*v + (1-eps if b == core else 0) for b,v in q.items()}

def pure_core_cost(i,base,profile,eps):
    """Directly enumerate full opponents' strategies, not resource Bernoullis."""
    others = [j for j in range(n) if j != i]
    ds = [distribution(profile[j],qs[j],eps) for j in others]
    ans = F(0)
    for choices in product(*(spaces[j] for j in others)):
        probability = F(1)
        for b,d in zip(choices,ds): probability *= d[b]
        ans += probability*sum(delay(e,1+sum(e in b for b in choices)) for e in base)
    return ans

def transformed_delay(e,k,eps):
    """Independent Bernoulli convolution, a separate calculation."""
    h, f = 1-eps+eps*p[e], eps*p[e]
    probs = [h]*(k-1)+[f]*(n-k)
    ans = F(0)
    for bits in product((0,1),repeat=n-1):
        pr = F(1)
        for bit,a in zip(bits,probs): pr *= a if bit else 1-a
        ans += pr*delay(e,1+sum(bits))
    return ans

comparisons = 0
for eps in (F(1,10), F(1,100)):
    for e in E:
        assert all(transformed_delay(e,k,eps) <= transformed_delay(e,k+1,eps)
                   for k in range(1,n))
    for profile in product(*spaces):
        for i in range(n):
            current = pure_core_cost(i,profile[i],profile,eps)
            for alternative in spaces[i]:
                alt = pure_core_cost(i,alternative,profile,eps)
                loads_without = {e:sum(e in profile[j] for j in range(n) if j != i)
                                 for e in E}
                transformed_diff = (sum(transformed_delay(e,loads_without[e]+1,eps)
                                        for e in alternative)
                                    - sum(transformed_delay(e,loads_without[e]+1,eps)
                                          for e in profile[i]))
                assert alt-current == transformed_diff
                # The actual mixed payoff difference is (1-eps)*(alt-current):
                # the own-tremble term cancels because opponents are fixed.
                own_tremble = sum(qs[i][b]*pure_core_cost(i,b,profile,eps) for b in spaces[i])
                old_mixed = (1-eps)*current+eps*own_tremble
                new_mixed = (1-eps)*alt+eps*own_tremble
                assert new_mixed-old_mixed == (1-eps)*transformed_diff
                comparisons += 1

# Independent affine case: different full-support distributions, unequal marginals.
qs_affine = tuple({b:F(1,len(space)) for b in space} for space in spaces)
ps_affine = tuple(tuple(sum(q[b] for b in q if e in b) for e in E) for q in qs_affine)
assert ps_affine[0] != ps_affine[1]
affine_checks = 0
for eps in (F(1,10),F(1,100)):
    for profile in product(*spaces):
        for i in range(n):
            others = [j for j in range(n) if j != i]
            ds = [distribution(profile[j],qs_affine[j],eps) for j in others]
            for e in E:
                a,b = e+1,e
                direct = F(0)
                for choices in product(*(spaces[j] for j in others)):
                    pr = F(1)
                    for base,d in zip(choices,ds): pr *= d[base]
                    direct += pr*(a*(1+sum(e in base for base in choices))+b)
                k = 1+sum(e in profile[j] for j in others)
                formula = a*(1-eps)*k+b+eps*a*(1+sum(ps_affine[j][e] for j in range(n))-ps_affine[i][e])
                assert direct == formula
                affine_checks += 1

# Counterexample to arXiv:2401.03861v1 Lemma 3.7's strict local implication.
cost = (2,2,1,1)
old = frozenset((0,1))
single_exchanges = [b for b in all_bases if len(b-old)==1]
assert max(cost[e] for e in old)==2
assert all(max(cost[e] for e in b)==2 for b in single_exchanges)
assert min(max(cost[e] for e in b) for b in all_bases)==1

print(json.dumps({"arithmetic":"fractions.Fraction", "seed":None,
  "players":n,"resources":len(E),"profiles":125,
  "epsilon":["1/10","1/100"],"payoff_difference_checks":comparisons,
  "unequal_marginal_affine_checks":affine_checks,
  "common_marginal":[str(x) for x in p],
  "strict_local_counterexample":{"matroid":"U(2,4)","costs":cost,
  "current":[0,1],"current_cost":2,"all_single_exchange_costs":2,
  "global_optimum_cost":1},
  "status":"finite audit passed; candidate universal theorem remains unreviewed"},indent=2))
