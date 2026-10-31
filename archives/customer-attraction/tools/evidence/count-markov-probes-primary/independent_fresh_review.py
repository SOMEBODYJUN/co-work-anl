"""Exact independent enumeration of the saved auxiliary discovery, not CAG.

No original probe/compiler/solver is imported. The output includes all pair
menus, all global last maps, a complete legal fresh-history witness, and exact
checks. It does not compile new customers or assert a welfare counterexample.
"""
from pathlib import Path
from itertools import combinations,product
from functools import lru_cache
import json

E=Path(__file__).resolve().parent
raw=json.loads((E/'replay-fresh/stdout.txt').read_text())
phi={frozenset(map(int,k.split(','))):v for k,v in raw['phi'].items()}
P=tuple(range(6));m=3
assert len(phi)==35 and raw['trial']==205
assert {len(s) for s in phi}=={2,3}
def payoff(s,a):return phi[s]-phi[s-{a}]
def fresh(s):return tuple(a for a in P if a not in s)
def label(s):return ''.join(map(str,sorted(s)))

@lru_cache(None)
def outcomes(s):
    if len(s)==m:return frozenset([s])
    children={a:outcomes(s|{a}) for a in fresh(s)}
    floor=max(min(payoff(z,a) for z in children[a]) for a in children)
    return frozenset(z for a in children for z in children[a] if payoff(z,a)>=floor)

target=frozenset([0,2,5]);assert target in outcomes(frozenset())
policy={}
def build(h,z):
    if len(h)==m:return
    s=frozenset(h);choices=fresh(s)
    punish={a:min(outcomes(s|{a}),key=lambda z:(payoff(z,a),tuple(sorted(z)))) for a in choices}
    floor=max(payoff(punish[a],a) for a in choices)
    a=next(a for a in choices if z in outcomes(s|{a}) and payoff(z,a)>=floor)
    policy[h]=a
    for b in choices:build(h+(b,),z if b==a else punish[b])
build((),target)
assert len(policy)==37
count=nonself=ties=0;minimum=None
def verify(h):
    global count,nonself,ties,minimum
    if len(h)==m:return frozenset(h)
    children={a:verify(h+(a,)) for a in fresh(frozenset(h))}
    a=policy[h];own=payoff(children[a],a)
    for b,z in children.items():
        gap=own-payoff(z,b);assert gap>=0
        count+=1;nonself+=a!=b;ties+=gap==0
        minimum=gap if minimum is None else min(minimum,gap)
    return children[a]
assert verify(())==target and count==156 and nonself==119

pairs=tuple(map(frozenset,combinations(P,2)))
menus={s:tuple(a for a in fresh(s) if payoff(s|{a},a)==max(payoff(s|{b},b) for b in fresh(s))) for s in pairs}
maps=[];allroots=set();second_count=0
for seq in product(*(menus[s] for s in pairs)):
    last=dict(zip(pairs,seq));seconds={}
    for a in P:
        values={b:payoff(frozenset([a,b,last[frozenset([a,b])]]),b) for b in P if b!=a}
        seconds[a]=tuple(b for b in values if values[b]==max(values.values()))
    local=set()
    for bs in product(*(seconds[a] for a in P)):
        second_count+=1
        terms={a:frozenset([a,bs[a],last[frozenset([a,bs[a]])]]) for a in P}
        scores={a:payoff(terms[a],a) for a in P}
        local.update(terms[a] for a in P if scores[a]==max(scores.values()))
    allroots.update(local)
    maps.append({'last':{label(s):last[s] for s in pairs},'root_sets':sorted(map(label,local))})
full=outcomes(frozenset());assert target not in allroots
assert {label(s) for s in full-allroots}=={''.join(map(str,z)) for z in raw['onlyfull']}
assert allroots<=full
out={'status':'pass','scope':'six-topic three-player no-repeat auxiliary subset-potential game only',
 'original_main_runs':0,'new_independent_script_runs':1,'timing_recorded':False,'solver_calls':0,
 'original_imports':False,'CAG_customers_compiled':False,'trial':raw['trial'],'phi':raw['phi'],
 'full_root_sets':sorted(map(label,full)),'count_uniform_root_sets':sorted(map(label,allroots)),
 'only_full':sorted(map(label,full-allroots)),
 'last_pair_menus':{label(s):menus[s] for s in pairs},'all_last_maps':len(maps),
 'second_maps_exhausted':second_count,'last_map_results':maps,
 'explicit_full_fresh_policy':[{'history':list(h),'action':a} for h,a in sorted(policy.items(),key=lambda z:(len(z[0]),z[0]))],
 'complete_legal_fresh_decision_nodes':len(policy),'comparisons_including_self':count,
 'comparisons_excluding_self':nonself,'ties_including_self':ties,'minimum_IC_margin':minimum,
 'not_a_complete_unrestricted_CAG_policy':True,'not_a_half_counterexample':True}
(E/'independent-fresh-review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['phi','last_pair_menus','last_map_results','explicit_full_fresh_policy']},ensure_ascii=False))
