"""Common actual customer type marginals, each intervention on the same SPE.

A finite relaxation. Only exact nonnegative checked duals prove welfare bounds.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

anchors=list(product(product((0,1),repeat=7),(0,1)))
etas=(Q(0),Q(1,6),Q(1,5),Q(1,4),Q(1,3),Q(1,2),Q(1))

def returns(word):
    count=sum(word)
    return [Q(q,count) if count else Q(0) for q in word]

def rows(tau, word, legal, member, start):
    """Exact certified row values on a customer; all rows sum to >= 0."""
    result={}
    u=returns(word)
    p=sum(word[:4]);a=word[4];D=(p+1)*(p+2)
    for i in range(start,6):
        d=sum(word[:i])+6-i
        result[f'F{i}']=tau*u[i]-Q(member,d)
        for j,z in enumerate(legal):
            result[f'H{i}-{j}']=u[i]-Q(z,d)
    for eta in etas:
        result[f'R{eta}']=tau*u[4]+eta*u[5]-member*min(Q(1,p+1),Q(1,p+2)+eta/(p+a+1))
    result['PAIR']=u[4]+u[5]+Q(a,D)-member*(Q(2)/(tau*(p+1))-Q(1)/(tau**2*D))
    for j,z in enumerate(legal):
        result[f'MIXED{j}']=u[4]+u[5]+Q(a,D)-Q(z,p+1)-Q(member)/tau*(Q(1,p+1)-Q(z,D))
    return result

def system(tau, choices):
    from scipy.sparse import coo_matrix

    columns=[]; labels=[]; w=[]; o=[]
    for group in [None,*choices]:
        for idx,(anchor,member) in enumerate(anchors):
            e=anchor[:6]; maximum=anchor[6]
            if group is None:
                x=rows(tau,e,anchor,member,0)
                x['CAP-C']=tau*maximum-member
                x['W-opt']=member-int(any(e))
                for j,t in enumerate(anchor):
                    x[f'CAP{j}']=maximum-t
                    x[f'OPT{j}']=member*(1-t)-6*(1-member)*t
                w.append(int(any(e)));o.append(member)
                columns.append(x);labels.append((group,idx,()))
            else:
                i,q=group
                for tail in product((0,1),repeat=5-i):
                    v=e[:i]+(anchor[q],)+tail
                    x=rows(tau,v,anchor+tail,member,i+1)
                    x['IC-own']=returns(e)[i]-returns(v)[i]
                    for j,t in enumerate(tail):
                        x[f'CAP{j}']=maximum-t
                        x[f'OPT{j}']=member*(1-t)-6*(1-member)*t
                    w.append(0);o.append(0)
                    columns.append({(group,k):v for k,v in x.items()});labels.append((group,idx,tail))
    name_list=list(dict.fromkeys(k for x in columns for k in x))
    lookup={k:i for i,k in enumerate(name_list)}
    ab=[];ai=[];aj=[];eb=[];ei=[];ej=[]
    gluing={(mode,i):1+g*len(anchors)+i for g,mode in enumerate(choices) for i in range(len(anchors))}
    for j,(x,(mode,idx,tail)) in enumerate(zip(columns,labels)):
        for k,v in x.items():
            if v:
                ai.append(lookup[k]);aj.append(j);ab.append(-float(v))
        if mode:
            ei.append(gluing[mode,idx]);ej.append(j);eb.append(1.)
        else:
            if o[j]:ei.append(0);ej.append(j);eb.append(1.)
            for alt in choices:
                ei.append(gluing[alt,idx]);ej.append(j);eb.append(-1.)
    Aub=coo_matrix((ab,(ai,aj)),shape=(len(name_list),len(columns))).tocsc()
    Aeq=coo_matrix((eb,(ei,ej)),shape=(1+len(gluing),len(columns))).tocsc()
    return name_list,columns,labels,w,o,Aub,Aeq

def solve(tau,choices):
    import numpy as np
    from scipy.optimize import linprog

    n,col,labels,w,o,Aub,Aeq=system(tau,choices)
    sol=linprog(w,A_ub=Aub,b_ub=np.zeros(Aub.shape[0]),A_eq=Aeq,
                b_eq=np.r_[1,np.zeros(Aeq.shape[0]-1)],bounds=(0,None),method='highs')
    ans={'tau':str(tau),'branches':choices,'constraints':len(n),'columns':len(col),'status':sol.status,
         'min_welfare_float':sol.fun,'inverse_factor_float':1/sol.fun if sol.success else None}
    if sol.success:
        ans['row_weights']=[(k, float(-v)) for k,v in zip(n,sol.ineqlin.marginals) if -v>1e-8]
        ans['support']=[(ls,float(v)) for ls,v in zip(labels,sol.x) if v>1e-8]
    return ans

if __name__=='__main__':
    opts = [tuple((i,6) for i in range(4)),
            tuple((i,6) for i in range(4))+tuple((i,j) for i in range(4) for j in (4,5))]
    report=[]
    for tau in map(Q,['6','5','49/10','29/6']):
        for chosen in opts:
            r=solve(tau,chosen);report.append(r)
            print(tau,len(chosen),r['constraints'],r['columns'],
                  r['min_welfare_float'],r['inverse_factor_float'],flush=True)
    Path('glued_branch_probe_output.json').write_text(json.dumps(report,indent=2)+'\n')
