"""Independent-of-solver exact audit of the five-client collision-free SPE.
This script hardcodes four actual subsets of five distinct unit clients.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).parent
# Clients x0,x1 share topics 0,1,2; a likes only 0; b likes 1,3; d likes only 3.
topics=({0,1,2},{0,1,3},{0,1},{3,4})
follower=(1,0,3,0);root_action=2

def utility(path,i):
 return sum((Fraction(1,sum(x in topics[a]for a in path))for x in topics[path[i]]),Fraction(0))
def coverage(path):return len(set().union(*(topics[a]for a in path)))
def finish(h):
 if not h:h=(root_action,)
 if len(h)==1:h=h+(follower[h[0]],)
 return h
slacks=[];followers=[]
for a in range(4):
 pay=[utility((a,b),1)for b in range(4)];assert pay[follower[a]]==max(pay);followers.append([str(v)for v in pay]);slacks.extend(pay[follower[a]]-v for v in pay)
rootpay=[utility(finish((a,)),0)for a in range(4)];assert rootpay[root_action]==max(rootpay);slacks.extend(rootpay[root_action]-v for v in rootpay)
actual=finish(());loads=[sum(x in topics[a]for a in actual)for x in range(5)];opt=max(coverage(path)for path in product(range(4),repeat=2));phi=sum((sum((Fraction(1,j)for j in range(1,c+1)),Fraction(0))for c in loads),Fraction(0));assert len(set(topics[actual[0]])&set(topics[actual[1]]))==0
result={'unit_clients':5,'topics':[sorted(t)for t in topics],'root':root_action,'follower':follower,'follower_payoff_matrix':followers,'root_payoffs':[str(v)for v in rootpay],'actual':actual,'payoffs':[str(utility(actual,i))for i in range(2)],'W':coverage(actual),'OPT':opt,'optimal_paths':[path for path in product(range(4),repeat=2)if coverage(path)==opt],'load_histogram':{str(c):loads.count(c)for c in sorted(set(loads))},'Phi':str(phi),'two_layer_occupancy':sum(min(c,2)for c in loads),'histories':5,'comparisons':len(slacks),'nonself_comparisons':15,'strict_comparisons':sum(s>0 for s in slacks),'minimum_slack':str(min(slacks))}
assert result['W']==4 and opt==5 and phi==4
print(json.dumps(result,indent=2));(ROOT/'collision_free_obstruction_audit.json').write_text(json.dumps(result,indent=2)+'\n')
