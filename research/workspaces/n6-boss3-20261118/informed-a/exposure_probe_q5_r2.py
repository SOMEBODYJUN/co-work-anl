"""Exact corrected q5 catalog exposure and full-SPE subtree discriminator; stdlib only."""
from fractions import Fraction
from itertools import combinations
from functools import lru_cache
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
K = 5
anchors = [frozenset(range(5*j,5*j+5)) for j in range(6)]
extras = [frozenset((a+t)%20 for t in range(5)) for a in (1,4,8,12,16)]
assert len(set(extras)) == 5
assert all(B not in anchors for B in extras)
assert all(len(B) == K for B in anchors+extras)
cover = anchors+extras
prefix=(0,0,0,0,1,1,0,0,0,0,0)

def exposure(j,F):
    return sum((Fraction(sum(x in extras[a] for a in F),1+sum(x in extras[a] for a in F)) for x in anchors[j]),Fraction())

rows=[]
for j in range(4):
    choices=[(exposure(j,F),F) for l in range(4) for F in combinations(range(5),l)]
    value,F=max(choices)
    rows.append({'anchor':j,'exact_max_loss':str(value),'margin_over_half':str(value-Fraction(K,2)),
                 'attacking_extra_indices':list(F)})

@lru_cache(None)
def terminal(c):
    loads=[sum(c[a] for a,S in enumerate(cover) if x in S) for x in range(30)]
    pay=tuple(sum(60//loads[x] for x in S if loads[x]) for S in cover)
    welfare=sum(v>0 for v in loads)
    return pay,welfare

nodes=[0]*7
@lru_cache(None)
def outcomes(c):
    occupied=sum(c)
    nodes[occupied]+=1
    if occupied==6:
        return frozenset((c,))
    children=[]
    for a in range(len(cover)):
        cp=list(c); cp[a]+=1
        child=outcomes(tuple(cp))
        worst=min(terminal(q)[0][a] for q in child)
        children.append((a,child,worst))
    threshold=max(z[2] for z in children)
    return frozenset(q for a,child,_ in children for q in child if terminal(q)[0][a]>=threshold)

# Record all possible terminal counts conditional on each first action, before
# choosing the current action; exactly implements arbitrary off-path SPE ties.
first=[]
for a in range(len(cover)):
    cp=list(prefix);cp[a]+=1
    out=outcomes(tuple(cp))
    first.append({'action':a,'minimum_current_payoff':str(Fraction(min(terminal(q)[0][a] for q in out),60)),
                  'maximum_current_payoff':str(Fraction(max(terminal(q)[0][a] for q in out),60)),
                  'outcome_count':len(out)})
root=outcomes(prefix)
summary={
    'model':'six unit providers, 30 distinct unit customers, 11 labels, exactly 5 distinct nonanchor extra covers, complete pure SPE outcome recursion',
    'catalog':{'anchors':[sorted(S) for S in anchors],'extras':[sorted(S) for S in extras]},
    'prefix_labels':[4,5],
    'exposure_ignoring_future_best_response':rows,
    'current_guaranteed_by_best_action':str(Fraction(max(Fraction(r['minimum_current_payoff']) for r in first))),
    'first_action_subtrees':first,
    'all_SPE_subtree_outcome_count':len(root),
    'all_SPE_subtree_minimum_final_welfare':min(terminal(q)[1] for q in root),
    'all_SPE_subtree_maximum_final_welfare':max(terminal(q)[1] for q in root),
    'counts_visited_by_total_players':nodes,
    'root_outcomes':[list(q) for q in sorted(root)],
    'note':'Fixed 2-label prefix is allowed off-path. This certifies only this finite subtree, not the universal six-player target.'
}
(ROOT/'exposure-probe-q5-r2.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('root_outcomes','catalog')},indent=2))
