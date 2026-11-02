"""Exact integer attack on the strengthened arbitrary-background opportunity bound.

For each sampled unit-customer instance, checks every legal count prefix and
every full-history SPE output and admissible current action from that prefix.
The outer set of instances remains finite. No universal conclusion follows.
"""
import argparse,json,random,runpy
from pathlib import Path
import numpy as np

D=runpy.run_path(str(Path(__file__).with_name('fullset_search.py')));Oracle=D['Oracle']

def main():
    ps=argparse.ArgumentParser();ps.add_argument('--topics',type=int,default=7);ps.add_argument('--players',type=int,default=5);ps.add_argument('--trials',type=int,default=1000);ps.add_argument('--seed',type=int,default=2026102126);ps.add_argument('--output',required=True);args=ps.parse_args()
    O=Oracle(args.topics,args.players);rng=random.Random(args.seed);records=[];best=-1e99;checked=0
    for tr in range(args.trials):
        mass=np.array([rng.choice([0,0,0,0,1,2,5,10,30]) for _ in O.masks],dtype=np.int64)
        O.solve(mass);local={'value':-1e99}
        for layer in O.layers:
            for q in layer:
                for a,ch in enumerate(O.child[q]):
                    feasible=O.out[ch][O.U[O.out[ch],a]>=O.floor[q]]
                    checked+=len(feasible)
                    if not len(feasible):continue
                    gaps=O.L*(O.OPT-O.W[feasible])-O.m*O.U[feasible,a];j=int(np.argmax(gaps));value=int(gaps[j])/O.L
                    if value>local['value']+1e-10:
                        t=int(feasible[j]);local={'value':value,'background':q,'target_action':a,'terminal':O.term[t],'utility_scaled':int(O.U[t,a]),'utility_scale':O.L,'optimum':O.OPT,'welfare':int(O.W[t])}
        if local['value']>best+1e-10:
            best=local['value'];rec=dict(local,trial=tr,weights={str(mask):int(v) for mask,v in zip(O.masks,mass) if v});records.append(rec);print(json.dumps({a:b for a,b in rec.items() if a!='weights'}),flush=True)
        Path(args.output).write_text(json.dumps({'scope':__doc__,'parameters':vars(args),'completed':tr+1,'admissible_prefix_action_outcomes_checked':checked,'record_improvements':records},indent=2)+'\n')
        if tr%100==0:print('completed',tr,'best',best,flush=True)
        if best>0:break
if __name__=='__main__':main()
