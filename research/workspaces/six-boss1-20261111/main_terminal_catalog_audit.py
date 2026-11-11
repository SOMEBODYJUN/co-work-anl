"""Exact linear interfaces between old B/C, old R/Z and one true B4 branch.

The B4 branch forces A6 at the actual fourth source and has true fifth/sixth
actions H1,H2. The ell coordinate is not used as a named theme here. Every
terminal query has its own true prefix; fifth-node queries use only the
legitimate one-future-player safe lower bound. Same row weights apply to all
customers. Only prescribed one-node marginals are needed for these rows.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import gzip
import hashlib
import json


def q(a, b):
    return F(a, b) if a else F()


def canonical(values):
    d = {}
    return ''.join(str(d.setdefault(x, len(d))) for x in values)


def key(row):
    a = sorted((int(j), F(v)) for j, v in row.items() if v)
    if not a:
        return ()
    scale = abs(a[0][1])
    return tuple((j, str(v/scale)) for j, v in a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('point', type=Path)
    ap.add_argument('matrix', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    raw = json.loads(args.point.read_bytes())
    matrix = json.loads(gzip.decompress(args.matrix.read_bytes()))
    cols = raw['columns'][:4849]
    weights = [F(c['weight']) for c in cols]
    hist = {}
    replies = defaultdict(dict)
    b4 = defaultdict(list)
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            h = j
            hist[h] = c
        elif c['kind'] == 'joint-reply':
            f, same, u, v = c['group']
            replies[h].setdefault((f, same, tuple(u), tuple(v)), {})[tuple(c['state'])] = j
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            assert len(c['hidden']) == 2
            b4[c['hist_column']].append((j, tuple(c['hidden'])))
    nodes = [e for e in product(range(2), range(6), range(6)) if e[0] or e[1] != e[2]]
    triple = defaultdict(list)
    nodegroups = defaultdict(list)
    for e, (f, j, k) in enumerate(nodes):
        nodegroups[f, int(j == k)].append(e)
        for i in range(6):
            triple[f, canonical((i, j, k))].append((i, e))
    rows = defaultdict(lambda: defaultdict(F))
    for h, c in hist.items():
        a = tuple(map(int, c['actual_bits']))
        p = sum(a[:3]); P = sum(a[:4]); ell = sum(a[:5])
        words = [w for w, n in zip(product(range(2), repeat=3), c['hist']) for _ in range(n)]
        groups = [(f, int(i == j), words[i], words[j]) for f, i, j in nodes]
        rden = [p+words[i][0]+words[j][1+f]+1 for f, i, j in nodes]

        def own(row, e, fn, factor=F(1)):
            base = fn(0, 0)
            row[h] += factor*base
            for st, col in replies[h][groups[e]].items():
                row[col] += factor*(fn(*st)-base)

        def branch(row, fn, factor=F(1)):
            for col, (h1, h2) in b4[h]:
                row[col] += factor*fn(h1, h2)

        for orbit, members in triple.items():
            factor = F(1, len(members))
            for i, e in members:
                t, b, cc = words[i]
                for kind, slot in [('R', 0), ('Z', 1)]:
                    row = rows['C-to-'+kind, *orbit]
                    row[h] += factor*q(cc, p+t+b+cc)
                    own(row, e, lambda r,z: -F((r,z)[slot], p+t+b+1), factor)
                    row = rows['B-safe-to-'+kind, *orbit]
                    row[h] += factor*q(b, p+t+b+cc)
                    own(row, e, lambda r,z: -F((r,z)[slot], p+t+2), factor)
                for name, value in zip(('T', 'B', 'C'), (t, b, cc)):
                    own(rows['R-to-'+name, *orbit], e,
                        lambda r,z: F(r-value, rden[e]), factor)
                    own(rows['Z-to-'+name, *orbit], e,
                        lambda r,z: F(z-value, P+r+1), factor)

        for orbit, members in nodegroups.items():
            factor = F(1, len(members))
            for e in members:
                for slot in range(2):
                    row = rows['R-to-H'+str(slot+1), *orbit]
                    own(row, e, lambda r,z: F(r, rden[e]), factor)
                    branch(row, lambda h1,h2: -F((h1,h2)[slot], rden[e]), factor)
                    row = rows['H1-safe-to-'+('R','Z')[slot], *orbit]
                    branch(row, lambda h1,h2: q(h1,p+a[5]+h1+h2), factor)
                    own(row, e, lambda r,z: -F((r,z)[slot], p+a[5]+2), factor)
                for j, aj in enumerate(a):
                    own(rows['R-to-A'+str(j+1), *orbit], e,
                        lambda r,z: F(r-aj,rden[e]), factor)
                    own(rows['Z-to-A'+str(j+1), *orbit], e,
                        lambda r,z: F(z-aj,P+r+1), factor)

        for t,b,cc in words:
            factor = F(1,6)
            for slot in range(2):
                row=rows['C-to-H'+str(slot+1),]
                row[h]+=factor*q(cc,p+t+b+cc)
                branch(row,lambda h1,h2:-F((h1,h2)[slot],p+t+b+1),factor)
                row=rows['B-safe-to-H'+str(slot+1),]
                row[h]+=factor*q(b,p+t+b+cc)
                branch(row,lambda h1,h2:-F((h1,h2)[slot],p+t+2),factor)
            for name,value in zip(('T','B','C'),(t,b,cc)):
                branch(rows['F-to-'+name,],lambda h1,h2:F(h2-value,p+a[5]+h1+1),factor)
                branch(rows['H1-safe-to-'+name,],lambda h1,h2:q(h1,p+a[5]+h1+h2)-F(value,p+a[5]+2),factor)
        for j,aj in enumerate(a):
            branch(rows['F-to-A'+str(j+1),],lambda h1,h2:F(h2-aj,p+a[5]+h1+1))
            branch(rows['H1-safe-to-A'+str(j+1),],lambda h1,h2:q(h1,p+a[5]+h1+h2)-F(aj,p+a[5]+2))
        for slot in range(2):
            row=rows['A6-to-H'+str(slot+1),]
            row[h]+=q(a[5],sum(a))
            branch(row,lambda h1,h2:-F((h1,h2)[slot],ell+1))
    existing = {key({int(j):F(v) for j,v in row}): i for i,row in enumerate(matrix['rows'])}
    report=[]
    for name,row in sorted(rows.items(),key=lambda x:str(x[0])):
        sparse={j:v for j,v in row.items() if v}
        value=sum(v*weights[j] for j,v in sparse.items())
        report.append({'name':list(name),'slack':str(value),'approx':float(value),
                       'existing_positive_scale_row':existing.get(key(sparse)),
                       'row':[[j,str(v)] for j,v in sorted(sparse.items())]})
    data={'scope':'True terminal / fifth-safe marginal interfaces at this bound point; no SPE claim.',
          'point_sha256':hashlib.sha256(args.point.read_bytes()).hexdigest(),
          'matrix_sha256':hashlib.sha256(args.matrix.read_bytes()).hexdigest(),
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'rows':report,'negative':sum(F(x['slack'])<0 for x in report),
          'zero':sum(F(x['slack'])==0 for x in report),'positive':sum(F(x['slack'])>0 for x in report),
          'absent_up_to_positive_scale':sum(x['existing_positive_scale_row'] is None for x in report)}
    args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='rows'},ensure_ascii=False))
    print(json.dumps([{k:r[k] for k in ('name','slack','approx','existing_positive_scale_row')}
                      for r in report if F(r['slack'])<0],ensure_ascii=False))


if __name__=='__main__':
    main()
