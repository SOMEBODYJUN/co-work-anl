"""Exact audit: aggregate child-profit state does not suffice for half induction.

Standard library only. Encodes 61 distinct unit customers by multiplicity, verifies
one genuine complete four-player SPE, and separately verifies a non-SPE menu.
The menu is a relaxation countermodel, never an SPE counterexample.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json

LABELS = 'ABCDEF'
TYPES = [('A',12),('B',8),('C',4),('D',8),('AE',6),('AF',6),
         ('CE',3),('CF',3),('AEF',6),('BEF',2),('CEF',1),('DEF',2)]
N = [(frozenset(LABELS.index(x) for x in s), n) for s,n in TYPES]

def pay(profile):
    answer = [F(0) for _ in profile]
    for liked,n in N:
        c = sum(t in liked for t in profile)
        if c:
            for j,t in enumerate(profile):
                if t in liked: answer[j] += F(n,c)
    return tuple(answer)

def welfare(profile):
    return sum(n for liked,n in N if any(t in liked for t in profile))

def optimum_profit(prefix, r):
    best = F(0); arg = ()
    for q in combinations_with_replacement(range(6), r):
        value = F(0)
        for liked,n in N:
            b = sum(t in liked for t in prefix)
            c = sum(t in liked for t in q)
            if c: value += F(n*c,b+c)
        if value > best: best,arg = value,q
    return best,arg

# Genuine complete SPE: first three always A; final BR priority F>E>D>C>B>A.
def actual_action(h):
    if len(h)<3: return 0
    return max(range(6), key=lambda t:(pay(h+(t,))[-1],t))

def actual_terminal(h):
    while len(h)<4: h += (actual_action(h),)
    return h

def audit():
    nodes=comparisons=0
    for depth in range(4):
        for h in product(range(6),repeat=depth):
            out=actual_terminal(h);u=pay(out)[depth];nodes+=1
            for a in range(6):
                other=actual_terminal(h+(a,));comparisons+=1
                assert u >= pay(other)[depth], (h,a,u,pay(other)[depth])
    root=actual_terminal(());u=pay(root)
    full,fullarg=optimum_profit((),4)
    child,childarg=optimum_profit((0,),3)
    assert full==61 and child==36 and u[0]==9
    genuine={
       'nodes':nodes,'comparisons_including_chosen':comparisons,
       'actual_profile':''.join(LABELS[a] for a in root),
       'payoffs':[str(x) for x in u], 'welfare':welfare(root),
       'F4':str(full),'F3_after_A':str(child),
       'local_loss':str(full-child),'twice_root_payoff':str(2*u[0]),
       'local_bridge_deficit':str(full-child-2*u[0]),
       'actual_child_half_slack':str(2*sum(u[1:])-child),
       'whole_half_slack':str(2*sum(u)-full)}
    # This menu only asserts aggregate child guarantees and root incentives.
    # It deliberately omits child incentive compatibility.
    tails=((0,0,0),(0,0,1),(0,0,2),(0,0,3),(0,4,4),(0,5,5))
    rows=[]
    for a,tail in enumerate(tails):
        profile=(a,)+tail; us=pay(profile);f,arg=optimum_profit((a,),3)
        pt=sum(us[1:]);assert pt >= F(5,8)*f
        rows.append({'root':LABELS[a],'tail':''.join(LABELS[x] for x in tail),
          'root_payoff':str(us[0]),'tail_profit':str(pt),'F3':str(f),
          'F3_maximizer':''.join(LABELS[x] for x in arg),
          'tail_to_F3':str(pt/f),'slack_above_3_over_5':str(pt-F(3,5)*f)})
    assert all(F(row['root_payoff'])<=F(15,2) for row in rows)
    assert welfare((0,0,0,0))==30 and 2*30<full
    chosen=pay((0,0,0,0))[-1];dev=pay((0,0,0,2))[-1]
    assert chosen==F(15,2) and dev==11
    return {'scope':'Exact relaxation obstruction, not a half-coverage SPE counterexample',
      'genuine_complete_SPE':genuine,'non_SPE_menu':rows,
      'menu_root_payoff':str(F(15,2)),'menu_welfare':30,
      'menu_all_child_ratios_at_least':str(F(5,8)),
      'failed_child_history':'AAA','prescribed_last_action':'A',
      'last_chosen_payoff':str(chosen),'last_profitable_deviation':'C',
      'last_deviation_payoff':str(dev)}

if __name__=='__main__': print(json.dumps(audit(),ensure_ascii=False,indent=2))
