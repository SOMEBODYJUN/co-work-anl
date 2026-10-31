from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json,sys
o=json.loads(Path(sys.argv[1]).read_text());p=len(o['topics']);clients=o['customers']
assert o['players']==3 and p==6 and len(clients)==7 and o['static_competitors']==3
likes=[set(x['likes']) for x in clients]
def query(a,bg):
 return sum((Q(1,1+sum(t in B for t in bg)) for B in likes if a in B),Q(0))
backgrounds=list(product(range(p),repeat=3))
values=[sum((query(a,bg) for bg in backgrounds),Q(0))/len(backgrounds) for a in range(p)]
assert values==[Q(665,432)]*6
z=o['selected_actual_path']
profits=[sum((Q(1,sum(t in B for t in z)) for B in likes if a in B),Q(0)) for a in z]
assert profits==[Q(3,2),Q(5,2),Q(2)]
def cover(z):return sum(any(t in B for t in z) for B in likes)
w=cover(z);opt=max(cover(v) for v in backgrounds);assert (w,opt)==(6,7)
qvalues=[sum((query(a,bg) for bg in o['upper_bound_Q_backgrounds']),Q(0))/2 for a in range(p)]
assert qvalues==[Q(4,3)]*6
assert values[0]-profits[0]==Q(17,432)>0
print(json.dumps(dict(exact=True,unit_customers=7,topics=6,static_iid_competitor_backgrounds=len(backgrounds),pure_queries=6,unit_share_query_evaluations=len(backgrounds)*6,iid_query_payoffs=list(map(str,values)),iid_common_Nash_payoff=str(values[0]),all_pure_payoffs_equal=True,selected_actual_path=z,selected_actual_profits=list(map(str,profits)),selected_actual_W=w,OPT3_by_all_ordered_tuples=opt,lambda_minus_selected_root=str(values[0]-profits[0]),explicit_two_background_Q_query_payoffs=list(map(str,qvalues)),SPE_history_checks=0,bank_original_SPE_program_runs=0,scope='New definition-level static arithmetic on one explicit input; complete SPE proven separately in prose; not a general search or proof of minimum size'),indent=2))
