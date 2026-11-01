"""Read every cross-Z record, construct a common cube, and compare saved events.

No graph builder, optimizer, prior 60-ZZ audit, or original verifier is invoked.
One omitted early-R query is evaluated directly to state the SPE obstruction.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from collections import Counter, defaultdict
from math import lcm
import ast
import json
import sys


def group(g):
    return g[0], g[1], tuple(g[2]), tuple(g[3])


def main():
    if len(sys.argv) != 4:
        raise SystemExit('usage: audit.py repo original-event-dir new-audit-output-dir')
    repo, event, out = map(lambda x: Path(x).resolve(), sys.argv[1:])
    out.mkdir(parents=True, exist_ok=False)
    evidence = repo / 'archives/customer-attraction/tools/evidence'
    point_path = evidence / 'zz-threshold-closure-program/related/zz_cross_exact.json'
    base_path = evidence / 'cross-source-graph-program/related/cross_source_priced_optimum_exact.json'
    raw, base_raw = point_path.read_bytes(), base_path.read_bytes()
    point, base = json.loads(raw), json.loads(base_raw)
    assert sha256(raw).hexdigest() == '239ab62a100cd77f12cc9b8d131048e87babccb2103c781953af33909c364111'
    assert sha256(base_raw).hexdigest() == point['source_sha256'] == '955c456ad3381a8cdc72139ba9ccc73dfe70297183e72727ae6ad165dc80e947'
    # Complete lossless reading: retain every top-level field and every record.
    rational_strings, rational_ids, groups, group_ids, encoded = [], {}, [], {}, []
    def rid(s):
        F(s)
        if s not in rational_ids:
            rational_ids[s] = len(rational_strings)
            rational_strings.append(s)
        return rational_ids[s]
    def gid(g):
        key = json.dumps(g, separators=(',', ':'))
        if key not in group_ids:
            group_ids[key] = len(groups)
            groups.append(g)
        return group_ids[key]
    for z in point['variables']:
        assert list(z) == ['hist_column', 'left', 'right', 'group', 'r', 'weight']
        encoded.append([z['hist_column'], rid(z['left']), rid(z['right']), gid(z['group']), z['r'], rid(z['weight'])])
    reading = {'source_sha256': sha256(raw).hexdigest(), 'top_fields_in_original_order': {k: v for k, v in point.items() if k != 'variables'}, 'rational_strings': rational_strings, 'groups': groups, 'row_columns': ['hist_column', 'left_rational_id', 'right_rational_id', 'group_id', 'r', 'weight_rational_id'], 'all_302_rows': encoded}
    rebuilt = dict(reading['top_fields_in_original_order'])
    rebuilt['variables'] = [{'hist_column': h, 'left': rational_strings[l], 'right': rational_strings[u], 'group': groups[g], 'r': r, 'weight': rational_strings[y]} for h, l, u, g, r, y in encoded]
    assert (json.dumps(rebuilt, indent=2) + '\n').encode() == raw
    (out / 'lossless-reading.json').write_text(json.dumps(reading, ensure_ascii=False, indent=2) + '\n')
    cols = base['columns']
    old_weights = [F(c['weight']) for c in cols]
    new_weights = [F()] * len(cols)
    new_weights[0] = old_weights[0]
    hs, current = {}, None
    for j, col in enumerate(cols):
        if col['kind'] == 'hist':
            current = j
            words = tuple(w for w, n in zip(product((0, 1), repeat=3), col['hist']) for _ in range(n))
            hs[j] = {'column': col, 'words': words, 'groups': {}, 'slabs': []}
            new_weights[j] = old_weights[j]
        elif col['kind'] == 'joint-reply':
            hs[current]['groups'].setdefault(group(col['group']), {})[tuple(col['state'])] = j
    slabs = {}
    for j, v in enumerate(point['variables']):
        slabs.setdefault((v['hist_column'], v['left'], v['right']), []).append(j)
    recovered = [F()] * len(point['variables'])
    cube = []
    for (hi, left, right), indices in slabs.items():
        mass = F(right) - F(left)
        free, fixed, rbits = [], {}, []
        for local, j in enumerate(indices):
            v = point['variables'][j]
            y, r = F(v['weight']), v['r']
            assert 0 <= y <= mass and r in (0, 1)
            rbits.append(r)
            if y == 0 or y == mass:
                fixed[local] = int(y == mass)
            else:
                free.append(local)
            target = hs[hi]['groups'][group(v['group'])]
            if r:
                new_weights[target[1, 0]] += mass - y
                new_weights[target[1, 1]] += y
            else:
                new_weights[target[0, 1]] += y
        atoms = []
        for bits in product((0, 1), repeat=len(free)):
            zb = [fixed.get(k, 0) for k in range(len(indices))]
            probability = F(1)
            for local, bit in zip(free, bits):
                zb[local] = bit
                p = F(point['variables'][indices[local]]['weight']) / mass
                probability *= p if bit else 1 - p
            weight = mass * probability
            assert weight > 0
            for local, bit in enumerate(zb):
                if bit:
                    recovered[indices[local]] += weight
            atoms.append({'Z_bits': ''.join(map(str, zb)), 'mass': str(weight)})
        assert sum((F(x['mass']) for x in atoms), F()) == mass
        cube.append({'hist_column': hi, 'left': left, 'right': right, 'variable_indices': indices, 'R_bits': ''.join(map(str, rbits)), 'free_Z_count': len(free), 'atoms': atoms})
        hs[hi]['slabs'].append({'left': left, 'right': right, 'variables': len(indices), 'positive': sum(F(point['variables'][j]['weight']) > 0 for j in indices), 'free': len(free), 'atoms': len(atoms)})
    assert recovered == [F(z['weight']) for z in point['variables']]
    assert len(cube) == 24 and sum(len(s['atoms']) for s in cube) == 227
    l = 1
    for s in cube:
        for atom in s['atoms']:
            l = lcm(l, F(atom['mass']).denominator)
    unit_scale = 720 * l
    assert all((F(a['mass']) * unit_scale / 720).denominator == 1 for s in cube for a in s['atoms'])
    (out / 'conditional-cube-atoms.json').write_text(json.dumps({'scope': 'One representative six-word assignment per histogram; average all 720 index permutations to obtain the full labelled catalogue. No strategy or payoff matrix is supplied.', 'unit_customer_scale_after_720_permutations': str(unit_scale), 'slabs': cube}, ensure_ascii=False, indent=2) + '\n')
    marginal_changes = []
    for hi, h in hs.items():
        for g, states in h['groups'].items():
            old_r = old_weights[states[1, 0]] + old_weights[states[1, 1]]
            new_r = new_weights[states[1, 0]] + new_weights[states[1, 1]]
            assert old_r == new_r
            assert sum(new_weights[j] for j in states.values()) <= old_weights[hi]
            old_z = old_weights[states[0, 1]] + old_weights[states[1, 1]]
            new_z = new_weights[states[0, 1]] + new_weights[states[1, 1]]
            if old_z != new_z:
                marginal_changes.append({'hist_column': hi, 'group': [g[0], g[1], list(g[2]), list(g[3])], 'old_Z': str(old_z), 'new_Z': str(new_z), 'difference': str(new_z - old_z)})
    for j, c in enumerate(cols):
        if c['kind'] == 'overlap':
            h = hs[c['hist_column']]
            st1, st2 = [h['groups'][group(g)] for g in c['groups']]
            new_weights[j] = min(old_weights[st1[1, 0]] + old_weights[st1[1, 1]], old_weights[st2[1, 0]] + old_weights[st2[1, 1]])
    assert new_weights == [F(x) for x in json.loads((event / 'affine-lifted-weights.json').read_text())]
    changed = [{'column': j, 'kind': col['kind'], 'old': str(a), 'new': str(b), 'difference': str(b - a)} for j, (col, a, b) in enumerate(zip(cols, old_weights, new_weights)) if a != b]
    (out / 'changed-coordinates.json').write_text(json.dumps({'coordinate_changes': changed, 'Z_marginal_changes': marginal_changes}, ensure_ascii=False, indent=2) + '\n')
    # One named omitted floor: actual third player, family-0 off-diagonal R.
    source_profit = F()
    old_query = new_query = F()
    for hi, h in hs.items():
        a = tuple(map(int, h['column']['actual_bits']))
        if a[2]:
            source_profit += old_weights[hi] * F(1, sum(a))
        denominator = sum(a[:2]) + 4
        for i, j in product(range(6), repeat=2):
            if i == j:
                continue
            st = h['groups'][0, 0, h['words'][i], h['words'][j]]
            old_query += (old_weights[st[1, 0]] + old_weights[st[1, 1]]) / denominator
            new_query += (new_weights[st[1, 0]] + new_weights[st[1, 1]]) / denominator
    floor = 30 * source_profit - new_query
    assert old_query == new_query
    assert floor == F(-4749850661723892253166888285611, 107365313311072858536618851786648)
    rows = json.loads((event / 'all-row-slacks.json').read_text())
    prior_path = evidence / 'zz-threshold-closure-program/interface-audit.json'
    prior = json.loads(prior_path.read_text())['modes']['cross']
    for a, b in zip(rows[4927:], prior['all_ZZ_slacks'], strict=True):
        f, g, pat = ast.literal_eval(a['name'][4:])
        assert (f, g, list(pat)) == (b['family'], b['query_family'], b['equality_pattern'])
        assert F(a['slack']) == F(b['slack'])
    w = sum(old_weights[hi] for hi, h in hs.items() if '1' in h['column']['actual_bits'])
    assert w == F(point['W']) and sum(old_weights[hi] for hi in hs) == F(point['O']) == 1
    assert all(sum(w[0] for w in h['words']) == 1 for h in hs.values())
    hist_table = [{'hist_column': hi, 'actual_bits': h['column']['actual_bits'], 'hist': h['column']['hist'], 'mass': str(old_weights[hi]), 'groups': len(h['groups']), 'slabs': h['slabs']} for hi, h in hs.items()]
    result = {'status': 'PASS_LOSSLESS_FULL_READ_COMMON_CUBE_AND_SAVED_RUN_COMPARISON', 'scope': '302 records losslessly decoded; independent affine-coordinate and 227 conditional-atom construction; one omitted R-floor evaluated. No old matrix or 60-ZZ generator rerun.', 'audit_sha256': sha256(Path(__file__).read_bytes()).hexdigest(), 'point_sha256': sha256(raw).hexdigest(), 'base_source_sha256': sha256(base_raw).hexdigest(), 'original_bytes_reconstructed_exactly': True, 'records': len(encoded), 'rational_strings': len(rational_strings), 'group_descriptors': len(groups), 'histograms': hist_table, 'slabs': len(cube), 'conditional_atoms': sum(len(s['atoms']) for s in cube), 'unit_scale_decimal_digits': len(str(unit_scale)), 'all_302_Z_marginals_from_atoms_match': True, 'all_194_R_marginals_unchanged': True, 'affine_1905_values_match_original_capture': True, 'coordinate_changes': dict(Counter(c['kind'] for c in changed)), 'total_coordinate_changes': len(changed), 'Z_marginal_changes': len(marginal_changes), 'bounds_statistics': {'zero': sum(F(z['weight']) == 0 for z in point['variables']), 'upper': sum(F(z['weight']) == F(z['right'])-F(z['left']) for z in point['variables']), 'interior': sum(0 < F(z['weight']) < F(z['right'])-F(z['left']) for z in point['variables'])}, 'source_W_independently_recomputed': str(w), 'O_and_actual_OPT6_for_realization': '1', 'strict_half_gap': str(1-2*w), 'saved_original_and_prior_independent_ZZ_slacks_equal': 60, 'one_omitted_floor': {'key': [2, 0, 0, 0], 'actual_player_one_based': 3, 'source_profit': str(source_profit), 'query_sum': str(new_query), 'slack': str(floor), 'unchanged_from_old_R_source': True, 'conclusion': 'No complete SPE with these labelled actual/hist/R statistics; does not exclude other points or prove general half.'}}
    (out / 'data-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('histograms',)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
