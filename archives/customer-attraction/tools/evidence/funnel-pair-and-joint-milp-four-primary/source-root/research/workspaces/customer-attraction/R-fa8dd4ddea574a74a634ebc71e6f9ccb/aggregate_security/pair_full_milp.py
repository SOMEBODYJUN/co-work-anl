"""Floating full ordered-history SPE discovery for first-two security payment.
No global floating bound is a proof. Normalize u_1+u_2=1; maximize 2t.
All customer types and every historical action choice remain present.
"""
from pathlib import Path
from itertools import product,combinations_with_replacement
import json,time,argparse
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix

def joint(k,path,query,seconds):
    m=len(path);n=(1<<k)-1
    masks=np.arange(1,1<<k);inc=((masks[:,None]>>np.arange(k))&1).astype(float)
    nodes=tuple(h for d in range(m) for h in product(range(k),repeat=d))
    u={};z={};idx=n
    for h in nodes:
        for a in range(k):u[h,a]=idx;idx+=1
    for h in nodes:
        for a in range(k):z[h,a]=idx;idx+=1
    t=idx;count=idx+1;lo=np.zeros(count);hi=np.full(count,m,dtype=float);integ=np.zeros(count,dtype=np.uint8)
    for j in z.values():hi[j]=1;integ[j]=1
    for d,a in enumerate(path):lo[z[path[:d],a]]=hi[z[path[:d],a]]=1
    I=[];J=[];X=[];L=[];H=[]
    def add(row,lb=-np.inf,ub=np.inf):
        rr=len(L)
        for j,x in row.items():
            if x:I.append(rr);J.append(j);X.append(float(x))
        L.append(lb);H.append(ub)
    def child(h,a):
        if len(h)<m:return {u[h,a]:1}
        den=inc@np.bincount(h,minlength=k)
        row=np.divide(inc[:,a],den,out=np.zeros(n),where=den>0)
        return {j:x for j,x in enumerate(row) if x}
    def diff(h,a,ch,b):
        row={u[h,a]:1}
        for j,x in child(ch,b).items():row[j]=row.get(j,0)-x
        return row
    # u1+u2 is an actual sum, including factor2 if topics repeat.
    pair={}
    for a in path[:2]:pair[u[(),a]]=pair.get(u[(),a],0)+1
    add(pair,1,1)
    # Every topic has at most m*u1 mass, hence total mass <=km.
    add({j:1 for j in range(n)},ub=m*k)
    for a in range(k):
        row={j:float(inc[j,a]) for j in range(n) if inc[j,a]};row[u[(),path[0]]]=-m;add(row,ub=0)
    for h in nodes:
        add({z[h,a]:1 for a in range(k)},1,1)
        for a in range(k):
            for b in range(k):
                row=diff(h,b,h+(a,),b);row[z[h,a]]=m;add(row,ub=m)
                row=diff(h,b,h+(a,),b);row[z[h,a]]=-m;add(row,lb=-m)
            for b in range(k):
                if b==a:continue
                row=diff(h,a,h+(b,),b);row[z[h,a]]=-m;add(row,lb=-m)
    for bg in combinations_with_replacement(range(k),m-1):
        beta=(inc@query)/(1+inc@np.bincount(bg,minlength=k))
        row={j:-x for j,x in enumerate(beta) if x};row[t]=1;add(row,ub=0)
    A=coo_matrix((X,(I,J)),shape=(len(L),count)).tocsc();c=np.zeros(count);c[t]=-2
    start=time.time();res=milp(c,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(L),np.array(H)),options={'time_limit':seconds,'mip_rel_gap':0,'presolve':True})
    out={'k':k,'m':m,'path':path,'query':list(query),'status':int(res.status),'message':res.message,'seconds':time.time()-start,'floating_2v_lower_over_pair':float(-res.fun) if res.fun is not None else None,'floating_dual_bound':float(-res.mip_dual_bound) if hasattr(res,'mip_dual_bound') else None,'bound_is_not_a_proof':True,'variables':count,'constraints':len(L)}
    if res.x is not None:
        out['w']=res.x[:n].tolist();out['actions']=[{'h':list(h),'a':max(range(k),key=lambda a:res.x[z[h,a]])} for h in nodes]
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=6);ap.add_argument('--path',default='0,1,2');ap.add_argument('--query');ap.add_argument('--seconds',type=float,default=50);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();query=np.array(list(map(float,a.query.split(',')))) if a.query else np.ones(a.k)/a.k
    out=joint(a.k,tuple(map(int,a.path.split(','))),query,a.seconds);a.output.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ('w','actions')},flush=True)
if __name__=='__main__':main()
