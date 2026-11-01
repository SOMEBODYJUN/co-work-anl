"""Make genuine sparse 15-theme CAGs from the 437-row obstruction's 64 atoms.

Preserves fixed ABCDEUVWXY memberships and each atom's optimum multiplicity j;
randomly aligns the five T memberships. Does not claim to realize indexed replies.
Every queried equilibrium/LP is for the actual resulting 15-theme catalog.
"""
from __future__ import annotations
import argparse,json,random,time,sys,itertools,math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from cone_walk import Engine,HERE,ROOT
from customer_attraction import Instance,CustomerType,StrategyCertificate,verify_certificate

def dag_cone(eng,target):
    policy={};rows=[]
    def rec(t,sid,target):
        if t==eng.m:return target
        key=(t,sid,target)
        if key in policy:return target
        childids=eng.children[t][sid]
        admissible=[a for a,cid in enumerate(childids) if target in eng.R[t+1][cid] and eng.u[target,a]>=eng.floor[t][sid]-eng.eps]
        chosen=eng.rng.choice(admissible);childterms=[]
        for a,cid in enumerate(childids):
            if a==chosen:dest=target
            else:
                C=eng.R[t+1][cid];vals=eng.u[C,a];mini=vals.min()
                dest=int(eng.rng.choice(list(C[vals<=mini+eng.eps])))
            childterms.append(dest)
        policy[key]=(chosen,childterms)
        for a,(cid,dest) in enumerate(zip(childids,childterms)):
            rec(t+1,int(cid),dest)
            if a!=chosen:rows.append(eng.pay[target,chosen]-eng.pay[dest,a])
        return target
    rec(0,0,target)
    G=np.unique(np.array(rows,dtype=np.int16),axis=0);G=G[np.any(G!=0,axis=1)]
    return policy,G

def expand(eng,policy,target):
    actions={}
    def rec(h,sid,target):
        t=len(h)
        if t==eng.m:return
        chosen,dests=policy[(t,sid,target)];actions[h]=chosen
        for a,(cid,dest) in enumerate(zip(eng.children[t][sid],dests)):rec(h+(a,),int(cid),dest)
    rec((),0,target);return actions

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--steps',type=int,default=6);ap.add_argument('--seed',type=int,default=18202677);ap.add_argument('--symmetric',action='store_true');args=ap.parse_args()
    rng=random.Random(args.seed);start=time.monotonic();records=[];best=F(0)
    frozen=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
    for iteration in range(args.steps):
        masses={}
        for atom in frozen['atoms']:
            j=sum(n for k,n in enumerate(atom['AB_hist']) if k>=4)
            selections=list(itertools.combinations(range(5),j)) if args.symmetric else [rng.sample(range(5),j)]
            for selected in selections:
                mask=sum((int(b)<<a) for a,b in enumerate(atom['bits']))+sum(1<<(10+a) for a in selected)
                mass=atom['mass_numerator']*(10//math.comb(5,j) if args.symmetric else 1)
                masses[mask]=masses.get(mask,0)+mass
        masks=sorted(masses);raw=[masses[k] for k in masks]
        # Normalize for floating proposal utility arithmetic only.
        r=np.array(raw,dtype=float)/float(frozen['denominator'])/(10 if args.symmetric else 1)
        eng=Engine(5,15,rng,masks=masks)
        target,ratio=eng.solve(r)
        desired=eng.index[5][(1,1,1,1,1)+(0,)*10]
        desired_ok=bool(desired in eng.R[0][0])
        print(json.dumps({'iteration':iteration,'stage':'actual_all_SPE_proposal','ratio':ratio,'types':len(masks),'original_ABCDE_feasible_proposal':desired_ok,'root':eng.terminal[target].tolist(),'elapsed':round(time.monotonic()-start,2)}),flush=True)
        policy,G=dag_cone(eng,target)
        actualids=np.argsort(eng.v@r)[-2:].tolist()
        actualids+=[eng.portfolios.index((10,11,12,13,14))]
        for jid in list(dict.fromkeys(actualids)):
            result=eng.optimize(target,G,jid)
            if result is None:continue
            x,value=result
            rec={'iteration':iteration,'types':len(masks),'dag_nodes':len(policy),'rows':len(G),'input_ratio_proposal':ratio,'lp_ratio_proposal':value,'portfolio':eng.portfolios[jid],'root':eng.terminal[target].tolist()};records.append(rec)
            if value>float(best)+1e-9:
                clones=eng.exact_recover(G,target,x)
                if clones is not None:
                    instance=Instance(tuple('ABCDEUVWXY')+tuple('T'+str(i) for i in range(5)),tuple(CustomerType(frozenset(a for a in range(15) if mask&(1<<a)),n) for mask,n in zip(masks,clones) if n),5)
                    cert=StrategyCertificate(expand(eng,policy,target),tuple(map(int,eng.terminal[target])))
                    check=verify_certificate(instance,cert);check.assert_valid()
                    actual=F(instance.optimal_welfare(),instance.welfare(cert.terminal_counts))
                    if actual>best:
                        best=actual
                        proof={'seed':args.seed,'iteration':iteration,'ratio':str(best),'instance':instance.to_dict(),'strategy':cert.to_dict(),'verified_histories':check.checked_histories,'verified_deviations':check.checked_deviations,'source':'64-atom indexed relaxation projected to fixed10+opt5 themes; replies recomputed in actual catalog'}
                        (HERE/('projection_symmetric_m5p15_best.json' if args.symmetric else 'projection_m5p15_best.json')).write_text(json.dumps(proof,indent=2)+'\n')
                        print(json.dumps({'iteration':iteration,'new_exact_best':str(best),'rows':len(G),'dag_nodes':len(policy),'elapsed':round(time.monotonic()-start,2)}),flush=True)
        report={'parameters':vars(args),'best_exact_ratio':str(best),'records':records,'elapsed':round(time.monotonic()-start,2),'limitation':'Finite sparse-support and randomly aligned projections only; obstruction replies are not preserved; no universal conclusion.'}
        (HERE/('projection_symmetric_m5p15_run.json' if args.symmetric else 'projection_m5p15_run.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'best':str(best),'elapsed':round(time.monotonic()-start,2)}),flush=True)

if __name__=='__main__':main()
