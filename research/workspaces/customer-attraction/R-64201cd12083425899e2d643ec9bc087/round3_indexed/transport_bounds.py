"""Exact per-pair necessary transport bounds for the frozen 2396-row point.

Each indexed terminal node compares both the same-index and distinct-index
members of every indexed menu.  We allow a different customer-level coupling
for each pair, so passing is a necessary test only, never a completion or SPE.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).parent
OLD = HERE.parent / 'next_credible' / 'enhanced_2396_exact_obstruction.json'
ATOMS = json.loads(OLD.read_text())['atom_masses']
Q = 5
LABELS = 'ABCDEUVWXY'


def extract(a):
    b = dict(zip(LABELS, map(int, a['bits'])))
    d = sum(n * t[0] for n, t in zip(a['AB_hist'], product((0, 1), repeat=3)))
    families = {}
    for i, path in enumerate(('ABCDE', 'AEUVW', 'ABEXY')):
        ell, h = a['menus_lh'][i]
        hist = {(0, 0): Q-d-ell+h, (0, 1): ell-h,
                (1, 0): d-h, (1, 1): h}
        families['L'+str(i)] = (sum(b[x] for x in path[:3]), hist)
    for name, key, prefix, k in [('AB','AB_hist','AB',3), ('AE','AE_hist','AE',3),
                                 ('S','second_hist','A',4)]:
        families[name] = (sum(b[x] for x in prefix), {
            t:n for t,n in zip(product((0,1), repeat=k), a[key]) if n})
    menus = {'T': {0: 0, 1: d}}
    nodes = {}
    for name, (bg,hist) in families.items():
        for j in range(1, len(next(iter(hist)))):
            menus[name+str(j)] = {t:sum(n*v[j] for v,n in hist.items() if v[0]==t)
                                  for t in (0,1)}
        slots = {t:[] for t in (0,1)}
        u = F()
        for v,n in hist.items():
            den = bg+sum(v[:-1])+1
            slots[v[0]] += [F(1,den)]*n
            u += F(n*v[-1],den)
        assert sum(map(len,slots.values())) == Q
        nodes[name] = (slots,u)
    return nodes,menus


def main():
    totals = {}
    for atom in ATOMS:
        mass = F(atom['mass'])
        nodes,menus = extract(atom)
        for fn,(slots,u) in nodes.items():
            for mn,count in menus.items():
                lo=hi=F()
                for t in (0,1):
                    weights=sorted(slots[t]); k=count[t]
                    assert 0 <= k <= len(weights)
                    lo += sum(weights[:k],F())
                    hi += sum(weights[len(weights)-k:],F()) if k else F()
                allrhs = sum(count.values())*sum((sum(v,F()) for v in slots.values()),F())
                key=fn+'->'+mn
                row=totals.setdefault(key,{'U':F(),'min_diagonal_rhs':F(),
                    'max_diagonal_rhs':F(),'all_pairs_rhs':F()})
                for k,v in [('U',u),('min_diagonal_rhs',lo),
                            ('max_diagonal_rhs',hi),('all_pairs_rhs',allrhs)]:
                    row[k] += mass*v
    failures={}
    for k,v in totals.items():
        v['diagonal_best_slack']=v['U']-v['min_diagonal_rhs']
        v['offdiagonal_best_slack']=(Q-1)*v['U']-v['all_pairs_rhs']+v['max_diagonal_rhs']
        if min(v['diagonal_best_slack'],v['offdiagonal_best_slack'])<0:
            failures[k]={z:str(x) for z,x in v.items()}
    report={'scope':'exact necessary pairwise transportation bounds only; independent couplings for different pairs; not SPE',
            'atoms':len(ATOMS),'q':Q,'pairs':len(totals),
            'failures':failures,'all':{k:{z:str(x) for z,x in v.items()} for k,v in totals.items()}}
    (HERE/'transport_bounds.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='all'},indent=2))


if __name__=='__main__': main()
