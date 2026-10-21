"""Joint count-Markov SPE / customer-mass MILP for a fixed two-step attack.

This is candidate generation. The MILP's numerical bound proves no theorem.
Both root p and tail opponent Q are fixed independent distributions.
"""
from pathlib import Path
import argparse, importlib.util, json, sys, time
sys.dont_write_bytecode=True
import numpy as np
from itertools import combinations_with_replacement
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

ROOT=Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('pair_attack',Path(__file__).with_name('pair_attack.py'))
pa=importlib.util.module_from_spec(spec);spec.loader.exec_module(pa)

def inc(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
def counts(k,n):
    for z in combinations_with_replacement(range(k),n):
        yield tuple(z.count(a) for a in range(k))

def candidate(k,path,p,Q,seconds):
    n=len(path);s=pa.old.Space(n,k);nodes=tuple(q for d in range(n) for q in counts(k,d));uv={};zz={};idx=s.k
    for q in nodes:
        for a in range(k):uv[q,a]=idx;idx+=1
    for q in nodes:
        for a in range(k):zz[q,a]=idx;idx+=1
    ti,hi=idx,idx+1;idx+=2
    lower=np.zeros(idx);upper=np.ones(idx);integ=np.zeros(idx,np.uint8)
    upper[s.k-1]=0 # Universal-interest mass shifts every security value by 1/n.
    for j in zz.values():integ[j]=1
    q=(0,)*k
    for a in path:lower[zz[q,a]]=upper[zz[q,a]]=1;q=inc(q,a)
    terminal=s.tids[q]
    rows=[];cols=[];vals=[];lb=[];ub=[]
    def add(row,l=-np.inf,u=np.inf):
        i=len(lb)
        for j,x in row.items():
            if x:rows.append(i);cols.append(j);vals.append(float(x))
        lb.append(l);ub.append(u)
    def expr(q,t):
        if sum(q)<n:return {uv[q,t]:1}
        z=s.tids[q]
        return {j:float(x/s.L) for j,x in enumerate(s.pay[z,t]) if x}
    def diff(q,t,child,ct):
        r={uv[q,t]:1}
        for j,x in expr(child,ct).items():r[j]=r.get(j,0)-x
        return r
    add({j:1 for j in range(s.k)},1,1)
    for q in nodes:
        add({zz[q,a]:1 for a in range(k)},1,1)
        for a in range(k):
            z=zz[q,a]
            for t in range(k):
                row=diff(q,t,inc(q,a),t);row[z]=1;add(row,u=1)
                row=diff(q,t,inc(q,a),t);row[z]=-1;add(row,l=-1)
            for b in range(k):
                if b==a:continue
                row=diff(q,a,inc(q,b),b);row[z]=-1;add(row,l=-1)
    beta=np.einsum('bak,a->bk',s.static,p)
    for row in beta:add({**{j:-x for j,x in enumerate(row) if x},ti:1},u=0)
    T,rivals=pa.tail_tensor(s,path[:2]);TQ=np.einsum('bak,b->ak',T,Q)
    for row in TQ:add({**{j:x for j,x in enumerate(row) if x},hi:-1},u=0)
    A=coo_matrix((vals,(rows,cols)),shape=(len(lb),idx)).tocsc()
    obj=np.zeros(idx);obj[:s.k]=(s.pay[terminal,path[0]]+s.pay[terminal,path[1]])/s.L;obj[ti]=-n;obj[hi]=n-2
    started=time.monotonic();z=milp(obj,integrality=integ,bounds=Bounds(lower,upper),constraints=LinearConstraint(A,lb,ub),options={'time_limit':seconds,'mip_rel_gap':0.0})
    ans=dict(status='numerical joint candidate only; no theorem',k=k,n=n,path=path,p=p.tolist(),Q=Q.tolist(),tail_rivals=rivals,seconds=time.monotonic()-started,milp_status=int(z.status),message=z.message,objective=float(z.fun) if z.fun is not None else None,variables=idx,binaries=len(zz),rows=len(lb))
    if z.x is not None:
        policy={q:max(range(k),key=lambda a:z.x[zz[q,a]]) for q in nodes}
        ans['weights']=z.x[:s.k].tolist();ans['count_policy']=[dict(counts=q,action=a) for q,a in policy.items()]
        actions={h:policy[tuple(h.count(a) for a in range(k))] for h in s.histories};cone=s.full_policy(actions)
        w=z.x[:s.k]
        ans['floating_min_full_Gamma']=float(np.min(cone['gamma']@w)/s.L)
        ans['full_policy']=[dict(history=h,action=int(a)) for h,a in zip(s.histories,cone['policy'])]
        ans['actual_root_counts']=s.tc[cone['realized'][0]]
    return ans

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=6);ap.add_argument('--path',default='0,1,2,3');ap.add_argument('--tail',default='all');ap.add_argument('--seconds',type=float,default=45);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();path=tuple(map(int,a.path.split(',')));p=np.ones(a.k)/a.k
    rivals=list(combinations_with_replacement(range(a.k),len(path)-3));Q=np.zeros(len(rivals))
    chosen=list(range(a.k)) if a.tail=='all' else list(map(int,a.tail.split(',')))
    for i,B in enumerate(rivals):Q[i]=all(x in chosen for x in B)
    Q/=sum(Q)
    ans=candidate(a.k,path,p,Q,a.seconds);a.output.write_text(json.dumps(ans,indent=2)+'\n');print(json.dumps({k:v for k,v in ans.items() if k not in ('weights','count_policy','full_policy')}),flush=True)

if __name__=='__main__':main()
