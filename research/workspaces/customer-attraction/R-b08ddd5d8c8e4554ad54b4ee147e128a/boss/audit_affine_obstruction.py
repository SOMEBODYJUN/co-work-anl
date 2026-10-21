"""Independent ordered-history Fraction audit; does not import the package.
Only the explicitly stated 4-player obstruction is checked.
"""
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path
import json
K=4;M=4;types={1:3,2:1,4:2,7:1,8:2,10:1}
def utility(z,i):
 return sum((F(w,sum(bool(T>>a&1) for a in z)) for T,w in types.items() if T>>z[i]&1),F())
def welfare(z):return sum(w for T,w in types.items() if any(T>>a&1 for a in z))
@lru_cache(None)
def outcomes(h):
 if len(h)==M:return frozenset({h})
 i=len(h);children=[outcomes(h+(a,)) for a in range(K)]
 threshold=max(min(utility(z,i) for z in E) for E in children)
 return frozenset(z for E in children for z in E if utility(z,i)>=threshold)
children=[outcomes((a,)) for a in range(K)]
mins=[min(utility(z,0) for z in E) for E in children]
threshold=max(mins)
assert threshold==F(5,2)
E={(tuple(z.count(a) for a in range(K)),utility(z,0),welfare(z)) for z in children[0]}
assert E=={((2,0,1,1),F(11,6),9),((1,1,1,1),F(10,3),10)}
true_value=min(W for q,p,W in E if p>=threshold)
assert true_value==10
lam=F(2,3)
dual_value=min(F(W)-lam*(p-threshold) for q,p,W in E)
assert dual_value==F(85,9)
assert F(5,9)*F(11,6)+F(4,9)*F(10,3)==threshold
assert F(5,9)*9+F(4,9)*10==dual_value<true_value
report={'status':'PASS_FINITE_EXACT','types':types,'players':M,'topics':K,'root_minima':list(map(str,mins)),'root_threshold':str(threshold),'child0_points':[{'q':q,'p':str(p),'W':W} for q,p,W in sorted(E)],'pure_filtered_min':true_value,'lagrange_lambda':str(lam),'lagrange_max':str(dual_value),'ordered_histories_evaluated':outcomes.cache_info().currsize}
print(json.dumps(report,indent=2))
if __name__=='__main__':Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2))
