"""Restricted-support proposal after adding all common-pivot last-menu rows.

This is not full-domain pricing, a universal bound, or a complete SPE.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).parent
SIB=HERE.parent/'next_credible'
ROOT=HERE.parents[4]
sys.path.insert(0,str(SIB))
from offdiagonal_probe import rows as offrows
from crossmenu_probe import rows as crossrows
from menutax_probe import rows as taxrows
from alignedtax_probe import rows as alignrows
from tripleprofit_probe import rows as triplerows
from common_pivot_rows import rows as pivotrows
ns={}
src=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text()
exec(compile(src.split('from pathlib import Path')[0],'<canonical definitions>','exec'),ns)


def allrows(a):
    v=ns['evaluate'](list(map(int,a['bits'])),[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True)
    for f in (offrows,crossrows,taxrows,alignrows,triplerows,pivotrows):v.update(f(a))
    return v


def main():
    frozen=json.loads((SIB/'reopt_added_triple.json').read_text())
    atoms=frozen['atoms'];cols=[allrows(a) for a in atoms]
    names=list(cols[0]);G=np.array([[c[n] for c in cols] for n in names],float)
    w=[int(any(map(int,a['bits'][:5]))) for a in atoms]
    o=[int(any(a['AB_hist'][4:])) for a in atoms]
    r=linprog(-np.array(o,float),A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs')
    report={'scope':'2408 universally necessary rows restricted to 65 candidate atom columns; no full-domain conclusion',
            'status':r.message,'objective':-r.fun if r.success else None,
            'point':r.x.tolist() if r.success else None,'names':names,'atoms':atoms,
            'dual_lambda':(-r.ineqlin.marginals).tolist() if r.success else None,
            'dual_beta':float(-r.eqlin.marginals[0]) if r.success else None}
    (HERE/'reopt_common_pivot.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('point','names','dual_lambda','atoms')},indent=2))
    print(json.dumps({n:v for n,v in zip(names,report['dual_lambda']) if v>1e-10},indent=2))


if __name__=='__main__':main()
