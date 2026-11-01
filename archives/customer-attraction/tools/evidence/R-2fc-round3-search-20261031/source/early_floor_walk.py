"""Finite full-history SPE cone attack on early-player OPT/(2m-1) floor.

Every constraint uses an actual complete policy. Floating BI/LP propose only;
new best points are recovered with Fraction and canonical all-history checked.
This is not a general upper-bound certificate or a proof of the floor.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, random, sys, time
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
SRC=ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
old=load('early_floor_engine',SRC/'counterexample_search/cone_walk.py')
recovery=load('early_floor_recovery',SRC/'global_proof/individual_face_walk.py')

def path_for(eng,target,position,rng):
    """Among actual SPE-compatible on-path sequences, minimize this player's u."""
    nodes=[((),0)]
    for depth in range(position+1):
        choices=[]
        for h,sid in nodes:
            for a,cid in enumerate(eng.children[depth][sid]):
                if target in eng.R[depth+1][cid] and eng.u[target,a]>=eng.floor[depth][sid]-eng.eps:
                    choices.append((h+(a,),int(cid)))
        if not choices:return None
        if depth==position:
            low=min(eng.u[target,h[-1]] for h,sid in choices)
            return rng.choice([(h,sid) for h,sid in choices if eng.u[target,h[-1]]<=low+eng.eps])[0]
        nodes=choices

def policy_for(eng,target,prefix,rng,mode):
    """Reconstruct complete unmerged ordered histories with selected path prefix."""
    actions={};rows=[]
    def rec(h,depth,sid,dest):
        if depth==eng.m:return dest
        admissible=[a for a,cid in enumerate(eng.children[depth][sid])
                    if dest in eng.R[depth+1][cid] and eng.u[dest,a]>=eng.floor[depth][sid]-eng.eps]
        a=prefix[depth] if h==prefix[:depth] and depth<len(prefix) else rng.choice(admissible)
        assert a in admissible
        actions[h]=a;children=[]
        for b,cid in enumerate(eng.children[depth][sid]):
            if b==a:chosen=dest
            else:
                C=eng.R[depth+1][cid];v=eng.u[C,b];low=v.min()
                ties=C[v<=low+eng.eps]
                if mode!='random' and len(ties)>1:
                    value=eng.u[ties,prefix[-1]]
                    extreme=value.min() if mode=='min-attacker' else value.max()
                    ties=ties[np.abs(value-extreme)<=eng.eps]
                chosen=int(rng.choice(list(ties)))
            children.append(rec(h+(b,),depth+1,int(cid),chosen))
        actual=children[a]
        for b in range(eng.p):
            if b!=a:rows.append(eng.pay[actual,a]-eng.pay[children[b],b])
        return actual
    assert rec((),0,0,target)==target
    G=np.unique(np.array(rows,dtype=np.int16),axis=0)
    return actions,G[np.any(G,axis=1)]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=4)
    ap.add_argument('--topics',type=int,default=6);ap.add_argument('--steps',type=int,default=50)
    ap.add_argument('--position',type=int,default=0);ap.add_argument('--seed',type=int,default=2026102133)
    ap.add_argument('--seconds',type=float,default=120);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--min-support',type=int,default=1)
    ap.add_argument('--mode',choices=['random','min-attacker','max-attacker'],default='random')
    ap.add_argument('--start-json',type=Path,action='append',default=[])
    args=ap.parse_args();rng=random.Random(args.seed);m,p=args.players,args.topics
    assert args.position<m-2,'last-two floor already proved; attack earlier positions'
    eng=old.Engine(m,p,rng);started=time.monotonic();best=F(0);endpoints=[];records=[];seen=set()
    seeds=[old.baseline(m,p)]
    for source in args.start_json:
        obj=json.loads(source.read_text());inst=obj.get('instance') or obj['exact_symmetric_candidate']['instance']
        assert inst['players']==m and len(inst['topics'])==p
        r=[0]*len(eng.masks)
        for row in inst['customers']:r[sum(1<<a for a in row['topics'])-1]+=row['multiplicity']
        seeds.append(r)
    # Large private outside themes plus directed overlaps; broad dense types make
    # the floor slack, so sample chiefly sparse overlap perturbations.
    for j in range(min(12,args.steps-1)):
        r=np.array(old.baseline(m,p),dtype=float)*rng.choice([1,3,10])
        for k in range(rng.randrange(1,7)):
            B=rng.sample(range(p),rng.choice([2,2,3,min(p,4)]));mask=sum(1<<a for a in B)
            r[mask-1]+=rng.randint(1,15)
        seeds.append(r.tolist())
    for step in range(args.steps):
        if time.monotonic()-started>args.seconds:break
        if seeds:r=seeds.pop(0)
        elif endpoints:
            r=np.array(rng.choice(endpoints),dtype=float)*rng.choice([1,5,20])
            for j in range(rng.randrange(1,5)):r[rng.randrange(len(r))]+=rng.random()*.02
        else:break
        eng.solve(r);outcomes=eng.R[0][0]
        ranked=[]
        for target in outcomes:
            if sum(eng.terminal[target]>0)<args.min_support:continue
            prefix=path_for(eng,int(target),args.position,rng)
            if prefix is not None:ranked.append((eng.u[target,prefix[-1]],int(target),prefix))
        if not ranked:
            records.append({'step':step,'no_root_with_required_support':True})
            continue
        low=min(t[0] for t in ranked);_,target,prefix=rng.choice([t for t in ranked if t[0]<=low+eng.eps])
        mode=args.mode if step%3 else 'random'
        actions,G=policy_for(eng,target,prefix,rng,mode);a=prefix[-1]
        key=hashlib.sha256(repr(sorted(actions.items())).encode()).hexdigest()
        if key in seen:continue
        seen.add(key);norm=eng.pay[target,a]
        jids=list(dict.fromkeys([int(np.argmax(eng.v@np.asarray(r))),rng.randrange(len(eng.portfolios))]))
        for jid in jids:
            res=linprog(-eng.v[jid].astype(float),A_ub=-G.astype(float),b_ub=np.zeros(len(G)),
                        A_eq=[norm.astype(float)],b_eq=[1.],bounds=(0,None),method='highs')
            if not res.success:continue
            x=res.x;value=float(max(eng.v@x)*eng.L);endpoints.append(x.tolist())
            row={'step':step,'root':eng.terminal[target].tolist(),'prefix':prefix,'attacked_topic':a,
                 'ratio_proposal':value,'rows':len(G),'portfolio':eng.portfolios[jid],'cone_sha256':key}
            records.append(row)
            if value>float(best)+1e-8:
                clones=recovery.recover(G,norm,x)
                if clones is None:row['exact_recovery']=False;continue
                inst,cert=old.verify_canonical(m,p,clones,list(actions.items()),eng.terminal[target].tolist())
                q=tuple(map(int,eng.terminal[target]));u=inst.topic_payoff(a,q);O=inst.optimal_welfare();ratio=F(O,u)
                row['exact_ratio']=str(ratio)
                if ratio>best:
                    best=ratio
                    point={'scope':'one genuine complete-history pure SPE; finite early floor attack only',
                           'parameters':{**vars(args),'output':str(args.output),'start_json':list(map(str,args.start_json))},'step':step,'ratio':str(ratio),
                           'attacked_position':args.position,'attacked_topic':a,'u':str(u),'W':inst.welfare(q),
                           'OPT':O,'instance':inst.to_dict(),'strategy':cert.to_dict(),'full_strategy_verified':True}
                    args.output.with_suffix('.best.json').write_text(json.dumps(point,indent=2)+'\n')
                    print(json.dumps({'step':step,'best':str(best),'threshold':2*m-1,'elapsed':round(time.monotonic()-started,3)}),flush=True)
            if best>2*m-1:break
        report={'scope':'finite full-history SPE cones; absence of counterexample is not proof',
                'parameters':{**vars(args),'output':str(args.output),'start_json':list(map(str,args.start_json))},'finished_steps':step+1,
                'elapsed':time.monotonic()-started,'cones':len(seen),'best':str(best),'records':records}
        args.output.write_text(json.dumps(report,indent=2)+'\n')
        if best>2*m-1:break
    print(json.dumps({k:v for k,v in report.items() if k!='records'}),flush=True)

if __name__=='__main__':main()
