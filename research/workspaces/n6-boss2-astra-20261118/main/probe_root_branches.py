from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json, sys
import numpy as np
from scipy.optimize import linprog
import sympy as sp

def system(tau, source, include_opt):
    # One separately played branch. The forced label is maximum-cardinality.
    branch_labels = (*range(source), *range(6, 12-source))
    types = list(product(product((0,1),repeat=12-source),(0,1)))
    matrix = []
    goal = []
    welfare = []
    for bits,o in types:
        e=bits[:6]; v=tuple(bits[i] for i in branch_labels); maximum=bits[6]
        r={}
        payoff=[]
        floor=[]
        for label,word,start in (('A',e,0),('B',v,source+1)):
            c=sum(word); p=sum(word[:4]); a=word[4]; D=(p+1)*(p+2)
            u=[Q(q,c) if c else Q(0) for q in word]
            payoff.append(u)
            floor.append([sum(word[:i])+6-i for i in range(6)])
            for i in range(start,6):
                b=sum(word[:i])
                r[f'{label}-F{i+1}']=tau*u[i]-Q(o,b+6-i)
                for j,t in enumerate(bits):r[f'{label}-H{i+1}-{j+1}']=u[i]-Q(t,b+6-i)
            for eta in (Q(0),Q(1,6),Q(1,5),Q(1,4),Q(1,3),Q(1,2),Q(1)):
                r[f'{label}-R{eta}']=tau*u[4]+eta*u[5]-o*min(Q(1,p+1),Q(1,p+2)+eta/(p+a+1))
            r[f'{label}-PAIR']=u[4]+u[5]+Q(a,D)-o*(Q(2)/(tau*(p+1))-Q(1)/(tau*tau*D))
            for j,t in enumerate(bits):
                r[f'{label}-MIXED-{j+1}']=u[4]+u[5]+Q(a,D)-Q(t,p+1)-Q(o)/tau*(Q(1,p+1)-Q(t,D))
        for j,t in enumerate(bits):r[f'CAP-{j+1}']=maximum-t
        r['CAP-opt']=tau*maximum-o
        r['BRANCH-IC']=payoff[0][source]-payoff[1][source]
        if include_opt:
            for j,t in enumerate(bits):r[f'OPT-{j+1}']=o*(1-t)-6*(1-o)*t
            r['W-opt']=o-int(any(e))
        matrix.append(r)
        w=int(any(e));welfare.append(w);goal.append(2*w-o)
    return types,list(matrix[0]),matrix,goal,welfare

def solve(tau, source, include_opt):
    types,names,matrix,goal,welfare=system(tau,source,include_opt)
    rows=[[r[k] for k in names] for r in matrix]
    arr=np.array(rows,dtype=float)
    # Minimize universal factor (coefficient of actual welfare).
    sol=linprog([*np.zeros(len(names)),1],A_ub=np.column_stack((arr,-np.array(welfare))),
                b_ub=[-o for _,o in types],bounds=(0,None),method='highs')
    solution={'tau':str(tau),'forced_position':source+1,'status':sol.status,'types':len(types),'rows':len(names),'optimum_factor_float':sol.fun}
    if sol.success:
        solution['float_support']={k:float(v) for k,v in zip(names,sol.x) if v>1e-8}
        used=[j for j,v in enumerate(sol.x) if v>1e-8]
        active=np.flatnonzero(abs(sol.ineqlin.residual)<1e-8)
        def lifted(i,j):return rows[i][j] if j<len(names) else Q(-welfare[i])
        m=sp.Matrix([[lifted(i,j) for j in used] for i in active])
        pivots=m.T.rref()[1]
        if len(pivots)==len(used):
            rhs=sp.Matrix([-types[active[i]][1] for i in pivots])
            x=list(map(Q,m[list(pivots),:].inv()*rhs))
            vals=dict(zip(used,x))
            res=[vals[len(names)]*w-o-sum(vals[j]*rr[j] for j in used if j<len(names)) for (_,o),w,rr in zip(types,welfare,rows)]
            if min(x)>=0 and min(res)>=0:
                solution['factor_exact']=str(vals[len(names)])
                solution['nonzero_weights']={names[j]:str(v) for j,v in vals.items() if j<len(names)}
                solution['minimum_residual']=str(min(res))
                solution['zero_types']=sum(q==0 for q in res)
    return solution

if __name__=='__main__':
    reports=[]
    for tau in map(Q,['6','5','19/4','71/15']):
        for source in (3,2,1,0):
            ans=solve(tau,source,True);reports.append(ans)
            print(tau,source+1,ans['optimum_factor_float'],ans.get('factor_exact'),flush=True)
    Path('../branch_envelope_output.json').write_text(json.dumps(reports,indent=2)+'\n')
