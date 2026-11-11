"""Exact all-lambda failure certificate for the global A/C candidate family."""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from pathlib import Path
import json
from build_common import Data, HERE, POINT, LATENT, digest, save
from phase_mix import metrics


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--point', type=Path, default=POINT)
    ap.add_argument('--witness', type=Path, default=LATENT)
    ap.add_argument('--attempt', type=Path, default=HERE / 'phase_AC_attempt.json')
    ap.add_argument('--out-dir', type=Path, default=HERE)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    data = Data(args.point, args.witness)
    attempt = json.loads(args.attempt.read_bytes())
    assert attempt['input_sha256'] == digest(args.point)
    lower, upper = map(Q, attempt['lambda_interval'])
    phases = {ph: {b['hist_column']: b['atoms'] for b in blocks} for ph, blocks in attempt['phases'].items()}
    family, orbit = 'B4', (0, 0)
    spec = ('new-to-Z', orbit)
    budget = data.budgets(family)[data.specs(family).index(spec)]
    blocks = []
    D0, D1, primal, cell_count = Q(), Q(), Q(), 0
    for h in data.hist:
        P = sum(map(int, data.hist[h]['actual_bits'][:4]))
        atoms = []
        for ph in ('A', 'C'):
            for raw in phases[ph][h]:
                aa = {'phase': ph, 'index': raw['index'], 'mass': Q(raw['mass']),
                      'metrics': metrics(raw['states'], P)}
                aa['selected_mass'] = aa['mass'] * (1 - upper if ph == 'A' else upper)
                atoms.append(aa)
        atoms.sort(key=lambda a: (-a['metrics'][orbit][1], a['phase'], a['index']))
        states = sorted(data.family[family][h], key=lambda s: (-s['denom'], s['column']))
        low, high = min(s['denom'] for s in states), max(s['denom'] for s in states)
        cap = sum((s['mass'] for s in states if s['denom'] == high), Q())
        left = cap
        theta = max((a['metrics'][orbit][1] for a in atoms), default=Q()) if not left else Q()
        for a in atoms:
            if left:
                theta = a['metrics'][orbit][1]
                left -= min(a['selected_mass'], left)
        assert left == 0
        delta = Q(1, low) - Q(1, high)
        alpha = {(a['phase'], a['index']): a['metrics'][orbit][1] / low
                 - delta * max(Q(), a['metrics'][orbit][1] - theta) for a in atoms}
        beta = {s['column']: -delta * theta * (s['denom'] == high) for s in states}
        aa = {ph: sum((a['mass'] * alpha[a['phase'], a['index']] for a in atoms if a['phase'] == ph), Q())
              for ph in ('A', 'C')}
        bb = sum((s['mass'] * beta[s['column']] for s in states), Q())
        d0, d1 = aa['A'] + bb, aa['C'] - aa['A']
        D0 += d0; D1 += d1
        rr = {(a['phase'], a['index']): a['selected_mass'] for a in atoms}
        cc = {s['column']: s['mass'] for s in states}
        flow = []
        pcost = Q()
        for a in atoms:
            for s in states:
                assert alpha[a['phase'], a['index']] + beta[s['column']] <= data.cost(a, s, spec)
                cell_count += 1
                mass = min(rr[a['phase'], a['index']], cc[s['column']])
                if not mass:
                    continue
                rr[a['phase'], a['index']] -= mass; cc[s['column']] -= mass
                assert alpha[a['phase'], a['index']] + beta[s['column']] == data.cost(a, s, spec)
                pcost += mass * data.cost(a, s, spec)
                flow.append({'phase': a['phase'], 'atom': a['index'], 'family_state_column': s['column'], 'mass': mass})
        assert not any(rr.values()) and not any(cc.values())
        assert pcost == d0 + upper * d1
        primal += pcost
        blocks.append({'hist_column': h, 'threshold': theta,
                       'atom_potentials': [{'phase': ph, 'atom': ai, 'value': v} for (ph, ai), v in alpha.items()],
                       'state_potentials': [{'column': j, 'value': v} for j, v in beta.items()],
                       'positive_flow_at_upper': flow, 'cost_at_upper': pcost,
                       'dual_constant': d0, 'dual_lambda_coefficient': d1})
    assert primal == D0 + upper * D1
    assert D1 <= 0
    active = attempt['lambda_upper_active'][0]
    active_row = next(r for r in attempt['old_query_classes'] if [r['kind'], r['class']] == active)
    old_a, old_c = Q(active_row['phase_A_slack']), Q(active_row['phase_C_slack'])
    old_delta = old_c - old_a
    assert old_delta < 0 and old_a + upper * old_delta == 0
    multiplier = D1 / old_delta
    combined_constant = budget - D0 + multiplier * old_a
    assert multiplier >= 0 and combined_constant == budget - primal
    assert combined_constant < 0
    report = {'scope': 'all-lambda infeasibility of fixed global A/C family only; not original marginal-domain separation',
              'input_sha256': digest(args.point), 'input_A_sha256': digest(args.witness),
              'attempt_sha256': digest(args.attempt), 'source_sha256': digest(Path(__file__)),
              'query': spec, 'lambda_interval': (lower, upper), 'budget': budget,
              'exact_minimum_cost_at_upper': primal, 'exact_best_slack_over_interval': budget - primal,
              'dual_constant': D0, 'dual_lambda_coefficient': D1,
              'old_upper_constraint': active_row, 'old_IC_multiplier': multiplier,
              'combined_upper_bound_on_nonnegative_IC_sum': combined_constant,
              'all_dual_cells': cell_count, 'blocks': blocks,
              'fixed_global_AC_impossible': True}
    save(args.out_dir / 'phase_AC_obstruction.json', report)
    print({'fixed_global_AC_impossible': True, 'best_slack': float(budget - primal),
           'dual_slope': float(D1), 'all_dual_cells': cell_count})


if __name__ == '__main__':
    main()
