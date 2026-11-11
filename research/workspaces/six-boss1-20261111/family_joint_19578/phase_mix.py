"""Global A/C mixture with one common B4 transport, all old RZ queries.

C uses Z=[0,v), R=[0,t) union [v,v+q-t) at every one of 66 nodes.
The same global lambda applies to every hist and every family.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

from build_common import Data, HERE, POINT, LATENT, ORBIT, OI, NODES, FAMILIES, digest, save, serial


def canon(values):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in values)


def classes():
    answer = defaultdict(list)
    for i, e in enumerate(NODES):
        for j, f in enumerate(NODES):
            answer[e[0], f[0], canon(e[1:] + f[1:])].append((i, j))
    assert len(answer) == 42
    return dict(answer)


def metrics(states, P):
    rz = tuple((v // 2, v % 2) for v in states)
    return {o: (Q(sum(rz[k][0] for k in OI[o]), len(OI[o])),
                Q(sum(rz[k][1] for k in OI[o]), len(OI[o])),
                sum((Q(1, P + rz[k][0] + 1) for k in OI[o]), Q()) / len(OI[o]),
                sum((Q(rz[k][1], P + rz[k][0] + 1) for k in OI[o]), Q()) / len(OI[o])) for o in ORBIT}


def make_orientation(data, orientation='ZZ'):
    assert orientation in ('RR', 'RZ', 'ZR', 'ZZ')
    groups = defaultdict(dict)
    current = None
    for j, col in enumerate(data.cols):
        if col['kind'] == 'hist':
            current = j
        elif col['kind'] == 'joint-reply':
            f, diag, wi, wj = col['group']
            g = f, diag, tuple(wi), tuple(wj)
            groups[current].setdefault(g, {})[tuple(col['state'])] = data.mass[j]
    out = {}
    for h, hist in data.hist.items():
        H = data.mass[h]
        words = tuple(w for w, n in zip(product((0, 1), repeat=3), hist['hist']) for _ in range(n))
        intervals = []
        breakpoints = {Q(), H}
        for f, i, j in NODES:
            own = groups[h][f, int(i == j), words[i], words[j]]
            q = own[1, 0] + own[1, 1]
            v = own[0, 1] + own[1, 1]
            t = own[1, 1]
            if orientation[f] == 'Z':
                ri = ((Q(), t), (v, v + q - t))
                zi = ((Q(), v),)
                assert 0 <= t <= v <= v + q - t <= H
            else:
                ri = ((Q(), q),)
                zi = ((Q(), t), (q, q + v - t))
                assert 0 <= t <= q <= q + v - t <= H
            for lo, hi in ri + zi:
                breakpoints.update((lo, hi))
            intervals.append((ri, zi))
        ordered = sorted(breakpoints)
        atoms = []
        for lo, hi in zip(ordered, ordered[1:]):
            assert lo < hi
            mid = (lo + hi) / 2
            states = [2 * any(a <= mid < b for a, b in ri) + any(a <= mid < b for a, b in zi)
                      for ri, zi in intervals]
            atoms.append({'index': len(atoms), 'mass': hi - lo, 'states': list(map(int, states)),
                          'interval': (lo, hi), 'metrics': metrics(states, sum(map(int, hist['actual_bits'][:4])))})
        assert sum((a['mass'] for a in atoms), Q()) == H
        out[h] = atoms
    return out


def make_C(data):
    return make_orientation(data, 'ZZ')


def old_queries(data, atoms, hist_ids=None):
    cls = classes()
    kinds = ('R-R', 'R-Z', 'Z-R', 'Z-Z')
    sums = {(kind, key): Q() for kind in kinds for key in cls}
    for h, hist in data.hist.items():
        if hist_ids is not None and h not in hist_ids:
            continue
        words = tuple(w for w, n in zip(product((0, 1), repeat=3), hist['hist']) for _ in range(n))
        p = sum(map(int, hist['actual_bits'][:3]))
        P = sum(map(int, hist['actual_bits'][:4]))
        dR = tuple(p + words[i][0] + words[j][1 + f] + 1 for f, i, j in NODES)
        for atom in atoms[h]:
            r = tuple(v // 2 for v in atom['states'])
            z = tuple(v % 2 for v in atom['states'])
            dZ = tuple(P + v + 1 for v in r)
            for key, pairs in cls.items():
                buckets = [[0] * 7 for _ in kinds]
                for i, j in pairs:
                    buckets[0][dR[i]] += r[i] - r[j]
                    buckets[1][dR[i]] += r[i] - z[j]
                    buckets[2][dZ[i]] += z[i] - r[j]
                    buckets[3][dZ[i]] += z[i] - z[j]
                for kind, bucket in zip(kinds, buckets):
                    sums[kind, key] += atom['mass'] * sum((Q(v, d) for d, v in enumerate(bucket) if v), Q()) / len(pairs)
    return sums


def mix_interval(a, c):
    lower, upper = Q(), Q(1)
    upper_active = []
    lower_active = []
    for key, av in a.items():
        cv = c[key]
        assert av >= 0
        delta = cv - av
        if delta < 0:
            bound = av / -delta
            if bound < upper:
                upper, upper_active = bound, [key]
            elif bound == upper:
                upper_active.append(key)
        elif delta > 0 and av < 0:
            bound = -av / delta
            if bound > lower:
                lower, lower_active = bound, [key]
            elif bound == lower:
                lower_active.append(key)
    return lower, upper, lower_active, upper_active


def solve_B4(data, phases, interval):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    family = 'B4'
    specs = data.specs(family)
    variables = [(phase, h, a['index'], s['column']) for phase, by_h in phases.items()
                 for h in data.hist for a in by_h[h]
                 for s in data.family[family][h] if s['mass']]
    vmap = {v: i for i, v in enumerate(variables)}
    n = len(variables)
    lamcol, epscol = n, n + 1
    er, ec, ev, eb, ur, uc, uv = [], [], [], [], [], [], []
    for h in data.hist:
        ss = [s for s in data.family[family][h] if s['mass']]
        if not ss:
            continue
        for phase, by_h in phases.items():
            for a in by_h[h]:
                row = len(eb)
                eb.append(float(a['mass']) if phase == 'A' else 0.)
                for s in ss:
                    er.append(row); ec.append(vmap[phase, h, a['index'], s['column']]); ev.append(1.)
                er.append(row); ec.append(lamcol); ev.append(float(a['mass']) * (1 if phase == 'A' else -1))
        for s in ss[:-1]:
            row = len(eb); eb.append(float(s['mass']))
            for phase, by_h in phases.items():
                for a in by_h[h]:
                    er.append(row); ec.append(vmap[phase, h, a['index'], s['column']]); ev.append(1.)
        for phase, by_h in phases.items():
            for a in by_h[h]:
                for s in ss:
                    vi = vmap[phase, h, a['index'], s['column']]
                    for k, spec in enumerate(specs):
                        cost = data.cost(a, s, spec)
                        if cost:
                            ur.append(k); uc.append(vi); uv.append(float(cost))
    for k in range(len(specs)):
        ur.append(k); uc.append(epscol); uv.append(1.)
    eq = coo_matrix((ev, (er, ec)), shape=(len(eb), n + 2)).tocsc()
    ub = coo_matrix((uv, (ur, uc)), shape=(len(specs), n + 2)).tocsc()
    obj = np.zeros(n + 2); obj[epscol] = -1.
    result = linprog(obj, A_eq=eq, b_eq=eb, A_ub=ub,
                     b_ub=[float(x) for x in data.budgets(family)],
                     bounds=[(0, None)] * n + [(float(interval[0]), float(interval[1])), (None, None)],
                     method='highs', options={'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
    report = {'status': int(result.status), 'message': result.message, 'transport_variables': n,
              'margin_equalities': len(eb), 'query_inequalities': len(specs),
              'lambda_bounds': interval, 'variables_in_order': variables}
    if not result.success:
        return report, None, None
    report.update({'floating_lambda': float(result.x[lamcol]), 'floating_maximum_common_slack': float(result.x[epscol]),
                   'floating_query_weights': (-result.ineqlin.marginals).tolist(), 'floating_flow': result.x[:n].tolist()})
    if result.x[epscol] <= 1e-9:
        return report, None, None
    lam = min(interval[1], max(interval[0], Q(str(result.x[lamcol])).limit_denominator(10**9)))
    flow = {}
    for h in data.hist:
        rr = {(phase, a['index']): a['mass'] * (1 - lam if phase == 'A' else lam)
              for phase, by_h in phases.items() for a in by_h[h]}
        cc = {s['column']: s['mass'] for s in data.family[family][h] if s['mass']}
        entries = defaultdict(Q)
        for phase, ai in rr:
            for j in cc:
                target = Q(str(max(0., result.x[vmap[phase, h, ai, j]]))).limit_denominator(10**12)
                m = min(target, rr[phase, ai], cc[j])
                if m:
                    entries[phase, ai, j] += m; rr[phase, ai] -= m; cc[j] -= m
        for phase, ai in rr:
            for j in cc:
                m = min(rr[phase, ai], cc[j])
                if m:
                    entries[phase, ai, j] += m; rr[phase, ai] -= m; cc[j] -= m
        assert not any(rr.values()) and not any(cc.values())
        flow[h] = [(phase, ai, j, m) for (phase, ai, j), m in sorted(entries.items()) if m]
    return report, lam, flow


def evaluate(data, family, phases, lam, flow):
    specs = data.specs(family)
    cost = [Q()] * len(specs)
    for h in data.hist:
        rr = {(phase, a['index']): Q() for phase, by_h in phases.items() for a in by_h[h]}
        ss = {s['column']: s for s in data.family[family][h]}
        cc = {j: Q() for j in ss}
        seen = set()
        for phase, ai, j, m in flow[h]:
            assert (phase, ai, j) not in seen
            seen.add((phase, ai, j))
            assert m > 0
            rr[phase, ai] += m; cc[j] += m
            for k, spec in enumerate(specs):
                cost[k] += m * data.cost(phases[phase][h][ai], ss[j], spec)
        assert rr == {(phase, a['index']): a['mass'] * (1 - lam if phase == 'A' else lam)
                      for phase, by_h in phases.items() for a in by_h[h]}
        assert cc == {j: s['mass'] for j, s in ss.items()}
    queries = [{'query': spec, 'budget': b, 'cost': c, 'slack': b - c}
               for spec, b, c in zip(specs, data.budgets(family), cost)]
    return {'family': family, 'queries': queries, 'query_count': len(specs),
            'minimum_query_slack': min(q['slack'] for q in queries),
            'positive_flow_entries': sum(map(len, flow.values())),
            'blocks': [{'hist_column': h,
                        'positive_flow': [{'phase': ph, 'atom': a, 'family_state_column': j, 'mass': m}
                                          for ph, a, j, m in flow[h]]} for h in data.hist]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--point', type=Path, default=POINT)
    parser.add_argument('--witness', type=Path, default=LATENT)
    parser.add_argument('--out-dir', type=Path, default=HERE)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    data = Data(args.point, args.witness)
    phases = {'A': data.atoms, 'C': make_C(data)}
    phase_values = {phase: old_queries(data, atoms) for phase, atoms in phases.items()}
    previous = json.loads(args.witness.read_bytes())
    for record in previous['selected_query_records']:
        f, g, pattern = record['class']
        assert phase_values['A'][record['kind'], (f, g, tuple(pattern))] == Q(record['individual_slack'])
    lo, hi, loa, hia = mix_interval(phase_values['A'], phase_values['C'])
    assert 0 <= lo <= hi <= 1
    report = {'scope': 'fixed global A/C common-customer candidate family; no full-SPE claim',
              'input_point': str(args.point), 'input_sha256': digest(args.point),
              'input_A_witness': str(args.witness), 'input_A_sha256': digest(args.witness),
              'source_sha256': digest(Path(__file__)),
              'phase_rule': {'A': 'all R initial threshold; own Z intervals',
                             'C': 'all Z initial threshold; own R intervals'},
              'lambda_interval': (lo, hi), 'lambda_upper_active': hia, 'lambda_lower_active': loa,
              'old_query_classes': [{'kind': kind, 'class': key,
                                     'literal_queries': len(classes()[key]),
                                     'phase_A_slack': av, 'phase_C_slack': phase_values['C'][kind, key]}
                                    for (kind, key), av in phase_values['A'].items()],
              'phases': {phase: [{'hist_column': h, 'atoms': [{k: v for k, v in a.items() if k != 'metrics'} for a in by_h[h]]}
                                 for h in data.hist] for phase, by_h in phases.items()}}
    print('Old-query feasible lambda interval:', float(lo), float(hi), flush=True)
    discovery, lam, B4_flow = solve_B4(data, phases, (lo, hi))
    report['discovery'] = discovery
    print({k: v for k, v in discovery.items() if k not in ('variables_in_order', 'floating_flow')}, flush=True)
    if lam is not None:
        report['lambda'] = lam
        report['families'] = []
        for family in FAMILIES:
            if family == 'B4':
                flow = B4_flow
            else:
                flow = {h: [(phase, a['index'], s['column'],
                             a['mass'] * (1 - lam if phase == 'A' else lam) * s['mass'] / data.mass[h])
                            for phase, by_h in phases.items() for a in by_h[h]
                            for s in data.family[family][h] if s['mass'] and (1 - lam if phase == 'A' else lam)]
                        for h in data.hist}
            entry = evaluate(data, family, phases, lam, flow)
            assert entry['minimum_query_slack'] >= 0
            report['families'].append(entry)
            print(family, 'minimum exact slack', float(entry['minimum_query_slack']), 'positive flows', entry['positive_flow_entries'], flush=True)
        for entry in report['old_query_classes']:
            entry['selected_slack'] = (1 - lam) * entry['phase_A_slack'] + lam * entry['phase_C_slack']
            assert entry['selected_slack'] >= 0
        report['all_queries_feasible'] = True
        report['joint_measure_rule'] = 'mu(h,phase,atom,pi,s2,s3,s4,sM)=product_F flow_F(h,phase,atom,sF)/(720*selected_atom_mass(h,phase,atom)^3), with all pi in S6'
    else:
        report['all_queries_feasible'] = False
    save(args.out_dir / 'phase_AC_attempt.json', report)


if __name__ == '__main__':
    main()
