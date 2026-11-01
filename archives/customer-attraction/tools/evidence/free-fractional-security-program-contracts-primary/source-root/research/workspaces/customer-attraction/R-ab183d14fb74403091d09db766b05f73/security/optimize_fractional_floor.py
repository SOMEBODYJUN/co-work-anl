"""Fenchel LP attack on individual/local free-fractional security in a real SPE cone.
All numeric points are exploratory until rational certificate reconstruction.
"""
from pathlib import Path
import sys,json,argparse
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'R-acd97406d8c4409d962eab2adcdc520c'/'round3_security'))
from search_security import Search
from fractional_minmax_probe import value

def policy_cone(s,w,target,first_action):
    info,O,u=s.evaluate(w,need_outcomes=True)
    seen=set();rows=set();stack=[((0,)*s.k,target)];policy=[]
    while stack:
        q,t=stack.pop()
        if (q,t) in seen or sum(q)==s.n:continue
        seen.add((q,t));children=[O[c] for c in s.children[q]]
        floor=max(np.min(u[ch,b]) for b,ch in enumerate(children))
        acts=[b for b,ch in enumerate(children) if t in ch and u[t,b]>=floor]
        a=first_action if not sum(q) else acts[0]
        if a not in acts:raise ValueError('Specified root action inadmissible')
        policy.append(dict(prefix=q,target=int(t),action=int(a)))
        for b,ch in enumerate(children):
            dev=t if b==a else min(ch,key=lambda j:u[j,b])
            stack.append((s.children[q][b],dev))
            row=tuple((s.utility_coeff[t,a]-s.utility_coeff[dev,b]).tolist())
            if any(row):rows.add(row)
    return np.array(sorted(rows),dtype=float)/s.scale,policy

def saddle(s,w,r,bg=None):
    M=s.masks.astype(float);bg=np.zeros(len(w)) if bg is None else np.array(bg)
    v,q,pay=value(M,w,r,bg);den=1+bg+(r-1)*M@q;z=1/den
    H=M.T@(M*(w*z*z)[:,None])
    # Find a multiplier p on active query constraints; slight numeric slack allowed.
    useq=np.flatnonzero(q>1e-7);active=np.flatnonzero(pay>=v-1e-6)
    eq=[np.r_[np.ones(s.k),0]];beq=[1]
    for j in useq:eq.append(np.r_[H[j],-1]);beq.append(0)
    bounds=[((0,None) if j in active else (0,0)) for j in range(s.k)]+[(None,None)]
    lp=linprog(np.zeros(s.k+1),A_ub=np.c_[H,-np.ones(s.k)],b_ub=np.zeros(s.k),
       A_eq=eq,b_eq=beq,bounds=bounds,method='highs')
    if lp.success:p=lp.x[:s.k]
    else:
        # Any p remains a sound lower bound; choose best active pure query if
        # the floating optimum is too inaccurate to reconstruct KKT multipliers.
        p=np.zeros(s.k);p[active]=1/len(active)
    rho=M@p;a=rho*(2*z-(1+bg)*z*z);D=M.T*(rho*z*z)
    lower=float(a@w-(r-1)*np.max(D@w))
    return dict(value=v,q=q,p=p,z=z,a=a,D=D,lower=lower)

def select(s,w,kind):
    info,O,u=s.evaluate(w,need_outcomes=True);zero=(0,)*s.k
    children=[O[c] for c in s.children[zero]]
    floor=max(np.min(u[ch,a]) for a,ch in enumerate(children))
    root=saddle(s,w,s.n)
    best=None
    for a,ch in enumerate(children):
        roots=ch[u[ch,a]>=floor]
        if not len(roots):continue
        t=min(roots,key=lambda j:u[j,a]);ui=u[t,a]/s.scale
        nex=saddle(s,w,s.n-1,s.masks[:,a]) if kind=='local' else None
        d=ui-root['value'] if kind=='floor' else ui+(s.n-1)*nex['value']-s.n*root['value']
        if best is None or d<best[0]:best=(d,int(t),a,root,nex)
    return best

def optimize(s,w,kind,rounds):
    initial=w.copy();d,t,a,_,_=select(s,w,kind);G,policy=policy_cone(s,w,t,a)
    c=s.coverage_coeff[t].astype(float);u=s.utility_coeff[t,a].astype(float)/s.scale
    w=w/(c@w);trace=[];rootmul=s.n if kind=='local' else 1
    for it in range(rounds):
        r=saddle(s,w,s.n);A=[];b=[]
        # variables: weights, h (root max Fenchel cost), next upper t
        for row in G:A.append(np.r_[-row,0,0]);b.append(0)
        for row in r['D']:A.append(np.r_[row,-1,0]);b.append(0)
        obj=np.r_[u-rootmul*r['a'],rootmul*(s.n-1),0.]
        nex=None
        if kind=='local':
            nex=saddle(s,w,s.n-1,s.masks[:,a]);den=1+s.masks[:,a]+(s.n-2)*s.masks@nex['q']
            E=s.masks.T/den
            for row in E:A.append(np.r_[row,0,-1]);b.append(0)
            obj[-1]=s.n-1
        bounds=[(0,None)]*len(w)+[(0,None),(0,None)]
        bounds[-3]=(0,0) # universal customers removed, matching initial search
        lp=linprog(obj,A_ub=A,b_ub=b,A_eq=[np.r_[c,0,0]],b_eq=[1],bounds=bounds,method='highs')
        if not lp.success:return dict(status=lp.message,trace=trace)
        w=lp.x[:-2];rr=saddle(s,w,s.n)
        nn=saddle(s,w,s.n-1,s.masks[:,a]) if kind=='local' else None
        debt=u@w-rr['value'] if kind=='floor' else u@w+(s.n-1)*nn['value']-s.n*rr['value']
        trace.append(dict(iteration=it,linear_upper=float(lp.fun),actual_debt=float(debt),root_value=rr['value'],root_Fenchel_lower=rr['lower'],next_value=nn['value'] if nn else None,root_utility=float(u@w),min_spe_margin=float(np.min(G@w)),support=int(sum(w>1e-9))))
        if debt< -1e-8 or it and abs(trace[-1]['actual_debt']-trace[-2]['actual_debt'])<1e-10:break
    rr=saddle(s,w,s.n)
    return dict(status='NUMERIC_CANDIDATE_ONLY',n=s.n,k=s.k,kind=kind,initial=list(map(int,initial)),root_counts=s.final[t],root_action=a,weights=w.tolist(),trace=trace,root_query=rr['p'].tolist(),root_z=rr['z'].tolist(),root_fractional_q=rr['q'].tolist(),policy=policy,rows=G.tolist())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('seed',type=Path);ap.add_argument('--kind',choices=['floor','local'],default='floor')
    ap.add_argument('--count',type=int,default=10);ap.add_argument('--rounds',type=int,default=15);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    data=json.loads(a.seed.read_text());seeds=data.get('bank',[data.get('best',data)]);results=[]
    for i,x in enumerate(seeds[:a.count]):
        if x is None:continue
        s=Search(x['n'],x['k'])
        r=optimize(s,np.array(x['weights'],dtype=float),a.kind,a.rounds);results.append(r)
        print(json.dumps(dict(seed=i,kind=a.kind,trace=r.get('trace'),status=r['status'])),flush=True)
        a.output.write_text(json.dumps(dict(status='NUMERIC_EXPLORATION_ONLY',results=results),indent=2)+'\n')
        if r.get('trace') and r['trace'][-1]['actual_debt'] < -1e-8:break
if __name__=='__main__':main()
