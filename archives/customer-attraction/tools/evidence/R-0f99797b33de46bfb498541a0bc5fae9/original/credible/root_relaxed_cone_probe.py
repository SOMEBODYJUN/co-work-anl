"""All-big plus empty-root cones, with exactly all positive-depth SPE rows.

One finite diagnostic, not an exhaustive strategy or general half proof.
"""
from pathlib import Path
import sys,json,random
from fractions import Fraction as F
from itertools import combinations
import numpy as np
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone,payoff_row,dot,integer_clones,instance_from_clones,serializable
from customer_attraction import ExactSPESolver
HERE=Path(__file__).resolve().parent

def inc(k,a):return tuple(v+int(i==a) for i,v in enumerate(k))
def policy(S,root,rng):
    p=S.instance.topic_count;m=S.instance.players;A={():root}
    def expand(h,k,target):
        if len(h)==m:return
        floor=S.threshold(k)
        options=[a for a in range(p) if target in S.outcomes(inc(k,a)) and S.instance.topic_payoff(a,target)>=floor]
        a=rng.choice(options);A[h]=a;v=S.instance.topic_payoff(a,target)
        for b in range(p):
            child=inc(k,b)
            if b==a:q=target
            else:q=rng.choice([q for q in sorted(S.outcomes(child)) if S.instance.topic_payoff(b,q)<=v])
            expand(h+(b,),child,q)
    for b in range(p):
        k=inc((0,)*p,b);qs=S.outcomes(k)
        if b==root:
            w=min(map(S.instance.welfare,qs));q=rng.choice([q for q in sorted(qs) if S.instance.welfare(q)==w])
        else:q=rng.choice(sorted(qs))
        expand((b,),k,q)
    return A

def main():
    rng=random.Random(231034);reports=[];cones=[]
    for m in (3,4,5):
        p=m+1;weights=[0]*((1<<p)-1);weights[1]=m-1
        for a in range(2,p):weights[(1<<a)-1]=1
        I=instance_from_clones(p,m,weights);S=ExactSPESolver(I)
        for variant in range(2):
            A=policy(S,0,rng);C=StrategyCone(p,m,A)
            rows=set()
            for h,a in A.items():
                if not h:continue
                actual=payoff_row(p,C.terminals[h],a)
                for b in range(p):
                    row=tuple(x-y for x,y in zip(actual,payoff_row(p,C.terminals[h+(b,)],b)))
                    if any(row):rows.add(row)
            C.rows=tuple(sorted(rows));C.matrix=np.array(C.rows,dtype=float)
            cones.append({'m':m,'p':p,'variant':variant,'root_counts':C.root,
                          'actions':[{'history':list(h),'action':a} for h,a in sorted(A.items())]})
            for J in combinations(range(p),m):
                z=C.optimize(J)
                rec={'m':m,'p':p,'variant':variant,'portfolio':J,'rows':len(rows),
                     'status':z['status'],'exact_primal':bool(z.get('certified')),
                     'value':z.get('value'),'exact_optimal_dual':z.get('dual_optimal',False)}
                if z.get('certified'):
                    rec.update(values=z['values'],dual_bound=z.get('dual_bound'),dual_support=z.get('dual_support'))
                if z.get('certified'):
                    clones=integer_clones(z['values']);II=instance_from_clones(p,m,clones)
                    for h,a in A.items():
                        if not h:continue
                        v=II.topic_payoff(a,C.terminals[h])
                        assert all(v>=II.topic_payoff(b,C.terminals[h+(b,)]) for b in range(p))
                    if z['value']>2:
                        vals=[II.topic_payoff(b,C.terminals[(b,)]) for b in range(p)]
                        cert={'scope':'positive-depth-only SPE counterexample; root need not be optimal',
                              'instance':II.to_dict(),'strategy':{'actions':[{'history':list(h),'action':a} for h,a in sorted(A.items())]},
                              'W':II.welfare(C.root),'OPT':II.optimal_welfare(),'root_deviation_payoffs':list(map(str,vals)),
                              'Delta':str(max(vals)-vals[0])}
                        (HERE/'root_relaxed_cone_failure.json').write_text(json.dumps(cert,indent=2)+'\n')
                reports.append(rec)
            print(m,variant,'max=',max(r['value'] for r in reports if r['m']==m and r['variant']==variant and r['exact_primal']),flush=True)
            (HERE/'root_relaxed_cone_probe.json').write_text(json.dumps(serializable({'scope':'Finite all-big+empty-root positive-depth policy cones, exact primal/dual scope only','seed':231034,'cones':cones,'records':reports}),indent=2)+'\n')
if __name__=='__main__':main()
