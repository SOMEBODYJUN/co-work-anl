"""One fixed structural diagnostic: legal topics are actual bipartite edges.

The catalogue is never completed to a Cartesian product. Exact outcomes come
from the canonical full-history outcome-set BI. Finite results prove no general
claim and this is not intended as an expanding random-instance sweep.
"""
from fractions import Fraction
import json
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType,Instance,ExactSPESolver


def instance(k,kind,pattern):
    if kind=='cycle':
        edges=tuple((i,k+j) for i in range(k) for j in (i,(i+1)%k))
    elif kind=='band':
        edges=tuple((i,k+j) for i in range(k) for j in range(k) if abs(i-j)<=1)
    else:
        raise ValueError(kind)
    if pattern=='uniform':
        weights=(1,)*(2*k)
    elif pattern=='bank4':
        weights=(1,)*k+(4,)*k
    elif pattern=='staircase':
        weights=tuple(1<<(i%3) for i in range(k))+tuple(1<<((i+1)%3) for i in range(k))
    else:
        raise ValueError(pattern)
    types=tuple(CustomerType(frozenset(j for j,e in enumerate(edges) if v in e),weights[v]) for v in range(2*k))
    return Instance(tuple(f'{i}-{j-k}' for i,j in edges),types,k),edges,weights


def main():
    output=Path(__file__).with_name('restricted_resource_graph_probe.json')
    if output.exists():
        raise FileExistsError(output)
    reports=[]
    for kind in ('cycle','band'):
        for k in (3,4,5):
            for pattern in ('uniform','bank4','staircase'):
                started=time.monotonic()
                game,edges,weights=instance(k,kind,pattern)
                solver=ExactSPESolver(game)
                outcomes=solver.outcomes()
                worst=min(outcomes,key=lambda q:(game.welfare(q),q))
                optimum=game.optimal_welfare()
                welfare=game.welfare(worst)
                stats=solver.stats
                result={'kind':kind,'k':k,'pattern':pattern,'edges':edges,
                        'resource_weights':weights,'players':k,
                        'topics':len(edges),'full_spe_terminal_counts':len(outcomes),
                        'count_states':stats.count_states,'retained_outcomes':stats.retained_outcomes,
                        'worst_counts':worst,'welfare':welfare,'optimum':optimum,
                        'ratio':str(Fraction(optimum,welfare)),
                        'elapsed_seconds':round(time.monotonic()-started,3)}
                reports.append(result)
                print(json.dumps(result),flush=True)
    payload={'status':'finite_exact_structural_diagnostic',
             'scope':'18 predeclared cycle/band catalogues; no Cartesian completion, no universal conclusion.',
             'reports':reports}
    with output.open('x') as f:
        json.dump(payload,f,indent=2)
        f.write('\n')


if __name__=='__main__':
    main()
