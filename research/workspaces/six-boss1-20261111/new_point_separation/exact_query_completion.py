#!/usr/bin/env python3
"""A fresh exact common completion of the specified 81 queries at ZZ13931.

B4's old conditional product fails on new-to-Z, orbit (1,0).  Replace that
orbit by a rational sorted transportation; every other block keeps product.
The result is only a certificate on the explicitly specified marginal domain.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
RUN = HERE.parent
TAIL = RUN/'tail_constraints'
sys.path.insert(0, str(TAIL))
from transport_separator import Point, STATES, row_specs, budgets, primitive_cost, serial, discover


def make_family(point, family):
    specs = row_specs(point.labels[family])
    rhs = budgets(point, family, specs)
    product_cost = [F() for _ in specs]
    costs = [F() for _ in specs]
    blocks = []
    full_pairs = zero_blocks = positive_flows = 0
    for block in point.blocks(family):
        states = block.family_states
        mu = point.mass[block.hist_column]
        nr, nc = 4, len(states)
        full_pairs += nr*nc
        assert sum(block.group.rho, F()) == mu == sum((s.mass for s in states), F())
        if not mu:
            assert not any(block.group.rho) and not any(s.mass for s in states)
            zero_blocks += 1
            continue
        product = [[rho*s.mass/mu for s in states] for rho in block.group.rho]
        repair = family == 'B4' and block.group.orbit == (1, 0)
        rule = 'Z-first sorted transportation' if repair else 'conditional product'
        if repair:
            flow = [[F() for _ in states] for _ in range(4)]
            residual_old = list(block.group.rho)
            residual_new = [s.mass for s in states]
            # High terminal denominators are cheapest for the new terminal's
            # query to Z.  Keep all four old states, not only the Z marginal.
            order = sorted(range(nc), key=lambda j:(-states[j].terminal_denom, states[j].column))
            for ri in (1, 3, 0, 2):
                for si in order:
                    take = min(residual_old[ri], residual_new[si])
                    flow[ri][si] += take
                    residual_old[ri] -= take
                    residual_new[si] -= take
            assert not any(residual_old) and not any(residual_new)
        else:
            flow = product
        assert all(v >= 0 for row in flow for v in row)
        assert tuple(sum(row, F()) for row in flow) == block.group.rho
        assert [sum((flow[ri][si] for ri in range(4)), F()) for si in range(nc)] == [s.mass for s in states]
        sparse_flow = []
        for ri in range(4):
            for si, state in enumerate(states):
                if flow[ri][si]:
                    sparse_flow.append({'old_state':STATES[ri], 'new_state_column':state.column, 'mass':flow[ri][si]})
                for k, spec in enumerate(specs):
                    cost = primitive_cost(block, ri, state, spec)
                    if cost:
                        costs[k] += flow[ri][si]*cost
                        product_cost[k] += product[ri][si]*cost
        positive_flows += len(sparse_flow)
        blocks.append({'hist_column':block.hist_column, 'group':block.group.key,
                       'orbit':block.group.orbit, 'hist_mass':mu, 'rule':rule,
                       'old_four_state_masses':block.group.rho,
                       'new_state_masses':[(s.column,s.mass) for s in states],
                       'positive_flow':sparse_flow,
                       'all_old_and_new_marginals_exact':True})
    queries = [{'query':spec, 'budget':b, 'cost':c, 'slack':b-c,
                'old_product_cost':pc, 'old_product_slack':b-pc}
               for spec,b,c,pc in zip(specs,rhs,costs,product_cost)]
    minimum = min(r['slack'] for r in queries)
    return {'family':family, 'query_count':len(queries), 'feasible':minimum >= 0,
            'strictly_feasible':minimum > 0, 'minimum_query_slack':minimum,
            'minimum_query_slack_float':float(minimum),
            'old_product_minimum':min(r['old_product_slack'] for r in queries),
            'old_product_negative_queries':sum(r['old_product_slack'] < 0 for r in queries),
            'complete_domain_pairs':full_pairs, 'zero_mass_blocks':zero_blocks,
            'positive_blocks':len(blocks), 'positive_flow_entries':positive_flows,
            'queries':queries, 'blocks':blocks}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--point', type=Path, default=RUN/'zz_closure_lp/augmented_lp_exact.json')
    ap.add_argument('--output', type=Path, default=HERE/'exact_81_completion_13931.json')
    args = ap.parse_args()
    point = Point(args.point)
    results = [make_family(point, f) for f in ('B2','B3','B4','Mroot')]
    b4_specs = row_specs(point.labels['B4'])
    numerical = discover(point, 'B4', b4_specs, budgets(point,'B4',b4_specs), 1e-9)
    out = {'scope':'One exact simultaneous completion of the same specified 81 terminal queries, separately on their stated family/group transportation domain; not full SPE',
           'input':str(args.point.resolve()), 'input_sha256':hashlib.sha256(point.raw).hexdigest(),
           'input_W':point.report['W'], 'input_columns':len(point.columns),
           'label_note':'The tail-query H1 label denotes hidden[0]; early-cut H0 denotes hidden[0].',
           'completion_rule':'Conditional product except B4/orbit(1,0), which uses old-state order 01,11,00,10 and new-state terminal-denominator descending order',
           'zero_mass_rule':'All cells in a zero hist-mass block are exactly zero.',
           'all_81_queries_exactly_feasible':all(r['feasible'] for r in results),
           'all_81_queries_strictly_positive':all(r['strictly_feasible'] for r in results),
           'query_count':sum(r['query_count'] for r in results),
           'families':results, 'B4_float_discovery_only':numerical,
           'finite_nonseparation_conclusion':'Every nonnegative whole-row combination of these same queries, projected over this same conditional transport domain, has nonnegative slack at this point because this common exact completion exists.',
           'not_certified':['all old groups plus old overlap atom realizability','all families jointly with full label/history identities','unlisted deviations','complete SPE','universal half welfare'],
           'generator_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (TAIL/'transport_separator.py',Path(__file__).resolve())}}
    assert out['query_count'] == 81
    assert out['all_81_queries_exactly_feasible'] and out['all_81_queries_strictly_positive']
    args.output.write_text(json.dumps(serial(out), ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(serial({'output':str(args.output), 'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
                             'all_81_queries_exactly_feasible':True,
                             'families':[{k:v for k,v in r.items() if k not in ('queries','blocks')} for r in results]}), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
