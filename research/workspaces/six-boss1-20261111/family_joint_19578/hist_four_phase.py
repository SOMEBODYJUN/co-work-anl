"""Common family completion with four threshold orientations in each hist.

Each hist has a simplex of RR/RZ/ZR/ZZ phase weights. Those are construction
parameters, never customer-dependent IC multipliers. B4 shares one table
over all old groups. The other families use a hist-conditional product.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

from build_common import Data, HERE, POINT, LATENT, FAMILIES, digest, save, serial
from phase_mix import make_orientation, old_queries, classes

PHASES = ('RR', 'RZ', 'ZR', 'ZZ')


def evaluate(data, family, phases, weights, flow):
    specs = data.specs(family)
    costs = [Q()] * len(specs)
    for h in data.hist:
        rr = {(ph, a['index']): Q() for ph in PHASES for a in phases[ph][h]}
        states = {s['column']: s for s in data.family[family][h]}
        cc = {j: Q() for j in states}
        seen = set()
        for ph, ai, j, mass in flow[h]:
            assert mass > 0 and (ph, ai, j) not in seen
            seen.add((ph, ai, j))
            rr[ph, ai] += mass; cc[j] += mass
            for k, spec in enumerate(specs):
                costs[k] += mass * data.cost(phases[ph][h][ai], states[j], spec)
        assert rr == {(ph, a['index']): weights[h][ph] * a['mass'] for ph in PHASES for a in phases[ph][h]}
        assert cc == {j: state['mass'] for j, state in states.items()}
    queries = [{'query': sp, 'budget': b, 'cost': c, 'slack': b-c}
               for sp, b, c in zip(specs, data.budgets(family), costs)]
    return {'family': family, 'query_count': len(queries), 'queries': queries,
            'minimum_query_slack': min(q['slack'] for q in queries),
            'positive_flow_entries': sum(map(len, flow.values())),
            'blocks': [{'hist_column': h, 'positive_flow':
                        [{'phase': ph, 'atom': ai, 'family_state_column': j, 'mass': mass}
                         for ph, ai, j, mass in flow[h]]} for h in data.hist]}


def find(data, phases, old):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    family = 'B4'
    active_hist = [h for h in data.hist if data.mass[h]]
    variables = [(h, ph, a['index'], s['column']) for h in active_hist for ph in PHASES
                 for a in phases[ph][h] for s in data.family[family][h] if s['mass']]
    vmap = {v: i for i, v in enumerate(variables)}
    n = len(variables)
    weight_keys = [(h, ph) for h in active_hist for ph in PHASES]
    wi = {v: n+i for i, v in enumerate(weight_keys)}
    epscol = n + len(wi)
    er, ec, ev, eb, eq_labels = [], [], [], [], []
    ur, uc, uv, ub = [], [], [], []
    specs = data.specs(family)
    for h in active_hist:
        ss = [s for s in data.family[family][h] if s['mass']]
        row = len(eb); eb.append(1.)
        eq_labels.append(('phase-simplex', h))
        for ph in PHASES:
            er.append(row); ec.append(wi[h, ph]); ev.append(1.)
        for ph in PHASES:
            for a in phases[ph][h]:
                row = len(eb); eb.append(0.)
                eq_labels.append(('atom', h, ph, a['index']))
                er.append(row); ec.append(wi[h, ph]); ev.append(-float(a['mass']))
                for s in ss:
                    er.append(row); ec.append(vmap[h, ph, a['index'], s['column']]); ev.append(1.)
        for s in ss[:-1]:
            row = len(eb); eb.append(float(s['mass']))
            eq_labels.append(('family-state', h, s['column']))
            for ph in PHASES:
                for a in phases[ph][h]:
                    er.append(row); ec.append(vmap[h, ph, a['index'], s['column']]); ev.append(1.)
    for k, spec in enumerate(specs):
        row = len(ub); ub.append(float(data.budgets(family)[k]))
        ur.append(row); uc.append(epscol); uv.append(1.)
        for h, ph, ai, j in variables:
            state = next(s for s in data.family[family][h] if s['column'] == j)
            c = data.cost(phases[ph][h][ai], state, spec)
            if c:
                ur.append(row); uc.append(vmap[h, ph, ai, j]); uv.append(float(c))
    old_keys = list(next(iter(old.values())).values())[0].keys()
    included_old = []
    for key in old_keys:
        invariant = all(old[ph][h][key] == old['RR'][h][key] for h in active_hist for ph in PHASES)
        if invariant:
            assert sum((old['RR'][h][key] for h in active_hist), Q()) >= 0
            continue
        row = len(ub); ub.append(0.)
        included_old.append(key)
        for h in active_hist:
            for ph in PHASES:
                c = -old[ph][h][key]
                if c:
                    ur.append(row); uc.append(wi[h, ph]); uv.append(float(c))
    aeq = coo_matrix((ev, (er, ec)), shape=(len(eb), epscol+1)).tocsc()
    aub = coo_matrix((uv, (ur, uc)), shape=(len(ub), epscol+1)).tocsc()
    obj = np.zeros(epscol+1); obj[-1] = -1.
    result = linprog(obj, A_eq=aeq, b_eq=eb, A_ub=aub, b_ub=ub,
                     bounds=[(0, None)]*n + [(0,1)]*len(wi) + [(None,None)],
                     method='highs', options={'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
    report = {'status': int(result.status), 'message': result.message, 'transport_variables': n,
              'phase_weight_variables': len(wi), 'equalities': len(eb),
              'B4_query_rows': len(specs), 'nonconstant_old_query_rows': len(included_old),
              'variables_in_order': variables, 'phase_weights_in_order': weight_keys,
              'old_queries_in_order': included_old, 'equality_rows_in_order': eq_labels}
    if not result.success:
        return report, None, None
    report.update({'floating_common_slack': float(result.x[-1]),
                   'floating_flow': result.x[:n].tolist(),
                   'floating_phase_weights': result.x[n:epscol].tolist(),
                   'floating_equality_potentials': result.eqlin.marginals.tolist(),
                   'floating_IC_weights': (-result.ineqlin.marginals).tolist()})
    if result.x[-1] <= 1e-9:
        return report, None, None
    weights = {}
    for h in data.hist:
        if not data.mass[h]:
            weights[h] = {ph: Q(ph == 'RR') for ph in PHASES}
            continue
        vals = {ph: Q(str(max(0., result.x[wi[h, ph]]))).limit_denominator(10**9) for ph in PHASES}
        total = sum(vals.values(), Q())
        assert total > 0
        weights[h] = {ph: val/total for ph, val in vals.items()}
    # Pull infinitesimally toward RR to restore any rounding-sensitive old
    # query boundary. All old zero rows in RR are invariant or self-queries.
    pull = Q()
    for key in old_keys:
        av = sum((old['RR'][h][key] for h in data.hist), Q())
        candidate = sum((weights[h][ph] * old[ph][h][key] for h in data.hist for ph in PHASES), Q())
        if candidate < 0:
            assert av > 0, (key, candidate, av)
            pull = max(pull, -candidate/(av-candidate))
    pull += Q(1, 10**7)
    assert pull < Q(1,1000)
    report['exact_RR_pull_for_rounding'] = pull
    for h in data.hist:
        weights[h] = {ph: (1-pull)*weights[h][ph] + pull*(ph=='RR') for ph in PHASES}
        assert sum(weights[h].values(), Q()) == 1 and min(weights[h].values()) >= 0
    for key in old_keys:
        assert sum((weights[h][ph] * old[ph][h][key] for h in data.hist for ph in PHASES), Q()) >= 0
    flow = {}
    for h in data.hist:
        rr = {(ph,a['index']): weights[h][ph]*a['mass'] for ph in PHASES for a in phases[ph][h]}
        cc = {s['column']: s['mass'] for s in data.family[family][h] if s['mass']}
        values = defaultdict(Q)
        for ph, ai in rr:
            for j in cc:
                target = Q(str(max(0., result.x[vmap[h,ph,ai,j]]))).limit_denominator(10**12)
                mass = min(target, rr[ph,ai], cc[j])
                if mass:
                    values[ph,ai,j] += mass; rr[ph,ai] -= mass; cc[j] -= mass
        for ph, ai in rr:
            for j in cc:
                mass = min(rr[ph,ai], cc[j])
                if mass:
                    values[ph,ai,j] += mass; rr[ph,ai] -= mass; cc[j] -= mass
        assert not any(rr.values()) and not any(cc.values())
        flow[h] = [(ph,ai,j,mass) for (ph,ai,j),mass in sorted(values.items()) if mass]
    return report, weights, flow


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--point', type=Path, default=POINT)
    ap.add_argument('--witness', type=Path, default=LATENT)
    ap.add_argument('--out-dir', type=Path, default=HERE)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    data = Data(args.point, args.witness)
    phases = {ph: make_orientation(data,ph) for ph in PHASES}
    for h in data.hist:
        assert [(a['mass'],a['states']) for a in phases['RR'][h]] == [(a['mass'],a['states']) for a in data.atoms[h]]
    old = {ph: {h: old_queries(data, phases[ph], [h]) for h in data.hist} for ph in PHASES}
    discovery, weights, B4flow = find(data, phases, old)
    print({k:v for k,v in serial(discovery).items() if k not in
           ('variables_in_order','phase_weights_in_order','old_queries_in_order','equality_rows_in_order','floating_flow','floating_phase_weights','floating_IC_weights','floating_equality_potentials')}, flush=True)
    report = {'scope': 'four threshold phases per hist, one common RZ atom/family transport; not SPE',
              'input_point': str(args.point), 'input_sha256': digest(args.point),
              'input_A_witness': str(args.witness), 'input_A_sha256': digest(args.witness),
              'source_sha256': digest(Path(__file__)), 'discovery': discovery,
              'phase_order': PHASES, 'phase_rule': 'first letter is thresholded member for family0; second for family1',
              'phases': {ph: [{'hist_column':h,'atoms':[{k:v for k,v in a.items() if k!='metrics'} for a in phases[ph][h]]}
                              for h in data.hist] for ph in PHASES}}
    if weights is None:
        report['all_queries_feasible'] = False
        save(args.out_dir / 'hist_four_phase_attempt.json', report)
        return
    report['phase_weights'] = [{'hist_column':h,'weights':weights[h]} for h in data.hist]
    report['families'] = []
    for family in FAMILIES:
        if family == 'B4':
            flow = B4flow
        else:
            flow = {h:[(ph,a['index'],s['column'],weights[h][ph]*a['mass']*s['mass']/data.mass[h])
                       for ph in PHASES if weights[h][ph] for a in phases[ph][h]
                       for s in data.family[family][h] if s['mass']] for h in data.hist}
        audit = evaluate(data,family,phases,weights,flow)
        assert audit['minimum_query_slack'] >= 0, (family,audit['minimum_query_slack'])
        report['families'].append(audit)
        print(family,'exact minimum',float(audit['minimum_query_slack']),'flows',audit['positive_flow_entries'],flush=True)
    report['old_query_classes'] = []
    for key in old['RR'][next(iter(data.hist))]:
        value = sum((weights[h][ph]*old[ph][h][key] for h in data.hist for ph in PHASES),Q())
        assert value>=0
        kind,cl=key
        report['old_query_classes'].append({'kind':kind,'class':cl,'literal_queries':len(classes()[cl]),'slack':value})
    report['all_queries_feasible'] = True
    report['joint_measure_rule'] = 'mu(h,phase,atom,pi,s2,s3,s4,sM)=product_F flow_F(h,phase,atom,sF)/(720*selected_atom_mass(h,phase,atom)^3), all pi in S6'
    report['selected_positive_base_atoms'] = sum(len(phases[ph][h]) for h in data.hist for ph in PHASES if weights[h][ph])
    report['family_query_count'] = sum(f['query_count'] for f in report['families'])
    report['old_literal_query_count'] = sum(q['literal_queries'] for q in report['old_query_classes'])
    save(args.out_dir / 'hist_four_phase_completion.json',report)


if __name__ == '__main__':
    main()
