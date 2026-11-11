"""One common latent-atom/family-state transport per hist, all groups together.

Discovery uses only the S6-invariant orbit-average costs. The saved witness
has exact rational margins and is a joint coverage-layer completion, not SPE.
No old builder is imported; all interface data are read from frozen JSON.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
POINT = WORK / 'discounted_augmented_lp/augmented_lp_exact.json'
LATENT = WORK / 'old_r_joint/common_completion_19578.json'
POINT_SHA = 'a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505'
LATENT_SHA = '6e4932cd3ed8b216fcb5ccaf2379ef7f8257455577da5aaa08ea514397270ad0'
ORBIT = ((0, 0), (1, 0), (1, 1))
FAMILIES = ('B2', 'B3', 'B4', 'Mroot')
NODES = tuple((f, i, j) for f, i, j in product(range(2), range(6), range(6)) if f or i != j)
OID = tuple((f, int(i == j)) for f, i, j in NODES)
OI = {o: tuple(k for k, v in enumerate(OID) if v == o) for o in ORBIT}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def serial(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def save(path, data):
    path.write_text(json.dumps(serial(data), ensure_ascii=False, indent=2) + '\n')


class Data:
    def __init__(self, point=POINT, latent_path=LATENT):
        self.point_path = Path(point)
        self.latent_path = Path(latent_path)
        if self.point_path.resolve() == POINT.resolve():
            assert digest(self.point_path) == POINT_SHA
        if self.latent_path.resolve() == LATENT.resolve():
            assert digest(self.latent_path) == LATENT_SHA
        self.point = json.loads(self.point_path.read_bytes())
        latent = json.loads(self.latent_path.read_bytes())
        assert latent['input_sha256'] == digest(self.point_path)
        self.cols = self.point['columns'][:4849]
        self.mass = tuple(Q(c['weight']) for c in self.cols)
        assert all(m >= 0 for m in self.mass)
        self.hist = {i: c for i, c in enumerate(self.cols) if c['kind'] == 'hist'}
        assert len(self.hist) == 16
        assert sum((self.mass[i] for i in self.hist), Q()) == 1
        assert latent['literal_node_order'] == [list(e) for e in NODES]
        assert Q(latent['phase_A_weight']) == 1 and Q(latent['phase_B_weight']) == 0
        assert latent['symmetrization']['permutations'] == [list(p) for p in permutations(range(6))]
        self.atoms = {}
        for block in latent['phases']['A']:
            h = block['hist_column']
            assert block['actual_bits'] == self.hist[h]['actual_bits']
            assert block['hist'] == self.hist[h]['hist']
            assert Q(block['mass']) == self.mass[h]
            P = sum(map(int, block['actual_bits'][:4]))
            assert P == block['P']
            atoms = []
            for ai, atom in enumerate(block['atoms']):
                m = Q(atom['mass'])
                assert m > 0 and len(atom['states']) == 66
                rz = tuple((int(t) // 2, int(t) % 2) for t in atom['states'])
                assert all(r in (0, 1) and z in (0, 1) for r, z in rz)
                metrics = {
                    o: (
                        Q(sum(rz[k][0] for k in OI[o]), len(OI[o])),
                        Q(sum(rz[k][1] for k in OI[o]), len(OI[o])),
                        sum((Q(1, P + rz[k][0] + 1) for k in OI[o]), Q()) / len(OI[o]),
                        sum((Q(rz[k][1], P + rz[k][0] + 1) for k in OI[o]), Q()) / len(OI[o]),
                    ) for o in ORBIT
                }
                atoms.append({'index': ai, 'mass': m, 'states': atom['states'], 'metrics': metrics})
            assert sum((a['mass'] for a in atoms), Q()) == self.mass[h]
            self.atoms[h] = atoms
        assert set(self.atoms) == set(self.hist)
        assert sum(map(len, self.atoms.values())) == latent['base_atoms']['A']
        self.family = {f: defaultdict(list) for f in FAMILIES}
        self.labels = {}
        for j, col in enumerate(self.cols):
            kind = col['kind']
            if kind not in ('actual-B-family-state', 'maximum-root-family-state'):
                continue
            h = col['hist_column']
            actual = tuple(map(int, self.hist[h]['actual_bits']))
            hidden = tuple(col['hidden'])
            if kind == 'actual-B-family-state':
                source = col['source']
                assert source in (2, 3, 4)
                f = 'B' + str(source)
                seq = actual[:source - 1] + (actual[5],) + hidden
                labels = tuple('H' + str(k + 1) for k in range(len(hidden))) + ('Y-average',)
                members = hidden + (Q(col['ell'], 6),)
                assert set(col) == {'kind', 'source', 'hist_column', 'hidden', 'ell', 'weight'}
            else:
                f = 'Mroot'
                seq = (col['M'],) + hidden
                labels = ('M',) + tuple('H' + str(k + 1) for k in range(5)) + ('Y-average',)
                members = seq + (Q(col['ell'], 6),)
                assert set(col) == {'kind', 'hist_column', 'M', 'hidden', 'ell', 'weight'}
            assert len(seq) == 6 and col['ell'] in (0, 6)
            assert all(v in (0, 1) for v in seq)
            assert f not in self.labels or labels == self.labels[f]
            self.labels[f] = labels
            self.family[f][h].append({'column': j, 'mass': self.mass[j], 'sequence': seq,
                                      'denom': sum(seq[:-1]) + 1, 'members': members})
        for f in FAMILIES:
            assert set(self.family[f]) == set(self.hist)
            for h in self.hist:
                assert sum((s['mass'] for s in self.family[f][h]), Q()) == self.mass[h]
        self.old_z = {o: sum((a['mass'] * a['metrics'][o][3]
                             for aa in self.atoms.values() for a in aa), Q()) for o in ORBIT}

    def specs(self, family):
        return tuple(spec for o in ORBIT for spec in (
            ('new-to-R', o), ('new-to-Z', o),
            *(('Z-to-new', o, k, label) for k, label in enumerate(self.labels[family]))))

    def budgets(self, family):
        u = sum((s['mass'] * Q(s['sequence'][-1], s['denom'])
                 for ss in self.family[family].values() for s in ss), Q())
        return tuple(self.old_z[sp[1]] if sp[0] == 'Z-to-new' else u for sp in self.specs(family))

    @staticmethod
    def cost(atom, state, spec):
        r, z, inv, _ = atom['metrics'][spec[1]]
        if spec[0] == 'new-to-R':
            return r / state['denom']
        if spec[0] == 'new-to-Z':
            return z / state['denom']
        assert spec[0] == 'Z-to-new'
        return inv * state['members'][spec[2]]

    def evaluate(self, family, flow):
        specs = self.specs(family)
        costs = [Q()] * len(specs)
        marginal_checks = 0
        for h in self.hist:
            row = [Q()] * len(self.atoms[h])
            states = {s['column']: s for s in self.family[family][h]}
            column = {j: Q() for j in states}
            seen = set()
            for a, j, m in flow[h]:
                assert (a, j) not in seen
                seen.add((a, j))
                assert m > 0
                row[a] += m
                column[j] += m
                for k, spec in enumerate(specs):
                    costs[k] += m * self.cost(self.atoms[h][a], states[j], spec)
            assert row == [a['mass'] for a in self.atoms[h]]
            assert column == {j: s['mass'] for j, s in states.items()}
            marginal_checks += len(row) + len(column)
        queries = [{'query': spec, 'budget': b, 'cost': c, 'slack': b - c}
                   for spec, b, c in zip(specs, self.budgets(family), costs)]
        return {'queries': queries, 'query_count': len(queries),
                'minimum_query_slack': min(q['slack'] for q in queries),
                'negative_queries': sum(q['slack'] < 0 for q in queries),
                'positive_flow_entries': sum(map(len, flow.values())),
                'all_marginal_checks': marginal_checks}

    def product(self, family):
        return {h: [(a['index'], s['column'], a['mass'] * s['mass'] / self.mass[h])
                    for a in self.atoms[h] for s in self.family[family][h] if s['mass']]
                for h in self.hist}


def optimize(data, family):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix

    variables = [(h, a['index'], s['column']) for h in data.hist
                 for a in data.atoms[h] for s in data.family[family][h] if s['mass']]
    vmap = {v: i for i, v in enumerate(variables)}
    n = len(variables)
    ei, ej, ev, eb = [], [], [], []
    ui, uj, uv = [], [], []
    specs = data.specs(family)
    for h in data.hist:
        states = [s for s in data.family[family][h] if s['mass']]
        if not states:
            continue
        for a in data.atoms[h]:
            rid = len(eb)
            eb.append(float(a['mass']))
            for s in states:
                ei.append(rid); ej.append(vmap[h, a['index'], s['column']]); ev.append(1.)
        for s in states[:-1]:
            rid = len(eb)
            eb.append(float(s['mass']))
            for a in data.atoms[h]:
                ei.append(rid); ej.append(vmap[h, a['index'], s['column']]); ev.append(1.)
        for a in data.atoms[h]:
            for s in states:
                vi = vmap[h, a['index'], s['column']]
                for k, sp in enumerate(specs):
                    value = data.cost(a, s, sp)
                    if value:
                        ui.append(k); uj.append(vi); uv.append(float(value))
    for k in range(len(specs)):
        ui.append(k); uj.append(n); uv.append(1.)
    eq = coo_matrix((ev, (ei, ej)), shape=(len(eb), n + 1)).tocsc()
    ub = coo_matrix((uv, (ui, uj)), shape=(len(specs), n + 1)).tocsc()
    c = np.zeros(n + 1); c[-1] = -1
    result = linprog(c, A_eq=eq, b_eq=eb, A_ub=ub, b_ub=[float(v) for v in data.budgets(family)],
                     bounds=[(0, None)] * n + [(None, None)], method='highs',
                     options={'primal_feasibility_tolerance': 1e-9, 'dual_feasibility_tolerance': 1e-9})
    record = {'family': family, 'variables': n, 'margin_equalities': len(eb),
              'query_inequalities': len(specs), 'status': int(result.status), 'message': result.message}
    if not result.success:
        return record, None
    record.update({'floating_maximum_common_slack': float(result.x[-1]),
                   'floating_query_weights': (-result.ineqlin.marginals).tolist(),
                   'variables_in_order': variables, 'floating_flow': result.x[:-1].tolist()})
    if result.x[-1] <= 1e-8:
        return record, None

    # Rationalize desired entries, clip to remaining exact margins, then fill
    # the tiny residual transport. Verification below decides success exactly.
    # This is not a numerical claim of feasibility or optimality.
    flow = {}
    for h in data.hist:
        rr = {a['index']: a['mass'] for a in data.atoms[h]}
        cc = {s['column']: s['mass'] for s in data.family[family][h] if s['mass']}
        entries = defaultdict(Q)
        for a in rr:
            for j in cc:
                target = Q(str(max(0., result.x[vmap[h, a, j]]))).limit_denominator(10**12)
                m = min(target, rr[a], cc[j])
                if m:
                    entries[a, j] += m; rr[a] -= m; cc[j] -= m
        for a in rr:
            for j in cc:
                m = min(rr[a], cc[j])
                if m:
                    entries[a, j] += m; rr[a] -= m; cc[j] -= m
        assert not any(rr.values()) and not any(cc.values())
        flow[h] = [(a, j, m) for (a, j), m in sorted(entries.items()) if m]
    return record, flow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product-only', action='store_true')
    parser.add_argument('--point', type=Path, default=POINT)
    parser.add_argument('--witness', type=Path, default=LATENT)
    parser.add_argument('--out-dir', type=Path, default=HERE)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    data = Data(args.point, args.witness)
    record = {'scope': 'common RZ/family coverage layer; no complete SPE claim',
              'input_point': str(args.point), 'input_sha256': digest(args.point),
              'latent_completion': str(args.witness), 'latent_sha256': digest(args.witness),
              'builder_sha256': digest(Path(__file__)),
              'symmetry': 'same pi acts on old words and all RZ nodes; family state is fixed',
              'transport': 'one table per hist/family, no group index',
              'family_product_rule': 'm(h,a,pi,s2,s3,s4,sM) = product_F transport_F(h,a,sF) / (720*latent_mass(h,a)^3)',
              'families': [], 'discovery': []}
    for family in FAMILIES:
        flow = data.product(family)
        product_audit = data.evaluate(family, flow)
        entry = {'family': family, 'product_diagnostic': product_audit,
                 'labels': data.labels[family], 'rule': 'hist conditional product'}
        if product_audit['negative_queries'] and not args.product_only:
            discovery, candidate = optimize(data, family)
            record['discovery'].append(discovery)
            if candidate is not None:
                flow = candidate
                entry['rule'] = 'one common rationalized max-margin transport'
        entry.update(data.evaluate(family, flow))
        entry['feasible'] = entry['minimum_query_slack'] >= 0
        entry['blocks'] = [{'hist_column': h,
                            'positive_flow': [{'atom': a, 'family_state_column': j, 'mass': m}
                                              for a, j, m in flow[h]]} for h in data.hist]
        record['families'].append(entry)
        print(json.dumps(serial({k: v for k, v in entry.items() if k not in
                                ('blocks', 'queries', 'product_diagnostic')}), ensure_ascii=False), flush=True)
    record['all_81_queries_feasible'] = all(f['feasible'] for f in record['families'])
    record['query_count'] = sum(f['query_count'] for f in record['families'])
    assert record['query_count'] == 81
    output = args.out_dir / ('product_probe.json' if args.product_only else 'fixed_A_attempt.json')
    save(output, record)


if __name__ == '__main__':
    main()
