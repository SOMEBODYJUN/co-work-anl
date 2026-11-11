"""Read frozen descriptors; export the 210 common-X own-block interfaces.

No old point weights are evaluated, no LP is imported, and no parent matrix is
written.  The six-facet package is specified symbolically, not appended here.
"""
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
POINT = BASE / 'full624_augmented_lp/recovery/augmented_lp_exact.json'
ENVELOPE = BASE / 'maxb_augmented_lp/full_lift/maxb_envelope_structure.json'
LIFT = BASE / 'terminal_response_cycles/max_b_symbolic_lift.json'


def freeze(value):
    return tuple(map(freeze, value)) if isinstance(value, list) else value


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def main():
    raw = json.loads(POINT.read_text())
    # Descriptor-only use: deliberately do not parse or evaluate any weight.
    old = [{k: v for k, v in c.items() if k != 'weight'} for c in raw['columns'][:4849]]
    env = json.loads(ENVELOPE.read_text())
    lift = json.loads(LIFT.read_text())
    assert len(lift['new_columns']) == 436
    xmap = dict(env['hist_to_x'])
    lookup = {(r['hist_column'], freeze(r['query_token'])): r for r in env['auxiliaries']}
    own, b4, hist = defaultdict(dict), defaultdict(dict), {}
    for j, c in enumerate(old):
        if c['kind'] == 'hist':
            h = j
            hist[h] = c
        elif c['kind'] == 'joint-reply':
            own[h, freeze(c['group'])][tuple(c['state'])] = j
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            b4[c['hist_column']][tuple(c['hidden']) + (c['ell'] // 6,)] = j
    assert len(hist) == 16 and len(own) == 194 and len(b4) == 16

    blocks = []
    for r in env['auxiliaries']:
        h, token = r['hist_column'], freeze(r['query_token'])
        if token[0] == 'R':
            g = token[1]
            d = own[h, g]
            assert set(d) == {(0, 1), (1, 0), (1, 1)}
            m = {
                '00': [[h, '1']] + [[d[s], '-1'] for s in sorted(d)],
                '10': [[d[1, 0], '1']],
                '01': [[d[0, 1], '1']],
                '11': [[d[1, 1], '1']],
            }
            mate = lookup[h, ('Z', g)]
            key, labels = ['own-RZ', h, g], ['R', 'Z']
        elif token == ('H', 0):
            d = b4[h]
            assert set(d) == {tuple(map(int, f'{k:03b}')) for k in range(8)}
            m = {f'{a}{b}': [[j, '1'] for s, j in sorted(d.items()) if s[:2] == (a, b)]
                 for a in (0, 1) for b in (0, 1)}
            mate = lookup[h, ('H', 1)]
            key, labels = ['B4-H1H2', h], ['H1', 'H2']
        else:
            continue
        assert mate['x_column'] == r['x_column'] == xmap[h]
        blocks.append(dict(block=len(blocks), key=key, labels=labels,
                           H_column=h, X_column=xmap[h],
                           yQ_column=r['column'], yR_column=mate['column'],
                           mass_by_QR=m,
                           old_upper_rows=[r['x_upper_row'], r['query_upper_row'],
                                           mate['x_upper_row'], mate['query_upper_row']]))
    assert len(blocks) == 210
    assert sorted([b[k] for b in blocks for k in ('yQ_column', 'yR_column')]) == list(range(20601, 21021))
    expected = {j: c for j, c in enumerate(old)}
    expected.update({20585 + i: c for i, c in enumerate(lift['new_columns'])})
    used = sorted({b[k] for b in blocks for k in ('H_column', 'X_column', 'yQ_column', 'yR_column')} |
                  {j for b in blocks for r in b['mass_by_QR'].values() for j, _ in r})
    fingerprint = [[j, expected[j]] for j in used]
    groups = [[h, w] for h, c in hist.items() for w, n in enumerate(c['hist']) if n]
    assert len(groups) == 38
    output = dict(
        status='SYMBOLIC_OWN_INTERFACE_ONLY_NO_POINT_EVALUATED',
        coordinate_count=21021, block_count=210, own_RZ_blocks=194, B4_H1H2_blocks=16,
        facets_per_block=6, planned_additional_rows=1260, additional_columns_after_beta_elimination=0,
        sources=[dict(path=str(p.relative_to(BASE)), sha256=digest(p)) for p in (POINT, ENVELOPE, LIFT)],
        facet_order=['yQ+yR-x+m00', 'm10-yQ+yR', 'm01+yQ-yR',
                     'm00+m10-x+yR', 'm00+m01-x+yQ', 'x+m11-yQ-yR'],
        beta_lower_order=['0', 'yQ-m10', 'yR-m01', 'yQ+yR-x'],
        beta_upper_order=['m11', 'yQ', 'yR', 'm00-x+yQ+yR'],
        expected_column_indices=used,
        expected_descriptor_sha256=sha256(canonical(fingerprint)).hexdigest(),
        hist_records=[[h, c] for h, c in hist.items()], root_groups=groups,
        blocks=blocks,
        warning='Fixed supplied X/y failure excludes only those values; no re-optimization or claim about all X/y completions.',
    )
    (HERE / 'own_blocks.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: output[k] for k in ('status', 'block_count', 'planned_additional_rows',
                                            'additional_columns_after_beta_elimination')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
