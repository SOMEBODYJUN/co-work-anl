"""Exact toy checks and exploratory LP; no numerical experiment is a proof.

Reproduce: python toy_checks.py
Deterministic enumeration; short-strategy samples use seed 20261020.
SciPy LP proposes rational coefficients; all
reported finite-grid inequalities are then checked with Fraction.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random
from scipy.optimize import linprog


def two_player_counterexample():
    weights = [F(1), F(2)]
    strategies = [[{0, 1}, {2, 3}], [{0, 2}, {1, 3}]]
    def cost(profile, i):
        out = F(0)
        for e in strategies[i][profile[i]]:
            load = sum(weights[j] for j in range(2) if e in strategies[j][profile[j]])
            out += load * load if e in (0, 3) else F(9, 2)*load
        return out
    rows = []
    for p in product(range(2), repeat=2):
        c = [cost(p, i) for i in range(2)]
        ratios = []
        for i in range(2):
            q = list(p); q[i] = 1 - q[i]
            ratios.append(c[i]/cost(q, i))
        rows.append({'profile': p, 'costs': [str(x) for x in c],
                     'worst_deviation_ratio': str(max([F(1)] + ratios))})
    return {'rows': rows, 'minimum_approximation': str(min(F(x['worst_deviation_ratio']) for x in rows)),
            'has_pne': any(F(x['worst_deviation_ratio']) == 1 for x in rows)}


def monomial_row(a, b, w):
    # Existing users: a unit users and b users of weight 2. Adding player w.
    L, M2 = a+2*b, a+4*b
    denominator = w*(L+w)**2
    return [F((L+w)**3 - L**3, denominator),
            F((L+w)*(M2+w*w) - L*M2, denominator),
            F(w**3, denominator)]


def moment_potential_lp(limit):
    rows = [monomial_row(a,b,w) for a in range(limit+1)
            for b in range(limit+1-a) for w in (1,2)]
    # phi=A L^3+B L M2+C M3. Need 1 <= delta phi / (w c) <= alpha.
    A, rhs = [], []
    for r in rows:
        A.extend([[float(x) for x in r]+[-1], [-float(x) for x in r]+[0]])
        rhs.extend([0,-1])
    sol = linprog([0,0,0,1], A_ub=A, b_ub=rhs,
                  bounds=[(None,None)]*3+[(1,None)], method='highs')
    assert sol.success, sol.message
    coefs = [F(float(x)).limit_denominator(1000000) for x in sol.x[:3]]
    exact = [sum(x*y for x,y in zip(coefs,r)) for r in rows]
    lo, hi = min(exact), max(exact)
    assert lo > 0
    normalized = [x/lo for x in coefs]
    return {'existing_user_limit':limit, 'number_local_tests':len(rows),
            'proposed_ABC':[str(x) for x in coefs], 'finite_grid_ratio':str(hi/lo),
            'float_optimum':sol.fun, 'normalized_ABC':[str(x) for x in normalized],
            'note':'Finite grid only; unrestricted concurrency and arbitrary weights not certified.'}


def count_polynomial_lp(degree, limit):
    powers = [(u,v) for total in range(1, degree+2) for u in range(total+1)
              for v in [total-u]]
    rows = []
    for a in range(limit+1):
        for b in range(limit+1-a):
            for w in (1,2):
                aa,bb = (a+1,b) if w == 1 else (a,b+1)
                denom = w*(a+2*b+w)**degree
                rows.append([F(aa**u*bb**v-a**u*b**v,denom) for u,v in powers])
    constr, rhs = [],[]
    for r in rows:
        constr.extend([[float(x) for x in r]+[-1],[-float(x) for x in r]+[0]])
        rhs.extend([0,-1])
    sol = linprog([0]*len(powers)+[1],A_ub=constr,b_ub=rhs,
                  bounds=[(None,None)]*len(powers)+[(1,None)],method='highs')
    assert sol.success, sol.message
    coefs = [F(float(x)).limit_denominator(1000000) for x in sol.x[:-1]]
    vals = [sum(x*y for x,y in zip(coefs,r)) for r in rows]
    lo,hi = min(vals),max(vals)
    return {'latency_monomial_degree':degree,'existing_user_limit':limit,
            'coefficient_monomials':[[u,v] for u,v in powers],
            'rational_coefficients':[str(c) for c in coefs],
            'finite_grid_ratio':str(hi/lo),'float_optimum':sol.fun,
            'exact_minimum_marginal_ratio':str(lo),'exact_maximum_marginal_ratio':str(hi),
            'note':'Full count-polynomial ansatz. Rationalization gives a candidate, not a global proof or novelty claim.'}


def unweighted_binary_size_two_scan():
    rng = random.Random(20261020)
    n,m,trials=6,6,200
    best = None
    for trial in range(trials):
        strategies=[]
        for i in range(n):
            e=rng.sample(range(m),4)
            strategies.append([set(e[:2]),set(e[2:])])
        slopes=[rng.choice([1,2,4,8]) for e in range(m)]
        offsets=[rng.randrange(4) for e in range(m)]
        profiles=list(product(range(2),repeat=n))
        def loads(p): return [sum(e in strategies[i][p[i]] for i in range(n)) for e in range(m)]
        def potential(p):
            ks=loads(p)
            return sum(slopes[e]*ks[e]*(ks[e]+1)//2+offsets[e]*ks[e] for e in range(m))
        def private_cost(p,i):
            ks=loads(p)
            return sum(slopes[e]*ks[e]+offsets[e] for e in strategies[i][p[i]])
        phis={p:potential(p) for p in profiles}
        dist={};next_profile={}
        for p in sorted(profiles,key=lambda x:phis[x]):
            moves=[]
            for i in range(n):
                q=list(p);q[i]=1-q[i];q=tuple(q)
                assert phis[q]-phis[p] == private_cost(q,i)-private_cost(p,i)
                if phis[q]<phis[p]: moves.append(q)
            q=max(moves,key=lambda x:dist[x]) if moves else None
            dist[p]=0 if q is None else dist[q]+1
            next_profile[p]=q
        start=max(profiles,key=lambda p:dist[p])
        if best is None or dist[start]>best['longest_path_moves']:
            path=[];p=start
            while p is not None:
                path.append({'profile':p,'potential':phis[p]});p=next_profile[p]
            best={'trial':trial,'longest_path_moves':dist[start],
                  'strategies':[[sorted(s) for s in ss] for ss in strategies],
                  'slopes':slopes,'offsets':offsets,'path':path,
                  'number_pne':sum(dist[p]==0 for p in profiles)}
    return {'seed':20261020,'n':n,'m':m,'trials':trials,'states_per_instance':2**n,
            'best_observed':best,'note':'Every improvement graph was fully enumerated; the instance family was sampled. No asymptotic conclusion.'}


if __name__ == '__main__':
    result = {'counterexample':two_player_counterexample(),
              'unweighted_size_two_scan':unweighted_binary_size_two_scan(),
              'moment_potential_grid':[moment_potential_lp(k) for k in (2,5,15,50)],
              'count_polynomial_grid':[count_polynomial_lp(d,k) for d in (2,3) for k in (10,30,50)]}
    candidate = result['count_polynomial_grid'][-1]
    powers = candidate['coefficient_monomials']
    coeffs = list(map(F,candidate['rational_coefficients']))
    violations = []
    for a,b,w in [(100,0,2),(1000,0,2),(10000,0,2)]:
        aa,bb = (a+1,b) if w == 1 else (a,b+1)
        ratio = sum(c*(aa**u*bb**v-a**u*b**v) for c,(u,v) in zip(coeffs,powers))/(w*(a+2*b+w)**3)
        violations.append({'a':a,'b':b,'adding_weight':w,'exact_ratio':str(ratio),
                           'violates_normalized_lower_bound':ratio < 1})
    result['out_of_grid_falsification_of_cubic_50_user_candidate'] = violations
    sorted_checks=[]
    for d in (2,3):
        def descending_integral(a,b):
            return sum(2*(2*j)**d for j in range(1,b+1))+sum((2*b+j)**d for j in range(1,a+1))
        ratios=[F(descending_integral(a+(w==1),b+(w==2))-descending_integral(a,b),w*(a+2*b+w)**d)
                for a in range(51) for b in range(51-a) for w in (1,2)]
        sorted_checks.append({'degree':d,'existing_user_limit':50,
                              'exact_distortion':str(max(ratios)/min(ratios))})
    result['descending_discrete_integral_baseline'] = sorted_checks
    out = Path(__file__).with_name('toy_output.json')
    out.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
