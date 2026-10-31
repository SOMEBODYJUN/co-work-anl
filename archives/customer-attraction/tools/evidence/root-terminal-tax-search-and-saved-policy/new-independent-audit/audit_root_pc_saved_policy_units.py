from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement
from collections import Counter
import argparse, hashlib, json

ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
assert not args.out.exists(), 'No replay of an existing new targeted audit'
args.out.mkdir()
raw=args.input.read_bytes();obj=json.loads(raw);inst=obj['instance'];cert=obj['certificate'];n=len(inst['topics']);m=inst['players']
assert n==6 and m==5
units=[]
for row in inst['customers']:
    assert isinstance(row['multiplicity'],int) and row['multiplicity']>0
    t=frozenset(row['topics']);assert all(isinstance(a,int) and 0<=a<n for a in t)
    units.extend([t]*row['multiplicity'])
assert len(units)==9
actions={}
for row in cert['actions']:
    assert set(row)=={'history','action'}
    h=tuple(row['history']);a=row['action'];assert h not in actions and isinstance(a,int) and 0<=a<n
    actions[h]=a
domain={h for d in range(m)for h in product(range(n),repeat=d)}
assert set(actions)==domain and len(domain)==1555

@lru_cache(None)
def finish(h):
    return h if len(h)==m else finish(h+(actions[h],))
def utility(z,a):
    ans=F()
    for t in units:
        if a in t:
            load=sum(b in t for b in z);assert load>0;ans+=F(1,load)
    return ans
def welfare(z):return sum(any(a in t for a in z)for t in units)
def terminal_tax(z):
    return sum((F(load,load+1)for t in units if (load:=sum(a in t for a in z))),F())

counts=Counter();min_gap=None;history_rows=[]
for h in sorted(domain,key=lambda h:(len(h),h)):
    a=actions[h];z=finish(h);own=utility(z,a);profits=[]
    for b in range(n):
        dev=utility(finish(h+(b,)),b);gap=own-dev;assert gap>=0,(h,a,b,str(gap))
        profits.append(str(dev));counts['including_self']+=1
        if b!=a:counts['nonself']+=1;counts['strict_nonself' if gap>0 else 'tie_nonself']+=1
        min_gap=gap if min_gap is None else min(min_gap,gap)
    history_rows.append(dict(history=list(h),action=a,action_profits=profits))
z=finish(());q=tuple(z.count(a)for a in range(n));assert q==tuple(cert['terminal_counts'])
profiles=list(combinations_with_replacement(range(n),m));assert len(profiles)==252
opt=max(map(welfare,profiles));w=welfare(z);tax=terminal_tax(z);margin=F(w)+tax-opt
assert (w,opt,tax,margin)==(5,9,F(25,6),F(1,6)) and str(margin)==obj['tax_minus_opt']
assert obj['verification_valid'] is True and obj['violations']==0
payload=dict(scope='one saved 9-unit-client, five-player complete ordered-history policy; no BI, old discoverer, LP or canonical-module import',input_sha256=hashlib.sha256(raw).hexdigest(),topics=n,players=m,unit_clients=len(units),interest_types=len(inst['customers']),ordered_decision_histories=len(domain),actual_path=list(z),terminal_counts=list(q),comparison_counts=dict(counts),minimum_including_self_gap=str(min_gap),terminal_count_profiles=len(profiles),W=w,OPT=opt,tax=str(tax),W_plus_tax_minus_OPT=str(margin),OPT_over_W=str(F(opt,w)),same_coverage_distinct_labels_retained=[0,2],all_ordered_histories_and_all_legal_actions_pass=True,original_or_canonical_imports=0,LP_MILP_RNG_calls=0)
(args.out/'result.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
(args.out/'all-1555-history-action-and-profit-rows.json').write_text(json.dumps(history_rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(payload,ensure_ascii=False,indent=2))
