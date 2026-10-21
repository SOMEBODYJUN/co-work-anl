"""Explore all-history exact mover thresholds and minimum path sums."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance, CustomerType, ExactSPESolver
from fractions import Fraction
from functools import lru_cache
import random,json,argparse

def run(inst):
    solver=ExactSPESolver(inst)
    p=inst.topic_count;m=inst.players
    @lru_cache(None)
    def val(k):
        if sum(k)==m:return Fraction(0),()
        best=min((val(k[:a]+(k[a]+1,)+k[a+1:])[0],a) for a in range(p))
        child=k[:best[1]]+(k[best[1]]+1,)+k[best[1]+1:]
        return solver.threshold(k)+best[0],(best[1],)+val(child)[1]
    total,path=val((0,)*p)
    return total,path,solver

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--trials',type=int,default=1000);ap.add_argument('--seed',type=int,default=20261021);ap.add_argument('--players',type=int,default=4);ap.add_argument('--topics',type=int,default=5);args=ap.parse_args()
    rng=random.Random(args.seed); best=None
    for t in range(args.trials):
        customers=tuple(CustomerType(frozenset(i for i in range(args.topics) if mask>>i&1),r) for mask in range(1,1<<args.topics) if (r:=rng.randrange(5)))
        inst=Instance(tuple(map(str,range(args.topics))),customers,args.players)
        total,path,solver=run(inst); opt=inst.optimal_welfare()
        ratio=total/opt if opt else Fraction(1)
        if best is None or ratio<best:
            best=ratio
            record={'trial':t,'instance':inst.to_dict(),'threshold_total':str(total),'optimum':opt,'ratio':str(ratio),'path':path,'thresholds':[str(solver.threshold(inst.counts(path[:j]))) for j in range(args.players)]}
            print(json.dumps(record),flush=True)
        if 2*total<opt:
            print('COUNTEREXAMPLE',flush=True);return
if __name__=='__main__':main()
