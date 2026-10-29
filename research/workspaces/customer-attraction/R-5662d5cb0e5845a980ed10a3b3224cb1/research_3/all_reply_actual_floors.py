"""Actual-prefix safety floors for every new indexed R/Z label.

All rows are necessary SPE conditions. Finite fixed-support LP points are not SPE.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
SIB=HERE.parent/'research_5'
sys.path.insert(0,str(SIB))
import cross_source_graph as cross

GROUPS=((0,0),(1,0),(1,1))
KEYS=tuple((i,member,f,diag) for i in range(6) for member in range(2) for f,diag in GROUPS)
PAT=tuple(product((0,1),repeat=3))

def added_rows(cols):
    out=[[F()]*len(cols) for _ in KEYS]
    hi=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':
            hi=c;a=tuple(map(int,c['actual_bits']));whole=sum(a)
            for row,(i,member,f,diag) in zip(out,KEYS):
                row[j]=(6 if diag else 30)*(F(a[i],whole) if a[i] else F())
        elif c['kind']=='joint-reply':
            f,diag,wi,wj=c['group']
            ni=hi['hist'][PAT.index(tuple(wi))];nj=hi['hist'][PAT.index(tuple(wj))]
            multiplicity=ni if diag else ni*nj-(ni if wi==wj else 0)
            a=tuple(map(int,hi['actual_bits']))
            for row,(i,member,ff,dd) in zip(out,KEYS):
                if (ff,dd)==(f,diag):
                    row[j]=-F(multiplicity*c['state'][member],sum(a[:i])+6-i)
    return out

def build():
    cols,names,m,obj,norm=cross.build()
    names=names+['new-reply-floor:'+str(k) for k in KEYS];m=m+added_rows(cols)
    if '--old-query-cuts' in sys.argv:
        import old_query_reply_cuts as oq
        cuts=json.loads((HERE/'old_query_cuts.json').read_text())['selected']
        for c in cuts:
            names.append('old-query-reply-priced:'+str(c['cut']));m.append(oq.row(cols,c['cut']))
    if '--mixed-pair' in sys.argv:
        import mixed_pair_reply_rows as mp
        names.extend('mixed-new-old-pair:'+str(k) for k in mp.KEYS);m.extend(mp.rows(cols))
    return cols,names,m,obj,norm

def check_old():
    point=json.loads((SIB/'cross_source_priced_optimum_exact.json').read_text())
    cols=point['columns'];ys=[F(c['weight']) for c in cols]
    slacks=[sum(v*y for v,y in zip(row,ys)) for row in added_rows(cols)]
    print(json.dumps({'scope':'new 36 floor rows only on prior necessary point',
        'negative_rows':{str(k):str(v) for k,v in zip(KEYS,slacks) if v<0}},indent=2))

def main():
    if '--check-old' in sys.argv:check_old();return
    tag='all_reply_query_cuts' if '--old-query-cuts' in sys.argv else 'all_reply_floors'
    if '--mixed-pair' in sys.argv:tag='all_reply_mixed_pair'
    start=time.time();cols,names,m,obj,norm=build()
    print('built',len(m),'rows',len(cols),'cols',time.time()-start,flush=True)
    if '--verify' in sys.argv:
        d=json.loads((HERE/(tag+'_exact.json')).read_text());ys=[F(c['weight']) for c in d['columns']]
        assert len(ys)==len(cols) and min(ys)>=0
        assert sum(v*y for v,y in zip(norm,ys))==1
        slacks=[sum(v*y for v,y in zip(row,ys)) for row in m]
        w=sum(v*y for v,y in zip(obj,ys))
        assert min(slacks)>=0 and w==F(d['W']) and w<F(1,2)
        print(json.dumps({'rows':len(m),'min_slack':str(min(slacks)),'W':str(w)},indent=2));return
    a=np.array([[float(x) for x in row] for row in m]);sc=np.max(abs(a),axis=1);sc[sc==0]=1
    sol=linprog([float(x) for x in obj],A_ub=-a/sc[:,None],b_ub=np.zeros(len(m)),A_eq=[[float(x) for x in norm]],b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    report={'scope':'fixed 16-histogram support necessary graph, not SPE or full-domain bound','success':bool(sol.success),'status':sol.message,'W':sol.fun,'rows':len(m),'columns':len(cols),'seconds':time.time()-start}
    print(json.dumps(report,indent=2),flush=True)
    if sol.success and sol.fun<.5:
        exact=cross.cl.exact_point(cols,names,m,obj,norm,sol.x)
        exact['scope']='exact necessary graph point with all 36 new R/Z actual-prefix floors; not SPE or game'
        exact['additional_new_reply_floors']=len(KEYS)
        (HERE/(tag+'_exact.json')).write_text(json.dumps(exact,indent=2)+'\n')
        report['exact_verified']=True
    (HERE/(tag+'_status.json')).write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
