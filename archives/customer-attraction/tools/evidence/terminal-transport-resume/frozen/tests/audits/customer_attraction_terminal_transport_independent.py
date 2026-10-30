#!/usr/bin/env python3
"""Independent Fraction audit of CA-TERMINAL-REPLY-DUAL-LIFT.

Extracted from the independent reviewer's from-scratch implementation.
Imports neither the primary audit nor the model/solver. Defaults to print only.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json

def terminal(actions, h, n):
    while len(h) < n:
        h += (actions[h],)
    return h


def coefficient(mask, a, final):
    if not mask >> a & 1:
        return F(0)
    return F(1, sum((mask >> t) & 1 for t in final))


def review_leaf():
    m,n = 3,3
    actions = {():2, (0,):2, (1,):1, (2,):0}
    leaves = [2,2,1,2,2,2,2,1,1]
    actions.update({h:leaves[3*h[0]+h[1]] for h in product(range(m),repeat=2)})
    histories = [h for k in range(n) for h in product(range(m),repeat=k)]
    original_root = terminal(actions,(),n)
    actual_prefix = original_root[:-1]
    counts = lambda h: tuple(h.count(a) for a in range(m))
    representatives = {}
    for h in product(range(m),repeat=n-1):
        representatives.setdefault(counts(h),h)
    representatives[counts(actual_prefix)] = actual_prefix
    canonical = dict(actions)
    for h in product(range(m),repeat=n-1):
        canonical[h] = actions[representatives[counts(h)]]
    assert terminal(canonical,(),n) == original_root

    def gamma(strategy,h,a,mask):
        return coefficient(mask,strategy[h],terminal(strategy,h,n))-coefficient(mask,a,terminal(strategy,h+(a,),n))

    def delta(leaf,S,mask):
        old,new = actions[leaf],canonical[leaf]
        p = sum((mask >> t)&1 for t in leaf)
        numerator = ((mask >> S)&1)*(((mask >> old)&1)-((mask >> new)&1))
        return F(numerator,p*(p+1)) if numerator else F(0)

    original_slacks, canonical_negative = [], []
    identity_checks, reciprocal_checks, rank_checks = 0,0,0
    positive_types = (3,6,4)  # clients a:{A,B}; b:{B,C}; c:{C}
    for h in histories:
        for a in range(m):
            original = sum((gamma(actions,h,a,T) for T in positive_types),F(0))
            new = sum((gamma(canonical,h,a,T) for T in positive_types),F(0))
            original_slacks.append(original)
            if new < 0:
                canonical_negative.append({"history":list(h),"deviation":a,"slack":str(new)})
            for T in range(1,1<<m):
                if len(h) < n-1:
                    target = terminal(actions,h,n)[:-1]
                    source = terminal(actions,h+(a,),n)[:-1]
                    rhs = gamma(actions,h,a,T)+delta(target,actions[h],T)-delta(source,a,T)
                else:
                    g = representatives[counts(h)]
                    rhs = gamma(actions,h,a,T)+gamma(actions,g,actions[h],T)
                assert gamma(canonical,h,a,T) == rhs
                identity_checks += 1
            if len(h) < n-1:
                target = terminal(actions,h,n)[:-1]
                source = terminal(actions,h+(a,),n)[:-1]
                def rank(leaf):
                    return sum(leaf[j] != actions[leaf[:j]] for j in range(n-1))
                assert rank(source)-rank(target) == (a != actions[h])
                rank_checks += 1
    assert min(original_slacks) >= 0
    assert canonical_negative == [{"history":[2],"deviation":1,"slack":"-1/3"}]
    for h in product(range(m),repeat=n-1):
        g = representatives[counts(h)]
        for T in range(1,1<<m):
            assert gamma(actions,h,actions[g],T) == -gamma(actions,g,actions[h],T)
            reciprocal_checks += 1

    # Zero transfer is weaker than conservation at nonrepresentatives.
    # This genuine row starts at a nonrepresentative whose delta is zero.
    zero_E_h,zero_E_action = (1,),0
    zero_E_target = terminal(actions,zero_E_h,n)[:-1]
    zero_E_source = terminal(actions,zero_E_h+(zero_E_action,),n)[:-1]
    assert zero_E_source != representatives[counts(zero_E_source)]
    assert zero_E_source == (1,0) and zero_E_target == (1,1)
    assert all(delta(zero_E_target,actions[zero_E_h],T)-delta(zero_E_source,zero_E_action,T) == 0
               for T in range(1,1<<m))

    # Exercise explicit lift with arbitrary nonnegative weights, without
    # falsely asserting that their transfer residual is nonnegative.
    lambdas = {(h,a):F(1+len(h)+a,3) for h in histories for a in range(m)}
    lifted = {(h,a):F(0) for h in histories for a in range(m)}
    for (h,a),weight in lambdas.items():
        lifted[h,a] += weight
        if len(h) == n-1:
            g = representatives[counts(h)]
            lifted[g,actions[h]] += weight
    assert all(x >= 0 for x in lifted.values())
    transfer = []
    for T in range(1,1<<m):
        E = F(0)
        for (h,a),weight in lambdas.items():
            if len(h) < n-1:
                target = terminal(actions,h,n)[:-1]
                source = terminal(actions,h+(a,),n)[:-1]
                E += weight*(delta(target,actions[h],T)-delta(source,a,T))
        lhs = sum((weight*gamma(canonical,h,a,T) for (h,a),weight in lambdas.items()),F(0))
        rhs = sum((weight*gamma(actions,h,a,T) for (h,a),weight in lifted.items()),F(0))+E
        assert lhs == rhs
        transfer.append(str(E))
    result = {"status":"PASS", "original_root":list(original_root),"root_preserved":True,
              "original_SPE_comparisons":len(original_slacks),"canonical_negative":canonical_negative,
              "all_type_transformed_gamma_identities":identity_checks,
              "all_type_reciprocal_gauges":reciprocal_checks,"edge_rank_checks":rank_checks,
              "arbitrary_nonnegative_lambda_lift_transfer":transfer,
              "zero_E_nonrepresentative_source_example":{
                  "row_history":list(zero_E_h),"deviation":zero_E_action,
                  "source":list(zero_E_source),"target":list(zero_E_target),
                  "source_is_representative":False,"E_identically_zero":True},
              "mathematical_errors":[],
              "wording_corrections_acknowledged":[
                  "Graph source is ell_ha and graph target is ell_h.",
                  "Nonrepresentative conservation and representative endpoints are sufficient, not necessary for zero E."
              ],
              "important_correction":"Genuine incumbent-transfer edges lower deviation-count rank by exactly one: DAG; no nontrivial cycles.",
              "scope":"Conditional explicit lift given canonical certificate and nonnegative residual; no construction of universal lambda or debt budget"}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Exclusively create a new JSON report")
    args = parser.parse_args()
    result = review_leaf()
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output is not None:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
    print(rendered, end="")
