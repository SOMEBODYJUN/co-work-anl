"""Current independent input/scale/orbit audit. Does not solve any LP or rerun the generator."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
from math import lcm
import hashlib
import json

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent / 'full156-tail-parent-report/original/research_5'
PAIR = HERE.parent / 'full156-pair-master-point/original/pair_master_exact.json'
PAT = tuple(product(range(2), repeat=3))


def canonical(*aa):
    seen, out = {}, []
    def cv(x):
        if x not in seen:
            seen[x] = len(seen)
        return seen[x]
    for a in aa:
        if a[0] == 'A':
            out.append(tuple(a))
        elif a[0] in ('T', 'B', 'C'):
            out.append((a[0], cv(a[1])))
        else:
            out.append((a[0], a[1], cv(a[2]), cv(a[3])))
    return tuple(out), len(seen)


def main():
    point = json.loads((SHARED / 'combined_branch_master_exact.json').read_text())
    zpoint = json.loads(PAIR.read_text())
    kernel = json.loads((SHARED / 'full156_tail2_kernel_10344.json').read_text())
    hs, denoms, hi = {}, [], None
    assert all(F(c['weight']) >= 0 for c in point['columns'])
    for j, c in enumerate(point['columns']):
        if c['kind'] == 'hist':
            hi = j
            mass = F(c['weight'])
            assert len(c['actual_bits']) == 6 and set(c['actual_bits']) <= {'0', '1'}
            assert len(c['hist']) == 8 and all(isinstance(n, int) and n >= 0 for n in c['hist'])
            assert sum(c['hist']) == 6
            hs[j] = {'a': c['actual_bits'], 'counts': c['hist'], 'mass': mass, 'raw': {}, 'slabs': {}}
            denoms.append(mass.denominator)
        elif c['kind'] == 'joint-reply':
            f, d, wi, wj = c['group']
            g = (f, d, tuple(wi), tuple(wj))
            st = tuple(c['state'])
            raw = hs[hi]['raw'].setdefault(g, {})
            assert st not in raw
            raw[st] = F(c['weight'])
    implicit_00 = []
    for h in hs.values():
        words = [w for w, n in zip(PAT, h['counts']) for _ in range(n)]
        groups = {(f, int(i == j), words[i], words[j]) for f, i, j in product(range(2), range(6), range(6)) if f or i != j}
        assert set(h['raw']) == groups
        for raw in h['raw'].values():
            assert set(raw) == {(0, 1), (1, 0), (1, 1)}
            residual = h['mass'] - sum(raw.values())
            assert residual >= 0
            implicit_00.append(residual)
        h['rad'] = {g: raw[1, 0] + raw[1, 1] for g, raw in h['raw'].items()}
        denoms += [r.denominator for r in h['rad'].values()]
    expected = []
    for hi, h in hs.items():
        if not h['mass']:
            continue
        cuts = sorted({F(0), h['mass'], *h['rad'].values()})
        for left, right in zip(cuts, cuts[1:]):
            assert 0 <= left < right <= h['mass']
            h['slabs'][left, right] = {}
            for g, r in h['rad'].items():
                f, d, wi, wj = g
                expected.append({'hist_column': hi, 'left': str(left), 'right': str(right),
                    'group': [f, d, list(wi), list(wj)], 'r': int(right <= r)})
    assert len(expected) == len(zpoint['variables']) == 364
    for want, got in zip(expected, zpoint['variables']):
        assert set(got) == set(want) | {'weight'}
        assert {k: got[k] for k in want} == want
        hi, left, right = got['hist_column'], F(got['left']), F(got['right'])
        f, d, wi, wj = got['group']
        g = (f, d, tuple(wi), tuple(wj))
        y = F(got['weight'])
        assert 0 <= y <= right - left
        hs[hi]['slabs'][left, right][g] = (got['r'], y)
        denoms.append(y.denominator)
    positive = [h for h in hs.values() if h['mass']]
    assert sum(h['mass'] for h in positive) == 1
    assert all(sum(n * w[0] for n, w in zip(h['counts'], PAT)) == 1 for h in positive)
    changed_z = 0
    for h in positive:
        for g, raw in h['raw'].items():
            new_z = sum(s[g][1] for s in h['slabs'].values())
            changed_z += new_z != raw[0, 1] + raw[1, 1]
    S = 720 * lcm(*denoms)
    assert S == int(kernel['unit_customer_scale'])
    assert 60 * S == int(kernel['payoff_denominator_for_normalized_point'])
    actions = [('A', i) for i in range(6)] + [(f, i) for f in ('T', 'B', 'C') for i in range(6)]
    actions += [(f, k, i, j) for f in ('R', 'Z') for k, i, j in product(range(2), range(6), range(6)) if k or i != j]
    assert [list(a) for a in actions] == kernel['original_descriptors']
    unary, pair = {canonical(a) for a in actions}, set()
    for a, b in product(actions, repeat=2):
        x, k = canonical(a, b)
        y, kk = canonical(b, a)
        assert k == kk
        pair.add((min(x, y), k))
    assert len(unary) + len(pair) == kernel['kernel_classes'] == 246
    report = {'scope': 'current input realization and orbit contract only; no LP row feasibility or payoff/welfare recomputation',
        'status': 'PASS', 'source_columns': len(point['columns']), 'nonnegative_source_weights': True,
        'hist_rows': len(hs), 'positive_hist_rows': len(positive), 'total_normalized_mass': '1',
        'raw_groups': len(implicit_00), 'implicit_00_minimum': str(min(implicit_00)),
        'raw_group_domains_and_three_states_exact': True, 'positive_hist_slabs': sum(len(h['slabs']) for h in positive),
        'pair_variables': len(expected), 'all_variable_metadata_regenerated_equal_in_order': True,
        'all_slab_bounds_R_bits_Z_bounds_valid': True, 'Z_marginals_different_from_old_raw': changed_z,
        'T_memberships_per_positive_hist': 1, 'unit_customer_scale': str(S),
        'payoff_denominator': str(60 * S), 'single_moment_orbits': len(unary), 'pair_moment_orbits': len(pair),
        'pair_orbits_by_comparison_indices': dict(sorted(Counter(k for _, k in pair).items())),
        'original_generator_runs_in_this_script': 0,
        'source_sha256': hashlib.sha256((SHARED / 'combined_branch_master_exact.json').read_bytes()).hexdigest(),
        'pair_source_sha256': hashlib.sha256(PAIR.read_bytes()).hexdigest()}
    (HERE / 'input-contract.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
