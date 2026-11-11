"""Symbolic fixed-16-hist necessary lift for genuine fifth-source replies D_i.

Every row is homogeneous in the entire old point and the new nonnegative
variables.  Only discover.py specializes old coordinates to the bound point.
No D label, old R/Z event, or history is identified by equality of marginals.
The two min families are virtual upper envelopes, not common intersections.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
ROOT = WORK.parents[2]
POINT = WORK / 'union_augmented_lp/augmented_lp_exact.json'
MATRIX = WORK / 'union_augmented_lp/exact_matrix.json.gz'
EXPECTED_POINT = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
EXPECTED_MATRIX = '99253e05bfe4c5705619777a5989ec9fab5c38dc7e56f934bbe8d9c071040ded'
ORIGINAL = 4849
OLD = 15593
WORDS = list(product(range(2), repeat=3))
NODES = [(f,j,k) for f,j,k in product(range(2),range(6),range(6))
         if f or j != k]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def canonical(seq):
    seen = {}
    return ''.join(str(seen.setdefault(v, len(seen))) for v in seq)


def share(a,b):
    return F(a,b) if a else F()


def sparse(d):
    return [[j,str(v)] for j,v in sorted(d.items()) if v]


def main():
    assert sha(POINT) == EXPECTED_POINT
    assert sha(MATRIX) == EXPECTED_MATRIX
    point = json.loads(POINT.read_bytes())
    matrix = json.loads(gzip.decompress(MATRIX.read_bytes()))
    cols = matrix['columns']
    assert len(cols) == OLD and len(point['columns']) == OLD
    assert all(c == {k:v for k,v in p.items() if k != 'weight'}
               for c,p in zip(cols, point['columns']))
    hist, replies, b4 = {}, defaultdict(dict), defaultdict(list)
    for j,c in enumerate(cols[:ORIGINAL]):
        if c['kind'] == 'hist':
            h = j
            hist[h] = c
        elif c['kind'] == 'joint-reply':
            f,s,u,v = c['group']
            key = (f,s,tuple(u),tuple(v))
            replies[h].setdefault(key,{})[tuple(c['state'])] = j
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            assert len(c['hidden']) == 2 and c['ell'] in (0,6)
            b4[c['hist_column']].append((j,tuple(c['hidden']),c['ell']))
    assert len(hist) == 16 and len(NODES) == 66
    for h in hist:
        assert len(b4[h]) == 8
        assert all(set(st) == {(0,1),(1,0),(1,1)} for st in replies[h].values())

    newcols, xcol, ycol, zcol = [], {}, {}, {}
    def new(desc):
        idx = OLD + len(newcols)
        newcols.append(desc)
        return idx
    for h,c in hist.items():
        for w,n in zip(WORDS,c['hist']):
            if n:
                xcol[h,w] = new({'kind':'D-membership-marginal', 'hist_column':h,
                                  'word':list(w), 'multiplicity':n})

    rows = defaultdict(lambda: defaultdict(F))
    def row(name):
        return rows[tuple(name)]
    def add(r,j,v):
        r[j] += v
    def own(r,h,g,which,factor):
        for state,j in replies[h][g].items():
            member = state[which] if which < 2 else state[0]*state[1]
            if member:
                r[j] += factor
    def branch(r,h,fn,factor=F(1)):
        for j,(h1,h2),ell in b4[h]:
            r[j] += factor*fn(h1,h2,ell)
    def rz_min(h,g,w):
        key = (h,g,w)
        if key not in ycol:
            y = new({'kind':'virtual-R-D-min-upper', 'hist_column':h,
                     'group':[g[0],g[1],list(g[2]),list(g[3])],
                     'word':list(w), 'semantics':'upper envelope, not a physical intersection'})
            ycol[key] = y
            r = row(('R-D-min-at-most-R',y)); own(r,h,g,0,F(1)); add(r,y,-1)
            r = row(('R-D-min-at-most-D',y)); add(r,xcol[h,w],1); add(r,y,-1)
        return ycol[key]
    def f_min(h,w):
        key = (h,w)
        if key not in zcol:
            z = new({'kind':'virtual-H1-D-min-upper', 'hist_column':h,
                     'word':list(w), 'semantics':'upper envelope, not a physical intersection'})
            zcol[key] = z
            r = row(('H1-D-min-at-most-H1',z))
            branch(r,h,lambda h1,h2,ell:F(h1)); add(r,z,-1)
            r = row(('H1-D-min-at-most-D',z)); add(r,xcol[h,w],1); add(r,z,-1)
        return zcol[key]

    pair = defaultdict(list)
    triple = defaultdict(list)
    for i,j in product(range(6),repeat=2):
        pair[int(i==j)].append((i,j))
    for i in range(6):
        for e,(f,j,k) in enumerate(NODES):
            triple[f,canonical((i,j,k))].append((i,e))
    assert sorted(map(len,triple.values())) == [6,30,30,30,30,30,120,120]

    for h,c in hist.items():
        a = tuple(map(int,c['actual_bits']))
        p3, P, ell, total = sum(a[:3]),sum(a[:4]),sum(a[:5]),sum(a)
        words = [w for w,n in zip(WORDS,c['hist']) for _ in range(n)]
        assert len(words) == 6
        groups = [(f,int(j==k),words[j],words[k]) for f,j,k in NODES]
        rden = [p3+words[j][0]+words[k][1+f]+1 for f,j,k in NODES]
        s = p3+a[5]+1
        for w in set(words):
            r = row(('D-at-most-hist',h,*w)); add(r,h,1); add(r,xcol[h,w],-1)

        # A fixed global average of the six genuine fifth-source deviations.
        add(row(('D-source',)),h,share(a[4],total))
        # Actual source shares are used once in each independent valid IC row.
        for k in range(1,7):
            add(row(('A-to-D-safe' if k<6 else 'A6-to-D',k)),h,share(a[k-1],total))
        branch(row(('F-to-D-upper',)),h,lambda h1,h2,ell:share(h2,p3+a[5]+h1+h2))
        branch(row(('H1-safe-to-D',)),h,lambda h1,h2,ell:share(h1,p3+a[5]+h1+h2))

        for i,w in enumerate(words):
            t,b,cc = w
            x = xcol[h,w]
            fac = F(1,6)
            den = P+t+1
            add(row(('D-source',)),h,-fac*F(t,P+1))
            add(row(('D-source',)),x,fac*F(t,(P+1)*(P+2)))
            add(row(('capacity-D',)),x,-fac)
            for k in range(1,7):
                kd = sum(a[:k-1]) + 7-k
                add(row(('A-to-D-safe' if k<6 else 'A6-to-D',k)),x,-fac*F(1,kd))
            for k,ak in enumerate(a,1):
                r = row(('D-to-A',k)); add(r,x,fac*F(1,den)); add(r,h,-fac*F(ak,den))
            for slot in range(2):
                r = row(('D-to-H',slot+1)); add(r,x,fac*F(1,den))
                branch(r,h,lambda h1,h2,ell: -F((h1,h2)[slot],den),fac)
            y = f_min(h,w)
            r = row(('F-to-D-upper',)); add(r,x,-fac*F(1,s)); add(r,y,fac*F(1,s*(s+1)))
            add(row(('H1-safe-to-D',)),x,-fac*F(1,p3+a[5]+2))

        for same,members in pair.items():
            fac = F(1,len(members))
            for i,j in members:
                wi,wj = words[i],words[j]
                xi,xj = xcol[h,wi],xcol[h,wj]
                den = P+wi[0]+1
                for slot,kind in enumerate(('T','B','C')):
                    r = row(('D-to-'+kind,same)); add(r,xi,fac*F(1,den)); add(r,h,-fac*F(wj[slot],den))
                r = row(('D-to-D',same)); add(r,xi,fac*F(1,den)); add(r,xj,-fac*F(1,den))
                t,b,cc = wj
                r = row(('C-to-D',same)); add(r,h,fac*share(cc,p3+t+b+cc)); add(r,xi,-fac*F(1,p3+t+b+1))
                r = row(('B-safe-to-D',same)); add(r,h,fac*share(b,p3+t+b+cc)); add(r,xi,-fac*F(1,p3+t+2))

        for orbit,members in triple.items():
            fac = F(1,len(members))
            for i,e in members:
                w,g = words[i],groups[e]
                x = xcol[h,w]
                den = P+w[0]+1
                for slot,kind in enumerate(('R','Z')):
                    r = row(('D-to-'+kind,*orbit)); add(r,x,fac*F(1,den)); own(r,h,g,slot,-fac*F(1,den))
                r = row(('R-to-D',*orbit)); own(r,h,g,0,fac*F(1,rden[e])); add(r,x,-fac*F(1,rden[e]))
                y = rz_min(h,g,w)
                r = row(('Z-to-D-upper',*orbit))
                own(r,h,g,1,fac*F(1,P+1)); add(r,x,-fac*F(1,P+1))
                own(r,h,g,2,-fac*F(1,(P+1)*(P+2)))
                add(r,y,fac*F(1,(P+1)*(P+2)))
    add(row(('capacity-D',)),0,1)

    ordered = sorted(rows.items(),key=lambda nr:str(nr[0]))
    payload = {
        'schema':1, 'scope':'Homogeneous necessary D single-marginal / per-query min lift on all 16 given hist; not a common D measure or SPE.',
        'point_sha256':sha(POINT), 'matrix_sha256':sha(MATRIX),
        'original_columns':ORIGINAL,'fixed_old_columns':OLD,
        'old_descriptors':cols, 'new_columns':newcols,
        'rows':[{'name':list(name),'row':sparse(r)} for name,r in ordered],
        'nonnegative_new_columns':True,
        'triple_orbits':[{'orbit':list(o),'size':len(ms),'members':[[i,*NODES[e]] for i,e in ms]}
                         for o,ms in sorted(triple.items())],
        'pair_orbits':[{'same':same,'size':len(ms),'members':ms} for same,ms in sorted(pair.items())],
        'hist_columns':list(hist),
        'zero_mass_hist_columns':[h for h in hist if F(point['columns'][h]['weight'])==0],
        'family_counts':dict(Counter(name[0] for name,r in ordered)),
        'new_column_counts':dict(Counter(c['kind'] for c in newcols)),
        'old_auxiliary_coefficients_all_zero':all(j<ORIGINAL or j>=OLD for name,r in ordered for j,v in r.items() if v),
        'row_constants':0,
    }
    assert payload['old_auxiliary_coefficients_all_zero']
    dump(HERE/'symbolic_lift.json',payload)

    audit_path = WORK/'main_19662_terminal_catalog.json'
    audit = json.loads(audit_path.read_bytes())
    weights = [F(c['weight']) for c in point['columns']]
    assert audit['point_sha256'] == sha(POINT) and audit['matrix_sha256'] == sha(MATRIX)
    values = [sum(F(v)*weights[j] for j,v in r['row']) for r in audit['rows']]
    assert len(values)==152 and all(v>=0 for v in values)
    assert all(v==F(r['slack']) for v,r in zip(values,audit['rows']))
    sources = [POINT,MATRIX,WORK/'main_fifth_reply_contract.md',WORK/'union_augmented_lp.md',
               WORK/'main_terminal_catalog_audit.py',audit_path,WORK/'common_network_19662.md',
               ROOT/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
               ROOT/'archives/customer-attraction/subarchives/six-providers/问题--问题.md',
               ROOT/'research/GITHUB_RESOURCES.md']
    dump(HERE/'inputs.json',{
        'sources':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sources],
        'all_old_point_descriptors_match_matrix':True,
        'audited_existing_152_rows':{'negative':sum(v<0 for v in values),'zero':sum(v==0 for v in values),'positive':sum(v>0 for v in values)},
        'audited_existing_row_values':[{'name':r['name'],'slack':str(v)} for r,v in zip(audit['rows'],values)],
        'original_point_not_modified':True,'old_auxiliary_variables_fixed':True,
    })
    print(json.dumps({k:payload[k] for k in ('scope','family_counts','new_column_counts','hist_columns','zero_mass_hist_columns')},ensure_ascii=False))
    print(json.dumps({'symbolic_rows':len(ordered),'new_columns':len(newcols),'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json')}))


if __name__=='__main__':
    main()
