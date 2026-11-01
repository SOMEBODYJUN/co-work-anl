"""Independent arithmetic audit of the eight-label terminal-BR menu.

No canonical CAG, source author code, equilibrium solver, LP or floating point.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json
from pathlib import Path

TRIPLES = tuple(frozenset((i, (i+1)%8, (i+2)%8)) for i in range(8))
PAIRS = tuple(frozenset((i, i+4)) for i in range(4))
EXPECTED_BR = ({3,5}, {3,6}, {5}, {5,6}, {1,2,3,5,6,7}, {2,3}, {3}, {2,5})


def coeff(path, who):
    return tuple(sum((F(1, sum(j in block for j in path))
                      for block in types if path[who] in block), F())
                 for types in (TRIPLES, PAIRS))


def evaluate(c, a, b):
    return c[0]*a+c[1]*b


def static_coeff(background, query):
    return tuple(sum((F(1, 1+sum(j in block for j in background))
                      for block in types if query in block), F())
                 for types in (TRIPLES, PAIRS))


def units(a, b):
    return tuple(block for block in TRIPLES for _ in range(a)) + tuple(
        block for block in PAIRS for _ in range(b))


def unit_utility(customers, path, who):
    return sum((F(1, sum(j in block for j in path))
                for block in customers if path[who] in block), F())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    vcoeff = (F(23,16), F(5,8))
    backgrounds = tuple(combinations_with_replacement(range(8), 3))
    uniform_lower_checks = 0
    minimizers = []
    for background in backgrounds:
        values = [static_coeff(background, q) for q in range(8)]
        avg = tuple(sum((v[j] for v in values), F())/8 for j in range(2))
        assert all(x >= y for x,y in zip(avg, vcoeff))
        uniform_lower_checks += 1
        if avg == vcoeff:
            minimizers.append(background)
    upper_distribution = tuple(tuple((x+i)%8 for x in (0,3,6)) for i in range(8))
    for q in range(8):
        avg = tuple(sum((static_coeff(bg,q)[j] for bg in upper_distribution),F())/8
                    for j in range(2))
        assert avg == vcoeff

    menu_checks = terminal_coeff_checks = 0
    for i in range(8):
        path = (i,(i+4)%8,(i+1)%8)
        assert coeff(path,0) == (F(2),F(1,2))
        assert coeff(path,1) == (F(3),F(1,2))
        assert coeff(path,2) == (F(2),F(1))
        menu_checks += 3
        for j in range(8):
            last = [coeff((i,(i+j)%8,k),2) for k in range(8)]
            expected = {(i+x)%8 for x in EXPECTED_BR[j]}
            best = last[next(iter(expected))]
            for k,c in enumerate(last):
                delta = tuple(x-y for x,y in zip(best,c))
                # b=a+t, a,t strictly positive: this checks the whole cone.
                assert delta[0]+delta[1] >= 0 and delta[1] >= 0
                if k in expected:
                    assert delta == (0,0)
                else:
                    assert delta[0]+delta[1] > 0 or delta[1] > 0
                terminal_coeff_checks += 1

    unique_last = [coeff((0,2,k),2) for k in range(8)]
    for k,c in enumerate(unique_last):
        delta = tuple(x-y for x,y in zip(unique_last[5],c))
        assert delta[0] >= 0 and delta[1] >= 0
        if k != 5:
            assert delta[0] > 0  # a>0, any b>=0 suffices.
    assert coeff((0,2,5),1) == (F(5,2), F(1))

    numeric = []
    for a,b in ((1,5),(2,9),(2,25),(1,1),(1,0),(0,1),(0,0)):
        customers = units(a,b)
        numeric_checks = 0
        for i in range(8):
            for j in range(8):
                for k in range(8):
                    path=(i,j,k)
                    for who in range(3):
                        assert unit_utility(customers,path,who) == evaluate(coeff(path,who),a,b)
                        numeric_checks += 1
        br02_values = [unit_utility(customers,(0,2,k),2) for k in range(8)]
        br02 = [k for k,value in enumerate(br02_values) if value == max(br02_values)]
        d,e,f = (evaluate(c,a,b) for c in ((F(2),F(1,2)),(F(3),F(1,2)),(F(2),F(1))))
        v = evaluate(vcoeff,a,b)
        assert v-d == F(2*b-9*a,16)
        assert e-v == F(25*a-2*b,16)
        assert f-v == F(9*a+6*b,16)
        deviation = unit_utility(customers,(0,2,5),1)
        assert deviation-e == F(b-a,2)
        numeric.append({"a":a,"b":b,"unit_customers":len(customers),
                        "terminal_payoff_checks":numeric_checks,
                        "d":str(d),"e":str(e),"f":str(f),"v4":str(v),
                        "br_after_0_2":br02,"second_deviation_gain":str(deviation-e)})

    report = {"status":"independent_exact_pass",
              "blind_reconstruction": "Proof and symbolic tables were written before reading the source proof.",
              "static_uniform_lower_backgrounds":uniform_lower_checks,
              "matching_static_upper_distribution":upper_distribution,
              "common_lower_minimizers":minimizers,
              "menu_payoff_coefficients_checked":menu_checks,
              "all_terminal_coefficients_checked_on_a_positive_b_greater_a":terminal_coeff_checks,
              "last_after_0_2_coefficients_a_b":[[str(x) for x in c] for c in unique_last],
              "numeric_unit_cases":numeric,
              "limits":"These are a terminal-BR menu and a second-player obstruction, not a complete SPE or a half-coverage counterexample."}
    payload=json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        with args.output.open("x") as f:
            f.write(payload)
    print(payload)


if __name__ == "__main__":
    main()
