"""Independent Boolean-envelope audit of the original 4849 coordinates.

No original matrix builder is imported. This checks descriptors, the sign
contract of the RR envelope, exact replacement by min marginals, and the
known free-R ZZ Frechet bounds at a specified current point. It is not an
SPE realization or full-domain welfare certificate.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import gzip
import json
from pathlib import Path


def key(raw):
    return raw[0], raw[1], tuple(raw[2]), tuple(raw[3])


def partition(xs):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in xs)


def add(row, j, v):
    if v:
        row[j] = row.get(j, F()) + v
        if not row[j]:
            del row[j]


def dot(row, mass):
    return sum((v * mass[j] for j, v in row.items()), F())


def parse(path):
    raw = path.read_bytes()
    report = json.loads(raw)
    cols = report['columns'][:4849]
    assert len(cols) == 4849
    mass = [F(c['weight']) for c in cols]
    assert min(mass) >= 0
    hist = {i: c for i, c in enumerate(cols) if c['kind'] == 'hist'}
    groups = defaultdict(dict)
    current_hist = None
    old_hist = {}
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            current_hist = j
        elif c['kind'] == 'joint-reply':
            h = c['hist_column_old']
            if h in old_hist:
                assert old_hist[h] == current_hist
            old_hist[h] = current_hist
            groups[current_hist].setdefault(key(c['group']), {})[tuple(c['state'])] = j
    moments = {}
    for hi, gs in groups.items():
        for g, ids in gs.items():
            assert set(ids) == {(0, 1), (1, 0), (1, 1)}
            q = mass[ids[1, 0]] + mass[ids[1, 1]]
            v = mass[ids[0, 1]] + mass[ids[1, 1]]
            t = mass[ids[1, 1]]
            assert min(t, q-t, v-t, mass[hi]-q-v+t) >= 0
            moments[hi, g] = q, v, t
    family = defaultdict(list)
    for j, c in enumerate(cols):
        if c['kind'] in ('actual-B-family-state', 'maximum-root-family-state'):
            fam = ('B', c['source']) if 'source' in c else ('M', 0)
            family[fam, c['hist_column']].append(j)
    for (fam, hi), ids in family.items():
        assert sum((mass[j] for j in ids), F()) == mass[hi]
    return raw, report, cols, mass, hist, groups, moments, family


def zz_bounds(cols, mass, hist, groups, moments):
    rows = defaultdict(dict)
    direct = defaultdict(F)
    per_hist = defaultdict(lambda: defaultdict(F))
    selections = defaultdict(Counter)
    # Keep every literal pair; only exact index identity is a self query.
    edges = [(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i != j]
    count = Counter()
    for hi, h in hist.items():
        words = [w for w,n in zip(product(range(2), repeat=3),h['hist']) for _ in range(n)]
        def g(e):
            return e[0], int(e[1] == e[2]), words[e[1]], words[e[2]]
        p = sum(map(int,h['actual_bits'][:4])); D = (p+1)*(p+2)
        for e in edges:
            ge = g(e); qe,ve,te = moments[hi,ge]; ie = groups[hi][ge]
            for f in edges:
                name = (e[0],f[0],partition((e[1],e[2],f[1],f[2])))
                count[name] += 1
                row = rows[name]
                if e == f:
                    continue
                gf = g(f); qf,vf,tf = moments[hi,gf]; jf = groups[hi][gf]
                bound = (ve-vf)/F(p+1) + (min(qe,vf)-te)/F(D)
                direct[name] += bound
                per_hist[name][hi] += bound
                for st in ((0,1),(1,1)):
                    add(row,ie[st],F(1,p+1)); add(row,jf[st],-F(1,p+1))
                add(row,ie[1,1],-F(1,D))
                # Any fixed choice is a necessary linear upper bound; this
                # choice realizes the exact minimum at the input point.
                if qe <= vf:
                    selections[name][(hi,ge,gf,'R-source')] += 1
                    for st in ((1,0),(1,1)): add(row,ie[st],F(1,D))
                else:
                    selections[name][(hi,ge,gf,'Z-query')] += 1
                    for st in ((0,1),(1,1)): add(row,jf[st],F(1,D))
    out=[]
    for name, row in sorted(rows.items()):
        value = dot(row,mass)
        assert value == direct[name]
        out.append({'name':name,'literal_pair_hist_terms':count[name],
                    'literal_pairs_per_hist':count[name]//len(hist),
                    'value':str(value),'direct_frechet_value':str(direct[name]),
                    'per_hist_values':[[hi,str(per_hist[name][hi])] for hi in hist],
                    'endpoint_choices':[[hi,ge,gf,endpoint,n] for (hi,ge,gf,endpoint),n in sorted(selections[name].items())],
                    'row':[[j,str(v)] for j,v in sorted(row.items())]})
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('point',type=Path);p.add_argument('--matrix',type=Path);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();raw,report,cols,mass,hist,groups,moments,family=parse(a.point)
    saturated=list(mass); violations=[]; replacements=[]
    for j,c in enumerate(cols):
        if c['kind'] != 'overlap': continue
        hi=c['hist_column'];g,h=map(key,c['groups'])
        qg=moments[hi,g][0];qh=moments[hi,h][0]
        assert mass[j] <= min(qg,qh)
        saturated[j]=min(qg,qh)
        if mass[j] < max(F(),qg+qh-mass[hi]):
            violations.append({'column':j,'lower_slack':str(mass[j]-qg-qh+mass[hi])})
        if saturated[j] != mass[j]:
            replacements.append({'column':j,'old':str(mass[j]),'new':str(saturated[j])})
    out={'scope':'Boolean membership envelope only; no true-history/SPE completion',
         'input_path':str(a.point),'input_sha256':sha256(raw).hexdigest(),'point_W':report['W'],
         'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'original_columns_sha256':sha256(json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in cols],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),
         'column_kinds':dict(Counter(c['kind'] for c in cols)),
         'own_four_state_blocks':sum(map(len,groups.values())),
         'family_hist_marginals':len(family),
         'saved_overlap_frechet_lower_violations':violations,
         'saturation_changes':replacements,
         'saturation_change_count':len(replacements)}
    if a.matrix:
        mat=json.load(gzip.open(a.matrix,'rt'))
        strip = lambda c:{k:v for k,v in c.items() if k!='weight'}
        assert [strip(c) for c in mat['columns'][:4849]] == [strip(c) for c in cols]
        assert len(mat['columns']) == len(report['columns'])
        # New epigraphs keep the first 4849 coordinates unchanged. Every
        # extra coordinate is untouched by this RR envelope replacement.
        extra = [F(c['weight']) for c in report['columns'][4849:]]
        mass += extra
        saturated += extra
        js={j for j,c in enumerate(cols) if c['kind']=='overlap'}
        negative=[];mins=[];satmins=[];changed=0
        for i,(name,items) in enumerate(zip(mat['row_names'],mat['rows'])):
            row={j:F(v) for j,v in items}
            for j in js.intersection(row):
                if row[j]<0 and not name.startswith('overlap-upper:'):
                    negative.append([i,name,j,str(row[j])])
            v=dot(row,mass);w=dot(row,saturated)
            mins.append(v);satmins.append(w)
            changed += (v != w)
            if not name.startswith('overlap-upper:'): assert w >= v
        assert not negative
        assert min(mins) >= 0 and min(satmins) >= 0
        out.update(matrix_sha256=sha256(a.matrix.read_bytes()).hexdigest(),matrix_rows=len(mins),
                   unexpected_negative_overlap_coefficients=negative,original_min_slack=str(min(mins)),
                   saturated_min_slack=str(min(satmins)),saturation_changed_rows=changed)
    zz=zz_bounds(cols,mass,hist,groups,moments)
    out['known_ZZ_frechet_bounds_at_this_point']=zz
    out['ZZ_nonempty_literal_classes']=len(zz)
    out['ZZ_zero_self_classes']=sum(not x['row'] for x in zz)
    assert len(zz) == 42
    out['ZZ_negative_count']=sum(F(x['value'])<0 for x in zz)
    out['ZZ_minimum']=min(zz,key=lambda x:F(x['value']))
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('saved_overlap_frechet_lower_violations','saturation_changes','known_ZZ_frechet_bounds_at_this_point','ZZ_minimum')},ensure_ascii=False))
    print('ZZ minimum',out['ZZ_minimum']['name'],out['ZZ_minimum']['value'])

if __name__=='__main__':main()
