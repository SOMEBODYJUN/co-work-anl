"""Lift-independent cross-family common-catalog necessary conditions.

This is a fixed-support relaxation probe, never a complete SPE search.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from pathlib import Path
import importlib.util
import json
import numpy as np
from scipy.optimize import linprog

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').exists())
SOURCE = ROOT / 'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
NS = {}
exec((ROOT / 'tests/audits/customer_attraction_five_indexed.py').read_text().split(
    '\nfrom pathlib import Path\nfrom collections')[0], NS)
OLD = ROOT / 'research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/credible_counterexample/frozen_support_closure.py'
SPEC = importlib.util.spec_from_file_location('old_fixed_support', OLD)
OLDMODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OLDMODULE)


def cross_rows(atom):
    bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
    families = {}
    menus = {}
    for tag, field, arity, fixed in [('AB', 'AB_hist', 3, 'AB'),
                                    ('AE', 'AE_hist', 3, 'AE'),
                                    ('S', 'second_hist', 4, 'A')]:
        types = tuple(product((0, 1), repeat=arity))
        hist = atom[field]
        p = sum(bits[x] for x in fixed)
        families[tag] = p, types, hist
        for position in range(arity):
            menus[f'{tag}{position}'] = sum(n * ty[position]
                                           for n, ty in zip(hist, types))
    for k, tag in enumerate(('Lact', 'Lsec', 'Lthird')):
        menus[tag] = atom['menus_lh'][k][0]
    out = {}
    for tag, (p, types, hist) in families.items():
        arity = len(types[0])
        def sm(fn):
            return sum((n * fn(ty) for n, ty in zip(hist, types)), F(0))
        # Every indexed node compares every menu in the common catalog.
        for pos in range(1, arity):
            z = sm(lambda ty: F(ty[pos], p + sum(ty))
                   if ty[pos] else F(0))
            d = sm(lambda ty: F(1, p + sum(ty[:pos]) + arity - pos))
            for menu, count in menus.items():
                out[f'cross:{tag}:{pos}:K:{menu}'] = 5*z - count*d
        # The exact last-two residual-profit inequality for every pair of menus,
        # averaged independently over both comparison indices and source index.
        pos = arity - 2
        h = sm(lambda ty: (F(ty[-2] + ty[-1], p + sum(ty))
                          if ty[-2] + ty[-1] else F(0))
               + F(ty[-2], (p + sum(ty[:pos]) + 1)
                   * (p + sum(ty[:pos]) + 2)))
        d1 = sm(lambda ty: F(1, p + sum(ty[:pos]) + 1))
        d2 = sm(lambda ty: F(1, p + sum(ty[:pos]) + 2))
        for mx, my in combinations_with_replacement(menus, 2):
            qx, qy = menus[mx], menus[my]
            out[f'cross:{tag}:r2:{mx}:{my}'] = (
                25*h - (qx*(5-qy) + qy*(5-qx))*d1 - 2*qx*qy*d2)
    # The three fixed last-two nodes can also query any cross-family menu pair.
    for tag, path in [('actual', 'ABCDE'), ('second', 'AEUVW'), ('third', 'ABEXY')]:
        p = sum(bits[x] for x in path[:3])
        load = sum(bits[x] for x in path)
        h = (F(bits[path[3]]+bits[path[4]], load)
             if bits[path[3]]+bits[path[4]] else F(0))
        h += F(bits[path[3]], (p+1)*(p+2))
        for mx, my in combinations_with_replacement(menus, 2):
            qx, qy = menus[mx], menus[my]
            out[f'cross:{tag}:r2:{mx}:{my}'] = (
                25*h - F(qx*(5-qy)+qy*(5-qx), p+1) - F(2*qx*qy, p+2))
    return out


def conditional_rows(atom):
    """Diagonal/off-diagonal closure using the T_i shared by all families.

    Cross-family joint membership is unknown. The rearrangement extrema below
    give necessary, lift-independent inequalities, rather than pretending that
    every pair of independently feasible extrema can be achieved together.
    """
    bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
    families = {}
    menus = {}
    for tag, field, arity, fixed in [('AB', 'AB_hist', 3, 'AB'),
                                    ('AE', 'AE_hist', 3, 'AE'),
                                    ('S', 'second_hist', 4, 'A')]:
        types = tuple(product((0, 1), repeat=arity))
        data = tuple(ty for ty,n in zip(types, atom[field]) for _ in range(n))
        families[tag] = sum(bits[x] for x in fixed), data
    d = sum(ty[0] for ty in families['AB'][1])
    for k, (tag, fixed) in enumerate([('Lact', 'ABC'), ('Lsec', 'AEU'), ('Lthird', 'ABE')]):
        ell, h = atom['menus_lh'][k]
        data = ((0,0),)*(5-d-ell+h) + ((0,1),)*(ell-h) + ((1,0),)*(d-h) + ((1,1),)*h
        assert len(data) == 5
        families[tag] = sum(bits[x] for x in fixed), data
    for tag, (p, data) in families.items():
        for pos in range(1, len(data[0])):
            menus[f'{tag}{pos}'] = (tag, pos,
                tuple(sum(ty[pos] for ty in data if ty[0] == t) for t in (0,1)))
    out = {}
    for tag, (p, data) in families.items():
        arity = len(data[0])
        for pos in range(1, arity):
            z = sum((F(ty[pos], p+sum(ty)) if ty[pos] else F(0) for ty in data), F(0))
            weights = tuple(F(1, p+sum(ty[:pos])+arity-pos) for ty in data)
            for menu, (mtag,mpos,conditional_counts) in menus.items():
                if mtag == tag:
                    lo = hi = sum((weight*ty[mpos] for weight,ty in zip(weights,data)), F(0))
                else:
                    lo = hi = F(0)
                    for t, count in enumerate(conditional_counts):
                        vals = sorted(weight for weight,ty in zip(weights,data) if ty[0] == t)
                        lo += sum(vals[:count], F(0))
                        hi += sum(vals[len(vals)-count:], F(0)) if count else F(0)
                total = sum(conditional_counts)*sum(weights, F(0))
                out[f'conditional:{tag}:{pos}:diag:{menu}'] = z-lo
                out[f'conditional:{tag}:{pos}:offdiag:{menu}'] = 4*z-total+hi
    return out


def main():
    atoms = json.loads(SOURCE.read_text())['primal']['atoms']
    columns = []
    for atom in atoms:
        bits = tuple(map(int, atom['bits']))
        hists = [atom[k] for k in ('AB_hist', 'AE_hist', 'second_hist')]
        row = NS['evaluate'](bits, hists, atom['menus_lh'], True)
        row.update(OLDMODULE.module.rows(atom))
        row.update(cross_rows(atom))
        row.update(conditional_rows(atom))
        columns.append(row)
    names = tuple(columns[0])
    assert all(tuple(c) == names for c in columns)
    G = np.array([[c[name] for c in columns] for name in names], dtype=object)
    w = np.array([int(any(map(int, a['bits'][:5]))) for a in atoms], dtype=object)
    objective = np.array([int(sum(n*t[0] for n,t in zip(a['AB_hist'], NS['types'])) > 0)
                          for a in atoms], dtype=object)
    GF = np.array(G, dtype=float)
    result = linprog(-np.array(objective, dtype=float), A_ub=-GF,
                     b_ub=np.zeros(len(names)), A_eq=[np.array(w, dtype=float)],
                     b_eq=[1], bounds=(0, None), method='highs')
    report = {'scope': 'fixed original 64-atom support only; old 447 rows plus '
                      'cross-family indexed-menu K and all-menu-pair last-two rows '
                      'and conditional diagonal/off-diagonal K rows',
              'is_SPE_counterexample': False, 'row_count': len(names),
              'floating_success': result.success}
    if result.success:
        report['floating_optimum'] = float(-result.fun)
        beta = F(float(-result.eqlin.marginals[0])).limit_denominator(10**9)
        dual = [F(float(-x)).limit_denominator(10**9) for x in result.ineqlin.marginals]
        residual = [beta*w[j] - sum(mu*G[i,j] for i,mu in enumerate(dual)) - objective[j]
                    for j in range(len(atoms))]
        if all(mu >= 0 for mu in dual) and all(x >= 0 for x in residual):
            report['exact_upper_bound'] = str(beta)
            report['exact_dual'] = {n: str(mu) for n,mu in zip(names,dual) if mu}
            report['minimum_dual_residual'] = str(min(residual))
        active = abs(GF @ result.x) < 1e-7
        A = np.concatenate([w[None,:], G[active]])
        primal = OLDMODULE.recover(A, [1] + [0]*int(sum(active)), result.x)
        if primal is not None and min(primal) >= 0:
            assert sum(w[j]*primal[j] for j in range(len(atoms))) == 1
            slacks = [sum(G[i,j]*primal[j] for j in range(len(atoms)))
                      for i in range(len(names))]
            assert min(slacks) >= 0
            value = sum(objective[j]*primal[j] for j in range(len(atoms)))
            report['exact_primal_value'] = str(value)
            report['exact_reweighting'] = [str(x) for x in primal]
            report['minimum_primal_slack'] = str(min(slacks))
            report['exact_gap_above_two'] = str(value - 2)
            report['positive_atom_count'] = sum(x > 0 for x in primal)
            report['exact_optimality_verified'] = str(value) == report.get('exact_upper_bound')
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('exact_reweighting','exact_dual')}, indent=2))


if __name__ == '__main__':
    main()
