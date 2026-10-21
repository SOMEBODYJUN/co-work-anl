"""Small independent-oracle regression of the numerical DAG implementation.

Not a universal welfare proof and not an exact MILP infeasibility certificate.
Successful witnesses are checked with exact full-history payoff comparisons.
"""
from fractions import Fraction
from itertools import product
import json
from math import comb, prod
from pathlib import Path

import outcome_dag_milp as d


def main():
    matches = successful = 0
    for m in (1,2,3):
        for v in product(range(2),repeat=3):
            solver = d.ExactSPESolver(d.instance_from_clones(2,m,v))
            outcomes = solver.outcomes()
            for q in d.counts(2,m):
                if not solver.instance.welfare(q):
                    continue
                cone,meta = d.build(2,q,[0]*3,3,fixed_clones=v)
                if bool(cone) != (q in outcomes):
                    raise AssertionError((m,v,q,meta))
                if cone:
                    assert d.independently_verify(cone,v)
                    successful += 1
                matches += 1
    sharp = []
    for m in (2,3):
        cone,meta = d.build(2,(m,0),[1,1,1],10)
        assert cone
        proof = d.exact_optimize(cone,[1,1,1])
        assert proof['certified'] and proof['value'] == Fraction(m+1,m)
        sharp.append({'players':m,'exact_ratio':str(proof['value'])})
    # A previously documented real failure of count-Markov reduction.
    source = d.ROOT / 'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/strategy_duality/markov_obstruction_report.json'
    old = json.loads(source.read_text())
    cone,meta = d.build(5,(1,0,1,1,0),[0]*31,15,fixed_clones=old['legal_types'])
    assert cone and d.independently_verify(cone,old['legal_types'])
    nonmarkov = any(len(h)==len(hh) and sorted(h)==sorted(hh) and a != b
                   for h,a in cone.actions.items() for hh,b in cone.actions.items())
    assert nonmarkov
    formulas = []
    for p in range(1,7):
        for m in range(1,6):
            actual_y = sum(prod(v+1 for v in c) for c in d.counts(p,m))
            actual_z = p*sum(prod(v+1 for v in c) for c in d.counts(p,m-1))
            assert actual_y == comb(m+2*p-1,2*p-1)
            assert actual_z == p*comb(m+2*p-2,2*p-1)
            formulas.append({'topics':p,'players':m,'y':actual_y,'z_or_x':actual_z})
    out = {'scope':'finite implementation regression only',
           'fixed_input_positive_welfare_target_checks':matches,
           'successful_full_history_exact_checks':successful,
           'known_sharp_two_topic_regressions':sharp,
           'known_nonmarkov_root_023_accepted_and_exactly_verified':True,
           'same_count_different_action_observed':nonmarkov,
           'combinatorial_size_formula_checks':formulas}
    target = Path(__file__).with_name('outcome_dag_audit.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'combinatorial_size_formula_checks'}))


if __name__ == '__main__': main()
