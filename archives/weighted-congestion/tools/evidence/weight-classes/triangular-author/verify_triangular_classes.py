#!/usr/bin/env python3
"""Exact finite audit of triangular sorted-potential mixtures.

No external packages, tolerance, floating comparisons or optimizer.
The explicitly listed roots satisfy A=sum(t**j), d=1+t*A with integer t,
so roots, mixture coefficients, weights, costs and margins are rational.
Other parameter values remain the domain of the general proof.
The default writes JSON to stdout; --output NEW_PATH exclusively creates
a new evidence file and refuses to overwrite an existing record.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import argparse
import hashlib
import json
import sys


def ordered_potential(weights, counts, r, degree):
    K = len(weights)
    order = list(range(K-1, r, -1)) + list(range(r+1))
    load = Q(0)
    val = Q(0)
    for i in order:
        for _ in range(counts[i]):
            load += weights[i]
            val += weights[i] * load**degree
    return val


def insertion_audit():
    records = []
    triangular_edges = 0
    blended_edges = 0
    for K, t in [(1,1), (1,2), (2,1), (2,2), (3,1), (3,2), (4,1), (4,2)]:
        alpha = sum(t**j for j in range(K))
        d = 1+t*alpha
        lam = [Q(t**r, alpha) for r in range(K)]
        cum = [sum(lam[:i+1], Q(0)) for i in range(K)]
        assert sum(lam, Q(0)) == 1
        assert alpha == sum(((Q(d-1,alpha))**j for j in range(K)), Q(0))
        for i in range(K):
            assert 1+(d-1)*sum(lam[:i], Q(0)) == alpha*cum[i]
        count_max = 3 if K <= 2 else 2
        local_triangular = 0
        local_blended = 0
        spectra = [tuple(Q(3)**(-i) for i in range(K)),
                   tuple(Q(1001,3)**(-i) for i in range(K))]
        for weights in spectra:
            assert all(weights[i] > weights[i+1] for i in range(K-1))
            for counts in product(range(count_max+1), repeat=K):
                for degree in range(d+1):
                    old = [ordered_potential(weights, counts, r, degree) for r in range(K)]
                    for i in range(K):
                        nc = list(counts)
                        nc[i] += 1
                        Y = sum(weights[j] * nc[j] for j in range(K))
                        weighted_cost = weights[i] * Y**degree
                        new = [ordered_potential(weights, nc, r, degree) for r in range(K)]
                        delta = [new[r]-old[r] for r in range(K)]
                        for r in range(K):
                            if r < i:
                                assert weighted_cost <= delta[r] <= d*weighted_cost
                            elif r == i:
                                assert delta[r] == weighted_cost
                            else:
                                assert 0 <= delta[r] <= weighted_cost
                            local_triangular += 1
                        mixed = sum((lam[r]*delta[r] for r in range(K)), Q(0))
                        h_cost = cum[i]*weighted_cost
                        assert h_cost <= mixed <= alpha*h_cost
                        local_blended += 1
        triangular_edges += local_triangular
        blended_edges += local_blended
        records.append({"k":K,"integer_t":t,"d":d,"exact_root_A":alpha,
                        "lambdas":[str(x) for x in lam],
                        "cumulative_multipliers_per_weight":[str(x) for x in cum],
                        "weight_spectra":[[str(w) for w in spectrum] for spectrum in spectra],
                        "each_old_count_range":[0,count_max],"degrees":[0,d],
                        "triangular_edges":local_triangular,"blend_edges":local_blended})
    return {"records":records,"triangular_edges":triangular_edges,
            "blended_edges":blended_edges}


def polynomial(coeff, x):
    return sum((a*x**j for j,a in enumerate(coeff)), Q(0))


def shifted_coefficients(coeff, background):
    return [sum((coeff[j]*comb(j,r)*background**(j-r)
                 for j in range(r,len(coeff))), Q(0))
            for r in range(len(coeff))]


def background_rounding_audit():
    # Three mobile players, two rounded types; a fourth player is fixed
    # with a weight from neither type. The two-type optimum at d=7 is A=3.
    d, alpha, t = 7, Q(3), 2
    R = Q(101,100)
    original_w = [Q(4), Q(101,25), Q(101,100), Q(13,7)]
    rounded_w = [Q(4), Q(4), Q(1), Q(13,7)]
    type_of = [0,0,1]
    repr_w = [Q(4),Q(1)]
    lam = [Q(1,3),Q(2,3)]
    cum = [Q(1,3),Q(1)]
    for i in range(3):
        assert rounded_w[i] <= original_w[i] <= R*rounded_w[i]
    strategies = [
        (frozenset({0,1}),frozenset({1,2})),
        (frozenset({0}),frozenset({2})),
        (frozenset(),frozenset({0,2})),
        (frozenset({0,3}),),
    ]
    coeff = [[Q(0)]*(d+1) for _ in range(4)]
    coeff[0][0],coeff[0][1],coeff[0][7] = Q(1),Q(1),Q(2)
    coeff[1][3] = Q(1)
    coeff[2][0],coeff[2][7] = Q(3),Q(1,5)
    # resource 3 has zero costs but a nonzero fixed background
    fixed_load = [original_w[3] if e in strategies[3][0] else Q(0) for e in range(4)]
    shift = [shifted_coefficients(coeff[e],fixed_load[e]) for e in range(4)]
    for coeff_e in shift:
        assert all(a>=0 for a in coeff_e)

    def true_cost(state, weights):
        loads = [sum((weights[i] for i in range(4) if e in state[i]),Q(0))
                 for e in range(4)]
        return [sum((polynomial(coeff[e],loads[e]) for e in state[i]),Q(0))
                for i in range(4)]

    def shifted_cost(state, weights):
        loads = [sum((weights[i] for i in range(3) if e in state[i]),Q(0))
                 for e in range(4)]
        return [sum((polynomial(shift[e],loads[e]) for e in state[i]),Q(0))
                for i in range(3)]

    def phi(state):
        counts = [[sum(type_of[i]==g and e in state[i] for i in range(3))
                   for g in range(2)] for e in range(4)]
        val = Q(0)
        for e in range(4):
            for degree,a in enumerate(shift[e]):
                val += a*sum((lam[r]*ordered_potential(repr_w,counts[e],r,degree)
                              for r in range(2)),Q(0))
        return val

    states = list(product(*strategies))
    cache = {}
    for s in states:
        original_cost = true_cost(s,original_w)
        rounded_cost = true_cost(s,rounded_w)
        assert original_cost[:3] == shifted_cost(s,original_w)
        assert rounded_cost[:3] == shifted_cost(s,rounded_w)
        for i in range(3):
            assert rounded_cost[i] <= original_cost[i] <= R**d*rounded_cost[i]
        cache[s] = (original_cost,rounded_cost,phi(s))
    minval = min(v[2] for v in cache.values())
    minima = [s for s in states if cache[s][2]==minval]
    deviations = 0
    for s in states:
        real,rounded,p = cache[s]
        for i in range(3):
            h = cum[type_of[i]]*rounded_w[i]
            for action in strategies[i]:
                sp = s[:i]+(action,)+s[i+1:]
                real_new,rounded_new,pnew = cache[sp]
                assert pnew-p <= h*(alpha*rounded_new[i]-rounded[i])
                if s in minima:
                    assert rounded[i] <= alpha*rounded_new[i]
                    assert real[i] <= R**d*alpha*real_new[i]
                deviations += 1
    return {"d":d,"exact_root_A":str(alpha),"rounding_R":str(R),
            "lifted_factor":str(R**d*alpha),
            "original_weights":[str(w) for w in original_w],
            "rounded_weights":[str(w) for w in rounded_w],
            "fixed_loads":[str(x) for x in fixed_load],
            "strategies":[[sorted(a) for a in s] for s in strategies],
            "coefficients":[[str(a) for a in v] for v in coeff],
            "shifted_coefficients":[[str(a) for a in v] for v in shift],
            "states":len(states),"mobile_deviations":deviations,
            "rounded_global_minima":len(minima),
            "all_mobile_costs_and_deviations_preserved_by_shift":True,
            "all_lift_inequalities_exact":True}


def run():
    return {"status":"pass","python":sys.version.split()[0],
            "arithmetic":"fractions.Fraction; no tolerance, float or optimizer",
            "seed":None,
            "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "insertion_audit":insertion_audit(),
            "fixed_background_and_rounding":background_rounding_audit(),
            "scope":"explicit finite rational insertion edges and one full 4-player game; not general proof"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    output = json.dumps(run(),ensure_ascii=False,indent=2)+"\n"
    if args.output:
        with args.output.open("x",encoding="utf-8") as f:
            f.write(output)
    else:
        print(output,end="")
