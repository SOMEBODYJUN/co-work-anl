"""Fixed 31-client saved-input certificate; standard library, no discovery/LP.

Rebuild full two-player best replies and all SPE count outcomes.  Certify
the unique exact safety-optimal query and its static aggregate cost > W.
The supplied 1000/2419/etc random searches are never replayed/imported.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

here = Path(__file__).resolve().parent
source = here/'original/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/security_aggregate/static_regret_k6n2.json'
assert hashlib.sha256(source.read_bytes()).hexdigest() == 'ad55fdba240babd7d1448a3a4526595dc500617bf571028ea420798324dc2d96'
raw = json.loads(source.read_text())
best = raw['best']
w = {i+1:n for i,n in enumerate(best['weights']) if n}
assert w == {11:3,12:3,14:1,26:1,37:8,47:14,49:1}
assert best['k']==6 and best['n']==2 and sum(w.values())==31
catalog = range(6)
member = lambda mask,a: (mask>>a)&1
size = [sum(n*member(mask,a) for mask,n in w.items()) for a in catalog]
# F[B][a] is the query a against one fixed competitor B.
matrix = [[sum((F(n*member(mask,a),1+member(mask,B)) for mask,n in w.items()),F(0))
           for a in catalog] for B in catalog]
assert size == [26,19,26,22,2,23]
last_actions = [2,2,0,0,2,3]
br = [[a for a in catalog if matrix[B][a] == max(matrix[B])] for B in catalog]
assert br == [[2],[2],[0],[0],[2],[2,3]]
chosen_root = 5
ordered_leaf = [5,3]
assert last_actions[chosen_root] == ordered_leaf[1]
root_values = [matrix[last_actions[a]][a] for a in catalog]
assert root_values == list(map(F,[15,F(23,2),15,F(27,2),2,16]))
assert chosen_root in [a for a in catalog if root_values[a] == max(root_values)]
checks = []
for h,chosen,values in [((),chosen_root,root_values)]+[((B,),last_actions[B],matrix[B]) for B in catalog]:
    for a in catalog:
        slack = values[chosen]-values[a]
        assert slack>=0
        checks.append({'history':list(h),'prescribed':chosen,'alternative':a,
                       'prescribed_profit':str(values[chosen]),'alternative_profit':str(values[a]),
                       'slack':str(slack),'self':a==chosen})
assert len(checks)==42
assert sum(c['slack']!='0' for c in checks)==34
assert sum(c['slack']=='0' and not c['self'] for c in checks)==1
# Exhaustive full two-player strategy choices: each last node must choose a BR;
# children have disjoint histories, so their tied choices are independent.
policies = []
outcomes = set()
for replies in product(*br):
    values = [matrix[replies[a]][a] for a in catalog]
    for a in catalog:
        if values[a] == max(values):
            counts = tuple(int(t==a)+int(t==replies[a]) for t in catalog)
            outcomes.add(counts)
            policies.append({'root':a,'last_by_prefix':list(replies),'ordered_leaf':[a,replies[a]],'counts':list(counts)})
assert len(policies)==3 and len(outcomes)==best['root_outcomes']==2
assert tuple(best['terminal']) in outcomes
assert outcomes == {(1,0,1,0,0,0),(0,0,0,1,0,1)}
cover = lambda z:sum(n for mask,n in w.items() if any(member(mask,a) for a in z))
W = cover(ordered_leaf)
assert W==sum(w.values())==F(str(best['welfare']))==31
profits = [matrix[ordered_leaf[1-i]][ordered_leaf[i]] for i in range(2)]
assert profits == [16,15]
OPT = max(cover([a,b]) for a,b in product(catalog,repeat=2))
assert OPT==31
assert all(sum(n for mask,n in w.items() if member(mask,a)!=member(mask,b))>0
           for a,b in product(catalog,repeat=2) if a!=b)
p = [F(1,2),F(0),F(1,2),F(0),F(0),F(0)]
Q = p[:]
query_values = [sum((p[a]*matrix[B][a] for a in catalog),F(0)) for B in catalog]
dual_values = [sum((Q[B]*matrix[B][a] for B in catalog),F(0)) for a in catalog]
assert query_values == [14,18,14,F(69,4),F(103,4),F(59,4)]
assert dual_values == [14,11,14,F(53,4),F(7,4),F(47,4)]
assert min(query_values)==max(dual_values)==F(str(best['security']))==14
# Every optimal p' must be supported on query columns where Q has value 14.
# Thus support(p') subset {0,2}; opponent 0 gives 15-2p0 >=14,
# opponent 2 gives 13+2p0 >=14, hence p0=1/2. No approximate rank test.
assert [a for a,v in enumerate(dual_values) if v==14] == [0,2]
assert matrix[0][0]==13 and matrix[0][2]==15
assert matrix[2][0]==15 and matrix[2][2]==13
static_costs = [matrix[3][a]+matrix[5][a] for a in catalog]
assert static_costs == list(map(lambda a:F(str(a)),best['regret_values']))
assert static_costs == [32,F(43,2),32,26,3,F(55,2)]
minimum = sum((p[a]*static_costs[a] for a in catalog),F(0))
assert minimum==32 and minimum-W==1
print(json.dumps({'status':'PASS','scope':'one saved 31-unit-client game; exact full two-player SPE and all safety-optimal query distributions; not original random/LP replay',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'nonzero_weights':{str(m):n for m,n in w.items()},'customers':sum(w.values()),'theme_sizes':size,
 'payoff_matrix_rows_opponent_columns_query':[[str(v) for v in row] for row in matrix],
 'last_best_replies':br,'new_explicit_complete_strategy':{'root':5,'last_by_prefix':last_actions,'ordered_leaf':ordered_leaf},
 'actual_profits':list(map(str,profits)),'welfare':W,'OPT2':OPT,'all_spe_count_outcomes':[list(x) for x in sorted(outcomes)],
 'all_complete_two_player_SPE_policies':policies,'IC_comparisons_including_self':42,'proper_comparisons':35,
 'strict_proper':34,'tied_proper':1,'comparisons':checks,
 'p':list(map(str,p)),'Q':list(map(str,Q)),'query_values_by_opponent':list(map(str,query_values)),
 'dual_values_by_query':list(map(str,dual_values)),'security_value':'14',
 'whole_optimal_face':'strict dual slack excludes columns 1,3,4,5; opponent rows 0 and 2 force p0=p2=1/2',
 'optimal_face_is_singleton':True,'static_aggregate_costs':list(map(str,static_costs)),
 'minimum_over_entire_safety_optimal_face':str(minimum),'SSR_violation':str(minimum-W),
 'strong_aggregate_security_margin':str(W-2*14),'half_margin':str(2*W-OPT),
 'original_float_minimum':best['minimum_static_aggregate'],'original_float_gap':best['gap']},ensure_ascii=False,indent=2))
