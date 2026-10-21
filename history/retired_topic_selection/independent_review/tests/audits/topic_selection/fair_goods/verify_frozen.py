"""Independent scalar checks of all frozen minimum-witness instances."""
import itertools as it
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'toy_results.json').read_text())
out=[]
for case in data['keys']:
    sizes=case['sizes']; m=sum(sizes); r=m//4
    V=case['worst_observed_instance']['valuations']; count=0; feasible=0
    for groups in it.product(*(it.permutations(range(4),s) for s in sizes)):
        a=sum((tuple(z) for z in groups),())
        if any(a.count(i)!=r for i in range(4)): continue
        feasible+=1
        B=[[g for g in range(m) if a[g]==j] for j in range(4)]
        good=True
        for i in range(4):
            own=sum(V[i][g] for g in B[i])
            for j in range(4):
                other=sum(V[i][g] for g in B[j])
                if own<other-max(V[i][g] for g in B[j]): good=False
                if i<j and own<other: good=False
        count+=good
    assert feasible==case['feasible_labelled_allocations']
    assert count==case['minimum_witness_count']
    out.append({'key_sizes':sizes,'feasible':feasible,'scalar_witness_count':count,'matches_frozen':True})

for case in data['copies']+[json.loads((ROOT/'copies_exhaustive_results.json').read_text())['worst']]:
    rankings=case.get('worst_observed_instance',case)['rankings']
    c=case['copies']; n=len(rankings); t=len(c); count=0
    for recipients in it.product(*(it.combinations(range(n),s) for s in c)):
        good=True
        for i in range(n):
            for j in range(n):
                own=other=0
                for g in rankings[i]:
                    own+=(i in recipients[g]); other+=(j in recipients[g])
                    if own<other-1: good=False;break
                if not good:break
            if not good:break
        count+=good
    expected=case.get('minimum_witness_count',case.get('count'))
    assert count==expected
    out.append({'copies':c,'n':n,'scalar_witness_count':count,'matches_frozen':True})
(ROOT/'independent_scalar_verification.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
