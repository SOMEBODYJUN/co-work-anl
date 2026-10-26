"""Exact lifted stopping test for specified full new-reply IC families."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json,sys
import numpy as np
from scipy.optimize import linprog
import new_reply_budget as nr
from six_stress import exact_solve
HERE=Path(__file__).resolve().parent

def partition(xs):
    seen={};out=[]
    for x in xs:
        if x not in seen:seen[x]=len(seen)
        out.append(seen[x])
    return tuple(out)

P3=tuple(sorted({partition(z) for z in product(range(3),repeat=3)}))
P4=tuple(sorted({partition(z) for z in product(range(4),repeat=4)}))
EXTRA_NAMES=[('new-new',f,g,pat) for f,g,pat in product(range(2),range(2),P4)]
EXTRA_NAMES += [('new-old',f,q,pat) for f,q,pat in product(range(2),range(3),P3)]
EXTRA_NAMES += [('old-new',f,pat) for f,pat in product(range(2),P3)]
EI={name:i for i,name in enumerate(EXTRA_NAMES)}

def closure_coefficients(a,d,h):
    p=sum(a[:3]);ell=sum(a[:5]);words=[z for z,c in zip(nr.PAT,h) for _ in range(c)]
    edges=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
    group=lambda e:(e[0],int(e[1]==e[2]),words[e[1]],words[e[2]])
    counts=Counter(map(group,edges));groups=tuple(sorted(counts));gi={g:i for i,g in enumerate(groups)}
    const=[F()]*len(EXTRA_NAMES);coef=[[F()]*len(groups) for _ in EXTRA_NAMES]
    def den(e):
        f,i,j=e;return p+words[i][0]+words[j][1+f]+1
    for e in edges:
        f,i,j=e;ge=gi[group(e)];de=den(e)
        for v in edges:
            g,k,l=v;gv=gi[group(v)];row=EI['new-new',f,g,partition((i,j,k,l))]
            coef[row][ge]+=F(1,de);coef[row][gv]-=F(1,de)
        for k in range(6):
            tk,bk,ck=words[k]
            for q in range(3):
                row=EI['new-old',f,q,partition((i,j,k))]
                coef[row][ge]+=F(1,de);const[row]-=F(words[k][q],de)
            row=EI['old-new',f,partition((k,i,j))]
            const[row]+=nr.share(ck,p+tk+bk+ck);coef[row][ge]-=F(1,p+tk+bk+1)
    raw,zs=nr.row_parts(a,d,h);small=[]
    for f,diag,wi,wj in groups:
        t,b,c=wi;y=wj[1+f];delta=nr.delta((f,p,ell,t,b,y));count=counts[f,diag,wi,wj]
        small.append([count*delta.get(i,F()) for i in range(nr.NW)])
    return groups,raw,small,const,coef

def build(histcols):
    types,old=nr.old_system();ti={t:k for k,t in enumerate(types)};cols=[{'kind':'K'}];details=[]
    for c in histcols:
        a=tuple(map(int,c['actual_bits']));d=c['d'];h=tuple(c['hist'])
        groups,raw,small,const,coef=closure_coefficients(a,d,h)
        xi=len(cols);cols.append({k:v for k,v in c.items() if k!='weight'});ys=[]
        for group in groups:
            ys.append(len(cols));cols.append({'kind':'new-reply','hist_column':xi,'group':[group[0],group[1],list(group[2]),list(group[3])]})
        details.append((a,d,h,xi,ys,raw,small,const,coef))
    names=[n for n,_ in old]+nr.WP+[str(n) for n in EXTRA_NAMES]
    m=[[F()]*len(cols) for _ in names];obj=[F()]*len(cols);normal=[F()]*len(cols)
    for i,(_,row) in enumerate(old):m[i][0]=row[-1]
    m[len(old)+5+nr.CAP][0]=F(30);m[len(old)+5+nr.NF+nr.CAP][0]=F(36)
    bounds=[]
    for a,d,h,xi,ys,raw,small,const,coef in details:
        k=ti[a,d];obj[xi]=F(int(any(a)));normal[xi]=F(int(d>0))
        for i,(_,row) in enumerate(old):m[i][xi]=row[k]
        for i,v in enumerate(raw):m[len(old)+i][xi]=v
        for i,v in enumerate(const):m[len(old)+nr.NW+i][xi]=v
        for g,y in enumerate(ys):
            for i,v in enumerate(small[g]):m[len(old)+i][y]=v
            for i,row in enumerate(coef):m[len(old)+nr.NW+i][y]=row[g]
            bound=[F()]*len(cols);bound[xi]=F(1);bound[y]=-F(1);bounds.append(bound);names.append('reply-upper:'+str(y))
    m.extend(bounds)
    return cols,names,m,obj,normal

def exact_point(cols,names,m,obj,normal,solution):
    keep=[j for j,v in enumerate(solution) if v>1e-9]
    small=[[row[j] for j in keep] for row in m];vs=solution[keep]
    equations=[row+[F()] for row in small if abs(np.dot(np.array([float(x) for x in row]),vs))<1e-10*max([float(abs(x)) for x in row]+[1e-50])]
    equations.append([normal[j] for j in keep]+[F(1)])
    vals=exact_solve(equations,len(keep));full=[F()]*len(cols)
    for j,v in zip(keep,vals):full[j]=v
    assert min(full)>=0
    assert sum(x*y for x,y in zip(normal,full))==1
    slacks=[sum(x*y for x,y in zip(row,full)) for row in m]
    assert min(slacks)>=0,(names[slacks.index(min(slacks))],min(slacks))
    w=sum(x*y for x,y in zip(obj,full));assert w<F(1,2)
    for c,v in zip(cols,full):c['weight']=str(v)
    return {'scope':'exact feasible lifted necessary-condition point; not an SPE, not a game, not an exact optimum assertion','base_rows':702,'first_raw_rows':nr.NW,'additional_index_class_rows':len(EXTRA_NAMES),'O':'1','W':str(w),'strict_half_gap':str(1-2*w),'verified_rows':len(m),'minimum_slack':str(min(slacks)),'positive_columns':len(keep),'columns':cols}

def verify(report):
    hc=[c for c in report['columns'] if c['kind']=='hist'];cols,names,m,obj,normal=build(hc)
    assert all({k:v for k,v in x.items() if k!='weight'}=={k:v for k,v in y.items() if k!='weight'} for x,y in zip(cols,report['columns']))
    values=[F(c['weight']) for c in report['columns']];assert len(cols)==len(values);assert min(values)>=0
    assert sum(x*y for x,y in zip(normal,values))==1
    slacks=[sum(x*y for x,y in zip(row,values)) for row in m];assert min(slacks)>=0
    w=sum(x*y for x,y in zip(obj,values));assert w==F(report['W']);assert w<F(1,2)
    return {'verified_rows':len(m),'minimum_slack':str(min(slacks)),'W':str(w)}

def main():
    target=HERE/'full_new_reply_closure_exact.json'
    if '--verify' in sys.argv:
        print(json.dumps(verify(json.loads(target.read_text())),indent=2));return
    histcols=[c for c in json.loads((HERE/'new_reply_lift_exact.json').read_text())['columns'] if c['kind']=='hist']
    cols,names,m,obj,normal=build(histcols)
    print('full identity closure',len(m),'rows',len(cols),'columns',len(histcols),'histograms',flush=True)
    a=np.array([[float(x) for x in row] for row in m]);scale=np.max(abs(a),axis=1);scale[scale==0]=1
    sol=linprog([float(x) for x in obj],A_ub=-a/scale[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in normal]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    print(sol.message,'W',sol.fun,flush=True)
    if sol.success:
        report=exact_point(cols,names,m,obj,normal,sol.x);target.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='columns'},indent=2),flush=True)
    else:
        (HERE/'full_new_reply_closure_status.json').write_text(json.dumps({'scope':'restricted guessed histogram support only; no full-domain infeasibility claim','success':bool(sol.success),'status':sol.message,'histograms':len(histcols),'columns':len(cols),'rows':len(m)},indent=2)+'\n')

if __name__=='__main__':main()
