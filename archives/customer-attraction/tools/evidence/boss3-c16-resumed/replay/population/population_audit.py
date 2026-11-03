"""Definition-level all-ordered-history audit of population welfare drop.
No customer_attraction solver, recurrence implementation, or verifier is imported.
Customers are expanded as distinct unit rows. Fraction arithmetic is exact.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
TYPES=[((0,),1),((2,),3),((0,2),3),((1,2),1),((0,1,2),2),((3,),4),((0,3),1),((0,1,3),4),((1,2,3),3)]
UNIT_CUSTOMERS=[frozenset(B) for B,r in TYPES for _ in range(r)]
K=4

def payoff(path,i):
    a=path[i]
    return sum((Fraction(1,sum(b in B for b in path)) for B in UNIT_CUSTOMERS if a in B),Fraction())

def welfare(path):
    return sum(any(a in B for a in path) for B in UNIT_CUSTOMERS)

def counts(path):return tuple(path.count(a) for a in range(K))

def all_ordered_spe(m):
    tables={}
    def solve(h):
        if len(h)==m:return {h}
        i=len(h)
        child=[solve(h+(a,)) for a in range(K)]
        floor=max(min(payoff(q,i) for q in ends) for ends in child)
        answer={q for a,ends in enumerate(child) for q in ends if payoff(q,i)>=floor}
        tables[h]={'floor':str(floor),'children':[{'action':a,'min':str(min(payoff(q,i) for q in ends)),'max':str(max(payoff(q,i) for q in ends)),'counts':sorted({counts(q) for q in ends})} for a,ends in enumerate(child)],'outcome_counts':sorted({counts(q) for q in answer})}
        return answer
    answer=solve(())
    return answer,tables

def verify_full_certificate(data,m):
    actions={tuple(row['history']):row['action'] for row in data['actions']}
    expected={h for t in range(m) for h in product(range(K),repeat=t)}
    assert set(actions)==expected
    def follow(h):
        while len(h)<m:h=h+(actions[h],)
        return h
    comparisons=0
    for h in expected:
        i=len(h);actual=follow(h);value=payoff(actual,i)
        for a in range(K):
            alternative=follow(h+(a,))
            assert value>=payoff(alternative,i),(h,a,value,payoff(alternative,i))
            comparisons+=1
    path=follow(())
    return {'path':path,'payoffs':[str(payoff(path,i)) for i in range(m)],'welfare':welfare(path),'ordered_nodes':len(expected),'deviation_comparisons':comparisons}

def main():
    source=json.loads((ROOT/'population_small.json').read_text())
    report={'identity':'population welfare nonmonotonicity, exact finite result; not a half-coverage counterexample','unit_customers':len(UNIT_CUSTOMERS),'types':[{'topics':B,'multiplicity':r} for B,r in TYPES],'results':{}}
    for m in (3,4):
        ends,tables=all_ordered_spe(m)
        cert=verify_full_certificate(source[f'worst_certificate_{m}'],m)
        report['results'][m]={'all_spe_counts':sorted({counts(q) for q in ends}),'all_spe_welfares':sorted({welfare(q) for q in ends}),'ordered_spe_paths':len(ends),'root_menu':tables[()],'certificate_audit':cert,'all_ordered_node_tables':[{'history':h,**d} for h,d in sorted(tables.items())]}
    assert report['results'][3]['all_spe_welfares']==[22]
    assert report['results'][4]['all_spe_welfares']==[21]
    (ROOT/'population_audit.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({m:{k:v for k,v in d.items() if k!='all_ordered_node_tables'} for m,d in report['results'].items()},indent=2))
if __name__=='__main__':main()
