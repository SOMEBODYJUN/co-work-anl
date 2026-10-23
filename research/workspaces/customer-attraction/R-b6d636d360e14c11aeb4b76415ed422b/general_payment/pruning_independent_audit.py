"""Definition-level finite audit of the B_i-deleted catalogue.

No canonical CAG module, solver, certificate code, or author's script is
imported. Customer sets are expanded to distinct unit clients. Caching is by
full ordered history, preserving all history-dependent tie choices.
The arbitrary-k result comes from the analytic induction in the review.
"""
from __future__ import annotations
from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from math import factorial
from pathlib import Path
import json

def audit(k):
    names = tuple([f'A{i}' for i in range(k)] + [f'C{i}' for i in range(k)] + ['D'])
    customers = tuple([f'x{i}_{j}' for i in range(k) for j in range(2)]
                      + [f'a{i}' for i in range(k)] + ['b','d'])
    themes = []
    for i in range(k): themes.append(frozenset([f'x{i}_0',f'x{i}_1',f'a{i}']))
    for i in range(k): themes.append(frozenset([f'x{i}_0',f'x{i}_1']))
    themes.append(frozenset(['b','d']))
    m=k+1; p=len(themes); decision_nodes=0; branch_comparisons=0

    @lru_cache(None)
    def pay(path, pos):
        return sum((Fraction(1,sum(x in themes[a] for a in path))
                    for x in customers if x in themes[path[pos]]),Fraction(0))

    @lru_cache(None)
    def solve(h):
        nonlocal decision_nodes, branch_comparisons
        if len(h)==m: return frozenset([h])
        decision_nodes+=1
        children=[solve(h+(a,)) for a in range(p)]
        # Off-path continuations can be selected independently at each ordered
        # child. Therefore any target can be supported iff its current payoff
        # reaches the max of the actionwise smallest attainable payoff.
        floor=max(min(pay(path,len(h)) for path in child) for child in children)
        out=set()
        for a,child in enumerate(children):
            for path in child:
                branch_comparisons+=1
                if pay(path,len(h))>=floor: out.add(path)
        assert out
        return frozenset(out)

    paths=solve(())
    expected=frozenset(tuple(order)+(2*k,) for order in permutations(range(k)))
    assert paths==expected
    domain_nodes=0; old_c_nodes=0; checked_paths=0
    # The full history recursion was already expanded. Check the stronger
    # author's F/E statement on every history in its specified state domain.
    def check_domains(h=()):
        nonlocal domain_nodes,old_c_nodes,checked_paths
        if len(h)>m: return
        d_count=h.count(2*k)
        groups=[a%k for a in h if a!=2*k]
        if d_count<=1 and len(groups)==len(set(groups)):
            touched=set(groups); fresh=set(range(k))-touched
            old_c={a-k for a in h if k<=a<2*k}
            domain_nodes+=1; old_c_nodes+=bool(old_c)
            suffixes={path[len(h):] for path in solve(h)}
            if d_count:
                allowed={tuple(order) for order in permutations(fresh)}
            else:
                allowed={tuple(order)+(last,) for order in permutations(fresh)
                         for last in (2*k,*sorted(old_c))}
            assert suffixes==allowed,(k,h,suffixes,allowed)
            checked_paths+=len(suffixes)
            for a in range(p):
                if len(h)<m: check_domains(h+(a,))
    check_domains()
    welfare={len(set().union(*(themes[a] for a in path))) for path in paths}
    assert welfare=={3*k+2}
    return {'k':k,'players':m,'topics':p,'unit_clients':len(customers),
            'ordered_decision_nodes':decision_nodes,
            'attainable_child_path_tests':branch_comparisons,
            'root_ordered_SPE_paths':len(paths),'expected_factorial':factorial(k),
            'all_state_domain_nodes':domain_nodes,'old_C_domain_nodes':old_c_nodes,
            'state_domain_attainable_suffixes_checked':checked_paths,
            'root_welfare':3*k+2,'OPT':3*k+2,
            'root_paths_labels':[[names[a] for a in path] for path in sorted(paths)]}

if __name__=='__main__':
    report={'scope':'independent finite full ordered-history audit; analytic induction supplies arbitrary k',
            'canonical_solver_imported':False,'author_code_imported':False,
            'results':[audit(k) for k in (1,2,3)]}
    output=Path(__file__).with_name('pruning_independent_audit.json')
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
