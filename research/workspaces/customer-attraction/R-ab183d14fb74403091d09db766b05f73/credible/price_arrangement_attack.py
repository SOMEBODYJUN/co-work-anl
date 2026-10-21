"""Complete fractional-query arrangement for one full ordered-history SPE cone.

The query list is exhaustive for p<=5. No universal claim is made about policies.
Every reported positive point is recovered over Fraction and replayed over every
ordered history by the canonical verifier. Zero-mass duplicate themes are allowed
only as candidate points; the physical-catalog quotient is explicitly reported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,permutations
import sys,importlib.util,json,time,argparse
import numpy as np
from scipy.optimize import linprog
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction import Instance,CustomerType,ExactSPESolver,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import StrategyCone,payoff_row,dot,integer_clones,independently_verify
SRC=ROOT/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/credible_search/iterative_search.py'
spec=importlib.util.spec_from_file_location('arr_prior',SRC);prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)

def queries(p):
    """All vertices of the subset-sum arrangement in [0,1]^p.

    On each cell C(z)-t sum z is linear. Its maximum is at a vertex.
    Positive support s has s independent active subset sums =1; upper box
    constraints are singleton subset sums. Enumerate those exactly, with
    permutation symmetry used solely for generating the query set.
    """
    patterns={(F(0),)*p}
    for s in range(1,p+1):
        I=np.array([[int(mask>>a&1) for a in range(s)] for mask in range(1,1<<s)])
        for rows in combinations(range(len(I)),s):
            A=I[list(rows)]
            try:flt=np.linalg.solve(A,np.ones(s))
            except np.linalg.LinAlgError:continue
            if min(flt)>1e-8 and max(flt)<=1+1e-8:
                z=tuple(F(float(x)).limit_denominator(100000) for x in flt)
                if all(sum(F(int(c))*x for c,x in zip(row,z))==1 for row in A):
                    patterns.add(tuple(sorted(z,reverse=True))+(F(0),)*(p-s))
    return sorted({z for pat in patterns for z in permutations(pat)}),sorted(patterns)

def exact_export(cone,r,topic,Z):
    vals=tuple(F(float(x)).limit_denominator(10**7) for x in r)
    if not cone.verify(vals) or dot(cone.welfare,vals)!=1:vals=cone.recover_vertex(r)
    if vals is None or not cone.verify(vals) or dot(cone.welfare,vals)!=1:return None
    clones=integer_clones(vals)
    if not independently_verify(cone,clones):raise AssertionError('independent tree replay')
    game=Instance(tuple(f'T{a}' for a in range(cone.topics)),tuple(CustomerType(frozenset(a for a in range(cone.topics) if mask>>a&1),n) for mask,n in enumerate(clones,1) if n),cone.players)
    cert=StrategyCertificate(cone.actions,cone.root);check=verify_certificate(game,cert);check.assert_valid()
    U=game.topic_payoffs(cone.root)[topic];W=game.welfare(cone.root)
    C=sum(F(n)*min(F(1),sum(Z[a] for a in range(cone.topics) if mask>>a&1)) for mask,n in enumerate(clones,1))
    supports=[frozenset(i for i,c in enumerate(game.customers) if a in c.topics) for a in range(cone.topics)]
    return {'instance':game.to_dict(),'certificate':cert.to_dict(),'attacked_topic':topic,'u':str(U),'W':W,'OPT':game.optimal_welfare(),'z':[str(x) for x in Z],'Bz':str(C-U*sum(Z)),'Bz_minus_W':str(C-U*sum(Z)-W),'Bz_plus_u_minus_W':str(C-U*(sum(Z)-1)-W),'histories':check.checked_histories,'deviations':check.checked_deviations,'physical_topics':len(set(supports))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=5);ap.add_argument('--players',type=int,default=3);ap.add_argument('--rounds',type=int,default=8);ap.add_argument('--seed',type=int,default=102106);ap.add_argument('--discount',type=int,default=1);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    start=time.monotonic();s=prior.Search(args.topics,args.players,args.seed);Zs,pats=queries(s.p);C=np.minimum(1,np.array(Zs,float)@s.I.T);taus=np.array(Zs,float).sum(axis=1)
    queue=list(prior.seeds(s.p,s.m));records=[];best=-1e100;selected=None
    for step in range(args.rounds):
        label,r=queue[step] if step<len(queue) else s.rng.choice(queue)
        if step>=3:
            r=r.copy()
            for _ in range(3):r[s.rng.randrange(len(r))]+=.1*max(r.max(),1)
        s.solve(r);targets=list(s.R[s.root]);target=min(targets,key=lambda t:min(s.U[t,a] for a,c in enumerate(s.Q[t]) if c)/s.W[t]);topic=min((a for a,c in enumerate(s.Q[target]) if c),key=lambda a:s.U[target,a])
        actions,A=s.policy(int(target),['min','max','lowW','highW','uniform'][step%5]);local=None
        # Each LP is exact in r for fixed query; queries cover all fractional z.
        for j,Z in enumerate(Zs):
            gain=C[j]-(taus[j]-args.discount)*s.pay[target,topic]-s.w[target]
            out=linprog(-gain,A_ub=-A,b_ub=np.zeros(len(A)),A_eq=s.w[[target]],b_eq=[1],bounds=(0,None),method='highs')
            if out.success and (local is None or out.fun<local[0].fun):local=(out,j)
        out,j=local;value=-out.fun;queue.append((f'LP{step}',out.x))
        record={'step':step,'source':label,'root':s.Q[target],'topic':topic,'max_gap_per_W':value,'queries':len(Zs),'elapsed':time.monotonic()-start};records.append(record);print(json.dumps(record),flush=True)
        if value>best+1e-8:
            best=value;cone=StrategyCone(s.p,s.m,actions);selected=exact_export(cone,out.x,topic,Zs[j])
        report={'scope':'all fractional queries within each selected complete strategy cone; policies sampled only','players':s.m,'topics':s.p,'query_patterns':[[str(x) for x in pat] for pat in pats],'queries':len(Zs),'discount':args.discount,'records':records,'selected':selected,'universal_result':False}
        args.output.write_text(json.dumps(report,indent=2)+'\n')
        if value>1e-7 and selected is not None:return
if __name__=='__main__':main()
