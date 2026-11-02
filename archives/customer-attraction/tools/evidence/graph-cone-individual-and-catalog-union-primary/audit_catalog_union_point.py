"""One exact read-only check of the saved ten-singleton full policy.
No original source import, LP, SPE solver, or random search.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product, combinations
import json
from pathlib import Path
import sys

source = Path(sys.argv[1])
original_policy = Path(sys.argv[2])
out = Path(sys.argv[3])
doc = json.loads(source.read_text())
p, n = doc['p'], doc['n']
assert (p,n)==(10,5)
assert set(doc)=={'scope','p','n','J','player_topic','rootpath','clones','O','ui','actions'}
clones=doc['clones']
assert len(clones)==(1<<p)-1 and all(type(x) is int and x>=0 for x in clones)
expected_clones=[int(mask & (mask-1)==0) for mask in range(1,1<<p)]
assert clones==expected_clones
records=doc['actions']
assert all(set(r)=={'history','action'} for r in records)
actions={tuple(r['history']):r['action'] for r in records}
required={h for depth in range(n) for h in product(range(p),repeat=depth)}
assert len(records)==len(actions)==len(required)==11111 and set(actions)==required
assert all(type(a) is int and a in range(p) and all(type(b) is int and b in range(p) for b in h) for h,a in actions.items())
assert all(a not in h for h,a in actions.items())
def complete(h):
    while len(h)<n:
        h=h+(actions[h],)
    return h

def utility(h,a):
    leaf=complete(h)
    return Fraction(1,leaf.count(a))

checks=strict=equal=0
min_slack=None
for h,a in actions.items():
    prescribed=utility(h+(a,),a)
    assert prescribed==1
    for b in range(p):
        dev=utility(h+(b,),b)
        slack=prescribed-dev
        assert slack>=0
        checks+=1
        strict+=slack>0
        equal+=slack==0
        min_slack=slack if min_slack is None else min(min_slack,slack)
        # All future prescribed choices are fresh; this is an independent
        # direct formula for each forced branch on the original action table.
        assert dev==Fraction(1,h.count(b)+1)
leaf=complete(())
assert list(leaf)==doc['rootpath']==[4,5,6,7,8]
assert doc['player_topic']==leaf[0]==4
assert doc['J']==list(range(p))
actual=[Fraction(1,leaf.count(a)) for a in leaf]
U=sum(clones)
W=len(set(leaf))
portfolio_values=[len(set(J)) for J in combinations(range(p),n)]
OPT=max(portfolio_values)
assert U==doc['O']==10 and Fraction(doc['ui'])==actual[0]==1
assert W==OPT==5
reference=json.loads(original_policy.read_text())
reference_actions={tuple(r['history']):r['action'] for r in reference['strategy']['actions']}
assert actions==reference_actions
result={
    'status':'passed',
    'source_sha256':sha256(source.read_bytes()).hexdigest(),
    'reference_policy_sha256':sha256(original_policy.read_bytes()).hexdigest(),
    'all_action_records_consumed':len(records),
    'histories_by_depth':dict(sorted(Counter(map(len,actions)).items())),
    'actions_fresh_at_every_ordered_history':True,
    'complete_action_comparisons_including_self':checks,
    'nonself_action_comparisons':checks-len(actions),
    'strict_comparisons':strict,'equal_comparisons':equal,
    'minimum_IC_slack':str(min_slack),
    'same_complete_action_function_as_original_main_input':True,
    'nonzero_clone_support':[[mask,count] for mask,count in enumerate(clones,1) if count],
    'root_path':list(leaf),'actual_utilities':[str(u) for u in actual],
    'total_catalog_union':U,'actual_welfare':W,'OPT_5':OPT,
    'five_distinct_label_portfolios_checked':len(portfolio_values),
    'auxiliary_U_minus_9_ui':str(U-9*actual[0]),
    'intended_OPT5_minus_9_ui':str(OPT-9*actual[0]),
    'OPT5_minus_10_ui':str(OPT-10*actual[0]),
    'twice_W_minus_OPT5':2*W-OPT,
    'source_entries_executed':0,'LP_calls':0,'SPE_solver_calls':0,
    'scope':'All 11111 saved full-history actions and 1023 clone coordinates; fixed singleton point only. Auxiliary full-union target fails; intended individual and half targets hold.'
}
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
