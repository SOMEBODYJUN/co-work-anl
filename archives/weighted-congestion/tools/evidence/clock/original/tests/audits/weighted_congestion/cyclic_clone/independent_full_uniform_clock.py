#!/usr/bin/env python3
"""Independent literal-resource reconstruction of the degree-80 uniform-clock fixture.
No repository implementation or precomputed cost array is imported.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import argparse, json, hashlib, platform, sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[4])
parser.add_argument('--output', type=Path, help='new JSON output; refuses to overwrite')
args=parser.parse_args()
repo=args.repo.resolve()
input_relative='examples/weighted_congestion/anchored_actual_clock_degree43.json'
INPUT=repo/input_relative
source = json.loads(INPUT.read_text())
w = tuple(F(x) for x in source['weights'])
alpha = F(source['alpha'])
assert w==(F(1),F(1,2),F(1,4),F(1,8)) and alpha==F(21,20)
assert len(source['base_pairs'])==4 and all(p['degree']==3 for p in source['base_pairs'])
states = tuple(product((0,1), repeat=len(w)))

def complement(s):
    return tuple(1-x for x in s)

def flip(s,i):
    return s[:i] + (1-s[i],) + s[i+1:]

def resources_pair(name, literal, coefficient, degree):
    # literal maps each involved player to the action selecting resource 0.
    return [dict(name=name+str(side), required={i:a^side for i,a in literal.items()},
                 coefficient=coefficient, degree=degree) for side in (0,1)]

base = []
for j,p in enumerate(source['base_pairs']):
    literal = {i:(0 if x == 1 else 1) for i,x in enumerate(p['signature']) if x}
    assert all(x in (-1,0,1) for x in p['signature'])
    base += resources_pair('base'+str(j)+'_', literal, F(p['coefficient']), p['degree'])

def costs(resources,s):
    result = [F(0) for _ in w]
    loads = {}
    for resource in resources:
        users = [i for i,action in resource['required'].items() if s[i] == action]
        load = sum((w[i] for i in users), F(0))
        loads[resource['name']] = load
        # Evaluate only genuinely used resources. Thus degree zero is unambiguous
        # even when an unused resource has load zero.
        if users:
            charge = resource['coefficient'] * load**resource['degree']
            for i in users:
                result[i] += charge
    return tuple(result),loads

base_cost = {s:costs(base,s)[0] for s in states}
B = max(c for s in states for c in base_cost[s])
cycle=[]
s=(0,)*len(w)
for i in list(range(len(w)))*2:
    cycle.append((s,i))
    s=flip(s,i)
assert s==(0,)*len(w) and len({s for s,i in cycle}) == 8
eta = min(base_cost[s][i]-alpha*base_cost[flip(s,i)][i] for s,i in cycle)
assert B>0 and 0<eta<=B
triples = tuple((0,)+pair for pair in combinations(range(1,len(w)),2))
L = len(triples)
delta = max(1-min(w[i] for i in T)/sum((w[i] for i in T),F(0)) for T in triples)
M = 2*alpha*B
threshold = eta/(4*alpha**2*B*L)
assert B==F(56643761,70312500) and eta==F(49676111,6750000000)
assert delta==F(12,13) and L==3 and M==F(396506327,234375000)
assert threshold==F(1241902775,1798552699272)
triple_totals={T:sum((w[i] for i in T),F(0)) for T in triples}
assert tuple(triple_totals.values())==(F(7,4),F(13,8),F(11,8))

def clock_resources(degree):
    resources=[]
    for T in triples:
        W=sum((w[i] for i in T),F(0))
        resources += resources_pair('clock'+''.join(map(str,T))+'_', dict(zip(T,(0,1,0))), M/W**degree, degree)
    return resources

D=80
clock=clock_resources(D)
all_resources=base+clock
# Each action is the corresponding resource subset; distinct positive-cost
# literals distinguish the two actions for every player.
strategy_sets={i:tuple(frozenset(r['name'] for r in all_resources if r['required'].get(i)==a) for a in (0,1)) for i in range(len(w))}
assert all(S[0] and S[1] and S[0]!=S[1] for S in strategy_sets.values())
assert len({r['name'] for r in all_resources})==14
assert max(r['degree'] for r in all_resources)==80
assert all(r['coefficient']>0 for r in all_resources)
all_cost={s:costs(all_resources,s)[0] for s in states}
clock_cost={s:costs(clock,s)[0] for s in states}
margin = {(s,i):all_cost[s][i]-alpha*all_cost[flip(s,i)][i] for s in states for i in range(len(w))}
assert len(all_cost)==16 and sum(map(len,all_cost.values()))==64 and len(margin)==64
cycle_states={s for s,i in cycle}
canonical={s:i for s,i in cycle}
for s in states:
    if s in cycle_states:
        continue
    i=next(i for i in range(1,len(w)) if s[i]!=s[0])
    assert any(s[j]==s[0] for j in range(i+1,len(w)))
    canonical[s]=i
assert len(canonical)==16
# Frozen author proof interval table, inspected only after independent audit.
intervals={
 (0,0,0,0):(0,F(7,2000),F(9,2500)),
 (0,0,0,1):(3,F(73,10000),F(37,5000)),
 (0,0,1,0):(2,F(13461,10000),F(6731,5000)),
 (0,0,1,1):(2,F(81,10000),F(41,5000)),
 (0,1,0,0):(1,F(2913,1000),F(29131,10000)),
 (0,1,0,1):(1,F(11699,10000),F(117,100)),
 (0,1,1,0):(1,F(2203,1250),F(141,80)),
 (0,1,1,1):(1,F(101,10000),F(51,5000)),
}
for state,(player,lower,upper) in intervals.items():
    assert canonical[state]==player
    assert F(1,500)<lower<margin[state,player]<upper
assert all(margin[s,i]>0 for s,i in canonical.items())
assert min(margin[s,i] for s,i in cycle)>F(1,500)
assert min(margin[s,i] for s,i in canonical.items() if s not in cycle_states)>1
assert all(any(margin[s,i]>0 for i in range(len(w))) for s in states)
assert all(all_cost[s] == all_cost[complement(s)] for s in states)
assert all(base_cost[s] == base_cost[complement(s)] for s in states)
assert all(clock_cost[s] == clock_cost[complement(s)] for s in states)
assert all(margin[s,i] == margin[complement(s),i] for s in states for i in range(len(w)))
# Check every pair as actual complementary resource usage, and degree/coefficient.
for resources in (base,clock):
    for a,b in zip(resources[::2],resources[1::2]):
        assert a['coefficient']==b['coefficient'] and a['degree']==b['degree']
        for i in a['required']:
            assert a['required'][i] == 1-b['required'][i]
        for s in states:
            for i in a['required']:
                assert int(s[i]==a['required'][i])+int(s[i]==b['required'][i])==1
# The exact sufficient inequality fails at 80, first holds at 91, and back-
# multiplication gives the equivalent nonnegative budget slack sign.
smallest=1
while delta**smallest > threshold:
    smallest+=1
assert delta**0>threshold and delta**80>threshold and smallest==91
assert delta**90>threshold and delta**91<=threshold
assert (4*alpha**2*B*L*delta**80-eta)>0
assert (4*alpha**2*B*L*delta**91-eta)<=0
# Weak and zero boundaries: inequalities, never ratios.
def is_improvement(old,new,a):
    return old > a*new
assert not is_improvement(F(0),F(0),alpha)
assert is_improvement(F(1),F(0),alpha)
assert not is_improvement(alpha,F(1),alpha)
assert is_improvement(alpha+F(1,10**6),F(1),alpha)
# Empty action/zero-cost degree-0 resource under generic literal evaluator.
zero_resource=[dict(name='zero',required={0:0},coefficient=F(0),degree=0)]
assert all(costs(zero_resource,s)[0]==(F(0),)*len(w) for s in states)
# Every alpha-margin is independently reconstructed again from the resources at
# the current and destination states, rather than trusting the precomputed rows.
for (s,i),gap in margin.items():
    assert gap == costs(all_resources,s)[0][i]-alpha*costs(all_resources,flip(s,i))[0][i]

def fmt(x): return str(x)
def state_key(s): return ''.join(map(str,s))
report={
 'scope':'fixed finite input, alpha 21/20, original uniform architecture, D=80; no asymptotic claim',
 'input':input_relative, 'invocation':sys.argv, 'input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'python':platform.python_version(),
 'alpha':fmt(alpha),'weights':list(map(fmt,w)),'base_resource_count':len(base),'clock_resource_count':len(clock),
 'triple_totals':{''.join(map(str,T)):fmt(total) for T,total in triple_totals.items()},
 'B':fmt(B),'eta':fmt(eta),'L':L,'delta':fmt(delta),'M':fmt(M),'degree':D,
 'uniform_budget_threshold':fmt(threshold),'uniform_minimum_degree':smallest,
 'uniform_budget_fails_at80':True,'uniform_budget_succeeds_at91':True,
 'uniform_budget_powers':{str(d):fmt(delta**d) for d in (80,90,91)},
 'uniform_budget_backmultiply_slack':{str(d):fmt(4*alpha**2*B*L*delta**d-eta) for d in (80,90,91)},
 'strategies':{str(i):[sorted(S) for S in pair] for i,pair in strategy_sets.items()},
 'canonical_rational_lower_bounds':{'cycle':'1/500','illegal':'1'},
 'author_frozen_intervals':{state_key(s):{'player':p,'lower':fmt(lo),'upper':fmt(hi)} for s,(p,lo,hi) in intervals.items()},
 'checks':{'all_states':16,'player_costs':64,'deviations':64,'strict_canonical_exits':16,'complement_cost_symmetry':True,'weak_zero_boundaries':True},
 'base_costs':{state_key(s):list(map(fmt,base_cost[s])) for s in states},
 'total_costs':{state_key(s):list(map(fmt,all_cost[s])) for s in states},
 'deviation_margins':{state_key(s):[fmt(margin[s,i]) for i in range(len(w))] for s in states},
 'canonical_exits':{state_key(s):{'player':canonical[s],'kind':'cycle' if s in cycle_states else 'first-opposite','destination':state_key(flip(s,canonical[s])),'margin':fmt(margin[s,canonical[s]])} for s in states},
 'minimum_canonical_margin':fmt(min(margin[s,i] for s,i in canonical.items())),
 'minimum_cycle_margin':fmt(min(margin[s,i] for s,i in cycle)),
 'minimum_illegal_margin':fmt(min(margin[s,i] for s,i in canonical.items() if s not in cycle_states)),
}
if args.output is None:
    print(json.dumps(report,indent=2,ensure_ascii=False))
else:
    with args.output.open('x') as f:
        json.dump(report,f,indent=2,ensure_ascii=False); f.write('\n')
    print(json.dumps({'status':'verified','output':str(args.output),'states':len(states),'player_costs':64,'deviations':64,'strict_canonical_exits':16,'uniform_minimum_degree':smallest},ensure_ascii=False))
