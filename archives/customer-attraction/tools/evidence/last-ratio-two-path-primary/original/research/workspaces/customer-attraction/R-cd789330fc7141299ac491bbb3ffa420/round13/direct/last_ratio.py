import itertools
import numpy as np
from scipy.optimize import linprog

def run(m):
    n=2*m-1
    bits=np.array(list(itertools.product([0,1],repeat=n)),float).T
    paths=[list(range(m)),[m-1]+list(range(m,n))]
    counts=[bits[p].sum(axis=0) for p in paths]
    pay=[np.divide(bits[p],c,out=np.zeros((m,len(c))),where=c>0) for p,c in zip(paths,counts)]
    rows=[];names=[]
    for r,path in enumerate(paths):
      for i in range((0 if r==0 else 1),m):
        prefix=bits[path[:i]].sum(axis=0)
        for j in range(n):
          rows.append(pay[r][i]-bits[j]/(prefix+m-i)); names.append((r,i,j))
    rows.append(pay[0][0]-pay[1][0]); names.append('root')
    rows=np.array(rows)
    W=(counts[0]>0).astype(float)
    opt=linprog(-pay[0][-1],A_ub=-rows,b_ub=np.zeros(len(rows)),A_eq=W[None,:],b_eq=[1],bounds=(0,None),method='highs')
    print(m,opt.success,-opt.fun,[(tuple(map(int,bits[:,j])),round(x,9)) for j,x in enumerate(opt.x) if x>1e-8])
    if opt.success: np.savez(__file__+f'.{m}.npz',bits=bits,weights=opt.x,rows=rows,names=np.array(names,dtype=object))
for m in [3,4,5]:run(m)
