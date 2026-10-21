"""Discovery only: cap static queries using all actual-path deviation menus.

Every strategy is unfolded at every ordered history.  The restriction is only
on the independent static opponent distribution, not on incentive rows.
"""
from pathlib import Path
import argparse, gzip, importlib.util, json, sys, time
import numpy as np
from scipy.optimize import linprog

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'history/source/notes/customer_attraction/transport_round'))
spec = importlib.util.spec_from_file_location('old_cone', ROOT/'history/source/notes/customer_attraction/transport_round/common_q_generator.py')
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)


def menu_rows(s, cone):
    ids = {tuple(row): i for i, row in enumerate(s.Bc)}
    h = (); rows = set(); path = []
    while len(h) < s.n:
        i = s.ids[h]
        for a in range(s.m):
            q = list(s.tc[cone['branch'][i, a]])
            q[a] -= 1
            rows.add(ids[tuple(q)])
        action = int(cone['policy'][i]); path.append(action); h += (action,)
    rows = sorted(rows)
    return rows, path


def saddle(M):
    k = M.shape[1]
    z = linprog(np.r_[np.zeros(k),-1.], A_ub=np.c_[-M,np.ones(len(M))], b_ub=np.zeros(len(M)), A_eq=[np.r_[np.ones(k),0]], b_eq=[1], bounds=[(0,None)]*k+[(None,None)], method='highs')
    assert z.success, z.message
    return z.x[:-1], float(z.x[-1])


def attack(s, cone, w, rng, rounds=12):
    rows,path = menu_rows(s,cone); T = s.static[rows]
    G = cone['gamma']/s.L
    p,_ = saddle(T@w)
    best = None
    for j in range(rounds):
        beta = np.einsum('bak,a->bk',T,p)
        A = np.r_[np.c_[-G,np.zeros(len(G))],np.c_[-beta,np.ones(len(rows))]]
        bounds = [(0,None)]*(s.k+1)
        # Universal-interest clients change W and n*menu value identically.
        bounds[s.k-1] = (0,0)
        z = linprog(np.r_[cone['c'],-s.n],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[np.ones(s.k),0]],b_eq=[1],bounds=bounds,method='highs')
        assert z.success,z.message
        if best is None or z.fun<best['gap']-1e-10:
            best = dict(gap=float(z.fun),iteration=j,weights=z.x[:s.k].tolist(),p=p.tolist(),t=float(z.x[-1]),path=path,menu_backgrounds=[s.B[r] for r in rows],rows=rows,policy=[dict(history=h,action=int(a)) for h,a in zip(s.histories,cone['policy'])])
        if z.fun < -1e-7: break
        p,_=saddle(T@z.x[:s.k])
        if j%4==3:
            ext = linprog(rng.normal(size=s.k),A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[np.ones(s.k)],b_eq=[1],bounds=bounds[:s.k],method='highs')
            assert ext.success
            p,_=saddle(T@ext.x)
    return best


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=3);ap.add_argument('--k',type=int,default=6);ap.add_argument('--samples',type=int,default=20);ap.add_argument('--rounds',type=int,default=12);ap.add_argument('--seed',type=int,default=2026102117);ap.add_argument('--archive',action='store_true');ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();rng=np.random.default_rng(a.seed); spaces={};best=None;completed=0;t0=time.time()
    if a.archive:
        cases=json.load(gzip.open(ROOT/'evidence/certificates/customer_attraction/new_policy_security_cones.json.gz','rt'))['cases']
    else: cases=[None]*a.samples
    for case in cases:
        n,k = (case['players'],case['topics']) if case else (a.n,a.k)
        if (n,k) not in spaces: spaces[n,k]=old.Space(n,k)
        s=spaces[n,k]
        if case:
            cone=s.full_policy({tuple(z['history']):z['action'] for z in case['policy']})
            ext=linprog(rng.normal(size=s.k),A_ub=-cone['gamma']/s.L,b_ub=np.zeros(len(cone['gamma'])),A_eq=[np.ones(s.k)],b_eq=[1],bounds=[(0,None)]*(s.k-1)+[(0,0)],method='highs')
            if not ext.success:
                print(json.dumps(dict(skipped=case['name'],reason='no nonuniversal customer cone')),flush=True)
                continue
            w=ext.x
        else:
            density=rng.choice([.1,.3,.6,1]);w=np.where(rng.random(s.k)<density,rng.integers(1,21,s.k),0);w[-1]=0
            cone,_=s.synthesize(w,int(rng.integers(1,2**30)))
        z=attack(s,cone,w,rng,a.rounds);completed+=1
        if best is None or z['gap']<best['gap']-1e-10:
            best=dict(n=n,k=k,source=case['name'] if case else 'new full-history cone',**z)
            print(json.dumps(dict(completed=completed,gap=z['gap'],n=n,k=k,menu=len(z['rows']),elapsed=time.time()-t0)),flush=True)
        if z['gap'] < -1e-7:break
    a.output.write_text(json.dumps(dict(status='floating discovery only',completed=completed,seed=a.seed,elapsed=time.time()-t0,best=best),indent=2)+'\n')

if __name__=='__main__':main()
