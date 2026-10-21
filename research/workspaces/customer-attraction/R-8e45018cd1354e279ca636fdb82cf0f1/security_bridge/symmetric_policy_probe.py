"""Numerical whole-cone probe of a two-group full-history policy.

All r[i,j] are multiplicities PER interest subset with i labels in X and j
labels in Y. We impose within-group and group-swap symmetry. The policy picks
0, then an opposite-group fresh label, then fresh labels in the second
player's group after EVERY history. Prefix partitions exhaust its incentive
classes, including repeated off-path actions. Numerical LP is discovery only.
"""
from functools import lru_cache
from math import comb
from itertools import product
import argparse,json,time
import numpy as np
from scipy.optimize import linprog

@lru_cache(None)
def partitions(total, cap=None):
    if total==0:return ((),)
    cap=total if cap is None else min(cap,total)
    return tuple((v,)+tail for v in range(cap,0,-1) for tail in partitions(total-v,v))

@lru_cache(None)
def distributions(q):
    out={(0,0):1}
    for v in q:
        nxt=dict(out)
        for (s,l),w in out.items():nxt[s+1,l+v]=nxt.get((s+1,l+v),0)+w
        out=nxt
    rows=[{} for _ in range(len(q)+1)]
    for (s,l),w in out.items():rows[s][l]=w
    return tuple(rows)

def pad(q,n):return tuple(q)+(0,)*(n-len(q))

def utility_row(qx,qy,group,label,n,variables):
    own=(qx if group==0 else qy)[label]
    assert own>0
    xx=qx[:label]+qx[label+1:] if group==0 else qx
    yy=qy[:label]+qy[label+1:] if group==1 else qy
    dx,dy=distributions(tuple(xx)),distributions(tuple(yy))
    ans=[]
    for i,j in variables:
        value=0
        for a,b in {(i,j),(j,i)}:
            si,sj=a-(group==0),b-(group==1)
            if si<0 or sj<0 or si>=len(dx) or sj>=len(dy):continue
            value+=sum(w*v/(own+l+h) for l,w in dx[si].items() for h,v in dy[sj].items())
        ans.append(value)
    return np.array(ans)

def add_fresh(q,t):
    q=list(q)
    for _ in range(t):q[q.index(0)]=1
    return tuple(q)

def geometry(n):
    variables=[(i,j) for i in range(n+1) for j in range(i,n+1) if i+j]
    gamma=[]
    for d in range(2,n):
        for dx in range(d):
            dy=d-dx
            for px,py in product(partitions(dx),partitions(dy)):
                qx,qy=pad(px,n),pad(py,n)
                # h[1] is in Y, so Y appears at least once. Every such count
                # pattern is attainable by an ordered history of length d.
                yi=qy.index(0)
                chosen_y=add_fresh(qy,n-d)
                actual=utility_row(qx,chosen_y,1,yi,n,variables)
                for group,q in [(0,qx),(1,qy)]:
                    for old in sorted(set(q)):
                        ai=q.index(old);vx,vy=list(qx),list(qy)
                        (vx if group==0 else vy)[ai]+=1
                        vy=add_fresh(tuple(vy),n-d-1)
                        dev=utility_row(tuple(vx),tuple(vy),group,ai,n,variables)
                        gamma.append(actual-dev)
    # At the unique first-prefix class, the second player can join either
    # group, and their action determines every subsequent player's group.
    qx,qy=(1,)+(0,)*(n-1),(0,)*n
    actual=utility_row(qx,add_fresh(qy,n-1),1,0,n,variables)
    for ai in (0,1):
        vx=list(qx);vx[ai]+=1;vx=add_fresh(tuple(vx),n-2)
        gamma.append(actual-utility_row(vx,qy,0,ai,n,variables))
    G=np.unique(np.round(np.array(gamma),12),axis=0)
    betas=[];backgrounds=[]
    for dx in range(n):
        for px,py in product(partitions(dx),partitions(n-1-dx)):
            qx,qy=pad(px,n),pad(py,n)
            ax,ay=distributions(qx),distributions(qy)
            values=[]
            for i,j in variables:
                value=0
                for a,b in {(i,j),(j,i)}:
                    value+=(a+b)/(2*n)*sum(w*v/(1+l+h) for l,w in ax[a].items() for h,v in ay[b].items())
                values.append(value)
            betas.append(values);backgrounds.append((px,py))
    W=[]
    for i,j in variables:
        value=0
        for a,b in {(i,j),(j,i)}:
            value+=comb(n,a)*comb(n,b)-(comb(n-1,a) if a<=n-1 else 0)*(comb(1,b) if b<=1 else 0)
        W.append(value)
    return variables,G,np.array(betas),np.array(W),backgrounds

def run(n):
    t=time.time();variables,G,B,W,backgrounds=geometry(n)
    lp=linprog(W,A_ub=-np.vstack((G,B)),b_ub=np.r_[np.zeros(len(G)),-np.ones(len(B))],bounds=(0,None),method='highs')
    assert lp.success,lp.message
    return dict(players=n,types=len(variables),incentive_classes=len(G),background_classes=len(B),objective=float(lp.fun),gap=n-float(lp.fun),weights=[dict(i=i,j=j,r=float(r)) for (i,j),r in zip(variables,lp.x) if r>1e-8],elapsed=time.time()-t,status='numerical discovery only')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--min-n',type=int,default=3);ap.add_argument('--max-n',type=int,default=8);ap.add_argument('--output',required=True);args=ap.parse_args()
    records=[]
    for n in range(args.min_n,args.max_n+1):
        rec=run(n);records.append(rec);print(json.dumps(rec),flush=True)
        open(args.output,'w').write(json.dumps(records,indent=2)+'\n')
