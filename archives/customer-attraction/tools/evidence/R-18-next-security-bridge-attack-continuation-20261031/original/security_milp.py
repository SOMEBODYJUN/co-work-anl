"""Full-history MILP discovery: fixed query p, normalized root W=1, maximize static safety t.
Adapted from tests/audits/cone_attack_joint_milp.py, with identical justified M=m.
Floating MILP bounds never count as a proof.
"""
from pathlib import Path
import sys,json,time,argparse
from itertools import product,combinations_with_replacement
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix
ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT/'tests/audits'))
sys.path.insert(0,str(ROOT))
from customer_attraction_strategy_lp import payoff_row,coverage_row
P=Path(__file__).resolve().parent

def joint(p,path,query,seconds):
    m=len(path);n=(1<<p)-1
    nodes=tuple(h for d in range(m) for h in product(range(p),repeat=d))
    u={};z={};idx=n
    for h in nodes:
        for a in range(p):u[h,a]=idx;idx+=1
    for h in nodes:
        for a in range(p):z[h,a]=idx;idx+=1
    t=idx;count=idx+1;lo=np.zeros(count);hi=np.full(count,m,dtype=float);integ=np.zeros(count,dtype=np.uint8)
    for j in z.values():hi[j]=1;integ[j]=1
    for d,a in enumerate(path):lo[z[path[:d],a]]=hi[z[path[:d],a]]=1
    hi[u[(),path[0]]]=1
    I=[];J=[];X=[];L=[];H=[]
    def add(row,lb=-np.inf,ub=np.inf):
        r=len(L)
        for j,x in row.items():
            if x:I.append(r);J.append(j);X.append(float(x))
        L.append(lb);H.append(ub)
    def child(h,a):
        if len(h)<m:return {u[h,a]:1}
        q=tuple(h.count(b) for b in range(p))
        if not q[a]:return {}
        return {j:x for j,x in enumerate(payoff_row(p,q,a)) if x}
    def diff(h,a,ch,b):
        row={u[h,a]:1}
        for j,x in child(ch,b).items():row[j]=row.get(j,0)-x
        return row
    q=tuple(path.count(a) for a in range(p));crow=coverage_row(p,set(path))
    add({j:x for j,x in enumerate(crow) if x},1,1)
    add({j:1 for j in range(n)},ub=m*p)
    # Universal full-interest clients cancel from every security gap; fix to0 wlog.
    hi[n-1]=0
    for a in range(p):
        row={j:1 for j in range(n) if (j+1)&(1<<a)};row[u[(),path[0]]]=-m;add(row,ub=0)
    add({u[(),a]:n_a for a,n_a in enumerate(q) if n_a},1,1)
    for h in nodes:
        add({z[h,a]:1 for a in range(p)},1,1)
        for a in range(p):
            for b in range(p):
                row=diff(h,b,h+(a,),b);row[z[h,a]]=m;add(row,ub=m)
                row=diff(h,b,h+(a,),b);row[z[h,a]]=-m;add(row,lb=-m)
            for b in range(p):
                if b==a:continue
                row=diff(h,a,h+(b,),b);row[z[h,a]]=-m;add(row,lb=-m)
    for bg in combinations_with_replacement(range(p),m-1):
        beta=np.zeros(n)
        for a,p_a in enumerate(query):
            counts=tuple(bg.count(b)+(a==b) for b in range(p))
            beta+=p_a*np.array(payoff_row(p,counts,a),float)
        row={j:-x for j,x in enumerate(beta) if x};row[t]=1;add(row,ub=0)
    A=coo_matrix((X,(I,J)),shape=(len(L),count)).tocsc();c=np.zeros(count);c[t]=-1
    start=time.time();res=milp(c,integrality=integ,bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(L),np.array(H)),options={'time_limit':seconds,'mip_rel_gap':0,'presolve':True})
    out={'k':p,'m':m,'path':path,'query':list(query),'status':int(res.status),'message':res.message,'seconds':time.time()-start,'floating_objective':float(-res.fun) if res.fun is not None else None,'floating_dual_bound':float(-res.mip_dual_bound) if hasattr(res,'mip_dual_bound') else None,'bound_is_not_a_proof':True,'variables':count,'constraints':len(L)}
    if res.x is not None:
        out['w']=res.x[:n].tolist();out['actions']=[{'h':list(h),'a':max(range(p),key=lambda a:res.x[z[h,a]])} for h in nodes]
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=6);ap.add_argument('--path',default='0,1,2');ap.add_argument('--query');ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--tag',default='trial');a=ap.parse_args();query=np.array(list(map(float,a.query.split(',')))) if a.query else np.ones(a.k)/a.k
    out=joint(a.k,tuple(map(int,a.path.split(','))),query,a.seconds);(P/f'milp-{a.tag}.json').write_text(json.dumps(out,indent=2));print({k:v for k,v in out.items() if k not in ('w','actions')},flush=True)
if __name__=='__main__':main()
