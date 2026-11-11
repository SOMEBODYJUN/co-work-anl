"""Read-only source replay and one static evaluation; no optimizer or grid.

Independently rebuild the 81 conditional-product costs and verify the saved
13853 product flows.  Use the already proved Boss1 six-facet/odd-cycle audit
to evaluate exactly one current Boss2 complete-ZZ point.  All outputs stay
in this agent's workspace.  The cycle implementation is explicitly reused,
not represented as an independent derivation of the Boss1 theorem.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RUN2 = HERE.parent
ROOT = HERE.parents[3]
RUN1 = ROOT / 'research/workspaces/six-boss1-20261111'
STATES = tuple(product((0, 1), repeat=2))
ORBIT_SIZE = {(0, 0): 30, (1, 0): 30, (1, 1): 6}
FAMILIES = ('B2', 'B3', 'B4', 'Mroot')
CURRENT = RUN2 / 'master_cuts/complete_zz_5799_v1_original4849_exact.json'
CURRENT_SHA = '1af6fd35f9cf1a51220072e627df042b450a52a7c6ecac388a98247ecac043d2'
SOURCE = RUN1 / 'sorting_closure_lp/augmented_lp_exact.json'
SOURCE_SHA = '6bfe2ff663803e80aa30b900f609b300617ee6f62f02f898349e2bb4c95a8f07'
WITNESS = RUN1 / 'tail_constraints/sorting13853-exact-product-witness.json'
WITNESS_SHA = '2a4b762d8525a355671e0c39093a2459a417e49b9b5b376818d7cf05f98f4dd5'


def freeze(x):
    return tuple(freeze(t) for t in x) if isinstance(x, list) else x


def serial(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def load(path, expected=None):
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    if expected is not None:
        assert digest == expected
    return json.loads(raw), digest


def parse(point):
    cols = point['columns'][:4849]
    masses = [F(c['weight']) for c in cols]
    hist = {j: c for j, c in enumerate(cols) if c['kind'] == 'hist'}
    groups = defaultdict(dict)
    family = {f: defaultdict(list) for f in FAMILIES}
    current_hist = None
    labels = {}
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            current_hist = j
        elif c['kind'] == 'joint-reply':
            g = freeze(c['group'])
            groups[current_hist].setdefault(g, {})[tuple(c['state'])] = j
        elif c['kind'] in ('actual-B-family-state', 'maximum-root-family-state'):
            h = c['hist_column']
            a = tuple(map(int, hist[h]['actual_bits']))
            hidden = tuple(c['hidden'])
            if c['kind'] == 'actual-B-family-state':
                source = c['source']
                f = f'B{source}'
                seq = a[:source - 1] + (a[5],) + hidden
                members = hidden + (F(c['ell'], 6),)
                labs = tuple(f'H{i + 1}' for i in range(len(hidden))) + ('Y-average',)
            else:
                f = 'Mroot'
                seq = (c['M'],) + hidden
                members = seq + (F(c['ell'], 6),)
                labs = ('M',) + tuple(f'H{i + 1}' for i in range(5)) + ('Y-average',)
            assert len(seq) == 6
            denom = 1 + sum(seq[:-1])
            family[f][h].append((j, masses[j], denom, F(seq[-1], denom), members))
            assert f not in labels or labels[f] == labs
            labels[f] = labs
    for h, gs in groups.items():
        words = Counter({tuple(w): n for w, n in zip(product((0, 1), repeat=3), hist[h]['hist'])})
        totals = defaultdict(F)
        for g, ids in list(gs.items()):
            assert set(ids) == set(STATES[1:])
            rho = (masses[h] - sum(masses[j] for j in ids.values()),
                   *(masses[ids[s]] for s in STATES[1:]))
            assert min(rho) >= 0
            f, diag, wi, wj = g
            count = words[wi] if diag else words[wi] * (words[wj] - int(wi == wj))
            omega = F(count, ORBIT_SIZE[f, diag])
            assert count > 0
            totals[f, diag] += omega
            gs[g] = (ids, rho, omega)
        assert dict(totals) == {o: F(1) for o in ORBIT_SIZE}
        for f in FAMILIES:
            assert sum(s[1] for s in family[f][h]) == masses[h]
    assert len(hist) == 16 and sum(map(len, groups.values())) == 194
    return cols, masses, hist, groups, family, labels


def product_report(point, saved=None):
    cols, masses, hist, groups, family, labels = parse(point)
    saved_families = {f['family']: f for f in saved['families']} if saved else {}
    reports = []
    full_cells = verified_flows = verified_marginals = 0
    for f in FAMILIES:
        costs = defaultdict(F)
        terminal = sum(s[1] * s[3] for ss in family[f].values() for s in ss)
        old_z = defaultdict(F)
        saved_blocks = {(b['hist_column'], freeze(b['group'])): b
                        for b in saved_families.get(f, {}).get('blocks', [])}
        expected_blocks = set()
        for h, gs in groups.items():
            mu = masses[h]
            p4 = sum(map(int, hist[h]['actual_bits'][:4]))
            ss = family[f][h]
            price_mass = sum(mass / denom for _, mass, denom, _, _ in ss)
            members = [sum(s[1] * s[4][i] for s in ss) for i in range(len(labels[f]))]
            for g, (_, rho, omega) in gs.items():
                orbit = g[:2]
                full_cells += 4 * len(ss)
                old_z[orbit] += omega * sum(mass * F(z, p4 + r + 1)
                                            for (r, z), mass in zip(STATES, rho))
                if not mu:
                    assert not any(rho) and not any(s[1] for s in ss)
                    continue
                expected_blocks.add((h, g))
                q = rho[2] + rho[3]
                v = rho[1] + rho[3]
                price_old = sum(mass / (p4 + r + 1)
                                for (r, _), mass in zip(STATES, rho))
                costs['new-to-R', orbit] += omega * q * price_mass / mu
                costs['new-to-Z', orbit] += omega * v * price_mass / mu
                for i, label in enumerate(labels[f]):
                    costs['Z-to-new', orbit, i, label] += omega * members[i] * price_old / mu
                if saved is not None:
                    b = saved_blocks[h, g]
                    assert F(b['hist_mass']) == mu
                    assert tuple(map(F, b['old_four_state_masses'])) == rho
                    flow = {(tuple(e['old_state']), e['new_state_column']): F(e['mass'])
                            for e in b['positive_flow']}
                    assert len(flow) == len(b['positive_flow'])
                    expected = {(rz, j): mass * eta / mu
                                for rz, mass in zip(STATES, rho)
                                for j, eta, _, _, _ in ss if mass and eta}
                    assert flow == expected
                    for rz, mass in zip(STATES, rho):
                        assert sum(vv for (state, _), vv in flow.items() if state == rz) == mass
                    for j, eta, _, _, _ in ss:
                        assert sum(vv for (_, col), vv in flow.items() if col == j) == eta
                    verified_flows += len(flow)
                    verified_marginals += 4 + len(ss)
        if saved is not None:
            assert set(saved_blocks) == expected_blocks
        queries = []
        for orbit in ORBIT_SIZE:
            specs = [('new-to-R', orbit), ('new-to-Z', orbit)]
            specs += [('Z-to-new', orbit, i, lab) for i, lab in enumerate(labels[f])]
            for spec in specs:
                budget = old_z[orbit] if spec[0] == 'Z-to-new' else terminal
                queries.append({'query': spec, 'budget': budget, 'cost': costs[spec],
                                'slack': budget - costs[spec]})
        if saved is not None:
            assert serial(queries) == saved_families[f]['queries']
        minimum = min(q['slack'] for q in queries)
        reports.append({'family': f, 'queries': queries, 'query_count': len(queries),
                        'minimum_slack': minimum, 'minimum_slack_float': float(minimum),
                        'feasible': minimum >= 0, 'labels': labels[f]})
    assert sum(r['query_count'] for r in reports) == 81
    return {'all_81_product_costs_feasible': all(r['feasible'] for r in reports),
            'full_domain_cells': full_cells, 'saved_positive_flows_verified': verified_flows,
            'saved_positive_block_marginal_equalities_verified': verified_marginals,
            'families': reports}


def main():
    output = HERE / 'boss1_transport_static_zz_v1.json'
    assert not output.exists(), 'frozen output already exists'
    source, ssha = load(SOURCE, SOURCE_SHA)
    saved, wsha = load(WITNESS, WITNESS_SHA)
    current, csha = load(CURRENT, CURRENT_SHA)
    assert saved['input_sha256'] == ssha
    desc = lambda p: [{k: v for k, v in c.items() if k != 'weight'}
                      for c in p['columns'][:4849]]
    assert desc(source) == desc(current)
    dsha = sha256(json.dumps(desc(current), ensure_ascii=False, sort_keys=True,
                            separators=(',', ':')).encode()).hexdigest()
    source_report = product_report(source, saved)
    assert source_report['all_81_product_costs_feasible']
    current_report = product_report(current)
    sys.path.insert(0, str(RUN1 / 'zz_cyclic_math'))
    import audit_cycles
    import audit_three_cycles
    two = audit_cycles.audit(CURRENT)
    three = audit_three_cycles.audit(CURRENT)
    assert two['input_sha256'] == three['input_sha256'] == csha
    assert two['original_columns_sha256'] == three['original_columns_sha256'] == dsha
    out = {
        'scope': 'One static Boss2 complete-ZZ point; original Boss1 witness replay; no LP/grid/SPE claim',
        'optimizer_calls': 0, 'source_point_sha256': ssha, 'source_product_witness_sha256': wsha,
        'current_point_sha256': csha, 'original4849_descriptors_exactly_equal': True,
        'original4849_descriptor_sha256': dsha,
        'source_81_product_replay': source_report,
        'current_81_specific_product_completion': current_report,
        'current_two_node_six_facets': two, 'current_three_node_odd_cycles': three,
        'cycle_implementation': 'Reused already-proved Boss1 audit, not an independent theorem verifier',
        'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_files': {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest()
                         for p in [RUN1 / 'tail_constraints/conditional_product_witness.py',
                                   RUN1 / 'tail_constraints/transport_separator.py',
                                   RUN1 / 'zz_cyclic_math/audit_cycles.py',
                                   RUN1 / 'zz_cyclic_math/audit_three_cycles.py']},
    }
    tmp = output.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(serial(out), ensure_ascii=False, indent=2) + '\n')
    tmp.replace(output)
    print(json.dumps({'status': 'exact_static_audit_complete', 'output': str(output),
                      'sha256': sha256(output.read_bytes()).hexdigest(),
                      'source_81_exact_replay': True,
                      'current_81_product_feasible': current_report['all_81_product_costs_feasible'],
                      'current_product_minima': [r['minimum_slack_float'] for r in current_report['families']],
                      'two_node_negative': two['negative_count'], 'two_node_improved': two['improved_count'],
                      'three_node_negative': three['negative_count'], 'three_node_improved': three['improved_count']},
                     ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
