"""Finite checks of an arbitrary-player action-deletion obstruction.
The all-k proof is in comparison_catalogue_pruning_obstruction.md.
"""
from itertools import combinations
from fractions import Fraction as F
from pathlib import Path
import json
from customer_attraction import Instance, ExactSPESolver, verify_certificate

OUT=Path(__file__).parent

def family(k, include_B):
    covers=[]; labels=[]
    for i in range(k):
        X={('x',i,0),('x',i,1)}
        covers.append(X|{('a',i)}); labels.append(f'A{i+1}')
        if include_B:
            covers.append(X|{('b',)}); labels.append(f'B{i+1}')
        covers.append(X); labels.append(f'C{i+1}')
    covers.append({('b',),('d',)}); labels.append('D')
    return Instance.from_topic_sets(covers,k+1,labels)

def independent_solver(inst):
    # Direct ordered histories. This does not share count compression or utility
    # code with the package solver; each compressed customer is expanded.
    interests=[c.topics for c in inst.customers for _ in range(c.multiplicity)]
    def u(path,i):
        return sum((F(1,sum(a in B for a in path)) for B in interests if path[i] in B),F(0))
    def solve(prefix):
        if len(prefix)==inst.players: return {prefix}
        children=[solve(prefix+(a,)) for a in range(inst.topic_count)]
        i=len(prefix)
        threshold=max(min(u(path,i) for path in child) for child in children)
        return {path for child in children for path in child if u(path,i)>=threshold}
    return solve(())

def run():
    results=[]
    for k in range(1,4):
        full=family(k,True); pruned=family(k,False)
        sf=ExactSPESolver(full); sp=ExactSPESolver(pruned)
        actual=tuple(full.topics.index(f'C{i+1}') for i in range(k))+(full.topics.index('D'),)
        cert=sf.certificate(on_path=actual)
        verify_certificate(full,cert).assert_valid()
        target=tuple(1 if a.startswith('A') or a=='D' else 0 for a in pruned.topics)
        assert sp.outcomes()==frozenset({target})
        direct=independent_solver(pruned)
        assert direct==set(sp.ordered_outcomes())
        assert len(direct)==__import__('math').factorial(k)
        assert {path[-1] for path in direct}=={pruned.topics.index('D')}
        assert full.optimal_welfare()==pruned.optimal_welfare()==3*k+2
        assert full.welfare(full.counts(actual))==2*k+2
        results.append({'k':k,'m':k+1,'original_topics':full.topic_count,'pruned_topics':pruned.topic_count,
                        'original_certified_welfare':2*k+2,'pruned_all_SPE_welfare':sp.minimum_welfare(),
                        'unchanged_optimum':3*k+2,'pruned_count_outcomes':list(sp.outcomes()),
                        'pruned_ordered_paths':sorted(direct),'full_certificate_verified':True,
                        'independent_ordered_BI_agrees':True})
    (OUT/'comparison_catalogue_pruning_family.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

if __name__=='__main__': run()
