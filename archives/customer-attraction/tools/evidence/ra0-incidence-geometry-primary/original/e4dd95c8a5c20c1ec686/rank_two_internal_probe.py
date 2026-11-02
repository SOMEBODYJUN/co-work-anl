"""Exact seeded probe of maximal-incidence rank two with subtheme actions."""
from fractions import Fraction
from itertools import combinations,combinations_with_replacement
import argparse,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def main():
    p=argparse.ArgumentParser();p.add_argument('--cases',type=int,default=3000)
    p.add_argument('--seed',type=int,default=413017)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    rng=random.Random(args.seed)
    report={'cases':0,'requested_cases':args.cases,'seed':args.seed,
            'maxima_range':[3,5],'players_range':[3,4],
            'internal_subthemes':2,'root_theta_failures':[],
            'aggregate_theta_failures':[]}
    for case in range(args.cases):
        s=rng.randrange(3,6);n=rng.randrange(3,5)
        # Positive private blocks keep every base maximum distinct and maximal.
        units=[]
        for k in [1,2]:
            for support in combinations(range(s),k):
                mass=(rng.choice([1,2,3,5,8]) if k==1
                      else rng.choice([0,0,1,2,3,5,8]))
                units.extend([frozenset(support)]*mass)
        containers=[rng.randrange(s) for _ in range(2)]
        cs=[]
        for b in units:
            active=set(b)
            for j,a in enumerate(containers):
                if a in b and rng.randrange(2):active.add(s+j)
            cs.append(CustomerType(frozenset(active)))
        instance=Instance(tuple(map(str,range(s+2))),tuple(cs),n)
        solver=ExactSPESolver(instance);root=solver.outcomes()
        th=min(max(sum((Fraction(c.multiplicity,
                          1+sum(h.count(b) for b in c.topics))
                          for c in cs if a in c.topics),Fraction())
                   for a in range(s))
               for h in combinations_with_replacement(range(s),n-1))
        threshold=solver.threshold((0,)*(s+2))
        minimum=min(instance.welfare(q) for q in root)
        info={'case':case,'instance':instance.to_dict(),
              'containers':containers,'theta':str(th),
              'root_threshold':str(threshold),'minimum_welfare':minimum}
        if threshold<th:report['root_theta_failures'].append(info)
        if minimum<n*th:report['aggregate_theta_failures'].append(info)
        report['cases']+=1
        if report['root_theta_failures'] or report['aggregate_theta_failures']:break
    with args.output.open('x') as f:json.dump(report,f,indent=2)

if __name__=='__main__':main()
