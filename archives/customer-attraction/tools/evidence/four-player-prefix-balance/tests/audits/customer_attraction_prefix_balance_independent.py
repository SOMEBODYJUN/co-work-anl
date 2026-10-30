"""Independent expanded-unit-customer review of CA-PREFIX-BALANCE-NO."""
from fractions import Fraction
from itertools import product,combinations_with_replacement
import json
import argparse
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
instance=json.loads((ROOT/'examples/customer_attraction/prefix_balance_failure.json').read_text())
certificate=json.loads((ROOT/'evidence/certificates/customer_attraction/prefix_balance_failure.json').read_text())
p=len(instance['topics']);n=instance['players']
customers=[]
for group in instance['customers']:
    assert type(group['multiplicity']) is int and group['multiplicity']>=0
    customers.extend(frozenset(group['topics']) for _ in range(group['multiplicity']))
assert len(customers)==22
catalog=[frozenset(i for i,B in enumerate(customers) if a in B) for a in range(p)]
policy={tuple(e['history']):e['action'] for e in certificate['actions']}
required={h for depth in range(n) for h in product(range(p),repeat=depth)}
assert len(policy)==len(certificate['actions'])==259 and set(policy)==required
assert all(a in range(p) for a in policy.values())

def utility(profile,a):
    return sum((Fraction(1,sum(b in customers[x] for b in profile))
                for x in catalog[a]),Fraction(0))

def coverage(profile):
    return frozenset().union(*(catalog[a] for a in profile))

def replay(h):
    while len(h)<n:h=h+(policy[h],)
    return h

priority=[2,1,0,3,4,5]
for h,a in policy.items():
    if len(h)==0:expected=1
    elif len(h)==1:expected=1 if h[0]==2 else 2
    elif len(h)==2:expected=1 if h==(2,2) else 2
    else:
        vals={b:utility(h+(b,),b) for b in range(p)}
        expected=next(b for b in priority if vals[b]==max(vals.values()))
    assert a==expected,(h,a,expected)

comparisons=0;min_slack=None;min_positive=None;ties=0;root_values=[]
for h in required:
    a=policy[h];actual=replay(h);value=utility(actual,a)
    for b in range(p):
        other=utility(replay(h+(b,)),b)
        slack=value-other
        assert slack>=0,(h,a,b,slack)
        comparisons+=1;ties+=slack==0
        min_slack=slack if min_slack is None else min(min_slack,slack)
        if slack>0:min_positive=slack if min_positive is None else min(min_positive,slack)
        if not h:root_values.append(other)
assert comparisons==1554 and min_slack==0 and min_positive==Fraction(1,12)
assert root_values==[Fraction(11,3),Fraction(15,4),Fraction(41,12),Fraction(11,3),Fraction(11,3),Fraction(41,12)]
path=replay(())
assert path==(1,2,2,2)
assert [path.count(a) for a in range(p)]==certificate['terminal_counts']
values=[utility(path,a) for a in path]
assert values==[Fraction(15,4),Fraction(41,12),Fraction(41,12),Fraction(41,12)]
W=len(coverage(path));assert W==sum(values)==14
all_terminals=list(combinations_with_replacement(range(p),n))
OPT=max(map(lambda s:len(coverage(s)),all_terminals))
optima=[s for s in all_terminals if len(coverage(s))==OPT]
assert OPT==22 and optima==[(0,3,4,5)]
Fs=[];balances=[];prefix_values=[];completion_counts=[]
for t in range(n+1):
    C=coverage(path[:t]);r=n-t
    completions=list(combinations_with_replacement(range(p),r))
    maximum=max(len(C|coverage(s)) for s in completions)
    income=sum(values[:t],Fraction(0))
    Fs.append(maximum);prefix_values.append(income)
    balances.append(income+maximum-OPT);completion_counts.append(len(completions))
assert Fs==[22,18,18,16,14]
assert balances==[Fraction(0),Fraction(-1,4),Fraction(19,6),Fraction(55,12),Fraction(6)]
deltas=[Fs[t-1]-Fs[t] for t in range(1,n+1)]
assert deltas==[4,0,2,2] and sum(deltas)==OPT-W==8
loads=[sum(a in B for a in path[:-1]) for B in customers]
root_tax=sum((Fraction(h,1+h) for h in loads),Fraction(0))
assert root_tax==Fraction(109,12)
root_tax_slack=W+root_tax-OPT
assert root_tax_slack==Fraction(13,12)>0
assert 2*W-OPT==6>0
report={'status':'independent_exact_pass','unit_customers':len(customers),'full_history_nodes':len(required),'action_comparisons':comparisons,'minimum_slack':str(min_slack),'minimum_positive_slack':str(min_positive),'tied_comparisons_including_own_actions':ties,'actual_path':path,'player_payoffs':list(map(str,values)),'root_deviation_payoffs':list(map(str,root_values)),'welfare':W,'terminal_multisets_checked':len(all_terminals),'optimum':OPT,'optimal_multisets':optima,'F_remaining_completion':Fs,'completion_multisets_checked_by_prefix':completion_counts,'prefix_player_payoff_sums':list(map(str,prefix_values)),'prefix_balances':list(map(str,balances)),'opportunity_losses':deltas,'root_tax':str(root_tax),'root_tax_slack':str(root_tax_slack),'half_coverage_slack':2*W-OPT,'scope':'Refutes every-on-path-prefix nonnegative balance and root per-player opportunity payment; does not refute root total tax or half coverage.'}
report['input_sha256']=sha256((ROOT/'examples/customer_attraction/prefix_balance_failure.json').read_bytes()).hexdigest()
report['certificate_sha256']=sha256((ROOT/'evidence/certificates/customer_attraction/prefix_balance_failure.json').read_bytes()).hexdigest()
report['audit_sha256']=sha256(Path(__file__).read_bytes()).hexdigest()
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path)
args=parser.parse_args()
encoded=json.dumps(report,indent=2)+'\n'
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x',encoding='utf-8') as handle:handle.write(encoded)
print(encoded,end='')
