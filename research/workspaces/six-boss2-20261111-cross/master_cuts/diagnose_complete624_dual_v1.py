#!/usr/bin/env python3
"""Exact consistency of mandatory complementary equations, no optimization."""
from fractions import Fraction as F
from pathlib import Path
import json,math,time,sys
import numpy as np
from sympy import ZZ
from sympy.polys.matrices import DomainMatrix
import solve_complete624_v1 as m


def main():
    started=time.time();data,rows,obj,norm=m.load()
    point=json.loads(m.path('exact.json').read_text());W=F(point['W'])
    fl=np.load(m.path('float.npz'))
    support=[int(i) for i in np.flatnonzero(-fl['inequality_marginals']/fl['scales']>1e-10)]
    mandatory=[j for j,c in enumerate(point['columns']) if F(c['weight'])>0]
    L=[math.lcm(*(v.denominator for v in rows[i].values())) for i in support]
    D=math.lcm(*((obj[j]-W*norm[j]).denominator for j in mandatory))
    equations=[];origins=[];seen=set()
    for j in mandatory:
        eq=tuple([int(rows[i].get(j,F())*l) for i,l in zip(support,L)]+[int((obj[j]-W*norm[j])*D)])
        if not any(eq) or eq in seen:continue
        seen.add(eq);equations.append(eq);origins.append(j)
    n=len(support);entries={(i,j):ZZ(v) for i,row in enumerate(equations) for j,v in enumerate(row) if v}
    print(json.dumps({'stage':'mandatory-exact-rref','equations':len(equations),'variables':n}),flush=True)
    reduced,denom,pivots=DomainMatrix.from_dok(entries,(len(equations),n+1),ZZ).rref_den(method='FF')
    report={'scope':'Exact consistency diagnosis for the first numerical dual support; does not certify a bound.',
        'matrix_sha256':m.MATRIX_SHA,'point_sha256':m.sha(m.path('exact.json')),
        'script_sha256':m.sha(__file__),'command':[sys.executable,'-B',str(Path(__file__).resolve())],
        'positive_primal_columns':len(mandatory),'unique_mandatory_equations':len(equations),
        'dual_support_size':n,'augmented_rank':len(pivots),'mandatory_equations_consistent':n not in pivots,
        'free_dual_variables':n-len(pivots) if n not in pivots else None,
        'positive_column_indices':mandatory,'dual_support_row_indices':support,'seconds':time.time()-started}
    p=m.HERE/'complete624_mandatory_dual_diagnostic_v1.json'
    with p.open('x') as stream:stream.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('positive_column_indices','dual_support_row_indices')}),flush=True)


if __name__=='__main__':main()
