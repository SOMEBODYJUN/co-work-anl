#!/usr/bin/env python3
"""Independent finite audit for UM-TWO-STATE-POOL-EXACT-FRONTIER-v1.

Exhaust every nonempty selected row/column set, then use a fresh
capacity-one resource / cloned-slot augmenting matcher to compute its
maximum common integer quota.  This is deliberately exponential AUDIT
code; the proved closed-form family algorithm is polynomial.  Never loop
over the binary demand K.  Optional --source records the attacked file.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

VERSION='two-state-pool-exact-frontier-audit-v1.0'


def quota_matching(s, groups, quota):
    slots=[(side,index,h) for side,index in groups for h in range(quota)]
    owner={}
    def visit(slot, seen):
        side,index,_=slot
        neighbors=((index,j) for j in range(s)) if side=='row' else ((i,index) for i in range(s))
        for cell in neighbors:
            if cell in seen:
                continue
            seen.add(cell)
            if cell not in owner or visit(owner[cell],seen):
                owner[cell]=slot
                return True
        return False
    if not all(visit(slot,set()) for slot in slots):
        return None
    assigned={group:[] for group in groups}
    for cell,(side,index,_) in owner.items():
        assigned[(side,index)].append(cell)
    assert sum(map(len,assigned.values()))==len(owner)==quota*len(groups)
    for (side,index),cells in assigned.items():
        assert len(cells)==quota
        assert all((r==index if side=='row' else c==index) for r,c in cells)
    return assigned


def quota_profiles(s):
    all_groups=[('row',i) for i in range(s)]+[('col',i) for i in range(s)]
    profiles=[]
    sets=matching_calls=0
    for k in range(1,2*s+1):
        best=0
        winner=None
        for groups in combinations(all_groups,k):
            sets+=1
            attained=0
            for quota in range(1,s+1):
                matching_calls+=1
                witness=quota_matching(s,groups,quota)
                if witness is None:
                    break
                attained=quota
            a=sum(side=='row' for side,_ in groups)
            b=k-a
            # This equality is checked AFTER actual matching, never used to
            # decide matching or skip a selected set.
            hall_quota=(s*k-a*b)//k
            assert attained==hall_quota
            if attained>best:
                best=attained
                winner=groups
        h=min(s,(s*s)//k)
        assert best==h
        profiles.append({'k':k,'actual_maximum_quota':best,'formula_h_k':h,
                         'one_maximizing_selected_set':winner})
    return {'s':s,'selected_sets_exhausted':sets,'matching_calls':matching_calls,'profiles':profiles}


def exact_from_profiles(s,K,profiles):
    assert K>=s>=1
    actual=max(min(F(row['k'],2*s),F(row['actual_maximum_quota'],K)) for row in profiles)
    formula=max(min(F(k,2*s),F(min(s,(s*s)//k),K)) for k in range(1,2*s+1))
    assert actual==formula
    return actual


def audit(source=None):
    results=[]
    for s in range(1,7):
        found=quota_profiles(s)
        demands=sorted(set(range(s,2*s+2))|{2**131+17})
        evaluations=[]
        for K in demands:
            b=exact_from_profiles(s,K,found['profiles'])
            claimed=min(F(1,2),F(s,K))
            evaluations.append({'K':K,'exact_b_star':str(b),
                                'old_equation_3':str(claimed),'old_equation_correct':b==claimed})
            # Exact validity threshold for the old expression, independently
            # cross-checked against matching-based finite optima.
            assert (b==claimed)==(K>=2*s-2)
            if K==2*s:
                assert b==F(1,2)
        found['demands']=evaluations
        results.append(found)
    # Explicit 5-of-8 actual resource assignment, checked anew.
    groups=(('row',0),)+tuple(('col',j) for j in range(4))
    resources={('row',0):[(0,0),(0,1),(0,2)],
               ('col',0):[(1,0),(2,0),(3,0)],
               ('col',1):[(1,1),(2,1),(3,1)],
               ('col',2):[(1,2),(2,2),(3,2)],
               ('col',3):[(0,3),(1,3),(2,3)]}
    flat=[cell for cells in resources.values() for cell in cells]
    assert len(flat)==len(set(flat))==15
    assert all(len(cells)==3 for cells in resources.values())
    assert quota_matching(4,groups,3) is not None
    assert min(F(len(groups),8),F(3,4))==F(5,8)
    s4=next(r for r in results if r['s']==4)
    assert exact_from_profiles(4,4,s4['profiles'])==F(5,8)
    old_examples=[]
    for K in (8,16,32):
        b=exact_from_profiles(4,K,s4['profiles'])
        assert b==min(F(1,2),F(4,K))
        old_examples.append({'s':4,'K':K,'exact_b_star':str(b)})
    result={'claim':'UM-TWO-STATE-POOL-EXACT-FRONTIER-v1','version':VERSION,
            'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'arithmetic':'fractions.Fraction','seed':None,'scope':'complete finite selected-set matching audits for s=1..6, not the general proof',
            's_profiles':results,'original_listed_examples_preserved':old_examples,
            'explicit_counterexample':{'s':4,'K':4,'selected_groups':[list(g) for g in groups],
                'resources':[{'group':list(g),'cells':[list(cell) for cell in cells]}
                             for g,cells in resources.items()],
                'root_degree':5,'root_demand':8,'variable_degrees':[1]*5,
                'variable_demands':[1]*5,'label_degrees':[3]*5,'label_demands':[4]*5,
                'score':'5/8','exact_b_star':'5/8'},
            'status':'passed'}
    if source:
        result['attacked_source']={'path':str(source),'sha256':sha256(source.read_bytes()).hexdigest()}
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path)
    args=parser.parse_args()
    print(json.dumps(audit(args.source),ensure_ascii=False,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
