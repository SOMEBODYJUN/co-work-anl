"""Universally necessary aligned/excluded BR for common-pivot last menus.

At prefixes P^r,T_i, L_i^r is the genuine last reply. Compare L_i^s
and separately all L_j^s with j != i. These two rows cannot be replaced
by their all-pairs sum. The formulas are valid on the entire old atom domain.
"""
from fractions import Fraction as F
from itertools import product

LABELS='ABCDEUVWXY'
PATHS=('ABCDE','AEUVW','ABEXY')


def rows(a):
    b=dict(zip(LABELS,map(int,a['bits'])))
    d=sum(n*t[0] for n,t in zip(a['AB_hist'],product((0,1),repeat=3)))
    out={}
    for r,path in enumerate(PATHS):
        p=sum(b[x] for x in path[:3]);D=(p+1)*(p+2)
        ell,h=a['menus_lh'][r]
        for s in range(3):
            if r==s:continue
            ell_s,h_s=a['menus_lh'][s]
            diag=F(ell-ell_s,p+1)-F(h-h_s,D)
            allpairs=F(5*(ell-ell_s),p+1)+F(d*ell_s-5*h,D)
            out[f'common-pivot:{r}:diag-menu:{s}']=diag
            out[f'common-pivot:{r}:off-menu:{s}']=allpairs-diag
    return out
