"""Actual fifth re-queries every new R; preserve (R,Z) as four joint states."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys
import numpy as np
from scipy.optimize import linprog
import new_reply_budget as nr
import full_new_reply_closure as cl

HERE=Path(__file__).resolve().parent
STATES=((0,1),(1,0),(1,1))
BASIC=('source','pair','price','capacity')+tuple('actual'+str(k) for k in range(6))+('ownR','reverseR')
NEW_NAMES=[('basic',f,q) for f,q in product(range(2),BASIC)]
NEW_NAMES += [('Z-old',f,q,pat) for f,q,pat in product(range(2),range(3),cl.P3)]
NEW_NAMES += [('old-Z',f,pat) for f,pat in product(range(2),cl.P3)]
NI={k:i for i,k in enumerate(NEW_NAMES)}

def values(a,h):
    p=sum(a[:3]);pa=sum(a[:4]);ell=sum(a[:5]);s=sum(a)
    u5=nr.share(a[4],s);u6=nr.share(a[5],s)
    ha=nr.share(a[4]+a[5],s)+F(a[4],(pa+1)*(pa+2))
    words=[z for z,c in zip(nr.PAT,h) for _ in range(c)]
    edges=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
    group=lambda e:(e[0],int(e[1]==e[2]),words[e[1]],words[e[2]])
    groups=sorted(set(map(group,edges)));gi={g:i for i,g in enumerate(groups)}
    raw=[[F()]*(1+3*len(groups)) for _ in NEW_NAMES]
    for e in edges:
        f,i,j=e;ge=gi[group(e)];de=p+words[i][0]+words[j][1+f]+1
        def term(r,z):
            vz=nr.share(z,pa+r+z)
            basic=(u5-nr.share(r,pa+r+z),ha-F(r+z,pa+1)+F(r*z,(pa+1)*(pa+2)),u6-F(z,ell+1),-F(z))
            basic += tuple(vz-F(a[k],pa+r+1) for k in range(6))
            basic += (vz-F(r,pa+r+1),F(r-z,de))
            result={NI['basic',f,q]:v for q,v in zip(BASIC,basic)}
            for k,(tk,bk,ck) in enumerate(words):
                for q in range(3):
                    row=NI['Z-old',f,q,cl.partition((i,j,k))]
                    result[row]=result.get(row,F())+vz-F(words[k][q],pa+r+1)
                row=NI['old-Z',f,cl.partition((k,i,j))]
                result[row]=result.get(row,F())+nr.share(ck,p+tk+bk+ck)-F(z,p+tk+bk+1)
            return result
        zero=term(0,0)
        for row,v in zero.items():raw[row][0]+=v
        for si,(r,z) in enumerate(STATES):
            vv=term(r,z)
            for row,v in vv.items():raw[row][1+3*ge+si]+=v-zero.get(row,F())
    return groups,raw

def build(histcols):
    basecols,bnames,bm,bobj,bnorm=cl.build(histcols)
    # Old reply bounds are replaced with the complete four-state bound.
    nbase=702+nr.NW+len(cl.EXTRA_NAMES);bm=bm[:nbase];bnames=bnames[:nbase]
    cols=[];mapping={};newgroups={}
    for j,c in enumerate(basecols):
        if c['kind']=='new-reply':
            ids=[]
            for r,z in STATES:
                ids.append(len(cols));cols.append({'kind':'joint-reply','hist_column_old':c['hist_column'],'group':c['group'],'state':[r,z]})
            mapping[j]=[(ids[1],F(1)),(ids[2],F(1))];newgroups[j]=ids
        else:
            mapping[j]=[(len(cols),F(1))];cols.append(c)
    m=[[F()]*len(cols) for _ in range(nbase+len(NEW_NAMES))];names=bnames+[str(n) for n in NEW_NAMES]
    obj=[F()]*len(cols);normal=[F()]*len(cols)
    for j in range(len(basecols)):
        for jj,c in mapping[j]:
            obj[jj]=c*bobj[j];normal[jj]=c*bnorm[j]
            for i,row in enumerate(bm):m[i][jj]=c*row[j]
    m[nbase+NI['basic',0,'capacity']][0]=F(30);m[nbase+NI['basic',1,'capacity']][0]=F(36)
    bounds=[]
    for j,c in enumerate(basecols):
        if c['kind']!='hist':continue
        a=tuple(map(int,c['actual_bits']));h=tuple(c['hist']);groups,raw=values(a,h)
        xi=mapping[j][0][0]
        ys=[k for k,z in enumerate(basecols) if z['kind']=='new-reply' and z['hist_column']==j]
        assert len(ys)==len(groups)
        for i,row in enumerate(raw):m[nbase+i][xi]=row[0]
        for g,oldy in enumerate(ys):
            assert basecols[oldy]['group']==[groups[g][0],groups[g][1],list(groups[g][2]),list(groups[g][3])]
            ids=newgroups[oldy]
            for si,yy in enumerate(ids):
                for i,row in enumerate(raw):m[nbase+i][yy]=row[1+3*g+si]
            bound=[F()]*len(cols);bound[xi]=F(1)
            for yy in ids:bound[yy]=-F(1)
            bounds.append(bound);names.append('joint-state-upper:'+str(oldy))
    m.extend(bounds)
    return cols,names,m,obj,normal

def main():
    if '--verify' in sys.argv:
        report=json.loads((HERE/'actual_fifth_nested_exact.json').read_text())
        histcols=[c for c in report['columns'] if c['kind']=='hist']
        cols,names,m,obj,normal=build(histcols)
        assert len(cols)==len(report['columns'])
        assert all({k:v for k,v in x.items() if k!='weight'}=={k:v for k,v in y.items() if k!='weight'} for x,y in zip(cols,report['columns']))
        vals=[F(c['weight']) for c in report['columns']]
        assert min(vals)>=0 and sum(x*y for x,y in zip(normal,vals))==1
        slacks=[sum(x*y for x,y in zip(row,vals)) for row in m]
        assert min(slacks)>=0
        w=sum(x*y for x,y in zip(obj,vals));assert w==F(report['W']) and w<F(1,2)
        print(json.dumps({'verified_rows':len(m),'minimum_slack':str(min(slacks)),'W':str(w)},indent=2));return
    histcols=[c for c in json.loads((HERE/'full_new_reply_closure_exact.json').read_text())['columns'] if c['kind']=='hist']
    cols,names,m,obj,normal=build(histcols)
    print('nested actual-fifth',len(m),'rows',len(cols),'columns',flush=True)
    a=np.array([[float(x) for x in row] for row in m]);scale=np.max(abs(a),axis=1);scale[scale==0]=1
    sol=linprog([float(x) for x in obj],A_ub=-a/scale[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in normal]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    print(sol.message,'W',sol.fun,flush=True)
    if sol.success and sol.fun<.5:
        report=cl.exact_point(cols,names,m,obj,normal,sol.x)
        report['additional_nested_rows']=len(NEW_NAMES);report['scope']='exact feasible joint-four-state lifted necessary point, not SPE or exact optimum'
        (HERE/'actual_fifth_nested_exact.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='columns'},indent=2),flush=True)
    else:
        (HERE/'actual_fifth_nested_status.json').write_text(json.dumps({'scope':'restricted 16 histogram support; no full-domain claim','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols)},indent=2)+'\n')

if __name__=='__main__':main()
