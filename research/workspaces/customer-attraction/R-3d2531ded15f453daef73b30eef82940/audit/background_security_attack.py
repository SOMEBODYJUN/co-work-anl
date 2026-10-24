"""Attack the universal fixed-background aggregate security candidate.

This is a discovery experiment, never a positive result for a fixed scale.
SPE terminal sets are retained exactly in a count-state recursion; an ordered
strategy can be reconstructed independently after a candidate is discovered.
"""
from functools import lru_cache
from itertools import combinations_with_replacement
import json
import random
import sys

import numpy as np
from scipy.optimize import linprog


def compositions(n, p):
    if p == 1:
        yield (n,)
        return
    for k in range(n + 1):
        for tail in compositions(n - k, p - 1):
            yield (k,) + tail


def experiment(p, r, prefix, weights, optimize=False):
    masks = np.array(list(weights), dtype=int)
    w = np.array(list(weights.values()), dtype=float)
    inc = np.array([[(a >> j) & 1 for j in range(p)] for a in masks], dtype=int)
    base = inc @ np.array(prefix)

    @lru_cache(None)
    def utility(q):
        den = inc @ np.array(q)
        return (inc.T * np.divide(w, den, out=np.zeros_like(w), where=den > 0)) .sum(axis=1)

    @lru_cache(None)
    def outcomes(q, left):
        if left == 0:
            return frozenset((q,))
        children = []
        floor = -float("inf")
        for a in range(p):
            child = list(q)
            child[a] += 1
            terms = outcomes(tuple(child), left - 1)
            children.append(terms)
            floor = max(floor, min(utility(z)[a] for z in terms))
        return frozenset(z for a, terms in enumerate(children) for z in terms
                         if utility(z)[a] + 1e-9 >= floor)

    terms = outcomes(prefix, r)
    actual = min(terms, key=lambda z: np.dot(np.array(z) - prefix, utility(z)))
    total = float(np.dot(np.array(actual) - prefix, utility(actual)))

    bg = list(compositions(r - 1, p))
    payoff = []
    for k in bg:
        den = 1 + base + inc @ np.array(k)
        payoff.append((inc.T * (w / den)).sum(axis=1))
    payoff = np.array(payoff)
    # Max p-value of the static minimax query. Last variable is v.
    result = linprog(np.r_[np.zeros(p), -1],
                     A_ub=np.c_[-payoff, np.ones(len(bg))],
                     b_ub=np.zeros(len(bg)),
                     A_eq=np.array([np.r_[np.ones(p), 0]]), b_eq=[1],
                     bounds=[(0, None)] * p + [(None, None)], method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    value = result.x[-1]
    report = {"p": p, "r": r, "prefix": prefix,
            "weights": weights, "terminal": actual, "total": total,
            "value": value, "query": result.x[:-1].tolist(),
            "gap": total-r*value, "terminals": len(terms)}

    if optimize:
        # Reconstruct a full ordered policy supporting actual, including every
        # off-path threat. States with equal counts need not receive same leaf.
        coef_cache = {}

        def coefficients(z):
            if z not in coef_cache:
                den = inc @ np.array(z)
                coef_cache[z] = inc.T * np.divide(np.ones(len(w)), den,
                                  out=np.zeros(len(w)), where=den > 0)
            return coef_cache[z]

        rows = []
        policy = {}

        def support(q, left, z, history):
            if left == 0:
                return
            children = []
            floor = -float("inf")
            for a in range(p):
                child = list(q)
                child[a] += 1
                child = tuple(child)
                terms = outcomes(child, left-1)
                worst = min(terms, key=lambda t: utility(t)[a])
                children.append((child, terms, worst))
                floor = max(floor, utility(worst)[a])
            chosen = next(a for a,(child, terms, worst) in enumerate(children)
                          if z in terms and utility(z)[a]+1e-9 >= floor)
            policy[history] = chosen
            for a,(child, terms, worst) in enumerate(children):
                threat = z if a == chosen else worst
                rows.append(coefficients(z)[chosen] - coefficients(threat)[a])
                support(child, left-1, threat, history+(a,))

        support(prefix, r, actual, ())
        gamma = np.array(rows)
        k = inc @ (np.array(actual)-prefix)
        welfare = np.divide(k, base+k, out=np.zeros_like(w), where=base+k > 0)
        static_coefs = []
        for kvec in bg:
            den = 1+base+inc@np.array(kvec)
            static_coefs.append(inc.T/den)
        static_coefs = np.array(static_coefs)
        query = result.x[:-1]
        best_opt = None
        for _ in range(6):
            fixed_query_coefs = np.einsum('bap,a->bp', static_coefs, query)
            lp = linprog(np.r_[welfare, -r],
                         A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],
                                    np.c_[-fixed_query_coefs,np.ones(len(bg))]],
                         b_ub=np.zeros(len(gamma)+len(bg)),
                         A_eq=np.array([np.r_[np.ones(len(w)),0]]),b_eq=[1],
                         bounds=[(0,None)]*len(w)+[(None,None)],method='highs')
            if not lp.success:
                raise RuntimeError(lp.message)
            best_opt = lp.fun
            if best_opt < -1e-8:
                report['optimized'] = {"gap":float(best_opt),
                     "weights":{int(a):float(v) for a,v in zip(masks,lp.x[:-1])},
                     "query":query.tolist(),
                     "policy":{','.join(map(str,h)):a for h,a in policy.items()},
                     "worst_ic":float((gamma@lp.x[:-1]).min())}
                break
            # Security primal at the new multiplicities.
            pay = np.einsum('bap,p->ba',static_coefs,lp.x[:-1])
            qp = linprog(np.r_[np.zeros(p),-1],
                         A_ub=np.c_[-pay,np.ones(len(bg))],b_ub=np.zeros(len(bg)),
                         A_eq=[np.r_[np.ones(p),0]],b_eq=[1],
                         bounds=[(0,None)]*p+[(None,None)],method='highs')
            next_query = qp.x[:-1]
            if np.linalg.norm(next_query-query) < 1e-9:
                break
            query = next_query
        report['optimized_gap'] = best_opt
    return total - r * value, report


if __name__ == "__main__":
    rng = random.Random(90273)
    best = 1e100
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    for it in range(count):
        p = rng.choice([3, 4, 5, 6])
        r = rng.choice([3, 4])
        prefix = tuple(rng.choice([0, 0, 0, 1, 2, 3]) for _ in range(p))
        weights = {a: rng.choice([0, 0, 1, 2, 3, 5, 8, 13])
                   for a in range(1, 2**p)}
        weights = {a:w for a,w in weights.items() if w}
        gap, data = experiment(p, r, prefix, weights, optimize=len(sys.argv)>2)
        if data.get('optimized_gap', 1) < -1e-8:
            print(json.dumps({"iteration":it, **data}), flush=True)
            print("CANDIDATE_OPTIMIZED_COUNTEREXAMPLE",flush=True)
            break
        if gap < best:
            best = gap
            print(json.dumps({"iteration": it, **data}), flush=True)
        if gap < -1e-6:
            print("CANDIDATE_COUNTEREXAMPLE", flush=True)
            break
