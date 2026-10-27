"""Direct n=6 target attack on 18 labels and a fixed 117-type support.

A count policy defines actions at EVERY ordered history. Lazy constraint
generation checks every count-policy IC before accepting a floating point.
No numerical non-counterexample is a universal result. A ratio above two
would still require rational recovery and independent exact IC verification.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import argparse,json,time
import numpy as np
from scipy.optimize import linprog


def compositions(n,k):
    if k==1:
        yield (n,);return
    for first in range(n+1):
        for tail in compositions(n-first,k-1):
            yield (first,)+tail


def materialize(path):
    data=json.loads(path.read_text()); types=[];weights=[]
    for (mask,d,ell,h),value in data['positive_types']:
        for subset in combinations(range(6),d):
            t=sum(1<<i for i in subset)
            reply=0 if ell==0 else (t if (ell,h)==(d,d) else (63^t if (ell,h)==(6-d,0) else 63))
            types.append([(mask>>i)&1 for i in range(6)]+[(t>>i)&1 for i in range(6)]+[(reply>>i)&1 for i in range(6)])
            weights.append(float(F(value)/comb(6,d)))
    return np.array(types,dtype=np.int16),np.array(weights)


class Attack:
    def __init__(self,bits):
        self.bits=bits; self.k=18
        self.levels=[list(compositions(depth,18)) for depth in range(7)]
        states=[q for level in self.levels for q in level]
        self.nonterm=sum(len(level) for level in self.levels[:-1])
        self.stateid={q:i for i,q in enumerate(states)}
        self.child=np.array([[self.stateid[q[:a]+(q[a]+1,)+q[a+1:]] for a in range(18)]
                             for q in states[:self.nonterm]],dtype=np.int32)
        self.final=np.array(self.levels[-1],dtype=np.int16)
        load=self.final@bits.T
        self.inv60=(60//np.maximum(load,1)).astype(np.int16)
        self.cover=(load>0).astype(np.int8)
        self.price_columns=False
        print('nonterminal',self.nonterm,'final',len(self.final),'types',len(bits),flush=True)

    def profits(self,w):
        return (self.inv60*w[None,:])@self.bits

    def policy(self,w,rng):
        profits=self.profits(w); welfare=self.cover@w
        terminal=np.empty(self.nonterm+len(self.final),dtype=np.int32)
        terminal[self.nonterm:]=np.arange(len(self.final),dtype=np.int32)
        actions=np.empty(self.nonterm,dtype=np.int16)
        for sid in range(self.nonterm-1,-1,-1):
            leaves=terminal[self.child[sid]]
            vals=profits[leaves,np.arange(18)]
            possible=np.flatnonzero(vals>=max(vals)-1e-7)
            if rng.random()<.7:
                ww=welfare[leaves[possible]]
                possible=possible[ww<=min(ww)+1e-9]
            chosen=int(rng.choice(possible))
            actions[sid]=chosen;terminal[sid]=leaves[chosen]
        return actions,terminal

    def menu_dag(self,w,rng,cap):
        """Restricted set-valued BI; every retained outcome has a true witness."""
        profit=self.profits(w);welfare=self.cover@w
        menus=[None]*self.nonterm;threshold=np.empty(self.nonterm)
        def menu(sid):
            return menus[sid] if sid<self.nonterm else np.array([sid-self.nonterm],dtype=np.int32)
        for sid in range(self.nonterm-1,-1,-1):
            kids=[menu(int(child)) for child in self.child[sid]]
            floor=np.array([min(profit[kid,a]) for a,kid in enumerate(kids)])
            threshold[sid]=max(floor)
            possible=np.unique(np.concatenate([kid[profit[kid,a]>=threshold[sid]-1e-7] for a,kid in enumerate(kids)]))
            if len(possible)>cap:
                low=possible[np.argsort(welfare[possible])[:max(1,cap//2)]]
                other=possible[~np.isin(possible,low)]
                chosen=rng.choice(other,min(cap-len(low),len(other)),replace=False)
                possible=np.concatenate([low,chosen])
            menus[sid]=possible.astype(np.int32)
        desired=int(menus[0][np.argmin(welfare[menus[0]])])
        pair_index={(0,desired):0};pairs=[(0,desired)];actions=[];targets=[];next_leaves=[]
        cursor=0
        while cursor<len(pairs):
            sid,target=pairs[cursor];kids=[menu(int(child)) for child in self.child[sid]]
            eligible=[a for a,kid in enumerate(kids) if target in kid and profit[target,a]>=threshold[sid]-1e-7]
            action=int(rng.choice(eligible));chosen=[]
            for a,kid in enumerate(kids):
                child_target=target if a==action else int(kid[np.argmin(profit[kid,a])])
                chosen.append(child_target);child_sid=int(self.child[sid,a])
                if child_sid<self.nonterm and (child_sid,child_target) not in pair_index:
                    pair_index[(child_sid,child_target)]=len(pairs);pairs.append((child_sid,child_target))
            actions.append(action);targets.append(target);next_leaves.append(chosen);cursor+=1
        print('credible_DAG_nodes',len(pairs),'menu_cap',cap,flush=True)
        return np.array(actions,dtype=np.int16),np.array(targets,dtype=np.int32),np.array(next_leaves,dtype=np.int32),np.array(pairs,dtype=np.int32)

    def row(self,key):
        a,src,b,dst=key
        return self.bits[:,b]*self.inv60[dst]-self.bits[:,a]*self.inv60[src]

    def price(self,result,ordered_keys,root,limit=24):
        coefficients={}
        for key,dual in zip(ordered_keys,result.ineqlin.marginals):
            if abs(dual)<1e-10:continue
            a,src,b,dst=key
            coefficients[(dst,b)]=coefficients.get((dst,b),0)+dual
            coefficients[(src,a)]=coefficients.get((src,a),0)-dual
        masks=np.arange(1,1<<18,dtype=np.int32)
        rootmask=sum(1<<a for a,v in enumerate(self.final[root]) if v)
        reduced=-(((masks>>6)&63)>0).astype(float)-float(result.eqlin.marginals[0])*((masks&rootmask)>0)
        for (leaf,action),coefficient in coefficients.items():
            if abs(coefficient)<1e-10:continue
            load=np.zeros(len(masks),dtype=np.int16)
            for a,count in enumerate(self.final[leaf]):
                if count:load+=int(count)*((masks>>a)&1).astype(np.int16)
            reduced-=coefficient*((masks>>action)&1)*(60//np.maximum(load,1))
        existing=np.array([sum(int(b)<<a for a,b in enumerate(row)) for row in self.bits],dtype=np.int32)
        assert np.min(reduced[existing-1])>=-1e-5, 'dual pricing sign or numerical failure'
        reduced[existing-1]=np.inf
        bad=np.flatnonzero(reduced < -1e-7)
        if not len(bad):return 0,float(np.min(reduced))
        bad=bad[np.argsort(reduced[bad])[:limit]]
        newmasks=masks[bad]
        newbits=np.array([[(int(mask)>>a)&1 for a in range(18)] for mask in newmasks],dtype=np.int16)
        load=self.final@newbits.T
        self.inv60=np.hstack([self.inv60,(60//np.maximum(load,1)).astype(np.int16)])
        self.cover=np.hstack([self.cover,(load>0).astype(np.int8)])
        self.bits=np.vstack([self.bits,newbits])
        return len(bad),float(np.min(reduced))

    def optimize(self,actions,terminal,rng,max_cuts):
        leaves=terminal[self.child]
        return self.optimize_arrays(actions,terminal[:self.nonterm],leaves,rng,max_cuts)

    def optimize_arrays(self,actions,terminal,leaves,rng,max_cuts):
        keys=set(); ordered_keys=[];root=int(terminal[0]);rows=[];nodes=len(actions);price_rounds=0
        def insert(sid,alt):
            key=(int(actions[sid]),int(terminal[sid]),int(alt),int(leaves[sid,alt]))
            if key not in keys:
                keys.add(key);ordered_keys.append(key);rows.append(self.row(key))
        for sid in [0]+list(map(int,rng.choice(nodes,min(nodes,32),replace=False))):
            for alt in range(18):insert(sid,alt)
        for iteration in range(max_cuts):
            objective=(self.bits[:,6:12].sum(axis=1)>0).astype(float)
            result=linprog(-objective,A_ub=np.array(rows,dtype=float),b_ub=np.zeros(len(rows)),
                           A_eq=self.cover[root:root+1],b_eq=[1],bounds=(0,None),method='highs')
            if not result.success:
                return None,{'status':result.message,'rows':len(rows)}
            profit=self.profits(result.x)
            actual=profit[terminal,actions]
            violations=profit[leaves,np.arange(18)[None,:]]-actual[:,None]
            bad=np.flatnonzero(violations.ravel()>1e-7)
            if not len(bad):
                if self.price_columns and price_rounds<8:
                    added,minimum=self.price(result,ordered_keys,root)
                    print('customer_pricing','added',added,'minimum_reduced_cost',minimum,'types',len(self.bits),flush=True)
                    price_rounds+=1
                    if added:
                        rows=[self.row(key) for key in ordered_keys]
                        continue
                return result.x,{'status':'all_policy_IC_checked_float','rows':len(rows),'ratio':float(-result.fun),
                                 'maximum_scaled60_violation':float(np.max(violations)),'cut_iterations':iteration+1,
                                 'actual_terminal':self.final[root].tolist(),'customer_types':len(self.bits),'pricing_rounds':price_rounds}
            if len(bad)>1500:
                vals=violations.ravel()[bad]
                bad=bad[np.argpartition(vals,-1500)[-1500:]]
            before=len(rows)
            for index in bad:insert(int(index//18),int(index%18))
            print('cut',iteration,'ratio',-result.fun,'violations',len(bad),'rows',len(rows),flush=True)
            if len(rows)==before:
                return None,{'status':'numerical_stall','rows':len(rows)}
        return None,{'status':'cut_budget_incomplete','rows':len(rows)}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--steps',type=int,default=5)
    parser.add_argument('--max-cuts',type=int,default=35);parser.add_argument('--menus',type=int,default=1)
    parser.add_argument('--price',action='store_true');args=parser.parse_args()
    root=Path(__file__).parent; rng=np.random.default_rng(65650)
    bits,w=materialize(root/'potential_menu_joint_private.json')
    engine=Attack(bits);engine.price_columns=args.price;records=[];best=0
    for step in range(args.steps):
        started=time.time()
        if args.menus>1:
            actions,terminal,children,pairs=engine.menu_dag(w,rng,args.menus)
            solution,record=engine.optimize_arrays(actions,terminal,children,rng,args.max_cuts)
        else:
            actions,terminal=engine.policy(w,rng)
            solution,record=engine.optimize(actions,terminal,rng,args.max_cuts)
        record['step']=step;record['seconds']=time.time()-started;records.append(record)
        print('STEP',json.dumps(record),flush=True)
        if solution is None:break
        if record['ratio']>best:
            best=record['ratio']
            # This is a compact full-history policy via count lookup, still floating discovery.
            if args.menus>1:
                filename='large_catalog_menu_priced_best_discovery.npz' if args.price else 'large_catalog_menu_best_discovery.npz'
                np.savez_compressed(root/filename,bits=engine.bits,weights=solution,
                                    actions=actions,targets=terminal,children=children,pairs=pairs,
                                    actual_terminal=engine.final[terminal[0]])
            else:
                filename='large_catalog_priced_best_discovery.npz' if args.price else 'large_catalog_best_discovery.npz'
                np.savez_compressed(root/filename,bits=engine.bits,weights=solution,
                                    actions=actions,actual_terminal=engine.final[terminal[0]])
        if record['ratio']>2+1e-7:
            print('STRICT_FLOAT_TARGET_CANDIDATE_NEEDS_EXACT_RECOVERY',flush=True);break
        w=solution
        # A tiny legal perturbation changes tied selectors before the next cone.
        if step%2:w=w+1e-6*rng.random(len(w))
    stem=('large_catalog_menu_priced_target_attack.json' if args.price else 'large_catalog_menu_target_attack.json') if args.menus>1 else ('large_catalog_priced_target_attack.json' if args.price else 'large_catalog_target_attack.json')
    (root/stem).write_text(json.dumps({'scope':'finite true SPE-policy cones, floating discovery only',
               'seed':65650,'menu_cap':args.menus,'records':records,'largest_discovered_ratio':best},indent=2)+'\n')


if __name__=='__main__':main()
