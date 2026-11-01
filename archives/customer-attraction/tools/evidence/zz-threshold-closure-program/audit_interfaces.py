"""Read all three saved Z-slab points and independently sum their 60 Z->Z rows.

This never imports an author builder or optimizer, and does not certify the
3889/3945/4927 old rows for the split/cross outputs.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

PAT = tuple(product((0, 1), repeat=3))


def group(v):
    return v[0], v[1], tuple(v[2]), tuple(v[3])


def equality_pattern(indices):
    first = {}
    for x in indices:
        if x not in first:
            first[x] = len(first)
    return tuple(first[x] for x in indices)


def audit(source, saved, expected_rows):
    raw, eraw = source.read_bytes(), saved.read_bytes()
    old, point = json.loads(raw), json.loads(eraw)
    assert point['source_sha256'] == sha256(raw).hexdigest()
    cols = old['columns']
    weights = [F(c['weight']) for c in cols]
    assert len(cols) == 1905 and min(weights) >= 0
    hs, nearest = {}, None
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            nearest = j
            assert sum(c['hist']) == 6
            assert c['d'] == sum(n*w[0] for n, w in zip(c['hist'], PAT)) == 1
            hs[j] = {'column': c, 'mass': weights[j], 'groups': {}}
        elif c['kind'] == 'joint-reply':
            g, state = group(c['group']), tuple(c['state'])
            block = hs[nearest]['groups'].setdefault(g, {})
            assert state not in block
            block[state] = weights[j]
    expected, bounds, slabs = [], [], []
    for hi, h in hs.items():
        hm = h['mass']
        for st in h['groups'].values():
            assert set(st) == {(0, 1), (1, 0), (1, 1)} and sum(st.values()) <= hm
        if not hm:
            continue
        rm = {g: st[1, 0]+st[1, 1] for g, st in h['groups'].items()}
        assert all(0 <= r <= hm for r in rm.values())
        cuts = sorted({F(), hm, *rm.values()})
        for left, right in zip(cuts, cuts[1:]):
            assert left < right
            gs, rs = {}, {}
            for g in h['groups']:
                rs[g] = int(right <= rm[g])
                gs[g] = len(expected)
                expected.append({'hist_column': hi, 'left': str(left), 'right': str(right),
                                 'group': [g[0], g[1], list(g[2]), list(g[3])], 'r': rs[g]})
                bounds.append(right-left)
            slabs.append((hi, gs, rs))
    assert len(hs) == 16
    assert expected == [{k:v for k,v in z.items() if k != 'weight'} for z in point['variables']]
    ys = [F(z['weight']) for z in point['variables']]
    assert len(ys) == point['variables_count'] == len(expected)
    assert all(0 <= y <= b for y,b in zip(ys,bounds))
    W = sum(weights[j] for j,h in hs.items() if '1' in h['column']['actual_bits'])
    O = sum(h['mass'] for h in hs.values())
    assert str(W) == point['W'] == old['W'] and O == F(point['O']) == 1
    assert point['rows'] == expected_rows and point['minimum_slack'] == '0'
    assert sum(y > 0 for y in ys) == point['positive_variables']
    interior = sum(0 < y < b for y,b in zip(ys,bounds))
    assert interior == point['free_vertex_variables']
    patterns = sorted({equality_pattern(x) for x in product(range(4), repeat=4)})
    assert len(patterns) == 15
    zz = {(f,g,p): F() for f,g,p in product(range(2),range(2),patterns)}
    for hi, gs, rs in slabs:
        c = hs[hi]['column']; pa = sum(map(int,c['actual_bits'][:4]))
        words = [w for w,n in zip(PAT,c['hist']) for _ in range(n)]
        edges = [(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i != j]
        assert len(edges) == 66
        def g_of(e):
            f,i,j = e
            return f,int(i == j),words[i],words[j]
        for f,i,j in edges:
            ge = g_of((f,i,j))
            for g,k,l in edges:
                gf = g_of((g,k,l))
                zz[f,g,equality_pattern((i,j,k,l))] += (ys[gs[ge]]-ys[gs[gf]]) / (pa+1+rs[ge])
    assert len(zz) == 60 and min(zz.values()) >= 0
    return {'status':'PASS_INPUT_INTERFACE_AND_60_ZZ_ROWS',
            'source_sha256':sha256(raw).hexdigest(),'saved_sha256':sha256(eraw).hexdigest(),
            'source_bytes':len(raw),'saved_bytes':len(eraw),
            'original_metadata':{k:v for k,v in point.items() if k!='variables'},
            'source_columns_read':len(cols),'histograms':len(hs),
            'positive_histograms':sum(h['mass']>0 for h in hs.values()),
            'slabs':len(slabs),'variables':len(ys),'all_variable_descriptors_equal':True,
            'all_mass_bounds_exact':True,'positive_variables':sum(y>0 for y in ys),
            'strict_interior_variables':interior,'source_O':str(O),'source_W':str(W),
            'ZZ_rows':len(zz),'ZZ_zero_rows':sum(v==0 for v in zz.values()),
            'minimum_ZZ_slack':str(min(zz.values())),
            'all_ZZ_slacks':[{'family':f,'query_family':g,'equality_pattern':list(p),'slack':str(v)}
                             for (f,g,p),v in zz.items()],
            'limits':'Does not regenerate old graph rows, prove vertex rank/uniqueness, exact optimum, or a complete-history SPE.'}


if __name__ == '__main__':
    p=ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--saved-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();e=a.repo/'archives/customer-attraction/tools/evidence'
    jobs=[('default',e/'combined-branch-master-program/dependencies/research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json','zz_threshold_exact.json',3949),
          ('split',e/'split-basic-graph-program/related/split_basic_exact.json','zz_split_exact.json',4005),
          ('cross',e/'cross-source-graph-program/related/cross_source_priced_optimum_exact.json','zz_cross_exact.json',4987)]
    out={'scope':'all three frozen variable tables and independent 60-ZZ-row integration per table; no graph build or LP',
         'auditor_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'modes':{mode:audit(source,a.saved_dir/file,rows) for mode,source,file,rows in jobs}}
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({mode:{k:v for k,v in r.items() if k not in ['all_ZZ_slacks','original_metadata']}
                      for mode,r in out['modes'].items()},ensure_ascii=False,indent=2))
