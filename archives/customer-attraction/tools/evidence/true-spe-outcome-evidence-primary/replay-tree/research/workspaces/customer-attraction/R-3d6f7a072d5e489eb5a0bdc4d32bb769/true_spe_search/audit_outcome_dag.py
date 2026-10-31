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


def large_baseline():
    """Known feasible 9/5 example at the same size as the stalled search."""
    p,m = 7,5
    clones = [0]*((1<<p)-1)
    clones[0] = m
    for a in range(1,p): clones[(1<<a)-1] = 1
    objective = d.coverage_row(p,(0,1,2,3,4))
    cone,meta = d.build(p,(m,)+(0,)*(p-1),objective,25,fixed_clones=clones)
    assert cone and d.independently_verify(cone,clones)
    inst = d.instance_from_clones(p,m,clones)
    W = inst.welfare(cone.root); O = inst.optimal_welfare()
    assert Fraction(O,W) == Fraction(9,5)
    out = {'scope':'known feasible instance; fixed multiplicities only',
           'customers_nonzero_types':p,'customers_available_types':(1<<p)-1,
           'integer_clones':clones,'total_unit_customers':sum(clones),
           'milp':meta,'exact_full_history_verified':True,
           'ordered_history_nodes':len(cone.actions),
           'exact_deviation_checks':len(cone.actions)*(p-1),
           'welfare':W,'optimal_welfare':O,'ratio':str(Fraction(O,W))}
    Path(__file__).with_name('dag_baseline_fixed_m5p7.json').write_text(
        json.dumps(d.serializable(out),indent=2)+'\n')
    print(json.dumps(d.serializable({k:v for k,v in out.items() if k!='integer_clones'})))


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
    # Replay fixed-cone duals without rerunning LP or trusting MILP status.
    here = Path(__file__).parent
    certificate = json.loads((here/'fractional_weak_m4_certificate.json').read_text())
    fixed = d.StrategyCone(4,4,{tuple(a['history']):a['action']
                              for a in certificate['actions']})
    proofs = json.loads((here/'m4_new_budget_fixed_cone.json').read_text())
    duals = 0
    for record in proofs['records']:
        proof = record['result']; objective = tuple(map(Fraction,record['objective']))
        clones = proof['integer_clones']; W = d.dot(fixed.welfare,clones)
        assert d.independently_verify(fixed,clones)
        value = d.dot(objective,clones)/W
        assert value == Fraction(proof['value'])
        beta = Fraction(proof['exact_dual_bound'])
        mu = [Fraction(0)]*len(fixed.rows)
        for i,v in proof['dual_support']:
            assert 0 <= i < len(mu) and mu[i] == 0
            mu[i] = Fraction(v)
        assert all(v >= 0 for v in mu)
        assert all(beta*w-sum(v*row[j] for v,row in zip(mu,fixed.rows)) >= objective[j]
                   for j,w in enumerate(fixed.welfare))
        assert beta == value
        duals += 1
    out = {'scope':'finite implementation regression only',
           'fixed_input_positive_welfare_target_checks':matches,
           'successful_full_history_exact_checks':successful,
           'known_sharp_two_topic_regressions':sharp,
           'known_nonmarkov_root_023_accepted_and_exactly_verified':True,
           'same_count_different_action_observed':nonmarkov,
           'exact_fixed_m4_cone_new_budget_optimal_duals':duals,
           'combinatorial_size_formula_checks':formulas}
    target = Path(__file__).with_name('outcome_dag_audit.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'combinatorial_size_formula_checks'}))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--large-baseline',action='store_true')
    args = ap.parse_args()
    if args.large_baseline: large_baseline()
    else: main()
