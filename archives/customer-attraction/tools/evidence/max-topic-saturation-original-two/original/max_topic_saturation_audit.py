"""Exact coefficient audit for maximum-topic saturation; not a universal proof.
The companion Markdown supplies the symbolic proof for arbitrary m.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
report={'scope':'algebraic coefficient audit, independent of game solvers','masses':'one unit customer for each provider-incidence mask, checked separately','players_checked':[]}
for m in range(2,15):
 a=Fraction(m-2,m-1);checked=0
 for mask in range(1,1<<m):
  c=mask.bit_count();hasA=bool(mask&1);hasB=bool(mask&2)
  uA=Fraction(hasA,c);uB=Fraction(hasB,c);sizeA=Fraction(hasA);sizeB=Fraction(hasB);d=Fraction(hasA and not hasB)
  D=m*(m-1)*uA-(m-1)*sizeA-d
  F=(sizeB-sizeA)+a*d-(uB-uA)
  assert D>=0 and F>=0,(m,mask,D,F)
  lhs=(m-1)**2*uA-(m-2)*sizeA-uB
  assert lhs==F+a*D+(sizeA-sizeB)
  checked+=1
 report['players_checked'].append({'m':m,'customer_masks':checked,'D_and_F_nonnegative':True,'certificate_identity':True})
# A sharp family for every m: common core 3, A-only cohort 2, B-only cohort 2;
# all other providers copy A. Every action has size 5.
sharp=[]
for m in range(2,15):
 uA=Fraction(3,m)+Fraction(2,m-1);uB=Fraction(3,m)+2;M=5
 assert uB==(m-1)**2*uA-(m-2)*M
 sharp.append({'m':m,'M':M,'uA':str(uA),'uB':str(uB),'slack':'0'})
report['sharp_terminal_family']=sharp
# Floor-only induction obstruction: all 10-subsets of a 21-element universe.
A=frozenset(range(10));B=frozenset(range(8))|{10,11};C=frozenset(range(6))|{8,9,12,13}
path=[A,B,C]
def pay(set_for_player,others):
 return sum((Fraction(1,1+sum(x in t for t in others)) for x in set_for_player),Fraction())
u=[pay(path[i],path[:i]+path[i+1:]) for i in range(3)]
assert u==[4,5,5]
# Last player can choose all 9 uncovered customers and one B-only customer.
uncovered=set(range(21))-(A|B);best=frozenset(uncovered|{10})
assert len(uncovered)==9 and len(best)==10
lastdev=pay(best,[A,B]);assert lastdev==Fraction(19,2)>u[2]
# An explicit three-topic portfolio covers all 21 customers.
portfolio=[frozenset(range(10)),frozenset(range(10,20)),frozenset([20]+list(range(9)))]
assert len(set.union(*(set(t) for t in portfolio)))==21 and all(len(t)==10 for t in portfolio)
report['floor_only_obstruction']={'players':3,'unit_customers':21,'catalog':'all 10-subsets of [21]','maximum_topic_size':10,'root_payoff_cap':4,'global_size_cap':12,'optimum':21,'L':'21/5','constructed_payoffs':list(map(str,u)),'all_follower_payoffs_above_L':all(v>Fraction(21,5) for v in u[1:]),'last_profitable_deviation':str(lastdev),'is_SPE':False,'point':'size cap and follower floors alone do not replace the last-player best-response inequalities'}
HERE.joinpath('max_topic_saturation_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'m_values':len(report['players_checked']),'customer_masks':sum(x['customer_masks'] for x in report['players_checked']),'floor_only_obstruction':report['floor_only_obstruction']},indent=2))
