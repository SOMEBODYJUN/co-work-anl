#!/usr/bin/env python3
"""Exact refinement of R_m^PC by true copy-deviation follower information."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from functools import lru_cache
import json
import sys

from six_stress import make_system,exact_solve


def add_query_family(rows,types,m,prefix,source,psi,kcoef,ucoefs=()):
    def u(a,i):return F(a[i],sum(a)) if a[i] else F(0)
    def base(a):return u(a,source)+sum(v*u(a,i) for i,v in ucoefs)
    def add(name,fn):rows.append((name,[fn(a,d) for a,d in types]+[F(kcoef)]))
    for ti in range(m):
        for qi in range(m):
            add(f'{prefix}:A{ti+1}:A{qi+1}',lambda a,d,ti=ti,qi=qi:base(a)-psi(a,a[ti],a[qi]))
        add(f'{prefix}:A{ti+1}:Tavg',lambda a,d,ti=ti:base(a)-sum(F(d if q else m-d,m)*psi(a,a[ti],q) for q in range(2)))
        add(f'{prefix}:Tavg:A{ti+1}',lambda a,d,ti=ti:base(a)-sum(F(d if t else m-d,m)*psi(a,t,a[ti]) for t in range(2)))
    add(f'{prefix}:Tdiag',lambda a,d:base(a)-F(d,m)*psi(a,1,1)-F(m-d,m)*psi(a,0,0))
    def off(a,d):
        weights={(1,1):d*(d-1),(1,0):d*(m-d),(0,1):d*(m-d),(0,0):(m-d)*(m-d-1)}
        return base(a)-sum(F(v,m*(m-1))*psi(a,t,q) for (t,q),v in weights.items())
    add(f'{prefix}:Toffdiag',off)


def bridge_system(m=6):
    types,rows=make_system(m,priced=True)
    def psi(a,t,q):
        b=sum(a[:-2])
        return (F(t,b+t) if t else F(0))+F(q,b+t+1)
    add_query_family(rows,types,m,'capacitybridge',m-2,psi,1)
    return types,rows


def atoms(a,d,m,theme):
    if isinstance(theme,int):return [(F(1),a[theme])]
    return [(F(m-d,m),0),(F(d,m),1)]


def query_member(a,d,m,theme,query,t):
    if isinstance(query,int):return F(a[query])
    if query=='avg':return F(d,m)
    if query=='own':return F(t)
    if query=='other':return F(d-t,m-1)
    raise ValueError(query)


def parametric_row(types,m,cut):
    theme=cut['theme'];query=cut['query']
    alpha,beta,gamma=(F(cut[k]) for k in ('alpha','beta','gamma'))
    def coef(a,d):
        b=sum(a[:-2]);ell=sum(a[:-1]);s=sum(a)
        lhs=F(a[-2],s) if a[-2] else F(0)
        if a[-1]:lhs+=alpha*F(1,s)
        credit=F(0)
        for prob,t in atoms(a,d,m,theme):
            if not prob:continue
            q=query_member(a,d,m,theme,query,t)
            base=F(t,b+t) if t else F(0)
            v0=base+gamma*F(q,b+t+1)
            v1=F(t,b+t+1)+beta+F(alpha,ell+1)-gamma*F(1-q,b+t+1)
            credit+=prob*min(v0,v1)
        return lhs-credit
    name='freecopy:'+json.dumps(cut,separators=(',',':'),sort_keys=True)
    return name,[coef(a,d) for a,d in types]+[beta]


def separate_free_copy(types,m,n):
    """Optimize all nonnegative price/cap/follower-IC weights at this point.

    One true follower reply R is retained per forced T, simultaneously checked
    against every actual query and every available optimal-index query class.
    Returns only exact, verified negative cuts; float separation is not proof.
    """
    import numpy as np
    from scipy.optimize import linprog
    u5=sum(F(a[-2],sum(a))*v for (a,d),v in zip(types,n[:-1]) if a[-2])
    u6=sum(F(a[-1],sum(a))*v for (a,d),v in zip(types,n[:-1]) if a[-1])
    K=n[-1];cuts=[];diagnostics=[];witnesses=[]
    for theme in list(range(m))+['opt']:
        groups=[]
        for (a,d),v in zip(types,n[:-1]):
            if not v:continue
            for prob,t in atoms(a,d,m,theme):
                if prob:groups.append((a,d,t,v*prob))
        queries=list(range(m))+(['avg'] if isinstance(theme,int) else ['own','other'])
        qvalues={query:sum(mass*query_member(a,d,m,theme,query,t)/F(sum(a[:-2])+t+1) for a,d,t,mass in groups) for query in queries}
        query=max(queries,key=lambda q:qvalues[q]);require=qvalues[query]
        price=[F(1,sum(a[:-1])+1) for a,d,t,mass in groups]
        follower=[F(1,sum(a[:-2])+t+1) for a,d,t,mass in groups]
        discount=[F(t,(sum(a[:-2])+t)*(sum(a[:-2])+t+1)) if t else F(0) for a,d,t,mass in groups]
        base=sum(mass*F(t,sum(a[:-2])+t) for a,d,t,mass in groups if t)
        sol=linprog([-float(c) for c in discount],A_ub=[[float(c) for c in price],[1.]*len(groups),[-float(c) for c in follower]],b_ub=[float(u6),float(K),-float(require)],bounds=[(0,float(mass)) for a,d,t,mass in groups],method='highs')
        assert sol.success,sol.message
        gap=float(base)+sol.fun-float(u5)
        diagnostics.append({'theme':theme,'query':query,'minimum_gain_float':gap})
        if gap>1e-8:
            params=[F(float(-x)).limit_denominator(1000000) for x in sol.ineqlin.marginals]
            assert min(params)>=0
            cut={'theme':theme,'query':query,'alpha':str(params[0]),'beta':str(params[1]),'gamma':str(params[2])}
            name,row=parametric_row(types,m,cut)
            slack=sum(x*y for x,y in zip(row,n))
            assert slack<0,(gap,cut,slack)
            cut['separation_slack']=str(slack)
            cuts.append(cut)
        else:
            # Reconstruct an exact feasible reply at the current customer
            # point, rather than accepting a floating "no violated cut".
            support=[j for j,x in enumerate(sol.x) if x>1e-8]
            eqs=[]
            for coeff,bound in [(price,u6),([F(1)]*len(groups),K),(follower,require)]:
                if abs(sum(float(c)*x for c,x in zip(coeff,sol.x))-float(bound))<1e-8:
                    eqs.append([coeff[j] for j in support]+[bound])
            for j in support:
                if abs(sol.x[j]-float(groups[j][3]))<1e-8:
                    eqs.append([F(int(i==j)) for i in support]+[groups[j][3]])
            exact=exact_solve(eqs,len(support)) if support else []
            z=[F(0)]*len(groups)
            for j,v in zip(support,exact):z[j]=v
            assert all(0<=v<=group[3] for group,v in zip(groups,z))
            assert sum(c*v for c,v in zip(price,z))<=u6
            assert sum(z)<=K
            assert sum(c*v for c,v in zip(follower,z))>=require
            assert base-sum(c*v for c,v in zip(discount,z))<=u5
            witnesses.append({'theme':theme,'groups':[{'actual_bits':''.join(map(str,a)),'d':d,'t':t,'mass':str(mass),'reply_mass':str(v)} for (a,d,t,mass),v in zip(groups,z)]})
    return cuts,diagnostics,witnesses


def verify_reply_closure(result,types,witnesses):
    m=result['m'];n=decode(result,types)
    u5=sum(F(a[-2],sum(a))*v for (a,d),v in zip(types,n[:-1]) if a[-2])
    u6=sum(F(a[-1],sum(a))*v for (a,d),v in zip(types,n[:-1]) if a[-1])
    K=n[-1]
    assert {w['theme'] for w in witnesses}==set(range(m))|{'opt'}
    for witness in witnesses:
        theme=witness['theme']
        groups=[(a,d,t,v*prob) for (a,d),v in zip(types,n[:-1]) if v for prob,t in atoms(a,d,m,theme) if prob]
        raw=witness['groups']
        assert len(raw)==len(groups)
        z=[]
        for (a,d,t,mass),r in zip(groups,raw):
            assert (r['actual_bits'],r['d'],r['t'],F(r['mass']))==(''.join(map(str,a)),d,t,mass)
            value=F(r['reply_mass']);assert 0<=value<=mass
            z.append(value)
        assert sum(z)<=K
        assert sum(v/F(sum(a[:-1])+1) for (a,d,t,mass),v in zip(groups,z))<=u6
        leader=sum(mass*F(t,sum(a[:-2])+t) for a,d,t,mass in groups if t)
        leader-=sum(v*F(t,(sum(a[:-2])+t)*(sum(a[:-2])+t+1)) for (a,d,t,mass),v in zip(groups,z) if t)
        assert leader<=u5
        follower=sum(v/F(sum(a[:-2])+t+1) for (a,d,t,mass),v in zip(groups,z))
        queries=list(range(m))+(['avg'] if isinstance(theme,int) else ['own','other'])
        for query in queries:
            target=sum(mass*query_member(a,d,m,theme,query,t)/F(sum(a[:-2])+t+1) for a,d,t,mass in groups)
            assert follower>=target


def solve_exact_system(m,types,rows):
    import numpy as np
    from scipy.optimize import linprog
    w=[int(any(a)) for a,d in types]+[0]
    o=[int(d>0) for a,d in types]+[0]
    mat=np.array([[float(v) for v in row] for name,row in rows])
    sol=linprog(w,A_ub=-mat,b_ub=np.zeros(len(rows)),A_eq=[o],b_eq=[1],bounds=(0,None),method='highs')
    assert sol.success,sol.message
    support=[j for j,x in enumerate(sol.x) if x>1e-8]
    eqs=[[row[j] for j in support]+[F(0)] for name,row in rows if abs(float(np.dot([float(c) for c in row],sol.x)))<1e-8]
    eqs += [[F(o[j]) for j in support]+[F(1)]]
    exact=exact_solve(eqs,len(support))
    n=[F(0)]*len(sol.x)
    for j,v in zip(support,exact):n[j]=v
    assert min(n)>=0
    assert sum(F(x)*y for x,y in zip(o,n))==1
    value=sum(F(x)*y for x,y in zip(w,n))
    slacks={name:sum(c*x for c,x in zip(row,n)) for name,row in rows}
    assert min(slacks.values())>=0
    dsupport=[i for i,x in enumerate(sol.ineqlin.marginals) if x < -1e-8]
    eqs=[[rows[i][1][j] for i in dsupport]+[F(o[j]),F(w[j])] for j in support]
    dual=exact_solve(eqs,len(dsupport)+1)
    assert all(x>=0 for x in dual[:-1]) and dual[-1]==value
    residual=[F(w[j])-dual[-1]*o[j]-sum(v*rows[i][1][j] for i,v in zip(dsupport,dual)) for j in range(len(n))]
    assert min(residual)>=0
    result={'m':m,'n_types':len(types),'n_rows':len(rows),'W':str(value),'O':'1','K':str(n[-1]),'support':[{'actual_bits':''.join(map(str,a)),'d':d,'weight':str(n[j])} for j,(a,d) in enumerate(types) if n[j]],'min_slack':str(min(slacks.values())),'dual':{rows[i][0]:str(v) for i,v in zip(dsupport,dual)},'dual_nu':str(dual[-1]),'dual_min_residual':str(min(residual))}
    return result,n


def decode(result,types):
    lookup={(a,d):i for i,(a,d) in enumerate(types)}
    n=[F(0)]*(len(types)+1)
    for s in result['support']:n[lookup[(tuple(map(int,s['actual_bits'])),s['d'])]]=F(s['weight'])
    n[-1]=F(result['K'])
    return n


def verify(result,types,rows):
    n=decode(result,types)
    w=[int(any(a)) for a,d in types]+[0]
    o=[int(d>0) for a,d in types]+[0]
    assert min(n)>=0
    assert sum(F(x)*y for x,y in zip(o,n))==1
    assert sum(F(x)*y for x,y in zip(w,n))==F(result['W'])
    for name,row in rows:assert sum(x*y for x,y in zip(row,n))>=0,name
    nu=F(result['dual_nu']);dual={name:F(x) for name,x in result['dual'].items()}
    assert all(x>=0 for x in dual.values()) and nu==F(result['W'])
    assert set(dual)<=set(name for name,row in rows)
    for j in range(len(n)):
        assert F(w[j])-nu*o[j]-sum(dual.get(name,0)*row[j] for name,row in rows)>=0,j


if __name__=='__main__':
    target=Path(__file__).with_name('six_copy_refine_results.json')
    types,rows=bridge_system()
    old=json.loads(Path(__file__).with_name('six_stress_results.json').read_text())['relaxations'][-1]
    oldn=decode(old,types)
    oldslacks={name:sum(x*y for x,y in zip(row,oldn)) for name,row in rows if name.startswith('capacitybridge')}
    assert oldslacks['capacitybridge:A6:Tavg']<0
    if '--free-cuts' in sys.argv:
        freepath=Path(__file__).with_name('six_copy_free_results.json')
        if '--verify' in sys.argv:
            data=json.loads(freepath.read_text())
            for cut in data['cuts']:
                raw={k:v for k,v in cut.items() if k!='separation_slack'}
                rows.append(parametric_row(types,6,raw))
            verify(data['final'],types,rows)
            assert data['reply_closure_witnesses']
            verify_reply_closure(data['final'],types,data['reply_closure_witnesses'])
            print('EXACT VERIFIED FREE COPY',data['final']['W'],len(rows),'rows',len(data['cuts']),'new cuts')
        else:
            records=[];allcuts=[]
            for step in range(13):
                result,n=solve_exact_system(6,types,rows)
                cuts,diagnostics,witnesses=separate_free_copy(types,6,n)
                records.append({'step':step,'W':result['W'],'n_rows':len(rows),'n_cuts':len(cuts),'diagnostics':diagnostics})
                print('FREE COPY',step,result['W'],float(F(result['W'])),len(cuts),'cuts')
                if not cuts or step==12:break
                for cut in cuts:
                    raw={k:v for k,v in cut.items() if k!='separation_slack'}
                    name,row=parametric_row(types,6,raw)
                    assert name not in {name for name,row in rows}
                    rows.append((name,row));allcuts.append(cut)
            closure=witnesses if not cuts else []
            if closure:verify_reply_closure(result,types,closure)
            freepath.write_text(json.dumps({'cuts':allcuts,'rounds':records,'final':result,'reply_closure_witnesses':closure},indent=2)+'\n')
    elif '--verify' in sys.argv:
        result=json.loads(target.read_text())
        verify(result,types,rows)
        assert result['old_bad_point_bridge_slack']==str(oldslacks['capacitybridge:A6:Tavg'])
        print('EXACT VERIFIED',result['W'],result['n_types'],'types',result['n_rows'],'rows')
    else:
        result,n=solve_exact_system(6,types,rows)
        result['old_bad_point_bridge_slack']=str(oldslacks['capacitybridge:A6:Tavg'])
        target.write_text(json.dumps(result,indent=2)+'\n')
        print('NEW EXACT BOUND',result['W'],float(F(result['W'])),result['n_rows'],'rows')
        print('OLD POINT SLACK',result['old_bad_point_bridge_slack'])
        print('DUAL',result['dual'])
