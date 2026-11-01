"""Definition-level exact recovery: optimal partitioned frozen queries fail.

Does not import LP discovery, SPE solver, or another verifier.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json, math, argparse

OUT=Path(__file__).resolve().parent
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',default='probe.json')
    parser.add_argument('--output')
    args=parser.parse_args()
    blob=json.loads((OUT/args.source).read_text())
    discovery=blob.get('best',blob)
    types=list(product((0,1),repeat=6))[1:]
    fractions=[F(float(v)).limit_denominator(10000) for v in discovery['weights']]
    scale=math.lcm(*(x.denominator for x in fractions))
    masses=[int(x*scale) for x in fractions]
    assert all(x>=0 for x in masses)
    customers=[tuple(i for i,b in enumerate(bits) if b)
               for bits,n in zip(types,masses) for _ in range(n)]
    sets=[{x for x,liked in enumerate(customers) if a in liked} for a in range(6)]
    assert len({frozenset(s) for s in sets})==6
    def payoff(a,b,who):
        theme=a if who==0 else b
        return sum((F(1,int(x in sets[a])+int(x in sets[b])) for x in sets[theme]),F())
    replies=discovery['reply']
    assert replies[0]==1
    matrix=[[payoff(a,b,1) for b in range(6)] for a in range(6)]
    for a in range(6):assert matrix[a][replies[a]]==max(matrix[a])
    roots=[payoff(a,replies[a],0) for a in range(6)]
    assert roots[0]==max(roots)
    actual=sets[0]|sets[1]
    values={(a,b):len(sets[a]|sets[b]) for a,b in combinations_with_replacement(range(6),2)}
    optimum=max(values.values());best=[p for p,v in values.items() if v==optimum]
    assert best==[(2,3)]
    qvalues=[]
    for matching in [(2,3),(3,2)]:
        total=F();parts=[]
        for x in sets[2]|sets[3]:
            cost=[]
            for i,t in enumerate(matching):
                if x in sets[t]:
                    c=int(x in sets[0])+int(x in sets[1])
                    cost.append(F(1,c+1-int(x in sets[i])))
            total+=min(cost)
        qvalues.append(total)
    assert min(qvalues)>len(actual)
    report={'status':'definition-level exact counterexample to PFR-OPT-v1 only',
            'players':2,'topics':6,'unit_customers':len(customers),
            'types':[{'topics':[a for a,b in enumerate(bits) if b],'multiplicity':n}
                     for bits,n in zip(types,masses) if n],
            'complete_replies':replies,'root_action':0,
            'last_payoff_matrix':[[str(x) for x in row] for row in matrix],
            'root_deviation_payoffs':list(map(str,roots)),
            'actual_payoffs':[str(payoff(0,1,i)) for i in range(2)],
            'W':len(actual),'OPT':optimum,'unique_optimal_support':best[0],
            'all_pair_coverages':{str(p):v for p,v in values.items()},
            'partition_minima_for_two_matchings':list(map(str,qvalues)),
            'minimum_excess_over_W':str(min(qvalues)-len(actual)),
            'half_coverage_holds':optimum<=2*len(actual)}
    if args.output:
        output=OUT/args.output
        with output.open('x') as stream:stream.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
