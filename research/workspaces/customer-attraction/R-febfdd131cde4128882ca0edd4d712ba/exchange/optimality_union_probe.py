"""Exact m=5 optimality exchange union rows on two frozen projected points.

Only necessary OPT maximality rows are checked; no SPE completion is claimed.
All input files remain unchanged. This program writes only beside itself.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, lcm
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/__init__.py').is_file())
LABELS = 'ABCDEUVWXY'

def C(n, k):
    return comb(n, k) if 0 <= k <= n else 0

def row(d, union_count, k, count=1):
    # Sum over C(5,k) choices of deleted optimum indices.
    return C(5-d, k-d) * (count-union_count) * (d > 0) - C(5,k) * union_count * (d == 0)

def fixed_subsets(limit):
    return [q for n in range(limit+1) for q in combinations(range(10), n)]

def read_atoms(path):
    data = json.loads(path.read_text())
    if 'primal' in data:
        p = data['primal']
        atoms = [{**a, 'mass': str(F(a['mass_numerator'],p['denominator']))} for a in p['atoms']]
        objective = p['comparison_cover']
    else:
        atoms = data['atom_masses']
        objective = data['objective']
    den = lcm(*(F(a['mass']).denominator for a in atoms))
    for a in atoms:
        a['mass_integer'] = int(F(a['mass'])*den)
        a['bb'] = tuple(map(int,a['bits']))
        a['d'] = sum(a['AB_hist'][4:])
    return atoms, den, objective

def probe(path):
    atoms, den, objective = read_atoms(path)
    slacks = {}
    for k in range(1,6):
        for q in fixed_subsets(k):
            if not q: continue
            name = f'k{k}:fixed:'+''.join(LABELS[j] for j in q)
            slacks[name] = sum(a['mass_integer'] * row(a['d'], int(any(a['bb'][j] for j in q)), k) for a in atoms)
        # Each member of an old real-reply menu is a separate legal topic.
        for f in range(3):
            for q in fixed_subsets(k-1):
                name = f'k{k}:oldL{f}+'+''.join(LABELS[j] for j in q)
                slacks[name] = sum(a['mass_integer'] * row(a['d'], 5 if any(a['bb'][j] for j in q) else a['menus_lh'][f][0], k,5) for a in atoms)
        # Same-index real branch replies have a known within-cell joint union.
        for tag,key,letters in [('AB','AB_hist','XY'),('AE','AE_hist','XY'),('S','second_hist','UVW')]:
            types = tuple(product((0,1), repeat=len(letters)+1))
            for r in range(1,min(k,len(letters))+1):
                for poses in combinations(range(1,len(letters)+1),r):
                    menu = ''.join(letters[j-1] for j in poses)
                    for q in fixed_subsets(k-r):
                        name = f'k{k}:{tag}{menu}+'+''.join(LABELS[j] for j in q)
                        def val(a):
                            ell = 5 if any(a['bb'][j] for j in q) else sum(n*int(any(ty[j] for j in poses)) for n,ty in zip(a[key],types))
                            return row(a['d'],ell,k,5)
                        slacks[name] = sum(a['mass_integer'] * val(a) for a in atoms)
    # Keep the matched optimum topic T_i or require its removal. These rows
    # retain the correlation of each real branch's replies with its T_i.
    for k in range(1,5):
        for f in range(3):
            for q in fixed_subsets(k-1):
                for anchor in ('keep','drop'):
                    name = f'anchor-{anchor}:k{k}:oldL{f}+'+''.join(LABELS[j] for j in q)
                    def val(a):
                        d=a['d'];ell,h=a['menus_lh'][f]
                        if any(a['bb'][j] for j in q):ell,n00,n10=5,0,0
                        else:n00,n10=5-d-ell+h,d-h
                        if anchor=='keep':return (d>0)*C(4-d,k-d)*n00-(d==0)*C(4,k)*ell
                        return (d>0)*(C(5-d,k-d)*n10+C(4-d,k-1-d)*n00)-(d==0)*C(4,k-1)*ell
                    slacks[name]=sum(a['mass_integer']*val(a) for a in atoms)
        for tag,key,letters in [('AB','AB_hist','XY'),('AE','AE_hist','XY'),('S','second_hist','UVW')]:
            types=tuple(product((0,1),repeat=len(letters)+1))
            for r in range(1,min(k,len(letters))+1):
                for poses in combinations(range(1,len(letters)+1),r):
                    menu=''.join(letters[j-1] for j in poses)
                    for q in fixed_subsets(k-r):
                        for anchor in ('keep','drop'):
                            name=f'anchor-{anchor}:k{k}:{tag}{menu}+'+''.join(LABELS[j] for j in q)
                            def val(a):
                                d=a['d']
                                if any(a['bb'][j] for j in q):ell,n00,n10=5,0,0
                                else:
                                    ell=sum(n*int(any(ty[j] for j in poses)) for n,ty in zip(a[key],types))
                                    n00=sum(n*(1-ty[0])*(not any(ty[j] for j in poses)) for n,ty in zip(a[key],types))
                                    n10=sum(n*ty[0]*(not any(ty[j] for j in poses)) for n,ty in zip(a[key],types))
                                if anchor=='keep':return (d>0)*C(4-d,k-d)*n00-(d==0)*C(4,k)*ell
                                return (d>0)*(C(5-d,k-d)*n10+C(4-d,k-1-d)*n00)-(d==0)*C(4,k-1)*ell
                            slacks[name]=sum(a['mass_integer']*val(a) for a in atoms)
    negatives = {n:str(F(s,den)) for n,s in slacks.items() if s<0}
    minima = {str(k): min(((s,n) for n,s in slacks.items() if n.startswith(f'k{k}:')),key=lambda p:p[0]) for k in range(1,6)}
    anchored_min=min((s,n) for n,s in slacks.items() if n.startswith('anchor-'))
    return {'source':str(path.relative_to(ROOT)), 'scope':'Necessary optimum-maximality row evaluation only, not an SPE certificate.',
            'objective':objective,'atoms':len(atoms),'rows':len(slacks),'negative_rows':negatives,
            'minimum_by_k':{k:{'row':n,'slack':str(F(s,den))} for k,(s,n) in minima.items()},
            'anchored_minimum':{'slack':str(F(anchored_min[0],den)),'row':anchored_min[1]}}

if __name__ == '__main__':
    paths = [ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json', ROOT/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible/enhanced_2396_exact_obstruction.json']
    result = [probe(path) for path in paths]
    (HERE/'optimality_union_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
