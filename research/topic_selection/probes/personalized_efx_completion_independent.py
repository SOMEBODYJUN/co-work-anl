"""Independent exact full-allocation attack, with no scout imports.

Scope: additive goods, EFX after removal of every good, ordinary integral
Pareto dominance. This audits a proof-route obstruction, not nonexistence
of EFX+PO. Fractions avoid overflow and numerical tolerance.
"""
from fractions import Fraction as F
from itertools import product
import json, platform
from pathlib import Path


def audit(values, target=None):
    n = len(values)
    assert n > 0
    m = len(values[0])
    assert all(len(row) == m for row in values)
    profiles = list(product(range(n), repeat=m))
    rows = []
    for assignment in profiles:
        bundles = [tuple(g for g in range(m) if assignment[g] == i) for i in range(n)]
        utilities = tuple(sum((F(values[i][g]) for g in bundles[i]), F(0)) for i in range(n))
        violations = []
        for i in range(n):
            for j in range(n):
                for removed in bundles[j]:
                    remaining = sum((F(values[i][g]) for g in bundles[j] if g != removed), F(0))
                    if utilities[i] < remaining:
                        violations.append((i, j, removed, str(remaining)))
        rows.append((assignment, utilities, violations))
    def dom(x, y):
        return all(a >= b for a, b in zip(x, y)) and any(a > b for a, b in zip(x, y))
    efx_po = [x for x in rows if not x[2] and not any(dom(y[1], x[1]) for y in rows)]
    out = {'agents': n, 'goods': m, 'all_allocations': len(rows),
           'efx_allocations': sum(not x[2] for x in rows), 'efx_po_allocations': len(efx_po)}
    if target is not None:
        x = next(x for x in rows if x[0] == tuple(target))
        ds = [y for y in rows if dom(y[1], x[1])]
        out.update(target_utility=[str(z) for z in x[1]], target_is_efx=not x[2],
                   dominators=[{'assignment':y[0], 'utility':[str(z) for z in y[1]],
                                'efx':not y[2], 'violations':y[2]} for y in ds],
                   completion_failure=bool(ds) and all(y[2] for y in ds))
    return out


def family(a,b,c):
    return [[1,1,1,a,a],[1,1,b,1,1],[1,1,c,c,c]]


if __name__ == '__main__':
    target = (1,1,2,0,0)
    base = audit(family(F(2),F(3),F(4)), target)
    assert base['target_utility'] == ['4','2','4']
    assert base['target_is_efx'] and base['completion_failure']
    assert len(base['dominators']) == 2 and base['efx_po_allocations'] > 0
    checks = []
    for a,b,c in product([F(7,4),F(2)], [F(2),F(3)], [F(5,2),F(4)]):
        r = audit(family(a,b,c), target)
        expected = a < 2 or b > 2
        assert r['completion_failure'] == expected, (a,b,c,r)
        checks.append({'a':str(a),'b':str(b),'c':str(c),'obstruction':r['completion_failure'],
                       'dominators':len(r['dominators']),'efx_po':r['efx_po_allocations']})
    boundaries = []
    for a,b,c in [(F(3,2),F(3),F(4)),(F(2),F(3),F(2)),(F(2),F(2),F(4))]:
        r = audit(family(a,b,c), target)
        boundaries.append({'parameters':[str(a),str(b),str(c)],'result':r})
    degenerate = [audit([[]]), audit([[0,0],[0,0]]), audit([[F(1,1000003),0]])]
    assert degenerate[0]['efx_po_allocations'] == 1
    assert degenerate[1]['efx_po_allocations'] == 4
    assert degenerate[2]['efx_po_allocations'] == 1
    out = {'identity':'SEL-PB-EFX-MONOTONE-COMPLETION-OBSTRUCTION-v1',
           'python':platform.python_version(),'arithmetic':'fractions.Fraction, full assignments',
           'scope':'independent finite verification only; analytic family proof is separate',
           'base':base,'family_checks':checks,'boundary_checks':boundaries,'degenerate':degenerate}
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    dest=Path(parser.parse_args().output)
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'base':base,'family_cases':len(checks),'boundary_cases':len(boundaries),
                      'degenerate_cases':len(degenerate),'saved':str(dest)},ensure_ascii=False))
