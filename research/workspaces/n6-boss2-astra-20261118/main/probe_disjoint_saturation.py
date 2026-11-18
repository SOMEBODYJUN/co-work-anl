"""Experimental six equal disjoint opt groups with real random-optimal branches."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from probe_glued_branches import anchors, returns, rows

def model(groups):
    catalog_names=[*range(7)]
    cols=[]; positions=[]; obj=[]; target=[]
    eq_rhs=[1.,0.]
    constraints={}
    for mode in [None,*groups]:
        for i,(a,o) in enumerate(anchors):
            e=a[:6];k=a[6]
            if mode is None:
                r=rows(Q(6),e,a,o,0)
                for j,bit in enumerate(a):
                    r[f'CAP{j}']=k-bit
                    r[f'OPT{j}']=o*(1-bit)-6*(1-o)*bit
                cols.append(r);positions.append((None,i,0,(),k,o))
                obj.append(int(any(e)));target.append(o)
                continue
            source,force=mode
            for q in (range(2) if force=='target' and o else (0,)):
                for tail in product((0,1),repeat=5-source):
                    f=a[force] if force != 'target' else q
                    v=e[:source]+(f,)+tail
                    r=rows(Q(6),v,a+tail+(f,),o,source+1)
                    r['nodeIC']=returns(e)[source]-returns(v)[source]
                    for j,bit in enumerate(tail):
                        r[f'CAP{j}']=k-bit
                        r[f'OPT{j}']=o*(1-bit)-6*(1-o)*bit
                    cols.append({(mode,name):value for name,value in r.items()})
                    positions.append((mode,i,q,tail,k,o))
                    obj.append(0);target.append(0)
    for group,i,q,_,_,_ in positions:
        if group and (group,i,q) not in constraints:
            constraints[group,i,q]=len(eq_rhs)
            eq_rhs.append(0.)
    rnames={}
    for col in cols:
        for key in col:
            rnames.setdefault(key,len(rnames))
    ai=[];aj=[];av=[];ei=[];ej=[];ev=[]
    def equality(i,j,v):
        if v:
            ei.append(i);ej.append(j);ev.append(float(v))
    for j, (col, (mode,i,q,tail,k,o)) in enumerate(zip(cols,positions)):
        for name,value in col.items():
            if value:
                ai.append(rnames[name]);aj.append(j);av.append(-float(value))
        if mode is None:
            equality(0,j,o);equality(1,j,o-6*k)
            for g in groups:
                if g[1]=='target' and o:
                    equality(constraints[g,i,1],j,Q(-1,6))
                    equality(constraints[g,i,0],j,Q(-5,6))
                else:
                    equality(constraints[g,i,0],j,-1)
        else:
            equality(constraints[mode,i,q],j,1)
    a=coo_matrix((av,(ai,aj)),shape=(len(rnames),len(cols))).tocsc()
    b=coo_matrix((ev,(ei,ej)),shape=(len(eq_rhs),len(cols))).tocsc()
    answer=linprog(obj,A_ub=a,b_ub=np.zeros(a.shape[0]),A_eq=b,b_eq=eq_rhs,bounds=(0,None),method='highs')
    return {'status':int(answer.status),'welfare_float':answer.fun,'columns':len(cols),
            'rows':len(rnames),'equality_rows':len(eq_rhs),'groups':groups}
if __name__=='__main__':
    cases=[]
    for groups in [tuple((i,'target') for i in range(4)),
                   tuple((i,'target') for i in range(4))+tuple((i,6) for i in range(4))]:
        r=model(groups);cases.append(r);print(json.dumps(r),flush=True)
    Path('../saturation-output.json').write_text(json.dumps(cases,indent=2)+'\n')
