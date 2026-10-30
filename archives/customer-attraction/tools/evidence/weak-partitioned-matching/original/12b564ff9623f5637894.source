"""Recover and exactly check one policy/portfolio partition-query LP dual."""
from fractions import Fraction as F
from itertools import combinations,permutations
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import Instance,StrategyCertificate
from customer_attraction_strategy_lp import StrategyCone,coverage_row
from probe import optimize


def partition_row(p,path,assignment):
    result=[]
    for mask in range(1,1<<p):
        c=sum(mask>>a&1 for a in path)
        owners=[i for i,a in enumerate(assignment) if mask>>a&1]
        result.append(min((F(1,c+1-(mask>>path[i]&1)) for i in owners),default=F(0)))
    return tuple(result)


def main():
    source=ROOT/'research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json'
    d=json.loads(source.read_text());ins=Instance.from_dict(d['instance']);cert=StrategyCertificate.from_dict(d['certificate'])
    cone=StrategyCone(ins.topic_count,ins.players,dict(cert.actions));target=tuple(d['unique_optimal_supports'][0])
    result,path=optimize(cone,target,0.,'partition')
    if not result.success:raise RuntimeError(result.message)
    p,m=cone.topics,cone.players;n=(1<<p)-1
    optimal=coverage_row(p,target);alternatives=[t for t in combinations(range(p),m) if t!=target]
    hrows=[tuple(x-y for x,y in zip(optimal,coverage_row(p,t))) for t in alternatives]
    assignments=list(permutations(target));rrows=[partition_row(p,path,t) for t in assignments]
    mu=[F(float(-v)).limit_denominator(10**8) for v in result.ineqlin.marginals]
    beta=F(float(-result.eqlin.marginals[0])).limit_denominator(10**8)
    gi=len(cone.rows);hi=len(hrows);g=mu[:gi];h=mu[gi:gi+hi];mix=mu[gi+hi:]
    assert len(mix)==len(assignments)
    total=sum(mix,F(0))
    if total!=1:
        beta/=total;g=[v/total for v in g];h=[v/total for v in h];mix=[v/total for v in mix]
    assert all(v>=0 for v in g+h+mix) and sum(mix,F(0))==1
    residual=tuple(beta*cone.welfare[j]-sum(v*row[j] for v,row in zip(g,cone.rows))
                   -sum(v*row[j] for v,row in zip(h,hrows))
                   -sum(v*row[j] for v,row in zip(mix,rrows)) for j in range(n))
    valid=all(v>=0 for v in residual)
    report={'status':'exact_dual_certificate' if valid else 'rationalized_dual_failed_exact_check',
            'scope':'one complete policy, all nonnegative customer multiplicities, target weakly optimal',
            'source':str(source.relative_to(ROOT)),'target':target,'actual':path,
            'beta':str(beta),'minimum_residual':str(min(residual)),
            'SPE_multipliers':[(i,str(v)) for i,v in enumerate(g) if v],
            'optimality_multipliers':[(list(t),str(v)) for t,v in zip(alternatives,h) if v],
            'assignment_mixture':[(list(t),str(v)) for t,v in zip(assignments,mix) if v],
            'residual':[str(v) for v in residual]}
    out=HERE/'source_partition_dual.json';out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'residual','SPE_multipliers','optimality_multipliers','assignment_mixture'}}))

if __name__=='__main__':main()
