"""Necessary-condition relaxation, never an SPE counterexample generator.

All early actual-node guarantees, actual terminal comparisons, and symmetric
true penultimate-query/reply menu comparisons are selected jointly.  Customer
columns remember the full actual membership and (d,ell,h) of m query/reply pairs.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

def cell_rows(m,bits,d,l,h):
    p=sum(bits[:-2]);a,b=bits[-2:];q=p+a+b
    u=[F(e,q) if e else F(0) for e in bits]
    D=(p+1)*(p+2)
    rows={
      'menu:S':m*u[-2]-F(d,p+1)+F(h,D),
      'menu:Z':m*u[-1]-F(l,p+a+1),
      'menu:V':F(d*l-m*h,D),
      'menu:TT':F(m*(l-d),p+1)+F(d*d-m*h,D),
      'menu:TT_diag':F(l,p+1)-F(h,D)-F(d,p+2),
      'menu:TT_off':F((m-1)*(l-d),p+1)+F(d*d-d-(m-1)*h,D),
    }
    for k,e in enumerate(bits):
        rows[f'menu:R_to_actual:{k}']=F(l-m*e,p+1)+F(d*e-h,D)
    before=0
    for j,e in enumerate(bits):
        denom=before+m-j
        for k,t in enumerate(bits):
            rows[f'floor:{j}:actual:{k}']=u[j]-F(t,denom)
        rows[f'floor:{j}:T']=m*u[j]-F(d,denom)
        rows[f'floor:{j}:R']=m*u[j]-F(l,denom)
        before+=e
    return rows

def run(m):
    cells=[];rows=[];ws=[];os=[]
    for bits in product(range(2),repeat=m):
      for d in range(m+1):
       for l in range(m+1):
        for h in range(max(0,d+l-m),min(d,l)+1):
         rr=cell_rows(m,bits,d,l,h)
         if not rows:names=list(rr)
         cells.append((bits,d,l,h));rows.append(list(rr.values()))
         ws.append(int(any(bits)));os.append(int(d>0))
    arr=csr_matrix(np.array(rows,float).T)
    res=linprog(-np.array(os,float),A_ub=-arr,b_ub=np.zeros(arr.shape[0]),
                A_eq=[ws],b_eq=[1],bounds=(0,None),method='highs')
    report={'m':m,'success':res.success,'message':res.message,'cells':len(cells),'rows':len(names)}
    if res.success:
        report.update(ratio=-res.fun,point=[{'bits':list(cells[i][0]),'d':cells[i][1],
          'ell':cells[i][2],'h':cells[i][3],'mass':str(F(float(x)).limit_denominator(10**8))}
          for i,x in enumerate(res.x) if x>1e-8],
          multipliers={name:str(F(float(-x)).limit_denominator(10**8))
            for name,x in zip(names,res.ineqlin.marginals) if x < -1e-8})
    return report

if __name__=='__main__':
    pa=argparse.ArgumentParser();pa.add_argument('--max-m',type=int,default=7);args=pa.parse_args()
    reports=[];start=time.monotonic()
    for m in range(3,args.max_m+1):
        report=run(m);reports.append(report)
        print(json.dumps({k:v for k,v in report.items() if k not in ('point','multipliers')}),flush=True)
        Path(__file__).with_name('joint_menu_lp.json').write_text(json.dumps({'scope':'necessary-condition relaxation only','elapsed':time.monotonic()-start,'reports':reports},indent=2)+'\n')
