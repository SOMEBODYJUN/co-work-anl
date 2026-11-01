"""Exact separator for the symmetric 3-player-sharp price-lift template.

Does not construct a SPE. This is a Farkas obstruction for this named template.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
from math import lcm
import json
import numpy as np
from scipy.optimize import linprog
from three_price_template import value_row


def main():
    n = 3
    rows, targets, labels, welfare = [], [], [], []
    for a, b, c, q, r in product(range(2), repeat=5):
        for d in [0, 1, n]:
            for ell in [0, n]:
                labels.append((a,b,c,q,r,d,ell))
                row, target = value_row(n, F(0), a,b,c,q,r,d,ell,True)
                rows.append(list(map(F,row))); targets.append(F(target))
                welfare.append(F(int(a+b+c > 0)))
    mat = np.array(rows, float)
    res = linprog(np.array(targets, float), A_ub=-mat.T,
                  b_ub=np.zeros(11), A_eq=[np.array(welfare,float)], b_eq=[1],
                  bounds=(0,None), method='highs')
    assert res.success and res.fun < -1e-8, res
    x = [F(float(z)).limit_denominator(10**6) for z in res.x]
    values = [sum(xi*row[j] for xi,row in zip(x,rows)) for j in range(11)]
    targ = sum(xi*t for xi,t in zip(x,targets))
    assert min(values) >= 0 and targ < 0
    denominator = lcm(*(xi.denominator for xi in x))
    out = {'status':'exact template obstruction, not SPE', 'n':n,
           'variables':['K_Q*3','K_R*3','sum P','sum Z','sum S + sum V/n',
                        'F','sum J','sum K_T','sum K_L','K_B','K_C'],
           'integer_types':[{'a':lab[0],'b':lab[1],'c':lab[2], 'q':lab[3],
                             'r':lab[4],'d':lab[5],'ell':lab[6],
                             'multiplicity':int(xi*denominator)}
                            for xi,lab in zip(x,labels) if xi],
           'normalization_denominator':denominator,
           'slack_values_integer_scale':[str(v*denominator) for v in values],
           'target_integer_scale':str(targ*denominator)}
    print(json.dumps(out,indent=2))
    Path(__file__).with_name('three_price_template_obstruction.json').write_text(
        json.dumps(out,indent=2)+'\n')


if __name__ == '__main__':
    main()
