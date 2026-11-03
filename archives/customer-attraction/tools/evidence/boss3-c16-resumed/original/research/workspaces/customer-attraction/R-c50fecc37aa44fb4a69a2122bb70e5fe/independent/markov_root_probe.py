"""Exact reverse-DAG enumeration of count-Markov pure SPE policies.

This differs from ExactSPESolver: every count state has one shared successor,
including when distinct ordered histories merge. Finite evidence only.
"""
import argparse, itertools, json, random, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance, CustomerType, ExactSPESolver

def counts_of(k, t):
    if k == 1:
        yield (t,)
    else:
        for j in range(t+1):
            for tail in counts_of(k-1,t-j):
                yield (j,)+tail

def increment(p,a):
    return p[:a]+(p[a]+1,)+p[a+1:]

def markov_outcomes(instance, cap=1000000):
    k,m=instance.topic_count, instance.players
    states=[p for t in range(m-1,-1,-1) for p in counts_of(k,t)]
    terminal={p:p for p in counts_of(k,m)}
    payoff={p:instance.topic_payoffs(p) for p in terminal}
    found=set(); branches=0; stop=False
    allout=ExactSPESolver(instance).outcomes()
    def visit(i):
        nonlocal branches,stop
        if stop:return
        if i==len(states):
            found.add(terminal[(0,)*k]);branches+=1
            if found==allout or branches>=cap:stop=True
            return
        p=states[i]
        child=[terminal[increment(p,a)] for a in range(k)]
        best=max(payoff[q][a] for a,q in enumerate(child))
        # Different optimal actions giving identical outcomes induce the same
        # outcome map and can be quotient out for outcome-set enumeration.
        candidates={q for a,q in enumerate(child) if payoff[q][a]==best}
        for q in candidates:
            terminal[p]=q
            visit(i+1)
            if stop:break
    visit(0)
    return found,branches,(not stop or found==allout)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--samples',type=int,default=1000);parser.add_argument('--topics',type=int,default=3);parser.add_argument('--players',type=int,default=3);parser.add_argument('--seed',type=int,default=816);parser.add_argument('--cap',type=int,default=1000000);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    rng=random.Random(args.seed);checked=0;skipped=0;worst=0
    for j in range(args.samples):
        customers=tuple(CustomerType(frozenset(a for a in range(args.topics) if mask>>a&1),r) for mask in range(1,1<<args.topics) if (r:=rng.randrange(5)))
        ins=Instance(tuple(chr(65+a) for a in range(args.topics)),customers,args.players)
        unrestricted=ExactSPESolver(ins).outcomes()
        markov,branches,complete=markov_outcomes(ins,args.cap);worst=max(worst,branches)
        if not complete:skipped+=1;continue
        checked+=1
        if markov!=unrestricted:
            missing=sorted(unrestricted-markov)
            result={'status':'counterexample','sample':j,'instance':ins.to_dict(),'all_history_outcomes':sorted(unrestricted),'markov_outcomes':sorted(markov),'missing':missing,'all_history_certificate':ExactSPESolver(ins).certificate(missing[0]).to_dict(),'markov_policies_quotiented':branches}
            args.output.write_text(json.dumps(result,indent=2));print(json.dumps({'status':result['status'],'sample':j,'missing':missing,'branches':branches}));return
    result={'status':'finite_no_counterexample','samples':args.samples,'checked':checked,'skipped':skipped,'max_quotient_policies':worst,'topics':args.topics,'players':args.players,'seed':args.seed,'cap':args.cap}
    args.output.write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
