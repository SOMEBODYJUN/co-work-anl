"""Target only fresh-sigma lift, at a three-player local repeat deviation."""
from fractions import Fraction as F
from itertools import product
from math import lcm
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from probe_beta_clone_lift import original_pay,clone_pay

HERE=Path(__file__).parent
TYPES=tuple((B,b) for B in range(1,8) for b in range(3))

def coeff_orig(q,a):
    return [original_pay(((B,b,1),))(q,a) for B,b in TYPES]

def coeff_clone(q,a):
    return [clone_pay(((B,b,1),),3)(q,a) for B,b in TYPES]

def sub(a,b):return [x-y for x,y in zip(a,b)]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def terminal(a,b):
    q=[1,0,0];q[a]+=1;q[b]+=1;return tuple(q)

def main():
    for replies in product(range(3),repeat=3):
        d=[coeff_orig(terminal(a,replies[a]),a) for a in range(3)]
        original_rows=[]
        for a in range(3):
            chosen=coeff_orig(terminal(a,replies[a]),replies[a])
            for t in range(3):
                original_rows.append(sub(chosen,coeff_orig(terminal(a,t),t)))
        for selected in range(3):
            rows=original_rows+[sub(d[selected],v) for v in d]
            for last in [1,2]:
                q=[0]*9;q[0]=2;q[last*3]=1;q=tuple(q)
                gain=sub(coeff_clone(q,0),d[selected])
                last_chosen=coeff_clone(q,last*3)
                strict=[gain]
                # Every other fresh original action and the repeated old clone.
                for other in [1,3,6,0]:
                    if other//3==last:continue
                    z=[0]*9;z[0]=2;z[other]+=1
                    strict.append(sub(last_chosen,coeff_clone(tuple(z),other)))
                A=[[-float(x) for x in row]+[0.] for row in rows]
                A += [[-float(x) for x in row]+[1.] for row in strict]
                c=[0.]*len(TYPES)+[-1.]
                sol=linprog(c,A_ub=A,b_ub=[0.]*len(A),
                            A_eq=[[1.]*len(TYPES)+[0.]],b_eq=[1.],
                            bounds=[(0,None)]*(len(TYPES)+1),method='highs')
                if sol.success and sol.x[-1]>1e-8:
                    w=[F(float(v)).limit_denominator(10**6) for v in sol.x[:-1]]
                    if min(dot(row,w) for row in rows)<0 or min(dot(row,w) for row in strict)<=0:
                        continue
                    den=lcm(*(v.denominator for v in w));wi=[int(v*den) for v in w]
                    out={'status':'exact_local_fresh_lift_counterexample',
                         'types':[(B,b,v) for (B,b),v in zip(TYPES,wi) if v],
                         'prefix_original':0,'original_last_reply_after_current':replies,
                         'original_current_action':selected,'clone_last_reply_original':last,
                         'original_current_payoffs':[str(dot(v,wi)) for v in d],
                         'clone_repeat_payoff':str(dot(coeff_clone(q,0),wi)),
                         'minimum_original_IC':str(min(dot(row,wi) for row in rows)),
                         'minimum_strict_gain_or_reply_margin':str(min(dot(row,wi) for row in strict))}
                    (HERE/'beta_clone_local_lift_attack.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));return
    out={'status':'no_separation_in_exact_local_template',
         'scope':'Finite template computation only, not a proof or negative evidence.'}
    (HERE/'beta_clone_local_lift_attack.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))

if __name__=='__main__':main()
