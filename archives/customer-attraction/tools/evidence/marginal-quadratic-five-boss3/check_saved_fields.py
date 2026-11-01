"""Finite SAVED-data arithmetic only, not either original random program.

100 withdrawn full-customer curve records: static curve/payoff/gap fields only.
One saved quadratic game: exact6x6 security/dominance and support-payment test.
No BI, random generation, LP, canonical package or full-strategy certification.
"""
import ast
import collections
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
inputs=[]


def read(name):
    p=HERE/'original'/name;b=p.read_bytes();inputs.append(dict(path=str(p),size=len(b),sha256=hashlib.sha256(b).hexdigest()))
    return json.loads(b)


old=read('probe_k6_m3.json');later=read('probe_k7_m4.json');quad=read('quadratic_k6_m3.json')
assert set(old)==set(later)=={'status','args','violations','elapsed_seconds'}
assert old['args']==dict(seed=1,games=100,topics=6,players=3,out='probe_k6_m3.json')
assert later['args']==dict(seed=1,games=1000,topics=7,players=4,out='probe_k7_m4.json')and later['violations']==[]
records=old['violations'];assert len(records)==100 and [r['trial']for r in records]==list(range(100))
checked=[];weight_counts=[];totals=[];depths=collections.Counter()
for r in records:
    assert set(r)=={'players','topics','weights','target','prefix','action','residual','curve','payoff','gap','trial'}
    k=r['topics'];m=r['players'];assert(k,m)==(6,3)and r['residual']is False
    w={int(mask):n for mask,n in r['weights'].items()}
    assert len(w)==len(r['weights'])and all(1<=mask<(1<<k)and type(n)is int and n>0 for mask,n in w.items())
    s=r['target'];q=r['prefix'];a=r['action']
    assert len(s)==len(q)==k and sum(s)==m and all(type(x)is int and x>=0 for x in s+q)
    assert sum(q)<m and all(x<=y for x,y in zip(q,s))and type(a)is int and 0<=a<k and q[a]<s[a]
    curve=[0]
    for j in range(1,m+1):
        curve.append(max(sum(n for mask,n in w.items()if mask&sum(1<<b for b in J))for J in itertools.combinations(range(k),min(j,k))))
    value=sum((F(n,sum(s[b]for b in range(k)if mask>>b&1))for mask,n in w.items()if mask>>a&1),F(0))
    rem=m-sum(q);gap=curve[rem]-curve[rem-1]
    assert r['curve']==curve and F(r['payoff'])==value and r['gap']==gap and value<gap
    checked.append(dict(trial=r['trial'],remaining_players=rem,target=s,prefix=q,action=a,recomputed_full_curve=curve,recomputed_payoff=str(value),gap=gap,strict_shortfall=str(gap-value),static_fields_match=True,equilibrium_reachability_or_full_policy_not_reverified=True))
    weight_counts.append(len(w));totals.append(sum(w.values()));depths[sum(q)]+=1

src=(HERE/'original/marginal_curve_probe.py').read_bytes();inputs.append(dict(path=str(HERE/'original/marginal_curve_probe.py'),size=len(src),sha256=hashlib.sha256(src).hexdigest()))
loops=[n for n in ast.walk(ast.parse(src))if isinstance(n,ast.For)and isinstance(n.target,ast.Name)and n.target.id=='residual']
assert len(loops)==1 and ast.literal_eval(loops[0].iter)==(True,)

assert set(quad)=={'status','args','best','elapsed_seconds'}and quad['args']==dict(games=5000,topics=6,players=3,seed=19,out='quadratic_k6_m3.json')
z=quad['best'];assert set(z)=={'welfare','security','gap','worst_counts','query','G','h','trial'}
G=z['G'];h=z['h'];k=len(h);m=3
assert k==6 and len(G)==k and all(len(r)==k for r in G)and all(type(x)is int for r in G for x in r)and all(type(x)is int for x in h)
assert all(G[a][a]==10 and 0<=G[a][b]<=10 and G[a][b]==G[b][a]for a in range(k)for b in range(k))
assert all(x>=20 for x in h)and z['trial']==967
V=[[h[a]-2*G[a][b]for b in range(k)]for a in range(k)]
dominance=[[V[3][b]-V[a][b]for b in range(k)]for a in range(k)]
assert all(x>=0 for r in dominance for x in r)and min(V[3])==14
query=[F(1,2)if a in [0,3]else F(0)for a in range(k)]
query_values=[sum(query[a]*V[a][b]for a in range(k))for b in range(k)]
dual_column=[V[a][3]for a in range(k)]
assert query_values==[14,23,22,14,14,15]and max(dual_column)==14


def payoff(s,a):return h[a]-sum(G[a][b]*(s[b]-int(a==b))for b in range(k))


def total(s):return sum(s[a]*payoff(s,a)for a in range(k))


all3=[0,0,0,3,0,0];s1=[2,0,0,1,0,0];s2=[1,0,0,2,0,0]
assert z['worst_counts']==all3 and payoff(all3,3)==14 and total(all3)==z['welfare']==42
assert total(s1)==42 and total(s2)==46
out=dict(kind='saved finite arithmetic; no random programs, BI or LP replay',inputs=inputs,marginal=dict(saved_old_records=100,all_residual_false=True,current_source_residual_loop=[True],old_schema_branch_not_current_entry_output=True,all_static_fields_match=True,records=checked,prefix_depth_counts=dict(depths),type_count_minmax=[min(weight_counts),max(weight_counts)],customer_count_minmax=[min(totals),max(totals)],payoff_denominators_in_original=[6],full_strategies_or_reachability_not_certified=True,later_k7m4_requested_games=1000,later_k7m4_saved_violations=[],later_actual_nonempty_game_count_not_saved=True),quadratic=dict(saved_G=G,saved_h=h,V_query_against_two_same_opponents=V,action3_minus_other_rows=dominance,action3_weakly_dominant_against_all_two_opponent_counts=True,exact_replacement_query=list(map(str,query)),replacement_query_values=list(map(str,query_values)),opponents_both3_column=dual_column,exact_security='14',all3_complete_strategy_SPE_by_dominance=True,every_SPE_player_guarantee='14',exact_worst_total_payments='42',exact_gap='0',same_support_counts=[s1,s2],same_support_total_payments=[42,46],not_a_common_unit_customer_payoff_array_even_on_fixed_three_player_layer=True,reported_float_security=z['security'],reported_float_gap=z['gap'],floating_query_not_claimed_exact_primal=True,other4999_games_not_replayed=True),original_entry_or_RNG_BI_LP_runs=0)
(HERE/'saved-field-review.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(status='passed',old_full_curve_records_checked=100,residual_records=0,quadratic_security_exact='14',quadratic_worst_payments_exact='42',quadratic_gap_exact='0',same_support_payments=[42,46],original_RNG_BI_LP_runs=0)))
