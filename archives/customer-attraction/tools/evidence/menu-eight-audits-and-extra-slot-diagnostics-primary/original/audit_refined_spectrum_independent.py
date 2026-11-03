"""Independent standard-library audit of one refined-seat numerical example.

Reads only the author's raw instance/path JSON. Does not import the author's
script or a repository game/BI verifier. Expands every customer into a unit,
constructs a complete SPE realizing the supplied path, and rechecks every
ordered-history unilateral comparison directly.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'omission/refined_spectrum_strict_example.json'

def main():
    raw=json.loads(SOURCE.read_text());inst=raw['instance']
    m=inst['players'];k=len(inst['topics']);target=tuple(raw['path'])
    customers=[frozenset(row['topics']) for row in inst['customers']
        for _ in range(row.get('multiplicity',1))]
    topics=[frozenset(x for x,c in enumerate(customers) if a in c) for a in range(k)]
    def utility(i,z):
        a=z[i]
        return sum((F(1,sum(t in customers[x] for t in z)) for x in topics[a]),F())
    def welfare(z):return len(set().union(*(topics[a] for a in z)))

    # For each ordered history, retain exactly the full SPE terminal outcomes.
    # A target child can be supported iff its current payoff beats every other
    # action's least attainable continuation payoff. All children are independent
    # ordered subgames; we use this rule only on this finite example.
    @lru_cache(None)
    def possible(h):
        i=len(h)
        if i==m:return (h,)
        children=[possible(h+(a,)) for a in range(k)]
        threshold=max(min(utility(i,z) for z in child) for child in children)
        return tuple(z for child in children for z in child if utility(i,z)>=threshold)
    assert target in possible(())
    actions={}
    def build(h,z):
        i=len(h)
        if i==m:return
        a=z[i];actions[h]=a
        for b in range(k):
            child=h+(b,)
            chosen=z if b==a else min(possible(child),key=lambda v:(utility(i,v),v))
            build(child,chosen)
    build((),target)
    def follow(h):
        while len(h)<m:h=h+(actions[h],)
        return h

    comparisons=[]
    for d in range(m):
        for h in product(range(k),repeat=d):
            own=utility(d,follow(h))
            for a in range(k):
                other=utility(d,follow(h+(a,)))
                assert own>=other
                comparisons.append(own-other)
    actual=follow(())
    assert actual==target
    W=welfare(actual);payoffs=[utility(i,actual) for i in range(m)]
    assert sum(payoffs,F())==W
    opt=max(welfare(z) for z in product(range(k),repeat=m))
    opt_witness=next(z for z in product(range(k),repeat=m) if welfare(z)==opt)
    C=set().union(*(topics[a] for a in actual))
    maximal=[a for a in range(k) if not any(topics[a]<topics[b] for b in range(k))]
    # There are no equal-coverage labels in this input; make it an explicit check.
    assert len(set(topics))==k
    private={a:topics[a]-set().union(*(topics[b] for b in maximal if b!=a)) for a in maximal}
    omitted={a:private[a]-C for a in maximal}
    old=sorted((F(len(omitted[a]),seat)+F(len(topics[a]-omitted[a]),m)
        for a in maximal for seat in range(1,m+1)),reverse=True)
    rows=[]
    for i in range(m):
        r=m-i
        background=[sum(x in topics[a] for a in actual[:i]) for x in range(len(customers))]
        per_topic={}
        for a in maximal:
            base=sum((F(1,background[x]+r) for x in topics[a]-omitted[a]),F())
            per_topic[a]=[F(len(omitted[a]),seat)+base for seat in range(1,r+1)]
        spectrum=sorted((v for values in per_topic.values() for v in values),reverse=True)
        new=spectrum[r-1]
        direct=max(sum((F(1,background[x]+r) for x in topics[a]),F()) for a in range(k))
        old_rank=old[r-1];old_max=max(old_rank,direct)
        assert payoffs[i]>=new>=old_max
        rows.append({'position':i+1,'remaining':r,'actual_profit':str(payoffs[i]),
            'G_by_maximal_topic':{str(a):list(map(str,values)) for a,values in per_topic.items()},
            'G_sorted':list(map(str,spectrum)),'lambda':str(new),'old_rank':str(old_rank),
            'direct_floor':str(direct),'old_max':str(old_max)})
    new_sum=sum((F(row['lambda']) for row in rows),F())
    old_sum=sum((F(row['old_max']) for row in rows),F())
    assert new_sum==F(127,2) and old_sum==F(184,3) and new_sum-old_sum==F(13,6)
    assert W==raw['welfare']
    assert new_sum==F(raw['new']) and old_sum==F(raw['old_combined']) and new_sum-old_sum==F(raw['gap'])
    for row,claimed in zip(rows,raw['rows']):
        assert [row['remaining'],row['lambda'],row['old_rank'],row['direct_floor']]==claimed
    report={'scope':'independent finite numerical/definition audit; not a re-audit of the arbitrary-m proof',
        'source':str(SOURCE.relative_to(HERE.parent)),
        'strategy_status':'source JSON contains no strategy; independently completed one full SPE realizing its path',
        'unit_customers':len(customers),'distinct_topics':k,'players':m,'actual_path':list(actual),
        'profits':list(map(str,payoffs)),'W':W,'OPT':opt,'OPT_witness':list(opt_witness),
        'ordered_decision_histories':len(actions),'comparisons_including_own':len(comparisons),
        'proper_deviations':len(comparisons)-len(actions),'minimum_slack':str(min(comparisons)),
        'strict_comparisons':sum(v>0 for v in comparisons),'tie_comparisons':sum(v==0 for v in comparisons),
        'all_maximal_topics':maximal,'private_sizes':{str(a):len(private[a]) for a in maximal},
        'omitted_private_sizes':{str(a):len(omitted[a]) for a in maximal},
        'old_sorted_spectrum':list(map(str,old)),'rows':rows,
        'new_sum':str(new_sum),'old_max_sum':str(old_sum),'strict_gap':str(new_sum-old_sum),
        'actions':[{'history':list(h),'action':actions[h]} for h in sorted(actions,key=lambda h:(len(h),h))]}
    (HERE/'refined_spectrum_independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('unit_customers','actual_path','profits','W','OPT',
        'ordered_decision_histories','comparisons_including_own','proper_deviations','minimum_slack',
        'new_sum','old_max_sum','strict_gap')},indent=2))

if __name__=='__main__':main()
