"""Replay the 5112-row overlap lift with the archived row builders.

Run from the repository root with python -B and NumPy/SciPy available.
The original modules are materialized in an external temporary directory.
Only row builders are called. The verifier, optimization and finder entry
points are not run. Output goes to stdout.
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import sys
import tempfile

repo = Path.cwd()
ev = Path('archives/customer-attraction/tools/evidence')
evidence = repo / ev / 'terminal-capacity-refinement-boss3'
capacity_run = json.loads((evidence / 'runs/original-execution.json').read_text())
source_map = {
    rec['path']: repo / rec['stored_path']
    for rec in json.loads((repo / ev / 'combined-branch-master-program/source-manifest.json').read_text())['frozen_sources']
}
for rec in json.loads((evidence / 'related-inputs-manifest.json').read_text())['sources']:
    source_map[rec['path']] = evidence / 'related' / Path(rec['path']).name
for rec in json.loads((evidence / 'source-manifest.json').read_text())['sources']:
    source_map[rec['path']] = evidence / 'original' / rec['id'] / Path(rec['path']).name
with tempfile.TemporaryDirectory(dir=repo.parent, prefix='boss5_5112_') as root:
    runtime = Path(root)
    for rec in capacity_run['inputs']:
        data = source_map[rec['path']].read_bytes()
        assert len(data) == rec['size'] and sha256(data).hexdigest() == rec['sha256'], rec['path']
        target = runtime / rec['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (runtime / 'work.py').write_text('# original source root locator')
    script_path = next(runtime / p for p in source_map if p.endswith('/refine_terminal_portfolio.py'))
    sys.path.insert(0, str(script_path.parent))
    sys.argv.extend(['--capacity', '--verify'])
    import refine_terminal_portfolio as refine
    cols, names, rows, obj, norm = refine.base.build()
    assert len(rows) == 5043
    for file, tag, module in (
        ('continuous_refinement_cuts.json', 'continuous-old-query', refine.cc),
        ('terminal_portfolio_refinement_cuts.json', 'prior-terminal-query-portfolio', refine.pc),
        ('terminal_capacity_refinement_cuts.json', 'terminal-query-portfolio', refine.pc),
    ):
        for cut in json.loads((script_path.parent / file).read_text())['cuts']:
            names.append(tag + ':' + str(cut))
            rows.append(module.row(cols, cut))
    data = json.loads((script_path.parent / 'terminal_capacity_refinement_exact.json').read_text())
    old = [F(c['weight']) for c in data['columns']]
    assert json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in data['columns']], sort_keys=True) == json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in cols], sort_keys=True)
    r = {}
    rr = []
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            hi = j
        if c['kind'] == 'joint-reply':
            group = tuple(tuple(x) if isinstance(x,list) else x for x in c['group'])
            key = hi, group
            if c['state'][0]: r[key] = r.get(key,F())+old[j]
        if c['kind'] == 'overlap':
            g1, g2 = [tuple(tuple(x) if isinstance(x,list) else x for x in g) for g in c['groups']]
            rr.append((j, (c['hist_column'],g1), (c['hist_column'],g2)))
    lift = list(old)
    counts = Counter()
    for j,key1,key2 in rr:
        r1, r2 = r[key1], r[key2]
        h = old[key1[0]]
        assert old[j] <= min(r1,r2) <= h
        lift[j] = min(r1,r2)
        counts['rr_raised'] += lift[j] > old[j]
        counts['rr_frechet_violations'] += old[j] < max(0, r1+r2-h)
    assert counts == {'rr_raised':161,'rr_frechet_violations':151}
    assert len(rr)==1306 and len(rows)==5112
    changed = [i for i,(o,v) in enumerate(zip(old,lift)) if v!=o]
    old_support = [j for j,v in enumerate(old) if v]
    rr_ids = [i for i,_,_ in rr]
    def family(name):
        for prefix in ('overlap-upper:', "('Z-R'", "('pair-RR'"):
            if name.startswith(prefix):
                return prefix.strip("(:'")
        return 'other'

    sign_classes = Counter()
    affected = Counter()
    negative_coefficients=[]
    negative=[]
    old_slacks=[]
    lift_slacks=[]
    for i,(name,row) in enumerate(zip(names,rows)):
        typ = family(name)
        s0 = sum(row[j]*old[j] for j in old_support if row[j])
        ds = sum(row[j]*(lift[j]-old[j]) for j in changed if row[j])
        s1 = s0+ds
        sign='negative' if any(row[j]<0 for j in rr_ids) else ('positive' if any(row[j]>0 for j in rr_ids) else 'zero')
        sign_classes[(typ,sign)]+=1
        affected[(typ, (ds>0)-(ds<0))]+=1
        if sign == 'negative':
            negative_coefficients.append(name)
            nonzero_overlap = [(j, row[j]) for j in rr_ids if row[j]]
            assert len(nonzero_overlap) == 1 and nonzero_overlap[0][1] == -1, name
        if s1 < 0:
            negative.append((i + 1, name, str(s0), str(ds), str(s1)))
        old_slacks.append(s0); lift_slacks.append(s1)
    assert len(old_slacks) == 5112 and min(old_slacks) == min(lift_slacks) == 0
    assert not negative
    assert len(negative_coefficients) == 2612
    assert all(name.startswith('overlap-upper:') for name in negative_coefficients)
    assert all(all(row[j] == 0 for j in rr_ids) for row in rows[-69:])
    assert all(sum(v * w for v, w in zip(row, old)) == slack for row, slack in zip(rows[-29:], old_slacks[-29:]))
    assert all(s0 == s1 for s0, s1 in zip(old_slacks[-29:], lift_slacks[-29:]))
    assert sum(v*w for v,w in zip(obj,old))==sum(v*w for v,w in zip(obj,lift))==F(data['W'])
    assert sum(v*w for v,w in zip(norm,old))==sum(v*w for v,w in zip(norm,lift))==1
    payload={
        'sign_classes': sorted((typ,sign,n) for (typ,sign),n in sign_classes.items()),
        'affected': sorted((typ,sgn,n) for (typ,sgn),n in affected.items()),
        'negative_overlap_coefficient_families':Counter(family(name) for name in negative_coefficients),
        'negative_lift_rows':negative,
        'counts':dict(counts),
        'old_slack_sign': Counter((s>0)-(s<0) for s in old_slacks),
        'lift_slack_sign': Counter((s>0)-(s<0) for s in lift_slacks),
        'changed_overlaps': [[j, str(old[j]), str(lift[j])] for j in changed],
        'last_29_zero_rows': [j for j, s in enumerate(lift_slacks[-29:], 1) if s == 0],
        'source_exact_sha256': sha256((script_path.parent / 'terminal_capacity_refinement_exact.json').read_bytes()).hexdigest(),
        'original_row_count': len(rows),
        'new_positive_column_count': sum(v>0 for v in lift),
        'rows_decrease':sum(s1<s0 for s0,s1 in zip(old_slacks,lift_slacks)),
        'rows_increase':sum(s1>s0 for s0,s1 in zip(old_slacks,lift_slacks)),
        'W':data['W'],
        'K':str(lift[0]),
        'lift_slack_hash':sha256(json.dumps(list(map(str,lift_slacks)), separators=(',',':')).encode()).hexdigest(),
        'old_slack_hash':sha256(json.dumps(list(map(str,old_slacks)), separators=(',',':')).encode()).hexdigest()
    }
    print(json.dumps(payload,indent=2))
