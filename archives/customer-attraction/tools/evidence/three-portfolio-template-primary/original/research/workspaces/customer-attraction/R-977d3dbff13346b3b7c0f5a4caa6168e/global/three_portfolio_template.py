"""Universal membership LP for m=3 true-portfolio inequality.

Named themes are A,B,C,T_j,L_j,Q_j,R_j (j=0,1,2). Every L/R is
the real terminal reply at (A,T_j)/(T_j,Q_j), while Q_j is the real
second action after T_j. The target uses exactly the three actual-prefix
true deviation values; no response is frozen.
"""
from itertools import product
from pathlib import Path
from fractions import Fraction
import json,sys
import numpy as np
from scipy.optimize import linprog

def main():
    arr=np.asarray(list(product([0,1],repeat=15)),dtype=float).T
    A,B,C=arr[:3];T=arr[3:6];L=arr[6:9];Q=arr[9:12];R=arr[12:15]
    z=np.zeros(1<<15)
    def u(X,Y,Z):return X/(1+Y+Z)
    actual=[u(A,B,C),u(B,A,C),u(C,A,B)]
    W=np.minimum(1,A+B+C);O=np.minimum(1,T.sum(axis=0))
    V1=sum(u(T[j],Q[j],R[j]) for j in range(3))
    V2=sum(u(T[j],A,L[j]) for j in range(3))
    V3=sum(u(T[j],A,B) for j in range(3))
    weak='--weak' in sys.argv
    target=(3 if weak else 2)*W+V1+V2+V3-3*O
    # Symmetric sums retain all comparison indices simultaneously.
    groups={'A':[A],'B':[B],'C':[C],'T':T,'L':L,'Q':Q,'R':R}
    rows=[];names=[]
    def add(name,row):
        if np.max(np.abs(row))>1e-14:names.append(name);rows.append(row)
    for name,Xs in groups.items():
        add('C_vs_'+name,sum(actual[2]-u(X,A,B) for X in Xs))
        add('B_floor_'+name,sum(actual[1]-X/(A+2) for X in Xs))
        add('A_floor_'+name,sum(actual[0]-X/3 for X in Xs))
        add('L_all_vs_'+name,sum(u(L[j],A,T[j])-u(X,A,T[j]) for j in range(3) for X in Xs))
        add('R_all_vs_'+name,sum(u(R[j],T[j],Q[j])-u(X,T[j],Q[j]) for j in range(3) for X in Xs))
        add('Q_floor_'+name,sum(u(Q[j],T[j],R[j])-X/(T[j]+2) for j in range(3) for X in Xs))
    add('A_true_T',3*actual[0]-V1)
    add('B_true_T',3*actual[1]-V2)
    add('C_true_T',3*actual[2]-V3)
    for X,name in [(T,'T'),(L,'L'),(Q,'Q'),(R,'R')]:
        add('L_own_vs_'+name,sum(u(L[j],A,T[j])-u(X[j],A,T[j]) for j in range(3)))
        add('R_own_vs_'+name,sum(u(R[j],T[j],Q[j])-u(X[j],T[j],Q[j]) for j in range(3)))
        add('Q_floor_own_'+name,sum(u(Q[j],T[j],R[j])-X[j]/(T[j]+2) for j in range(3)))
    terminal_only='--terminal-only' in sys.argv
    if terminal_only:
        use=[i for i,name in enumerate(names) if name.startswith(('C_vs_','L_','R_'))]
        names=[names[i] for i in use];rows=[rows[i] for i in use]
    matrix=np.asarray(rows).T
    optimize_beta='--optimize-beta' in sys.argv
    if optimize_beta:
        result=linprog(np.r_[np.zeros(len(rows)),1],A_ub=np.column_stack([matrix,-W]),
            b_ub=V1+V2+V3-3*O,bounds=(0,None),method='highs')
    else:
        result=linprog(np.ones(len(rows)),A_ub=matrix,b_ub=target,
            bounds=(0,None),method='highs')
    report={'m':3,'membership_patterns':len(target),'slack_rows':len(rows),
        'target':('beta' if optimize_beta else ('3' if weak else '2'))+'W + sum(V_i,j) - 3O',
        'terminal_only':terminal_only,'status':result.message}
    if result.success:
        multipliers={name:str(Fraction(float(x)).limit_denominator(10**6))
                     for name,x in zip(names,result.x) if x>1e-8}
        report['candidate_multipliers']=multipliers
        if optimize_beta:
            report['candidate_beta']=str(Fraction(float(result.x[-1])).limit_denominator(10**6))
            target=result.x[-1]*W+V1+V2+V3-3*O
        report['min_float_residual']=float(np.min(target-matrix@result.x[:len(rows)]))
    print(json.dumps(report,indent=2))
    Path(__file__).with_name('three_portfolio_template'+('_terminal' if terminal_only else '')+('_optimized' if optimize_beta else ('_weak' if weak else ''))+'.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
