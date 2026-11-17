"""Definition-level exact check of the shared-count join and generic boundary.
Uses no repository SPE solver, model, or certificate implementation.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

A,B=0,1
H=[h for d in range(3) for h in product((A,B),repeat=d)]

def terminal(policy,h=()):
    while len(h)<3:h=h+(policy[h],)
    return h

def verify(policy,pay):
    for h in H:
        a=policy[h];q=terminal(policy,h)
        for b in (A,B):
            if pay(q,a)<pay(terminal(policy,h+(b,)),b):return False
    return True

def markov(policy):
    return policy[(A,B)]==policy[(B,A)]

def all_spe(pay):
    results=[]
    for choices in product((A,B),repeat=len(H)):
        policy=dict(zip(H,choices))
        if verify(policy,pay):results.append((policy,terminal(policy)))
    return results

def coverage(path,a):return F(1,path.count(a))
GENERIC={(3,0):(F(2),F(0)),(2,1):(F(3),F(1)),(1,2):(F(1),F(3)),(0,3):(F(0),F(3))}
def generic(path,a):return GENERIC[(path.count(A),path.count(B))][a]
def counts(path):return (path.count(A),path.count(B))
def record(pay):
    full=all_spe(pay);mp=[(p,q) for p,q in full if markov(p)]
    return {'full_strategy_count':len(full),'markov_strategy_count':len(mp),
            'full_terminal_counts':sorted(set(counts(q) for p,q in full)),
            'markov_terminal_counts':sorted(set(counts(q) for p,q in mp)),
            'full_paths':sorted(set(q for p,q in full)),
            'markov_paths':sorted(set(q for p,q in mp))}

def main():
    c=record(coverage);g=record(generic)
    assert (A,B,A) in map(tuple,c['full_paths'])
    assert (A,B,A) in map(tuple,c['markov_paths'])
    assert (B,A,A) in map(tuple,c['markov_paths'])
    assert c['full_terminal_counts']==c['markov_terminal_counts']
    assert g['full_terminal_counts']==[(0,3),(1,2),(2,1),(3,0)]
    assert g['markov_terminal_counts']==[(0,3),(3,0)]
    # Each last-player BR satisfies one cap; no BR satisfies both.
    caps={a:[] for a in (A,B)}
    br=[(A,B,A),(A,B,B)]
    for a in (A,B):caps[a]=[q for q in br if coverage(q,a)<=F(1,2)]
    assert caps[A] and caps[B] and not set(caps[A])&set(caps[B])
    data={'scope':'Exact join obstruction and generic non-CAG boundary; Q-CAG-HALF remains OPEN',
          'coverage_singleton':c,'generic_anonymous_game':g,
          'join_payoff_vectors':[[str(coverage(q,a)) for a in (A,B)]for q in br],
          'root_comparisons_per_strategy':len(H)*2}
    dest=Path(__file__).with_name('join_conflict_verification.json')
    dest.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
