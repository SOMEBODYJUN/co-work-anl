"""Review-only literal semantic checks against the supplied global evaluator.

This is not a standalone proof checker: it imports the supplied verifier for
comparison, and reuses its rounded projection tables. It independently forms
active raw rows by their literal indexed game semantics.
"""
from pathlib import Path
import importlib.util
import itertools
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / 'customer_attraction/proofs/half5_exact_v1'
spec = importlib.util.spec_from_file_location('reviewed_verifier', PACKAGE/'verify_certificate.py')
supplied = importlib.util.module_from_spec(spec)
spec.loader.exec_module(supplied)
bg, pc, deep, _ = supplied.source_tables()
domain = supplied.LiteralDomain(bg, pc, deep)
weights = json.loads((PACKAGE/'certificate.json').read_text())['integer_multipliers']
families = {f: [] for f in supplied.FAMILIES}
fixed = []
for name in weights:
    first = name.split(':')[0]
    if first in families:
        families[first].append(name)
    elif ':sum-S' in name:
        families['Sbranch'].append(name)
    else:
        fixed.append(name)


def scaled_share(b, path, seat):
    numerator = b[path[seat]]
    return 120*numerator//sum(b[x] for x in path) if numerator else 0


def fixed_literal(name, b, d, menus):
    z = name.split(':')
    if z[0] == 'MAX':
        return -120*b[supplied.LABELS[int(z[2])]], 1
    if name == 'MAXROOT-NEW':
        return 46313177*scaled_share(b, 'ABCDE', 0)-120*10**6*(d>0), -7412362
    if z[0] == 'DEEP':
        a, kap, gamma, scale, zeta = deep[int(z[1])]
        t, q = b[supplied.LABELS[int(z[2])]], b[supplied.LABELS[int(z[3])]]
        return a*scaled_share(b, 'ABCDE', 0)+120*(gamma*t-scale*q+(scale+zeta)*t*q), kap
    if z[0] in ('BG', 'PC'):
        idx = int(z[1]); t = b[supplied.LABELS[int(z[2])]]; q = b[supplied.LABELS[int(z[3])]]
        if z[0] == 'BG':
            kap, table, seat = bg[idx]
            background = b['A'] if seat == 1 else 2*b['A']+b['B']
            return 10**6*scaled_share(b, 'ABCDE', seat)-120*table[4*background+2*t+q], kap
        kap, table, coefs = pc[idx]
        pattern = 8*b['A']+4*b['B']+2*b['C']+b['D']
        return sum(coefs[i]*scaled_share(b, 'ABCDE', i) for i in range(5))-120*table[4*pattern+2*t+q], kap
    if z[0] == 'F':
        seat = 1 if z[1] == 'second' else 2
        return scaled_share(b, 'ABCDE', seat)-scaled_share(b, supplied.PATHS[z[1]], seat), 0
    path = supplied.PATHS[z[0]]
    p = sum(b[x] for x in path[:3]); delta = (p+1)*(p+2)
    if z[1] == 'reply':
        ell, overlap = menus[list(supplied.PATHS).index(z[0])]
        if z[2] == 'S':
            return 5*scaled_share(b,path,3)-120*d//(p+1)+120*overlap//delta, 0
        if z[2] == 'V':
            return 120*(d*ell-5*overlap)//delta, 0
        if z[2] == 'Z':
            return 5*scaled_share(b,path,4)-120*ell//(p+b[path[3]]+1), 0
        other = menus[list(supplied.PATHS).index(z[2].removeprefix('cross-L-'))][0]
        return 600*(ell-other)//(p+1)+120*(d*other-5*overlap)//delta, 0
    p = sum(b[x] for x in path[:4]); u = scaled_share(b,path,4)
    if z[2] == 'K':
        return u-120*b[z[3]]//(p+1), 0
    if z[2] == 'O':
        return 5*u+120*p//(p+1)-120*(d>0), 0
    ell = menus[list(supplied.PATHS).index(z[2].removeprefix('sum-L-'))][0]
    return 5*u-120*ell//(p+1), 0


def family_literal(name, tag, b):
    k = 4 if tag == 'Sbranch' else 3
    p = b['A']+(b['B'] if tag == 'AB' else b['E'] if tag == 'AE' else 0)
    e = domain.expanded[k]
    loads = p+e.sum(axis=2)
    shares = np.where(loads[:,:,None]>0,120*e//np.maximum(loads[:,:,None],1),0)
    z = name.split(':')
    if z[0] == tag:
        z = z[1:]
    kap = 0
    if z[0] in ('BG','PC'):
        idx, i, j = int(z[1]), int(z[3]), int(z[4])
        assert z[2] == 'eq'
        if z[0] == 'BG':
            kap, table, seat = bg[idx]
            background = b['A'] if seat == 1 else 2*b['A']+b['B']
            u = 10**6*scaled_share(b,'ABCDE',seat)
        else:
            kap, table, coefs = pc[idx]
            background = 8*b['A']+4*b['B']+2*b['C']+b['D']
            u = sum(coefs[i]*scaled_share(b,'ABCDE',i) for i in range(5))
        indices = 4*background+2*e[:,:,i]+e[:,:,j]
        return 5*u-120*np.array(table,dtype=np.int64)[indices].sum(axis=1), 5*kap
    if z[0] in ('F2','F3'):
        path = 'AEUVW' if tag == 'AE' else 'ABCDE'
        seat = 1 if k == 4 else 2
        return 5*scaled_share(b,path,seat)-shares[:,:,0].sum(axis=1), 0
    if z[0] in supplied.PATHS:
        path = supplied.PATHS[z[0]]
        labels = 'TUVW' if k == 4 else 'TXY'
        pos = labels.index(z[2].removeprefix('sum-').removeprefix('S'))
        return 5*scaled_share(b,path,4)-120*e[:,:,pos].sum(axis=1)//(1+sum(b[x] for x in path[:4])), 0
    if z[0] == 'pair':
        assert z[2] == 'query_equal'
        i,j = map(int,z[1])
        prefix = p+e[:,:,:k-2].sum(axis=2)
        a = 120//(prefix+1)
        g = 120//((prefix+1)*(prefix+2))
        h = shares[:,:,-2]+shares[:,:,-1]+e[:,:,-2]*g
        querysum = (e[:,:,i]+e[:,:,j]).sum(axis=1)
        intersect = e[:,:,i]*e[:,:,j]
        return (4*h-(querysum[:,None]-e[:,:,i]-e[:,:,j])*a+(intersect.sum(axis=1)[:,None]-intersect)*g).sum(axis=1), 0
    seat = int(z[0]); pos = seat-(6-k)
    denom = p+e[:,:,:pos].sum(axis=2)+k-pos
    reciprocal = 120//denom
    if z[1] == 'K':
        return shares[:,:,pos].sum(axis=1)-b[z[2]]*reciprocal.sum(axis=1), 0
    query = int(z[2]) if z[1] == 'offdiag' else ('TUVW' if k == 4 else 'TXY').index(z[1].removeprefix('sum-'))
    if z[1] == 'offdiag':
        return (4*shares[:,:,pos]-(e[:,:,query].sum(axis=1)[:,None]-e[:,:,query])*reciprocal).sum(axis=1), 0
    return 5*shares[:,:,pos].sum(axis=1)-e[:,:,query].sum(axis=1)*reciprocal.sum(axis=1), 0


family_entries = fixed_cases = 0
for bits in itertools.product((0,1),repeat=10):
    b = dict(zip(supplied.LABELS,bits))
    for tag,names in families.items():
        for name in names:
            key,const,kap = domain.family_parts(tag,b,{name:1})
            k,p,terms = key
            actual = np.full(len(domain.hist[k]),const,dtype=np.int64)
            for feature,coef in terms:
                actual += coef*domain.features[k,p][feature]
            expected,expectedkap = family_literal(name,tag,b)
            assert kap == expectedkap, name
            assert np.array_equal(actual,expected), (name,bits,np.flatnonzero(actual!=expected)[:5])
            family_entries += len(actual)
    for d in range(6):
        # The supplied menu formulas have visibly no mixed-menu products.
        # Check all individual corners and one joint corner against direct rows.
        corners = [(0,0),(d,d),(5-d,0),(5,d)]
        menuslist = [[(0,0)]*3,[(5,d)]*3]
        for menu in range(3):
            for corner in corners:
                menus = [(0,0)]*3; menus[menu] = corner; menuslist.append(menus)
        for name in fixed:
            these = menuslist if (':reply:' in name or ':sum-L-' in name) else menuslist[:1]
            for menus in these:
                value,kap = domain.fixed_value(name,b,d,menus)
                expected,expectedkap = fixed_literal(name,b,d,menus)
                assert (supplied.sc(value),kap) == (expected,expectedkap), (name,bits,d,menus,value,expected)
                fixed_cases += 1
report={'status':'passed','claim':'Literal semantic row cross-check, not an independent standalone certificate proof','family_histogram_entries_checked':family_entries,'fixed_row_cases_checked':fixed_cases,'active_rows':len(weights),'fixed_masks':1024,'domain_histogram_counts':{str(k):len(domain.hist[k]) for k in (3,4)}}
print(json.dumps(report,indent=2))
