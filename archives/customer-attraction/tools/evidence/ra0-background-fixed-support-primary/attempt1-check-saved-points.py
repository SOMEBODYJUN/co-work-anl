"""One fixed rational check of three saved points; no LP or SPE search.

The old 437-row evaluator is reused byte-for-byte from its certified helper's
definition prefix.  Added AP rows are rebuilt below.  The helper's top-level
6144-case universal dual audit is not executed.  Run with --repo PATH only.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

args = argparse.ArgumentParser()
args.add_argument('--repo', required=True)
repo = Path(args.parse_args().repo)
here = Path(__file__).resolve().parent
common = repo / 'archives/customer-attraction/tools/evidence/five-player-indexed'
helper = common / 'tests/audits/customer_attraction_five_indexed.py'
certificate = common / 'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
assert hashlib.sha256(helper.read_bytes()).hexdigest() == 'f9a82e26fe977158fb60acb0fc8b14f6bf88b3188b024ca09491cb98138ef9e9'
assert hashlib.sha256(certificate.read_bytes()).hexdigest() == '18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1'
definitions = helper.read_text().split('from pathlib import Path')[0]
ns = {}
exec(compile(definitions, '<reused exact 437-row definitions only>', 'exec'), ns)
data = json.loads(certificate.read_text())['primal']
atoms = data['atoms']
bits = [tuple(map(int, a['bits'])) for a in atoms]
assert len(atoms) == 64
for a, b in zip(atoms, bits):
    assert len(b) == 10 and set(b) <= {0, 1}
    d = []
    for name, width in [('AB_hist', 3), ('AE_hist', 3), ('second_hist', 4)]:
        hist = a[name]
        assert len(hist) == 2**width and sum(hist) == 5
        assert all(type(n) is int and n >= 0 for n in hist)
        d.append(sum(n*c[0] for n,c in zip(hist, product((0,1), repeat=width))))
    assert len(set(d)) == 1
    for ell, h in a['menus_lh']:
        assert 0 <= h <= d[0] and 0 <= ell-h <= 5-d[0]
cols = [ns['evaluate'](b, [a['AB_hist'], a['AE_hist'], a['second_hist']], a['menus_lh'], True)
        for a,b in zip(atoms,bits)]
old_names = list(cols[0])
assert old_names == data['rows'] and len(old_names) == 437
old_rows = [[c[n] for c in cols] for n in old_names]
w = [F(any(b[:5])) for b in bits]
o = [F(any(a['AB_hist'][4:])) for a in atoms]
old_point = [F(a['mass_numerator'], data['denominator']) for a in atoms]

def build_added(version):
    """Columns are frozen atom order, never a column-dependent M_C."""
    names, rows, bounds = [], [], []
    for family, path, indices in [
        ('background_pair', (0,1,2,3,4), range(4)),
        ('second_background', (0,4,5,6,7), range(2,4)),
        ('third_background', (0,1,4,8,9), range(3,4))]:
        for i in indices:
            k = 5-i
            for C in range(10):
                MC = 5 if version == 1 else k+max(
                    (sum(b[z] for z in path[:i]) for b in bits if b[C]), default=0)
                coef = (k-1)*(MC-1)+F(k*k,2)
                bounds.append({'family':family,'i':i,'C':C,'k':k,'M':MC,'coefficient':str(coef)})
                for D in range(10):
                    r = []
                    for b in bits:
                        past = sum(b[z] for z in path[:i])
                        total = sum(b[z] for z in path)
                        u = F(1,total) if b[path[i]] else F(0)
                        s = F(b[C],past+k)
                        f = F(b[D],past+k if b[C] else past+1)
                        r.append(s+coef*(u-s)-f)
                    rows.append(r)
                    names.append(f'{family}:i{i}:C{C}:D{D}')
    assert len(rows) == 700
    families = [('AB','AB_hist',3,1,2), ('AE','AE_hist',3,1,2),
                ('S3','second_hist',4,1,3), ('S4','second_hist',4,2,2)]
    for family, key, width, chosen, k in families:
        cells = list(product((0,1), repeat=width))
        def past_load(b,c):
            if family == 'AB': return b[0]+b[1]+c[0]
            if family == 'AE': return b[0]+b[4]+c[0]
            return b[0]+sum(c[:chosen])
        def prefix(b):
            if family == 'AB': return b[0]+b[1]
            if family == 'AE': return b[0]+b[4]
            return b[0]
        def member(C,b,c): return b[C] if C<10 else c[C-10]
        for C in range(10+width):
            MC = 5 if version == 1 else k+max(
                (past_load(b,c) for a,b in zip(atoms,bits)
                 for n,c in zip(a[key],cells) if n and member(C,b,c)), default=0)
            coef = (k-1)*(MC-1)+F(k*k,2)
            bounds.append({'family':family,'C':C,'k':k,'M':MC,'coefficient':str(coef)})
            for D in range(10+width):
                r = []
                for a,b in zip(atoms,bits):
                    value = F(0)
                    for n,c in zip(a[key],cells):
                        if n == 0: continue
                        past = past_load(b,c)
                        u = F(1,prefix(b)+sum(c)) if c[chosen] else F(0)
                        cb, db = member(C,b,c), member(D,b,c)
                        s = F(cb,past+k)
                        f = F(db,past+k if cb else past+1)
                        value += n*(s+coef*(u-s)-f)
                    r.append(value)
                rows.append(r)
                names.append(f'{family}_indexed_background:C{C}:D{D}')
    assert len(names) == len(set(names)) == len(rows) == 1430
    return names, rows, bounds

v1names, v1rows, v1bounds = build_added(1)
v2names, v2rows, v2bounds = build_added(2)
assert v1names == v2names
systems = {'actual_only':(v1names[:400],v1rows[:400]),
           'full_v1':(v1names,v1rows), 'v2':(v2names,v2rows)}
raw = here/'original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample'
files = {'actual_only':'background_rows_fixed_support_actual_only.json',
         'full_v1':'background_rows_fixed_support_full_v1.json',
         'v2':'background_rows_fixed_support_v2.json'}
reports = {name:json.loads((raw/file).read_text()) for name,file in files.items()}
points = {name:list(map(F,r['exact_primal_point'])) for name,r in reports.items()}
dot = lambda a,b:sum((x*y for x,y in zip(a,b)),F(0))
def slacks_summary(names, rows, point, include_all=False):
    values = [dot(r,point) for r in rows]
    minimum = min(values)
    out = {'rows':len(values),'minimum':str(minimum),'negative_rows':sum(v<0 for v in values),
           'zero_rows':sum(v==0 for v in values),
           'minimizers':[n for n,v in zip(names,values) if v==minimum]}
    if include_all: out['slacks'] = dict(zip(names,map(str,values)))
    return out
result = {'status':'PASS','scope':'One new fixed Fraction matrix check; no LP, no SPE reconstruction, no helper top-level audit.',
          'helper_definition_prefix_sha256':hashlib.sha256(definitions.encode()).hexdigest(),
          'old_point':{},'saved_points':{},'cross_feasibility':{}}
old_slacks = slacks_summary(old_names,old_rows,old_point)
assert old_slacks['negative_rows']==0 and dot(w,old_point)==1
assert dot(o,old_point)==F(data['comparison_cover'])
result['old_point']['old_437']=old_slacks
for name,(added_names,added_rows) in systems.items():
    report = reports[name];point = points[name]
    assert len(point)==64 and all(z>=0 for z in point)
    assert report['old_row_count']==437 and report['new_row_count']==len(added_rows)
    assert report['exact_primal_verified'] is True
    assert all(report[k] is False for k in ['game_SPE_witness','universal_bound','full_domain_dual_certificate'])
    assert dot(w,point)==1 and dot(o,point)==F(report['exact_primal_value'])>2
    checked = slacks_summary(old_names+added_names,old_rows+added_rows,point,True)
    assert checked['negative_rows']==0
    old_added = slacks_summary(added_names,added_rows,old_point)
    assert old_added['minimum']==report['old_point_min_background_slack']
    assert old_added['minimizers']==report['old_point_most_violated']
    result['old_point'][name]=old_added
    result['saved_points'][name]={'raw_sha256':hashlib.sha256((raw/files[name]).read_bytes()).hexdigest(),
        'point_sha256':hashlib.sha256(json.dumps(list(map(str,point)),separators=(',',':')).encode()).hexdigest(),
        'nonzero_coordinates':sum(z>0 for z in point),'normalization':'1','objective':str(dot(o,point)),
        'gap_above_two':str(dot(o,point)-2),'float_value_original':report['float_value'],
        'float_difference_from_exact':report['float_value']-float(dot(o,point)), 'verified':checked}
    result['cross_feasibility'][name] = {}
    for system,(an,ar) in systems.items():
        result['cross_feasibility'][name][system] = slacks_summary(old_names+an,old_rows+ar,point)
assert len({tuple(p) for p in points.values()})==3
result['version_comparison']={'same_row_names':True,'added_rows':1430,
    'rows_with_changed_coefficients':sum(a!=b for a,b in zip(v1rows,v2rows)),
    'changed_matrix_entries':sum(x!=y for a,b in zip(v1rows,v2rows) for x,y in zip(a,b)),
    'v2_common_bound_records':v2bounds,
    'bounds_sharpened':sum(a['M']>b['M'] for a,b in zip(v1bounds,v2bounds)),
    'v1_constant_M':5}
print(json.dumps(result,ensure_ascii=False,indent=2))
