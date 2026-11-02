"""Definition-level exact replay, with no imports from the canonical package."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json

P = 6
M = 3
X, Y = frozenset(range(3)), frozenset(range(3,6))
units = [frozenset([a,b]) for a in X for b in Y]
for I in combinations(X,2):
    for J in combinations(Y,2):
        units += [frozenset(I+J)]*3
assert len(units)==36


def utility(population, leaf, i):
    return sum((F(1, sum(a in B for a in leaf))
                for B in population if leaf[i] in B), F(0))


def coverage(population, leaf):
    return sum(bool(set(leaf)&B) for B in population)


def prescribed(h):
    if not h:return 0
    if len(h)==1:return 3 if h[0] in X else 0
    group=X if h[1] in X else Y
    return min(group-set(h))


@lru_cache(None)
def original_leaf(h):
    return h if len(h)==M else original_leaf(h+(prescribed(h),))


histories=[h for d in range(M) for h in product(range(P),repeat=d)]
slacks=[]
for h in histories:
    current=utility(units,original_leaf(h),len(h))
    for a in range(P):
        slack=current-utility(units,original_leaf(h+(a,)),len(h))
        assert slack>=0,(h,a,slack)
        slacks.append(slack)
old=original_leaf(())
assert old==(0,3,4)
assert [utility(units,old,i) for i in range(M)]==[10,12,12]
missed=[B for B in units if not set(old)&B]
assert missed==[frozenset([1,5]),frozenset([2,5])]
modified=tuple(frozenset([5]) if not set(old)&B else B for B in units)
assert len(modified)==36
assert coverage(units,old)==coverage(modified,old)==34
assert max(coverage(units,z) for z in product(range(P),repeat=M))==36
assert max(coverage(modified,z) for z in product(range(P),repeat=M))==36


def all_spe(population):
    @lru_cache(None)
    def rec(h):
        if len(h)==M:return frozenset([h])
        children=[rec(h+(a,)) for a in range(P)]
        floor=max(min(utility(population,z,len(h)) for z in child) for child in children)
        return frozenset(z for child in children for z in child
                         if utility(population,z,len(h))>=floor)
    return rec


rec=all_spe(modified)
root_ranges=[]
for a in range(P):
    us=[utility(modified,z,0) for z in rec((a,))]
    root_ranges.append((min(us),max(us)))
assert root_ranges==[(F(10),F(10)),(F(19,2),F(11)),(F(19,2),F(11)),
                     (F(12),F(12)),(F(12),F(12)),(F(12),F(12))]
assert rec(())==frozenset(product(Y,repeat=3)) & frozenset(z for z in product(range(P),repeat=3) if len(set(z))==3)
assert all(coverage(modified,z)==36 for z in rec(()))

table=[]
for a in range(P):
    pay=[utility(modified,(3,a,b),2) for b in range(P)]
    best=[b for b,v in enumerate(pay) if v==max(pay)]
    own={utility(modified,(3,a,b),1) for b in best}
    early={utility(modified,(3,a,b),0) for b in best}
    assert len(own)==len(early)==1
    table.append({'second':a,'last_best_replies':best,'second_u':str(next(iter(own))),
                  'root_u':str(next(iter(early)))})

# A different genuinely optimal comparison tuple permits private owners X1,X2.
favorable=tuple(frozenset([min(B)]) if not set(old)&B else B for B in units)
assert old in all_spe(favorable)(())

result={'status':'PASS; self-audit only, independent review pending',
        'claim_falsified':'fixed optimal tuple omitted-unit privatization preserving SPE welfare',
        'old_ordered_histories':len(histories),'old_all_action_comparisons':len(slacks),
        'old_z':old,'old_u':['10','12','12'],'old_W':34,'old_OPT':36,
        'fixed_optimal_tuple':[3,4,5],'forced_owners':[5,5],
        'modified_all_spe_ordered_leaves':sorted(rec(())),
        'modified_unique_spe_counts':[0,0,0,1,1,1],'modified_all_spe_W':36,
        'modified_OPT':36,'modified_root_ranges':[[str(x),str(y)] for x,y in root_ranges],
        'after_root_Y0_table':table,'favorable_optimal_tuple':[0,1,2],
        'favorable_owners':[1,2],'favorable_preserves_original_ordered_z':True}
out=Path(__file__).with_name('fixed_optimum_privatization_audit.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
