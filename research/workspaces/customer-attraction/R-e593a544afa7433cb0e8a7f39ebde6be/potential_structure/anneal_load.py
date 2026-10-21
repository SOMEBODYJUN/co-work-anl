"""Search only; minimized load-proxy gap is not a proof if nonnegative."""
import argparse, json, math, random, time
from load_search import solve

ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=4);ap.add_argument('--m',type=int,default=3);ap.add_argument('--trials',type=int,default=20000);ap.add_argument('--seed',type=int,default=1201);ap.add_argument('--out',default=None);args=ap.parse_args()
rng=random.Random(args.seed);m=args.m;p=args.p
sets=[tuple(a for a in range(p) if mask>>a&1) for mask in range(1,1<<p)]

def evaluate(w):
    types=[(B,n) for B,n in zip(sets,w) if n]
    gap,c,load,W,proxy,opt=solve(types,p,m)
    objective=float(gap)/max(1,opt)
    return objective,dict(types=types,p=p,m=m,gap=str(gap),counts=c,load=load,W=W,proxy=str(proxy),OPT=opt)

start=time.time();record=None
for it in range(args.trials):
    if it%1000==0:
        w=[0]*len(sets)
        w[0]=m*10
        for a in range(1,p):w[(1<<a)-1]=10
        current,data=evaluate(w)
    trial=w[:]
    a=rng.randrange(len(w))
    trial[a]=max(0,min(60,trial[a]+rng.choice([-5,-2,-1,1,2,5])))
    if not any(trial):continue
    obj,data=evaluate(trial)
    if record is None or obj<record['objective']:
        record=dict(iteration=it,objective=obj,**data)
        print(json.dumps(record),flush=True)
    if obj<0:break
    temp=.002+ .025*(1-(it%1000)/1000)
    if obj<=current or rng.random()<math.exp(min(0,(current-obj)/temp)):
        w,current=trial,obj
report=dict(seed=args.seed,iterations=it+1,elapsed=time.time()-start,best=record)
if args.out:
    with open(args.out,'x') as f:json.dump(report,f,indent=2)
print(json.dumps(report),flush=True)
