"""Exact sorted transport and all-cell dual for the fixed-A obstruction.

The dual uses the fixed joint latent atoms, so it is not a cut on the original
own-four-state marginal polytope. The complete B4 family state domain is kept.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from pathlib import Path
from build_common import Data, HERE, POINT, LATENT, digest, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--point', type=Path, default=POINT)
    parser.add_argument('--witness', type=Path, default=LATENT)
    parser.add_argument('--out-dir', type=Path, default=HERE)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    data = Data(args.point, args.witness)
    family, orbit = 'B4', (0, 0)
    spec = ('new-to-Z', orbit)
    query_index = data.specs(family).index(spec)
    budget = data.budgets(family)[query_index]
    total_primal, total_dual, cells = Q(), Q(), 0
    blocks = []
    common_flow = {}
    for h in data.hist:
        atoms = sorted(data.atoms[h], key=lambda a: (-a['metrics'][orbit][1], a['index']))
        states = sorted(data.family[family][h], key=lambda s: (-s['denom'], s['column']))
        assert len({s['denom'] for s in states}) == 2
        low_d, high_d = min(s['denom'] for s in states), max(s['denom'] for s in states)
        assert high_d == low_d + 1
        high_mass = sum((s['mass'] for s in states if s['denom'] == high_d), Q())
        remaining = high_mass
        theta = Q()
        for a in atoms:
            if remaining > 0:
                theta = a['metrics'][orbit][1]
                remaining -= min(a['mass'], remaining)
        assert remaining == 0
        c0, delta = Q(1, low_d), Q(1, low_d) - Q(1, high_d)
        alpha = {a['index']: c0 * a['metrics'][orbit][1]
                 - delta * max(Q(), a['metrics'][orbit][1] - theta) for a in atoms}
        beta = {s['column']: -delta * theta * (s['denom'] == high_d) for s in states}
        for a in atoms:
            for s in states:
                assert alpha[a['index']] + beta[s['column']] <= data.cost(a, s, spec)
                cells += 1
        rr = {a['index']: a['mass'] for a in atoms}
        cc = {s['column']: s['mass'] for s in states}
        flow = []
        primal = Q()
        for a in atoms:
            for s in states:
                m = min(rr[a['index']], cc[s['column']])
                if not m:
                    continue
                rr[a['index']] -= m; cc[s['column']] -= m
                cost = data.cost(a, s, spec)
                assert alpha[a['index']] + beta[s['column']] == cost
                primal += m * cost
                flow.append((a['index'], s['column'], m))
        assert not any(rr.values()) and not any(cc.values())
        dual = sum((a['mass'] * alpha[a['index']] for a in atoms), Q()) + sum(
            (s['mass'] * beta[s['column']] for s in states), Q())
        assert primal == dual
        total_primal += primal; total_dual += dual
        common_flow[h] = flow
        blocks.append({'hist_column': h, 'threshold': theta,
                       'low_denominator': low_d, 'high_denominator': high_d,
                       'high_denominator_mass': high_mass,
                       'atom_potentials': [{'atom': i, 'value': v} for i, v in alpha.items()],
                       'state_potentials': [{'column': i, 'value': v} for i, v in beta.items()],
                       'positive_flow': [{'atom': a, 'family_state_column': s, 'mass': m} for a, s, m in flow],
                       'primal_cost': primal, 'dual_cost': dual})
    assert total_primal == total_dual
    audit = data.evaluate(family, common_flow)
    assert audit['queries'][query_index]['cost'] == total_primal
    result = {'scope': 'failure of fixed A latent completion only; not a cut on the original own-state marginal domain',
              'input_sha256': digest(args.point), 'latent_sha256': digest(args.witness),
              'source_sha256': digest(Path(__file__)), 'query': spec,
              'budget': budget, 'exact_minimum_cost': total_primal,
              'exact_best_slack': budget - total_primal,
              'fixed_A_impossible': budget < total_primal,
              'dual_all_cells': cells, 'blocks': blocks,
              'joint_query_audit_on_sorted_transport': audit}
    save(args.out_dir / 'fixed_A_obstruction.json', result)
    print({'fixed_A_impossible': result['fixed_A_impossible'], 'best_slack': float(budget - total_primal),
           'all_dual_cells': cells, 'positive_flow_entries': audit['positive_flow_entries']})


if __name__ == '__main__':
    main()
