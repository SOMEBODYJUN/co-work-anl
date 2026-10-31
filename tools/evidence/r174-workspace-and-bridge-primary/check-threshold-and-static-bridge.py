"""Definition-level exact CAG checks, no imported solver or old program entry."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json

def payoff(catalogue,profile):
    counts=Counter(x for a in profile for x in catalogue[a])
    values=tuple(sum((F(1,counts[x]) for x in catalogue[a]),F(0)) for a in profile)
    assert sum(values)==len(counts)
    return values

def follow(policy,h,m):
    h=tuple(h)
    while len(h)<m:h=h+(policy[h],)
    return h

def check(catalogue,policy,m):
    histories=[h for d in range(m) for h in product(catalogue,repeat=d)]
    assert set(policy)==set(histories)
    rows=[];valid=True
    for h in histories:
        i=len(h);selected=policy[h];out=follow(policy,h,m)
        own=payoff(catalogue,out)[i]
        alternatives={a:payoff(catalogue,follow(policy,h+(a,),m))[i] for a in catalogue}
        valid=valid and own>=max(alternatives.values())
        rows.append({'history':list(h),'action':selected,'actual_terminal':list(out),'actual_current_payoff':str(own),'all_forced_action_payoffs':{a:str(x) for a,x in alternatives.items()}})
    return valid,rows

cat2={'A':frozenset('ab'),'B':frozenset('abc'),'C':frozenset('cd')}
forced={};L={}
for a in cat2:
    last={b:payoff(cat2,(a,b))[1] for b in cat2}
    br=[b for b in cat2 if last[b]==max(last.values())]
    forced[a]=[(a,b) for b in br]
    L[a]=min(payoff(cat2,z)[0] for z in forced[a])
theta=max(L.values());assert L=={'A':F(1),'B':F(3,2),'C':F(3,2)} and theta==F(3,2)
all_spe=[];brute_R=set();checked=0
for root in cat2:
    for replies in product(cat2,repeat=3):
        p={():root,**{(a,):b for a,b in zip(cat2,replies)}}
        good,rows=check(cat2,p,2);checked+=1
        if good:
            z=follow(p,(),2);brute_R.add(z)
            all_spe.append({'root':root,'last_replies':{a:p[(a,)] for a in cat2},'terminal':list(z),'root_payoff':str(payoff(cat2,z)[0])})
predicted={z for a in cat2 for z in forced[a] if payoff(cat2,z)[0]>=theta}
assert checked==81 and len(all_spe)==5 and brute_R==predicted
chosen={():'A',('A',):'C',('B',):'B',('C',):'B'}
good,rows2=check(cat2,chosen,2);assert good
z2=follow(chosen,(),2);u2=payoff(cat2,z2)
assert z2==('A','C') and u2==(F(2),F(2)) and L['A']<theta<=u2[0]

cat3={'A':frozenset('a'),'B':frozenset('ab'),'C':frozenset('bc')}
last={('A','A'):'C',('A','B'):'C',('A','C'):'B',('B','A'):'C',('B','B'):'C',('B','C'):'C',('C','A'):'C',('C','B'):'B',('C','C'):'B'}
policy3={():'C',('A',):'C',('B',):'B',('C',):'A',**last}
good,rows3=check(cat3,policy3,3);assert good
z3=follow(policy3,(),3);u3=payoff(cat3,z3);assert z3==('C','A','C') and u3==(F(1),F(1),F(1))
static=payoff(cat3,('C','B','C'))[1]
dynamic=payoff(cat3,follow(policy3,('C','B'),3))[1]
assert static==F(4,3)>u3[1] and dynamic==F(5,6)<u3[1]
W=F(1);D=F(1);v=F(2);O=F(3)
assert O<=W+v and v<=W+D and D<=W and O>2*W and O<=3*W
result={'status':'passed','arithmetic':'unit-customer Fraction definitions','new_exact_selfcheck_runs':1,'original_source_program_entries':0,'imported_existing_solvers':0,
 'selected_branch_lower_envelope_counterexample':{'catalogue':{a:sorted(s) for a,s in cat2.items()},'players':2,'forced_child_spe_terminals':{a:[list(z) for z in zs] for a,zs in forced.items()},'L':{a:str(x) for a,x in L.items()},'theta':str(theta),'chosen_complete_policy':rows2,'actual_terminal':list(z2),'actual_payoffs':list(map(str,u2)),'welfare':4,'OPT2':4,'false_claim':'L(selected)>=theta','correct_chain':'actual_u>=theta>=L(selected)','complete_strategy_maps_enumerated':checked,'complete_strategy_maps_spe':len(all_spe),'all_spe_complete_policies':all_spe,'actual_full_policy_IC_comparisons_including_stay':checked*4*3,'root_outcomes_from_full_policy_enum':sorted(map(list,brute_R)),'root_outcomes_from_threshold_recursion':sorted(map(list,predicted)),'half_counterexample':False},
 'static_nonPNE_three_player_certificate':{'catalogue':{a:sorted(s) for a,s in cat3.items()},'complete_policy':rows3,'nodes':13,'comparisons_including_stay':39,'nontrivial_alternatives':26,'actual_terminal':list(z3),'actual_payoffs':list(map(str,u3)),'static_player2_deviation_payoff':str(static),'true_player2_deviation_terminal':list(follow(policy3,('C','B'),3)),'true_player2_deviation_payoff':str(dynamic),'welfare':3,'OPT3':3,'half_counterexample':False},
 'smoothness_extra_budget_scalar_limit':{'W':'1','sum_static_deviations':'2','D':'1','comparison_value_O':'3','stated_scalar_inequalities_satisfied':True,'only_implies_three_W':True,'actual_CAG_SPE_counterexample_claimed':False},
 'limits':'Two explicit small catalogues plus a scalar accounting model; not a new all-catalogue half proof/counterexample. Boss6 original certificates/scripts not executed.'}
print(json.dumps(result,ensure_ascii=False,indent=2))
