"""Definition-level audit: no game module, solver, LP, or canonical verifier."""
import argparse,itertools,json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()
instance=json.loads((ROOT/'examples/customer_attraction/optimal_last_query_failure.json').read_text())
certificate=json.loads((ROOT/'evidence/certificates/customer_attraction/optimal_last_query_failure.json').read_text())
data={**instance,**certificate['expected'],
      'policy':[(entry['history'],entry['action']) for entry in certificate['strategy']['actions']]}
p=len(data['topics']);n=data['players']
customers=[(frozenset(c['topics']),c['multiplicity']) for c in data['customers']]
assert all(isinstance(w,int) and w>=0 and B<=set(range(p)) for B,w in customers)
policy={tuple(h):a for h,a in data['policy']}
required={h for depth in range(n) for h in itertools.product(range(p),repeat=depth)}
assert set(policy)==required
assert len(policy)==len(data['policy'])
assert all(a in range(p) for a in policy.values())

def terminal(h):
    result=h
    while len(result)<n:result=result+(policy[result],)
    return result

def utility(profile,a):
    return sum((Fraction(w,sum(b in B for b in profile))
                for B,w in customers if a in B),Fraction(0))

def welfare(profile):
    chosen=set(profile)
    return sum(w for B,w in customers if B & chosen)

minimum=None;comparisons=0;ties=0;root_alternatives=[]
for h in sorted(policy,key=lambda h:(len(h),h)):
    chosen=policy[h];actual=terminal(h);own=utility(actual,chosen)
    for a in range(p):
        alternative=terminal(h+(a,));value=utility(alternative,a)
        slack=own-value
        assert slack>=0,(h,chosen,a,actual,alternative,slack)
        minimum=slack if minimum is None else min(minimum,slack)
        comparisons+=1;ties+=slack==0
        if not h:root_alternatives.append({'topic':a,'terminal':alternative,'payoff':str(value)})

path=terminal(())
values=[utility(path,a) for a in path];W=welfare(path)
assert tuple(data['actual'])==path
assert list(map(str,values))==data['payoffs']
assert W==data['welfare']
assert sum(values)==W
prefix=path[:-1]
last_query=[sum((Fraction(w,1+sum(a in B for a in prefix))
                for B,w in customers if query in B),Fraction(0)) for query in range(p)]
assert last_query[path[-1]]==max(last_query)
assert list(map(str,last_query))==data['last_query_values']
profiles=list(itertools.combinations_with_replacement(range(p),n))
coverages=[welfare(s) for s in profiles]
OPT=max(coverages)
optima=[s for s,w in zip(profiles,coverages) if w==OPT]
query_sums=[sum((last_query[a] for a in s),Fraction(0)) for s in optima]
minimum_query=min(query_sums)
assert OPT==data['optimum']
assert [list(s) for s in optima]==data['optimal_multisets']
assert list(map(str,query_sums))==data['optimal_last_query_sums']
assert minimum_query==Fraction(data['minimum_optimal_last_query_sum'])
assert minimum_query>W
report={'status':'independent_exact_pass','history_nodes':len(policy),'action_comparisons':comparisons,'minimum_slack':str(minimum),'tied_comparisons_including_own_actions':ties,'terminal_multisets':len(profiles),'actual_path':path,'actual_player_payoffs':list(map(str,values)),'welfare':W,'optimum':OPT,'optimal_multisets':optima,'last_query_values':list(map(str,last_query)),'optimal_query_sums':list(map(str,query_sums)),'minimum_optimal_query_sum':str(minimum_query),'minimum_query_sum_minus_W':str(minimum_query-W),'root_alternatives':root_alternatives}
backgrounds=list(itertools.combinations(range(p),n-1))
dual_values=[sum((utility(bg+(a,),a) for bg in backgrounds),Fraction(0))/len(backgrounds) for a in range(p)]
report['uniform_distinct_background_security_cap']=str(max(dual_values))
report['uniform_distinct_background_security_rows']=list(map(str,dual_values))
if args.output:
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as destination:
        destination.write(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
