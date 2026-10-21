"""Explicit active/saturated modes plus arbitrary exact BI fallback.

Only finite invocations are computational evidence.  The all-k proof is in
all_k_padding.md.  Everything written by this script stays in this workspace.
"""
from fractions import Fraction as F
from functools import lru_cache
import argparse
import json
from pathlib import Path
from customer_attraction import CustomerType, Instance, ExactSPESolver

CORE = (({0},4),({1},4),({2},2),({2,3},2),({2,4},2),({0,3,4},6),({1,3,4},2))
SAT = {(0,1,3),(0,1,4),(0,2,3),(0,2,4),(0,3,4)}
PAIR_ACTION = {(0,0):1,(0,1):3,(0,2):3,(0,3):4,(0,4):3,
               (1,3):0,(1,4):0,(2,3):0,(2,4):0}

def instance(k):
    if not isinstance(k,int) or k<1: raise ValueError('k must be a positive integer')
    return Instance(('A','B','T','D','E','P'),tuple(CustomerType(frozenset(s),n) for s,n in CORE)+
                    (CustomerType(frozenset({5}),5*k),),k+3)

def increment(c,a): return c[:a]+(c[a]+1,)+c[a+1:]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('k',type=int)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    k=args.k;inst=instance(k);solver=ExactSPESolver(inst);m=k+3
    states=[];index={};arcs={};actions={};ends={}
    def fallback(c):return ('F',c,min(solver.outcomes(c)))
    def child_mode(mode,c,a):
        core=mode[1];p=c[5];t=len(core)
        if a==5:
            return ('S',core) if p<k else fallback(increment(c,a))
        if t==0:return ('S',(a,))
        if t==1:
            b=core[0]
            if b==0:
                if a==0:return ('S',(0,0)) if p==k else fallback(increment(c,a))
                return ('S',tuple(sorted((b,a))))
            if a==0 or (b in (1,2) and a in (3,4)):
                return ('S',tuple(sorted((b,a))))
            return fallback(increment(c,a))
        if t==2:
            if a==PAIR_ACTION[core]:return ('S',tuple(sorted(core+(a,))))
            return fallback(increment(c,a))
        return fallback(increment(c,a))
    def build(c,mode):
        state=(c,mode)
        if state in index:return index[state]
        sid=len(states);index[state]=sid;states.append(state)
        if sum(c)==m:ends[sid]=c;return sid
        if mode[0]=='F':
            _,_,target=mode;floor=solver.threshold(c)
            legal=[a for a in range(6) if target in solver.outcomes(increment(c,a)) and inst.topic_payoff(a,target)>=floor]
            chosen=legal[0];children=[]
            for a in range(6):
                cc=increment(c,a)
                tt=target if a==chosen else min(solver.outcomes(cc),key=lambda z:(inst.topic_payoff(a,z),z))
                children.append(build(cc,('F',cc,tt)))
        else:
            core=mode[1];p=c[5]
            if len(core)==0 or core==(0,):chosen=5 if p<k else 0
            elif len(core)==1:chosen=0
            elif len(core)==2:chosen=PAIR_ACTION[core]
            else:
                assert core in SAT,(c,core)
                chosen=5
            children=[build(increment(c,a),child_mode(mode,c,a)) for a in range(6)]
        actions[sid]=chosen;arcs[sid]=tuple(children);ends[sid]=ends[children[chosen]]
        return sid
    root=build((0,)*6,('S',()))
    comparisons=0;slack=None
    for sid,children in arcs.items():
        c,mode=states[sid];chosen=actions[sid];actual=ends[sid]
        for a,cid in enumerate(children):
            assert states[cid][0]==increment(c,a)
            delta=inst.topic_payoff(chosen,actual)-inst.topic_payoff(a,ends[cid])
            assert delta>=0,(sid,c,mode,chosen,a,actual,ends[cid],delta)
            comparisons+=1;slack=delta if slack is None else min(slack,delta)
    sid=root;path=[]
    while sid in arcs:
        a=actions[sid];path.append(a);sid=arcs[sid][a]
    assert path==[5]*k+[0,0,1]
    target=ends[root];alpha=F(m-1,m)
    load=[sum(target[a] for a in c.topics) for c in inst.customers]
    g=[sum((F(c.multiplicity)/(1+alpha*h) for c,h in zip(inst.customers,load) if a in c.topics),F(0)) for a in range(6)]
    G=sum((F(c.multiplicity)/(1+alpha*h) for c,h in zip(inst.customers,load) if h),F(0))
    W=inst.welfare(target);opt=inst.optimal_welfare();gap=m*max(g)-W-G
    report={'k':k,'players':m,'instance':inst.to_dict(),'path':path,'terminal':target,'welfare':W,'optimum':opt,
            'nodes':len(states),'decision_nodes':len(arcs),'comparisons':comparisons,'minimum_slack':str(slack),
            'M':str(max(g)),'G':str(G),'refined_tax_gap':str(gap),'g':[str(x) for x in g],
            'scope':'finite exact audit of explicit special-mode policy and BI fallback; all-k proof is analytic'}
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
