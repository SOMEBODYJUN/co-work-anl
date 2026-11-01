"""Discovery only: full credible continuation cones on two-anchor leaf catalogues.

All count-outcome sets enumerate arbitrary history-dependent SPEs.  The cone
recursion selects one complete policy independently on each ordered subtree;
deduplicating identical (count,target) continuation objects merely removes
identical constraints. Float LP output requires exact rational replay.
"""
from pathlib import Path
import argparse, importlib.util, json, random, time
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
OLD=ROOT/'research/workspaces/customer-attraction/R-ffea274483aa4105a317300038fe04ce/credible_counterexample/cone_search.py'
spec=importlib.util.spec_from_file_location('old_cone',OLD)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--m',type=int,default=5)
    ap.add_argument('--anchors',type=int,default=2);ap.add_argument('--steps',type=int,default=500)
    ap.add_argument('--seed',type=int,default=610219);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--two-used',action='store_true')
    args=ap.parse_args();rng=random.Random(args.seed);m=args.m;d=args.anchors;p=m+d
    search=module.Search(p,m)
    # Each leaf's customers can belong to any subset of anchor themes;
    # no customer belongs to two leaves.  Anchor-only types are also retained.
    masks=[z for z in range(1,1<<p) if (z>>d).bit_count()<=1]
    support=np.array([z-1 for z in masks],dtype=int)
    queue=[];records=[];best=0;started=time.time()
    def seed():
        w=np.zeros((1<<p)-1)
        if rng.randrange(3):
            w[0]=m
            for a in range(1,p):w[(1<<a)-1]=1
            for _ in range(3):w[rng.choice(masks)-1]+=rng.choice([0,1,2])
        else:
            for _ in range(rng.randrange(5,20)):w[rng.choice(masks)-1]+=rng.randrange(1,20)
        return w
    for step in range(args.steps):
        if not queue or step%20==0:queue.append(seed())
        w=queue.pop(0);ratio,targets,obj=search.solve(w)
        if args.two_used:
            anchors=[int(t) for t in search.out[0] if sum(search.leaves[int(t)][:d])==m and min(search.leaves[int(t)][:d])>0]
            if not anchors:
                queue.append(seed());continue
            worst=min(search.welfare[t] for t in anchors)
            targets=[t for t in anchors if search.welfare[t]<=worst+1e-7]
            ratio=float(np.max(search.obj@w)/worst)
        if ratio>best+1e-8:
            best=ratio;records.append({'step':step,'kind':'BI','ratio':float(ratio),'weights':w.tolist(),'target':[search.leaves[int(t)] for t in targets]})
            print('BEST',step,best,'targets',len(targets),flush=True)
        target=int(rng.choice(targets));rows,nodes,route=search.cone(target,rng)
        # Optimize the actual best benchmark, or all leaves to retain the
        # intended anchor/leaf witness, with small random face exploration.
        benchmark=search.obj[obj] if rng.randrange(4) else np.any(search.bits[:,d:],axis=1)
        objective=benchmark[support].astype(float)
        if step%7==0:objective+=np.array([rng.random() for _ in support])*1e-5
        res=linprog(-objective,A_ub=-rows[:,support],b_ub=np.zeros(len(rows)),
                    A_eq=search.cov[target,support][None,:],b_eq=[1],bounds=(0,None),method='highs')
        if res.success:
            x=np.zeros((1<<p)-1);x[support]=res.x;x[x<1e-10]=0
            score=float(benchmark@x)
            if score>best+1e-8:
                best=score;records.append({'step':step,'kind':'cone','ratio':score,'weights':x.tolist(),'target':search.leaves[target],'min_slack':float(np.min(rows@x))})
                print('BEST_CONE',step,best,'rows',len(rows),'nodes',nodes,flush=True)
            queue.append(x)
            if step%3==0:
                y=x*60
                for _ in range(2):y[rng.choice(masks)-1]+=rng.randrange(1,4)
                queue.append(y)
        if step%10==0:
            report={'m':m,'p':p,'steps':step,'best':best,'records':records,'seconds':time.time()-started,'status':'floating complete-policy cone discovery; no universal conclusion'}
            args.output.write_text(json.dumps(report,indent=2))
            print('STEP',step,'best',best,'elapsed',time.time()-started,flush=True)
    report={'m':m,'p':p,'steps':args.steps,'best':best,'records':records,'seconds':time.time()-started,'status':'floating complete-policy cone discovery; no universal conclusion'}
    args.output.write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
