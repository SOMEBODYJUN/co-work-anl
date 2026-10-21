"""Adaptive full-policy-cone attack on the two-step static-security budget.

Numerical screening only. Every policy is defined at every ordered history.
Both security games use independently fixed opponent backgrounds.
"""
from pathlib import Path
import argparse, importlib.util, json, random, sys, time
from math import lcm
sys.dont_write_bytecode = True
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'history/source/notes/customer_attraction/transport_round'))
spec = importlib.util.spec_from_file_location('old_cone', ROOT/'history/source/notes/customer_attraction/transport_round/common_q_generator.py')
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)

def saddle(M):
    k = M.shape[1]
    z = linprog(np.r_[np.zeros(k), -1.], A_ub=np.c_[-M, np.ones(len(M))], b_ub=np.zeros(len(M)), A_eq=[np.r_[np.ones(k), 0]], b_eq=[1], bounds=[(0,None)]*k+[(None,None)], method='highs')
    assert z.success, z.message
    return z.x[:-1], -z.ineqlin.marginals, z.x[-1]

def tail_tensor(s, first):
    bg = s.inc[:, first].sum(axis=1)+getattr(s,'background_load',0)
    rivals = list(combinations_with_replacement(range(s.m), s.n-3))
    T = np.array([s.inc.T/(1+bg+s.inc[:,B].sum(axis=1))[None,:] for B in rivals])
    return T, rivals

def residual_space(n,k,prefix):
    s=old.Space(n,k);s.prefix=tuple(prefix)
    s.background_load=s.inc[:,prefix].sum(axis=1) if prefix else np.zeros(s.k,dtype=np.int64)
    if prefix:
        s.L=lcm(*range(1,n+len(prefix)+1))
        den=s.den+s.background_load[None,:]
        inv=np.zeros_like(den)
        for d in range(1,n+len(prefix)+1):inv[den==d]=s.L//d
        s.pay=inv[:,None,:]*s.inc.T[None,:,:]
        s.static_den=s.static_den+s.background_load[None,:]
        s.static=s.inc.T[None,:,:]/s.static_den[:,None,:]
    return s

def worst_pair_policy(s, w, seed):
    roots, menus, floor, u = s.outcomes(w)
    root = (0,)*s.m
    best = None
    for a in range(s.m):
        qa = list(root); qa[a] += 1; qa = tuple(qa)
        for b in range(s.m):
            qab = list(qa); qab[b] += 1; qab = tuple(qab)
            _, _, vtail = saddle(tail_tensor(s, (a,b))[0]@w)
            for t in menus[qab]:
                if u[t,a] < floor[root] or u[t,b] < floor[qa]: continue
                val = (u[t,a]+u[t,b])/s.L + (s.n-2)*vtail
                if best is None or val < best[0]-1e-9: best = (val, a, b, t)
    _,a,b,target = best
    rng = random.Random(seed); pol = {}
    def expand(h,q,t):
        if len(h)==s.n: return
        ch=[q[:x]+(q[x]+1,)+q[x+1:] for x in range(s.m)]
        feasible=[x for x,c in enumerate(ch) if t in menus[c] and u[t,x]>=floor[q]]
        x = a if not h else b if h==(a,) else rng.choice(feasible)
        assert x in feasible
        pol[h]=x
        for y,c in enumerate(ch):
            ty=t if y==x else rng.choice([v for v in menus[c] if u[v,y]==min(u[z,y] for z in menus[c])])
            expand(h+(y,),c,ty)
    expand((),root,target)
    cone=s.full_policy(pol)
    assert np.min(cone['gamma']@w)>=0
    return cone, (a,b)

def attack(s, cone, first, w, rng, iterations):
    G=cone['gamma']/s.L
    terminal=cone['realized'][0]
    d=(s.pay[terminal,first[0]]+s.pay[terminal,first[1]])/s.L
    T,rivals=tail_tensor(s,first)
    p,_,_=saddle(s.static@w); _,q,_=saddle(T@w)
    best=None
    for j in range(iterations):
        beta=np.einsum('bak,a->bk',s.static,p)
        upper=np.einsum('bak,b->ak',T,q)
        A=np.r_[np.c_[-G,np.zeros((len(G),2))],np.c_[-beta,np.ones(len(beta)),np.zeros(len(beta))],np.c_[upper,np.zeros(s.m),-np.ones(s.m)]]
        bounds=[(0,None)]*(s.k+2);bounds[s.k-1]=(0,0)
        z=linprog(np.r_[d,-s.n,s.n-2],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[np.ones(s.k),0,0]],b_eq=[1],bounds=bounds,method='highs')
        assert z.success,z.message
        if best is None or z.fun<best['gap']-1e-10:
            best=dict(gap=z.fun,weights=z.x[:s.k].tolist(),p=p.tolist(),q=q.tolist(),first=first,rivals=rivals,iteration=j,policy=[dict(history=h,action=int(a)) for h,a in zip(s.histories,cone['policy'])])
        if z.fun < -1e-8:break
        p,_,_=saddle(s.static@z.x[:s.k]); _,q,_=saddle(T@z.x[:s.k])
        if j%4==3:
            extreme=linprog(rng.normal(size=s.k),A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[np.ones(s.k)],b_eq=[1],bounds=bounds[:s.k],method='highs')
            assert extreme.success
            p,_,_=saddle(s.static@extreme.x); _,q,_=saddle(T@extreme.x)
    return best

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--n',type=int,default=4); ap.add_argument('--k',type=int,default=6); ap.add_argument('--samples',type=int,default=100); ap.add_argument('--iterations',type=int,default=8); ap.add_argument('--seed',type=int,default=8976021); ap.add_argument('--background',default='');ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args(); rng=np.random.default_rng(a.seed); prefix=tuple(map(int,a.background.split(','))) if a.background else ();s=residual_space(a.n,a.k,prefix); best=None; completed=0; t0=time.time()
    for i in range(a.samples):
        density=rng.choice([.1,.3,.6,1.]); w=np.where(rng.random(s.k)<density,rng.integers(1,21,s.k),0);w[-1]=0
        cone,first=worst_pair_policy(s,w,int(rng.integers(1,2**30)))
        z=attack(s,cone,first,w,rng,a.iterations); completed+=1
        if best is None or z['gap']<best['gap']-1e-10:
            best=z; print(json.dumps(dict(sample=i,gap=z['gap'],first=first,histories=len(s.histories),elapsed=time.time()-t0)),flush=True)
        if z['gap'] < -1e-8:break
    a.output.write_text(json.dumps(dict(status='numerical screening only; no exact certificate',n=a.n,k=a.k,prefix=prefix,seed=a.seed,completed=completed,elapsed=time.time()-t0,best=best),indent=2)+'\n')

if __name__=='__main__':main()
