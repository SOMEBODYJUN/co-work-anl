"""Necessary-row cone: actual path and every earlier player copying the actual last theme.

All branch suffixes are independent hidden memberships. LP searches a proof,
not a game, and a gap cannot constitute an SPE counterexample.
"""
import itertools, json, sys
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, save_npz

def frac(a,b):
    return a/b if a else 0.0

def make(m):
    states=list(itertools.product(range(2),repeat=m+1)) # final bit O
    actual=[]
    for i in range(m):
        actual.append((f'cap:A{i}',1,lambda a,o,i=i:-a[i]))
        for q in range(m):
            actual.append((f'actual:{i}:safe:A{q}',0,
              lambda a,o,i=i,q=q: frac(a[i],sum(a))-frac(a[q],sum(a[:i])+m-i)))
        actual.append((f'actual:{i}:safe:O',0,
          lambda a,o,i=i:m*frac(a[i],sum(a))-frac(o,sum(a[:i])+m-i)))
    actual.append(('root:K',-1,lambda a,o:m*frac(a[0],sum(a))))
    def hp(path):
        b=sum(path[:-2]);c,d=path[-2:]
        return frac(c+d,sum(path))+frac(c,(b+1)*(b+2))
    actual.append(('actual:pairO',0,lambda a,o:m/2*hp(a)-frac(o,sum(a[:-2])+1)))
    branches=[]
    for i in range(m-1):
        rows=[]
        def path(a,h,i=i): return a[:i]+(a[-1],)+h
        rows.append((f'copy:{i}',0,lambda a,o,h,i=i,path=path:frac(a[i],sum(a))-frac(a[-1],sum(path(a,h)))))
        for j in range(i+1,m):
            hj=j-i-1
            rows.append((f'cap:H{j}',1,lambda a,o,h,hj=hj,path=path:-h[hj]))
            for q in range(m):
                rows.append((f'true:{j}:safe:A{q}',0,
                  lambda a,o,h,j=j,q=q,path=path:frac(path(a,h)[j],sum(path(a,h)))-frac(a[q],sum(path(a,h)[:j])+m-j)))
            for q in range(i+1,m):
                rows.append((f'true:{j}:safe:H{q}',0,
                  lambda a,o,h,j=j,q=q,path=path:frac(path(a,h)[j],sum(path(a,h)))-frac(path(a,h)[q],sum(path(a,h)[:j])+m-j)))
            rows.append((f'true:{j}:safe:O',0,
              lambda a,o,h,j=j,path=path:m*frac(path(a,h)[j],sum(path(a,h)))-frac(o,sum(path(a,h)[:j])+m-j)))
            for g in range(m):
                rows.append((f'global:{g}:H{j}',0,
                  lambda a,o,h,j=j,g=g,path=path:frac(a[g],sum(a))-frac(path(a,h)[j],sum(a[:g])+m-g)))
        if i<=m-3:
            rows.append(('pairO',0,lambda a,o,h,path=path:m/2*hp(path(a,h))-frac(o,sum(path(a,h)[:-2])+1)))
            # last-two overlap formula for arbitrary actual pair, including equal labels.
            for q in range(m):
                for r in range(q,m):
                    rows.append((f'pair:A{q}:A{r}',0,
                      lambda a,o,h,q=q,r=r,path=path:hp(path(a,h))-
                       frac(a[q]+a[r],sum(path(a,h)[:-2])+1)+
                       frac(a[q]*a[r],(sum(path(a,h)[:-2])+1)*(sum(path(a,h)[:-2])+2))))
        branches.append((i,rows))
    # Lambda columns then branch per-external-state epigraph columns then alpha.
    names=[x[0] for x in actual]
    kappas=[x[1] for x in actual]
    offsets=[]
    for i,rows in branches:
        offsets.append(len(names));names.extend(f'b{i}:{r[0]}' for r in rows);kappas.extend(r[1] for r in rows)
    nl=len(names);ne=len(states)*len(branches);alpha=nl+ne;nvar=alpha+1
    rr=[];cc=[];vv=[];rhs=[]
    def add(entries,b):
        row=len(rhs)
        for c,v in entries:
            if v:rr.append(row);cc.append(c);vv.append(v)
        rhs.append(b)
    for st,(a_o) in enumerate(states):
        a=a_o[:-1];o=a_o[-1]
        ent=[(j,f(a,o)) for j,(_,_,f) in enumerate(actual)]
        ent.extend((nl+bi*len(states)+st,1) for bi in range(len(branches)))
        ent.append((alpha,-int(any(a))))
        add(ent,-o)
    add(list(enumerate(kappas)),0)
    for bi,(i,rows) in enumerate(branches):
        for st,a_o in enumerate(states):
            a=a_o[:-1];o=a_o[-1]
            for h in itertools.product(range(2),repeat=m-i-1):
                ent=[(offsets[bi]+j,f(a,o,h)) for j,(_,_,f) in enumerate(rows)]
                ent.append((nl+bi*len(states)+st,-1))
                add(ent,0)
    mat=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nvar)).tocsr()
    cost=np.zeros(nvar);cost[alpha]=1
    print(f'm={m}, lambda={nl}, vars={nvar}, rows={len(rhs)}, nnz={len(vv)}',flush=True)
    res=linprog(cost,A_ub=mat,b_ub=rhs,bounds=[(0,None)]*nl+[(None,None)]*ne+[(0,None)],method='highs')
    out={'m':m,'success':res.success,'message':res.message}
    if res.success:
        out['ratio']=res.fun;out['active']={name:float(res.x[j]) for j,name in enumerate(names) if res.x[j]>1e-8}
        prefix=__file__.replace('copy_cone.py',f'cone{m}_model')
        save_npz(prefix+'.npz',mat)
        np.savez(prefix+'_solution.npz',x=res.x,dual=-res.ineqlin.marginals,b=np.array(rhs),cost=cost,
                 nl=nl,ne=ne,alpha=alpha)
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':
    m=int(sys.argv[1]);out=make(m)
    if len(sys.argv)>2:
        with open(sys.argv[2],'w') as f:json.dump(out,f,indent=2)
