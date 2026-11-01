"""Cross R overlaps have only positive prices; nested R events realize minima.

Add Z_e->R_f, R_e->Z_f and actual strong PAIR(R_e,R_f), in all four-index
classes. Never add Z_e->Z_f under this overlap interface.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
import json,sys
import numpy as np
from scipy.optimize import linprog
import new_reply_budget as nr
import full_new_reply_closure as cl
import actual_fifth_nested as nest
HERE=Path(__file__).resolve().parent
NAMES=[(kind,f,g,pat) for kind,f,g,pat in product(('Z-R','R-Z','pair-RR'),range(2),range(2),cl.P4)]
NI={n:i for i,n in enumerate(NAMES)}

def build(histcols):
    oldcols,onames,om,oobj,onorm=nest.build(histcols)
    cols=list(oldcols);details=[]
    histindex=None;byhist={}
    for j,c in enumerate(oldcols):
        if c['kind']=='hist':histindex=j;byhist[j]={}
        elif c['kind']=='joint-reply':
            f,diag,wi,wj=c['group'];key=(f,diag,tuple(wi),tuple(wj))
            byhist[histindex].setdefault(key,{})[tuple(c['state'])]=j
    for hi,groups in byhist.items():
        overlaps={}
        for g,h in combinations(sorted(groups),2):
            overlaps[g,h]=len(cols);cols.append({'kind':'overlap','hist_column':hi,'groups':[list(g),list(h)]})
        details.append((hi,groups,overlaps))
    nold=len(om);m=[row+[F()]*(len(cols)-len(oldcols)) for row in om]
    m += [[F()]*len(cols) for _ in NAMES];names=onames+[str(n) for n in NAMES]
    obj=oobj+[F()]*(len(cols)-len(oldcols));normal=onorm+[F()]*(len(cols)-len(oldcols))
    for hi,groups,overlaps in details:
        c=oldcols[hi];a=tuple(map(int,c['actual_bits']));h=tuple(c['hist']);p=sum(a[:3]);pa=sum(a[:4]);s=sum(a)
        D=(pa+1)*(pa+2);ha=nr.share(a[4]+a[5],s)+F(a[4],D)
        words=[z for z,n in zip(nr.PAT,h) for _ in range(n)]
        edges=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
        def group(e):return (e[0],int(e[1]==e[2]),words[e[1]],words[e[2]])
        def add_r(row,g,v):
            m[row][groups[g][1,0]]+=v;m[row][groups[g][1,1]]+=v
        def add_z(row,g,v):
            m[row][groups[g][0,1]]+=v;m[row][groups[g][1,1]]+=v
        def add_overlap(row,g,h,v):
            if g==h:add_r(row,g,v)
            else:m[row][overlaps[tuple(sorted((g,h)))]]+=v
        for e in edges:
            f,i,j=e;ge=group(e);de=p+words[i][0]+words[j][1+f]+1
            for ee in edges:
                g,k,l=ee;gg=group(ee);pat=cl.partition((i,j,k,l))
                row=nold+NI['Z-R',f,g,pat]
                add_z(row,ge,F(1,pa+1));add_r(row,gg,-F(1,pa+1))
                m[row][groups[ge][1,1]]-=F(1,D);add_overlap(row,ge,gg,F(1,D))
                row=nold+NI['R-Z',f,g,pat]
                add_r(row,ge,F(1,de));add_z(row,gg,-F(1,de))
                row=nold+NI['pair-RR',f,g,pat]
                m[row][hi]+=ha;add_r(row,ge,-F(1,pa+1));add_r(row,gg,-F(1,pa+1));add_overlap(row,ge,gg,F(1,D))
        for (g,h),j in overlaps.items():
            for source in (g,h):
                row=[F()]*len(cols);row[groups[source][1,0]]=F(1);row[groups[source][1,1]]=F(1);row[j]=-F(1)
                m.append(row);names.append('overlap-upper:'+str(j)+':'+str(source))
    return cols,names,m,obj,normal

def verify(report):
    histcols=[c for c in report['columns'] if c['kind']=='hist'];cols,names,m,obj,normal=build(histcols)
    # JSON turns nested overlap tuples into lists; canonical JSON compares them.
    assert json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in cols])==json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in report['columns']])
    vals=[F(c['weight']) for c in report['columns']];assert min(vals)>=0
    assert sum(x*y for x,y in zip(normal,vals))==1
    slacks=[sum(x*y for x,y in zip(row,vals)) for row in m];assert min(slacks)>=0
    w=sum(x*y for x,y in zip(obj,vals));assert w==F(report['W']) and w<F(1,2)
    # Overlaps affect ordinary raw rows only positively; upper-bound rows are
    # the last rows and do not enter the mathematical nonnegative raw family.
    rawrows=702+nr.NW+len(cl.EXTRA_NAMES)+len(nest.NEW_NAMES)+len(NAMES)
    # Joint-state bounds were placed before the additional raw rows, so check
    # every row except explicitly named overlap upper bounds instead.
    for j,c in enumerate(cols):
        if c['kind']=='overlap':
            assert all(row[j]>=0 for name,row in zip(names,m) if not name.startswith('overlap-upper:'))
    return {'verified_rows':len(m),'minimum_slack':str(min(slacks)),'W':str(w),'positive_overlap_sign_check':True}

def main():
    target=HERE/'attractive_nested_exact.json'
    if '--verify' in sys.argv:
        print(json.dumps(verify(json.loads(target.read_text())),indent=2));return
    histcols=[c for c in json.loads((HERE/'actual_fifth_nested_exact.json').read_text())['columns'] if c['kind']=='hist']
    cols,names,m,obj,normal=build(histcols)
    print('attractive cross replies',len(m),'rows',len(cols),'columns',flush=True)
    a=np.array([[float(x) for x in row] for row in m]);scale=np.max(abs(a),axis=1);scale[scale==0]=1
    sol=linprog([float(x) for x in obj],A_ub=-a/scale[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in normal]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    print(sol.message,'W',sol.fun,flush=True)
    if sol.success and sol.fun<.5:
        report=cl.exact_point(cols,names,m,obj,normal,sol.x)
        report['additional_nested_rows']=len(nest.NEW_NAMES);report['additional_attractive_rows']=len(NAMES)
        report['scope']='exact feasible nested-overlap lifted necessary point, not SPE or exact optimum'
        target.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='columns'},indent=2),flush=True)
    else:
        (HERE/'attractive_nested_status.json').write_text(json.dumps({'scope':'restricted 16 histogram support only','status':sol.message,'success':bool(sol.success),'W':sol.fun,'rows':len(m),'columns':len(cols)},indent=2)+'\n')

if __name__=='__main__':main()
