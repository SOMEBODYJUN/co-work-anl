"""Finite floating exploration of the union of all actual-node deviation backgrounds.

A positive gap only refutes that restricted static menu, not genuine v_n.
Uses the already saved complete-policy cone construction, no frozen output edits.
"""
from __future__ import annotations
import argparse, importlib.util, itertools as it, json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
BASE=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('old_security',BASE/'security_transport/search_security.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def menus(k,n,policy,terminals, all_nodes=False):
    root=terminals[()]
    histories=list(policy) if all_nodes else [root[:i] for i in range(n)]
    bgs=set()
    for h in histories:
        i=len(h)
        for a in range(k):
            z=terminals[h+(a,)]
            bgs.add(tuple(sorted(z[:i]+z[i+1:])))
    return sorted(bgs)

def matrix(members,bgs):
    loads=np.array([members[list(b)].sum(axis=0) for b in bgs])
    return members[None,:,:]/(1+loads[:,None,:])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=3);ap.add_argument('--topics',type=int,default=6);ap.add_argument('--trials',type=int,default=100);ap.add_argument('--seed',type=int,default=205190);ap.add_argument('--all-nodes',action='store_true');ap.add_argument('--integer',action='store_true');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    n,k=args.players,args.topics;rng=np.random.default_rng(args.seed)
    members,full=old.data(k,n)
    summary={'kind':'finite floating exploration only','arguments':{**vars(args),'output':str(args.output)},'best_gap':0.,'completed':0,'records':[]}
    for trial in range(args.trials):
        w=(rng.integers(0,4,size=(1<<k)-1).astype(float) if args.integer else rng.exponential(size=(1<<k)-1));w[rng.random(len(w))<0.8]=0;w=w if w.sum() else np.ones_like(w);w/=w.sum()
        policy,terminals=old.random_spe(members,n,w,rng)
        gamma,c,rows=old.cone(members,policy,terminals)
        bgs=menus(k,n,policy,terminals,args.all_nodes);static=matrix(members,bgs)
        p,v=old.safety(static,w)
        ps=[p,np.ones(k)/k,rng.dirichlet(np.ones(k))]
        best=0.
        for iteration in range(8):
            p=ps[iteration] if iteration<len(ps) else old.safety(static,ans.x[:-1])[0]
            ans=old.optimize(members,static,gamma,c,p,n)
            gap=-ans.fun;best=max(best,gap)
            if gap>summary['best_gap']+1e-10:
                summary['best_gap']=float(gap)
                summary['witness']={'trial':trial,'policy':{','.join(map(str,h)):int(a) for h,a in policy.items()},'root':list(terminals[()]),'backgrounds':[list(x) for x in bgs],'p':p.tolist(),'w':ans.x[:-1].tolist(),'t':float(ans.x[-1])}
        summary['completed']=trial+1;summary['records'].append({'trial':trial,'best_gap':float(best),'menus':len(bgs)})
        if trial%10==0 or summary['best_gap']>1e-7:
            args.output.write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({'trial':trial,'best_gap':summary['best_gap']}),flush=True)
        if summary['best_gap']>1e-7:break
    args.output.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'completed':summary['completed'],'best_gap':summary['best_gap']}),flush=True)
if __name__=='__main__':main()
